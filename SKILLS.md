# 🎯 OPENCLAW AGENT — SKILLS

> Competency map for Alfred and every sub-agent. Skills define what each agent **can do** and when to activate them.

---

## Skill Routing Table

> Alfred uses this table to decide which agent handles a request.

| Skill Domain | Sub-Skills | Agent | Model |
|-------------|-----------|-------|-------|
| **Backend Development** | REST API, GraphQL, WebSocket, auth, payments | SAM | Opus 4.5 |
| **Frontend Development** | React, Next.js, responsive UI, animations | SAM | Opus 4.5 |
| **Mobile Development** | React Native, Expo, cross-platform | SAM | Opus 4.5 |
| **Database Engineering** | Schema design, migrations, optimization | SAM | Opus 4.5 |
| **DevOps** | Docker, CI/CD, deployment, Nginx | SAM | Opus 4.5 |
| **Testing** | Unit, integration, E2E, load testing | MARK | Flash |
| **CI/CD Pipeline** | GitHub Actions, automated testing | MARK | Flash |
| **Bug Detection** | Error analysis, reproduction, triage | MARK | Flash |
| **Bug Fixing (simple)** | Config fixes, typos, minor logic | MARK | Flash |
| **Bug Fixing (complex)** | Multi-file, architectural issues | SAM | Opus 4.5 |
| **Monitoring** | Uptime, health checks, alerting | MARK | Flash |
| **Lead Scraping** | Google Maps data extraction | John | Flash |
| **Lead Enrichment** | Apollo.io data enrichment | John | Flash |
| **Lead Qualification** | Scoring, segmentation | John | Flash |
| **Outreach Automation** | Email drips, n8n workflows | John | Flash |
| **Google Ads** | Campaign creation, keyword strategy | TONY | Flash |
| **Meta Ads** | Facebook/Instagram campaigns | TONY | Flash |
| **SEO** | On-page, keywords, schema markup | TONY | Flash |
| **Social Media** | Content creation, scheduling, analytics | TONY | Flash |
| **Competitor Analysis** | Feature comparison, pricing, gaps | TONY | Flash |
| **Pain Point Analysis** | User research, problem identification | TONY | Flash |
| **Sales Copywriting** | Pitch emails, landing pages, ad copy | TONY | Flash |
| **Content Marketing** | Blog posts, email sequences | TONY | Flash |
| **Project Planning** | PRD, task decomposition, scheduling | Alfred | Flash |
| **Agent Coordination** | Task assignment, conflict resolution | Alfred | Flash |
| **Client Communication** | Reports, deliverables, handoff | Alfred | Flash |

---

## SAM's Skill Set (The Builder)

### Architecture Skills
```
├── System Architecture Design
│ ├── Monolith → Modular monolith → Microservices (right-sizing)
│ ├── Event-driven architecture (when needed)
│ └── API-first design
│ ├── Database Architecture
│ ├── Relational schema design (PostgreSQL)
│ ├── Indexing strategy
│ ├── Migration management
│ └── Data modeling (ERD)
│ └── Infrastructure Architecture
├── Docker multi-stage builds
├── Docker Compose orchestration
├── Reverse proxy (Nginx)
└── SSL/TLS configuration
```

### Coding Skills
```
├── Python Backend
│ ├── FastAPI (async REST APIs)
│ ├── SQLAlchemy (ORM + raw SQL)
│ ├── Celery (async tasks)
│ ├── JWT authentication
│ ├── Role-based access control
│ ├── Payment integration (Stripe)
│ ├── Email integration (Resend/SendGrid)
│ └── WebSocket real-time features
│ ├── Frontend
│ ├── React (hooks, context, state management)
│ ├── Next.js (SSR, SSG, App Router)
│ ├── Vite (fast SPA builds)
│ ├── Tailwind CSS (responsive design)
│ ├── Form handling (react-hook-form)
│ ├── Data fetching (SWR, React Query)
│ └── Charts & dashboards (Recharts, Chart.js)
│ ├── Mobile
│ ├── React Native (cross-platform)
│ ├── Expo (managed workflow)
│ ├── Native navigation
│ ├── Push notifications
│ └── App store deployment
│ └── DevOps
├── Docker containerization
├── GitHub Actions CI/CD
├── Environment management
├── Zero-downtime deployment
└── Database backup/restore
```

### SaaS Product Patterns (SAM's Templates)

SAM has pre-built patterns for common Micro SaaS products:

| Pattern | Description | Example Products |
|---------|-------------|-----------------|
| **Booking System** | Online scheduling + reminders + client management | MedSpa Booking, Salon Scheduler |
| **CRM Lite** | Contact management + follow-ups + pipeline | Painting CRM, Fitness Trainer CRM |
| **Invoice & Billing** | Invoicing + payments + receipts | Freelancer Invoicer, Contractor Biller |
| **Appointment Manager** | Calendar + availability + notifications | Doctor Schedule, Consulting Booker |
| **Review Manager** | Collect + manage + respond to reviews | Restaurant Reviews, Auto Shop Reputation |
| **Inventory Tracker** | Stock levels + orders + supplier management | Bakery Stock, Boutique Inventory |
| **Client Portal** | Dashboard for clients to track orders/projects | Photography Portal, Landscaping Tracker |
| **Job Board (Niche)** | Post + apply + manage niche jobs | Dental Jobs, Veterinary Careers |
| **Learning Platform** | Courses + progress + certificates | Yoga Certification, Pet Grooming Academy |
| **Waitlist/Queue** | Digital waitlist + SMS notifications | Restaurant Waitlist, Clinic Queue |

Each pattern includes:
- Database schema template
- API endpoint template
- Frontend page templates
- Test suite template
- Docker configuration
- Deployment scripts

---

## MARK's Skill Set (The Guardian)

### Testing Skills
```
├── Unit Testing
│ ├── pytest (Python backend)
│ ├── Vitest/Jest (Frontend)
│ ├── Mock strategies (dependency injection)
│ ├── Fixture management
│ └── Code coverage analysis
│ ├── Integration Testing
│ ├── API endpoint testing (httpx)
│ ├── Database transaction testing
│ ├── Third-party API mock testing
│ └── Auth flow testing
│ ├── E2E Testing
│ ├── Playwright (browser automation)
│ ├── User flow testing
│ ├── Mobile viewport testing
│ └── Cross-browser validation
│ └── Performance Testing
├── Locust (load testing)
├── API response time benchmarks
├── Database query profiling
└── Container resource monitoring
```

### CI/CD Skills
```
├── GitHub Actions
│ ├── Multi-stage pipeline design
│ ├── Matrix testing (multi-version)
│ ├── Docker build & push
│ ├── Automated deployment triggers
│ └── Secret management
│ ├── Continuous Integration
│ ├── Lint on every push
│ ├── Test on every PR
│ ├── Build validation
│ └── Security scanning
│ └── Continuous Deployment
├── Staging auto-deploy (dev branch)
├── Production deploy (main, manual gate)
├── Health check verification
└── Rollback procedures
```

### Monitoring Skills
```
├── Uptime Monitoring
│ ├── Uptime Kuma setup & config
│ ├── HTTP/HTTPS endpoint checks
│ ├── Alert configuration (email/webhook)
│ └── Status page generation
│ ├── Error Tracking
│ ├── Sentry integration
│ ├── Error categorization
│ ├── Alert thresholds
│ └── Error resolution tracking
│ └── Log Analysis
├── Docker container logs
├── Application log parsing
├── Error pattern detection
└── Performance anomaly alerts
```

---

## John's Skill Set (The Hunter)

### Lead Generation Skills
```
├── Google Maps Scraping
│ ├── Location-based business search
│ ├── Multi-city batch scraping
│ ├── Data extraction (name, phone, website, rating, reviews)
│ ├── Rate limit management
│ └── Deduplication
│ ├── Apollo.io Enrichment
│ ├── Domain-based company lookup
│ ├── Decision-maker identification
│ ├── Contact info extraction (email, phone, LinkedIn)
│ ├── Company metadata (size, revenue, tech stack)
│ └── Bulk enrichment workflows
│ ├── Lead Qualification
│ ├── Scoring algorithms
│ ├── Segmentation (HOT/WARM/COLD)
│ ├── Ideal customer profile matching
│ └── Disqualification criteria
│ └── Outreach Automation
├── Email template personalization
├── Multi-touch drip sequences (n8n)
├── Follow-up timing optimization
├── Reply detection & routing
└── CRM integration (if applicable)
```

### Niche Research Skills
```
├── Market Sizing
│ ├── Google Maps count by location + niche
│ ├── Business density mapping
│ └── Growth trend analysis
│ └── Competitive Intelligence
├── Identify competitor customers
├── Technology stack detection
└── Pricing tier analysis
```

---

## TONY's Skill Set (The Marketer)

### Advertising Skills
```
├── Google Ads
│ ├── Search campaign architecture
│ ├── Display campaign setup
│ ├── Keyword research + grouping
│ ├── Negative keyword strategy
│ ├── Bid strategy selection
│ ├── Ad copy A/B testing
│ ├── Landing page optimization
│ └── Performance reporting
│ ├── Meta Ads (Facebook + Instagram)
│ ├── Campaign objective selection
│ ├── Audience creation (custom + lookalike)
│ ├── Creative development (image + video + carousel)
│ ├── Placement optimization
│ ├── Budget allocation
│ ├── Retargeting setup
│ └── Attribution tracking
│ └── Ad Analytics
├── CTR optimization
├── CPC/CPA tracking
├── ROAS calculation
├── Funnel analysis
└── Campaign iteration
```

### SEO Skills
```
├── On-Page SEO
│ ├── Title tag optimization
│ ├── Meta description writing
│ ├── Header hierarchy (H1-H6)
│ ├── Internal linking strategy
│ ├── Image alt text
│ ├── URL structure
│ └── Schema markup (JSON-LD)
│ ├── Technical SEO
│ ├── Sitemap generation
│ ├── robots.txt configuration
│ ├── Page speed optimization
│ ├── Mobile responsiveness
│ ├── Core Web Vitals
│ └── Canonical URLs
│ └── Content SEO
├── Keyword research (volume, difficulty, intent)
├── Content gap analysis
├── Blog post optimization
└── Long-tail keyword targeting
```

### Social Media Skills
```
├── Content Creation
│ ├── Platform-specific formatting
│ ├── Carousel design concepts
│ ├── Caption writing
│ ├── Hashtag strategy
│ ├── Call-to-action optimization
│ └── Content calendar planning
│ ├── Platform Management
│ ├── Instagram (posts, stories, reels)
│ ├── Facebook (pages, groups, events)
│ ├── LinkedIn (company pages, articles)
│ ├── X/Twitter (tweets, threads)
│ └── YouTube (descriptions, tags, playlists)
│ ├── Competitor Analysis
│ ├── Feature-by-feature comparison
│ ├── Pricing analysis
│ ├── Marketing channel audit
│ ├── Customer review mining (pain points)
│ └── Market positioning map
│ └── Sales Support
├── Cold email copywriting
├── Follow-up sequences
├── Objection handling scripts
├── Case study creation
└── Demo/landing page copy
```

---

## Skill Activation Protocol

When Alfred receives a task, he follows this decision tree:

```
INCOMING TASK
│
▼
Is it coding/architecture?
├── Yes → SAM (Opus 4.5)
│
▼
Is it testing/monitoring/CI?
├── Yes → MARK (Flash, escalate to Opus for fixes)
│
▼
Is it lead gen/scraping/outreach?
├── Yes → John (Flash)
│
▼
Is it marketing/ads/social/SEO?
├── Yes → TONY (Flash)
│
▼
Is it planning/coordination/reporting?
└── Yes → Alfred handles directly (Flash)
```

---

## Skill Gap Protocol

If a task requires a skill **none of the agents have**:

1. **Search open-source GitHub** for existing solutions
2. **Research documentation** with Gemini-3-Flash
3. **Prototype with minimal code** using SAM (Opus 4.5)
4. If still blocked → **escalate to human operator** with a research brief
