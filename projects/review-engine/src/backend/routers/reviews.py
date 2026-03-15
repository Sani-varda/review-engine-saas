from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import models, database, auth
from pydantic import BaseModel, EmailStr
import uuid
from lib.services import messaging
from lib.ai_service import generate_review_reply

from datetime import datetime

router = APIRouter(prefix="/reviews", tags=["reviews"])

class ReviewRequestCreate(BaseModel):
    customer_id: int
    business_id: int

class ReviewRequestOut(BaseModel):
    id: str
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class ReviewSubmit(BaseModel):
    rating: int
    feedback: Optional[str] = None

class GenerateReplyRequest(BaseModel):
    review_text: str
    business_name: str = "our business"
    star_rating: int = 5

@router.get("/stats")
def get_business_stats(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Infer business_id from the first business owned by the user
    business = db.query(models.Business).filter(models.Business.owner_id == current_user.id).first()
    if not business:
        return {
            "total": 0, "sent": 0, "opened": 0, "completed": 0,
            "high_rating": 0, "private_feedback": 0, "avg_rating": 0, "conversion_rate": 0
        }
        
    requests = db.query(models.ReviewRequest).filter(models.ReviewRequest.business_id == business.id).all()
    
    total = len(requests)
    sent = len([r for r in requests if r.status == "SENT"])
    opened = len([r for r in requests if r.status in ["OPENED", "COMPLETED"]])
    completed = len([r for r in requests if r.status == "COMPLETED"])
    high_rating = len([r for r in requests if r.status == "COMPLETED" and r.rating >= 4])
    private_feedback = len([r for r in requests if r.status == "COMPLETED" and r.rating < 4])
    
    avg_rating = 0
    if completed > 0:
        avg_rating = sum([r.rating for r in requests if r.rating]) / completed

    return {
        "total": total,
        "sent": sent,
        "opened": opened,
        "completed": completed,
        "high_rating": high_rating,
        "private_feedback": private_feedback,
        "avg_rating": round(avg_rating, 1),
        "conversion_rate": round((completed / opened * 100), 1) if opened > 0 else 0,
        "auto_reply_enabled": business.auto_reply_enabled
    }

@router.get("/activity")
def get_recent_activity(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    business = db.query(models.Business).filter(models.Business.owner_id == current_user.id).first()
    if not business:
        return []
        
    requests = db.query(models.ReviewRequest).filter(models.ReviewRequest.business_id == business.id).order_by(models.ReviewRequest.updated_at.desc()).limit(10).all()
    
    return [
        {
            "name": r.customer.name,
            "status": r.status,
            "rating": r.rating,
            "updated_at": r.updated_at.isoformat()
        } for r in requests
    ]

@router.post("/generate-reply")
async def generate_reply(req: GenerateReplyRequest, current_user: models.User = Depends(auth.get_current_user)):
    reply = await generate_review_reply(req.review_text, req.business_name, req.star_rating)
    if not reply:
        raise HTTPException(status_code=500, detail="AI generation failed")
    return {"reply": reply}

@router.post("/request", response_model=ReviewRequestOut)
def create_review_request(request: ReviewRequestCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Verify customer and business exist
    customer = db.query(models.Customer).filter(models.Customer.id == request.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Generate unique review request
    new_request = models.ReviewRequest(
        customer_id=request.customer_id,
        business_id=request.business_id,
        status="PENDING"
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    
    # Send Review Request (SMS/Email)
    review_link = f"http://localhost:3000/review/{new_request.id}"
    
    success = messaging.send_review_request(
        customer_name=customer.name,
        business_name=new_request.business.name,
        review_link=review_link,
        to_phone=customer.phone,
        to_email=customer.email
    )
    
    if success:
        new_request.status = "SENT"
        db.commit()
    
    return new_request

@router.get("/{request_id}")
def get_review_request_status(request_id: str, db: Session = Depends(database.get_db)):
    review_req = db.query(models.ReviewRequest).filter(models.ReviewRequest.id == request_id).first()
    if not review_req:
        raise HTTPException(status_code=404, detail="Review request not found")
    
    # Mark as opened if first time
    if review_req.status == "SENT":
        review_req.status = "OPENED"
        db.commit()
        
    return {
        "id": review_req.id,
        "business_name": review_req.business.name,
        "status": review_req.status
    }

@router.post("/{request_id}/submit")
def submit_review(request_id: str, review: ReviewSubmit, db: Session = Depends(database.get_db)):
    review_req = db.query(models.ReviewRequest).filter(models.ReviewRequest.id == request_id).first()
    if not review_req:
        raise HTTPException(status_code=404, detail="Review request not found")
    
    if review_req.status == "COMPLETED":
        raise HTTPException(status_code=400, detail="Review already submitted")

    review_req.rating = review.rating
    review_req.feedback = review.feedback
    review_req.status = "COMPLETED"
    db.commit()

    # OWNER ALERTS FOR LOW RATING
    if review.rating < 4:
        # Fetch owner email from business
        business = review_req.business
        if business.owner_email:
            messaging.send_owner_alert(
                owner_email=business.owner_email,
                business_name=business.name,
                customer_name=review_req.customer.name,
                rating=review.rating,
                feedback=review.feedback or "No written feedback provided."
            )

    # GATING LOGIC
    if review.rating >= 4:
        return {
            "action": "REDIRECT",
            "url": review_req.business.google_review_url or "https://google.com",
            "message": "Thank you! Please share your experience on Google."
        }
    else:
        return {
            "action": "THANK_YOU",
            "message": "Thank you for your feedback. We will look into this immediately."
        }
