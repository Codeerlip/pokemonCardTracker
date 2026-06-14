# P-008 — main.py — one-shot mode + env var webhook

## Status
In Progress

## Agent
core-engineer

## Goal
Remove the while loop so main.py exits after one full pass; read DISCORD_WEBHOOK_URL from env var with fallback to config.json for local runs.

## Scope
- `vinted-bot/main.py`

## Acceptance criteria
- [ ] AC1: Running `python main.py` completes and exits (no infinite loop)
- [ ] AC2: `DISCORD_WEBHOOK_URL` env var overrides config.json value when set
- [ ] AC3: `--dry-run` still works locally

## Verification
- Existing tests (T-001–T-022) must still pass

## Notes
- Polling interval is now controlled entirely by GitHub Actions cron schedule
- Local users can still use config.json for the webhook URL
