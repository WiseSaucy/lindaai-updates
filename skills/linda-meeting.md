---
name: linda-meeting
description: This skill should be used when the user asks to "prep for a meeting", "meeting prep", "prepare for a meeting", "meeting brief", "pre-meeting brief", "brief me on this meeting", "meeting intelligence", "who am I meeting with", "prep for a call", "prepare for a call", "get ready for my meeting with", "research before my meeting", "meeting agenda", "meeting talking points", "build an agenda", "pre-call research", "meeting background", "I have a meeting with", "meeting with [name] about [topic]", "what should I know before my meeting", "prep me", "call prep", "call brief", "prepare talking points", "objection handling for meeting", "follow-up template", "post-meeting template", or wants to prepare for any upcoming meeting, call, or face-to-face conversation with thorough intelligence and structure.
version: 1.0.0
---

# Meeting Prep — Pre-Meeting Intelligence Brief

## Overview

Meeting Prep builds a complete intelligence dossier before any meeting, call, or conversation. You tell LindaAI who the meeting is with and what it's about. LindaAI researches the person and/or company, checks internal CRM notes, constructs a tailored agenda, develops talking points with supporting evidence, anticipates objections, and generates a post-meeting follow-up template. The output is a single document you can glance at 5 minutes before the meeting and walk in prepared like you spent hours getting ready.

## When This Skill Applies

- User says "prep for a meeting" or "meeting prep"
- User says "prepare for a meeting with [name]"
- User says "brief me on [person/company] before our call"
- User says "I have a meeting with [name] about [topic]"
- User says "meeting agenda for [topic]"
- User says "who am I meeting with?" (with context)
- User says "call prep" or "prep me for a call with [name]"
- User says "what should I know before my meeting?"
- User says "build an agenda" or "create talking points"
- User says "research [person] before our meeting"
- User says "objection handling" in the context of an upcoming meeting
- User says "post-meeting follow-up template"
- User mentions a specific person/company and an upcoming meeting or call

## How It Works

### License Check

Before proceeding, verify the LindaAI license:

1. Read `~/.claude/linda-license.json`
2. If the file does not exist, stop and tell the user:
   > 🤠 "Whoa there, partner — no LindaAI license found on this machine. You'll need a valid license to use LindaAI skills. Reach out to get set up and we'll have you in the saddle in no time."
   Do not proceed with any other steps.
3. If today's date is past the `expiration_date`, stop and tell the user:
   > 🤠 "Whoa there, partner — your LindaAI license expired on [expiration_date]. Reach out to renew and we'll get you back in the saddle." 🏇
   Do not proceed with any other steps.
4. If `status` is not `"active"`, stop and tell the user:
   > 🤠 "Whoa there, partner — your LindaAI license is currently [status]. Reach out to get this sorted and we'll have you riding again in no time."
   Do not proceed with any other steps.
5. **Server Verification (tamper check):** If the license file contains an `api_url` field, use WebFetch to check `{api_url}/v1/licenses/validate/{license_key}`. Parse the JSON response.
   - If the server responds with `"valid": false`, the local license has been tampered with. Stop and tell the user:
     > 🤠 "Hold up, partner — your license didn't check out with the server. Something's not matching up. Reach out to support to get this straightened out."
     Then use WebFetch to POST a tamper alert to `{api_url}/v1/licenses/tamper-alert` with JSON body: `{"license_key": "[key]", "local_expiration": "[local expiration_date]", "server_expiration": "[server expires from response]", "local_status": "[local status]", "details": "Local file passed but server validation failed"}`. Do not proceed.
   - If the server is unreachable or returns an error, proceed anyway (allow offline use — don't block paying customers because of a server hiccup).
   - If the server responds with `"valid": true`, proceed.
6. If all checks pass, proceed.

### Step 1: Gather Meeting Context

Determine from the user's request:

1. **Who:** Name of the person or company. Multiple attendees? Get all of them.
2. **What:** The meeting topic or purpose (deal negotiation, partnership pitch, client onboarding, investor update, networking intro, sales call, etc.)
3. **When:** Date and time if provided (affects urgency and prep depth)
4. **Where:** In-person, Zoom, phone call? Affects logistics recommendations.
5. **Background:** What has happened before this meeting? First meeting or follow-up?
6. **Desired Outcome:** What does the user want to walk away with? (A signed contract, a next meeting, a commitment, information, a relationship started)
7. **Concerns:** Anything the user is worried about or wants to handle carefully?

**Auto-personalization:** Check `brain/people/` for the person:
- If a file exists, read it for relationship context, prior interactions, communication preferences, and current deal status
- If no file exists, proceed with external research and note the gap

### Step 2: Research the Person/Company

#### Internal Research (brain/)
- Check `brain/people/` for existing contact files
- Check `brain/projects/` for any shared projects or deals
- Check `brain/daily/` for recent mentions or interactions
- Check `brain/research/` for any prior research on the person or company

#### External Research (web)

> 🤠 "Hold tight — heading over yonder to gather up the details."

Run targeted web searches:

| Data Point | Search Strategy |
|-----------|----------------|
| **Person's role and background** | Search "[Full Name] [Company] LinkedIn", "[Full Name] [Company]" |
| **Company overview** | Search "[Company Name]", "[Company Name] about", "[Company Name] Crunchbase" |
| **Recent news/activity** | Search "[Full Name] OR [Company Name] 2025 2026 news" |
| **Social presence** | Search "[Full Name] Twitter", "[Full Name] LinkedIn posts" |
| **Company financials/size** | Search "[Company Name] funding", "[Company Name] revenue", "[Company Name] employees" |
| **Mutual connections** | Check brain/people/ for anyone connected to this person/company |
| **Content they have published** | Search "[Full Name] podcast", "[Full Name] interview", "[Full Name] blog" |
| **Their priorities/pain points** | Search "[Company Name] challenges 2026", "[Company Name] hiring" (hiring = growth signals) |

If WebSearch returns limited results, note what was found and what was not. Never fabricate information.

### Step 3: Build the Person/Company Profile

Compile a concise intelligence profile:

```markdown
## Person Profile

**Name:** [Full Name]
**Title:** [Current Title]
**Company:** [Company Name]
**Role:** [What they actually do, beyond the title]
**Background:** [Career trajectory, notable experience, education if relevant]
**Communication Style:** [Inferred from content/profiles — formal, casual, data-driven, relationship-first]
**What They Care About:** [Based on their content, company priorities, recent activity]
**Recent Activity:** [Anything notable in the last 3-6 months — promotions, funding, launches, posts]
**Mutual Connections:** [Anyone in brain/people/ who connects to them]
**Social Profiles:** [LinkedIn, Twitter/X, other relevant links]
```

For company meetings (no specific person), build a company profile:

```markdown
## Company Profile

**Name:** [Company Name]
**Industry:** [Sector]
**Founded:** [Year]
**Size:** [Employee count, revenue range if known]
**What They Do:** [2-3 sentences]
**Key People:** [CEO, relevant decision-makers]
**Recent News:** [Last 3-6 months]
**Competitors:** [Who they compete with]
**Potential Synergies:** [Why this meeting matters — what could we do together?]
```

### Step 4: Construct the Meeting Agenda

Build a structured agenda tailored to the meeting type:

```markdown
## Proposed Agenda

**Meeting:** [Topic]
**With:** [Person/Company]
**Duration:** [Estimated time]

### 1. Opening (2-3 min)
- [Rapport builder — reference something specific about them]
- [Set the frame — what we are here to discuss]

### 2. Discovery / Context Setting (5-10 min)
- [Questions to understand their current situation]
- [Questions to understand their needs/pain points]
- [Questions to confirm assumptions]

### 3. Core Discussion (15-25 min)
- [Topic A — key point, supporting evidence, your position]
- [Topic B — key point, supporting evidence, your position]
- [Topic C — if applicable]

### 4. Handling Concerns (5-10 min)
- [Anticipated objection 1 — prepared response]
- [Anticipated objection 2 — prepared response]

### 5. Next Steps & Close (3-5 min)
- [Propose specific next step]
- [Confirm timelines and responsibilities]
- [Close with clear commitment or follow-up date]
```

Agenda length and depth should match the meeting type:
- **Quick intro call:** 15-min agenda, lightweight
- **Sales presentation:** 30-45 min, structured with a pitch flow
- **Negotiation:** Detailed with fallback positions
- **Partner/investor meeting:** Formal, data-backed, clear ask
- **Networking/relationship:** Casual, question-focused, give before you ask

### Step 5: Develop Talking Points

For each agenda section, provide:

1. **Key Point:** The core message in one sentence
2. **Supporting Evidence:** Data, examples, or anecdotes that back it up
3. **Transition:** How to naturally move to the next point
4. **If They Push Back:** A prepared pivot or reframe

Structure talking points as a quick-reference list the user can glance at:

```markdown
## Talking Points — Quick Reference

### Opening
- [Specific rapport builder: "I saw your post about X — really resonated because..."]
- [Frame setter: "I wanted to connect because I think there's a real opportunity to..."]

### Key Messages
1. **[Point 1]:** [One sentence] — Evidence: [Supporting fact or example]
2. **[Point 2]:** [One sentence] — Evidence: [Supporting fact or example]
3. **[Point 3]:** [One sentence] — Evidence: [Supporting fact or example]

### Questions to Ask Them
1. [Open-ended question about their situation]
2. [Question that reveals their pain points]
3. [Question that positions your solution]
4. [Question that gauges timeline/urgency]
5. [Question that identifies decision-makers]

### Power Phrases
- "[Phrase that positions you as an authority]"
- "[Phrase that creates urgency without pressure]"
- "[Phrase that builds trust]"
```

### Step 6: Anticipate Objections

Based on the meeting context, identify the 3-5 most likely objections and prepare responses:

```markdown
## Objection Handling

### Objection 1: "[Likely objection]"
**Why they might say this:** [Root cause]
**Response:** "[Prepared response that addresses the concern without being defensive]"
**Pivot to:** [How to redirect the conversation productively]

### Objection 2: "[Likely objection]"
**Why they might say this:** [Root cause]
**Response:** "[Prepared response]"
**Pivot to:** [Redirect]

### Objection 3: "[Likely objection]"
...
```

Objection types to consider:
- **Price/Cost:** "That's too expensive" / "We don't have budget"
- **Timing:** "Not the right time" / "Maybe next quarter"
- **Trust:** "I need to think about it" / "I need to talk to my partner"
- **Competition:** "We're already working with someone" / "What makes you different?"
- **Scope:** "We only need part of this" / "This seems like too much"
- **Risk:** "What if it doesn't work?" / "What's the guarantee?"

### Step 7: Create Post-Meeting Follow-Up Template

Generate a ready-to-customize follow-up email template:

```markdown
## Post-Meeting Follow-Up Template

**Send within:** [Timeframe — same day for hot leads, 24 hours for most meetings]

---

**Subject:** [Meeting-specific subject line]

[Name],

[Reference something specific from the meeting — proves you were paying attention]

[Recap the key points discussed — 2-3 bullet points max]

[Restate the next step that was agreed upon]

[Clear CTA — what happens next and by when]

[Sign-off]

---

**If the meeting went well:** [Variation that accelerates the timeline]
**If the meeting was lukewarm:** [Variation that adds value and keeps the door open]
**If the meeting went poorly:** [Variation that leaves a professional impression for future opportunity]
```

### Step 8: Compile and Save the Brief

Assemble everything into a single document:

```markdown
# Meeting Prep Brief: [Person/Company] — [Topic]

> **Date:** YYYY-MM-DD
> **Meeting With:** [Name, Title, Company]
> **Topic:** [What the meeting is about]
> **Desired Outcome:** [What you want to walk away with]
> **Prepared By:** LindaAI

---

## Intelligence Profile
[Person/Company profile from Step 3]

## Proposed Agenda
[Agenda from Step 4]

## Talking Points
[Quick reference from Step 5]

## Objection Handling
[Prepared objections from Step 6]

## Post-Meeting Follow-Up Templates
[Templates from Step 7]

## Pre-Meeting Checklist
- [ ] Review this brief (5 min before the meeting)
- [ ] Have relevant documents/links ready to share
- [ ] Confirm meeting logistics (link, address, phone number)
- [ ] Silence notifications
- [ ] Have a notebook or note-taking app open
- [ ] Know your walk-away point (if negotiation)

---

🤠 *Generated by LindaAI* 🏇
*Update brain/people/{name}.md after the meeting with outcomes and next steps.*
```

Save to: `brain/research/meeting-prep-{person-slug}-{YYYY-MM-DD}.md`

### Step 9: Present to User

Give the user:
1. The intelligence profile (key things to know about this person)
2. The proposed agenda (offer to adjust)
3. The top 3 talking points (most important things to say)
4. The #1 objection to prepare for
5. Where the full brief was saved
6. Reminder to update brain/people/ after the meeting

## Quality Standards

1. **Real research, not filler.** Every fact in the intelligence profile comes from an actual source. If info is not available, say so — do not invent background details.
2. **Tailored, not generic.** The agenda, talking points, and objections must be specific to THIS meeting with THIS person about THIS topic. Generic meeting templates are worthless.
3. **Actionable.** The user should be able to glance at this 5 minutes before the meeting and feel prepared.
4. **Honest assessment.** If the meeting looks like it will be difficult, say so. Flag risks. Do not sugarcoat.
5. **Respect privacy.** Research only publicly available information. Do not suggest accessing private data or systems without authorization.
6. **CRM integration.** Always check brain/people/ first. Always recommend updating it after the meeting.

## Output Format

A single comprehensive markdown file saved to `brain/research/meeting-prep-{person-slug}-{YYYY-MM-DD}.md`. Typically 1,500-3,000 words depending on the meeting complexity and available information about the person/company.

## Example Usage

**User:** "Meeting prep — I have a call with Sarah Chen tomorrow about the syndication fund partnership"

**AI executes:**
- Checks `brain/people/sarah-chen.md` for existing context
- Researches Sarah Chen online for recent activity and background
- Builds a partnership-focused agenda with talking points about fund structure
- Anticipates objections around risk, commitment level, and equity split
- Creates follow-up templates for three outcomes (yes, maybe, no)
- Saves to `brain/research/meeting-prep-sarah-chen-2026-03-03.md`

**User:** "Prep me for a cold pitch meeting with the CEO of AutoNation"

**AI executes:**
- No CRM file exists — relies on external research
- Deep dives AutoNation: CEO bio, company size, recent news, pain points
- Builds a sales-pitch agenda with value proposition tailored to AutoNation
- Heavy objection prep (cold meeting = more resistance)
- Saves to `brain/research/meeting-prep-autonation-ceo-2026-03-03.md`

**User:** "I have a meeting with my CPA about tax strategy — prep me"

**AI executes:**
- Checks brain/people/ for CPA contact info
- Lighter external research (focus on tax-relevant context)
- Builds an agenda focused on questions to ask the CPA
- Talking points center on the user's financial situation and goals (from brain/goals.md)
- Saves to `brain/research/meeting-prep-cpa-tax-strategy-2026-03-03.md`

## Error Handling

- **If the user does not specify who the meeting is with:** Ask: "Who is the meeting with? I need at least a name (and ideally their company or role) to build a useful brief."
- **If the user does not specify the meeting topic:** Ask: "What is this meeting about? Knowing the topic lets me tailor the agenda, talking points, and objection handling."
- **If WebSearch returns very little about the person:** Note honestly in the profile: "Limited public information available for [Name]. This brief is based on what was found — consider asking them directly about their background at the start of the meeting." Proceed with available data.
- **If no CRM file exists for the person:** Proceed with external research. Note: "I don't have [Name] in your contacts. Want me to create a contact file after this meeting?"
- **If the user provides a company but no specific person:** Build a company-level brief and suggest asking who specifically will be in the meeting: "I've prepped a company-level brief. If you can get the name of who you'll actually be speaking with, I can add a personal profile."
- **If `brain/research/` does not exist:** Create it automatically before saving.
- **If a meeting prep file already exists for this person (same date):** Overwrite it — the user is likely re-running the prep with updated info. Note: "Updated your existing meeting prep brief for [Name]."
- **If the desired outcome is unclear:** Draft the brief with a general "explore the opportunity" framing, but flag: "I didn't have a specific desired outcome, so I've framed this as an exploratory meeting. If you have a specific ask (close a deal, get a commitment, secure funding), tell me and I'll sharpen the talking points."

---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
