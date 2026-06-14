# P-001 — Project scaffold + requirements.txt

## Status
In Progress

## Agent
core-engineer

## Goal
Create the vinted-bot/ directory with all module stubs and a complete requirements.txt.

## Scope
- `vinted-bot/main.py`
- `vinted-bot/vinted.py`
- `vinted-bot/filters.py`
- `vinted-bot/db.py`
- `vinted-bot/notifier.py`
- `vinted-bot/config.json`
- `vinted-bot/requirements.txt`

## Acceptance criteria
- [ ] AC1: All module files exist with importable stubs (no import errors).
- [ ] AC2: `requirements.txt` lists all runtime and dev dependencies.
- [ ] AC3: `python main.py --dry-run` exits without crashing (stub loop).

## Verification
- T-001: Import all modules without error
- T-002: `python main.py --dry-run` exits with code 0

## Notes
Full implementations delegated to P-002 through P-006. Stubs only here.
