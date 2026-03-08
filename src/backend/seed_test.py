from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import uuid

def seed():
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Create a test business
        business = db.query(models.Business).filter(models.Business.name == "MoonLIT Arc Test Spa").first()
        if not business:
            business = models.Business(
                name="MoonLIT Arc Test Spa",
                google_review_url="https://search.google.com/local/writereview?placeid=ChIJo_f3vXUUrjsR3Z5u_3vXUUrjs"
            )
            db.add(business)
            db.commit()
            db.refresh(business)
            print(f"✅ Created Business: {business.name}")

        # Create a test customer
        customer = db.query(models.Customer).filter(models.Customer.email == "customer@example.com").first()
        if not customer:
            customer = models.Customer(
                name="Sani Test",
                email="customer@example.com",
                phone="+919999999999"
            )
            db.add(customer)
            db.commit()
            db.refresh(customer)
            print(f"✅ Created Customer: {customer.name}")

    finally:
        db.close()

if __name__ == "__main__":
    seed()
