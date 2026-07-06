---
name: linda-schedule
description: This skill should be used when the user asks to "build a schedule", "project schedule", "construction schedule", "look ahead", "3 week look ahead", "two week look ahead", "critical path", "milestones", "update the schedule", "schedule delay", "Gantt", "baseline schedule", "am I on schedule", "schedule variance", "what's on the critical path", "phase the work", or any request involving building, updating, or reporting on a construction project schedule.
version: 1.0.0
tags: [construction, scheduling, critical-path, look-ahead, project-management]
---

# Project Scheduler

## Overview

Builds and maintains the project schedule — the backbone every other part of the job hangs on. LindaAI turns a list of activities into a sequenced schedule with durations, dependencies, and milestones; identifies the critical path (the chain that, if it slips, slips the whole job); generates the weekly look-ahead the field actually uses; and tracks variance so delays are caught early instead of explained late.

## When This Skill Applies

- User says "build a schedule" or "schedule out {project}"
- User wants a 2- or 3-week look-ahead for the field/subs
- User asks "what's on the critical path" or "am I on schedule"
- User needs to log a delay and see its impact
- User wants milestones or to update an existing schedule

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Capture Activities
For each task: name, duration (days), predecessor(s), trade/responsible, and whether it's a milestone.
| ID | Activity | Days | Depends On | Trade | Milestone |
|----|----------|------|-----------|-------|-----------|
| 10 | Foundation pour | 5 | 5 (excavation) | Concrete | — |
| 20 | Framing | 12 | 10 | Carpentry | — |
| 30 | Dry-in | 3 | 20 | — | ✅ Weather-tight |

### Step 2: Sequence & Critical Path
- Compute start/finish dates from durations + dependencies.
- Identify the **critical path** — the longest dependent chain (zero float). Call it out explicitly: "Foundation → Framing → Dry-in → MEP rough is your critical path; protect these dates."
- Note near-critical chains (low float) that could become critical.

### Step 3: Look-Ahead (the field tool)
On request, produce a **2- or 3-week look-ahead**: every activity starting or active in the window, by date, with the responsible trade — the sheet you hand subs at the weekly coordination meeting.

### Step 4: Track Variance
- "Am I on schedule?" → compare actual % complete vs planned; list activities behind, critical ones first.
- Log a delay (cause: weather / RFI / sub / material / owner) and show downstream impact on the finish date.
- Flag when a delay's root cause is a slow RFI or owner decision → that's often a **time-impact / change-order** basis.

## Hard Rules
- Always identify and protect the **critical path** — that's where schedule is won or lost.
- A delay isn't "logged" until its downstream impact on the finish date is shown.
- Tie delays to a documented cause (RFI #, weather day, change) so they're defensible.

## Handoffs
- Delay caused by RFI/owner → **linda-changeorder** (time-impact basis) + note in **linda-rfi**
- Daily progress that feeds the schedule → **linda-dwr** (daily work report)
- Schedule status for the owner → **linda-projecttrack / linda-mail**

---
*LindaAI Construction PM Pack — Built by Daniel Wise*
