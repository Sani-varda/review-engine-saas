import os
from twilio.rest import Client
import resend
from dotenv import load_dotenv

load_dotenv()

class MessagingService:
    def __init__(self):
        # Twilio
        self.twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
        
        # Resend
        self.resend_api_key = os.getenv("RESEND_API_KEY")
        if self.resend_api_key:
            resend.api_key = self.resend_api_key

    def send_sms(self, to_phone: str, message: str):
        if not all([self.twilio_sid, self.twilio_token, self.twilio_phone]):
            print(f"⚠️ Twilio keys missing. Mocking SMS to {to_phone}: {message}")
            return True
            
        try:
            client = Client(self.twilio_sid, self.twilio_token)
            message = client.messages.create(
                body=message,
                from_=self.twilio_phone,
                to=to_phone
            )
            return True
        except Exception as e:
            print(f"❌ Twilio Error: {e}")
            return False

    def send_email(self, to_email: str, subject: str, html_content: str):
        if not self.resend_api_key:
            print(f"⚠️ Resend key missing. Mocking Email to {to_email}: {subject}")
            return True
            
        try:
            params = {
                "from": "onboarding@resend.dev", # Default for test
                "to": [to_email],
                "subject": subject,
                "html": html_content,
            }
            resend.Emails.send(params)
            return True
        except Exception as e:
            print(f"❌ Resend Error: {e}")
            return False

    def send_review_request(self, customer_name: str, business_name: str, review_link: str, to_phone: str = None, to_email: str = None):
        message = f"Hi {customer_name}! How was your visit to {business_name}? We'd love your feedback: {review_link}"
        
        success = True
        if to_phone:
            success = self.send_sms(to_phone, message)
        
        if to_email:
            email_html = f"""
            <div style="font-family: sans-serif; padding: 20px; color: #333;">
                <h2>How was your visit to {business_name}?</h2>
                <p>Hi {customer_name}, we'd love to hear about your experience today.</p>
                <a href="{review_link}" style="background: #0f172a; color: #fff; padding: 12px 24px; text-decoration: none; border-radius: 8px; display: inline-block;">
                    Leave a Review
                </a>
            </div>
            """
            success = self.send_email(to_email, f"Review your visit to {business_name}", email_html) and success
            
        return success

    def send_owner_alert(self, owner_email: str, business_name: str, customer_name: str, rating: int, feedback: str):
        subject = f"⚠️ Low Rating Alert: {business_name}"
        html_content = f"""
        <div style="font-family: sans-serif; padding: 20px; color: #333;">
            <h2 style="color: #ef4444;">Negative Feedback Received</h2>
            <p><strong>Business:</strong> {business_name}</p>
            <p><strong>Customer:</strong> {customer_name}</p>
            <p><strong>Rating:</strong> {rating} / 5</p>
            <p><strong>Feedback:</strong> {feedback}</p>
            <hr style="border: 1px solid #eee; margin: 20px 0;">
            <p style="font-size: 12px; color: #666;">This is an automated alert from The Review Engine.</p>
        </div>
        """
        return self.send_email(owner_email, subject, html_content)

# Global instance
messaging = MessagingService()
