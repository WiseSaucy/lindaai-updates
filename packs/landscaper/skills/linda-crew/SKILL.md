---
name: linda-crew
description: This skill should be used when the user asks to "dispatch the crew", "assign crews", "send the crew their jobs", "crew dispatch", "build today's job sheet", "send out routes", "text the crew their day", "crew assignments", "who's doing what today", "assign jobs to crews", "balance the crews", or any request to assign and dispatch landscaping crews to their daily work.
version: 1.0.0
tags: [landscaping, dispatch, crew-management, field-ops]
---

# Crew Dispatch

## Overview

Assigns crews to jobs for the day, builds each crew's job sheet (route + scope + notes per stop), and sends it to them via text or email. Pulls today's work from the optimized route (`/linda-route`) and the property cards (`/linda-propcard`). One command, every crew has their day.

## When This Skill Applies

- User says "dispatch the crews" or "send the crews their day"
- User wants to assign jobs to crews for a specific day
- User asks "who's doing what today?"
- User wants to balance workload across crews
- User wants to send today's route + scope to a specific crew

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Determine Date & Crews

- Date defaults to today
- Read `brain/landscaper/crews.json`:
```json
{
  "crews": [
    { "id": "C1", "name": "Crew 1", "lead": "Miguel", "phone": "555-...", "size": 3, "truck": "F-250 #1" },
    { "id": "C2", "name": "Crew 2", "lead": "James", "phone": "555-...", "size": 2, "truck": "F-150 #2" }
  ]
}
```

### Step 2: Pull Today's Stops

Source priority:
1. `brain/landscaper/routes/{YYYY-MM-DD}-{crew}.md` (already optimized)
2. Otherwise, recurring stops from property cards where `service_day = today`
3. Plus any one-off jobs from `brain/landscaper/jobs/{YYYY-MM-DD}.md`

### Step 3: Auto-Balance (if requested)

If Boss says "balance the crews," distribute stops by total estimated minutes (drive + on-site) to even loads ±10%. Respect existing assignments on property cards unless told to override.

### Step 4: Build Per-Crew Job Sheet

For each crew:

```markdown
# {Crew Name} — {YYYY-MM-DD}

**Lead:** {name}  ·  **Truck:** {truck}  ·  **Depart yard:** {time}

| # | Time | Property | Address | Service | Notes |
|---|------|----------|---------|---------|-------|
| 1 | 7:18 | Maple HOA | 123 Main | Mow + edge + blow | Gate code 1234 |
| 2 | 8:08 | Smith Residence | 456 Oak | Mow only | Big dog — knock |

**Special supplies needed today:** {list any beyond standard kit}
**Estimated finish:** {time}

🤠 LindaAI 🏇
```

### Step 5: Send

Channels (configurable in `brain/landscaper/config.md`):
- SMS via the email-to-SMS gateway or any installed SMS tool
- Email via existing email tool
- Print to a shared folder for paper crews

Default: text the lead + email the office. Confirm to Boss what was sent where.

### Step 6: Save Dispatch Record

```
brain/landscaper/dispatch/{YYYY-MM-DD}.md
```

Index of which crew got which stops, with timestamps of dispatch.

## Output Format

Boss sees:

```markdown
# Dispatch — {YYYY-MM-DD}

| Crew | Lead | Stops | Drive | On-site | Finish | Status |
|------|------|------:|------:|--------:|-------:|--------|
| C1   | Miguel | 12 | 1:35 | 5:50 | 3:25 PM | Sent ✅ |
| C2   | James  | 9  | 1:10 | 4:30 | 2:40 PM | Sent ✅ |

## Today's Special
- Mulch delivery to yard 8:00 — Crew 1 loads first
- Henderson called about the gate — code now 5567

🤠 *Dispatched by LindaAI* 🏇
```

## Example Usage

**User:** "Dispatch the crews."

**LindaAI:** "Let's gooooooo Boss." Pulls routes, builds sheets, texts leads, emails office, saves dispatch log. "Yeeee Hawww 🤠 — Crew 1 has 12 stops, Crew 2 has 9. Both off the lot by 7. Both home by 3:30."

**User:** "Add Mrs. Henderson to Crew 1 today."

**LindaAI:** Inserts the stop, re-optimizes Crew 1's route, sends an updated job sheet.

**User:** "Balance the crews — Crew 1 always finishes 2 hours after Crew 2."

**LindaAI:** Re-distributes, shows the new load split.

## Voice & Tone

- Country, direct, **Boss**.
- Brief and crew-friendly when texting leads — no fluff, just the day.

## Error Handling

- **Crew has no phone on file:** Ask Boss once, save to `crews.json`.
- **No routes built yet:** Run `/linda-route` first or offer to do it inline.
- **Stop has no service-day assignment:** List as "unassigned" and ask Boss to place it.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
