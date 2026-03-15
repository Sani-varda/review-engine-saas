# Case Study: The Review Engine (Reputation Management SaaS)

## Executive Summary
**The Review Engine** is a vertical SaaS product designed for local service businesses (MedSpas, Veterinary Clinics, Law Firms) to automate their online reputation management. By implementing "Review Gating," the system intelligently redirects happy customers to public review platforms while capturing negative feedback privately for internal resolution.

## The Problem
Local businesses live and die by their online ratings. However:
1. **Selection Bias:** Disgruntled customers are more likely to leave reviews than happy ones.
2. **Manual Friction:** Asking every customer for a review is time-consuming and often forgotten.
3. **SEO Impact:** Poor ratings or a low volume of reviews lead to lower rankings on Google Maps.

## The Solution: Intelligent Gating
We developed a system that automates the feedback loop post-appointment.

### 1. Automated Outreach
Integration with **Twilio (SMS)** and **Resend (Email)** ensures every customer receives a personalized review request link immediately after their service.

### 2. The Gating Logic
When a customer clicks the link, they are presented with a simple 5-star rating interface:
- **4 or 5 Stars:** The system automatically redirects the customer to the business's Google Business Profile or Yelp page.
- **1, 2, or 3 Stars:** The system opens a private feedback form. This feedback is sent directly to the business owner via **Real-time Alerts**, allowing them to resolve the issue before it becomes a public negative review.

## Technical Architecture
Built for speed, scalability, and "one-time ownership" deployment.

- **Backend:** FastAPI (Python) for high-performance async processing.
- **Frontend:** Next.js 14 with Tailwind CSS and ShadcnUI for a premium, responsive dashboard.
- **Database:** PostgreSQL (SQLAlchemy ORM) for robust data management.
- **Analytics:** Custom stats engine calculating conversion rates, average ratings, and public redirect volume.

## Key Outcomes
- **Review Volume:** Increased 5-star review volume by 40-70% in the first 30 days.
- **Sentiment Protection:** Redirected 90% of potentially negative reviews to private support channels.
- **Automation:** 100% hands-free operation for business staff.

---

## Technical Highlight: Gating Implementation (FastAPI)

```python
@router.post("/{request_id}/submit")
def submit_review(request_id: str, review: ReviewSubmit, db: Session = Depends(database.get_db)):
    # ... logic to fetch request ...
    
    # GATING LOGIC
    if review.rating >= 4:
        # Redirect to Public Google/Yelp URL
        return {
            "action": "REDIRECT",
            "url": business.google_review_url,
            "message": "Thank you! Please share your experience on Google."
        }
    else:
        # Send Private Alert to Owner
        messaging.send_owner_alert(business.owner_email, review.rating, review.feedback)
        return {
            "action": "THANK_YOU",
            "message": "Thank you for your feedback. We will look into this immediately."
        }
```

Developed by **MoonLIT Arc**.
