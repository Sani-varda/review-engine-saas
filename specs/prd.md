# 📋 PRD: The Review Engine (MVP)

> **Objective:** Automated reputation management for high-ticket local businesses.
> **Target:** MedSpas, Dental Clinics, Luxury Salons.

---

## 🎯 Core Problem
Businesses have "silent satisfied customers" and "vocal unhappy ones." This leads to a lower Google rating than they deserve, costing them search visibility and trust.

## 💡 The Solution
A "Review Gatekeeper" system:
1. **Trigger:** Business marks an appointment as "Completed" (or via API/CSV).
2. **Action:** System sends a personalized SMS/Email link.
3. **The Gate:**
   - **4-5 Stars:** Redirected to the business's public Google/Yelp/FB profile.
   - **1-3 Stars:** Redirected to a private "Feedback Form" (sent to owner, not public).
4. **Dashboard:** Basic analytics showing sentiment and conversion.

---

## 🛠️ MVP Feature Set (7-Day Sprint)

### Phase 1: Core Backend (SAM)
- [ ] **Auth:** Simple login for business owners.
- [ ] **Customer Management:** Basic list (Name, Phone, Email).
- [ ] **Review Logic:** Unique link generation per customer.
- [ ] **Integrations:** 
  - **Twilio** (SMS)
  - **Resend** (Email)
  - **Stripe** (Subscription)

### Phase 2: Frontend (SAM)
- [ ] **Client Dashboard:** "Send Review Request" button + Review Stats.
- [ ] **Review Landing Page:** Mobile-optimized 5-star selector.
- [ ] **Feedback Page:** Form for negative sentiment capture.

### Phase 3: Automation (MARK)
- [ ] **Automatic Follow-up:** 24h reminder if no interaction.
- [ ] **Owner Alerts:** Real-time notification of negative feedback.

---

## 📐 Architecture
- **Backend:** FastAPI (Python)
- **Frontend:** Next.js + Tailwind
- **Database:** PostgreSQL (Supabase or Local Docker)
- **Deployment:** Docker Compose on VPS / Render

---

## 📅 Sprint Plan (7 Days)
- **Day 1:** Architecture & DB Schema (SAM)
- **Day 2:** Auth & Core API (SAM)
- **Day 3:** Review Logic & Link Gen (SAM)
- **Day 4:** Frontend Dashboard (SAM)
- **Day 5:** SMS/Email Integration (SAM) + Testing (MARK)
- **Day 6:** Landing Page Polish & Analytics (SAM)
- **Day 7:** Deployment & GitHub Push (Alfred)
