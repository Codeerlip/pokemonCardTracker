# Session Log

## Last session
- **Date:** 2026-06-28
- **Completed:** B-006 — language filter extended to description field; P-016 — single-part set numbers no longer require delta keyword (e.g. "Pikachu 035" now matches); Pikachu δ Nintendo Promo max_price raised to €275. 61/61 tests pass.
- **In progress:** —
- **Next up:** Disambiguation fix (P-015): require set number for cards with multiple tracked delta variants (Rayquaza, Pikachu, Mew)

---

## Decision log

### 2026-07-03 — P-018 fetch listing detail for description language check
Vinted catalog API never returns the description field. Added vinted.fetch_description() calling /api/v2/items/{id}, invoked in main.py after initial filters pass. Re-runs check_no_foreign_language_tag with the full description. Fail-open on errors. T-037..T-039 added; 67/67 tests pass.

### 2026-06-28 — P-017 description set-number conflict check
Extended check_title_relevance() to also scan the description for a conflicting X/Y set number when none appears in the title. Catches cases like "Mewtwo Delta Species / 24/110" in description when the target is 12/113. T-034..T-036 added. 64/64 tests pass.

### 2026-06-28 — P-016 relax single-part set number filter + Pikachu δ promo price
Single-part set numbers (e.g. "35") now pass check_title_relevance when the bare number appears in the title — no delta keyword required, consistent with 2-part behaviour. Pikachu δ Nintendo Promo max_price raised from €15 to €275 (CardMarket floor is €240). T-033 added.

### 2026-06-28 — B-006 description language filter
Extended check_no_foreign_language_tag() to also scan the listing description. "Language: Italian" in description now correctly blocks the listing. T-030..T-032 added.

### 2026-06-27 — B-005 foreign language tag filter + Eevee max_price
Added check_no_foreign_language_tag() to filters.py; blocks standalone language codes (ITA, FR, ger, por…) and full words (français, deutsch, italiano). Eevee δ EX Delta Species max_price raised from €3 to €7.

### 2026-06-19 — B-004 Pikachu δ Nintendo Promo single-number filter
For single-component set numbers (e.g. "35"), the title must contain BOTH the bare number AND a delta keyword. Previously the δ symbol alone was sufficient, so "Pikachu δ Nintendo promo" (no "35") passed incorrectly.

### 2026-06-18 — P-014 image_check.py English card vision check
Added `image_check.py` using `claude-haiku-4-5` vision. Downloads listing image, encodes base64, asks "YES/NO is this English?". Fail-open on missing API key, network errors, or API errors so no valid listings are silently dropped. Wired into `main.py` filter chain after existing filters.

### 2026-06-18 — B-003 Rayquaza 26/110 wrong-set false-positive
Added conflicting X/Y set number detection to `check_title_relevance`. If title contains an explicit `N/M` that differs from the target card's `set_number`, reject even when "delta" keyword appears.

### 2026-06-16 — B-002 false-positive Pikachu EVO 35 notification
Single-token set numbers (e.g. "35") were bypassing the delta keyword check. Fixed by requiring ≥2 parts before the set-number shortcut fires. Two regression tests added.

### 2026-06-15 — B-001 recency filter fix
Vinted catalog API dropped all date fields. `check_recency(None)` now returns `True` (pass through). DB deduplication prevents repeat notifications for the same listing.

### 2026-06-14 — GitHub Actions deployment
P-008/P-009 done. main.py is now one-shot; cron runs every 15 min via GH Actions. SQLite DB cached between runs via actions/cache. Env var DISCORD_WEBHOOK_URL overrides config.json.

### 2026-06-14 — Full implementation in one session
P-001–P-006 all implemented and tested in one pass. 22 tests covering filters, db, vinted parsing, notifier, and imports. Venv at vinted-bot/.venv. Run with `.venv/bin/python main.py --dry-run`.

### 2026-06-14 — Framework adopted
Adopted Vlot orchestrator framework for this Python bot project. Agent roster simplified to core-engineer / database-engineer / notifier-engineer / testing-engineer. No work starts without explicit approval.
