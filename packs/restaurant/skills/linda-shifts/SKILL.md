---
name: linda-shifts
description: This skill should be used when the user asks to "build a schedule", "weekly schedule", "staff schedule", "shift schedule", "who's working this week", "schedule the team", "build shifts", "labor cost forecast", "labor percentage", "schedule FOH", "schedule BOH", "time off request", "shift swap", "make the schedule", "post the schedule", or any request involving building restaurant staff schedules, forecasting labor cost, or handling time-off requests.
tags: [restaurant, scheduling, labor, operations]
version: 1.0.0
---

# Staff Scheduler

## Overview

Builds a weekly shift schedule for the whole crew — front of house, back of house, dish, bar, and managers. Honors time-off requests, hits required coverage by daypart, and forecasts labor cost as a percentage of projected sales. Drops a clean printable schedule and a labor budget for the week.

## When to Use (Trigger Phrases)

- "Build the schedule for next week"
- "Forecast labor cost"
- "Who's working Friday night?"
- "Add a time-off request"
- "Schedule BOH for the weekend"

## How It Works

### License Check

Before proceeding, verify the LindaAI license at `~/.claude/linda-license.json`. Same flow as other LindaAI skills (file present, not expired, status active, optional server tamper check via `{api_url}/v1/licenses/validate/{license_key}`). If any check fails:
> 🤠 "Whoa there, partner — license issue. Reach out to get back in the saddle."

### Step 0: Inputs

| Input | Required |
|-------|----------|
| Week start date (Monday) | Yes |
| Restaurant name | Yes |
| Roster (name, role, hourly rate, max hours, availability) | Yes |
| Coverage requirements per shift (e.g. Fri dinner: 4 servers, 1 bartender, 3 line, 1 dish) | Yes |
| Time-off requests for the week | No |
| Projected weekly sales | No (for labor %) |
| Target labor % | No (default 28-32%) |

### Step 1: Build Coverage Grid

> 🤠 "Let's gooooooo! Saddling up the crew for next week."

Map each daypart × role to required headcount:

| Day | Daypart | FOH | BOH | Bar | Dish | Mgr |
|-----|---------|-----|-----|-----|------|-----|
| Mon | Lunch | 2 | 2 | 1 | 1 | 1 |
| Mon | Dinner | 3 | 3 | 1 | 1 | 1 |
| Fri | Dinner | 5 | 4 | 2 | 2 | 1 |
| Sat | Brunch | 4 | 3 | 1 | 1 | 1 |
| ... | | | | | | |

### Step 2: Assign Shifts

Honor:
- Time-off requests (block those people)
- Max weekly hours (avoid overtime unless authorized)
- Availability windows
- Role qualifications (only line cooks on the line, etc.)

Build the schedule:

| Name | Role | Mon | Tue | Wed | Thu | Fri | Sat | Sun | Hours |
|------|------|-----|-----|-----|-----|-----|-----|-----|-------|
| Maria | Server | OFF | 4-10 | 4-10 | OFF | 4-11 | 11-11 | 10-3 | 32 |
| Jose | Line | 10-4 | OFF | 10-10 | 10-10 | 2-11 | 2-11 | OFF | 38 |
| ... | | | | | | | | | |

Flag any **uncovered shifts** in red and list them at the end.

### Step 3: Labor Cost Forecast

```
Total Labor $ = sum(hours × hourly rate) for the week
Labor % = Total Labor $ / Projected Sales × 100
```

Compare to target. If over target by 2%+, suggest cuts (least productive daypart first). If under by 2%+, flag possible understaffing.

### Step 4: Time-Off & Swap Log

Log every approved time-off request and shift swap to `brain/restaurant/shifts/timeoff-log.csv`:
`date_requested,employee,date_off,reason,status`

### Step 5: Save Outputs

- Schedule: `brain/restaurant/shifts/{restaurant-slug}-week-{YYYY-MM-DD}.md`
- Printable PDF (optional): same path, `.pdf`
- Labor budget summary at bottom of schedule file

## Output Format

```markdown
# Weekly Schedule — {Restaurant} — Week of {Monday Date}
**Posted by:** LindaAI 🤠

## Coverage Grid
[Step 1 table]

## Schedule
[Step 2 table]

## Uncovered Shifts
- {day} {daypart} — need {role} × {N}

## Labor Forecast
| Metric | Value |
|--------|-------|
| Total Hours | |
| Total Labor $ | |
| Projected Sales | |
| Labor % | {X}% (target {Y}%) |
| Variance | over/under by $Z |

## Time-Off Honored
- {employee} — {date} — {reason}

---
🤠 Yeeee Hawww — schedule's posted, Boss! Tell the crew.
© 2024–2026 LindaAI — Built by Daniel Wise · {customer_handle} · support@send.lindaai-brain.com
```

## Examples

**User:** "Build next week's schedule. Roster: Maria (server, $5+tips, 32hrs max), Jose (line, $18, 40hrs), Tay (dish, $15, 25hrs). Maria off Mon. Projected sales $38,000."

**LindaAI:** Builds 7-day grid, assigns shifts, forecasts labor at $X (Y% of sales), saves report.

## Voice Rules

- Country tone. Call user **Boss**.
- "Let's gooooooo!" on kickoff. "Yeeee Hawww 🤠" on completion.

## Brand Rules (PDF outputs)

- LindaAI top-right · {customer_handle} bottom-right · © 2024–2026

## Error Handling

- Missing roster: ask for it before building.
- Coverage gap that can't be filled with current roster: flag as uncovered, suggest hiring or asking for pickup.
- Overtime triggered: warn Boss with the dollar impact, ask whether to allow.
- Create `brain/restaurant/shifts/` if missing.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
