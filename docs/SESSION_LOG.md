# Session Log

## Last session
- **Date:** 2026-06-16
- **Completed:** B-002 — false-positive Discord alert for Pikachu (EVO 35 Evoluties) matching Nintendo Promo Pikachu search. Fixed `check_title_relevance` to require ≥2 set-number parts before skipping delta keyword check. 35 tests pass.
- **In progress:** —
- **Next up:** Add card image thumbnail to match notification (listing photo from Vinted API already extracted in _parse)

---

## Decision log

### 2026-06-16 — B-002 false-positive Pikachu EVO 35 notification
Single-token set numbers (e.g. "35") were bypassing the delta keyword check. Fixed by requiring ≥2 parts before the set-number shortcut fires. Two regression tests added.

### 2026-06-15 — B-001 recency filter fix
Vinted catalog API dropped all date fields. `check_recency(None)` now returns `True` (pass through). DB deduplication prevents repeat notifications for the same listing.

### 2026-06-14 — GitHub Actions deployment
P-008/P-009 done. main.py is now one-shot; cron runs every 15 min via GH Actions. SQLite DB cached between runs via actions/cache. Env var DISCORD_WEBHOOK_URL overrides config.json.

### 2026-06-14 — Full implementation in one session
P-001–P-006 all implemented and tested in one pass. 22 tests covering filters, db, vinted parsing, notifier, and imports. Venv at vinted-bot/.venv. Run with `.venv/bin/python main.py --dry-run`.

### 2026-06-14 — Framework adopted
Adopted Vlot orchestrator framework for this Python bot project. Agent roster simplified to core-engineer / database-engineer / notifier-engineer / testing-engineer. No work starts without explicit approval.
