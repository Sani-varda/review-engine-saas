# 💓 OPENCLAW AGENT — HEARTBEAT

> Self-diagnostic, health monitoring, and continuous status awareness for Alfred and all sub-agents.

---

## Heartbeat Protocol

Alfred runs heartbeat checks at **three intervals**:

| Frequency | Check Type | Purpose |
|-----------|-----------|---------|
| **Per-task** | Task Completion Check | Verify each task produced expected output |
| **Per-sprint-day** | Daily Standup | Review day's progress, plan next day |
| **Per-project** | Project Health Audit | Full system check before delivery |

---

## 1. Task Completion Check (Per-Task)

Run after **every sub-agent task completes**:

```yaml
heartbeat_type: TASK_CHECK
task_id: PRJ-001-TASK-005
agent: SAM
checks:
  output_exists: true/false
  output_valid: true/false
  tests_pass: true/false
  no_errors: true/false
  within_budget: true/false
result: HEALTHY | DEGRADED | FAILED
```

### Decision Matrix

| Checks Passing | Status | Action |
|---------------|--------|--------|
| 5/5 | ✅ HEALTHY | Proceed to next task |
| 3-4/5 | ⚠️ DEGRADED | Auto-fix, then re-check |
| 0-2/5 | ❌ FAILED | Retry → Escalate → Block |

---

## 2. Daily Standup (Per-Sprint-Day)

Run at the **end of each working day**:

```yaml
heartbeat_type: DAILY_STANDUP
project: medspa-booking
sprint_day: 3 of 7
agents:
  SAM:
    status: ACTIVE
    tasks_completed: 4
    tasks_remaining: 6
    blockers: []
    token_usage: 12,400
  MARK:
    status: ACTIVE
    tests_written: 15
    tests_passing: 14
    tests_failing: 1
    token_usage: 3,200
  John:
    status: ACTIVE
    leads_found: 47
    leads_qualified: 12
    token_usage: 1,800
  TONY:
    status: IDLE
    reason: "Marketing phase starts Day 5"
    token_usage: 0
overall:
  schedule: ON_TRACK | BEHIND | AHEAD
  total_tokens_used: 17,400
  token_budget_remaining: 82,600
  tomorrow_focus: "Complete payment integration + Start mobile UI"
```

### Rules
1. **Must run** — Even if no progress was made
2. **Honest assessment** — Never lie about ON_TRACK status
3. **Actionable** — Every blocker must have a proposed resolution
4. **Forward-looking** — Always define tomorrow's focus

---

## 3. Project Health Audit (Pre-Delivery)

Run **before any client delivery**:

```yaml
heartbeat_type: PROJECT_AUDIT
code_health:
  all_tests_pass: true/false
  test_coverage: "XX%"
  lint_clean: true/false
  no_hardcoded_secrets: true/false
  dependencies_pinned: true/false
infrastructure_health:
  docker_builds: true/false
  containers_healthy: true/false
  database_migrated: true/false
  ssl_configured: true/false
  backups_configured: true/false
documentation_health:
  readme_exists: true/false
  setup_guide_tested: true/false
  api_docs_current: true/false
  env_example_exists: true/false
marketing_health:
  landing_page_live: true/false
  seo_meta_configured: true/false
  ad_campaigns_ready: true/false
lead_gen_health:
  leads_database_populated: true/false
  outreach_templates_ready: true/false
result: READY_TO_SHIP | NEEDS_WORK | CRITICAL_ISSUES
```

---

## 4. Self-Healing Protocol

```
FAILURE DETECTED
▼
STEP 1: Auto-Diagnose
  → Read error logs
  → Identify root cause
  → Check known-issues registry
▼
STEP 2: Auto-Fix (Gemini-3-Flash)
  → Apply known fix or generate one
  → Re-run failed check
  → Pass? → ✅ Resume
▼
STEP 3: Escalate to Opus 4.5 (SAM)
  → Full context analysis
  → Generate deeper fix
  → Re-run failed check
  → Pass? → ✅ Resume
▼
STEP 4: Escalate to Human Operator
  → Log full error context
  → Send notification
  → Block task until resolved
```

### Known Issue Auto-Fixes

| Category | Auto-Fix Strategy |
|----------|------------------|
| Dependency conflict | Update requirements, rebuild container |
| Port already in use | Kill process, retry on alternate port |
| Test flaky | Re-run 3x, quarantine if intermittent |
| API rate limit | Exponential backoff, rotate key |
| Build failure | Clear cache, rebuild from scratch |
| Database connection | Check env vars, restart DB container |
| Out of disk | Clean Docker volumes, old logs |
| Git conflict | Auto-merge if clean, escalate if complex |

---

## 5. Health Dashboard

```
╔══════════════════════════════════════════════╗
║        OPENCLAW HEALTH DASHBOARD             ║
║ Project: medspa-booking                      ║
║ Sprint Day: 3/7                              ║
╠══════════════════════════════════════════════╣
║ 🤖 AGENTS                                    ║
║ ├── Alfred ✅ ACTIVE                         ║
║ ├── SAM    ✅ ACTIVE                         ║
║ ├── MARK   ✅ ACTIVE                         ║
║ ├── John   ✅ ACTIVE                         ║
║ └── TONY   ⏸️  IDLE (Day 5)                   ║
║                                              ║
║ 📊 PROGRESS                                  ║
║ ├── Tasks:  8/20  [████░░░░░░] 40%           ║
║ ├── Tests: 14/15  [█████████░] 93%           ║
║ ├── Bugs:   1 open                           ║
║ └── Schedule: ✅ ON TRACK                    ║
║                                              ║
║ 💰 TOKENS                                    ║
║ ├── Today:  5,200                            ║
║ ├── Total: 17,400                            ║
║ └── Remaining: 82,600                        ║
╚══════════════════════════════════════════════╝
```

---

## 6. Heartbeat Storage

```
/projects/{project-name}/.heartbeat/
├── daily/
│   ├── day-01.yaml
│   └── day-02.yaml
├── tasks/
│   ├── TASK-001.yaml
│   └── TASK-002.yaml
├── audits/
│   └── pre-delivery.yaml
└── incidents/
    └── INC-001.yaml
```
