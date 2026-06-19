# B-004 — False-positive Pikachu δ Nintendo Promo — delta keyword passes without set number in title

## Status
Investigating

## Severity
P2

## Root cause
`check_title_relevance` for single-component set numbers (e.g. `"35"`) only required a delta keyword
(`"delta"`, `"δ"`, `"species"`) to appear in the title. The bare number `"35"` itself was never required.
A listing titled `"Pikachu δ Nintendo promo"` contains the `δ` character and therefore passes, even
though it does not mention `"35"` and may not be the Nintendo Promo card at all.

## Fix
After the conflicting-X/Y check, add an additional gate for single-part set numbers:
if `parts[0]` (e.g. `"35"`) is not present anywhere in the title, reject immediately.
This means the listing must contain **both** the set number **and** a delta keyword to pass.

Multi-part set numbers (e.g. `"13/113"`) are unaffected — they already have their own two-component
match and X/Y conflict logic.

## Files touched
- `vinted-bot/filters.py`
- `vinted-bot/tests/test_filters.py`

## Verification
- T-023: `check_title_relevance("Pikachu δ Nintendo promo", "Pikachu δ", "35")` → False (no "35" in title)
- T-024: `check_title_relevance("Pikachu δ promo 35", "Pikachu δ", "35")` → True (has "35" + δ keyword)
