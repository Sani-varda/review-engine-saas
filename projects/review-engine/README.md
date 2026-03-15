# The Review Engine (Production SaaS)

> Automated Reputation Management for Local Businesses.

The Review Engine is a high-performance, production-ready vertical SaaS designed to help local businesses (Dental Clinics, MedSpas, Salons, etc.) dominate their local market by automating review collection, intelligently gating feedback, and leveraging AI for review management.

---

## Key Features

### 1. Intelligent Review Gating
Automatically filter customer sentiment before it hits public platforms.
- **High Ratings (4-5 Stars):** Customers are instantly redirected to your Google Business Profile, Yelp, or Facebook page to post public reviews.
- **Low Ratings (1-3 Stars):** Customers are routed to a private feedback form. The owner is notified in real-time to resolve the issue internally, preventing public negative reviews.

### 2. AI-Powered Review Management
Manage your Google Business Profile directly from the dashboard.
- **Auto-Fetch:** Automatically syncs reviews from your Google Maps locations.
- **AI Auto-Replies:** Generates personalized, empathetic responses to Google reviews using **Gemini-3-Flash**.
- **One-Tap Posting:** Edit and post AI-drafted replies back to Google with a single click.

### 3. Multi-Platform Support
- **Web Dashboard:** A premium Next.js dashboard for full management and deep analytics.
- **Mobile App (Flutter):** Manage reviews, send invites, and track stats on the go with a native iOS/Android experience.
- **Review Landing Pages:** High-converting, mobile-optimized pages for customer feedback.

### 4. Automated Outreach
- **Omnichannel:** Send review requests via **SMS (Twilio)** or **Email (Resend)**.
- **CRM Integration:** Manage customer lists and track the status of every review request (Sent, Opened, Completed).

### 5. Advanced Analytics
- Real-time tracking of average ratings, review growth, and conversion rates.
- Detailed activity logs of all customer interactions.

---

## Technical Stack

- **Backend:** FastAPI (Python 3.11) - Async, high-performance API.
- **Frontend:** Next.js 14 + Tailwind CSS + Lucide Icons.
- **Mobile:** Flutter (iOS & Android).
- **Database:** PostgreSQL (SQLAlchemy ORM).
- **AI:** Google Gemini-3-Flash.
- **DevOps:** Docker & Docker Compose.

---

## Project Structure

```bash
projects/review-engine/
├── src/
│   ├── backend/    # FastAPI Python API
│   ├── frontend/   # Next.js Web Dashboard
│   └── mobile/     # Flutter Cross-Platform App
├── docs/           # Architecture & Whitepapers
├── specs/          # PRD & Technical Specs
└── docker-compose.yml
```

---

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Google Cloud Project (for GBP API & OAuth2)
- Twilio Account (for SMS)
- Resend Account (for Email)

### Quick Start
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sani-varda/review-engine-saas.git
   cd review-engine-saas/projects/review-engine
   ```

2. **Configure Environment**:
   Create a `.env` file in `projects/review-engine/` (see `.env.example`).

3. **Deploy with Docker**:
   ```bash
   docker compose up -d --build
   ```

---

## Business Logic: The Gating Flow

```python
if review.rating >= 4:
    # Redirect to Public Google/Yelp URL
    return {
        "action": "REDIRECT",
        "url": business.google_review_url
    }
else:
    # Capturing Negative Sentiment Privately
    messaging.send_owner_alert(business.owner_email, review.rating, review.feedback)
    return {
        "action": "THANK_YOU",
        "message": "Thank you. We will contact you shortly to resolve this."
    }
```

---

## License
Proprietary - Developed by **MoonLIT Arc**.
