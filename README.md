# AI Workshop: Transcript → User Stories → Working Software

A workshop exercise in building a **durable, improvable working process with Claude**:

1. **Exercise 1:** turn a meeting transcript into a GitHub Project of user stories, tasks and spikes, and *prove* nothing in the transcript was missed.
2. **Exercise 2:** build a **vertical slice** of those stories as working software, with every acceptance criterion traced to a test.

The sample input is a fictional kickoff meeting for modernizing a state agency's case management system ([dca-case-management-kickoff-transcript.md](dca-case-management-kickoff-transcript.md)). The output is the [DCA Case Management](https://github.com/users/atalapatra/projects/1) GitHub Project.

## The process at a glance

```
transcript ──► ledger (backlog/*.md) ──► validate ──► human review ──► sync ──► verify ──► retro
                 ▲   source of truth       │ every utterance                    │ GitHub == ledger   │
                 └─────── fix ◄────────────┘ accounted for                      └────────────────────┘ improve rules
```

1. **Read** the whole transcript before extracting — later statements can correct earlier ones.
2. **Classify** every requirement-bearing statement into a ledger using the [classification rules](process/classification-rules.md).
3. **Validate** coverage offline: every one of the transcript's utterances must be cited by an item or explicitly marked as no-requirement.
4. **Review** the ledger with a human before anything touches GitHub.
5. **Sync** the ledger to GitHub issues and a Project (idempotent — re-run any time).
6. **Verify** the live Project matches the ledger exactly.
7. **Retro** — record what was learned in [lessons-learned.md](process/lessons-learned.md) and update the rules.

The full step-by-step is the Claude skill [`transcript-to-backlog`](.claude/skills/transcript-to-backlog/SKILL.md); in Claude Code, ask it to turn a transcript into a backlog and it will follow that process.

## Building a slice (exercise 2)

The first slice, **[Intake to deadline](slices/intake-to-deadline.md)**, covers a caseworker searching for a person, recording an application, verifying documents against a program checklist, and working a queue where expedited Housing cases are flagged automatically and sorted to the top.

Stories: [DCA-001](https://github.com/atalapatra/11112026-ai-workshop/issues/1) search · [DCA-004](https://github.com/atalapatra/11112026-ai-workshop/issues/4) intake · [DCA-011](https://github.com/atalapatra/11112026-ai-workshop/issues/11) checklist · [DCA-012](https://github.com/atalapatra/11112026-ai-workshop/issues/12) verification · [DCA-033](https://github.com/atalapatra/11112026-ai-workshop/issues/33) 30-day clock · [DCA-034](https://github.com/atalapatra/11112026-ai-workshop/issues/34) expedited flag · [DCA-035](https://github.com/atalapatra/11112026-ai-workshop/issues/35) expedited queue/alerts

How it's built ([build-process.md](process/build-process.md), skill [`build-slice`](.claude/skills/build-slice/SKILL.md)):
- Each acceptance-criterion bullet in the ledger becomes a test tagged `@pytest.mark.story("DCA-034", 2)`.
- `trace` fails if any criterion in the slice has no tagged test. That closes the chain **transcript → ledger → GitHub issue → test**.
- Business rules are pure functions in `app/domain/`; "today" is injectable, so deadline rules are tested on fixed dates.
- Done means the tests pass, the tests are proven to bite (rules broken on purpose), and the journey has been walked in the browser.

## Story vs. task vs. spike (short version)

| Type | Use when | Example |
|---|---|---|
| **Spike** | We must *find something out* before we can design or estimate. Time-boxed; output is knowledge. | Profile CAMS data to size the duplicate problem |
| **Task** (`decision`) | A client owner must make a policy/business call. | Decision: approval threshold $3,500 vs $5,000 |
| **User story** | A named role gets new value they can see or use. | Supervisor bulk-reassigns a caseload |
| **Task** | Necessary work with no direct end-user value. | Register the app in Entra ID |

Not everything becomes an issue: items can also be **parking-lot** (deferred, still tracked), **superseded** (corrected later in the meeting), **rejected**, or **merged** into another item. Full rules and worked examples: [process/classification-rules.md](process/classification-rules.md).

## How we validate completeness

| Check | Command | Catches |
|---|---|---|
| Utterance coverage | `validate` | Any transcript line not cited by an item or marked no-requirement |
| Meeting recap cross-check | `validate` | Parking-lot, open-question, commitment and next-step recaps that don't map to an issue |
| Item format | `validate` | Stories without a role/acceptance criteria, spikes without question/time-box/output, decisions without an owner |
| GitHub drift | `verify` | Missing, duplicate, orphaned or edited issues/project items vs. the ledger |

## Repo layout

| Path | What it is |
|---|---|
| [dca-case-management-kickoff-transcript.md](dca-case-management-kickoff-transcript.md) | Input: the meeting transcript |
| [backlog/dca-kickoff.md](backlog/dca-kickoff.md) | **Ledger** — source of truth for every item, with transcript citations |
| `backlog/dca-kickoff.github.json` | Generated by `sync`: project/field IDs and ledger ID → issue number map |
| [process/classification-rules.md](process/classification-rules.md) | Rules for disposition, type, labels and project fields |
| [process/lessons-learned.md](process/lessons-learned.md) | Retro log — what each run taught us and what changed |
| [scripts/backlog.py](scripts/backlog.py) | `validate` / `sync` / `verify` tooling (Python 3, stdlib only) |
| [.claude/skills/transcript-to-backlog/SKILL.md](.claude/skills/transcript-to-backlog/SKILL.md) | The process as a reusable Claude skill |
| [CLAUDE.md](CLAUDE.md) | Project instructions Claude loads every session |
| [process/build-process.md](process/build-process.md) | How a story becomes tested software; Definition of Done; conventions |
| [slices/intake-to-deadline.md](slices/intake-to-deadline.md) | Slice 1: stories in scope, stubs, out of scope, decisions made while building |
| [.claude/skills/build-slice/SKILL.md](.claude/skills/build-slice/SKILL.md) | The build process as a reusable Claude skill |
| `app/domain/` | Pure business rules: search matching, deadlines/expedited, checklist generation |
| `app/db.py`, `app/schema.sql`, `app/seed.py` | SQLite persistence, schema (immutable verifications), reference + demo data |
| `app/web/`, `app/templates/`, `app/static/` | FastAPI routes (one module per area), Jinja templates, CSS |
| `tests/` | One file per story; every test tagged with the acceptance criterion it proves |
| `.claude/launch.json` | `dca-app` dev server config for the Claude browser preview |

## Usage

Prerequisites: Python 3 and the GitHub CLI with the `project` scope.

```bash
gh auth refresh -s project
```

Check the ledger covers the transcript:

```bash
python3 scripts/backlog.py validate backlog/dca-kickoff.md
```

Preview, then push to GitHub:

```bash
python3 scripts/backlog.py sync backlog/dca-kickoff.md --project-title "DCA Case Management" --dry-run
```

```bash
python3 scripts/backlog.py sync backlog/dca-kickoff.md --project-title "DCA Case Management"
```

Confirm GitHub matches the ledger:

```bash
python3 scripts/backlog.py verify backlog/dca-kickoff.md
```

**To change the backlog, edit the ledger and re-run `sync`.** Never hand-edit generated issues; `verify` will flag the drift.

### Running the app

One-time setup (Python 3.12+):

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Create a fresh database with demo data (fictional people only):

```bash
.venv/bin/python -m app.seed
```

Start the app at http://localhost:8000 and use the header dropdown to switch between caseworker, supervisor and program admin (stand-in for SSO):

```bash
.venv/bin/uvicorn app.main:app --reload
```

Run the tests:

```bash
.venv/bin/pytest -q
```

Check every acceptance criterion in the slice has a test:

```bash
python3 scripts/backlog.py trace backlog/dca-kickoff.md slices/intake-to-deadline.md
```

Set `DCA_TODAY=2026-11-20` to see the deadline clock on a different day.

## Current state

| | |
|---|---|
| Transcript | DCA kickoff, 2026-11-03 — 325 utterances, all accounted for |
| GitHub Project | [DCA Case Management](https://github.com/users/atalapatra/projects/1) — 107 issues, `verify` passing |
| Breakdown | 67 stories, 28 tasks (8 decisions, 8 action items), 6 spikes, 6 parked stories |
| Ledger-only | 3 superseded, 1 rejected, 1 merged recap |
| Slice 1 | [Intake to deadline](slices/intake-to-deadline.md): 7 stories built, 79 tests passing, `trace` 22/22 acceptance criteria |

## Changelog

- **2026-11-11** — Initial process: classification rules, ledger format, `validate`/`sync`/`verify` tooling, Claude skill. DCA kickoff transcript converted and synced (107 issues). Renamed project field `Type` → `Item Type` (reserved by GitHub). Workshop slide deck removed from the repo and `*.pptx` ignored.
- **2026-11-11** — Exercise 2: slice 1 "Intake to deadline" built (FastAPI + SQLite, 7 stories, 79 tests). Added `trace` subcommand, build process, `build-slice` skill, slice file. Search changed to POST after the browser walkthrough found SSNs in URLs.
