---
name: brain-dump
description: This skill should be used when the user says "add this to the brain", "remember this", "brain dump", "save this", "file this", "store this in the brain", "log this", "capture this", "note this down", "put this in the brain", "save to brain", "brain capture", "quick capture", "remember that", "don't forget", "add to knowledge base", "save this info", "file this away", "store this for later", or wants to quickly capture information and have AI intelligently route it to the correct location in the brain/ directory structure.
version: 1.0.0
---

# Brain Dump — Quick Capture & Intelligent Filing

## Overview

Brain Dump is LindaAI's fastest way to get information into the shared brain. You speak naturally — a thought, a fact, a decision, a contact, a goal update, anything — and LindaAI analyzes the content, determines the correct brain/ subdirectory, and files it in the right place using the correct template format. No manual filing, no thinking about where it goes.

## When This Skill Applies

- User says "add this to the brain" or "brain dump"
- User says "remember this" or "remember that"
- User says "save this" or "file this" or "store this"
- User says "note this down" or "capture this"
- User says "don't forget" followed by information
- User provides unstructured information and wants it organized
- User mentions a new contact, decision, goal change, project update, or learning
- User wants to quickly log something without specifying where it goes
- User says "put this in the brain" or "save to brain"
- User rattles off multiple pieces of information and wants them all captured

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

### Step 1: Receive the Brain Dump

Listen to whatever the user provides. It can be:
- A single fact ("John's email is john@example.com")
- A paragraph of thoughts
- Multiple unrelated pieces of information
- A voice-to-text style stream of consciousness
- A decision that was just made
- A goal update or status change
- A new contact or relationship detail
- A process or workflow description
- A learning or insight

### Step 2: Classify Each Piece of Information

Analyze the content and categorize each distinct piece into one or more of these brain/ destinations:

| Category | Brain Location | Trigger Signals |
|----------|---------------|-----------------|
| Goal update | `brain/goals.md` | Mentions goals, priorities, deadlines, status changes, quarterly objectives |
| New person / contact info | `brain/people/{name}.md` | Names, phone numbers, emails, roles, relationship context |
| Project update | `brain/projects/{project}.md` or `brain/projects/README.md` | Project names, milestones, blockers, status changes |
| Daily log entry | `brain/daily/{YYYY-MM-DD}.md` | Today's events, decisions, accomplishments, reflections |
| New SOP / process | `brain/sops/{name}.md` | Workflow descriptions, step-by-step processes, "how we do X" |
| Knowledge / domain info | `brain/knowledge-base/{category}/` | Business knowledge, method details, ecosystem info |
| Research finding | `brain/research/{topic}.md` | Market data, competitor info, statistics, opportunities |
| Calendar / planning | `brain/calendar/{month}.md` | Dates, events, deadlines, scheduling |
| Blueprint / spec | `brain/blueprints/{name}.md` | Technical plans, operational specs, architecture decisions |
| Identity / preferences | `brain/identity/USER.md` | Personal preferences, communication style, values |

### Step 3: Read the Target File(s)

Before writing, ALWAYS read the target file first to understand:
- Current content (avoid duplicates)
- File format and structure
- Where to insert the new information

If the target file does not exist yet:
- For people: Copy format from `brain/people/_TEMPLATE.md`
- For SOPs: Copy format from `brain/sops/_TEMPLATE.md`
- For projects: Copy format from `brain/projects/_TEMPLATE.md`
- For daily logs: Use the template from `brain/daily/README.md`
- For other files: Use clean markdown with a header, date, and organized sections

### Step 4: Write to the Correct Location

**For existing files:** Use the Edit tool to append or update the relevant section. Never overwrite existing content unless explicitly correcting it.

**For new files:** Use Write to create the file following the appropriate template.

**For daily logs:** Always append to today's file (`brain/daily/{YYYY-MM-DD}.md`). Create it if it does not exist.

**For people:** Check if the person already has a file. If yes, update it. If no, create one from the template.

**For goals:** Edit the specific section of `brain/goals.md` that applies (weekly priorities, monthly focus, status updates, etc.).

### Step 5: Update Indexes if Needed

If you created a NEW file (not just edited an existing one), update the relevant index:
- New person → Add to `brain/people/README.md` Index table
- New project → Add to `brain/projects/README.md` Dashboard table
- New SOP → Add to `brain/sops/README.md` Index table
- New research → No index needed (standalone files)

### Step 6: Confirm What Was Filed

Report back to the user with:
- What information was captured
- Where each piece was filed (full path)
- Any new files that were created
- Any questions if something was ambiguous

## Routing Decision Tree

```
User provides information
    |
    ├── Contains a person's name + contact details?
    |       → brain/people/{firstname-lastname}.md
    |
    ├── Mentions a goal, priority, or status change?
    |       → brain/goals.md (edit the relevant section)
    |
    ├── References a specific active project?
    |       → brain/projects/{project-name}.md
    |
    ├── Describes a repeatable process or workflow?
    |       → brain/sops/{process-name}.md
    |
    ├── Contains market research, competitor data, or statistics?
    |       → brain/research/{topic-slug}.md
    |
    ├── Is about today's events, decisions, or reflections?
    |       → brain/daily/{YYYY-MM-DD}.md
    |
    ├── Is domain knowledge (T.O.P. Method, SellFi, creative finance)?
    |       → brain/knowledge-base/{relevant-subfolder}/
    |
    ├── Is a technical plan, spec, or architecture decision?
    |       → brain/blueprints/{plan-name}.md
    |
    ├── Is about scheduling, deadlines, or calendar events?
    |       → brain/calendar/{YYYY-MM}.md
    |
    └── Unclear or mixed content?
            → brain/daily/{YYYY-MM-DD}.md (safe default)
            → Ask user if a more specific location is preferred
```

## Multi-Item Brain Dumps

When the user dumps multiple unrelated pieces of information at once:

1. Parse each distinct piece separately
2. Route each to its correct destination
3. Make all edits/writes
4. Report a summary showing each item and where it was filed

Example: "Remember that John's number is 555-1234, we decided to push the launch to March 15, and I learned that Carvana does $12B in annual revenue"
- Item 1 (John's number) → `brain/people/john.md`
- Item 2 (launch date) → `brain/goals.md` + `brain/daily/{today}.md`
- Item 3 (Carvana revenue) → `brain/research/competitor-intelligence.md`

## Output Format

After filing, respond with a clean summary:

```
Brain dump captured:

1. [Description of item 1]
   Filed to: brain/people/john-smith.md (updated contact info)

2. [Description of item 2]
   Filed to: brain/goals.md (updated March deadline)
   Also logged to: brain/daily/2026-03-02.md

3. [Description of item 3]
   Filed to: brain/research/competitor-intelligence.md (new data point)

New files created: 1 (brain/people/john-smith.md)
Files updated: 3
```

## Edge Cases

- **Ambiguous content:** Default to daily log, then ask if a more specific location is preferred
- **Contradicts existing data:** Flag the contradiction, ask the user which version is correct before overwriting
- **Sensitive information (passwords, keys):** Never store credentials in brain/ files. Warn the user and suggest storing in `~/.claude/credentials/` or a secure location instead
- **Very large dumps:** Break into logical chunks, file each separately, report the full manifest
- **Duplicate information:** If the info already exists in the brain, tell the user rather than creating a duplicate

## Example Usage

**User:** "Brain dump: talked to Marcus today, he's interested in being a TC for TOP Wheels. His email is marcus@email.com. Also, I posted 3 TikToks today. And I think we should add a referral system to SellFi."

**AI Action:**
1. Creates `brain/people/marcus.md` from template with role=potential TC, email, context about TOP Wheels interest
2. Updates `brain/people/README.md` index
3. Appends to `brain/daily/2026-03-02.md` — logged 3 TikTok posts under accomplishments
4. Appends to `brain/projects/sellfi-platform.md` or creates a note in the SellFi project about referral system feature idea
5. Reports what was filed and where

## Error Handling

- **If the target brain/ subdirectory does not exist:** Create it automatically before writing. For example, if routing to `brain/research/` and the directory is missing, create it. Never error on a missing directory — initialize silently.
- **If a target file does not exist yet (new person, new project, etc.):** Create it using the appropriate `_TEMPLATE.md` from the brain. If no template exists for that category, create a clean markdown file with a descriptive header and today's date.
- **If the user's input is ambiguous and could belong in multiple locations:** Default to the daily log (`brain/daily/{YYYY-MM-DD}.md`) as the safe catch-all, then ask the user: "I filed this in today's daily log. Would you prefer it in a more specific location like {suggested alternative}?"
- **If the information contradicts existing data in the brain:** Do not silently overwrite. Flag the contradiction: "The brain currently says {existing info}. You just said {new info}. Which is correct? I'll update once you confirm."
- **If the user provides sensitive data (passwords, API keys, SSNs, financial account numbers):** Do NOT store in brain/ files. Warn the user: "This looks like sensitive credentials. I won't store this in the brain — it should go in a secure location like `~/.claude/credentials/` or a password manager."
- **If the user provides a very large brain dump (multiple paragraphs of mixed info):** Parse it into individual items, route each separately, and present a numbered manifest of what went where. If any item is ambiguous, list it at the end with a question.
- **If reading a target file fails (corrupted or malformed markdown):** Write the new information to the daily log as a fallback, and warn: "I couldn't read {file path} — it may be malformed. I saved the info to today's daily log instead. You may want to check that file."
- **If the user says "brain dump" but does not provide any content:** Ask: "What would you like me to capture? Just tell me and I'll file it in the right place."


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
