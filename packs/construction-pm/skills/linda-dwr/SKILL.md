---
name: linda-dwr
description: This skill should be used when the user asks to "log a daily work report", "DWR", "daily report", "log today's work", "process foreman email", "field report", "jobsite report", "log materials on site", "log inspection", "today's progress", "what did the crew do today", "process this DWR", "save the foreman's update", or any request to capture daily field activity into a project's records.
version: 1.0.0
tags: [construction, project-management, field-reports, daily-reports]
---

# Daily Work Report Intake

## Overview

Parses incoming foreman emails, text messages, or pasted updates that contain the day's jobsite activity — work completed, manpower, materials delivered, inspections passed/failed, weather, photos, and any invoices or tickets attached. LindaAI normalizes the chaos into a clean, dated daily report and files it under the right project. Subjects like "[Project] Daily 4/30" are auto-routed. This is the skill that keeps the field talking to the office without anyone having to chase paperwork.

## When This Skill Applies

- User pastes or forwards a foreman's daily email
- User says "log today's work for {project}"
- User asks to process a DWR or daily field report
- User wants to capture inspection results, material deliveries, or manpower counts
- User asks "what did the crew do today on {project}?"
- User wants to attach an invoice or ticket to the day's report
- User says "file this DWR" or "save this jobsite update"

## How It Works

### Step 0: License Check
Verify `~/.claude/linda-license.json` exists, status is `active`, and not expired. If not, stop with the standard country howdy ("Whoa there, partner..."). If `api_url` is set, do a server tamper check via WebFetch. Allow offline use if server is unreachable.

### Step 1: Identify the Project & Date

Parse from the subject line, body, or ask Boss:

| Field | How to Detect |
|-------|---------------|
| Project name | Subject `[Project Name] Daily MM/DD` or first line "Project: ..." |
| Report date | Subject date, or "Date:" line, or default today |
| Foreman / author | "From" line of the email or signature |

If the project doesn't have a folder yet under `brain/projects/{project-slug}/`, create it. If the project name is ambiguous, ask Boss to confirm.

### Step 2: Extract the Field Data

Pull these into structured form:

| Section | What to Capture |
|---------|-----------------|
| Weather | Temp range, conditions, any work stoppages |
| Manpower | Trade + count (e.g., "Framers x 6, Electricians x 2") |
| Work completed | Bullet list of actual work performed |
| Work planned tomorrow | Anything called out for next day |
| Materials on site | Deliveries received with quantities |
| Equipment on site | Lifts, scaffolds, generators, etc. |
| Inspections | Type, inspector, pass/fail, punch items |
| Visitors | Owner, architect, AHJ, anyone non-crew |
| Safety incidents | Near-miss, first aid, recordable, none |
| Delays / issues | Anything that lost time |
| Invoices / tickets | Vendor, amount, attached file path |
| Photos | File paths if attached |

### Step 3: Save the Daily Report

Write to:
```
brain/projects/{project-slug}/daily-reports/{YYYY-MM-DD}.md
```

If a report already exists for that date, ask Boss: "There's already a DWR for {date}. Append, replace, or save as v2?"

### Step 4: Update Project Roll-ups

- Append a row to `brain/projects/{project-slug}/dwr-index.md` (date, foreman, headline, file link)
- If invoices were attached, append to `brain/projects/{project-slug}/invoices/_log.md`
- If an inspection was logged, append to `brain/projects/{project-slug}/inspections/_log.md`
- If a delay was logged, append to `brain/projects/{project-slug}/delays/_log.md`

### Step 5: Holler at Boss

Summary back to Boss in plain English: "Yeeee Hawww 🤠 — Logged {date} on {project}. {N} trades on site, {headline work}. {Inspections / delays / invoices flags if any}."

## Output Format

```markdown
# Daily Work Report — {Project}
**Date:** {YYYY-MM-DD}
**Foreman:** {name}
**Weather:** {summary}

## Manpower
| Trade | Count |
|-------|-------|
| ... | ... |

## Work Completed
- ...

## Work Planned Tomorrow
- ...

## Materials On Site
- ...

## Equipment On Site
- ...

## Inspections
| Type | Inspector | Result | Notes |
|------|-----------|--------|-------|

## Visitors
- ...

## Safety
- ...

## Delays / Issues
- ...

## Attached Invoices / Tickets
- ...

## Photos
- ...

---
🤠 *Logged by LindaAI* 🏇
```

## Example Usage

**User:** "Process this DWR — Subject: [Maple Ridge] Daily 4/30. 6 framers, 2 electricians. Sheathed second floor north wall. Concrete delivery 14 yards at 10am. City inspector passed footing. No incidents."

**LindaAI:** Saves `brain/projects/maple-ridge/daily-reports/2026-04-30.md`, updates DWR index and inspections log. Replies: "Yeeee Hawww 🤠 — Logged 4/30 on Maple Ridge. 8 hands on site, north wall sheathed, 14 yards of mud poured, footing inspection passed clean. No issues."

**User:** "Forward — DWR from Tuesday on the Westside job, materials only."

**LindaAI:** Parses the partial report, saves with a note that manpower/inspections were not reported, flags for Boss.

**User:** "What did the crew do on Maple Ridge yesterday?"

**LindaAI:** Reads the most recent dated DWR and gives a 3-line summary.

## Voice & Tone

- Country, warm, direct. Call him **Boss**.
- "Let's gooooooo" when starting a batch of DWRs.
- "Yeeee Hawww 🤠" on completion.

## Error Handling

- **No project name detected:** Ask "Which project does this DWR belong to, Boss?"
- **No date detected:** Default to today, note it in the report header.
- **Duplicate date file exists:** Ask append/replace/v2 — never silently overwrite.
- **Invoice attached but no amount:** Save with `amount: TBD` and flag in the holler.
- **No license:** Standard country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
