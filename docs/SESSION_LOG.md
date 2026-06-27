# Session Log

## Last session
- **Date:** 2026-06-27
- **Completed:** B-005 — language tag filter (ITA/FR/français/deutsch etc.); Eevee δ max_price raised to €7. 57/57 tests pass.
- **In progress:** —
- **Next up:** Disambiguation fix (P-015, Scenario 1/2): require set number for cards with multiple tracked delta variants (Rayquaza, Pikachu, Mew)

---

## Decision log

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
