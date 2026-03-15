# 📋 OPENCLAW AGENT — TASK MANAGEMENT

> How tasks are created, prioritized, assigned, tracked, and completed.

---

## Task Lifecycle

```
CREATED → ASSIGNED → IN_PROGRESS → IN_REVIEW → DONE
      │          │            │             ▲
      ▼          ▼            ▼             │
   BLOCKED    FAILED → RETRY → ESCALATED
```

---

## Priority Levels

| Level | Label | Response Time | Examples |
|-------|-------|--------------|----------|
| **P0** | 🔴 CRITICAL | Immediate | Production down, data loss |
| **P1** | 🟠 HIGH | Same day | Core feature bug, deployment blocker |
| **P2** | 🟡 MEDIUM | Next day | Non-core bug, UI polish |
| **P3** | 🟢 LOW | This sprint | Documentation, refactor |

---

## Task Format

```yaml
task_id: PRJ-001-TASK-007
project: medspa-booking
title: "Build appointment booking API"
priority: P1
status: IN_PROGRESS
assigned_to: SAM
model: Opus 4.5
deadline: 2026-03-03T18:00:00Z
sprint_day: 3
dependencies:
  - PRJ-001-TASK-003 # Auth module
  - PRJ-001-TASK-005 # Database models
acceptance_criteria:
  - CRUD endpoints for appointments
  - Conflict detection (no double-booking)
  - Pydantic validation
  - JWT auth required
  - Unit tests
context_files:
  - /projects/medspa/specs/prd.md
  - /projects/medspa/specs/api-spec.yaml
output:
  path: /src/backend/routes/appointments.py
  tests: /tests/unit/test_appointments.py
estimated_tokens: 3000
```

---

## Assignment Rules

| Task Category | Agent | Model |
|--------------|-------|-------|
| Backend/frontend/mobile code | SAM | Opus 4.5 |
| Database schema/migrations | SAM | Opus 4.5 |
| Docker/CI/CD config | SAM | Opus 4.5 |
| Unit/integration/E2E tests | MARK | Gemini-3-Flash |
| Bug fixes (simple) | MARK | Gemini-3-Flash |
| Bug fixes (complex) | SAM | Opus 4.5 |
| Monitoring setup | MARK | Gemini-3-Flash |
| Lead scraping/enrichment | John | Gemini-3-Flash |
| Outreach automation | John | Gemini-3-Flash |
| Ad campaigns | TONY | Gemini-3-Flash |
| SEO/social/content | TONY | Gemini-3-Flash |
| Planning/coordination | Alfred | Gemini-3-Flash |

---

## Task Dependencies (DAG)

```
TASK-001: Project Setup ─────────────────────┐
TASK-002: Database Models ──────────┐       │
TASK-003: Auth Module ─────────────┐│       │
                                    ││       │
TASK-004: Booking API ◄────────────┘│       │
TASK-005: Client Mgmt API ◄────────┘       │
                                            │
TASK-006: Frontend Auth ◄───────────────────┘
TASK-007: Dashboard UI ◄── TASK-004 + TASK-005
TASK-008: Landing Page ◄── TASK-001
TASK-009: Unit Tests ◄── TASK-003 + TASK-004
TASK-010: Integration Tests ◄── TASK-009
TASK-011: SEO Setup ◄── TASK-008
TASK-012: Lead Scraping ◄── TASK-001
TASK-013: Ad Campaign ◄── TASK-008 + TASK-011
TASK-014: Deployment ◄── TASK-010
TASK-015: Client Delivery ◄── TASK-014
```

### Rules
1. No task starts before dependencies are DONE
2. Parallel tasks run simultaneously
3. Blocked tasks auto-requeue when blocker resolves

---

## Sprint Board Format

```markdown
## Sprint Board: MedSpa Booking (Day 3/7)

### 🔴 BLOCKED (none)

### 🔵 IN PROGRESS
| ID | Task | Agent | Progress | ETA |
|----|------|-------|----------|-----|
| TASK-004 | Booking API | SAM | 60% | Today |
| TASK-009 | Unit Tests | MARK | 40% | Today |

### ✅ DONE
| ID | Task | Agent | Day |
|----|------|-------|-----|
| TASK-001 | Project Setup | SAM | 1 |
| TASK-002 | DB Models | SAM | 1 |
| TASK-003 | Auth Module | SAM | 2 |

### 📋 TODO
| ID | Task | Agent | Priority | Depends |
|----|------|-------|----------|---------|
| TASK-005 | Client API | SAM | P1 | TASK-002 ✅ |
| TASK-007 | Dashboard | SAM | P1 | TASK-004/005 |
```

---

## Completion Report

```yaml
task_id: PRJ-001-TASK-003
status: DONE
agent: SAM
tokens_used: 2,847
files_created:
  - /src/backend/auth/router.py
  - /src/backend/auth/service.py
tests_passing: 8/8
next_unblocked:
  - TASK-004
  - TASK-006
  - TASK-009
```

---

## Escalation Protocol

| Condition | Action |
|-----------|--------|
| Stuck > 2 hours | Report BLOCKED to Alfred |
| 2 failed retries | Re-route to Opus 4.5 |
| 3 failed retries | Escalate to human |
| Deadline at risk | Trigger scope cut |
| Token budget exceeded | Alfred reviews and decides |

---

## Storage

```
/projects/{project}/.tasks/
├── backlog.yaml
├── sprint-board.yaml
├── completed.yaml
└── incidents.yaml
```
