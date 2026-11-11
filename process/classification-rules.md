# Classification Rules: Story vs. Task vs. Spike

These rules decide what every item pulled from a transcript becomes. Apply them **in order** — the first rule that matches wins. When a rule is ambiguous in practice, add a worked example to the bottom of this file and record why in [lessons-learned.md](lessons-learned.md).

## Step 1 — Is it backlog work at all? (disposition)

Every statement that carries a requirement, constraint, decision, or commitment gets a ledger entry. Not every ledger entry becomes an issue.

| Disposition | When | Goes to GitHub? |
|---|---|---|
| `backlog` | In scope for the current phase. | Yes — Phase `Phase 1` |
| `parking-lot` | Explicitly deferred ("park it", "future phase", "future bucket"). | Yes — Phase `Parking Lot`, label `parking-lot` |
| `superseded` | Stated, then corrected or overruled later in the meeting (e.g. "system decides" → "system recommends"). | No. Ledger records `superseded_by` pointing at the item that replaced it. |
| `rejected` | Explicitly refused by the decision-maker ("No." / "Absolutely not."). | No. Ledger only, with the quote. |
| `merged` | Restates something already captured (the playback summary, a "+1", a detail that belongs inside another story's acceptance criteria). | No. Ledger records `merged_into`. |
| `no-requirement` | Small talk, logistics, intros, sign-offs. | No. Listed only in the ledger's `no_requirement` timestamps so coverage stays exhaustive. |

**Later beats earlier.** If a speaker corrects themselves or the meeting converges on a different answer, the final position is the requirement and the earlier one is `superseded`. The facilitator's playback is *not* authoritative — check it against the discussion (in the DCA kickoff the playback got eligibility backwards and was corrected).

**Authority matters.** A sponsor saying "park it" parks it, even if another attendee wanted it. A security/IT owner saying "not in phase one" for a public-facing capability parks it unless the sponsor overrules.

## Step 2 — Which type?

Ask these questions in order.

### 1. Is the main uncertainty something we must *find out* before we can estimate or design? → **Spike**

A spike is time-boxed investigation whose output is **knowledge** (a recommendation, a data profile, a documented format), not shippable functionality.

Signals:
- "Nobody knows / nobody's ever counted / it isn't written down anywhere."
- "Someone needs to look at / dig into / map out ... **before** we decide ..."
- Feasibility is unknown ("I'm not saying no, but I'm not saying yes").
- Vendor/contract/option discovery ("I don't know whether the state has a contract").

Must have: a question to answer, a time-box, and a named output (doc, decision record, sample data). Should name the story/stories it unblocks.

### 2. Is it an unresolved *policy or business decision* that someone on the client side owns? → **Task** (label `decision`)

These are not spikes: nobody investigates, an owner decides. Title as `Decision: <question>`. Body names the decision owner, the options heard in the meeting, and the stories blocked by it. Blocked stories get the label `blocked`.

Signals: "I need to check with policy / legal", "put it on the list for policy", two attendees disagree on a fact (e.g. $3,500 vs $5,000).

### 3. Does a person in a named role get new value they can see or use in the system? → **User Story**

Signals: someone describes what they want to *do* or *see* ("I want a screen that shows ...", "the system should flag ...", "I want to be able to refer ..."). Non-functional requirements that a user directly experiences (page load time, screen-reader support) are also stories, written from that user's point of view.

Format:
```
As a <role>, I want <capability>, so that <outcome>.
```
Followed by **Acceptance criteria** as Given/When/Then or checklist bullets, using the exact numbers and rules from the transcript (30 days, 10 days, day 20/25, 25 per program, etc.), each traceable to a timestamp.

One story per independently deliverable capability. If a story has more than ~7 acceptance criteria or spans two roles with different goals, split it.

### 4. Otherwise it is necessary work with no direct end-user value → **Task**

Signals: setup, configuration, data loading, content clean-up, environment provisioning, integration plumbing, external dependencies, documents to receive, meetings to hold.

Examples: register the app in Entra ID, load income-limit tables, consolidate 40 notice templates, build a realistic fake data set, schedule the appeals deep-dive.

Tasks coming from a client commitment ("I'll send ...") get label `action-item` and name the owner.

## Step 3 — Labels and fields

| Field | Values |
|---|---|
| Label `type:story` / `type:task` / `type:spike` | Exactly one per issue. |
| Label `area:<x>` | `intake`, `documents`, `eligibility`, `approvals`, `assignment`, `deadlines`, `case-notes`, `security`, `notices`, `appeals`, `household`, `payments`, `reporting`, `qa`, `recertification`, `platform`, `migration`, `training`, `public-access` |
| Label `decision` | Decision tasks only. |
| Label `blocked` | Story waiting on a decision task or spike. |
| Label `parking-lot` | Disposition `parking-lot`. |
| Label `action-item` | Client commitment from the meeting. |
| Project field `Item Type` | Story / Task / Spike (mirrors the label; `Type` is reserved by GitHub). |
| Project field `Phase` | Phase 1 (disposition `backlog`) / Parking Lot. Workflow uses the built-in `Status`. |
| Project field `Area` | Same as the `area:` label. |
| Project field `Source` | Transcript timestamps, e.g. `00:07:33, 00:08:02`. |
| Project field `Ledger ID` | e.g. `DCA-014`; also the issue title prefix (used for idempotent sync). |

## Step 4 — Traceability (non-negotiable)

Every ledger item lists `sources`: the transcript timestamps it came from. Every issue body ends with a **Source** section quoting those timestamps. The validator fails if any requirement-bearing utterance is not cited by some ledger item or listed as `no-requirement`.

---

## Worked examples (DCA kickoff)

| Transcript | Result | Why |
|---|---|---|
| "I want the system to calculate eligibility automatically" (00:10:53) then GC correction (00:26:23) | 00:10:53 `superseded` → story "Eligibility recommendation with caseworker determination" | Later beats earlier. |
| Round-robin assignment (00:14:11) | `superseded` by "Suggested assignee" story | Sponsor conceded at 00:14:55. |
| "Does anybody know how bad the duplicate problem is?" (00:05:48) | Spike: profile CAMS person data | Unknown data drives the matching design. |
| Pay stubs valid 30 vs 60 days (00:09:03–00:09:25) | Task `decision` | Policy owner must answer; no investigation needed. |
| Approval threshold $3,500 vs $5,000 (00:13:09) | Task `decision` + story built with a configurable threshold | The story doesn't need to wait if the value is configurable — note this in the story. |
| Text message reminders (00:22:37) | `parking-lot` story **plus** a backlog spike on SMS vendor options | Parked feature, but Priya named concrete discovery work that can start now. |
| Timesheets (00:37:37) | `rejected` | "Absolutely not." |
| "Somebody has to load those tables before we go live" (00:12:28) | Task | Data loading, no new user capability. |
| "Fake data that looks real" (00:44:33) | Task (training) | Said after "we're done" — late items still count. |
