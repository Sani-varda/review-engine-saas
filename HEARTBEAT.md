# 💓 HEARTBEAT.md — OpenClaw Continuous Work Loop

## THE HEARTBEAT LOOP

1. READ BOARD
   └─ Load BOARD.md → identify highest priority active task
2. ASSESS STATE
   └─ What was last completed?
   └─ What is the next subtask?
3. EXECUTE
   ├─ (If coding) → Call SAM (Opus 4.5)
   ├─ (If lead gen/marketing) → Call John/TONY (Flash)
   └─ (If planning) → Alfred handles (Flash)
4. TEST & COMMIT
   └─ Run tests, git add/commit/push
5. UPDATE BOARD
   └─ Check off completed tasks, update BOARD.md
6. SLEEP
   └─ Pause based on intensity (Default: 15-min)

---

## FIX LOOP (Alfred Protocol)

When a test or build fails:
1. Attempt 1: Identify root cause, apply minimal targeted fix.
2. Attempt 2: Expand context, apply deeper fix.
3. Attempt 3: Architectural fix/restructure.
4. After 3 fails: Log full diagnosis to .logs/fixes.md, flag to human.

---

## INTENSITY SETTINGS

| Mode | Cycle Interval | Use When |
|------|---------------|----------|
| `SPRINT` | Continuous (no sleep) | < 2 days to deadline |
| `STANDARD` | 15-min cycles | 3-6 days to deadline |
| `CRUISE` | 60-min cycles | > 6 days, low urgency |
| `IDLE` | Manual trigger only | No active tasks |

Default: `STANDARD`
