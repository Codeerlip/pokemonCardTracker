# B-002 — False-positive notification for non-delta Pikachu (EVO 35)

## Status
Fixed

## Severity
P2 — degraded UX (unwanted Discord notification)

## Agent
core-engineer

## Root cause
`check_title_relevance` in `filters.py` has a set-number shortcut that returns `True` as soon as all parts of `set_number` appear in the title, skipping the delta-keyword check entirely. For the Nintendo Promo Pikachu (set_number `"35"`), `parts = ["35"]` — a single generic token. The listing "Pikachu (EVO 35) Evoluties" contains both "pikachu" and "35", so the shortcut fires and the listing passes despite being from the Evolutions set.

## Fix
Require `len(parts) >= 2` before the set-number shortcut can fire. Single-component set numbers (like `"35"`) fall through to the existing delta/δ/species keyword check, which correctly rejects "Evoluties" listings.

## Files changed
- `vinted-bot/filters.py` — condition on `len(parts) >= 2`
- `vinted-bot/tests/test_filters.py` — two regression tests added

## Verification
- T-042: `check_title_relevance("Pikachu (EVO 35) Evoluties", "Pikachu δ", "35")` → `False`
- T-043: `check_title_relevance("Pikachu delta promo 35", "Pikachu δ", "35")` → `True`
