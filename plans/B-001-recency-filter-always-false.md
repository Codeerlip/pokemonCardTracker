---
name: B-001-recency-filter-always-false
description: Vinted catalog API no longer returns date fields; check_recency returns False for all listings, silencing every alert
metadata:
  type: bug
  severity: P1
  status: Fixed
---

## Root cause

Vinted's catalog API (`/api/v2/catalog/items`) dropped `created_at_ts` and `created_at`
from item payloads. `_parse()` in `vinted.py` sets `created_at_ts = None` for every
listing. `check_recency(None, ...)` hit the guard `if not created_at_ts: return False`,
rejecting 100% of listings before any notification could fire.

## Fix

`filters.py` — `check_recency`: when `created_at_ts` is `None`, return `True` (pass
through). The DB `mark_seen()` deduplication ensures each listing fires at most once,
so an old listing triggers one notification and is permanently suppressed.

## Verification

- `test_check_recency_none_ts_passes` added to `test_filters.py`
- `pytest` 36/36 pass
