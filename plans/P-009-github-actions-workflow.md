# P-009 — GitHub Actions cron workflow

## Status
In Progress

## Agent
infrastructure

## Goal
Create .github/workflows/vinted-bot.yml to run the bot every 15 minutes, with SQLite persistence via actions/cache and Discord webhook injected from GitHub Secrets.

## Scope
- `.github/workflows/vinted-bot.yml` (new file)

## Acceptance criteria
- [ ] AC1: Workflow triggers on schedule (*/15 * * * *) and workflow_dispatch
- [ ] AC2: seen_listings.db is cached and restored between runs
- [ ] AC3: DISCORD_WEBHOOK_URL is read from GitHub Secret (not config.json)
- [ ] AC4: Bot completes without error on ubuntu-latest

## Verification
- Manual workflow_dispatch run completes successfully
- Second run shows deduplication working (no duplicate Discord messages)

## Notes
- Cache key uses run_id so each run saves a new cache entry; restore-keys picks up most recent
- Free tier: unlimited minutes for public repos; 2,000 min/mo for private
