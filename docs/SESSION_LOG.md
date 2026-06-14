# Session Log

## Last session
- **Date:** 2026-06-14
- **Completed:** P-008 (one-shot main.py) + P-009 (GitHub Actions workflow). 36/36 tests pass. Discord webhook URL set in config.json and bot running locally.
- **In progress:** —
- **Next up:** P-010 (manual): push repo to GitHub, add DISCORD_WEBHOOK_URL as repo secret, replace URL in config.json with placeholder before pushing

---

## Decision log

### 2026-06-14 — GitHub Actions deployment
P-008/P-009 done. main.py is now one-shot; cron runs every 15 min via GH Actions. SQLite DB cached between runs via actions/cache. Env var DISCORD_WEBHOOK_URL overrides config.json.

### 2026-06-14 — Full implementation in one session
P-001–P-006 all implemented and tested in one pass. 22 tests covering filters, db, vinted parsing, notifier, and imports. Venv at vinted-bot/.venv. Run with `.venv/bin/python main.py --dry-run`.

### 2026-06-14 — Framework adopted
Adopted Vlot orchestrator framework for this Python bot project. Agent roster simplified to core-engineer / database-engineer / notifier-engineer / testing-engineer. No work starts without explicit approval.
