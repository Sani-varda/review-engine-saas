# 🤖 MoonLIT Outreach Workflow (n8n)

> **Objective:** Automate the handoff from lead generation (Notion) to outreach (Email/LinkedIn).

---

## 🏗️ Workflow Logic

### 1. Lead Intake (Notion Trigger)
- **Trigger:** Poll Notion "MoonLIT DB" for new pages added with `High Probability = True`.
- **Frequency:** Every 6 hours.

### 2. Verification & Cleaning
- **Logic:** Filter out leads without emails or phone numbers (unless they have LinkedIn).
- **Tool:** internal script or n8n filter.

### 3. Personalization
- **AI Step:** Use OpenAI/Gemini to craft a personalized snippet based on the niche and location.
- **Template:** "Hi {Founder Name}, I noticed {Business Name} in {Location} has great reviews on Google but no website. We build review engines that..."

### 4. Dispatch
- **Channel A (Email):** Send via Resend/SendGrid.
- **Channel B (LinkedIn):** Log to a "To-Action" list for manual outreach (or automation if enabled).

---

## 🛠️ Setup Instructions
1. Install n8n via Docker (see `docker-compose.yml`).
2. Import `n8n/workflows/outreach-v1.json` (to be created).
3. Connect credentials (Notion, OpenAI, Resend).
