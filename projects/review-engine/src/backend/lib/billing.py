import os
import stripe
from dotenv import load_dotenv

load_dotenv()

class BillingService:
    def __init__(self):
        self.api_key = os.getenv("STRIPE_API_KEY")
        self.webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        if self.api_key:
            stripe.api_key = self.api_key

    def create_checkout_session(self, business_id: int, business_email: str):
        if not self.api_key:
            print("⚠️ Stripe API key missing. Mocking Checkout Session.")
            return {"id": "mock_session_id", "url": "https://checkout.stripe.com/mock"}

        try:
            # We assume a price ID for the 'Basic' plan
            price_id = os.getenv("STRIPE_BASIC_PRICE_ID")
            
            checkout_session = stripe.checkout.Session.create(
                customer_email=business_email,
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1,
                    },
                ],
                mode="subscription",
                success_url="http://localhost:3000/dashboard?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://localhost:3000/billing",
                metadata={
                    "business_id": str(business_id)
                }
            )
            return {"id": checkout_session.id, "url": checkout_session.url}
        except Exception as e:
            print(f"❌ Stripe Error: {e}")
            return None

    def handle_webhook(self, payload: bytes, sig_header: str):
        if not self.webhook_secret:
            return None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.webhook_secret
            )
            
            # Handle the event
            if event["type"] == "checkout.session.completed":
                session = event["data"]["object"]
                # Update business status to 'active' in DB
                return {
                    "type": "checkout.session.completed",
                    "business_id": session["metadata"].get("business_id"),
                    "customer_id": session.get("customer"),
                    "subscription_id": session.get("subscription")
                }
            
            return {"type": event["type"]}
        except Exception as e:
            print(f"❌ Stripe Webhook Error: {e}")
            return None

billing = BillingService()
