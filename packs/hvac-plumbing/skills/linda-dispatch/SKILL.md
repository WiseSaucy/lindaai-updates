---
name: linda-dispatch
description: This skill should be used when the user asks to "book a service call", "dispatch a tech", "schedule a job", "new service call", "book a repair", "assign a tech", "customer needs service", "book {customer}", "schedule maintenance visit", "emergency call", "send confirmation to customer", "dispatch board", or any request involving HVAC or plumbing job booking and tech assignment.
version: 1.0.0
tags: [hvac, plumbing, dispatch, scheduling]
---

# Job Dispatch

## Overview

Books incoming HVAC and plumbing service calls. LindaAI captures the customer info, problem description, urgency, and equipment, finds the next available tech for the right skill set and zone, books the time slot, and fires off a confirmation to the customer with the window and the tech's name. Updates the dispatch board and feeds straight into `/linda-techroute` for the tech's daily plan.

## When This Skill Applies

- Customer calls or messages with a service need
- User says "book a service call for {customer}"
- User wants to assign a tech to a job
- User wants to send a confirmation text/email to a customer
- User asks "what's open on the board today?"

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Capture Job Info

| Field | Required |
|-------|----------|
| Customer name | yes — look up in `brain/hvac-plumbing/customers/` |
| Phone | yes |
| Address | yes |
| Trade | HVAC / Plumbing / Both |
| Problem | yes — plain-language |
| Urgency | Emergency / Same-day / Next-day / Scheduled |
| Equipment make/model | if known |
| Maintenance plan member? | check `/linda-maintain` records |

### Step 2: Pick the Slot

Read `brain/hvac-plumbing/dispatch/{YYYY-MM-DD}.json`. Find the next slot that:
- Matches required trade
- Has a tech with the right skill (read `techs.json` skill tags)
- Is in the customer's zone
- Maintenance-plan members get priority

Default windows: 8–10 AM, 10 AM–noon, noon–2 PM, 2–4 PM. Emergencies override the queue.

### Step 3: Assign a Tech

Tech roster `brain/hvac-plumbing/techs.json`:
```json
{
  "techs": [
    { "id": "T1", "name": "Mike", "phone": "555-...", "trade": ["HVAC"], "skills": ["mini-split","heat-pump","gas-furnace"], "zone": "north" },
    { "id": "T2", "name": "Carlos", "phone": "555-...", "trade": ["Plumbing"], "skills": ["water-heater","drain","gas"], "zone": "south" }
  ]
}
```

Choose by zone proximity → skill match → load balance.

### Step 4: Save the Booking

```json
{
  "ticket_id": "JOB-{YYYYMMDD}-{NNN}",
  "customer": "...",
  "address": "...",
  "phone": "...",
  "trade": "HVAC",
  "problem": "AC not cooling, blowing warm air",
  "urgency": "same-day",
  "scheduled_date": "2026-04-30",
  "window": "10:00–12:00",
  "tech_id": "T1",
  "tech_name": "Mike",
  "equipment": "Carrier 24ABC6 split system",
  "membership": "Gold",
  "status": "scheduled",
  "created": "2026-04-30T08:14:00",
  "notes": []
}
```

Append to:
```
brain/hvac-plumbing/dispatch/{YYYY-MM-DD}.json
```

### Step 5: Confirmation to Customer

Send via configured channel (SMS / email):

> "Hi {Name} — this is {Company}. We've got you booked for {date} between {window}. Your tech is **{tech name}**. He'll call when he's about 30 minutes out. Reply STOP to cancel. Yeeeyup, see you then. — {Company}"

Save copy to `brain/hvac-plumbing/customers/{slug}/confirmations/{ticket}.md`.

### Step 6: Update Dispatch Board

Boss sees the live board on request:

```markdown
# Dispatch Board — {YYYY-MM-DD}

| Time | Tech | Customer | Address | Trade | Urgency | Status |
|------|------|----------|---------|-------|---------|--------|
| 8–10 | Mike | Smith | 123 Oak | HVAC | scheduled | confirmed |
| 10–12 | Mike | Henderson | 789 Elm | HVAC | same-day | en route |
| 10–12 | Carlos | Jones | 456 Pine | Plumbing | scheduled | confirmed |

🤠 *Dispatched by LindaAI* 🏇
```

## Example Usage

**User:** "Book Mrs. Henderson, 789 Elm, AC not cooling, same-day. She's a Gold member."

**LindaAI:** "Let's gooooooo Boss." Finds 10–12 slot with Mike (HVAC, north zone), books JOB-20260430-007, fires confirmation text. "Yeeee Hawww 🤠 — Henderson booked 10–12 with Mike. Confirmation text sent."

**User:** "Emergency — burst pipe at 1100 W Main."

**LindaAI:** Bumps the next plumbing slot, dispatches Carlos immediately, alerts the customer who got bumped with apology + reschedule offer.

**User:** "Show today's board."

**LindaAI:** Returns the table.

## Voice & Tone

- Country, direct, **Boss**.
- Customer confirmations: warm and clear, never robotic.

## Error Handling

- **No techs available in window:** Offer next available slot, ask if Boss wants to overflow to the next day or push another job.
- **Customer unknown:** Capture and create a customer record on the fly.
- **No phone for confirmation:** Ask, but still book the job.
- **Maintenance plan lookup fails:** Default to non-member and flag for Boss to verify.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
