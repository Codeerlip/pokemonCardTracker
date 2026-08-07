# B-007 — Discord debrief crashes with 400 Bad Request on large match batches

## Status
Fixed

## Severity
P0

## Root cause
`notifier.send_debrief` builds the header embed's `description` from a summary line for
**every** match in the batch, with no length cap. Discord limits an embed `description` to
4096 characters and the combined text across all embeds in one webhook POST to 6000
characters. Adding 21 new cards in one config update produced a "first-run backfill" of
50+ never-before-seen matches in a single poll cycle, pushing the header embed (and the
total payload, on top of the already-capped 9 per-match embeds) past Discord's limits.
The webhook POST returns `400 Bad Request`, `resp.raise_for_status()` raises, and the
whole job crashes with exit code 1 — meaning **no matches from that run are ever sent**,
including the legitimate ones bundled in the same payload. Every scheduled run since the
config update failed the same way.

## Fix
Cap the header summary to the same 9 matches shown in detail embeds (mirroring the existing
"+N more not shown" footer overflow note), so the summary text size no longer scales with
the total match count.

## Files touched
- `vinted-bot/notifier.py`
- `vinted-bot/tests/test_notifier.py`

## Verification
- T-040: `send_debrief` with >9 matches caps the header description to 9 summary lines plus
  an "…and N more" line, and does not raise on a large batch.
- T-041: `send_debrief` with <=9 matches includes every match in the header summary with no
  overflow line.
