# P-014 — image_check.py — Claude vision English-language card check

## Status
In Progress

## Agent
core-engineer

## Goal
Add a module that downloads a listing image and uses Claude Haiku vision to determine whether the card shown is in English, filtering out non-English editions.

## Scope
- `vinted-bot/image_check.py` (new)
- `vinted-bot/main.py` (wire in filter)
- `vinted-bot/requirements.txt` (add `anthropic`)
- `vinted-bot/tests/test_image_check.py` (new)

## Acceptance criteria
- [ ] AC1: `check_card_is_english(image_url, session)` returns `True` for an English card image.
- [ ] AC2: `check_card_is_english` returns `False` for a non-English card image.
- [ ] AC3: If the image cannot be fetched or the API call fails, the function returns `True` (fail-open — don't block potentially valid listings).
- [ ] AC4: `ANTHROPIC_API_KEY` is read from env var; if absent, function returns `True` (fail-open).
- [ ] AC5: `main.py` calls the check after title/condition/price/recency pass; non-English cards are skipped and marked seen.

## Verification
- T-019: check_card_is_english returns True for mocked English response
- T-020: check_card_is_english returns False for mocked non-English response
- T-021: check_card_is_english returns True when image fetch fails (fail-open)
- T-022: check_card_is_english returns True when API key absent (fail-open)

## Notes
- Use `claude-haiku-4-5` — cheapest/fastest for binary classification.
- Encode image as base64; pass as `image` block in Claude messages API.
- Fail-open on any exception to avoid silent gaps in coverage.
- Pass the existing `requests.Session` so headers/cookies are reused.
