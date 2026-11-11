# Build Process: Story → Working Software

How Claude builds a slice of the backlog. The ledger (`backlog/*.md`) stays the source of truth for *what* to build; this file is *how*.

## 1. Define the slice first
A slice file in `slices/` lists the stories in scope, what is stubbed, and what is explicitly out of scope. A vertical slice cuts through every layer (UI → API → database) for a narrow set of stories; it does not build any layer completely.

Pick stories that:
- form one end-to-end user journey,
- are not `blocked` by an open decision or spike,
- need as few stubs as possible (stub cross-cutting concerns like SSO, don't build them).

## 2. Acceptance criteria are the spec
Each acceptance-criteria bullet in the ledger becomes **at least one automated test** tagged with the story ID and the bullet's 1-based index:

```python
@pytest.mark.story("DCA-034", 2)
def test_expedited_due_date_skips_weekends_and_holidays(...): ...
```

If an acceptance criterion is wrong or untestable, **fix the ledger first** (and re-run `sync` so the issue updates), then write the test. Code never silently diverges from the story.

## 3. Build order per story
1. Read the story's acceptance criteria and sources in the ledger.
2. Write the tests for each criterion (they should fail).
3. Implement domain logic in `app/domain/` as plain functions (no web/database imports) — easiest to test.
4. Add persistence in `app/db.py` and routes/templates in `app/web/`.
5. Run the full suite: `.venv/bin/pytest`.
6. Run `trace` (below) — the story is not done until every criterion is covered.
7. Click through the feature in the running app.

## 4. Definition of Done (per story)
- [ ] Every acceptance criterion has a passing test tagged `story("DCA-xxx", n)`.
- [ ] Full test suite passes.
- [ ] Tests proven to bite: break each key business rule on purpose and confirm the matching test fails (tests written alongside the code never got to fail first).
- [ ] Feature works in the running app (manually exercised).
- [ ] Stubs and deviations recorded in the slice file.
- [ ] README "Current state" updated.

## 5. Traceability check
```bash
python3 scripts/backlog.py trace backlog/dca-kickoff.md slices/intake-to-deadline.md
```
Fails if any acceptance criterion of an in-scope story has no tagged test, or a test is tagged with a story/criterion that doesn't exist. This is the build-time equivalent of `validate`: the transcript is covered by the ledger, the ledger is covered by tests.

## 6. Architecture conventions
| Layer | Location | Rule |
|---|---|---|
| Domain logic | `app/domain/*.py` | Pure functions, dates passed in (never call `date.today()`), no I/O. |
| Persistence | `app/db.py` | stdlib `sqlite3`; schema in `app/schema.sql`; seed data in `app/seed.py`. |
| Web | `app/web/*.py`, `app/templates/` | FastAPI routes, server-rendered Jinja templates, plain forms (no JS required). Anything carrying PII (SSN, DOB) is POSTed, never put in a URL. |
| Clock | `app/clock.py` | Single source of "today"; overridable in tests and via `DCA_TODAY` env var for demos. |
| Identity | `app/web/session.py` | Stub for DCA-045 (SSO): pick a seeded user from a header dropdown. |

## 7. Working independently (for teams)
Stories in a slice should touch separate files where possible: one domain module and one route module per story area. When several people (or Claude sessions) build in parallel, give each a story, its own branch/worktree, and the same three inputs — the ledger, this file, and the slice file. Shared files (`schema.sql`, `base.html`) are changed by one owner at a time.
