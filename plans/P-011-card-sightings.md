# P-011 — db.py — card sightings tracking

## Status
In Progress

## Agent
database-engineer

## Goal
Track how many Vinted listings appear per card per run so scarcity can be assessed over time.

## Scope
- `vinted-bot/db.py`

## Acceptance criteria
- [ ] AC1: `record_sightings(card_name, count)` upserts into card_sightings table
- [ ] AC2: `get_all_sightings()` returns dict of card_name → {total_seen, runs_checked}
- [ ] AC3: Table created automatically on first connect

## Verification
- T-NNN: record_sightings increments total_seen and runs_checked correctly
- T-NNN: get_all_sightings returns correct aggregated data

## Notes
- total_seen / runs_checked = average listings per run (scarcity signal)
- Counts include all listings returned by Vinted, not just new/unmatched ones
