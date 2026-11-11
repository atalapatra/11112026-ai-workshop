# Lessons Learned

Append one entry per run. The point is to improve the rules and tooling, not to record history for its own sake: each lesson should end with what changed (or "no change").

## 2026-11-11 — DCA kickoff transcript (first run)

**Result:** 325 utterances → 107 issues (67 stories, 28 tasks incl. 8 decisions + 8 action items, 6 spikes, 6 parked stories) + 5 ledger-only items (3 superseded, 1 rejected, 1 merged recap).

**What the validator caught on the first pass**
- 21 utterances listed as both "no-requirement" and cited by an item → rule: cited wins; overlap is an error.
- One closing remark (00:43:44) missed entirely; one mistyped timestamp.
- 10 stories written "As the deputy director…" failed the "As a" check → validator now accepts a/an/the.
- `blocked_by` on items that are merely *affected* by a decision → rule: use `blocked_by` (+ `blocked` label) only when work truly can't start; otherwise reference the decision in text.

**Traps in this transcript worth remembering**
- **Self-correction:** sponsor asked for automatic eligibility decisions (00:10:53), reversed it 16 minutes later after legal advice (00:26:23). Later beats earlier.
- **Wrong playback:** facilitator's summary (00:40:31) repeated the superseded version. Recaps are cross-checks, not sources of truth.
- **"Park" means two things:** "Let's park that one" on note editing (00:18:56) was an *open decision*, not a parking-lot feature. Check the recap lists to see which bucket the meeting put it in.
- **Parked feature with live discovery work:** SMS reminders are parked, but the vendor/contract question is a spike that can start now.
- **Late additions:** training environment and fake data came *after* "we're done".
- **Policy disagreements are decisions, not spikes:** $3,500 vs $5,000 needs an owner to decide, not research.
- **Unrecapped integration:** the print-center manifest (00:38:54) was called "potential integration" but not put in the parking lot → modeled as a spike + manual-entry story. Judgment call; confirm with client.

**GitHub sync**
- `gh` needs the `project` scope (`gh auth refresh -s project`) — the default login lacks it.
- `Type` is a reserved Projects field name → field renamed to `Item Type`. Idempotent sync meant the failed first run cost nothing; re-run picked up the already-created project.
- Running `verify` mid-sync shows only "missing project item" errors for not-yet-synced items — expected, not a failure.

**Open improvements**
- Sync uses ~5 `gh` calls per issue; batch via GraphQL if backlogs get large.
- Consider an LLM-assisted "second reader" pass that reads only the transcript and lists requirements, then diff its list against the ledger to catch misclassification (the coverage check proves every utterance was *cited*, not that it was *understood*).

## 2026-11-11 — Slice 1 build: intake to deadline

**Result:** 7 stories (DCA-001, 004, 011, 012, 033, 034, 035) built as a FastAPI + SQLite app. 79 tests; `trace` covers 22/22 acceptance criteria; journey walked in the browser as caseworker and supervisor.

**What worked**
- **Acceptance criteria as the test spec, checked mechanically.** `trace` extends the transcript → ledger chain to ledger → tests. Writing it *before* the code gave a concrete 0/22 → 22/22 target.
- **Pure domain functions with dates passed in** made the hard rules (business days, holidays, 18th birthdays, the 7-day window) easy to pin down with a fixed "today" (Veterans Day 2026 turned out to be a great test date).
- **Mutation spot-check.** The tests passed on the first run, which proves nothing on its own. Breaking three rules on purpose (7-day boundary, holiday skip, supervisor notification) confirmed each was caught by the intended test. Now part of the Definition of Done.

**What tests missed and the browser caught**
- **SSN in the URL.** Search was a GET form, so SSNs landed in the URL, server logs and browser history. Every test passed. Found only by using the app → fixed (POST) and made a convention in build-process.md.
- **Editable prefilled fields** for an existing person were silently ignored by the server → made read-only.

**Judgment calls** are recorded in `slices/intake-to-deadline.md` under "Decisions made while building" (calendar vs business days, 18 = adult, verifications final, checklist snapshots).

**Open improvements**
- The ledger has no non-functional "privacy" acceptance criteria (e.g. "SSNs never in URLs or logs"). Consider a cross-cutting NFR checklist applied to every story at build time.
- Parallel build (sessions/worktrees per story) wasn't exercised. The file-per-story-area layout should support it; try it on slice 2.
