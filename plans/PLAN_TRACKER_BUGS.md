# Bug Tracker

## Legend
| Severity | Meaning |
|---|---|
| P0 | Critical / data-loss or silent duplicate notifications |
| P1 | Major / broken feature |
| P2 | Minor / degraded UX |
| P3 | Cosmetic |

| Status | Meaning |
|---|---|
| Open | Logged, not investigated |
| Investigating | Root cause analysis in progress |
| Fixed | Fix applied and verified |
| Wontfix | Accepted risk, will not fix |

---

## Bugs

| ID | Title | Severity | Status | Notes |
|---|---|---|---|---|
| B-001 | Recency filter rejects all listings — Vinted API dropped timestamp fields | P1 | Fixed | `created_at_ts`/`created_at` absent from catalog response; None → False silenced all alerts |
