# Plan Tracker

## Legend
| Status | Meaning |
|---|---|
| Planned | Logged, not started |
| In Progress | Implementation underway |
| Done | Implementation complete + tests registered |
| Cancelled | Will not implement |

---

## Features

| ID | Title | Status | Agent | Notes |
|---|---|---|---|---|
| P-001 | Project scaffold + requirements.txt | Done | core-engineer | T-001 passing |
| P-002 | vinted.py — Vinted catalog search | Done | core-engineer | T-013, T-014, T-015 passing |
| P-003 | filters.py — language, condition, price | Done | core-engineer | T-002..T-008 passing |
| P-004 | db.py — SQLite seen-listings | Done | database-engineer | T-009..T-012 passing |
| P-005 | notifier.py — Telegram delivery | Done | notifier-engineer | T-016..T-018 passing |
| P-006 | main.py — polling loop + --dry-run | Done | core-engineer | 22/22 tests pass |
| P-007 | config.json — card list + settings | Done | core-engineer | 43 cards from Excel, max_price = typical sale price, token placeholders remain |

## Refactors

| ID | Title | Status | Agent | Notes |
|---|---|---|---|---|

## Infrastructure / Tooling

| ID | Title | Status | Agent | Notes |
|---|---|---|---|---|
| P-008 | main.py — one-shot mode + env var webhook | Done | core-engineer | 36/36 tests pass |
| P-009 | GitHub Actions cron workflow | Done | infrastructure | .github/workflows/vinted-bot.yml created |
| P-011 | db.py — card sightings tracking | Done | database-engineer | 36/36 tests pass |
| P-012 | notifier.py — run debrief Discord message | Done | notifier-engineer | Visual embed with emoji dots + match highlights |
| P-013 | filters.py — recency filter (30-day max age) | Done | core-engineer | 36/36 tests pass |
| P-014 | image_check.py — Claude vision English-language card check | Done | core-engineer | T-019..T-022 passing, 50/50 tests pass |
| P-016 | filters.py — relax single-part set number to not require delta keyword | Done | core-engineer | T-033 passing, 61/61 tests pass |
