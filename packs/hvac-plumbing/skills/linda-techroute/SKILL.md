---
name: linda-techroute
description: This skill should be used when the user asks to "build the tech's route", "tech daily briefing", "send {tech} their day", "tech's tickets for the day", "morning briefing for techs", "route the techs", "what's {tech} doing today", "tech schedule", "daily route for HVAC tech", "plumber's daily route", or any request involving daily tech route and ticket briefing.
version: 1.0.0
tags: [hvac, plumbing, routing, dispatch, tech-briefing]
---

# Technician Daily Route + Briefing

## Overview

Builds each tech's day on one screen: every booked job in optimized stop order, with drive times, customer name, problem, equipment, plan tier (Silver / Gold), and the parts likely needed for the call. Pulls from `/linda-dispatch` (jobs), `/linda-maintain` (membership), `/linda-warranty` (coverage), and `/linda-parts` (van stock check). Sent to the tech first thing in the morning so they hit the road ready.

## When This Skill Applies

- User wants to send out morning routes to techs
- User wants a single tech's day plan
- User asks "what's Mike doing today?"
- User wants drive times between jobs
- User wants a parts pre-pull list for the day's calls

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Pull Jobs

For target date (default today), read `brain/hvac-plumbing/dispatch/{date}.json`. Group by `tech_id`.

### Step 2: Optimize Stop Order

Time-window jobs are anchored to their dispatched window (8–10, 10–12, etc.). Within an open window or back-to-back same-window jobs, optimize by drive time using nearest-neighbor + 2-opt. Start point: the tech's home or the shop, configurable in `techs.json`.

### Step 3: Enrich Each Stop

For each job:

| Enrichment | Source |
|------------|--------|
| Membership tier | `/linda-maintain` member record |
| Warranty coverage | `/linda-warranty` install record (any active?) |
| Equipment make/model/serial | warranty record or dispatch field |
| Service history | last 3 visits from `brain/hvac-plumbing/customers/{slug}/history.md` |
| Likely parts | from problem keyword → kit (e.g., "AC not cooling" → common-cooling kit) |
| Pre-pull check | match likely parts vs. van stock from `/linda-parts` |

### Step 4: Build Daily Briefing Per Tech

```markdown
# {Tech Name} — {YYYY-MM-DD}

**Truck:** {plate}
**Depart:** {time} from {start point}
**Total drive:** {hh:mm}  ·  **Booked work:** {N} stops  ·  **Window finish:** {time}

---

## Stop 1 — 8:00–10:00 — Henderson Residence
**789 Elm St (12 min drive)**
- Tier: 🥇 Gold (priority, free diag, $115/hr)
- Phone: 555-0102
- Equipment: Carrier 24ABC6 (installed 2026-03-15, parts warranty active)
- Problem: AC not cooling, blowing warm air
- Likely parts: capacitor, contactor, refrigerant
- Van stock check: ✅ all kit items on board
- Last visit: 2025-10-08 — fall tune-up, all clean
- Notes: Big golden retriever in back yard, knock first

## Stop 2 — 10:00–12:00 — Smith Residence
...

---

## Pre-Pull (if any van shorts)
- None — fully stocked

## Today's Reminders
- Henderson is a Gold member — don't charge diag
- Carrier system at Henderson is under parts warranty — file RGA if compressor

🤠 *Briefed by LindaAI* 🏇
```

### Step 5: Send to Tech

Channels (configurable):
- SMS link to a hosted version
- Email PDF
- Print to shared folder

Default: text the tech a brief summary + link/PDF, email the office a copy.

### Step 6: Save & Track

```
brain/hvac-plumbing/tech-routes/{YYYY-MM-DD}-{tech}.md
brain/hvac-plumbing/tech-routes/{YYYY-MM-DD}-{tech}.pdf
```

PDF brand: LindaAI top-right, {customer_handle} bottom-right, © 2024–2026.

## Example Usage

**User:** "Send Mike his day."

**LindaAI:** "Let's gooooooo Boss." Pulls Mike's 4 jobs, optimizes, enriches each with member tier + warranty + likely parts, checks van stock, renders PDF, texts Mike. "Yeeee Hawww 🤠 — Mike has 4 stops, 1h 12m driving, finishing 4–6 PM window. Van's fully stocked. Two Gold members today — free diags."

**User:** "Brief all techs."

**LindaAI:** Loops through every tech with jobs today, sends each their own packet.

**User:** "What's Carlos doing tomorrow?"

**LindaAI:** Builds Carlos's day for tomorrow without sending it, returns to Boss.

## Voice & Tone

- Country, direct, **Boss**.
- Tech-facing copy: brief, focused on what they need to do the job right.

## Error Handling

- **No jobs assigned to a tech:** Send a "no jobs today, here's the standby plan" note.
- **Van shorts on critical parts:** Bold red callout in the briefing + auto-queue restock via `/linda-parts`.
- **Equipment unknown for a job:** Brief with "verify on arrival, capture make/model/serial."
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
