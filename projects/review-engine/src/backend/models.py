from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    businesses = relationship("Business", back_populates="owner")

class Business(Base):
    __tablename__ = "businesses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_email = Column(String, nullable=True)
    google_place_id = Column(String, nullable=True)
    google_review_url = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="businesses")
    customers = relationship("Customer", back_populates="business")
    review_requests = relationship("ReviewRequest", back_populates="business")

    # Google Business Profile Integration
    google_account_id = Column(String, nullable=True) # e.g. accounts/123...
    google_location_id = Column(String, nullable=True) # e.g. accounts/123/locations/456...
    google_refresh_token = Column(String, nullable=True)
    google_connected = Column(Boolean, default=False)

class GoogleReview(Base):
    __tablename__ = "google_reviews"
    id = Column(String, primary_key=True) # Google's review ID
    business_id = Column(Integer, ForeignKey("businesses.id"))
    reviewer_name = Column(String)
    star_rating = Column(Integer)
    comment = Column(Text, nullable=True)
    reply_text = Column(Text, nullable=True)
    status = Column(String, default="NEW") # NEW, REPLIED
    create_time = Column(DateTime)
    update_time = Column(DateTime)

    business = relationship("Business")

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    business = relationship("Business", back_populates="customers")
    review_requests = relationship("ReviewRequest", back_populates="customer")

class ReviewRequest(Base):
    __tablename__ = "review_requests"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    business_id = Column(Integer, ForeignKey("businesses.id"))
    status = Column(String, default="PENDING") # PENDING, SENT, OPENED, COMPLETED
    rating = Column(Integer, nullable=True) # Captured during the gating process
    feedback = Column(Text, nullable=True) # Captured if rating < 4
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship("Customer", back_populates="review_requests")
    business = relationship("Business", back_populates="review_requests")
