---
name: build-slice
description: Build a vertical slice of the DCA backlog as working software, with every acceptance criterion traced to a test. Use when asked to build, implement, or extend stories from the ledger.
---

# Build a slice

Read `process/build-process.md` (how), the slice file in `slices/` (what), and the stories' entries in `backlog/dca-kickoff.md` (acceptance criteria). Read `process/lessons-learned.md` for traps from earlier runs.

1. **New slice?** Create `slices/<name>.md` with a `stories:` line, stubs, out-of-scope, and an empty "Decisions made while building" section. Prefer stories that aren't `blocked`.
2. **Per story:** write tests tagged `@pytest.mark.story("DCA-xxx", n)` for each acceptance criterion → implement domain logic in `app/domain/` → persistence in `app/db.py` → routes/templates in `app/web/`, `app/templates/`.
3. **Check:**
   ```bash
   .venv/bin/pytest -q
   python3 scripts/backlog.py trace backlog/dca-kickoff.md slices/<name>.md
   ```
4. **Prove the tests bite:** break each key rule on purpose and confirm the right test fails, then restore.
5. **Use it:** `.venv/bin/python -m app.seed`, start the `dca-app` preview (`.claude/launch.json`), and walk the journey in the browser as each role. Look for things tests can't see (PII in URLs, confusing UI).
6. **Record:** interpretation calls → slice file "Decisions"; anything surprising → `process/lessons-learned.md`; update `README.md` (layout, usage, current state, changelog).

If an acceptance criterion is wrong, fix the ledger and re-run `sync` before changing code.
