# P-012 — notifier.py — run debrief Discord message

## Status
In Progress

## Agent
notifier-engineer

## Goal
After each run, post one Discord embed summarising matches found and card visibility — only when at least one listing was seen across all cards.

## Scope
- `vinted-bot/notifier.py`
- `vinted-bot/main.py`

## Acceptance criteria
- [ ] AC1: send_debrief() posts one embed per run (not per card)
- [ ] AC2: Embed shows matches and per-card listing counts for cards with sightings > 0
- [ ] AC3: Debrief not sent when total listings found = 0 (no noise on empty runs)
- [ ] AC4: Debrief not sent in --dry-run mode

## Verification
- T-NNN: send_debrief posts correct embed payload
- T-NNN: send_debrief not called when total_found = 0

## Notes
- Fires after full pass through all 43 cards, not per card
- Zero-sighting cards omitted from visibility list to keep embed compact
