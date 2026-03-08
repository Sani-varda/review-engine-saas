from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.orm import Session
import models, database
from lib.billing import billing
import os

router = APIRouter(prefix="/billing", tags=["billing"])

@router.post("/checkout")
def create_checkout(business_id: int, db: Session = Depends(database.get_db)):
    business = db.query(models.Business).filter(models.Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
        
    session = billing.create_checkout_session(
        business_id=business.id,
        business_email=business.owner_email or "test@example.com" # Placeholder
    )
    
    if session:
        return {"url": session["url"], "session_id": session["id"]}
    else:
        raise HTTPException(status_code=400, detail="Could not create checkout session")

@router.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()
    event_data = billing.handle_webhook(payload, stripe_signature)
    
    if event_data and event_data["type"] == "checkout.session.completed":
        # Business successfully subscribed
        business_id = event_data.get("business_id")
        # Logic to update business subscription status
        print(f"💰 Subscription successful for Business ID: {business_id}")
        
    return {"status": "success"}
