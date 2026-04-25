---
name: linda-leads
description: This skill should be used when the user asks to "track a lead", "add a lead", "update a lead", "view my pipeline", "show my leads", "move a lead to the next stage", "mark a lead as closed", "mark a lead as lost", "who do I need to follow up with", "show follow-up reminders", "pipeline status", "lead pipeline", "CRM", "add a contact to the pipeline", "new prospect", "update deal status", "what leads are in negotiation", "who's in my pipeline", "lead management", "sales pipeline", "deal tracker", or anything related to managing leads, prospects, contacts through a sales pipeline. Also triggers when the user says "add to pipeline", "pipeline report", "lead report", "sales funnel", "prospect tracker", or "follow up list".
version: 1.0.0
---

# Lead Tracker

## Overview

LindaAI runs a file-based lead and contact pipeline manager that tracks prospects through defined sales stages. All data is stored as markdown files in `brain/pipeline/`, making it human-readable, version-controllable, and accessible to any session. Each lead gets its own file with full history, and LindaAI keeps the master pipeline index updated so you always have a clean dashboard view.

## When This Skill Applies

- User wants to add a new lead or prospect
- User wants to update a lead's status or stage
- User asks to view the pipeline or see all leads
- User asks "who do I need to follow up with?"
- User wants to mark a deal as closed-won or closed-lost
- User asks for a pipeline report or summary
- User mentions CRM, sales pipeline, deal tracker, or lead management
- User says "add to pipeline", "move to negotiating", "lost the deal", etc.
- User wants to log notes or interactions against a lead

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

### Directory Structure

```
brain/pipeline/
  README.md              -- Master pipeline index (dashboard view)
  leads/
    {firstname-lastname}.md   -- Individual lead files
```

### Pipeline Stages

| Stage | Code | Description |
|-------|------|-------------|
| New | `new` | Just added, no outreach yet |
| Contacted | `contacted` | Initial outreach made |
| Qualified | `qualified` | Confirmed fit, has budget/need/authority |
| Negotiating | `negotiating` | Active deal discussion, terms being worked |
| Closed-Won | `closed-won` | Deal done, revenue captured |
| Closed-Lost | `closed-lost` | Deal dead, with reason logged |

### Step 1: Initialize Pipeline (first time only)

Check if `brain/pipeline/` exists. If not, create the directory structure and README.md index.

Create `brain/pipeline/README.md`:

```markdown
# Lead Pipeline

> **Last Updated:** {date}

## Dashboard

| Lead | Company | Stage | Value | Next Action | Follow-Up Date |
|------|---------|-------|-------|-------------|----------------|

## Stage Summary

| Stage | Count | Total Value |
|-------|-------|-------------|
| New | 0 | $0 |
| Contacted | 0 | $0 |
| Qualified | 0 | $0 |
| Negotiating | 0 | $0 |
| Closed-Won | 0 | $0 |
| Closed-Lost | 0 | $0 |
```

Create `brain/pipeline/leads/` directory.

### Step 2: Add a New Lead

When user says "add a lead" or provides lead info, create a lead file at `brain/pipeline/leads/{firstname-lastname}.md`:

```markdown
# {Full Name}

> **Stage:** new
> **Created:** {YYYY-MM-DD}
> **Last Updated:** {YYYY-MM-DD}
> **Follow-Up Date:** {YYYY-MM-DD, default 3 days from now}

## Contact Info

| Field | Value |
|-------|-------|
| Name | {name} |
| Company | {company or "—"} |
| Phone | {phone or "—"} |
| Email | {email or "—"} |
| Source | {where the lead came from or "—"} |

## Deal Info

| Field | Value |
|-------|-------|
| Estimated Value | ${amount or "TBD"} |
| Product/Service | {what they need} |
| Timeline | {when they need it} |
| Decision Maker | {yes/no/unknown} |

## Notes

- {YYYY-MM-DD}: Lead added. {any initial notes}

## Interaction History

| Date | Type | Summary |
|------|------|---------|
| {date} | Added | Lead created |
```

After creating the lead file, update the `brain/pipeline/README.md` dashboard table.

### Step 3: Update a Lead

When user says "move {name} to negotiating" or "update {name}":

1. Read the lead file from `brain/pipeline/leads/`
2. Update the `> **Stage:**` field
3. Update `> **Last Updated:**` date
4. Add a note to the Notes section with what changed
5. Add entry to Interaction History
6. Update the dashboard in `brain/pipeline/README.md`

### Step 4: View Pipeline

When user says "show pipeline" or "pipeline status":

1. Read `brain/pipeline/README.md` for the dashboard
2. Optionally read individual lead files for detail
3. Present a clean summary:
   - Total leads by stage
   - Total pipeline value
   - Leads needing follow-up (follow-up date is today or past)
   - Leads that have been stale (no update in 7+ days)

### Step 5: Follow-Up Reminders

When user asks "who do I need to follow up with?" or "follow-up reminders":

1. Read all lead files in `brain/pipeline/leads/`
2. Check each lead's `Follow-Up Date` against today's date
3. Flag any lead where:
   - Follow-up date is today or in the past
   - Lead has been in the same stage for 7+ days with no activity
   - Lead is in "contacted" or "negotiating" stage (high-priority follow-ups)
4. Present sorted by urgency

### Step 6: Pipeline Report

When user asks for a pipeline report:

1. Read all lead files
2. Calculate:
   - Total leads per stage
   - Total pipeline value (sum of estimated values for active leads)
   - Conversion rate (closed-won / total closed)
   - Average time in pipeline
   - This week's activity (new leads added, stages changed, deals closed)
3. Present as a formatted report

## Output Format

### Adding a Lead
```
Lead added: {Name} ({Company})
Stage: New
Estimated Value: ${amount}
Follow-up set for: {date}
Pipeline updated.
```

### Pipeline Dashboard
```
PIPELINE SUMMARY — {date}
================================
New:          {count} leads  (${value})
Contacted:    {count} leads  (${value})
Qualified:    {count} leads  (${value})
Negotiating:  {count} leads  (${value})
Closed-Won:   {count} leads  (${value})
Closed-Lost:  {count} leads  (${value})
--------------------------------
Active Pipeline: {count} leads, ${total value}

NEEDS FOLLOW-UP:
- {Name} — {stage} — follow-up was {date}
- {Name} — {stage} — no activity for {N} days
```

### Stage Update
```
{Name} moved from {old stage} to {new stage}.
Notes: {any notes added}
Next follow-up: {date}
```

## Example Usage

**User:** "Add John Smith to the pipeline. He's from ABC Motors, interested in a connection deal, estimated $5K. His email is john@abcmotors.com"

**AI:** Creates `brain/pipeline/leads/john-smith.md`, updates dashboard, confirms.

**User:** "Move John Smith to qualified"

**AI:** Updates stage, adds note, sets follow-up for 3 days, updates dashboard.

**User:** "Show my pipeline"

**AI:** Reads all lead files, presents dashboard with stage counts, values, and follow-up alerts.

**User:** "Who needs follow-up?"

**AI:** Scans all leads, identifies overdue follow-ups, presents sorted list.

**User:** "Mark John Smith as closed-won. Connection fee was $4,500."

**AI:** Updates stage to closed-won, logs final value, adds to interaction history, updates dashboard.

**User:** "/lead-tracker add Sarah Lee — she's a buyer from Facebook Marketplace, budget $15K, phone 555-9876"

**AI:** Creates `brain/pipeline/leads/sarah-lee.md` with stage: new, source: Facebook Marketplace, value: $15,000, phone captured. Updates dashboard. Sets follow-up for 3 days.

**User:** "/lead-tracker pipeline"

**AI:** Reads all lead files and produces:
```
PIPELINE SUMMARY — 2026-03-02
================================
New:          2 leads  ($20,000)
Contacted:    1 lead   ($8,000)
Qualified:    3 leads  ($45,000)
Negotiating:  1 lead   ($12,000)
Closed-Won:   4 leads  ($38,500)
Closed-Lost:  1 lead   ($5,000)
--------------------------------
Active Pipeline: 7 leads, $85,000
Won This Month:  $38,500

NEEDS FOLLOW-UP:
- Sarah Lee — new — follow-up was 2026-02-28
- Marcus Thompson — negotiating — no activity for 8 days

STALE LEADS (no update in 7+ days):
- James Rivera — contacted — last updated 2026-02-22
```

**User:** "/lead-tracker update Marcus Thompson --stage closed-won --value 4500 --notes 'TC fee collected, deal closed successfully'"

**AI:** Updates Marcus from negotiating to closed-won, sets final value to $4,500, adds timestamped note and interaction history entry, updates dashboard totals.

## Error Handling

- **If `brain/pipeline/` directory does not exist:** Create it automatically along with `brain/pipeline/leads/` and the initial `README.md` dashboard file. Do not error — initialize silently and proceed.
- **If user does not provide a lead name:** Ask specifically: "What is the lead's name? I need at least a first and last name to create their file."
- **If user does not provide enough info for required fields:** Create the lead with what is available, fill missing fields with "TBD", and inform the user: "I created the lead with the info you gave me. These fields are still TBD: [list]. You can update them anytime with `/lead-tracker update [name]`."
- **If a lead file already exists for that name:** Do not overwrite. Instead, warn: "A lead file already exists for {name}. Did you mean to update their record? Use `/lead-tracker update {name}` to modify existing leads." If the user confirms they want a new entry (different person, same name), create the file with a numeric suffix: `{firstname-lastname}-2.md`.
- **If the user references a lead name that does not exist:** Search all lead files using fuzzy matching (partial name, misspellings). If a close match is found, suggest: "I didn't find '{name}' but I found '{close match}'. Did you mean them?" If no match, report: "No lead found matching '{name}'. Current leads: [list names]."
- **If `brain/pipeline/README.md` dashboard gets out of sync with individual lead files:** When running `/lead-tracker pipeline` or `/lead-tracker status`, always rebuild the dashboard from the individual lead files rather than trusting the cached dashboard. Update the README.md with fresh data.
- **If deal value is provided in non-numeric format:** Parse common formats like "$5K", "$5,000", "5000", "five thousand" and convert to numeric. If unparseable, ask: "I couldn't parse the deal value '{input}'. Can you give me a number like $5,000?"
- **If the user tries to move a lead backward in the pipeline (e.g., from negotiating back to new):** Allow it, but confirm: "Moving {name} from {current stage} back to {requested stage}. This is unusual — are you sure? I'll log the reason in the notes."
- **If the user tries to update a closed lead (closed-won or closed-lost):** Allow it, but confirm: "This lead is already marked as {stage}. Do you want to reopen it? I'll move it to the stage you specified and log the reopen in the history."


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
