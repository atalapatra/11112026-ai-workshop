# Ledger: DCA Case Management – Requirements Kickoff (2026-11-03)

transcript: dca-case-management-kickoff-transcript.md

Format: each item starts with `## <ID> | <type> | <disposition> | <title>`, then `key: value` metadata lines, a blank line, then the issue body (Markdown).
Types: `story`, `task`, `spike`, `-` (not an issue). Dispositions and rules: see [process/classification-rules.md](../process/classification-rules.md).
A **Source** section with transcript quotes is appended automatically when issues are created.

Transcription note: "Intra I.D." in the transcript is Microsoft **Entra ID**.

---

## DCA-001 | story | backlog | Find existing people with tolerant search
area: intake
sources: 00:04:19, 00:04:50, 00:04:53, 00:05:08

As a **caseworker**, I want search to find a person even when their name or identifiers were entered differently, so that I don't create another duplicate record.

**Acceptance criteria**
- [ ] Search by name, date of birth, SSN (full or last four) and address.
- [ ] Name matching tolerates spelling variants, hyphenated vs. unhyphenated surnames, and spacing differences.
- [ ] SSN matches regardless of formatting (with or without dashes).
- [ ] SSN is optional — search works on name + DOB alone.

## DCA-002 | story | backlog | Show possible duplicate people when starting an application
area: intake
sources: 00:05:10, 00:05:38
blocked_by: DCA-009
labels: blocked

As a **caseworker**, I want the system to show me likely matches when I start a new application, so that I can decide whether this person is already known — without the system merging anyone automatically.

**Acceptance criteria**
- [ ] On new application, system lists candidate matches using name, DOB, last four of SSN and address, with the reason each was matched.
- [ ] System **never** merges records automatically.
- [ ] Caseworker chooses: use existing person, or confirm new person.
- [ ] Merge decisions record who decided and when.

**Notes:** Matching rules depend on the CAMS data profile (DCA-009).

## DCA-003 | story | backlog | Attach a new application to an existing household
area: intake
sources: 00:05:40

As a **caseworker**, I want a new application for a known household to attach to that household, so that we don't re-enter the family from scratch.

**Acceptance criteria**
- [ ] When an existing person/household is selected, the application is created under that household.
- [ ] Existing household members, address and income are pre-filled and can be confirmed or updated.

## DCA-004 | story | backlog | Record a new application at intake
area: intake
sources: 00:04:19, 00:06:32

As a **caseworker**, I want to record household members, income, address and the program applied for, so that the application can be processed.

**Acceptance criteria**
- [ ] Capture household members, income per member, address, and program (Housing, Utility Relief, Child Care).
- [ ] Capture how the application arrived: walk-in, phone, mail, fax (incl. community partners), email.
- [ ] Capture the date received (starts the processing clock — see DCA-033).

## DCA-005 | story | backlog | Household view across all programs
area: household
sources: 00:01:07, 00:01:57, 00:02:56, 00:03:04, 00:03:16, 00:03:25, 00:25:13, 00:25:26, 00:43:20

As a **caseworker**, I want one view of a household across Housing, Utility Relief and Child Care, so that a family tells their story once and I know who else at DCA is working with them.

**Acceptance criteria**
- [ ] Shows every household member.
- [ ] Shows each program applied for or receiving, its status, and the assigned caseworker.
- [ ] Shows documents on file for the household.
- [ ] A caseworker working one program can see that another program's case exists and who owns it.

## DCA-006 | story | backlog | Keep household membership history
area: household
sources: 00:39:31, 00:39:47, 00:39:55

As a **hearing officer**, I want to see who was in the household when a decision was made, so that appeals are judged on the facts at the time.

**Acceptance criteria**
- [ ] Adding/removing a member records effective dates; prior composition is never overwritten.
- [ ] Each application/determination shows household composition as of its date.

## DCA-007 | story | backlog | Flag a child on active Child Care cases in two households
area: household
sources: 00:40:00, 00:40:08, 00:40:16, 00:40:23, 00:40:25, 00:40:29

As a **caseworker**, I want to be warned when a child on my Child Care application is on an active Child Care case in another household, so that we avoid double payments.

**Acceptance criteria**
- [ ] A person can belong to more than one household.
- [ ] If a child is on an active Child Care case elsewhere, the system shows a flag.
- [ ] The flag **does not block** the application (split custody is legitimate); caseworker records how it was resolved.

## DCA-008 | story | backlog | Refer a household to another program
area: household
sources: 00:25:35, 00:25:54
blocked_by: DCA-090
labels: blocked

As a **caseworker**, I want to refer a household I'm serving to another program with one action, so that the new application starts with what we already know.

**Acceptance criteria**
- [ ] "Refer to <program>" creates a new application for the target program.
- [ ] Household, income, and reusable documents carry over (subject to DCA-014).
- [ ] Consent handling per decision DCA-090.

## DCA-009 | spike | backlog | Profile CAMS person data to size duplicates and design matching
area: migration
sources: 00:05:48, 00:05:58, 00:06:02, 00:06:22

**Question:** How bad is duplication in CAMS, and which identifiers are populated reliably enough to match on?

**Time-box:** 1 week.

**Approach:** Take a copy of CAMS person data (in an approved environment); measure field completeness (SSN, DOB, address), estimate duplicate rate, and sample known duplicates.

**Output:** Data profile report + recommended matching rules for DCA-002 and dedup approach for DCA-080.

## DCA-010 | task | backlog | Design phase-one architecture so a public portal can plug in later
area: public-access
sources: 00:06:56, 00:07:08, 00:07:15, 00:07:22

Phase one is staff-facing only. Design intake and case services (e.g. API-first) so a future resident portal (DCA-102) can be added without rework.

**Done when:** Architecture decision record approved by Priya Raman (IT) and Dana Whitfield (sponsor).

## DCA-011 | story | backlog | Program-specific document checklist
area: documents
sources: 00:07:33, 00:07:58, 00:08:02

As a **caseworker**, I want the system to show the documents each program requires, so that I know what's missing without a paper checklist.

**Acceptance criteria**
- [ ] Housing: ID, lease, eviction or past-due notice, proof of income for every household member over 18.
- [ ] Utility Relief: ID, income, utility bill; shutoff notice if requesting emergency assistance.
- [ ] Child Care: income, proof of work or school for the parent, birth certificate (or equivalent) for each child.
- [ ] Items can be checked off as received.
- [ ] Required documents are configurable by a program admin.

## DCA-012 | story | backlog | Record who verified each document and when
area: documents
sources: 00:03:53, 00:08:02, 00:08:26

As a **QA reviewer**, I want every verified document to show who verified it, when, and what was looked at, so that "income verified" findings stop.

**Acceptance criteria**
- [ ] Checking off a checklist item stores the verifying user, timestamp, and the document it's linked to.
- [ ] Verification history is visible on the case and cannot be edited.

## DCA-013 | story | backlog | Capture documents by scan, upload, or tablet photo
area: documents
sources: 00:08:35

As a **caseworker**, I want to add documents by scanning at the front desk, uploading emailed files, or photographing them on a tablet during a home visit, so that all documents live in the case.

**Acceptance criteria**
- [ ] Upload from desktop (scanner output, email attachments).
- [ ] Capture a photo from a tablet camera.
- [ ] Each document is tagged with type and linked to a person/household.

## DCA-014 | story | backlog | Reuse household documents across applications
area: documents
sources: 00:03:25, 00:08:51, 00:09:03
blocked_by: DCA-086
labels: blocked

As a **caseworker**, I want documents a family already gave us to be reused on their other applications while still valid, so that we don't ask for the same pay stub twice.

**Acceptance criteria**
- [ ] Documents on file for a household are offered to satisfy checklist items on new applications.
- [ ] A document is only reusable within its age limit for that program and document type (limits configurable — values per DCA-086).
- [ ] Expired documents are shown but not counted as satisfying the checklist.

## DCA-015 | task | backlog | Encrypt and access-control stored documents
area: security
sources: 00:09:32

Stored documents (IDs, Social Security cards, pay stubs) must be encrypted at rest and in transit and restricted by role, per DCA security standards (DCA-095).

**Done when:** Controls documented and verified against Priya Raman's standards.

## DCA-016 | story | backlog | Generate request-for-information letter with 10-day due date
area: documents
sources: 00:09:45, 00:09:50, 00:09:57, 00:10:31

As a **caseworker**, I want to generate a request-for-information letter listing the missing documents, so that the family knows exactly what to send and by when.

**Acceptance criteria**
- [ ] Letter lists the outstanding checklist items.
- [ ] Due date = 10 days from the letter date, tracked on the case.
- [ ] The 30-day processing clock **does not pause** while waiting.
- [ ] After the due date, the caseworker may deny for missing information.

## DCA-017 | story | backlog | Extend an RFI due date with a required reason
area: documents
sources: 00:10:10, 00:10:20, 00:10:29

As a **caseworker**, I want to extend the RFI due date, so that families with genuine obstacles aren't denied.

**Acceptance criteria**
- [ ] Extension requires a reason; save is blocked without one.
- [ ] Extension, reason, user and date are visible on the case for appeals.

## DCA-018 | story | backlog | Remind the caseworker when an RFI is due
area: documents
sources: 00:10:41

As a **caseworker**, I want a reminder when the 10-day RFI period ends, so that I don't forget to follow up.

**Acceptance criteria**
- [ ] Reminder appears in the caseworker's work queue on the due date.

## DCA-019 | story | backlog | Eligibility recommendation with caseworker determination
area: eligibility
sources: 00:11:11, 00:11:15, 00:11:17, 00:26:14, 00:26:21, 00:26:23, 00:26:47, 00:26:51, 00:27:04, 00:27:09, 00:40:56

As a **caseworker**, I want the system to calculate and show a recommended eligibility outcome while I record the actual determination, so that the math is done for me but a person legally decides.

**Acceptance criteria**
- [ ] System calculates a recommended outcome from program rules (DCA-020/021/022) and shows the calculation.
- [ ] Caseworker records the determination; the record shows **who** decided and when.
- [ ] If the determination differs from the recommendation, a reason is required.
- [ ] The system never records a determination on its own.

**Notes:** Supersedes the earlier "system decides automatically" request (DCA-108) per DCA general counsel.

## DCA-020 | story | backlog | Housing eligibility rules
area: eligibility
sources: 00:10:53, 00:11:39, 00:11:43

As a **caseworker**, I want the Housing recommendation to apply Housing's rules, so that it reflects policy.

**Acceptance criteria**
- [ ] Income limit by household size as a % of area median income.
- [ ] State residency.
- [ ] Housing crisis evidenced by eviction notice or past-due notice.

## DCA-021 | story | backlog | Utility Relief eligibility rules
area: eligibility
sources: 00:10:53, 00:11:43

As a **caseworker**, I want the Utility Relief recommendation to apply Utility's rules, so that it reflects policy.

**Acceptance criteria**
- [ ] Income limit by household size as a % of area median income.
- [ ] Utility bill on file.

## DCA-022 | story | backlog | Child Care eligibility rules
area: eligibility
sources: 00:10:53, 00:11:43

As a **caseworker**, I want the Child Care recommendation to apply Child Care's rules, so that it reflects policy.

**Acceptance criteria**
- [ ] Income limit by household size as a % of area median income.
- [ ] Parent meets work or school requirement.
- [ ] Child is under 13, or under 18 if the child has a disability.

## DCA-023 | story | backlog | Program admin maintains thresholds and limits
area: eligibility
sources: 00:12:00, 00:12:06, 00:12:13, 00:13:30

As a **program admin**, I want to update income limits, approval thresholds and other rule values myself, so that annual changes don't need a vendor change request.

**Acceptance criteria**
- [ ] Income limits, AMI percentages, approval thresholds and similar values are editable in an admin screen by the program admin role.
- [ ] Values have effective dates; applications use the values in effect on their received date.
- [ ] Changes are audit-logged.

## DCA-024 | task | backlog | Load current and next-year income limit tables before go-live
area: eligibility
sources: 00:12:28, 00:12:46

Load this year's income limits and next spring's new limits before go-live, using the DCA-023 admin feature — not an IT script.

**Done when:** Both years loaded and verified by the program team; Priya's annual CAMS script is retired.

## DCA-025 | story | backlog | QA list of determinations that differ from the recommendation
area: qa
sources: 00:11:29

As a **QA manager**, I want a list of determinations where the caseworker departed from the recommendation, with reasons, so that I can sample them.

**Acceptance criteria**
- [ ] Filter by program, date range, region, caseworker.
- [ ] Shows recommendation, determination, and reason.

## DCA-026 | story | backlog | Supervisor approval for Housing payments over a threshold
area: approvals
sources: 00:12:48, 00:12:53, 00:12:55, 00:13:07, 00:13:30

As a **supervisor**, I want Housing payments above the threshold routed to me for approval before they're paid, so that large payments get a second look.

**Acceptance criteria**
- [ ] Approved Housing determinations with payment above the configured threshold go to the supervisor's approval queue.
- [ ] Payment is not released (not in the payment file) until approved.
- [ ] Threshold is configurable (DCA-023); initial value per decision DCA-087.

## DCA-027 | story | backlog | Supervisor review of denials by new caseworkers
area: approvals
sources: 00:13:36, 00:13:41, 00:13:52, 00:13:58

As a **supervisor**, I want every denial by a caseworker in their first 90 days to come to me for review, so that we reduce reversals on appeal.

**Acceptance criteria**
- [ ] Caseworker start date is recorded; denials within 90 days of it route to the supervisor before the notice is issued.
- [ ] The 90-day period is configurable.

## DCA-028 | story | backlog | Route applications to the regional office by residence
area: assignment
sources: 00:15:15

As a **supervisor**, I want new applications to land in my regional office's queue based on where the applicant lives, so that I only assign my region's work.

**Acceptance criteria**
- [ ] Region determined from the household address.
- [ ] Supervisors can route statewide/exception cases manually.

## DCA-029 | story | backlog | Suggest an assignee for new applications
area: assignment
sources: 00:14:25, 00:14:28, 00:14:30, 00:14:55, 00:15:03, 00:15:09

As a **supervisor**, I want the system to suggest who should get a new application, so that I can assign with one click while keeping control.

**Acceptance criteria**
- [ ] Suggestion considers: caseworker already serving the household, language match (e.g. Spanish, Vietnamese), current caseload.
- [ ] Supervisor accepts the suggestion or picks someone else.
- [ ] No automatic assignment.

## DCA-030 | story | backlog | Bulk reassign a caseworker's caseload
area: assignment
sources: 00:15:24, 00:15:39

As a **supervisor**, I want to move all or selected cases from one caseworker to others at once, so that leave and absences don't cost me an afternoon.

**Acceptance criteria**
- [ ] Select a caseworker, select all/some open cases, reassign to one or more caseworkers.
- [ ] Reassignments are audit-logged.

## DCA-031 | story | backlog | Supervisor team workload dashboard
area: deadlines
sources: 00:15:41, 00:15:47

As a **supervisor**, I want a screen showing each caseworker's open cases and which are near deadline, so that I can retire the whiteboard.

**Acceptance criteria**
- [ ] Per caseworker: open case count, cases at/after day 20, expedited cases.
- [ ] Drill into a caseworker's list.

## DCA-032 | story | backlog | Director dashboard rolled up by region
area: deadlines
sources: 00:16:00, 00:16:08, 00:16:17, 00:16:24

As the **deputy director**, I want the team workload view rolled up by region, so that I can see current performance each morning.

**Acceptance criteria**
- [ ] Open cases, near-deadline cases, and timeliness by region and program.
- [ ] Data is current as of today at minimum (exact refresh interval per DCA-093).

## DCA-033 | story | backlog | Track the 30-day processing clock on every application
area: deadlines
sources: 00:02:29, 00:09:57

As a **caseworker**, I want each application to show days elapsed and days remaining against the 30-day standard, so that I can prioritize.

**Acceptance criteria**
- [ ] Clock starts on the received date; applies to all three programs.
- [ ] Clock does not pause for RFIs.
- [ ] Shows days remaining in lists and on the case.

## DCA-034 | story | backlog | Automatically flag expedited Housing cases
area: deadlines
sources: 00:16:36, 00:16:48, 00:16:51, 00:16:59, 00:17:07

As a **caseworker**, I want Housing applications with an eviction scheduled within 7 days to be flagged expedited automatically, so that we meet the 3-business-day deadline.

**Acceptance criteria**
- [ ] Entering an eviction date within 7 days of receipt sets the case to expedited.
- [ ] Expedited due date = 3 business days from receipt (business-day calendar with state holidays).
- [ ] Does not depend on the paper-form checkbox.

## DCA-035 | story | backlog | Expedited cases go to the top and alert prominently
area: deadlines
sources: 00:17:15, 00:17:21

As a **caseworker**, I want expedited cases at the top of my queue with an obvious alert, so that they can't be missed.

**Acceptance criteria**
- [ ] Expedited cases sort first in work queues.
- [ ] Visually distinct (e.g. red) and generate a notification to the assigned caseworker and supervisor.

## DCA-036 | story | backlog | Day-20 and day-25 deadline alerts
area: deadlines
sources: 00:17:24

As a **caseworker**, I want an alert at day 20, and my supervisor and I want one at day 25, so that regular cases don't miss day 30.

**Acceptance criteria**
- [ ] Day 20: notify assigned caseworker.
- [ ] Day 25: notify caseworker and supervisor.

## DCA-037 | story | backlog | Weekly regional timeliness alert to the director
area: deadlines
sources: 00:17:35, 00:17:46, 00:17:53, 00:18:01

As the **deputy director**, I want a weekly email when a region falls behind, so that I can intervene.

**Acceptance criteria**
- [ ] Sent Monday morning.
- [ ] Lists regions where more than 10% of open cases are past day 25 (threshold configurable).

## DCA-038 | story | backlog | Case notes cannot be edited once saved; corrections are addenda
area: case-notes
sources: 00:18:09
blocked_by: DCA-088
labels: blocked

As a **hearing officer**, I want saved case notes to be unchangeable with corrections added as addenda, so that the record shows what we knew and when.

**Acceptance criteria**
- [ ] Saved notes are read-only; an addendum links to the original and both are shown.
- [ ] Any edit window is per decision DCA-088 (default: none).

## DCA-039 | story | backlog | Search case notes
area: case-notes
sources: 00:19:05

As a **caseworker**, I want to search a case's notes, so that I can find e.g. when we talked to the landlord without scrolling.

**Acceptance criteria**
- [ ] Notes are separate entries (not one text block) with author and date.
- [ ] Keyword search and filter by contact type and date.

## DCA-040 | story | backlog | Tag case notes with contact type
area: case-notes
sources: 00:19:17, 00:19:24

As a **caseworker**, I want to tag each note with a contact type, so that notes are easy to scan and filter.

**Acceptance criteria**
- [ ] Contact types include phone call, home visit, office visit, landlord contact; list is configurable.

## DCA-041 | story | backlog | Tamper-proof audit log of views and changes
area: security
sources: 00:19:28, 00:19:34, 00:19:46, 00:19:51

As an **IT security admin**, I want a full audit log of who viewed or changed what, when and from where, so that we can investigate misuse.

**Acceptance criteria**
- [ ] Logs record views and changes with user, timestamp, record, and source (IP/device).
- [ ] No one, including admins, can edit or delete log entries.
- [ ] Retained 7 years after case closure.

## DCA-042 | story | backlog | Restrict access to sensitive cases
area: security
sources: 00:19:57, 00:20:19

As the **appeals & QA manager**, I want employee, employee-relative, and domestic-violence cases restricted to authorized staff, so that no one browses them.

**Acceptance criteria**
- [ ] A case can be marked restricted with a reason (employee, relative of employee, domestic violence).
- [ ] Only users in an authorized group can open restricted cases.
- [ ] Every view of a restricted case is logged.

## DCA-043 | story | backlog | Report of who viewed restricted cases
area: security
sources: 00:20:22

As the **appeals & QA manager**, I want a report of every view of restricted cases, so that inappropriate access is caught.

**Acceptance criteria**
- [ ] Filter by case, user, date range; shows user, timestamp, action.

## DCA-044 | story | backlog | Hide confidential addresses for domestic violence cases
area: security
sources: 00:20:30, 00:20:36
blocked_by: DCA-089
labels: blocked

As a **caseworker**, I want a domestic-violence client's address hidden everywhere except where I need it to work the case, so that it can't leak.

**Acceptance criteria**
- [ ] Address is suppressed from list screens, reports, and exports.
- [ ] Whether the whole case is restricted per decision DCA-089.

## DCA-045 | story | backlog | Sign in with state account via Entra ID and MFA
area: platform
sources: 00:32:57

As a **DCA staff member**, I want to sign in with my state account, so that I don't manage another password.

**Acceptance criteria**
- [ ] SSO with Microsoft Entra ID; MFA enforced.
- [ ] No local usernames/passwords.

## DCA-046 | task | backlog | Register the app in Entra ID and create role security groups
area: platform
sources: 00:33:08

DCA IT registers the application in Entra ID and creates a security group per role (DCA-047). **Needed before developers can sign in to the test environment — schedule first.**

**Owner:** Priya Raman's team.

## DCA-047 | story | backlog | DCA IT manages role-based access
area: platform
sources: 00:33:24

As an **IT admin**, I want to control which role each user has, so that DCA — not the vendor — manages access.

**Acceptance criteria**
- [ ] Roles: caseworker, supervisor, hearing officer, QA reviewer, program admin, IT admin, read-only auditor.
- [ ] Role membership driven by Entra security groups managed by DCA IT.

## DCA-048 | task | backlog | Host in the state cloud at FedRAMP Moderate
area: platform
sources: 00:33:36, 00:33:48

Hosting must be in the DCA state cloud environment, meeting the FedRAMP Moderate baseline (federal Utility Relief funds). Requirements in Priya's ~40-page security document (DCA-095).

## DCA-049 | task | backlog | Provision development, test, and training environments
area: platform
sources: 00:33:51, 00:44:11, 00:44:25

Stand up dev, test and training environments in the state cloud account. Agree a responsibility split (DCA IT vs. Northgate) first. Training uses fake data only (DCA-083).

## DCA-050 | story | backlog | Section 508 accessibility
area: platform
sources: 00:34:04, 00:34:08
labels: accessibility

As a **caseworker who uses a screen reader**, I want every screen to work with assistive technology, so that I can do my job without a coworker's help.

**Acceptance criteria**
- [ ] Meets Section 508 / WCAG 2.1 AA.
- [ ] Core workflows tested end-to-end with a screen reader by a real user.

## DCA-051 | story | backlog | Open a case in a few seconds
area: platform
sources: 00:36:30, 00:36:32, 00:36:42, 00:36:47

As a **caseworker** with a client in front of me, I want a case to open within a few seconds, so that I'm not waiting 40 seconds like in CAMS.

**Acceptance criteria**
- [ ] Case opens in ≤ 3 seconds at the 95th percentile under peak load (target to confirm).

## DCA-052 | task | backlog | Load test for January peak before go-live
area: platform
sources: 00:36:51, 00:37:02, 00:37:08, 00:37:19, 00:37:23

Prove the system handles a January Monday morning: ~180 staff users, ~120 concurrent, application volume ~3× normal (≈40,000 applications/year baseline — Dana to confirm, DCA-097). Results reviewed by Priya before go-live.

## DCA-053 | story | backlog | Learnable without lengthy training
area: platform
sources: 00:03:04

As a **new caseworker**, I want the system to be intuitive, so that I don't need two weeks of training to use it.

**Acceptance criteria**
- [ ] Usability test: a caseworker new to the system completes intake for a sample application with no more than a short orientation (target set with DCA).

## DCA-054 | story | backlog | Generate determination notices from templates
area: notices
sources: 00:20:54, 00:20:59, 00:21:12, 00:21:21

As a **caseworker**, I want approval and denial notices generated from standard templates, so that every notice is consistent and legally complete.

**Acceptance criteria**
- [ ] Template chosen by program and outcome.
- [ ] Denial reasons selected from the standard reason-code list (DCA-055); caseworker may add an explanation.
- [ ] Appeal-rights language is always included and cannot be removed or edited by staff.

## DCA-055 | task | backlog | Clean up and load denial reason codes
area: notices
sources: 00:21:37

Consolidate the ~60 reason codes in Linda's spreadsheet (several are duplicates), get sign-off, and load them. Required before notices can be used.

## DCA-056 | task | backlog | Consolidate notice templates and translate to Spanish
area: notices
sources: 00:22:06, 00:22:22

Review the ~40 Word templates across the three programs (some unchanged since 2015, some with the pre-2020 Eastside address), consolidate them, and translate the new set into Spanish.

## DCA-057 | story | backlog | Notices in English and Spanish, other languages on request
area: notices
sources: 00:21:52, 00:21:59

As a **caseworker**, I want to send notices in the family's language, so that families understand them.

**Acceptance criteria**
- [ ] Every template available in English and Spanish.
- [ ] Preferred language recorded on the household.
- [ ] Other languages (Vietnamese, Haitian Creole, Somali, ...) can be flagged for translation on request.

## DCA-058 | story | backlog | Deliver notices by central mail or email with consent
area: notices
sources: 00:22:28, 00:22:32

As a **caseworker**, I want notices sent via central print/mail by default, or email when the family agrees, so that delivery follows their preference.

**Acceptance criteria**
- [ ] Notices queue for the central print center.
- [ ] Email delivery only when consent is recorded.

## DCA-059 | story | backlog | Record when each notice was generated and mailed
area: notices
sources: 00:38:23, 00:38:38, 00:38:45

As a **hearing officer**, I want proof of when a notice was generated and mailed, so that I can determine whether an appeal was timely.

**Acceptance criteria**
- [ ] Notice record stores generated date and mailed date.
- [ ] Mailed date can be recorded from the print center's daily manifest (manual entry until DCA-060 resolves automation).

## DCA-060 | spike | backlog | Investigate importing the print center's mailing manifest
area: notices
sources: 00:38:54

**Question:** Can the print center's daily mailed-items manifest (currently a PDF) be received in a machine-readable form and matched to notices?

**Time-box:** 3 days.

**Output:** Recommendation (integration, structured file, or manual entry) for DCA-059.

## DCA-061 | story | backlog | Log an appeal request and check timeliness
area: appeals
sources: 00:23:12, 00:23:18, 00:23:39

As an **appeals staff member**, I want to log an appeal on the case when it arrives, so that requests aren't lost on paper.

**Acceptance criteria**
- [ ] Record date received and channel (phone, mail, in person).
- [ ] System checks whether it's within 30 days of the notice date and shows the result.
- [ ] Applies to denials and benefit reductions.

## DCA-062 | story | backlog | Assign a hearing officer with no conflict of interest
area: appeals
sources: 00:23:39, 00:23:57, 00:24:01

As the **appeals manager**, I want to assign a hearing officer to an appeal, so that it gets heard — and the system must prevent assigning anyone who worked the original case.

**Acceptance criteria**
- [ ] Anyone who worked on the original case (assigned, determined, approved) cannot be selected — **blocked, not warned**.

## DCA-063 | story | backlog | Schedule a hearing with at least 10 days' notice
area: appeals
sources: 00:24:03

As a **hearing officer**, I want to schedule a hearing and send the family a hearing notice, so that they have at least 10 days' notice.

**Acceptance criteria**
- [ ] Hearing date cannot be less than 10 days after the hearing notice date.
- [ ] Hearing notice generated (with DCA-054 templates).

## DCA-064 | story | backlog | Record hearing outcome and return reversed/remanded cases
area: appeals
sources: 00:24:03, 00:24:18, 00:24:23, 00:24:27, 00:24:33, 00:24:40

As a **hearing officer**, I want to record the outcome, so that the case proceeds correctly.

**Acceptance criteria**
- [ ] Outcomes: upheld, reversed, remanded.
- [ ] Reversed/remanded cases go back to the regional office supervisor's queue for reassignment (supervisor decides who; default suggestion excludes the original caseworker).

## DCA-065 | story | backlog | Continue Child Care benefits pending appeal
area: appeals
sources: 00:24:43, 00:25:01, 00:25:05

As a **Child Care family**, I want my benefits to continue at the current level if I appeal a reduction or termination within 10 days, so that care isn't disrupted (federal requirement).

**Acceptance criteria**
- [ ] Applies to Child Care only.
- [ ] Appeal received within 10 days of the notice → benefits continue at current level until the hearing decision.
- [ ] Appeal after 10 days → no continuation.

## DCA-066 | story | backlog | Nightly payment file for finance
area: payments
sources: 00:27:12, 00:27:18, 00:27:34, 00:27:56, 00:27:59, 00:28:02
blocked_by: DCA-067
labels: blocked

As a **finance staff member**, I want a nightly file of approved payments, so that I can upload it to WestPay as today.

**Acceptance criteria**
- [ ] Includes approved payments to landlords (Housing), utility companies (Utility), and providers (Child Care).
- [ ] Excludes payments awaiting supervisor approval (DCA-026).
- [ ] Layout matches what finance requires (DCA-067).

## DCA-067 | spike | backlog | Document the CAMS payment file layout with finance
area: payments
sources: 00:28:09, 00:28:28

**Question:** What format does finance need for the WestPay upload? The CAMS layout isn't documented.

**Time-box:** 1 week.

**Output:** Written file specification agreed with the finance team.

## DCA-068 | story | backlog | Landlord and vendor registry with duplicate checking
area: payments
sources: 00:28:31, 00:28:53, 00:28:59

As a **caseworker**, I want to find or register a landlord/vendor once, with the system warning about likely duplicates, so that one landlord isn't paid under five names.

**Acceptance criteria**
- [ ] Vendor record holds legal name, W-9, address, bank details.
- [ ] Possible duplicates (name variants like "Smith Properties" vs "Smith Property Management LLC") are shown on creation; staff decide.

## DCA-069 | story | backlog | Mask vendor bank account details
area: payments
sources: 00:29:02

As an **IT security admin**, I want full bank account numbers visible only to authorized roles, so that sensitive data is limited.

**Acceptance criteria**
- [ ] Caseworkers see masked account numbers (e.g. last four).

## DCA-070 | story | backlog | Monthly legislative report
area: reporting
sources: 00:29:33, 00:29:42

As the **deputy director**, I want the monthly legislative report generated by the system, so that my team stops spending four days a month building it.

**Acceptance criteria**
- [ ] Applications received, approved, denied — by program and county.
- [ ] Timeliness: % within 30 days, % expedited within 3 days.
- [ ] Average benefit amount; denial reasons.
- [ ] Matches the current templates (DCA-097).

## DCA-071 | story | backlog | Quarterly federal Utility Relief report
area: reporting
sources: 00:29:42

As the **deputy director**, I want the quarterly federal report for Utility Relief generated by the system, so that federal reporting is accurate and fast.

**Acceptance criteria**
- [ ] Same measures as DCA-070 for Utility Relief, quarterly, in the federal format.

## DCA-072 | story | backlog | Export lists to Excel with privacy controls
area: reporting
sources: 00:30:13, 00:30:23, 00:30:26, 00:30:29, 00:30:46, 00:30:48, 00:30:54, 00:30:59

As a **supervisor**, I want to export what I'm viewing to Excel, so that I can work with my team's numbers.

**Acceptance criteria**
- [ ] Export available on case lists and dashboards (priority: open cases with days remaining; monthly closures per caseworker).
- [ ] Exports never include SSNs.
- [ ] Restricted-case rules and DV address suppression apply.
- [ ] Every export is logged (who, what, when).

## DCA-073 | story | backlog | Monthly random QA sample and assignment
area: qa
sources: 00:31:10, 00:31:14

As the **QA manager**, I want the system to draw a random monthly sample of closed cases and assign them to reviewers, so that no one hand-picks file numbers.

**Acceptance criteria**
- [ ] 25 closed cases per program per month (configurable), randomly selected.
- [ ] Assigned to QA reviewers.

## DCA-074 | story | backlog | QA review checklist
area: qa
sources: 00:31:14, 00:31:37, 00:31:41

As a **QA reviewer**, I want to complete the review checklist in the system, so that results are captured consistently.

**Acceptance criteria**
- [ ] Common questions plus program-specific questions (from Linda's current forms, DCA-096).

## DCA-075 | story | backlog | QA results rollup
area: qa
sources: 00:31:14

As the **QA manager**, I want review results to roll up, so that I can see error trends.

**Acceptance criteria**
- [ ] Summaries by program, region, caseworker and question.

## DCA-076 | story | backlog | Flag Child Care recertification at 45 days and send renewal packet
area: recertification
sources: 00:31:49, 00:31:55, 00:31:57

As a **caseworker**, I want Child Care cases flagged 45 days before their 6-month end date with a renewal packet sent, so that I stop tracking renewals in a spreadsheet.

**Acceptance criteria**
- [ ] Certification period = 6 months.
- [ ] At 45 days before end: case flagged and renewal packet sent to the family.

## DCA-077 | story | backlog | Follow up and close non-responsive Child Care recertifications
area: recertification
sources: 00:31:57, 00:32:22, 00:32:24

As a **caseworker**, I want the system to follow up and, if there's still no response by the end date, close the case with a notice, so that renewals don't slip.

**Acceptance criteria**
- [ ] Follow-up sent if no response (timing to confirm).
- [ ] At end date with no response: case closes; closure notice with appeal rights sent.
- [ ] Reinstatement window per decision DCA-091.

## DCA-078 | story | backlog | Lock closed cases; reopening needs a reason and supervisor approval
area: case-notes
sources: 00:38:58, 00:39:09, 00:39:15, 00:39:18, 00:39:27

As the **QA manager**, I want closed cases to be locked, so that the record is final.

**Acceptance criteria**
- [ ] Closed cases are read-only.
- [ ] Reopen requires a reason and supervisor approval; approval is quick (single click in the supervisor's queue).

## DCA-079 | spike | backlog | Map the CAMS database
area: migration
sources: 00:34:20, 00:34:48

**Question:** What is actually in CAMS? Several tables are unexplained; the builder retired in 2017.

**Time-box:** 2 weeks.

**Output:** Data inventory (tables, meaning, volumes, quality) to inform migration scope (DCA-092) and dedup (DCA-080).

## DCA-080 | task | backlog | Deduplicate person and landlord records during migration
area: migration
sources: 00:35:19, 00:35:26
blocked_by: DCA-009, DCA-079
labels: blocked

Whatever is migrated must be deduplicated first so we don't move the mess. Uses matching rules from DCA-009; caseworker/data steward confirms merges.

## DCA-081 | story | backlog | Use the system on a tablet during field visits
area: platform
sources: 00:35:28, 00:36:22

As a **caseworker doing home visits**, I want the system to work well on a tablet, so that I can work in rural counties.

**Acceptance criteria**
- [ ] Core screens (case view, notes, document photo capture) usable on a tablet.
- [ ] Offline capture is out of scope here (see DCA-107, DCA-082).

## DCA-082 | spike | backlog | Assess device management for offline notes and photos
area: platform
sources: 00:35:45, 00:36:04, 00:36:22

**Question:** Can DCA device management support limited offline capture safely?

**Time-box:** 1 week.

**Investigate:** remote wipe; encryption of locally stored data; behaviour when a tablet doesn't connect for a week.

**Output:** Feasibility recommendation to Priya; decides whether DCA-107 moves out of the parking lot.

## DCA-083 | task | backlog | Build a realistic fake data set for training
area: training
sources: 00:44:29, 00:44:33, 00:44:41, 00:44:48

Create realistic synthetic data — households, income, documents, appeals, etc. — so training feels real. No production data. Not "Test Person One".

## DCA-084 | task | backlog | Plan training and go-live communication for staff
area: training
sources: 00:44:11, 00:44:25

Staff must know about and practice on the new system before go-live (in 2019 they found out the morning of). Produce a training schedule and communication plan.

## DCA-085 | spike | backlog | Explore SMS vendor and contract options
area: notices
sources: 00:22:46

**Question:** Does the state have a texting contract, and what would SMS require (vendor, consent storage, opt-out)?

**Time-box:** 3 days.

**Output:** Options summary so the parked text-reminder feature (DCA-103) can be scheduled.

## DCA-086 | task | backlog | Decision: document age limits by program and document type
area: documents
sources: 00:09:03, 00:09:09, 00:09:12, 00:09:18, 00:09:25, 00:42:09, 00:42:26
labels: decision

**Owner:** Dana Whitfield (policy team).
**Question:** How old may each document type be for each program? (Pay stubs: 30 days for Housing per Marcus; possibly 60 for Child Care.)
**Blocks:** DCA-014.

## DCA-087 | task | backlog | Decision: Housing supervisor approval threshold
area: approvals
sources: 00:13:09, 00:13:14, 00:13:18, 00:13:22, 00:42:09, 00:42:26
labels: decision

**Owner:** Dana Whitfield.
**Question:** Is the threshold $3,500 (Marcus: lowered in July, per memo) or $5,000 (Dana)?
**Input:** Marcus's memo (DCA-094).
**Affects:** DCA-026 (configurable, so not blocking build).

## DCA-088 | task | backlog | Decision: case note editing window vs. addendum-only
area: case-notes
sources: 00:18:28, 00:18:37, 00:18:39, 00:18:47, 00:18:56, 00:19:00, 00:41:43, 00:41:46, 00:42:09
labels: decision

**Owner:** Linda Castellanos with DCA legal.
**Options:** addendum-only (Linda) vs. same-day/one-hour self-edit window (Marcus).
**Blocks:** DCA-038.

## DCA-089 | task | backlog | Decision: domestic violence restriction scope
area: security
sources: 00:20:30, 00:20:36, 00:20:52, 00:42:09
labels: decision

**Owner:** Linda Castellanos.
**Question:** Is the whole case restricted, or only the address?
**Blocks:** DCA-044.

## DCA-090 | task | backlog | Decision: family consent before a cross-program referral
area: household
sources: 00:25:57, 00:26:02, 00:26:07, 00:26:12, 00:42:09
labels: decision

**Owner:** Dana Whitfield (policy).
**Question:** Must the family agree before a referral creates a new application? How is consent recorded?
**Blocks:** DCA-008.

## DCA-091 | task | backlog | Decision: Child Care reinstatement window after non-response closure
area: recertification
sources: 00:32:27, 00:32:35, 00:32:41, 00:32:47, 00:42:09
labels: decision

**Owner:** Dana Whitfield (policy).
**Question:** Is there a 30-day window to reinstate without a full new application?
**Affects:** DCA-077.

## DCA-092 | task | backlog | Decision: CAMS migration scope
area: migration
sources: 00:34:24, 00:34:29, 00:34:39, 00:35:07, 00:35:11, 00:42:09
blocked_by: DCA-079
labels: decision

**Owner:** Dana Whitfield with Priya Raman and Linda Castellanos.
**Options:** open cases only; open + 7 years of closed cases (retention schedule); or keep CAMS read-only as an archive (Priya prefers retiring CAMS — server out of support).
**Input:** CAMS data map (DCA-079).

## DCA-093 | task | backlog | Decision: dashboard refresh frequency
area: deadlines
sources: 00:16:08, 00:16:17, 00:16:24
labels: decision

**Owner:** Sam Patel to follow up with Dana Whitfield.
**Question:** Is every-15-minutes acceptable, or is daily enough? Minimum: current as of today.
**Affects:** DCA-031, DCA-032.

## DCA-094 | task | backlog | Receive Marcus's memo on the approval threshold
area: approvals
sources: 00:13:18, 00:42:26, 00:42:33
labels: action-item

**Owner:** Marcus Oyelaran → Dana Whitfield. Input to DCA-087.

## DCA-095 | task | backlog | Receive security requirements and integration standards
area: security
sources: 00:09:32, 00:33:36, 00:42:36
labels: action-item

**Owner:** Priya Raman. Review and trace into DCA-015, DCA-048 and other security items.

## DCA-096 | task | backlog | Receive appeal forms, notice templates, and QA checklist
area: appeals
sources: 00:31:41, 00:31:46, 00:42:41
labels: action-item

**Owner:** Linda Castellanos. Inputs to DCA-054, DCA-056, DCA-074 and the appeals stories.

## DCA-097 | task | backlog | Receive legislative report templates and application volumes
area: reporting
sources: 00:30:06, 00:30:10, 00:37:23, 00:42:46
labels: action-item

**Owner:** Dana Whitfield. Inputs to DCA-070, DCA-071, DCA-052 (~40,000 applications/year to confirm).

## DCA-098 | task | backlog | Hold appeals and QA deep-dive session
area: appeals
sources: 00:42:51
labels: action-item

**Owner:** Jordan Ellis to schedule with Linda Castellanos.

## DCA-099 | task | backlog | Hold reporting deep-dive session
area: reporting
sources: 00:42:51
labels: action-item

**Owner:** Jordan Ellis to schedule with Dana Whitfield and the staff who build reports today.

## DCA-100 | task | backlog | Observe caseworkers at work
area: intake
sources: 00:42:51, 00:43:10
labels: action-item

**Owner:** Jordan Ellis with Marcus Oyelaran. Shadow two caseworkers (Teresa and Andre).

## DCA-101 | task | backlog | Send kickoff meeting notes
area: platform
sources: 00:43:53
labels: action-item

**Owner:** Sam Patel. Due end of day Thursday, 2026-11-05.

## DCA-102 | story | parking-lot | Residents apply online through a public portal
area: public-access
sources: 00:06:40, 00:06:56, 00:07:25, 00:41:51

As a **resident**, I want to apply and upload documents from my phone, so that I don't have to come to the front desk.

**Parked:** future phase — public-facing, needs identity proofing and a different security posture. Phase one must not preclude it (DCA-010).

## DCA-103 | story | parking-lot | Text message reminders to families ⭐
area: notices
sources: 00:22:37, 00:22:46, 00:23:03, 00:23:09, 00:41:51

As a **family**, I want text reminders like "Your documents are due Friday", so that I respond on time.

**Parked (starred by sponsor):** needs messaging vendor, consent storage and opt-out. Discovery in DCA-085.

## DCA-104 | story | parking-lot | Direct WestPay integration
area: payments
sources: 00:27:34, 00:28:02, 00:41:51

As a **finance staff member**, I want payments sent to WestPay automatically, so that no manual upload is needed.

**Parked:** Department of Finance intake takes 6–9 months. Phase one uses the nightly file (DCA-066).

## DCA-105 | story | parking-lot | Import Westmarch Power shutoff list as an outreach list
area: payments
sources: 00:29:09, 00:29:22, 00:29:27, 00:29:30, 00:41:51

As a **caseworker**, I want the weekly Westmarch Power shutoff list imported as an outreach list, so that we can reach families before shutoff.

**Parked (no star):** outside-party integration.

## DCA-106 | story | parking-lot | Public chatbot for eligibility and status questions
area: public-access
sources: 00:37:55, 00:38:06, 00:38:18, 00:41:51

As a **resident**, I want to ask a chatbot "Am I eligible?" or "Where's my application?", so that I get answers without calling.

**Parked:** public-facing (same as portal); status lookups require verifying identity.

## DCA-107 | story | parking-lot | Offline capture of notes and photos on tablets
area: platform
sources: 00:35:28, 00:35:45, 00:35:56, 00:36:04, 00:36:22, 00:41:51

As a **caseworker in an area without signal**, I want to take notes and photos offline and have them upload later, so that home visits aren't wasted.

**Parked — needs more discussion:** depends on device-management spike DCA-082. Full-case offline is not requested.

## DCA-108 | - | superseded | System makes the eligibility determination automatically
sources: 00:10:53
superseded_by: DCA-019

Dana's original ask, corrected at 00:26:23 after general counsel advised a person must make the determination.

## DCA-109 | - | superseded | Round-robin automatic case assignment
sources: 00:14:11
superseded_by: DCA-029

Marcus objected (00:14:25); Dana agreed to supervisor assignment with system suggestions (00:14:55).

## DCA-110 | - | superseded | Playback: "the system makes the decision with an override"
sources: 00:40:31
superseded_by: DCA-019

Facilitator's playback had eligibility backwards; Dana corrected it at 00:40:56. Rest of the playback is covered by DCA-112.

## DCA-111 | - | rejected | Replace the timesheet system
sources: 00:37:37, 00:37:46, 00:37:48, 00:37:50, 00:42:03, 00:42:05

Rejected by sponsor ("No.") and IT ("Absolutely not."). Logged in the "heard you" column only.

## DCA-112 | - | merged | Meeting playback, parking-lot recap, and open-question recap
sources: 00:41:01, 00:41:28, 00:41:31, 00:41:35, 00:41:40, 00:41:43, 00:41:46, 00:41:51, 00:42:09, 00:42:26
merged_into: DCA-005, DCA-002, DCA-011, DCA-019, DCA-026, DCA-029, DCA-034, DCA-054, DCA-061, DCA-041, DCA-042, DCA-070, DCA-071, DCA-072, DCA-073, DCA-045, DCA-047, DCA-048, DCA-050, DCA-092, DCA-076, DCA-008, DCA-038, DCA-102, DCA-103, DCA-104, DCA-105, DCA-106, DCA-107, DCA-086, DCA-087, DCA-088, DCA-089, DCA-090, DCA-091

Summaries restate items captured elsewhere. Used as a cross-check (see CHECK sections below).

---

## CHECK | Parking lot recap | 00:41:51
- online applications -> DCA-102
- text message reminders (star) -> DCA-103
- WestPay integration beyond a nightly file -> DCA-104
- Westmarch Power shutoff list -> DCA-105
- chatbot -> DCA-106
- offline mode needs more discussion -> DCA-107

## CHECK | Open questions recap | 00:42:09
- document age limits by program -> DCA-086
- approval threshold 3500 vs 5000 -> DCA-087
- note editing -> DCA-088
- DV restriction whole case vs address -> DCA-089
- family consent before referral -> DCA-090
- Child Care reinstatement window -> DCA-091
- migration scope -> DCA-092

## CHECK | Commitments to send material | 00:42:26
- Marcus: threshold memo -> DCA-094
- Priya: security requirements and integration standards -> DCA-095
- Linda: appeal forms, notice templates, QA checklist -> DCA-096
- Dana: legislative report templates and application numbers -> DCA-097

## CHECK | Next steps | 00:42:51
- appeals and QA session -> DCA-098
- reporting session -> DCA-099
- caseworker observation -> DCA-100
- notes by Thursday -> DCA-101

## no-requirement
00:00:04, 00:00:11, 00:00:14, 00:00:19, 00:00:29, 00:00:57, 00:01:19, 00:01:27, 00:01:41, 00:01:45, 00:01:50, 00:02:28, 00:03:39, 00:03:41, 00:03:47, 00:04:10, 00:06:28, 00:07:31, 00:10:48, 00:12:25, 00:13:34, 00:14:04, 00:16:30, 00:18:03, 00:31:08, 00:32:49, 00:37:29, 00:43:17, 00:43:44, 00:43:49, 00:43:51, 00:44:02, 00:44:04, 00:44:06, 00:44:08, 00:44:54
