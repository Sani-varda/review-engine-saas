from database import SessionLocal
import models
import httpx
import os
from lib.ai_service import generate_review_reply
from datetime import datetime

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

async def refresh_access_token(refresh_token: str) -> str:
    async with httpx.AsyncClient() as client:
        r = await client.post("https://oauth2.googleapis.com/token", data={
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        })
        if r.status_code != 200:
            raise Exception(f"Failed to refresh token: {r.text}")
        return r.json()["access_token"]

async def sync_and_reply():
    """Fetches new Google reviews for all connected businesses and auto-replies."""
    db = SessionLocal()
    try:
        businesses = db.query(models.Business).filter(
            models.Business.google_connected == True,
            models.Business.auto_reply_enabled == True,
            models.Business.google_refresh_token != None,
            models.Business.google_location_id != None
        ).all()
        
        print(f"🔄 Auto-reply sync: checking {len(businesses)} businesses...")
        
        for business in businesses:
            try:
                access_token = await refresh_access_token(business.google_refresh_token)
                async with httpx.AsyncClient() as client:
                    # Google Location ID is usually in format accounts/{acc}/locations/{loc}
                    url = f"https://mybusiness.googleapis.com/v4/{business.google_location_id}/reviews"
                    resp = await client.get(url, headers={"Authorization": f"Bearer {access_token}"})
                    
                    if resp.status_code != 200:
                        print(f"❌ Failed to fetch reviews for {business.name}: {resp.text}")
                        continue
                        
                    reviews = resp.json().get("reviews", [])
                    
                    for review in reviews:
                        # Skip if already replied on Google
                        if review.get("reviewReply"):
                            continue
                            
                        review_id = review.get("reviewId") or review.get("name", "").split("/")[-1]
                        
                        # Check local DB status
                        existing = db.query(models.GoogleReview).filter(
                            models.GoogleReview.id == review_id
                        ).first()
                        
                        if existing and existing.status == "REPLIED":
                            continue
                            
                        # Generate AI reply
                        star_map = {"FIVE": 5, "FOUR": 4, "THREE": 3, "TWO": 2, "ONE": 1}
                        star_rating = star_map.get(review.get("starRating", "FIVE"), 5)
                        comment = review.get("comment", "")
                        
                        # Only auto-reply to high ratings (4-5) as per typical SaaS default
                        if star_rating >= 4:
                            print(f"🤖 Generating AI reply for {business.name} review ID: {review_id}")
                            ai_reply = await generate_review_reply(comment, business.name, star_rating)
                            
                            if not ai_reply:
                                continue
                                
                            # Post reply to Google
                            reply_url = f"https://mybusiness.googleapis.com/v4/{business.google_location_id}/reviews/{review_id}/reply"
                            async with httpx.AsyncClient() as client:
                                post_resp = await client.put(
                                    reply_url,
                                    headers={"Authorization": f"Bearer {access_token}"},
                                    json={"comment": ai_reply}
                                )
                                
                                if post_resp.status_code == 200:
                                    # Save to DB
                                    if not existing:
                                        # Use createTime from Google if present
                                        create_time_raw = review.get("createTime")
                                        try:
                                            create_time = datetime.fromisoformat(create_time_raw.replace('Z', '+00:00')) if create_time_raw else datetime.utcnow()
                                        except:
                                            create_time = datetime.utcnow()
                                            
                                        new_review = models.GoogleReview(
                                            id=review_id,
                                            business_id=business.id,
                                            reviewer_name=review.get("reviewer", {}).get("displayName", "Anonymous"),
                                            star_rating=star_rating,
                                            comment=comment,
                                            reply_text=ai_reply,
                                            status="REPLIED",
                                            create_time=create_time,
                                            update_time=datetime.utcnow()
                                        )
                                        db.add(new_review)
                                    else:
                                        existing.reply_text = ai_reply
                                        existing.status = "REPLIED"
                                        existing.update_time = datetime.utcnow()
                                    
                                    db.commit()
                                    print(f"✅ Auto-replied to review {review_id}")
                                else:
                                    print(f"❌ Failed to post reply to Google: {post_resp.text}")
            except Exception as e:
                print(f"❌ Error processing business {business.name}: {e}")
    finally:
        db.close()
