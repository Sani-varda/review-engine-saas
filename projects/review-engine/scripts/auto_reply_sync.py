import asyncio
import httpx
import os
from sqlalchemy import create_url
from sqlalchemy.orm import Session
import sys

# Add backend path to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../projects/review-engine/src/backend'))

import models, database
from routers.google_business import refresh_access_token
from lib.ai_service import generate_review_reply

async def sync_and_reply():
    print("🚀 Starting Review Sync & AI Auto-Reply Cycle...")
    db = next(database.get_db())
    
    # 1. Fetch all connected businesses
    businesses = db.query(models.Business).filter(models.Business.google_connected == True).all()
    
    for business in businesses:
        if not business.google_refresh_token or not business.google_location_id:
            continue
            
        print(f"📊 Processing {business.name}...")
        
        try:
            access_token = await refresh_access_token(business.google_refresh_token)
            
            # Fetch reviews
            url = f"https://mybusiness.googleapis.com/v4/{business.google_location_id}/reviews"
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, headers={"Authorization": f"Bearer {access_token}"})
                
                if resp.status_code != 200:
                    print(f"❌ Failed to fetch reviews for {business.name}: {resp.text}")
                    continue
                
                reviews = resp.json().get("reviews", [])
                
                for r in reviews:
                    review_id = r["reviewId"]
                    comment = r.get("comment", "")
                    rating_str = r.get("starRating", "FIVE")
                    rating = 5 if rating_str == "FIVE" else 4 if rating_str == "FOUR" else 3 if rating_str == "THREE" else 2 if rating_str == "TWO" else 1
                    
                    # Check if already replied
                    if r.get("reviewReply"):
                        continue
                        
                    # Auto-reply logic (e.g. only for 4-5 stars)
                    if rating >= 4:
                        print(f"🤖 Generating AI reply for review by {r['reviewer']['displayName']}...")
                        ai_reply = await generate_review_reply(comment, business.name, rating)
                        
                        if ai_reply:
                            # Post reply
                            reply_url = f"https://mybusiness.googleapis.com/v4/{business.google_location_id}/reviews/{review_id}/reply"
                            reply_resp = await client.put(
                                reply_url,
                                headers={"Authorization": f"Bearer {access_token}"},
                                json={"comment": ai_reply}
                            )
                            
                            if reply_resp.status_code == 200:
                                print(f"✅ Auto-replied to {r['reviewer']['displayName']}")
                            else:
                                print(f"❌ Failed to post reply: {reply_resp.text}")
                                
        except Exception as e:
            print(f"❌ Error processing {business.name}: {e}")

if __name__ == "__main__":
    asyncio.run(sync_and_reply())
