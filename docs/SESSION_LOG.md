# Session Log

## Last session
- **Date:** 2026-06-14
- **Completed:** P-011 (card sightings DB) + P-012 (visual run debrief). Bot live on GitHub Actions, first real match caught (Heracross δ €9.89). 36/36 tests pass.
- **In progress:** —
- **Next up:** Add card image thumbnail to match notification (listing photo from Vinted API already extracted in _parse)

---

## Decision log

### 2026-06-14 — GitHub Actions deployment
P-008/P-009 done. main.py is now one-shot; cron runs every 15 min via GH Actions. SQLite DB cached between runs via actions/cache. Env var DISCORD_WEBHOOK_URL overrides config.json.

### 2026-06-14 — Full implementation in one session
P-001–P-006 all implemented and tested in one pass. 22 tests covering filters, db, vinted parsing, notifier, and imports. Venv at vinted-bot/.venv. Run with `.venv/bin/python main.py --dry-run`.

### 2026-06-14 — Framework adopted
Adopted Vlot orchestrator framework for this Python bot project. Agent roster simplified to core-engineer / database-engineer / notifier-engineer / testing-engineer. No work starts without explicit approval.
