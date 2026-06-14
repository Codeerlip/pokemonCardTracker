# Vinted Delta Species Bot — Claude Code Instructions

## Workflow

Every work item and every bug must be tracked before work begins. The tracker is the source of truth for project state.

### Work items (features, refactors, infra, docs, spikes)

1. Add a row to [plans/PLAN_TRACKER.md](./plans/PLAN_TRACKER.md) under the correct category section.
2. Create a detail file at `plans/P-NNN-short-name.md` using [plans/TEMPLATE_plan.md](./plans/TEMPLATE_plan.md).
3. IDs are sequential integers zero-padded to three digits: P-001, P-002, …
4. Status transitions: the implementation commit moves the item to In Progress. A follow-up commit that registers passing tests in TEST_TRACKER.md moves it to Done.
- One concern per plan item. If a task spans multiple concerns, split into separate entries — one P-NNN per concern.

### Bugs

1. Add a row to [plans/PLAN_TRACKER_BUGS.md](./plans/PLAN_TRACKER_BUGS.md) before writing any fix code.
2. Create a detail file at `plans/B-NNN-short-name.md` (same template shape as plans).
3. IDs are sequential: B-001, B-002, …
4. Severity: P0 (critical/data-loss) · P1 (major/broken feature) · P2 (minor/degraded UX) · P3 (cosmetic).
5. Allowed statuses: Open · Investigating · Fixed · Wontfix.

### Build output

- Run `python -m pytest` after every `.py` change that is not doc/comment-only.
- Build is only considered failed if there are import errors or test failures.
- Use `python main.py --dry-run` to validate end-to-end flow without sending Telegram messages.

### General rules

- Python 3.10+ only.
- Use `requests` (not aiohttp). Use `sqlite3` (stdlib). No ORM.
- All config via `config.json` — no hardcoded values anywhere.
- `--dry-run` flag must always be respected: no Telegram messages, console output only.
- Handle Vinted rate limits with exponential backoff + random jitter.
- Use browser-like headers and a session with cookies on all Vinted requests.

### Session handoff

- After every completed task, update [docs/SESSION_LOG.md](./docs/SESSION_LOG.md):
  - Set the "Last session" block to reflect current state (date, completed, in progress, next up).
  - Prepend a new entry to "## Decision log" (keep max 20 entries — drop oldest beyond that).
- At the start of every new session, read `docs/SESSION_LOG.md` first. It tells you what just happened and what to watch out for before touching anything.
- Keep entries concise — 4 lines max per entry.

---

## Orchestrator

Every session starts in orchestrator mode. On first message:
1. Read [docs/SESSION_LOG.md](./docs/SESSION_LOG.md) to orient on what happened last session.
2. Read [plans/PLAN_TRACKER.md](./plans/PLAN_TRACKER.md) and [plans/PLAN_TRACKER_BUGS.md](./plans/PLAN_TRACKER_BUGS.md) to confirm current item statuses.
3. Summarise: what was completed, what is in progress, what is next.
4. If the user provides new findings: log them into the tracking system before proposing anything. Deduplicate against existing items first.
5. Propose an execution order (highest severity first) and ask for approval before starting any task.
6. After approval: invoke the right subagent per task, update SESSION_LOG.md after each completed item, and ask for approval before moving to the next.

Never start work without explicit approval.
Never log the same finding twice — check existing IDs first.
Never self-execute code changes — always delegate to the matching agent.

### Agent roster

Route by inspecting which files the fix will touch, then match against the **Files / signals** column.

| Agent | Invoke when the task involves | Files / signals |
|---|---|---|
| core-engineer | Vinted API, filtering logic, polling loop, config loading | `vinted.py`, `filters.py`, `main.py`, `config.json` |
| database-engineer | SQLite schema, seen-listing deduplication | `db.py`, `*.sql` |
| notifier-engineer | Telegram message formatting and delivery | `notifier.py` |
| testing-engineer | Writing tests, TEST_TRACKER updates — invoked after implementation | `tests/**`, `TEST_TRACKER.md` |

---

## Architecture principles

### Modularity

- One module = one responsibility. If a file does two things, split it.
- No cross-module state. Pass data; do not reach into siblings.

### Reusability

- Search the codebase before writing a helper. Extend, do not fork.
- 2+ call sites = extract. 1 call site = leave inline. No premature abstraction.

### Single source of truth (DRY)

- Constants, enums, config keys: defined once, imported everywhere.
- All card definitions and thresholds live in `config.json` only.

### Clean architecture

- Data layer (`db.py`), business logic (`filters.py`, `vinted.py`), and notification (`notifier.py`) never bleed into each other.
- Side effects (network, Telegram, SQLite) live at the module edges.
- `main.py` is the only orchestrator — it wires modules together.

### Change discipline

- Touch only what the task requires. No drive-by refactors.
- Violations unrelated to the current task → log a P-NNN entry in PLAN_TRACKER.md.

---

## Testing

- Every plan detail file must list, under **Verification**, the tests that prove each Acceptance criterion.
- The testing-engineer registers each test as a row in [testing/TEST_TRACKER.md](./testing/TEST_TRACKER.md) before the parent plan moves to "Done".
- Test IDs are sequential and zero-padded: T-001, T-002, …
- A plan cannot move to status "Done" while any of its linked tests are failing or unregistered.
- Use `pytest` with mock fixtures for Vinted API and Telegram calls — never hit real endpoints in tests.

---

## Product context

Project: **Vinted Delta Species Pokémon Card Alert Bot**
Language: Python 3.10+
Entry point: `vinted-bot/main.py`

### Domain rules

- **No real Telegram messages in tests or --dry-run.** Any code path that sends a Telegram message outside of a live run is a P0 bug.
- **Vinted API is unofficial.** All requests must use realistic browser headers and session cookies. Bare requests without headers are a P1 bug.
- **Deduplication is required.** A listing must never trigger more than one notification. Missing a `mark_seen()` call is a P1 bug.
- **Config is the single source of truth.** Hardcoded card names, prices, or Telegram credentials are P1 bugs.
- **Rate limiting must be respected.** Any polling loop without exponential backoff + jitter on failure is a P2 bug.
