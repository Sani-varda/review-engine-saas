# 📋 PRD: The Review Engine (MVP)

> **Objective:** Automated reputation management for high-ticket local businesses.
> **Target:** MedSpas, Dental Clinics, Luxury Salons.

---

## 🎯 Core Problem
Businesses have "silent satisfied customers" and "vocal unhappy ones." This leads to a lower Google rating than they deserve, costing them search visibility and trust.

## 💡 The Solution
A "Review Gatekeeper" and "Review Manager" system:
1.  **Gatekeeper**: (Existing) Redirects high ratings to Google, keeps low ratings private.
2.  **Manager**: (New) Fetches actual Google reviews from the Business Profile API and provides AI-powered auto-replies.

---

## 🛠️ Feature Set (V2 - Upgrade)

### Phase 4: Google My Business Integration (SAM)
- [x] **Google OAuth2**: Implementation of Google Sign-In with scopes for `business.manage`.
- [x] **GBP API Service**: 
  - [x] Fetch reviews from a business location.
  - [x] Post replies to reviews.
- [ ] **Sync Engine**: Periodic fetching of new reviews.

### Phase 5: AI Auto-Reply (SAM)
- [x] **AI Draft Generation**: Use Gemini-3-Flash to generate personalized, empathetic replies to Google reviews.
- [x] **Context Awareness**: Replies should reflect the business's personality and the customer's feedback.
- [ ] **Auto-Mode**: Configuration to automatically post AI replies for 4-5 star reviews.

### Phase 6: Management Dashboard (SAM)
- [x] **Review Feed**: View all Google reviews in one place.
- [x] **Draft Editor**: View and edit AI-generated drafts before posting.
- [x] **Status Tracking**: See which reviews have been replied to.

---

## 📅 Roadmap (V2 Sprint)
- **Day 1:** Google GCP Setup & Auth Flow (SAM)
- **Day 2:** GBP API Integration (Reviews Fetch/Post) (SAM)
- **Day 3:** AI Reply Engine (Gemini Integration) (SAM)
- **Day 4:** Frontend: Review Management Dashboard (SAM)
- **Day 5:** Auto-Reply Configuration & Testing (SAM/MARK)
- **Day 6:** Polish & Final Deployment (Alfred)
