# 🔄 OPENCLAW AGENT — WORKFLOW

> Complete lifecycle from niche discovery to client delivery. Every project follows this pipeline.

---

## Master Pipeline

```
┌─────────┐   ┌──────────┐   ┌───────────┐   ┌──────────┐   ┌──────────┐
│ PHASE 1 │───▶│ PHASE 2 │───▶│ PHASE 3 │───▶│ PHASE 4 │───▶│ PHASE 5 │
│Discovery│   │ Planning │   │   Build   │   │  Verify  │   │  Launch  │
│ (Alfred)│   │ (Alfred) │   │   (SAM)   │   │  (MARK)  │   │(TONY+John│
└─────────┘   └──────────┘   └───────────┘   └──────────┘   └──────────┘
                                   │                              │
                                   ▼                              ▼
                             ┌──────────┐
                             │ PHASE 6  │
                             │ Deliver  │
                             │ (Alfred) │
                             └──────────┘
```

---

## Phase 1: Discovery (Alfred — Gemini-3-Flash)
**Objective:** Identify a profitable small business niche.

### Activities
1. **Niche Identification** — Scan small business verticals (med spas, salons, gyms, restaurants, clinics)
2. **Problem Validation** — Define top 3 pain points, map competitors, estimate willingness to pay
3. **Opportunity Scoring**
```yaml
niche: "Med Spa Booking"
pain_level: 9/10
competition: 4/10
build_complexity: 5/10
monetization: 8/10
score: 7.5/10
decision: GO | NO-GO
```

### Output
- `specs/niche-analysis.md` — Research document
- `specs/problem-statement.md` — Core problem definition
- GO/NO-GO decision

### Duration: 0.5–1 day

---

## Phase 2: Planning (Alfred — Gemini-3-Flash)
**Objective:** Create product specification and sprint plan.

### Activities
1. **PRD** — Product requirements with MVP features, target user, pricing
2. **Technical Architecture** — System diagram, DB schema, API endpoints, stack confirmation
3. **Sprint Planning** — Break PRD into tasks, assign to agents, set deadlines
4. **Marketing Brief** — Target audience, value prop, competitors, SEO keywords (for TONY)
5. **Lead Gen Brief** — Geographic targets, business type, ideal customer profile (for John)

### Output
- `specs/prd.md`, `specs/architecture.md`, `specs/sprint-plan.md`
- `marketing/brief.md`, `leads/brief.md`

### Duration: 0.5–1 day

---

## Phase 3: Build (SAM — Opus 4.5)
**Objective:** Build the production-grade application.

### 3A: Foundation (Day 1–2)
- Initialize repository + Docker environment
- Backend skeleton (FastAPI, DB models, migrations, auth)
- Frontend skeleton (Next.js/Vite, routes, layout, auth pages)
- CI/CD setup (GitHub Actions, linting, test runner)

### 3B: Core Features (Day 3–4)
- Backend CRUD APIs + business logic + validation + error handling
- Frontend dashboard + feature UI + settings + responsive design
- Integrations (email, SMS, payments — as needed)

### 3C: Polish (Day 5)
- Landing page, admin panel, mobile responsiveness
- Loading states, error handling, SEO meta tags
- Final API documentation

### Parallel Work
- **MARK** writes tests as SAM delivers code
- **TONY** prepares marketing assets (if Day 5+ in 14-day sprint)
- **John** begins lead scraping (if brief is ready)

### Handoff: SAM → MARK
```yaml
from: SAM
to: MARK
type: CODE_READY
branch: feature/auth-module
files_changed: 12
tests_needed:
  - Unit tests for auth endpoints
  - Integration test for login flow
```

---

## Phase 4: Verify (MARK — Flash + Opus 4.5 for fixes)
**Objective:** Ensure production-grade quality.

### Activities
1. **Unit Testing** — Every endpoint, business logic, DB operations (80%+ coverage)
2. **Integration Testing** — API-to-DB flows, auth flows, third-party integrations
3. **E2E Testing** — Full user journeys via Playwright
4. **Security Scan** — Secrets check, input sanitization, CORS, auth bypass
5. **Performance Check** — API < 200ms, page load < 3s, query optimization

### Bug Fix Routing
| Severity | Model | Deadline |
|----------|-------|----------|
| CRITICAL | Opus 4.5 (SAM) | Immediate |
| HIGH | Opus 4.5 (SAM) | Same day |
| MEDIUM | Gemini-3-Flash (MARK) | Next day |
| LOW | Gemini-3-Flash (MARK) | Before delivery |

---

## Phase 5: Launch (TONY + John)

### 5A: Marketing (TONY)
- **SEO:** Meta tags, sitemap, robots.txt, schema markup, keyword optimization
- **Ads:** Google Ads + Meta Ads campaigns, audience targeting, A/B test copy
- **Social Media:** Create profiles (IG, FB, LinkedIn, X, YouTube), launch posts, 30-day calendar
- **Content:** Landing page copy, blog posts, email templates

### 5B: Lead Generation (John)
- **Google Maps Scraping:** Find businesses by niche + location, extract contact data
- **Apollo.io Enrichment:** Enrich with owner name, email, company size, revenue
- **Qualification:** Score leads (HOT/WARM/COLD), segment by readiness
- **Outreach:** Personalized email templates, 3-email drip via n8n automation

---

## Phase 6: Deliver (Alfred)

### Activities
1. **Production Deployment** — Cloud deploy, domain + SSL, env vars, DB migrations
2. **Documentation** — Setup guide, user manual, API docs, admin guide
3. **Client Handoff** — Repo access, credentials (secure), walkthrough/video, billing setup
4. **Post-Delivery** — Uptime Kuma monitoring, error alerting, Day 7 follow-up

---

## n8n Automation Workflows

| Workflow | Trigger | Actions |
|----------|---------|---------|
| Lead Enrichment | New lead in raw CSV | Enrich via Apollo.io → Save qualified |
| Outreach Drip | Lead qualified | Send 3-email sequence |
| Bug Alert | Error in production | Notify Alfred + MARK |
| Daily Report | End of day cron | Compile standup → heartbeat file |
| Deployment | PR merged to main | Docker build → Deploy → Health check |
| Social Post | Scheduled | Post to IG/FB/LinkedIn/X |

---

## Parallel Execution Timeline (14 Days)

```
Day:    1  2  3  4  5  6  7  8  9  10 11 12 13 14
SAM:    [===FOUNDATION===][====CORE FEATURES====][POLISH][ BUG FIXES ]
MARK:   [             ][======TESTING======][===BUG REPORTS===][=FINAL QA=]
TONY:   [             ][   RESEARCH   ][===MARKETING ASSETS===][LAUNCH]
John:   [             ][===LEAD SCRAPING===][==ENRICHMENT==][=OUTREACH=]
Alfred: [PLAN][      COORDINATE      ][   MONITOR   ][ ASSEMBLE ][ DELIVER ]
```
