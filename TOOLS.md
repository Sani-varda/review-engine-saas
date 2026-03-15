# 🔧 OPENCLAW AGENT — TOOLS

> Complete inventory of tools, APIs, and integrations available to Alfred and sub-agents.

---

## Tool Categories

| Category | Tools | Primary User |
|----------|-------|-------------|
| **Core Development** | Python, Node.js, Docker | SAM |
| **Frameworks** | FastAPI, Next.js, React Native | SAM |
| **Databases** | PostgreSQL, Redis, SQLite | SAM |
| **Automation** | n8n, GitHub Actions, Celery | SAM, MARK |
| **Lead Generation** | Google Maps API, Apollo.io API | John |
| **Marketing** | Google Ads API, Meta Ads API | TONY |
| **Social Media** | Instagram API, LinkedIn API, X API | TONY |
| **Monitoring** | Uptime Kuma, Docker health checks | MARK |
| **Version Control** | Git, GitHub | All |
| **Deployment** | Docker Compose, Nginx, Certbot | SAM |

---

## 1. Core Development Tools

### Python Ecosystem

| Tool | Purpose | Install |
|------|---------|---------|
| **Python 3.11+** | Primary backend language | System |
| **FastAPI** | Async REST API framework | `pip install fastapi[all]` |
| **SQLAlchemy** | ORM for PostgreSQL | `pip install sqlalchemy` |
| **Alembic** | Database migrations | `pip install alembic` |
| **Pydantic** | Data validation & schemas | `pip install pydantic` |
| **Celery** | Async task queue | `pip install celery` |
| **pytest** | Unit/integration testing | `pip install pytest` |
| **httpx** | Async HTTP client (testing) | `pip install httpx` |
| **ruff** | Fast Python linter | `pip install ruff` |
| **uvicorn** | ASGI server | `pip install uvicorn` |
| **python-jose** | JWT token handling | `pip install python-jose[cryptography]` |
| **passlib** | Password hashing (bcrypt) | `pip install passlib[bcrypt]` |
| **python-dotenv** | Environment variable loading | `pip install python-dotenv` |
| **Jinja2** | Email/template rendering | `pip install jinja2` |
| **requests** | HTTP client (sync) | `pip install requests` |

### Node.js / Frontend

| Tool | Purpose | Install |
|------|---------|---------|
| **Node.js 20+** | Frontend runtime | System |
| **Next.js 14+** | React framework (SSR/SSG) | `npx create-next-app` |
| **Vite** | Fast frontend build tool | `npm create vite` |
| **React** | UI component library | (via Next.js/Vite) |
| **TypeScript** | Type-safe JavaScript | (via Next.js/Vite) |
| **Vitest** | Frontend unit testing | `npm install vitest` |
| **Playwright** | E2E browser testing | `npm install @playwright/test` |
| **ESLint** | JavaScript linting | `npm install eslint` |
| **Tailwind CSS** | Utility-first CSS | `npm install tailwindcss` |

### Mobile

| Tool | Purpose | Install |
|------|---------|---------|
| **React Native** | Cross-platform mobile | `npx react-native init` |
| **Expo** | React Native framework | `npx create-expo-app` |
| **EAS Build** | Cloud builds for mobile | `npm install -g eas-cli` |

---

## 2. Infrastructure & DevOps

### Containerization

| Tool | Purpose | Config |
|------|---------|--------|
| **Docker** | Container runtime | System install |
| **Docker Compose** | Multi-container orchestration | `docker-compose.yml` |
| **Nginx** | Reverse proxy + SSL | Docker container |
| **Certbot** | Free SSL certificates (Let's Encrypt) | Docker container |

### CI/CD

| Tool | Purpose | Config |
|------|---------|--------|
| **GitHub Actions** | CI/CD pipelines (free) | `.github/workflows/` |
| **GitHub Container Registry** | Docker image hosting (free) | `ghcr.io` |

### Monitoring (Open-Source)

| Tool | Purpose | Deploy |
|------|---------|--------|
| **Uptime Kuma** | Uptime monitoring + alerts | Docker (self-hosted) |
| **Docker Healthchecks** | Container health monitoring | docker-compose.yml |
| **Sentry** (free tier) | Error tracking | SDK integration |

---

## 3. Databases

| Database | Use Case | Deploy |
|----------|----------|--------|
| **PostgreSQL** | Primary relational database | Docker |
| **Redis** | Caching + Celery broker + sessions | Docker |
| **SQLite** | Local dev, lightweight apps | File-based |

### Database Tools

| Tool | Purpose |
|------|---------|
| **Alembic** | Schema migrations (Python) |
| **Prisma** | ORM + migrations (Node.js) |
| **pgAdmin** | PostgreSQL GUI (Docker) |
| **Redis Commander** | Redis GUI (Docker) |

---

## 4. Automation & Workflows

### n8n (Self-Hosted)

| Feature | Usage |
|---------|-------|
| **Purpose** | Visual workflow automation |
| **Deploy** | Docker (self-hosted, free) |
| **Use Cases** | Lead outreach drips, social media posting, error alerts, daily reports |
| **Integration** | Webhooks, HTTP requests, email, Slack |

```yaml
# docker-compose.yml snippet for n8n
n8n:
  image: n8nio/n8n
  ports:
    - "5678:5678"
  environment:
    - N8N_BASIC_AUTH_ACTIVE=true
    - N8N_BASIC_AUTH_USER=admin
    - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
  volumes:
    - n8n_data:/home/node/.n8n
```

### Celery (Python)

| Feature | Usage |
|---------|-------|
| **Purpose** | Async task processing |
| **Broker** | Redis |
| **Use Cases** | Email sending, lead enrichment, report generation |

---

## 5. Lead Generation APIs

### Google Maps API

| Endpoint | Purpose | Rate Limit |
|----------|---------|-----------|
| **Places Search** | Find businesses by query + location | 1 QPS default |
| **Place Details** | Get phone, website, hours, reviews | 1 QPS default |
| **Geocoding** | Convert addresses to coordinates | 50 QPS |

```python
# Usage pattern
import googlemaps
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))
results = gmaps.places(
    query="med spa",
    location=(30.2672, -97.7431), # Austin, TX
    radius=50000
)
for place in results["results"]:
    details = gmaps.place(place["place_id"])
    # Extract: name, phone, website, rating, reviews
```

### Apollo.io API

| Endpoint | Purpose | Docs |
|----------|---------|------|
| **People Search** | Find decision-makers | api.apollo.io |
| **Organization Search** | Find company details | api.apollo.io |
| **Enrichment** | Enrich contact/company data | api.apollo.io |

```python
# Usage pattern
import requests
headers = {"x-api-key": os.getenv("APOLLO_API_KEY")}
response = requests.post(
    "https://api.apollo.io/api/v1/mixed_people/search",
    headers=headers,
    json={
        "person_titles": ["owner", "manager"],
        "organization_domains": ["example-medspa.com"]
    }
)
```

---

## 6. Marketing & Ads APIs

### Google Ads API

| Feature | Usage |
|---------|-------|
| **Campaign Management** | Create/update search + display campaigns |
| **Keyword Planning** | Research keyword volumes + CPC |
| **Reporting** | Pull performance metrics |
| **Authentication** | OAuth 2.0 |

### Meta (Facebook/Instagram) Ads API

| Feature | Usage |
|---------|-------|
| **Campaign Creation** | Create ad campaigns with targeting |
| **Ad Creative** | Upload images/videos, create ad copy |
| **Audience Targeting** | Custom + Lookalike audiences |
| **Reporting** | Performance metrics, ROAS |
| **Authentication** | Facebook Login + Marketing API access |

### Social Media APIs

| Platform | API | Actions |
|----------|-----|---------|
| **Instagram** | Graph API | Post images, stories, get insights |
| **Facebook** | Graph API | Page posts, comments, events |
| **LinkedIn** | Marketing API | Company posts, articles |
| **X (Twitter)** | API v2 | Tweets, threads, analytics |
| **YouTube** | Data API v3 | Upload videos, manage playlists |

---

## 7. Communication & Email

| Tool | Purpose | Cost |
|------|---------|------|
| **Resend** | Transactional email | Free tier (100/day) |
| **SendGrid** | Email at scale | Free tier (100/day) |
| **Twilio** | SMS + WhatsApp | Pay-per-use |
| **SMTP (Mailtrap)** | Email testing | Free tier |

---

## 8. Open-Source Alternatives Registry

> Alfred ALWAYS checks this table before recommending a paid tool.

| Need | Paid Option | Free/Open-Source Alternative |
|------|------------|----------------------------|
| Workflow automation | Zapier | **n8n** (self-hosted) |
| Uptime monitoring | Pingdom | **Uptime Kuma** (self-hosted) |
| Error tracking | Datadog | **Sentry** (free tier) |
| Analytics | Mixpanel | **Plausible/Umami** (self-hosted) |
| Email marketing | Mailchimp | **Listmonk** (self-hosted) |
| CRM | Salesforce | **Twenty CRM** (open-source) |
| Project management | Jira | **Plane** (open-source) |
| Form builder | Typeform | **Tally** (free tier) |
| Landing pages | Unbounce | **Next.js** (custom build) |
| Authentication | Auth0 | **Supabase Auth** (free tier) |
| File storage | S3 | **MinIO** (self-hosted) |
| Database admin | — | **pgAdmin / Redis Commander** |
| Logs | Datadog | **Loki + Grafana** (self-hosted) |
| Container registry | Docker Hub | **GitHub Container Registry** (free) |
| SSL certificates | Paid CAs | **Let's Encrypt** (free) |
| DNS | Cloudflare Pro | **Cloudflare** (free tier) |

---

## 9. Development Environment

### Required System Tools

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Backend development |
| Node.js | 20+ | Frontend development |
| Docker | latest | Containerization |
| Docker Compose | v2+ | Service orchestration |
| Git | latest | Version control |
| GitHub CLI (`gh`) | latest | GitHub operations from CLI |

### IDE / Editor (Human Operator)

- **VS Code** with extensions: Python, ESLint, Prettier, Docker, GitLens
- **Google Antigravity** as AI coding assistant

### Environment Variables Template

```env
# .env.example — NEVER commit actual .env files
# Core
OPENCLAW_ENV=development
OPENCLAW_DEBUG=true

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
REDIS_URL=redis://localhost:6379/0

# Auth
JWT_SECRET_KEY=change-me-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRY_MINUTES=1440

# APIs
GOOGLE_MAPS_API_KEY=your-key-here
APOLLO_API_KEY=your-key-here
GOOGLE_ADS_CLIENT_ID=your-id-here
META_ADS_ACCESS_TOKEN=your-token-here

# Email
RESEND_API_KEY=your-key-here
SENDGRID_API_KEY=your-key-here

# Social Media
INSTAGRAM_ACCESS_TOKEN=your-token-here
LINKEDIN_ACCESS_TOKEN=your-token-here
TWITTER_API_KEY=your-key-here

# n8n
N8N_PASSWORD=your-password-here
```
