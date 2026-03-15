# ⚖️ OPENCLAW AGENT — RULES

> Hard rules. No exceptions. These govern every action Alfred and his sub-agents take.

---

## R1 — Model Routing Rules

> **CRITICAL: These rules are non-negotiable.**

| Task Type | Required Model | Rationale |
|-----------|---------------|-----------|
| Chat, Q&A, explanations | Gemini-3-Flash | Cheapest capable |
| Task decomposition | Gemini-3-Flash | Doesn't need deep reasoning |
| Lead generation queries | Gemini-3-Flash (John) | API calls, not code |
| Marketing copy, ad text | Gemini-3-Flash (TONY) | Creative but lightweight |
| SEO analysis | Gemini-3-Flash (TONY) | Analysis, not coding |
| Social media posts | Gemini-3-Flash (TONY) | Short-form content |
| **Architecture design** | **Opus 4.5 (SAM)** | Needs deep reasoning |
| **Production code** | **Opus 4.5 (SAM)** | Quality-critical |
| **Complex bug fixes** | **Opus 4.5 (MARK → SAM)** | Needs code understanding |
| **Database schema** | **Opus 4.5 (SAM)** | Data integrity matters |
| **CI/CD pipeline code** | **Opus 4.5 (SAM)** | Infrastructure-critical |
| Simple config changes | Gemini-3-Flash | No deep reasoning needed |
| Test writing | Gemini-3-Flash (MARK) | Pattern-based |
| Complex test debugging | Opus 4.5 (MARK) | Needs code understanding |

**Fallback:** If Gemini-3-Flash is unavailable → Gemini-3.1-Pro (NEVER Opus 4.5 for chat tasks).

---

## R2 — Token Budget Rules

### Per-Interaction Limits

| Context | Max Tokens (Output) |
|---------|-------------------|
| Alfred orchestration message | 500 |
| Sub-agent task assignment | 300 |
| Status report | 200 |
| SAM code generation | 4,000 |
| MARK test/report | 2,000 |
| John lead gen output | 1,000 |
| TONY marketing content | 1,500 |

### Token-Saving Mandates

1. **Reference, don't repeat** — Point to files instead of copying content
2. **Structured output only** — Use JSON/YAML/tables, not prose
3. **No "let me explain"** — Skip preambles, deliver answers directly
4. **Compress context** — When handing off between agents, send only relevant data
5. **Cache decisions** — Write decisions to files so they're never re-derived
6. **Batch operations** — Group related tasks into single agent calls

---

## R3 — Workspace Organization Rules

### Project Directory Structure

Every SaaS project MUST follow this structure:

```
/projects/{project-name}/
├── specs/ # Requirements, PRD, user stories
│ ├── prd.md
│ ├── features.md
│ └── api-spec.yaml
├── src/ # Source code (SAM's domain)
│ ├── backend/
│ ├── frontend/
│ ├── mobile/
│ └── shared/
├── tests/ # All tests (MARK's domain)
│ ├── unit/
│ ├── integration/
│ └── e2e/
├── infra/ # Docker, CI/CD, deployment
│ ├── docker/
│ ├── ci/
│ └── deploy/
├── marketing/ # TONY's domain
│ ├── ads/
│ ├── seo/
│ ├── social/
│ └── assets/
├── leads/ # John's domain
│ ├── raw/
│ ├── qualified/
│ └── outreach/
├── docs/ # Client-facing documentation
│ ├── setup-guide.md
│ ├── user-manual.md
│ └── api-docs.md
├── .env.example # Environment template (NEVER .env in git)
├── docker-compose.yml
├── README.md
└── CHANGELOG.md
```

### Naming Rules

- **Files:** `kebab-case.ext` (e.g., `user-auth.py`, `lead-scraper.js`)
- **Directories:** `kebab-case/`
- **Python modules:** `snake_case.py`
- **Classes:** `PascalCase`
- **Functions:** `snake_case`
- **Constants:** `UPPER_SNAKE_CASE`
- **Environment vars:** `UPPER_SNAKE_CASE` prefixed with `OPENCLAW_`

---

## R4 — Security Rules

### Secrets Management

1. **NEVER** hardcode API keys, passwords, or tokens in source code
2. **ALWAYS** use `.env` files (excluded from git via `.gitignore`)
3. **ALWAYS** provide `.env.example` with placeholder values
4. Use Docker secrets or environment variables for production
5. Rotate keys after any suspected exposure

### Code Security

1. Validate all inputs — Never trust user data
2. Parameterize SQL queries — No string concatenation
3. Use HTTPS everywhere — No HTTP in production
4. Implement rate limiting on all public APIs
5. Hash passwords with bcrypt (work factor >= 12)
6. JWT tokens expire within 24 hours; refresh tokens within 30 days
7. CORS restricted to known domains only

### Data Security

1. NEVER store client data outside the project directory
2. NEVER log sensitive data (passwords, tokens, PII)
3. Encrypt data at rest and in transit
4. Backup databases before migrations

---

## R5 — Quality Gates

### Before Code Merge (SAM → MARK)

- [ ] All unit tests pass
- [ ] No linting errors
- [ ] No security vulnerabilities (basic scan)
- [ ] Code follows project structure rules
- [ ] API endpoints documented

### Before Deployment (MARK → Alfred)

- [ ] All integration tests pass
- [ ] E2E tests pass on staging
- [ ] Docker containers build successfully
- [ ] Environment variables documented
- [ ] Database migrations tested
- [ ] Rollback procedure documented

### Before Client Delivery (Alfred → Client)

- [ ] Production deployment verified
- [ ] Client documentation complete
- [ ] Setup guide tested on clean environment
- [ ] Access credentials delivered securely
- [ ] Subscription/billing configured

---

## R6 — Deadline Management

### The 7-Day Sprint

| Day | Focus | Must Complete |
|-----|-------|--------------|
| 1 | Architecture + Setup | Project structure, DB schema, Docker setup |
| 2 | Core Backend | Auth, core API endpoints, database models |
| 3 | Core Frontend | Landing page, auth UI, main features UI |
| 4 | Feature Completion | All MVP features working end-to-end |
| 5 | Testing + Fixes | MARK runs full test suite, SAM fixes bugs |
| 6 | Marketing + Leads | TONY prepares ads/SEO, John generates leads |
| 7 | Deploy + Deliver | Production deployment, client handoff |

### The 14-Day Sprint

| Days | Focus |
|------|-------|
| 1-2 | Architecture, setup, core backend |
| 3-4 | Core frontend + mobile (if applicable) |
| 5-6 | Secondary features, integrations |
| 7-8 | Testing, bug fixes, performance tuning |
| 9-10 | Marketing assets, SEO, ad campaigns |
| 11-12 | Lead generation, outreach setup |
| 13 | Staging deployment, final QA |
| 14 | Production deployment, client delivery |

### Deadline Rules

1. **Scope cuts before deadline extensions** — Reduce features, never miss dates
2. **Daily progress is mandatory** — Every day must produce measurable output
3. **Blockers have a 2-hour timeout** — If stuck for 2 hours, escalate immediately
4. **End-of-day checkpoint** — Alfred reviews all agent progress

---

## R7 — Communication Rules

### Inter-Agent Format

```yaml
from: ALFRED
to: SAM
type: TASK_ASSIGN
priority: P1
task_id: PRJ-001-TASK-003
summary: "Build user authentication module"
deadline: "Day 3 EOD"
context_file: "/projects/medspa/specs/auth.md"
acceptance_criteria:
- JWT-based auth with refresh tokens
- Email + password login
- Password reset flow
- Unit tests for all endpoints
```

### Rules

1. **No free-form text** — All communication uses structured formats
2. **No redundant context** — Reference files, don't inline content
3. **Blockers reported immediately** — Don't wait for status check
4. **Progress reported at milestones** — Not on every function written

---

## R8 — Technology Rules

### Mandatory Stack (Default)

| Layer | Technology |
|-------|-----------|
| Backend | Python (FastAPI) |
| Frontend | Next.js or Vite + React |
| Mobile | React Native / Expo |
| Database | PostgreSQL |
| Cache | Redis |
| Queue | Celery + Redis |
| Container | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Orchestration | n8n (self-hosted) |
| Monitoring | Uptime Kuma (self-hosted) |

### Dependency Rules

1. Minimize dependencies — Every package is a liability
2. Pin versions — No floating versions in production
3. Audit before adding — Check last commit date, stars, vulnerabilities
4. Prefer stdlib — Use built-in libraries over third-party when possible

---

## R9 — Git Rules

1. **Branching:** `main` → `dev` → `feature/{name}` → PR → `dev` → `main`
2. **Commits:** Conventional commits (`feat:`, `fix:`, `docs:`, `chore:`)
3. **No force pushes** to `main` or `dev`
4. **PRs require** passing tests before merge
5. **One feature per branch**
6. **Tag releases** with semver (`v1.0.0`)

---

## R10 — Client Delivery Rules

### Deliverables Checklist

- [ ] Deployed application (accessible URL)
- [ ] Source code repository (transferred or shared)
- [ ] Admin credentials (sent securely)
- [ ] Setup guide (step-by-step)
- [ ] User manual (for end users)
- [ ] API documentation (if applicable)
- [ ] Subscription/billing setup
- [ ] Domain + SSL configured - [ ] Backup & recovery procedure
- [ ] 30-day support window documented
