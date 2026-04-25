---
name: linda-pulse
description: This skill should be used when the user asks for a "project pulse", "project status", "what's the status of my projects", "project check", "what am I working on", "what's behind schedule", "what's blocked", "project dashboard", "show me my projects", "project overview", "what needs attention", "what needs my attention today", "project update", "status update on projects", "quick pulse check", "pulse check", "what's on fire", "project health", "project report", "active projects", "show projects", "what's going on with my projects", or anything related to checking the current state of all active projects at a glance.
version: 1.0.0
---

# Project Pulse

## Overview

LindaAI runs a quick pulse check across all active projects in `brain/projects/`. Reads every project file and the project dashboard, then generates a real-time status report that highlights what is on track, what is behind, what is blocked, and what needs attention today. Designed for a 60-second glance at your entire project portfolio — LindaAI keeps the whole ranch in view.

## When This Skill Applies

- User asks for a project status update or pulse check
- User wants to know what needs attention right now
- User asks "what am I working on?"
- User asks "what's behind?" or "what's on fire?"
- User wants a project dashboard or overview
- User asks "what should I focus on today?" (project context)
- Start of a work session when the user wants to get oriented
- User mentions "project health" or "project report"

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

### Step 1: Read the Project Dashboard

Read `brain/projects/README.md` to get the master project list, statuses, and priorities.

### Step 2: Read All Individual Project Files

Use Glob to find all `.md` files in `brain/projects/` (excluding README.md and _TEMPLATE.md):

```
brain/projects/*.md
```

Read each project file to extract:
- Project name
- Status (Not Started, In Progress, On Track, Paused, Behind, Done)
- Priority (High, Medium, Low)
- Current milestone or phase
- Next action item
- Blockers or risks
- Last updated date
- Any deadlines

### Step 3: Read Today's Context

If available, read:
- `brain/goals.md` — To check project alignment with quarterly goals
- `brain/daily/{today's date}.md` — To see what was planned for today
- `brain/calendar/` — To check any upcoming deadlines

### Step 4: Classify Each Project

Assign each project a health indicator:

| Health | Criteria |
|--------|----------|
| ON TRACK | Active work happening, no blockers, on schedule |
| NEEDS ATTENTION | Slipping slightly, minor blockers, or no update in 5+ days |
| BEHIND | Past deadline, significant blockers, or paused when it should be active |
| BLOCKED | Cannot progress — waiting on something external |
| PAUSED | Intentionally paused (not a problem unless it conflicts with goals) |
| DONE | Completed — acknowledge and archive |

### Step 5: Identify Today's Action Items

From all active projects, pull out:
1. Items that are due today or overdue
2. Items flagged as "next action" in project files
3. High-priority projects that have not been updated recently
4. Any project whose status conflicts with its priority (e.g., High priority but Paused)

### Step 6: Check Goal Alignment

Compare active projects against the current quarterly goals from `brain/goals.md`:
- Flag any goal that has no project actively supporting it
- Flag any project that does not clearly map to a goal
- Highlight if effort is concentrated on lower-priority items while high-priority goals are unsupported

### Step 7: Generate the Pulse Report

Compile everything into a concise, scannable report.

## Output Format

```
PROJECT PULSE — {date}
========================================

OVERALL: {X} active projects | {Y} need attention | {Z} behind

HEALTH DASHBOARD:
-----------------
{status icon} {Project Name} [{priority}]
   Status: {status} | Last Updated: {date}
   Next: {next action}
   {blocker note if any}

{status icon} {Project Name} [{priority}]
   Status: {status} | Last Updated: {date}
   Next: {next action}

... (all projects listed, sorted by priority then health)

NEEDS ATTENTION NOW:
--------------------
1. {Project} — {why it needs attention} — {recommended action}
2. {Project} — {why} — {action}

BEHIND SCHEDULE:
----------------
1. {Project} — was due {date} — {what's holding it up}

GOAL ALIGNMENT:
---------------
{goal 1}: Supported by {Project A, Project B} — {on track / gap}
{goal 2}: Supported by {Project C} — {on track / gap}
{goal 3}: NO ACTIVE PROJECT — needs attention

TODAY'S PRIORITY ACTIONS:
-------------------------
1. {action} on {project} — {why today}
2. {action} on {project} — {why today}
3. {action} on {project} — {why today}

========================================
```

### Health Icons (for text output):

| Icon | Meaning |
|------|---------|
| [OK] | On Track |
| [!!] | Needs Attention |
| [BEHIND] | Behind Schedule |
| [BLOCKED] | Blocked |
| [PAUSED] | Intentionally Paused |
| [DONE] | Completed |

## Example Usage

**User:** "Pulse check"

**AI:** Reads all project files, generates the full pulse report showing 6 active projects, 2 needing attention, 1 behind schedule. Highlights that SellFi is behind its March deadline and deal flow has been paused too long. Recommends 3 priority actions for today.

**User:** "What needs my attention today?"

**AI:** Scans projects, daily log, and goals. Surfaces the 3 most urgent items across all projects with recommended actions.

**User:** "Project status"

**AI:** Full dashboard view of all projects with health indicators, sorted by priority.

**User:** "What's on fire?"

**AI:** Filters to only BEHIND and BLOCKED projects, explains why each is critical, and recommends immediate actions.

**User:** "Am I working on the right things?"

**AI:** Compares active project effort against quarterly goals, identifies misalignment, and recommends reprioritization if needed.

## Error Handling

- **If `brain/projects/README.md` does not exist:** Report: "No project dashboard found at `brain/projects/README.md`. You don't have any projects tracked yet. Want me to set up the project tracking structure?"
- **If `brain/projects/` contains no project files (only README.md and _TEMPLATE.md):** Report: "Your project dashboard exists but has no active projects. Add projects to `brain/projects/README.md` or create project files to start tracking."
- **If `brain/goals.md` does not exist:** Skip the goal alignment check and note: "I couldn't find `brain/goals.md`, so I skipped the goal alignment analysis. Create a goals file to enable this feature."
- **If `brain/daily/` directory does not exist or has no log for today:** Skip today's context and note: "No daily log found for today. The pulse check is based on project files and goals only."
- **If a project file is malformed or missing expected fields (status, priority, etc.):** Include it in the report with a flag: "Could not parse status/priority for '{project name}'. The file may need reformatting. Skipping health classification for this project."
- **If the user asks for a pulse check but there are no projects behind or needing attention:** Report the positive news: "All {N} projects are on track. No blockers, no overdue items. Here's the full dashboard anyway."
- **If `brain/calendar/` files reference deadlines that projects do not reflect:** Flag the mismatch: "The calendar shows a deadline for '{item}' on {date}, but no project is tracking this. Is this still relevant?"
- **If Glob finds too many .md files in `brain/projects/` (over 50):** Process them all but present a condensed summary, grouping by status and priority rather than listing every project individually.


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
