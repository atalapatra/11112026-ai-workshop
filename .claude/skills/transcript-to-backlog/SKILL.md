---
name: transcript-to-backlog
description: Turn a meeting transcript into a traceable backlog of user stories, tasks and spikes, validate full coverage, and sync it to a GitHub Project. Use when given a requirements/kickoff/discovery transcript and asked for stories, a backlog, or GitHub issues.
---

# Transcript → Backlog

Durable process. Rules live in `process/classification-rules.md`; lessons from past runs in `process/lessons-learned.md`. **Read both before starting.**

## 1. Read the whole transcript first
Don't extract while reading. Corrections, reversals and late additions ("one more thing, before everyone drops") change earlier statements. Note:
- every place someone **corrects** or **overrules** an earlier statement
- every "park it" / "future" / "open question" / "I'll send" / "next steps"
- the facilitator's recaps (playback, parking lot, open questions) — these become CHECK sections, not requirements, and may be wrong
- transcription errors (e.g. "Intra I.D." = Entra ID)

## 2. Write the ledger: `backlog/<meeting>.md`
Copy the format of `backlog/dca-kickoff.md`. For each requirement-bearing statement apply the classification rules (disposition first, then type). Every item cites `sources:` timestamps. Put content-free utterances (greetings, "Got it", "Thanks") in `## no-requirement`.

Add a `## CHECK | <recap name> | <timestamp>` section for each recap the meeting itself produced, mapping each phrase to an item ID. This is the independent cross-check that what *they* think was said is in the backlog.

## 3. Validate until it passes
```bash
python3 scripts/backlog.py validate backlog/<meeting>.md
```
`UNCOVERED` lines are utterances not cited anywhere — either they hold a requirement you missed or they belong in no-requirement. Fix the ledger, never the validator, unless the rule itself is wrong (then log it in lessons-learned).

## 4. Review with the human
Summarize: counts by type/disposition, every superseded/rejected item with its reason, every judgment call. Get approval before touching GitHub.

## 5. Sync and verify
```bash
gh auth refresh -s project            # once; Projects v2 needs this scope
python3 scripts/backlog.py sync backlog/<meeting>.md --project-title "<Project>" --dry-run
python3 scripts/backlog.py sync backlog/<meeting>.md --project-title "<Project>"
python3 scripts/backlog.py verify backlog/<meeting>.md
```
Sync is idempotent (matches issues by the `DCA-xxx:` title prefix) — re-run after any ledger edit. The ledger is the source of truth; edit it, not the issues. `verify` fails on missing, duplicate, orphaned or drifted issues/project items.

## 6. Retro
Append to `process/lessons-learned.md`: what the validator caught, which classification calls were hard, and any rule you changed. If a rule changed, add a worked example to the rules file.
