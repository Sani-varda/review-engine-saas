import os
import sys
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from lib.services import messaging

def run_follow_ups():
    db = SessionLocal()
    try:
        # Define the threshold (24 hours ago)
        threshold = datetime.utcnow() - timedelta(hours=24)
        
        # Find SENT requests created more than 24 hours ago that are not COMPLETED/OPENED
        pending_requests = db.query(models.ReviewRequest).filter(
            models.ReviewRequest.status == "SENT",
            models.ReviewRequest.created_at < threshold
        ).all()
        
        print(f"⏰ Checking follow-ups. Found {len(pending_requests)} qualifying requests.")
        
        for req in pending_requests:
            customer = req.customer
            business = req.business
            review_link = f"http://localhost:3000/review/{req.id}"
            
            message = f"Hi {customer.name}! Just a quick reminder about your visit to {business.name}. We'd love your feedback: {review_link}"
            
            print(f"🚀 Sending follow-up for {customer.name} ({business.name})...")
            
            # Use MessagingService
            success = messaging.send_sms(customer.phone, message) if customer.phone else True
            if customer.email:
                email_html = f"""
                <div style="font-family: sans-serif; padding: 20px; color: #333;">
                    <h2>Quick Reminder</h2>
                    <p>Hi {customer.name}, just following up on your experience at {business.name}. We'd appreciate 30 seconds of your time!</p>
                    <a href="{review_link}" style="background: #0f172a; color: #fff; padding: 12px 24px; text-decoration: none; border-radius: 8px; display: inline-block;">
                        Leave a Review
                    </a>
                </div>
                """
                success = messaging.send_email(customer.email, f"Reminder: Review your visit to {business.name}", email_html) and success
            
            if success:
                req.status = "FOLLOW_UP_SENT"
                db.commit()
                print(f"✅ Follow-up sent for request {req.id}")
                
    except Exception as e:
        print(f"❌ Error in follow-up script: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_follow_ups()
