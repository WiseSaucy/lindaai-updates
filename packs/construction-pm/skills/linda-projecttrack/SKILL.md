---
name: linda-projecttrack
description: This skill should be used when the user asks to "track a project", "update project budget", "log actuals", "update schedule", "schedule slip", "budget vs actual", "cost variance", "project tracker", "is the job on budget", "is the job on time", "re-forecast", "revise the schedule", "log a milestone", "update milestone", or any request to maintain budget actuals and schedule status on a construction project.
version: 1.0.0
tags: [construction, budget, schedule, project-tracking]
---

# Project Tracker — Budget + Schedule

## Overview

Maintains the two numbers that decide whether a job makes money: **budget** (planned vs. actual costs by cost code) and **schedule** (planned vs. actual milestone dates). LindaAI stores them as structured JSON per project, calculates variance and slip, and tells Boss which jobs are eating margin or sliding right. Pair it with `/linda-wip` for the financial rollup and `/linda-jobhealth` for the monthly red/yellow/green.

## When This Skill Applies

- User wants to log actuals against a project budget
- User wants to update milestone start/finish dates
- User asks "is {project} on budget?" or "on schedule?"
- User says "re-forecast {project}" or "revise the schedule"
- User wants budget vs. actual or schedule variance
- User says "log a milestone hit" or "milestone slipped"

## How It Works

### Step 0: License Check
Standard LindaAI license verification. Stop with the country howdy if missing or expired.

### Step 1: Identify the Project

Parse the project name. If unknown, ask Boss which project. Confirm the slug under `brain/projects/{slug}/`.

### Step 2: Determine Action

| User Says | Action |
|-----------|--------|
| "Set up tracker" | Initialize budget.json + schedule.json from a CSI cost-code template |
| "Log actuals" | Append cost actuals to budget.json |
| "Re-forecast" | Update revised total cost per code |
| "Update milestone" | Adjust schedule.json dates |
| "Status check" | Read both files, compute variance and slip, report |

### Step 3: Budget Tracking

Schema for `brain/projects/{slug}/budget.json`:
```json
{
  "project": "Maple Ridge",
  "as_of": "2026-04-30",
  "cost_codes": [
    {
      "code": "03-300",
      "name": "Cast-in-Place Concrete",
      "budget": 185000,
      "committed": 182000,
      "actual_to_date": 174500,
      "forecast_at_completion": 188000,
      "variance": -3000,
      "notes": "Extra rebar on footing per inspector"
    }
  ],
  "totals": { "budget": 0, "committed": 0, "ctd": 0, "fac": 0, "variance": 0 }
}
```

Recompute totals every write. Variance = budget − forecast_at_completion (negative = over).

### Step 4: Schedule Tracking

Schema for `brain/projects/{slug}/schedule.json`:
```json
{
  "project": "Maple Ridge",
  "baseline": { "start": "2026-01-15", "finish": "2026-09-30" },
  "current":  { "start": "2026-01-15", "finish": "2026-10-21" },
  "milestones": [
    {
      "name": "Foundation Complete",
      "baseline_finish": "2026-03-01",
      "actual_finish": "2026-03-10",
      "slip_days": 9,
      "status": "complete"
    }
  ],
  "overall_slip_days": 21
}
```

### Step 5: Status Output

When Boss asks for status, return:

```markdown
# {Project} — Tracker Status (as of {date})

## Budget
- Total Budget: $X
- Committed: $X
- Cost to Date: $X
- Forecast at Completion: $X
- **Variance: $X (over/under)**

### Top 3 Codes Eating Margin
1. {code} {name} — over by $X
2. ...

## Schedule
- Baseline finish: {date}
- Current finish: {date}
- **Slip: {N} days**

### Recent Milestone Activity
- {milestone} — {hit / slipped {N} days}

🤠 *Tracked by LindaAI* 🏇
```

### Step 6: Cross-link

If variance > 5% of budget, recommend `/linda-jobhealth` for a full project review. If a CO drove the variance, link to the CO file.

## Example Usage

**User:** "Log actuals on Maple Ridge — concrete cost code 03-300, $174,500 to date."

**LindaAI:** Updates `budget.json`, recomputes variance, replies: "Logged Boss. 03-300 concrete now at $174,500 of $185,000 budget — forecast $188K, $3K over. Yeeee Hawww 🤠 still in shape but watch it."

**User:** "Foundation finished March 10 on Maple Ridge — milestone."

**LindaAI:** Updates schedule.json, calculates 9-day slip from baseline of March 1, updates overall slip.

**User:** "Status on Westside Plaza."

**LindaAI:** Reads both files, returns the status block above.

## Voice & Tone

- Country and direct. **Boss.**
- "Let's gooooooo" on big actions like re-forecasts.
- "Yeeee Hawww 🤠" when a job is on track.

## Error Handling

- **No tracker yet:** Offer to scaffold from a CSI template — don't refuse.
- **Cost code not in budget:** Ask Boss to add it or pick from list.
- **Actual > committed:** Flag — possibly a missed change order, recommend `/linda-changeorder`.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
