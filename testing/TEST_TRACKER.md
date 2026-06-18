# Test Tracker

## Legend
| Status | Meaning |
|---|---|
| Passing | Test exists and passes |
| Failing | Test exists but fails |
| Planned | Test defined in plan, not yet written |

---

## Tests

| ID | Title | Plan | Status | File |
|---|---|---|---|---|
| T-001 | All modules importable without error | P-001 | Passing | tests/test_imports.py |
| T-002 | detect_language returns dutch for Dutch markers | P-003 | Passing | tests/test_filters.py |
| T-003 | detect_language returns english for English markers | P-003 | Passing | tests/test_filters.py |
| T-004 | detect_language returns unknown for ambiguous text | P-003 | Passing | tests/test_filters.py |
| T-005 | check_condition allows good/new/like_new | P-003 | Passing | tests/test_filters.py |
| T-006 | check_condition rejects satisfactory/poor | P-003 | Passing | tests/test_filters.py |
| T-007 | check_price accepts price within/at limit | P-003 | Passing | tests/test_filters.py |
| T-008 | check_price rejects price above limit | P-003 | Passing | tests/test_filters.py |
| T-009 | is_seen returns False for unseen listing | P-004 | Passing | tests/test_db.py |
| T-010 | mark_seen then is_seen returns True | P-004 | Passing | tests/test_db.py |
| T-011 | mark_seen is idempotent | P-004 | Passing | tests/test_db.py |
| T-012 | Different listing IDs are independent in DB | P-004 | Passing | tests/test_db.py |
| T-013 | search() returns parsed listing objects | P-002 | Passing | tests/test_vinted.py |
| T-014 | search() returns empty list on empty response | P-002 | Passing | tests/test_vinted.py |
| T-015 | _parse() handles missing fields gracefully | P-002 | Passing | tests/test_vinted.py |
| T-016 | send() POSTs to Telegram with correct payload | P-005 | Passing | tests/test_notifier.py |
| T-017 | send() message includes card name and price | P-005 | Passing | tests/test_notifier.py |
| T-018 | send() message includes Vinted URL | P-005 | Passing | tests/test_notifier.py |
| T-019 | check_card_is_english returns True for mocked English response | P-014 | Passing | tests/test_image_check.py |
| T-020 | check_card_is_english returns False for mocked non-English response | P-014 | Passing | tests/test_image_check.py |
| T-021 | check_card_is_english returns True when image fetch fails (fail-open) | P-014 | Passing | tests/test_image_check.py |
| T-022 | check_card_is_english returns True when API key absent (fail-open) | P-014 | Passing | tests/test_image_check.py |
