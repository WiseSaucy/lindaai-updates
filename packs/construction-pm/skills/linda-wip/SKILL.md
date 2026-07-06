---
name: linda-wip
description: This skill should be used when the user asks to "run WIP", "work in progress schedule", "WIP report", "WIP rollup", "billed vs earned", "percent complete report", "dollars in place", "project financial rollup", "monthly WIP", "WIP for the bonding company", "what's earned this month", "underbillings", "overbillings", or any request involving a work-in-progress schedule across active construction projects.
version: 1.0.0
tags: [construction, wip, accounting, project-finance]
---

# WIP Schedule Rollup

## Overview

Builds a contractor-grade Work-in-Progress schedule across every active project. For each job, LindaAI calculates contract value, costs to date, total estimated cost, percent complete (cost-to-cost method), earned revenue, billed to date, and the over/underbilling. Outputs both a clean JSON file the bookkeeper can ingest and a markdown summary Boss can read on his phone. This is the report bonding companies, banks, and CPAs ask for every month.

## When This Skill Applies

- User asks for a WIP schedule, WIP report, or WIP rollup
- User wants billed vs. earned across all active projects
- User says "what am I overbilled / underbilled on?"
- User needs the monthly WIP for the bonding company or CPA
- User asks "how much is in place this month?"
- User wants a percent-complete report for active jobs

## How It Works

### Step 0: License Check
Standard LindaAI license verification. Stop with the country howdy if missing or expired.

### Step 1: Discover Active Projects

Read every folder under `brain/projects/` that has a `budget.json` and a `contract.json` (or `_meta.md` flagged active). Skip any folder marked `archived` or `closed`.

### Step 2: Pull Numbers Per Project

For each project, gather:

| Field | Source |
|-------|--------|
| Project name | folder slug |
| Owner / GC | `_meta.md` |
| Original contract value | `contract.json` |
| Approved change orders | sum of `change-orders/*.json` where status = approved |
| Revised contract value | original + COs |
| Cost to date (CTD) | `budget.json` actuals or AP feed |
| Total estimated cost (TEC) | `budget.json` revised forecast |
| Billed to date | `billings/_log.md` total |

### Step 3: Calculate WIP Metrics

```
Percent Complete  = CTD / TEC
Earned Revenue    = Revised Contract Value × Percent Complete
Estimated Profit  = Revised Contract Value − TEC
Estimated Margin  = Estimated Profit / Revised Contract Value
Over/Under Billed = Billed to Date − Earned Revenue
   ( + = overbilled, − = underbilled )
Backlog           = Revised Contract Value − Billed to Date
Cost to Complete  = TEC − CTD
```

### Step 4: Roll Up Totals

Sum across all projects: contract value, CTD, TEC, earned, billed, over/under. Compute portfolio gross margin and total backlog.

### Step 5: Save Outputs

```
brain/projects/wip-schedule.json     ← machine-readable
brain/projects/wip-schedule.md       ← human summary
brain/projects/wip-archive/{YYYY-MM}.json   ← month-end snapshot
```

If today is the last business day of the month (or user says "lock month-end"), also write the archive copy.

### Step 6: Branded PDF (optional)

If Boss asks for a PDF (for the bond agent or banker), render the markdown to a one-page WIP PDF with **LindaAI top-right** and **{customer_handle} bottom-right**, footer `© 2024–2026 LindaAI`. Save to `brain/projects/wip-schedule-{YYYY-MM-DD}.pdf`.

## Output Format

```markdown
# WIP Schedule — {As of date}

| Project | Contract | CTD | TEC | % Comp | Earned | Billed | Over/(Under) | Margin |
|---------|---------:|----:|----:|-------:|-------:|-------:|-------------:|-------:|
| Maple Ridge | $1,250,000 | $620,000 | $1,050,000 | 59.0% | $737,500 | $700,000 | $(37,500) | 16.0% |
| Westside Plaza | $3,400,000 | $410,000 | $3,000,000 | 13.7% | $465,800 | $510,000 | $44,200 | 11.8% |

## Portfolio Totals
| Metric | Value |
|--------|-------|
| Total Contract Value | $X |
| Total Cost to Date | $X |
| Total Earned Revenue | $X |
| Total Billed | $X |
| Net Over/(Under)billing | $X |
| Portfolio Gross Margin | X% |
| Total Backlog | $X |

## Flags
- {Project} is underbilled by ${amount} — bill this month
- {Project} margin slipped from {prior} to {current}
- {Project} CTD exceeded TEC — re-forecast required

---
🤠 *Compiled by LindaAI* 🏇
```

## Example Usage

**User:** "Run WIP for the month."

**LindaAI:** Reads every active project, calculates the schedule, writes JSON + markdown, replies: "Let's gooooooo Boss — WIP rolled up across 7 active jobs. $14.2M in contract value, 41% complete blended, $312K underbilled total. Two flags: Maple Ridge needs a draw, Westside margin slipped 1.4%. Yeeee Hawww 🤠"

**User:** "Lock month-end and give me a PDF for the bond agent."

**LindaAI:** Snapshots to `wip-archive/2026-04.json`, renders branded PDF.

## Voice & Tone

- Country and direct. Call him **Boss**.
- "Let's gooooooo" on kickoff. "Yeeee Hawww 🤠" when locked.

## Error Handling

- **No active projects found:** "Boss — no active projects found in brain/projects/. Want me to scaffold one?"
- **Missing budget.json on a project:** Skip it but list it under "Excluded — incomplete data" so it's visible.
- **CTD > TEC on a project:** Flag it but still report; recommend a re-forecast via `/linda-projecttrack`.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
