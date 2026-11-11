# AI Workshop – Transcript to User Stories

Turning meeting transcripts into a GitHub Project of stories, tasks and spikes, with a repeatable, self-improving process.

- Process: `.claude/skills/transcript-to-backlog/SKILL.md` (use it for any transcript → backlog request)
- Rules: `process/classification-rules.md` — story vs. task vs. spike, dispositions, labels
- Lessons: `process/lessons-learned.md` — read before a run, append after
- Ledgers (source of truth): `backlog/*.md`; GitHub state written to `backlog/*.github.json`
- Tooling: `python3 scripts/backlog.py {validate|sync|verify} <ledger>` and `trace <ledger> <slice>` (stdlib only)
- Building software: `.claude/skills/build-slice/SKILL.md`, `process/build-process.md`, slices in `slices/`
- App: FastAPI + SQLite in `app/` (domain rules in `app/domain/`, pure, dates passed in); tests in `tests/` tagged `@pytest.mark.story("DCA-xxx", n)`; run with `.venv/bin/pytest -q`

Conventions
- Edit the ledger, then re-run `sync`; never hand-edit generated issues.
- `validate` must PASS before `sync`; `verify` must PASS before calling a backlog done.
- Keep `README.md` current: whenever you add or change a file, rule, command, transcript or project, update its repo layout, usage, "Current state" table, and add a dated line to its Changelog in the same change.
- When a classification call is hard, record it in lessons-learned and, if it changes a rule, add a worked example to the rules file.
