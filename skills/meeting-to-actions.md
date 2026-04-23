---
name: meeting-to-actions
description: This skill should be used when the user provides "meeting notes", "call notes", "meeting transcript", "call transcript", "zoom transcript", "recording transcript", "extract action items", "meeting summary", "what did we decide", "process these meeting notes", "meeting recap", "call summary", "debrief", "post-meeting", "after the call", "here are my notes from the meeting", "parse this transcript", "meeting follow-ups", "action items from the call", "meeting minutes", or wants to extract decisions, action items, and follow-ups from any meeting-related text.
version: 1.0.0
---

# Meeting to Actions — Extract Decisions, Actions & Follow-Ups

## Overview

Meeting to Actions takes raw meeting notes, transcripts, or call recordings and transforms them into structured output: key decisions made, action items with owners and deadlines, follow-ups needed, and a clean summary. Powered by LindaAI, it then files the relevant pieces into the brain -- updating project files, creating daily log entries, adding people notes, and flagging anything that changes goals or priorities. LindaAI makes sure no action item gets left in the dust.

## When This Skill Applies

- User provides meeting notes or a transcript and says "process this"
- User says "meeting notes" or "call notes" or "here are my notes from the meeting"
- User says "extract action items" or "what did we decide?"
- User says "meeting summary" or "call summary" or "recap"
- User says "debrief" or "post-meeting" or "after the call"
- User pastes a transcript and wants it organized
- User says "parse this transcript" or "meeting follow-ups"
- User says "meeting minutes" or "action items from the call"
- User provides a Zoom, Google Meet, or phone call transcript
- User describes what happened in a meeting verbally (brain-dump style)

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

### Step 1: Receive the Input

Accept the meeting content in any format:
- **Raw transcript:** Timestamped or plain text from Zoom, Google Meet, Otter.ai, etc.
- **Manual notes:** Bullet points or freeform text the user typed during/after the call
- **Voice-to-text dump:** Unstructured stream of what happened
- **File reference:** User points to a file containing notes (read it)

If the user provides a file path, read it with the Read tool.

Also gather context:
- **Who was in the meeting?** (names, roles)
- **What was the meeting about?** (topic, project, deal)
- **When did it happen?** (date — default to today if not specified)

### Step 2: Extract Key Decisions

Scan the content for decisions — statements where a choice was made, a direction was set, or an agreement was reached. Decisions sound like:
- "We decided to..."
- "We agreed that..."
- "The plan is to..."
- "We're going with..."
- "Let's do..."
- Any clear resolution of a previously open question

For each decision, capture:
- **What was decided**
- **Who made or agreed to the decision** (if identifiable)
- **Context** (why this decision was made, if stated)
- **Impact** (what does this change?)

### Step 3: Extract Action Items

Scan for action items — tasks that someone committed to doing. Action items sound like:
- "[Name] will..."
- "I'll handle..."
- "Can you [do X]?"
- "Next step is..."
- "We need to..."
- "Follow up on..."
- "Send [something] to [someone]"
- Any commitment to do something by a certain time

For each action item, capture:

| Field | What to Extract |
|-------|----------------|
| **Action** | What needs to be done (clear, specific) |
| **Owner** | Who is responsible (name or role) |
| **Deadline** | By when (extract if mentioned, mark "TBD" if not) |
| **Priority** | High/Medium/Low based on urgency signals in the conversation |
| **Related Project** | Which brain/ project does this connect to? |

### Step 4: Extract Follow-Ups

Identify items that are not hard action items but require follow-up:
- "Let's circle back on..."
- "We'll revisit this next week"
- "Check in on [topic] after [event]"
- "Keep me posted on..."
- "Let me think about this and get back to you"
- Unresolved questions or open items

### Step 5: Extract Key Information

Pull out any noteworthy information shared during the meeting:
- Numbers, statistics, or data points mentioned
- New contacts or introductions
- Market intel or competitive info
- Personal details about attendees (preferences, concerns, interests)
- Deadlines or dates mentioned
- Commitments or promises made

### Step 6: Generate the Meeting Summary

Compile everything into a structured document:

```markdown
# Meeting Summary: [Meeting Topic/Name]

> **Date:** YYYY-MM-DD
> **Attendees:** [List of people]
> **Duration:** [If known]
> **Related Project:** [brain/ project if applicable]

---

## Summary

[2-4 sentences capturing what the meeting was about and the key outcome]

---

## Key Decisions

| # | Decision | Made By | Impact |
|---|----------|---------|--------|
| 1 | [What was decided] | [Who] | [What this changes] |
| 2 | [What was decided] | [Who] | [What this changes] |

## Action Items

| # | Action | Owner | Deadline | Priority | Status |
|---|--------|-------|----------|----------|--------|
| 1 | [Task] | [Name] | [Date/TBD] | High | Pending |
| 2 | [Task] | [Name] | [Date/TBD] | Medium | Pending |
| 3 | [Task] | [Name] | [Date/TBD] | Low | Pending |

## Follow-Ups

- [ ] [Follow-up item 1] — [Owner] — [Timeline]
- [ ] [Follow-up item 2] — [Owner] — [Timeline]

## Key Information Shared

- [Important data point or insight]
- [New contact or introduction]
- [Market intel]

## Open Questions

- [Question that was raised but not resolved]
- [Topic to revisit later]

---

## Raw Notes

[Include or link to the original notes/transcript for reference]
```

### Step 7: File Into the Brain

After generating the summary, update relevant brain files:

1. **Daily Log:** Append meeting summary to `brain/daily/{YYYY-MM-DD}.md`
   - Add under "Done" section: "Met with [attendees] about [topic]"
   - Add key decisions under "Decisions Made"

2. **Project Files:** If the meeting relates to an active project:
   - Read the project file from `brain/projects/`
   - Add action items to "Current Tasks" section
   - Log key decisions in "Key Decisions Made" table
   - Update "Blockers" if any were discussed

3. **People Files:** If new information was learned about a person:
   - Update their file in `brain/people/` (preferences, contact info, relationship context)
   - Create a new person file if they are not in the brain yet

4. **Goals:** If any decisions impact goals or priorities:
   - Flag this to the user: "This decision may affect [goal]. Update goals.md?"

5. **SOPs:** If a process was discussed or refined:
   - Note it for potential SOP creation

### Step 8: Report to User

Present:
1. The clean meeting summary (decisions + action items table)
2. Where each piece was filed in the brain
3. Any flags (goal impacts, missing deadlines, unresolved questions)
4. Suggested next steps

## Quality Standards

1. **No action item left behind.** If someone said they would do something, it appears in the action items table.
2. **Owners are named.** "We need to do X" is not an action item until it has an owner. If no owner was specified, flag it as "Owner: TBD" and ask the user.
3. **Decisions are decisions.** Do not list discussion topics as decisions. A decision has a clear outcome.
4. **Deadlines matter.** If a deadline was mentioned, capture it. If not, mark TBD and flag it.
5. **Verify before writing.** Read existing brain files before updating them to avoid overwriting.
6. **Preserve the original.** Always keep the raw notes/transcript accessible for reference.

## Output Format

A structured meeting summary (as shown above) plus updates to relevant brain files (daily log, project files, people files). The summary itself is appended to the daily log and optionally saved as a standalone file for important meetings.

## Example Usage

**User:** "Here are my notes from the call with Marcus about him becoming a TC:
- He's interested, has experience with 3 deals
- Wants to start next week
- Needs the TC training packet
- We agreed on $500/deal fee structure
- He'll send his LLC docs by Friday
- I need to send him the TC agreement via Dropbox Sign"

**AI produces:**
- Meeting summary with 1 decision (fee structure) and 3 action items
- Creates `brain/people/marcus.md` with role=TC, context, fee agreement
- Appends to today's daily log
- Updates TOP Wheels project file with new TC pipeline activity
- Flags: "Action item for you: Send TC agreement via Dropbox Sign to Marcus"

**User:** [Pastes a 45-minute Zoom transcript]

**AI produces:**
- Extracts all decisions, action items, follow-ups from the full transcript
- Generates a clean 1-page summary
- Files everything appropriately
- Presents the summary with "5 decisions made, 8 action items identified, 3 follow-ups needed"

**User:** "Debrief from the Squad Up Summit meeting — we decided to do a live demo of SellFi on stage, John will handle the AV setup, I need to prep a 10-minute pitch, and we should follow up with the event organizer about the time slot"

**AI produces:**
- 1 decision (live demo on stage)
- 3 action items (John: AV setup, User: prep pitch, User: follow up with organizer)
- Updates SellFi project file
- Logs to daily

## Error Handling

- **If the user provides no meeting notes or transcript:** Ask: "I need meeting notes or a transcript to process. You can paste text directly, describe what happened, or point me to a file path."
- **If the user provides a file path that does not exist:** Report: "I could not find a file at '{path}'. Double-check the path and try again, or paste the notes directly."
- **If the notes are too short or vague to extract meaningful actions:** Extract what you can and flag: "These notes are pretty brief — I extracted {N} items but there may be more. Can you add any details about what was decided or assigned?"
- **If action items have no clear owner:** List them with "Owner: TBD" and flag: "These {N} action items don't have clear owners assigned. Can you tell me who's responsible for each?"
- **If action items have no deadlines:** Set them as "Deadline: TBD" and tell the user: "None of these action items had a deadline hitched to 'em. Want me to set default deadlines (say, 1 week from today) or leave them as TBD?"
- **If `brain/daily/` directory does not exist:** Create it automatically before writing the daily log entry.
- **If the daily log file for today already exists:** Append the meeting summary to the existing log rather than overwriting. Add it under a "## Meetings" section.
- **If a referenced project file in `brain/projects/` does not exist:** Do not create a new project file automatically. Instead, note: "The meeting referenced '{project name}' but no matching project file exists. Want me to create one?"
- **If a person mentioned in the meeting is not in `brain/people/`:** Note the new contact and offer: "'{name}' was mentioned in the meeting but doesn't have a contact entry. Want me to create one with the context from this meeting?"
- **If the transcript is extremely long (thousands of lines):** Process it in logical sections (beginning, middle, end), extract all items, and deduplicate before presenting the final summary.


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
