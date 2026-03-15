from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import models, database, auth
import httpx
import os
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from lib.ai_service import generate_review_reply

router = APIRouter(prefix="/google", tags=["google_business"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

class GoogleConnectionStatus(BaseModel):
    connected: bool
    business_name: str | None = None

async def refresh_access_token(refresh_token: str) -> str:
    """Helper to get a new access token using the refresh token."""
    async with httpx.AsyncClient() as client:
        r = await client.post("https://oauth2.googleapis.com/token", data={
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        })
        if r.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to refresh access token")
        return r.json()["access_token"]

@router.get("/auth-url")
def get_auth_url(business_id: int, current_user: models.User = Depends(auth.get_current_user)):
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Google OAuth configuration missing")
    
    scopes = [
        "https://www.googleapis.com/auth/business.manage",
        "openid",
        "email",
        "profile"
    ]
    scope_str = " ".join(scopes)
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={GOOGLE_REDIRECT_URI}&"
        f"response_type=code&"
        f"scope={scope_str}&"
        f"access_type=offline&"
        f"prompt=consent&"
        f"state={business_id}"
    )
    return {"url": auth_url}

@router.post("/callback")
async def google_callback(code: str, business_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Exchange code for tokens
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
    
    if token_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to exchange token")
    
    tokens = token_response.json()
    refresh_token = tokens.get("refresh_token")
    access_token = tokens.get("access_token")

    # Verify business belongs to user
    business = db.query(models.Business).filter(models.Business.id == business_id, models.Business.owner_id == current_user.id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    # Update business with refresh token
    if refresh_token:
        business.google_refresh_token = refresh_token
    
    business.google_connected = True
    
    # FETCH ACCOUNT AND LOCATION ID
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # 1. Fetch Accounts
        accounts_resp = await client.get(
            "https://mybusinessaccountmanagement.googleapis.com/v1/accounts",
            headers=headers
        )
        if accounts_resp.status_code == 200 and accounts_resp.json().get("accounts"):
            account_id = accounts_resp.json()["accounts"][0]["name"]
            business.google_account_id = account_id
            
            # 2. Fetch Locations for that account
            locations_resp = await client.get(
                f"https://mybusinessbusinessinformation.googleapis.com/v1/{account_id}/locations?readMask=name,title",
                headers=headers
            )
            if locations_resp.status_code == 200 and locations_resp.json().get("locations"):
                # Pick the first location for now
                location = locations_resp.json()["locations"][0]
                business.google_location_id = location["name"] # e.g. accounts/123/locations/456
                # We could also sync the name if we wanted
    
    db.commit()
    return {"status": "success", "account_id": business.google_account_id, "location_id": business.google_location_id}

@router.get("/reviews")
async def get_google_reviews(business_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    business = db.query(models.Business).filter(models.Business.id == business_id, models.Business.owner_id == current_user.id).first()
    if not business or not business.google_refresh_token or not business.google_location_id:
        raise HTTPException(status_code=400, detail="Google Business not connected or location not set")

    access_token = await refresh_access_token(business.google_refresh_token)
    
    # Actual Google Business Profile API call for reviews
    async with httpx.AsyncClient() as client:
        # Note: the endpoint for reviews is under the Business Information API or My Business Reviews API
        # The correct v4 endpoint for reviews is:
        url = f"https://mybusiness.googleapis.com/v4/{business.google_location_id}/reviews"
        resp = await client.get(url, headers={"Authorization": f"Bearer {access_token}"})
        
        if resp.status_code != 200:
            # Fallback to empty list or handle error
            return []
            
        return resp.json().get("reviews", [])

@router.post("/reviews/{review_id}/ai-reply")
async def get_ai_reply(review_id: str, business_id: int, review_text: str, rating: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    business = db.query(models.Business).filter(models.Business.id == business_id, models.Business.owner_id == current_user.id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
        
    reply = await generate_review_reply(review_text, business.name, rating)
    return {"reply": reply}

@router.post("/reviews/{review_id}/reply")
async def reply_to_review(review_id: str, business_id: int, reply_text: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    business = db.query(models.Business).filter(models.Business.id == business_id, models.Business.owner_id == current_user.id).first()
    if not business or not business.google_refresh_token or not business.google_location_id:
        raise HTTPException(status_code=400, detail="Google Business not connected")

    access_token = await refresh_access_token(business.google_refresh_token)
    
    # Actual Google Business Profile API call to post a reply
    url = f"https://mybusiness.googleapis.com/v4/{business.google_location_id}/reviews/{review_id}/reply"
    async with httpx.AsyncClient() as client:
        resp = await client.put(
            url,
            headers={"Authorization": f"Bearer {access_token}"},
            json={"comment": reply_text}
        )
        
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=f"Google API error: {resp.text}")
            
    return {"status": "success", "reply": reply_text}
