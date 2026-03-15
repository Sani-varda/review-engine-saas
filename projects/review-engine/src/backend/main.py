from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, reviews, billing, google_business
import models, database
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from scripts.auto_reply_sync import sync_and_reply
from contextlib import asynccontextmanager

# Create tables
models.Base.metadata.create_all(bind=database.engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start the auto-reply scheduler
    scheduler = AsyncIOScheduler()
    # Run every 1 hour (adjust as needed for production)
    scheduler.add_job(sync_and_reply, 'interval', hours=1)
    scheduler.start()
    print("⏰ Auto-reply scheduler started.")
    yield
    # Shutdown
    scheduler.shutdown()
    print("⏰ Auto-reply scheduler stopped.")

app = FastAPI(
    title="The Review Engine API", 
    version="0.1.0",
    lifespan=lifespan
)

# CORS Configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(reviews.router)
app.include_router(billing.router)
app.include_router(google_business.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2026-03-01T14:05:00Z"}
