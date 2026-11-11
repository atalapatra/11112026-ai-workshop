# Meeting Transcript

**Meeting:** DCA Case Management Modernization – Requirements Kickoff
**Date:** Tuesday, November 3, 2026
**Time:** 10:00 AM – 10:46 AM Eastern
**Platform:** Microsoft Teams
**Recording and transcription:** Automatically generated. Transcript may contain errors.

**Attendees**

- Dana Whitfield – Deputy Director, Program Operations, Westmarch Department of Community Assistance (DCA)
- Marcus Oyelaran – Casework Supervisor, Eastside Regional Office, DCA
- Priya Raman – IT Manager, Infrastructure and Security, DCA
- Linda Castellanos – Manager, Appeals and Quality Assurance, DCA (joined late)
- Jordan Ellis – Engagement Lead, Northgate Digital
- Sam Patel – Business Analyst, Northgate Digital

---

**[00:00:04] Jordan Ellis:** Okay, I think we've got most people. Let me just, um, can everyone hear me alright?

**[00:00:11] Dana Whitfield:** Yep, we can hear you.

**[00:00:14] Jordan Ellis:** Great. Marcus, I see you're on. Are you joining from the regional office?

**[00:00:19] Marcus Oyelaran:** Yeah, I'm at Eastside. Sorry in advance, somebody's running the shredder in the next room, so if you hear a, like, grinding noise, that's what that is.

**[00:00:29] Jordan Ellis:** No worries at all. So, thanks everyone for making time. This is our first requirements session for the new case management system. The goal today is really for us to listen. We want to hear what's not working, what you need, what keeps you up at night. Sam is going to be taking notes and might jump in with clarifying questions. We've got about forty-five minutes. Could we just do quick intros? I'll start. I'm Jordan Ellis, I'm the engagement lead from Northgate. Sam?

**[00:00:57] Sam Patel:** Hi everyone, Sam Patel, I'm the business analyst on the Northgate side. I'll be the one sending you a lot of follow-up questions, so, apologies in advance.

**[00:01:07] Dana Whitfield:** Dana Whitfield, Deputy Director of Program Operations. I oversee the three assistance programs, so Emergency Housing Assistance, the Utility Relief Program, and Child Care Support. I'm, I guess, the sponsor for this whole thing.

**[00:01:19] Priya Raman:** Priya Raman, IT manager. I cover infrastructure and security, so I'll probably be the person saying no a lot today. [laughter]

**[00:01:27] Marcus Oyelaran:** Marcus Oyelaran, I supervise the casework team at Eastside. I've got eleven caseworkers, well, ten right now, we've got an open position. I've been with DCA about fourteen years, so I've used CAMS basically my whole career.

**[00:01:41] Jordan Ellis:** Great. And I think Linda is joining a little late?

**[00:01:45] Dana Whitfield:** Yeah, she's coming from another meeting, she'll hop on.

**[00:01:50] Jordan Ellis:** Perfect. Dana, do you want to kick us off with the big picture? Why now, what does success look like?

**[00:01:57] Dana Whitfield:** Sure. So, um, the short version is CAMS is from 2004. It was built for one program, Housing, and then we kind of bolted the other two on over the years. And it shows. Caseworkers keep side spreadsheets, there's still a lot of paper, and the biggest thing for me is we cannot see a household across programs. Somebody can be getting utility help and child care help and be about to get evicted, and three different people at DCA are working with that family and none of them know it.

**[00:02:28] Jordan Ellis:** Mm-hmm.

**[00:02:29] Dana Whitfield:** And then the other piece is timeliness. We have a thirty-day processing standard. Thirty days from when we receive an application to when we make a determination. And we are missing it. We had an audit finding last year, um, we were at something like seventy-one percent on time for Housing. So that's, that's a problem with the legislature, and honestly it's a problem for families, because thirty days is a long time when you have an eviction notice.

**[00:02:56] Jordan Ellis:** So if I'm hearing you, success is one system for all three programs, one view of the household, and getting timeliness up.

**[00:03:04] Dana Whitfield:** Yes. One system, one view of the family, and we hit our deadlines. And I want it to be modern. Like, easy to use. People shouldn't need a two-week training to figure it out.

**[00:03:16] Sam Patel:** Can I ask a quick one? When you say "one view of the household," what would you want to see on that screen?

**[00:03:25] Dana Whitfield:** Everybody in the household, which programs they've applied for or are getting, what the status is on each one, who the caseworker is, and the documents. Ideally we don't ask the family for the same pay stub three times.

**[00:03:39] Sam Patel:** Got it, thanks.

**[00:03:41] Linda Castellanos:** Hi, sorry, sorry, this is Linda, I was in another meeting that ran over.

**[00:03:47] Jordan Ellis:** Hi Linda, no problem, we just did intros. Do you want to introduce yourself quickly?

**[00:03:53] Linda Castellanos:** Sure. Linda Castellanos, I manage Appeals and Quality Assurance. So when someone's denied and they appeal, that comes to my team, and we also do the case reviews, the QA sampling. So I care a lot about, you know, what's documented and whether we can prove what we did.

**[00:04:10] Jordan Ellis:** Great. Marcus, can I come to you? Walk us through what a day looks like for one of your caseworkers. Where does it hurt?

**[00:04:19] Marcus Oyelaran:** Oh, boy. Okay. So, somebody walks in, or calls, or we get a paper application in the mail, or one of the community partners faxes something over, yes, we still get faxes. First thing the caseworker does is search CAMS to see if the person's already in there. And the search is terrible. If the name is spelled differently, or somebody has a hyphenated last name and it was entered without the hyphen, you don't find them. So we end up with duplicates. I've seen the same person in there four times.

**[00:04:50] Sam Patel:** What do they search on today?

**[00:04:53] Marcus Oyelaran:** Name and date of birth, mostly. You can search by Social but people don't always want to give it at the front desk, and honestly the field is, it's not, you have to type it exactly with the dashes or it doesn't work.

**[00:05:08] Sam Patel:** Okay.

**[00:05:10] Marcus Oyelaran:** So what I'd want is, when you start a new application, the system looks for possible matches. Name, date of birth, last four of the Social, address maybe. And it shows you, hey, these might be the same person. But, and this is important, I don't want it to just merge them automatically. I've seen systems do that and then you've got a father and son with the same name merged together and it's a nightmare. Show me, and let the caseworker decide.

**[00:05:38] Dana Whitfield:** Agreed.

**[00:05:40] Marcus Oyelaran:** And then if it is the same household, I want the new application to attach to that household. Not start over.

**[00:05:48] Priya Raman:** Can I ask something on that? Does anybody actually know how bad the duplicate problem is? Like, is it a few hundred records, or is it thousands?

**[00:05:58] Marcus Oyelaran:** Nobody's ever counted. It's bad. That's all I know.

**[00:06:02] Priya Raman:** Because how you match people depends a lot on what the data looks like. If half the records don't have a Social on them, matching on the last four isn't going to get you very far. I'd want somebody to take a copy of the CAMS data and actually look at it before we decide how the matching should work.

**[00:06:22] Sam Patel:** That's fair. Good to know that before we commit to an approach.

**[00:06:28] Jordan Ellis:** That makes sense. And then after the search, what happens?

**[00:06:32] Marcus Oyelaran:** Then they do the intake. Household members, income, address, what program. And then documents. That's the other big one.

**[00:06:40] Dana Whitfield:** Can I jump in before documents? Because, um, the other thing I really want is for people to be able to apply online. Like, residents. Fill it out on their phone, upload their stuff. That would cut down on so much of the front desk work.

**[00:06:56] Priya Raman:** So, I want to flag that. That's a public-facing portal. That's a completely different security posture, identity proofing for the public, all of that. I thought we'd agreed phase one was staff-facing only.

**[00:07:08] Dana Whitfield:** We did, we did. I just, I don't want us to build something that makes it impossible later.

**[00:07:15] Priya Raman:** That's fair. Can we say that? Staff-facing for phase one, but designed so a portal can plug in later?

**[00:07:22] Dana Whitfield:** Yes. Okay. Let's say that.

**[00:07:25] Sam Patel:** I'll note that as a parking lot item, online applications, future phase.

**[00:07:31] Jordan Ellis:** Thanks. Marcus, documents.

**[00:07:33] Marcus Oyelaran:** Right. So each program needs different documents. For Housing, it's ID, the lease, the eviction notice or the past-due notice from the landlord, and proof of income for everybody in the household over eighteen. For Utility Relief, it's ID, income, and the utility bill, and if they're asking for the emergency piece, the shutoff notice. Child Care, it's income, proof of work or school for the parent, and birth certificates or something for the kids.

**[00:07:58] Sam Patel:** And today, how do caseworkers know what's missing?

**[00:08:02] Marcus Oyelaran:** Paper checklist. Literally. We print a checklist and staple it to the folder. What I'd love is the system knows what each program needs and shows a checklist, and you check things off as they come in. And when you check it off, it records who verified it and when. Because right now we have, um, Linda will tell you, in QA we can't always tell who looked at the pay stub.

**[00:08:26] Linda Castellanos:** That's right. That's one of our most common findings. "Income verified," with no indication of who verified it or what they looked at.

**[00:08:35] Marcus Oyelaran:** And then the documents themselves need to be in the system. Scanned at the front desk, or if somebody emails them, we need to upload them, and if a caseworker's out on a home visit, they should be able to take a picture with the tablet.

**[00:08:51] Dana Whitfield:** And reuse. That's the big one for me. If the family gave us a pay stub for Utility, and two weeks later they apply for Housing, we should not be asking again.

**[00:09:03] Marcus Oyelaran:** As long as it's not too old. Pay stubs are only good for thirty days.

**[00:09:09] Dana Whitfield:** I thought it was sixty.

**[00:09:12] Marcus Oyelaran:** For Child Care it might be sixty. For Housing we've always done thirty.

**[00:09:18] Dana Whitfield:** Hmm. Okay, I need to check that with the policy team. I don't want to say the wrong thing.

**[00:09:25] Sam Patel:** I'll put that down as an open question. Document age limits by program and by document type.

**[00:09:32] Priya Raman:** And just so we're thinking about it, if we're storing IDs and Social Security cards and pay stubs, that's a lot of sensitive data. Those documents need to be encrypted, access-controlled, the usual. I'll send over our standards.

**[00:09:45] Jordan Ellis:** Thank you. What happens when a document is missing?

**[00:09:50] Marcus Oyelaran:** We send a letter. A request for information. The family has ten days to get it to us.

**[00:09:57] Linda Castellanos:** And to be precise on the policy, the thirty-day clock does not stop while we're waiting. That trips people up. If the documents aren't in by day ten, the application can be denied for missing information.

**[00:10:10] Marcus Oyelaran:** "Can be." In practice we give extensions a lot. People are dealing with a lot. Somebody's in the hospital, somebody's landlord won't give them a copy of the lease.

**[00:10:20] Linda Castellanos:** Which is fine, but the extension has to be documented with a reason. Because if they end up appealing, I need to see that.

**[00:10:29] Marcus Oyelaran:** Sure.

**[00:10:31] Sam Patel:** So the system generates the request letter listing what's missing, tracks the ten-day due date, and allows an extension with a required reason. Is that right?

**[00:10:41] Marcus Oyelaran:** Yeah. And, oh, and remind the caseworker when the ten days is up. Because they forget. We all forget.

**[00:10:48] Jordan Ellis:** That's helpful. Let's talk eligibility. How is a determination made today?

**[00:10:53] Dana Whitfield:** So, this is something I'm really excited about. I want the system to calculate eligibility automatically. Each program has income limits based on household size, a percentage of area median income, and then some other rules. The system should just do that math. Caseworkers spend way too much time with calculators.

**[00:11:11] Marcus Oyelaran:** We do need to be able to override, though.

**[00:11:15] Dana Whitfield:** Sure.

**[00:11:17] Marcus Oyelaran:** Because there are always situations. Somebody's income just dropped, they lost their job last week, the pay stubs say one thing but the reality is different. There's policy for that, but it's judgment.

**[00:11:29] Linda Castellanos:** Every override needs a reason. And I want to be able to pull a list of overrides for QA. That's one of the things we'd sample.

**[00:11:39] Sam Patel:** Is income the only factor, or are there others?

**[00:11:43] Dana Whitfield:** For Housing it's income, residency in the state, and the housing crisis itself, so the eviction notice or the past-due. Utility is income and the bill. Child Care is income, the work or school requirement, and the child's age, under thirteen, or under eighteen if the child has a disability.

**[00:12:00] Priya Raman:** And these rules change, right? Like, the income limits get updated every year?

**[00:12:06] Dana Whitfield:** Every year, yes, when the new median income numbers come out. And the legislature tinkers with things.

**[00:12:13] Priya Raman:** Then I'd really ask that thresholds and limits be configurable by somebody on the business side. I don't want to be opening a change request with a vendor every April because a number changed.

**[00:12:25] Jordan Ellis:** Noted. That's a good one.

**[00:12:28] Priya Raman:** And related to that, the new income limits for next year come out in the spring. Whatever we build, somebody has to load those tables before we go live, and this year's too. In CAMS that's me running a script every April, and I would really like it to not be me anymore.

**[00:12:46] Dana Whitfield:** [laughs] Noted, Priya.

**[00:12:48] Marcus Oyelaran:** Can I also mention approvals? Because that's tied to this.

**[00:12:53] Jordan Ellis:** Please.

**[00:12:55] Marcus Oyelaran:** For Housing, if the payment is over a certain amount it needs supervisor approval before it goes out. So the caseworker does the determination, and it comes to me, and I approve it.

**[00:13:07] Sam Patel:** What's the amount?

**[00:13:09] Marcus Oyelaran:** It's thirty-five hundred now. They lowered it in July.

**[00:13:14] Dana Whitfield:** Did they? I think it's still five thousand.

**[00:13:18] Marcus Oyelaran:** We got a memo. I can find it.

**[00:13:22] Dana Whitfield:** Okay, send it to me, because if it changed and I didn't know about it, that's a whole other conversation. [laughter]

**[00:13:30] Priya Raman:** Which is exactly why it should be configurable.

**[00:13:34] Dana Whitfield:** Fair.

**[00:13:36] Sam Patel:** And do denials need supervisor approval, or only approvals over the threshold?

**[00:13:41] Marcus Oyelaran:** Just the big approvals today. Although, honestly, I'd like to see denials for, um, for new caseworkers. Like their first ninety days. Everything they deny, I want to look at.

**[00:13:52] Linda Castellanos:** I would love that. Most of our reversals on appeal are from newer staff.

**[00:13:58] Sam Patel:** Okay, so supervisor review of denials for caseworkers within their first ninety days. Got it.

**[00:14:04] Jordan Ellis:** Let's talk about how work gets assigned. Marcus, how does a new application get to a caseworker?

**[00:14:11] Dana Whitfield:** Can I take this one? Because I have an opinion. [laughter] I think it should be automatic. Round-robin. Application comes in, it goes to the next caseworker. It's fair, it's fast, nobody's sitting there in the morning assigning cases.

**[00:14:25] Marcus Oyelaran:** Respectfully, no. That doesn't work.

**[00:14:28] Dana Whitfield:** Okay. Tell me why.

**[00:14:30] Marcus Oyelaran:** Because not every case is the same. If I've got a caseworker who already has this family on Utility, I want the Housing case to go to them too. They know the family. If the family speaks Spanish, I want it to go to one of my three Spanish speakers. I've got one person who speaks Vietnamese. And some caseworkers are carrying really heavy cases right now and some aren't, and round-robin doesn't know that.

**[00:14:55] Dana Whitfield:** Okay. That's fair. So, supervisors assign, but can the system suggest who it should go to? Based on those things?

**[00:15:03] Marcus Oyelaran:** That I'd love. Suggest, and I click to accept or pick somebody else.

**[00:15:09] Sam Patel:** So the factors for suggesting are: existing caseworker for the household, language, current caseload. Anything else?

**[00:15:15] Marcus Oyelaran:** Region. Applications should go to the regional office for where they live. Unless it's, like, a statewide thing, but that's rare.

**[00:15:24] Marcus Oyelaran:** Oh, and when somebody's out. If a caseworker is out sick for two weeks or goes on leave, I need to move their whole caseload. Today I do that one case at a time in CAMS and it takes, it takes an afternoon.

**[00:15:39] Sam Patel:** Bulk reassignment. Got it.

**[00:15:41] Jordan Ellis:** And how do you, as a supervisor, see how your team is doing?

**[00:15:47] Marcus Oyelaran:** Whiteboard. [laughter] I'm not kidding. I have a whiteboard and a spreadsheet. What I want is a screen that shows me each caseworker, how many open cases, and which ones are getting close to the deadline.

**[00:16:00] Dana Whitfield:** And I want the same thing, rolled up. By region. In real time. Like a dashboard I can look at in the morning.

**[00:16:08] Sam Patel:** When you say real time, would it be okay if it updated, say, every fifteen minutes? Or does it need to be up-to-the-second?

**[00:16:17] Dana Whitfield:** Oh, I mean, I don't know. I just don't want to be looking at last week's numbers.

**[00:16:24] Sam Patel:** Okay, so current as of today, at minimum. I'll follow up on that.

**[00:16:30] Jordan Ellis:** Let's go into deadlines specifically, since that came up in the audit. What would help?

**[00:16:36] Linda Castellanos:** Can I start? So, the thirty-day standard applies to all three programs. But for Housing, if the eviction is scheduled within seven days, it's an expedited case, and we have three business days.

**[00:16:48] Sam Patel:** Three business days from receipt?

**[00:16:51] Linda Castellanos:** From receipt of the application. And that's where we miss the most, honestly, because nobody flags it as expedited at intake.

**[00:16:59] Marcus Oyelaran:** It's on the paper form, there's a checkbox, but if the person doesn't check it or the caseworker misses it…

**[00:17:07] Dana Whitfield:** So the system should figure it out. If they enter the eviction date and it's within seven days, it's expedited. Automatically.

**[00:17:15] Marcus Oyelaran:** Yes, and it should go to the top of the list. And make noise.

**[00:17:21] Jordan Ellis:** What does "make noise" look like?

**[00:17:24] Marcus Oyelaran:** I don't know. Red. Notification. Something. [laughter] For regular cases, I'd say, at day twenty, give the caseworker a heads up. At day twenty-five, tell the caseworker and me.

**[00:17:35] Dana Whitfield:** And if a whole region is falling behind, I want to know. Like, if more than, I don't know, ten percent of a region's cases are past day twenty-five. Send me something.

**[00:17:46] Sam Patel:** Would a weekly email work for that, or do you want it as it happens?

**[00:17:53] Dana Whitfield:** Weekly is fine. Monday morning. Actually, no, as it happens. No. Weekly. Let's say weekly, I'll be in the dashboard anyway.

**[00:18:01] Sam Patel:** Weekly. Okay. [laughs]

**[00:18:03] Jordan Ellis:** Let's talk about case notes and documentation. Linda, I imagine you have thoughts.

**[00:18:09] Linda Castellanos:** I do. So, case notes are, for appeals, they're evidence. When a hearing officer reviews a case, the notes are a big part of what they look at. So the number one thing for me is, once a note is saved, it cannot be edited. If you need to correct it, you add an addendum. The original stays.

**[00:18:28] Marcus Oyelaran:** Oh, come on, Linda. If I make a typo, I have to add an addendum that says "I meant 'tenant,' not 'tenet'"?

**[00:18:37] Linda Castellanos:** Yes. [laughter]

**[00:18:39] Marcus Oyelaran:** Can we at least have, like, an hour? Or the same day? You can fix your own note on the same day.

**[00:18:47] Linda Castellanos:** I'd have to talk to legal. My instinct is no. Because the whole point is, what did we know, and when.

**[00:18:56] Dana Whitfield:** Let's park that one. We'll figure it out.

**[00:19:00] Sam Patel:** I'll log it as an open decision. Note editing window versus addendum only.

**[00:19:05] Marcus Oyelaran:** And the notes should be searchable. Right now in CAMS, the notes are just one long block of text. If I'm trying to find when we talked to the landlord, I'm scrolling forever.

**[00:19:17] Marcus Oyelaran:** And it'd be good to tag the note. Like, phone call, home visit, office visit, landlord contact.

**[00:19:24] Sam Patel:** Contact type on each note. Got it.

**[00:19:28] Jordan Ellis:** Priya, this might be a good moment to talk about the audit trail side.

**[00:19:34] Priya Raman:** Yeah. So, from a security standpoint, we need a full audit log. Who viewed a record, who changed what, when, from where. And it needs to be retained for, I think we said seven years?

**[00:19:46] Linda Castellanos:** Seven years after the case closes. That's our records retention schedule.

**[00:19:51] Priya Raman:** Right. And the audit log itself can't be editable by anyone, including admins.

**[00:19:57] Linda Castellanos:** And there's another piece related to that. Restricted cases. So if a DCA employee applies for benefits, or a relative of an employee, that case needs to be restricted. Only certain people can see it. Same with domestic violence situations, where the address has to be confidential. We had an incident, I won't go into it, but someone looked up a case they shouldn't have.

**[00:20:19] Dana Whitfield:** That was a bad week.

**[00:20:22] Linda Castellanos:** So restricted cases, limited access, and every single view gets logged and I want a report of who looked at them.

**[00:20:30] Sam Patel:** For the domestic violence cases, is it the whole case that's restricted, or specifically the address?

**[00:20:36] Linda Castellanos:** Hmm. Good question. I think, the address for sure. Caseworkers need to work the case, but the address shouldn't show up on, like, a list screen, or a report, or an export. I'd have to check whether the whole case should be locked down.

**[00:20:52] Sam Patel:** Okay. Open question.

**[00:20:54] Jordan Ellis:** Let's talk about the notices that go out to families. Dana?

**[00:20:59] Dana Whitfield:** So every determination, approval or denial, we send a notice. Today they're Word templates and the caseworker fills them in, and they're inconsistent, and sometimes the appeal rights paragraph gets deleted, which is a big deal.

**[00:21:12] Linda Castellanos:** It's a huge deal. If the notice doesn't include appeal rights, the appeal window doesn't start. So technically they could appeal a year later.

**[00:21:21] Dana Whitfield:** So the system should generate the notice. Templates by program, by outcome. The denial reasons come from a list, a standard list of reason codes, and the caseworker can add an explanation. And the appeal rights language is always there and they can't remove it.

**[00:21:37] Linda Castellanos:** On the reason codes, we do have a list. It's about sixty codes in a spreadsheet, and some of them say basically the same thing in different words. That list would need to be cleaned up and loaded before anyone could use it.

**[00:21:52] Marcus Oyelaran:** And Spanish. A lot of our families need Spanish notices. And sometimes Vietnamese, and we've had Haitian Creole, Somali.

**[00:21:59] Dana Whitfield:** English and Spanish for sure. For others, I think today we get them translated on request.

**[00:22:06] Dana Whitfield:** And honestly, the templates themselves are a mess. We have something like forty Word templates across the three programs, and some of them haven't been touched since 2015. Somebody needs to go through all of them, consolidate them, and get the new versions translated into Spanish.

**[00:22:22] Marcus Oyelaran:** Some of them still have the old Eastside address on them. We moved in 2020.

**[00:22:28] Sam Patel:** How do notices get to the family? Mail?

**[00:22:32] Dana Whitfield:** Mail, mostly. We print centrally. Email if the person agrees to it.

**[00:22:37] Dana Whitfield:** Oh, and text messages! I'd love reminders by text. Like, "Your documents are due Friday." Families respond to texts. They don't respond to letters.

**[00:22:46] Priya Raman:** So, text messaging means a messaging vendor, it means storing consent, it means opt-out handling. It's doable but it's not small. And I don't even know whether the state has a contract for a texting service. Somebody would have to find out what our options are. Can we park that?

**[00:23:03] Dana Whitfield:** Park it. But I want it. Put a star next to it. [laughter]

**[00:23:09] Sam Patel:** Parking lot, with a star.

**[00:23:12] Jordan Ellis:** Linda, let's go into appeals since you're here. Can you walk us through it?

**[00:23:18] Linda Castellanos:** Sure. So once a family gets a denial notice, or a notice reducing their benefit, they have thirty days from the date on the notice to request an appeal. They can do that by phone, by mail, in person. Today, whoever takes that call writes it on a piece of paper and walks it over to my team. Sometimes it gets lost.

**[00:23:39] Linda Castellanos:** So, we need to log the appeal request on the case. Date received, how it came in. The system should check whether it's within the thirty days. And then it gets assigned to a hearing officer, and this is important, the hearing officer cannot be anyone who worked on the original case.

**[00:23:57] Sam Patel:** Should the system prevent that, or warn?

**[00:24:01] Linda Castellanos:** Prevent. Absolutely prevent.

**[00:24:03] Linda Castellanos:** Then we schedule a hearing, and the family has to get a notice of the hearing at least ten days before it. Then the hearing happens, and the outcome is upheld, reversed, or remanded, which means we send it back to be redone.

**[00:24:18] Sam Patel:** And if it's reversed or remanded, what happens to the case?

**[00:24:23] Linda Castellanos:** It goes back to the regional office.

**[00:24:27] Marcus Oyelaran:** It should go to a different caseworker, though. Not the one who denied it.

**[00:24:33] Linda Castellanos:** It goes back to the supervisor, and the supervisor reassigns it. Usually to someone else, but that's the supervisor's call.

**[00:24:40] Marcus Oyelaran:** Okay, that works.

**[00:24:43] Linda Castellanos:** Oh, and there's one more complicated piece for Child Care. If a family is already receiving Child Care Support and we reduce or end it, and they appeal within ten days of the notice, their benefits continue at the current level until the hearing decision. That's federal. So the system has to know that.

**[00:25:01] Sam Patel:** Continued benefits pending appeal. Only for Child Care?

**[00:25:05] Linda Castellanos:** Only for Child Care. The other two are one-time payments mostly, so it doesn't apply the same way.

**[00:25:13] Jordan Ellis:** This is great detail, thank you. Can I go back to something Dana said at the beginning? The household view. Marcus, when a caseworker is working one program, what do they need to see about the others?

**[00:25:26] Marcus Oyelaran:** Honestly, just knowing it exists is half of it. "This family has an open Utility case, caseworker is Teresa." Then I can call Teresa.

**[00:25:35] Marcus Oyelaran:** And referrals. If I'm doing a Utility case and I can see the family is behind on rent, I want to be able to refer them to Housing. Click a button, it creates the Housing application, and it carries over the household and the income and the documents we already have. Instead of starting over.

**[00:25:54] Dana Whitfield:** Yes. That's exactly the picture.

**[00:25:57] Sam Patel:** And should the family have to agree to the referral before it's created?

**[00:26:02] Marcus Oyelaran:** Oh. Um. Yeah, probably. You'd ask them on the phone. Dana?

**[00:26:07] Dana Whitfield:** I think so. I'd want policy to weigh in.

**[00:26:12] Sam Patel:** Open question. Got it.

**[00:26:14] Dana Whitfield:** Can I go back to eligibility for a second? Because I need to correct something I said.

**[00:26:21] Jordan Ellis:** Of course.

**[00:26:23] Dana Whitfield:** I said the system should calculate eligibility automatically. I talked to our general counsel last week, and I'd forgotten this until Linda was talking about appeals. She was pretty clear that we don't want the system making the determination. Legally, the caseworker makes the determination. The system can show a recommendation, it can do the math, but a person decides, and the record has to show that a person decided.

**[00:26:47] Linda Castellanos:** That's consistent with what we'd defend at a hearing.

**[00:26:51] Sam Patel:** So, to make sure I have it: the system calculates and displays a recommended outcome, the caseworker records the actual determination, and if the caseworker's determination differs from the recommendation, that's where a reason is required.

**[00:27:04] Dana Whitfield:** Yes. That's better than what I said before. Use that.

**[00:27:09] Marcus Oyelaran:** That actually works better for us anyway.

**[00:27:12] Jordan Ellis:** Okay. Let's talk payments. Once something is approved, how does money go out?

**[00:27:18] Dana Whitfield:** So for Housing, we pay the landlord directly. For Utility, we pay the utility company. For Child Care, we pay the provider. And all of that goes through WestPay, which is the state's financial system. I assumed the new system would just send payments to WestPay.

**[00:27:34] Priya Raman:** So, WestPay integration is, um, I want to be careful here. WestPay is run by the Department of Finance, not us. They have a whole intake process for new integrations and it's, it's six to nine months. Realistically. For phase one, I think we're looking at the system generating a payment file every night, and the finance team uploads it, same as they do today from CAMS.

**[00:27:56] Dana Whitfield:** Today it's a file?

**[00:27:59] Priya Raman:** Today it's a file.

**[00:28:02] Dana Whitfield:** I did not know that. [laughter] Okay. A file for phase one. A real integration later.

**[00:28:09] Priya Raman:** Although, to be honest, I don't know exactly what format finance needs that file in. The CAMS file was set up before my time, and I'm not sure the layout is written down anywhere. Somebody would have to dig into that and sit down with finance before we say the nightly file is the easy part.

**[00:28:28] Jordan Ellis:** Understood. We won't assume anything there yet.

**[00:28:31] Marcus Oyelaran:** And can we talk about landlords? Because that's a mess. To pay a landlord, they have to be set up as a vendor. W-9, the address, the bank info. And today we've got the same landlord in there under five different names. "Smith Properties," "Smith Property Management LLC," "John Smith." So the payments go out and nobody can tell it's the same landlord.

**[00:28:53] Sam Patel:** So you'd want a landlord and vendor registry with duplicate checking, similar to the person matching?

**[00:28:59] Marcus Oyelaran:** Yes. Exactly like that.

**[00:29:02] Priya Raman:** And bank account info is, again, very sensitive. Limited access. Most caseworkers shouldn't see full account numbers.

**[00:29:09] Dana Whitfield:** Oh, and the power company. Westmarch Power sends us a list every week of customers with shutoff notices, and we reach out. It'd be great if that came in automatically and created, like, an outreach list.

**[00:29:22] Priya Raman:** That's another integration with an outside party. Can we park that one too?

**[00:29:27] Dana Whitfield:** Fine. Park it. No star.

**[00:29:30] Sam Patel:** [laughs] Parking lot, no star.

**[00:29:33] Jordan Ellis:** We've got about twenty minutes left. Let's make sure we cover reporting. Dana, what do you have to report and to whom?

**[00:29:42] Dana Whitfield:** So, monthly, we report to the legislature, and for Utility Relief, because it's partly federally funded, we report to the federal government quarterly. It's counts. Applications received, approved, denied, by program, by county. Timeliness, so percent processed within thirty days and within three days for expedited. Average benefit amount. Denial reasons. Today, someone on my team spends, I'm not exaggerating, four days a month pulling that together from CAMS and spreadsheets.

**[00:30:06] Sam Patel:** Do you have the current report templates you could share?

**[00:30:10] Dana Whitfield:** I can send those, yes.

**[00:30:13] Marcus Oyelaran:** And for us, I just want to be able to export stuff to Excel. Everything. My caseload, my team's numbers, whatever I'm looking at, export button.

**[00:30:23] Priya Raman:** [sighs] I knew this was coming.

**[00:30:26] Marcus Oyelaran:** [laughs] Come on, Priya.

**[00:30:29] Priya Raman:** I get it, I do. But every export is personal information walking out the door onto somebody's laptop. If we do exports, they need to leave out Social Security numbers, they need to respect the restricted-case rules Linda talked about, and they need to be logged. Who exported what, when.

**[00:30:46] Linda Castellanos:** Agreed.

**[00:30:48] Marcus Oyelaran:** That's fine. I don't need Socials. I need names and dates and statuses.

**[00:30:54] Sam Patel:** Do you know which specific exports your team uses most today?

**[00:30:59] Marcus Oyelaran:** Honestly, mostly the open cases with the days remaining. That's the whiteboard. And at the end of the month, how many each caseworker closed.

**[00:31:08] Sam Patel:** Helpful, thank you.

**[00:31:10] Jordan Ellis:** Linda, anything for reporting from the QA side?

**[00:31:14] Linda Castellanos:** Yes. For QA, every month we pull a random sample of closed cases for review. Today it's, someone literally picks file numbers. I'd want the system to pull a random sample, by program, a set number, I think it's twenty-five per program per month, and assign them to my reviewers. And then the reviewers fill out a review checklist in the system, and the results roll up.

**[00:31:37] Sam Patel:** Is the checklist the same for every program?

**[00:31:41] Linda Castellanos:** Mostly. There are some program-specific questions. I can send the current forms.

**[00:31:46] Sam Patel:** That would be great.

**[00:31:49] Marcus Oyelaran:** Can I bring up something that's not on the list? Child Care has recertification.

**[00:31:55] Dana Whitfield:** Oh, yes. Good.

**[00:31:57] Marcus Oyelaran:** So Child Care isn't one-time. Families are approved for six months and then they have to recertify. Today we track that in, yes, a spreadsheet. The system should flag the case, I'd say, forty-five days before the end date, and send the family a renewal packet. And if they don't respond, it should follow up, and if they still don't respond by the end date, the case closes, with a notice, of course.

**[00:32:22] Linda Castellanos:** With appeal rights.

**[00:32:24] Marcus Oyelaran:** With appeal rights. [laughter]

**[00:32:27] Sam Patel:** When a case closes for non-response, is there a grace period if the family comes back a week later?

**[00:32:35] Marcus Oyelaran:** Hmm. I think there's a thirty-day window where they can reinstate without a full new application. Dana?

**[00:32:41] Dana Whitfield:** I believe that's right, but put it on the list for policy.

**[00:32:47] Sam Patel:** Will do.

**[00:32:49] Jordan Ellis:** Priya, I want to make sure we give you time on the technical requirements. What do we need to know?

**[00:32:57] Priya Raman:** Sure. A few things. One, single sign-on with our state directory. We're on Microsoft Intra I.D. Everyone signs in with their state account, multi-factor authentication required. No separate usernames and passwords.

**[00:33:08] Priya Raman:** And on that, my team will need to register the application in Intra and set up security groups for each of the roles I'm about to list. That has to happen before your developers can even sign in to a test environment, so it needs to be early.

**[00:33:24] Priya Raman:** Two, role-based access. Caseworker, supervisor, hearing officer, QA reviewer, program admin, IT admin, and probably a read-only role for, like, auditors. And roles need to be manageable by us, not by the vendor.

**[00:33:36] Priya Raman:** Three, hosting has to be in our state cloud environment. FedRAMP Moderate baseline at minimum because of the federal Utility money. I'll send the security requirements document, it's about forty pages, sorry.

**[00:33:48] Sam Patel:** [laughs] We'll read it.

**[00:33:51] Priya Raman:** We'll also need the environments set up in that cloud account. Development, test, and training, at least. Some of that is my team and some of it is yours, so we'll need to work out who does what.

**[00:34:04] Priya Raman:** Four, accessibility. Section 508. That's not optional.

**[00:34:08] Marcus Oyelaran:** And it matters, I have a caseworker who uses a screen reader. CAMS is basically unusable for her. She's amazing, and she has to have a coworker help her with some screens. That shouldn't happen.

**[00:34:20] Priya Raman:** Right. And then five, data migration from CAMS.

**[00:34:24] Dana Whitfield:** Can we just bring over the open cases? Start fresh?

**[00:34:29] Linda Castellanos:** No, we need history. If someone appeals a case from last year, we need it. And with the seven-year retention, we have to keep it somewhere.

**[00:34:39] Priya Raman:** We could keep CAMS running read-only for historical lookups, but honestly I'd love to turn CAMS off. It's on a server that's out of support.

**[00:34:48] Priya Raman:** And part of the problem is that nobody really knows what's in the CAMS database. There are tables in there that nobody at DCA can explain. The person who built most of it retired in 2017. Before anybody decides how much to migrate, someone needs to go in and map out what's actually there.

**[00:35:07] Dana Whitfield:** Okay. I don't know the answer. Let's flag it.

**[00:35:11] Sam Patel:** Open question on migration scope. Open cases only, versus seven years of closed cases, versus keeping CAMS as a read-only archive.

**[00:35:19] Marcus Oyelaran:** And whatever we bring over, the duplicates need to get cleaned up. Otherwise we're just moving the mess.

**[00:35:26] Priya Raman:** Good point.

**[00:35:28] Marcus Oyelaran:** Oh, and tablets. My caseworkers do home visits, especially out in the rural counties. They need to be able to use it on a tablet. And out there, half the time, there's no signal. So it needs to work offline and then sync when they get back.

**[00:35:45] Priya Raman:** Offline is a really big ask. Like, caching sensitive data on a device that could be left in a car. I'm not saying no, but I'm, I'm not saying yes.

**[00:35:56] Marcus Oyelaran:** What if it's just, like, I can take notes and pictures offline, and it uploads later? I don't need the whole case offline.

**[00:36:04] Priya Raman:** That's more reasonable. I'd want to look at what our device management can actually do first, though. Can we wipe a tablet remotely, can the app keep anything it stores encrypted, what happens if a tablet doesn't connect for a week. I'd want answers to those before it turns into a requirement.

**[00:36:22] Sam Patel:** I'll capture that as: tablet-friendly for field visits, with a question on limited offline capture of notes and photos.

**[00:36:30] Jordan Ellis:** And performance, any expectations?

**[00:36:32] Marcus Oyelaran:** Fast. [laughter] I'm serious. CAMS takes like forty seconds to open a case sometimes. When you've got someone sitting across from you, forty seconds is forever.

**[00:36:42] Sam Patel:** Would a few seconds to open a case feel acceptable?

**[00:36:47] Marcus Oyelaran:** A few seconds would feel like a miracle.

**[00:36:51] Priya Raman:** And it needs to handle, what, we've got about a hundred and eighty staff who'd be in it, maybe a hundred and twenty at the same time on a busy day.

**[00:37:02] Dana Whitfield:** More during winter. Utility season. Applications go up like three times in January.

**[00:37:08] Priya Raman:** And for the record, we've never load tested CAMS. Ever. Before go-live, I'd want proof that the new system handles a Monday morning in January, not just a quiet Tuesday in July.

**[00:37:19] Sam Patel:** Good to know. Any idea of annual application volume?

**[00:37:23] Dana Whitfield:** Across the three programs, I think around forty thousand applications last year. I'll confirm.

**[00:37:29] Jordan Ellis:** Great. Okay, I want to leave room for anything we haven't covered. What else is on people's minds?

**[00:37:37] Marcus Oyelaran:** Okay, this is half a joke. While we're replacing things, can it also do our timesheets? Because the timesheet system is, somehow, worse than CAMS.

**[00:37:46] Dana Whitfield:** [laughs] No.

**[00:37:48] Priya Raman:** Absolutely not.

**[00:37:50] Jordan Ellis:** I'll put that in the "heard you" column. [laughter]

**[00:37:55] Dana Whitfield:** I do have one. Everybody's talking about AI. Could we have a chatbot? Like ChatGPT, on our website, where families can ask questions. "Am I eligible," "where's my application," that kind of thing.

**[00:38:06] Priya Raman:** That's public-facing, so that's the same conversation as the portal. And "where's my application" means it's looking up personal information for someone we haven't verified. I'd put that in the future bucket.

**[00:38:18] Dana Whitfield:** Future bucket. Okay. But I want to come back to it.

**[00:38:23] Linda Castellanos:** Can I add one thing about the notices? When we send a notice, we need proof it was sent. Date generated, date mailed. Because for appeals, the thirty days runs from the notice date, and families sometimes say they never got it.

**[00:38:38] Sam Patel:** So the notice record stores the generated date and mailed date. Is there anything that confirms mailing today?

**[00:38:45] Linda Castellanos:** The print center sends back a manifest. A list of what they mailed each day. Right now it's a PDF that someone files.

**[00:38:54] Sam Patel:** Got it. That's another potential integration, the print center manifest.

**[00:38:58] Linda Castellanos:** And, sorry, one more. When a case is closed, it should be closed. Locked. If someone needs to reopen it, there should be a reason, and a supervisor should approve.

**[00:39:09] Marcus Oyelaran:** That's fine, as long as it's quick. Sometimes we close something by accident.

**[00:39:15] Linda Castellanos:** [inaudible] … reason, that's all I'm asking.

**[00:39:18] Jordan Ellis:** Linda, I think you cut out for a second, but I think we got it. Reopening requires a reason and supervisor approval.

**[00:39:27] Linda Castellanos:** Yes, sorry, my internet is being… yes.

**[00:39:31] Marcus Oyelaran:** Can I say one thing about the household? Households change. Somebody moves out, a baby is born, a grandmother moves in. Today, if the household changes, we kind of overwrite it, and then you can't tell who was in the household at the time of the application.

**[00:39:47] Linda Castellanos:** Which matters for appeals. The hearing officer needs to see the household as it was when we made the decision.

**[00:39:55] Sam Patel:** So household membership needs history. Who was in the household, and when.

**[00:40:00] Marcus Oyelaran:** Right. And the same person can be in two households. Like, kids with divorced parents, and both parents apply for Child Care.

**[00:40:08] Dana Whitfield:** Oh, that's a good one. That's a real problem, actually. We've had double payments for the same child.

**[00:40:16] Sam Patel:** So the system should flag when a child is on an active Child Care case in another household?

**[00:40:23] Dana Whitfield:** Flag it. Yes.

**[00:40:25] Marcus Oyelaran:** Flag, not block. There are legitimate split-custody situations.

**[00:40:29] Dana Whitfield:** Right. Flag.

**[00:40:31] Jordan Ellis:** This has been incredibly helpful. Let me try to play back what I heard at a high level, and then Sam will send detailed notes. So, one system for Housing, Utility, and Child Care, staff-facing in phase one. A household view across programs. Intake with smart duplicate matching where the caseworker decides on merges. Program-specific document checklists with verification tracking. Eligibility calculation, and the system makes the decision with an override for caseworkers.

**[00:40:56] Dana Whitfield:** No, sorry, the other way. The system recommends, the caseworker decides.

**[00:41:01] Jordan Ellis:** Sorry, yes, thank you. The system recommends, the caseworker decides, and a reason is required when they differ. Supervisor approval over a threshold, configurable. Supervisor-assigned work with system suggestions. Deadline tracking with expedited cases flagged automatically. Notices generated from templates with appeal rights always included. A full appeals workflow. Audit logging, restricted cases. Reporting for the legislature and federal reporting, plus exports with controls. QA sampling. And then a list of technical requirements from Priya: single sign-on, roles, hosting, accessibility, migration.

**[00:41:28] Sam Patel:** And recertification for Child Care.

**[00:41:31] Jordan Ellis:** And recertification for Child Care. Did I miss anything big?

**[00:41:35] Marcus Oyelaran:** Referrals between programs. That's a big one for me.

**[00:41:40] Jordan Ellis:** Referrals between programs. Yes.

**[00:41:43] Linda Castellanos:** And the notes. The note history.

**[00:41:46] Jordan Ellis:** Case notes, with the open question on editing. Got it.

**[00:41:51] Jordan Ellis:** And in the parking lot: online applications, text message reminders, which has a star, the WestPay integration beyond a nightly file, the Westmarch Power shutoff list, the chatbot, and offline mode needs more discussion.

**[00:42:03] Marcus Oyelaran:** And timesheets.

**[00:42:05] Jordan Ellis:** And timesheets, which is a firm no. [laughter]

**[00:42:09] Sam Patel:** I've got a list of open questions too. Document age limits by program. The approval threshold, thirty-five hundred versus five thousand. Note editing. Whether domestic violence restrictions cover the whole case or the address. Whether families consent before a referral. The reinstatement window for Child Care. And migration scope.

**[00:42:26] Dana Whitfield:** That's a good list. I'll take the policy ones. Marcus, send me that memo on the threshold.

**[00:42:33] Marcus Oyelaran:** Will do. Sending it right after this.

**[00:42:36] Priya Raman:** I'll send the security requirements and the integration standards.

**[00:42:41] Linda Castellanos:** I'll send the appeal forms, the notice templates, and the QA checklist.

**[00:42:46] Dana Whitfield:** And I'll send the legislative report templates and the application numbers.

**[00:42:51] Jordan Ellis:** Perfect. For next steps, we'd like to schedule two deeper sessions. One on appeals and quality assurance with Linda, and one on reporting with Dana and whoever on your team builds the reports today. And then a session with a couple of caseworkers, Marcus, if you can spare them, so we can watch how they actually work.

**[00:43:10] Marcus Oyelaran:** Yeah, I can give you two people. Maybe Teresa and Andre. They'll have opinions. [laughs]

**[00:43:17] Jordan Ellis:** Opinions are exactly what we want.

**[00:43:20] Dana Whitfield:** Can I say one last thing? Just, for the Northgate folks. I know we threw a lot at you. The thing I care about most, if you take one thing away, is the family. Right now, families tell their story three times to three different people, and we still miss deadlines. If this system means a family tells their story once and gets an answer on time, that's the win.

**[00:43:44] Jordan Ellis:** That's really clear, thank you, Dana. We'll keep that front and center.

**[00:43:49] Priya Raman:** And securely. [laughter]

**[00:43:51] Dana Whitfield:** And securely.

**[00:43:53] Jordan Ellis:** And securely. Okay. Sam will send notes by end of day Thursday, and I'll send invites for the follow-up sessions. Thanks, everyone.

**[00:44:02] Marcus Oyelaran:** Thanks, all.

**[00:44:04] Linda Castellanos:** Thank you.

**[00:44:06] Dana Whitfield:** Thanks, everyone.

**[00:44:08] Sam Patel:** Thanks so much.

**[00:44:11] Marcus Oyelaran:** Oh, wait, sorry, before everyone drops. One more thing, really quick. Is there going to be a training environment? Like, a practice version? Because when we got the CAMS update in 2019, we found out about it the morning it went live.

**[00:44:25] Dana Whitfield:** [laughs] Yes. There will be training.

**[00:44:29] Priya Raman:** A training environment with fake data, not real data. Please.

**[00:44:33] Marcus Oyelaran:** Fake data that looks real, though. If every case is "Test Person One," my folks won't take it seriously.

**[00:44:41] Priya Raman:** Then someone has to build a realistic fake data set. Households, income, documents, appeals, the whole thing.

**[00:44:48] Jordan Ellis:** Noted. Training environment with realistic fake data. Okay, now we're really done. [laughter] Thanks, everyone.

**[00:44:54] Marcus Oyelaran:** Bye.

---

*Recording stopped at 00:44:54. Meeting ended at 10:46 AM.*
