from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import models, database, auth
import httpx
import os
from typing import List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/google", tags=["google_business"])

# In a real app, these would be in environment variables
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "dummy_client_id")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "dummy_client_secret")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:3000/api/google/callback")

class GoogleConnectionStatus(BaseModel):
    connected: bool
    business_name: str | None = None

@router.get("/auth-url")
def get_auth_url(business_id: int, current_user: models.User = Depends(auth.get_current_user)):
    # Redirect URL for Google OAuth
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
    
    # In a real app, we'd fetch the Account and Location IDs here
    # For MVP, we'll assume we can list them and pick the first one or let user choose
    # Let's mock fetching them
    
    db.commit()
    return {"status": "success"}

@router.get("/reviews", response_model=List[dict])
async def get_google_reviews(business_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    business = db.query(models.Business).filter(models.Business.id == business_id, models.Business.owner_id == current_user.id).first()
    if not business or not business.google_refresh_token:
        raise HTTPException(status_code=400, detail="Google Business not connected")

    # In a real app, we'd use the refresh token to get a new access token
    # then call https://mybusiness.googleapis.com/v4/accounts/{accountId}/locations/{locationId}/reviews
    
    # Mocking review data for now
    mock_reviews = [
        {
            "reviewId": "1",
            "reviewer": {"displayName": "John Doe"},
            "starRating": "FIVE",
            "comment": "Amazing service! Highly recommend.",
            "createTime": "2026-03-10T10:00:00Z",
            "reply": None
        },
        {
            "reviewId": "2",
            "reviewer": {"displayName": "Jane Smith"},
            "starRating": "FOUR",
            "comment": "Very good, but waiting time was a bit long.",
            "createTime": "2026-03-12T14:30:00Z",
            "reply": {"comment": "Thank you Jane! We are working on improving our wait times."}
        }
    ]
    return mock_reviews

@router.post("/reviews/{review_id}/reply")
async def reply_to_review(review_id: str, business_id: int, reply_text: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    business = db.query(models.Business).filter(models.Business.id == business_id, models.Business.owner_id == current_user.id).first()
    if not business or not business.google_refresh_token:
        raise HTTPException(status_code=400, detail="Google Business not connected")

    # In a real app, we'd use the refresh token to get a new access token
    # then call PUT https://mybusiness.googleapis.com/v4/accounts/{accountId}/locations/{locationId}/reviews/{reviewId}/reply
    
    return {"status": "success", "reply": reply_text}
