# Slice 1: Intake to Deadline

**Journey:** A caseworker searches for a person, records a new application, works the program's document checklist (recording who verified each document), and sees the application in a work queue that shows its deadline — with expedited Housing cases flagged automatically and pushed to the top.

## Stories in scope
stories: DCA-001, DCA-004, DCA-011, DCA-012, DCA-033, DCA-034, DCA-035

| ID | Issue | Story |
|---|---|---|
| DCA-001 | #1 | Find existing people with tolerant search |
| DCA-004 | #4 | Record a new application at intake |
| DCA-011 | #11 | Program-specific document checklist |
| DCA-012 | #12 | Record who verified each document and when |
| DCA-033 | #33 | Track the 30-day processing clock on every application |
| DCA-034 | #34 | Automatically flag expedited Housing cases |
| DCA-035 | #35 | Expedited cases go to the top and alert prominently |

## Stubs (stand-ins for out-of-slice stories)
| Stub | Stands in for | How |
|---|---|---|
| User picker in the header | DCA-045 SSO, DCA-047 roles | Seeded users with a role; selection stored in a cookie. |
| Assignment = the caseworker who records the application | DCA-028, DCA-029 | No routing or suggestions. |
| Document reference is free text ("Pay stub dated 10/30/2026") | DCA-013 document capture | No file upload. |
| Notifications are an in-app list | Email/other channels | Bell count in the header. |
| Holiday calendar is seeded (2026–2027 US federal holidays) | Program admin holiday maintenance | Table, no admin UI. |

## Out of scope
Duplicate-match prompts and merging (DCA-002, blocked on DCA-009), attaching to an existing household (DCA-003), document reuse (DCA-014), RFIs (DCA-016–018), day-20/25 alerts (DCA-036), eligibility, everything else.

## Decisions made while building
_Record interpretation calls here so they can be confirmed with the client._

- **30-day clock is calendar days**, due date = received date + 30. The transcript says "thirty days" with no business-day qualifier, unlike expedited.
- **Expedited = eviction date 0–7 calendar days after the received date** (Housing only). An eviction date already in the past at intake is also treated as expedited.
- **Expedited due date = 3 business days after receipt**, excluding weekends and seeded holidays; the received day is day 0.
- **"Proof of income for everybody over 18"** is computed from each member's date of birth on the received date; a member who is exactly 18 counts as an adult.
- **Verifications are final.** Once a document is verified it can't be changed or removed (enforced in the database too). Correcting a mistaken verification needs a future "addendum"-style feature, like case notes (DCA-038).
- **Checklists are snapshots.** Changes a program admin makes apply to new applications only.
- **Search uses POST**, so SSNs never appear in URLs, server logs or browser history. Found during the in-browser walkthrough, not by tests.
- **Starting from a search result reuses the existing person** (no duplicate); their name/DOB are read-only on the intake form. Attaching to their existing *household* is DCA-003 (out of slice).

## Status
Built 2026-11-11. 79 tests, `trace` 22/22 acceptance criteria covered, full journey exercised in the browser.
