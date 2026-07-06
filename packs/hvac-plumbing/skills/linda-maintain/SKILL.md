---
name: linda-maintain
description: This skill should be used when the user asks to "track maintenance plans", "maintenance contracts", "tune-up reminders", "service agreement", "annual maintenance", "MSA", "club members", "Silver Gold members", "schedule tune-ups", "renewal reminders", "who's due for a tune-up", "maintenance plan tracker", "enroll customer in plan", or any request involving recurring HVAC or plumbing maintenance contract management.
version: 1.0.0
tags: [hvac, plumbing, maintenance, recurring-revenue, retention]
---

# Maintenance Contract Tracker

## Overview

Tracks every customer on a recurring maintenance plan — Silver / Gold — and the systems each plan covers. LindaAI knows when each tune-up is due, when each plan renews, who's overdue, who's expired, and who's a candidate to enroll. Generates the reminder texts, schedules the tune-up visits via `/linda-dispatch`, and renders renewal notices. This is the recurring-revenue spine of the business.

## When This Skill Applies

- User wants to enroll a new customer in a plan
- User asks "who's due for a tune-up this month?"
- User asks "whose plan is up for renewal?"
- User wants to send out spring/fall tune-up reminders
- User wants the count of active plan members and MRR

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Plan Schema

`brain/hvac-plumbing/plans.json`:
```json
{
  "tiers": {
    "Silver": {
      "monthly": 14.99,
      "annual": 169,
      "tune_ups_per_year": 1,
      "labor_rate": 130,
      "diag_fee": 0,
      "parts_discount": 0.10
    },
    "Gold": {
      "monthly": 24.99,
      "annual": 279,
      "tune_ups_per_year": 2,
      "labor_rate": 115,
      "diag_fee": 0,
      "parts_discount": 0.15,
      "priority_dispatch": true
    }
  }
}
```

Member record at `brain/hvac-plumbing/members/{customer-slug}.json`:
```json
{
  "customer": "...",
  "tier": "Gold",
  "started": "2025-04-01",
  "billing": "monthly",
  "next_charge": "2026-05-01",
  "renews": "2026-04-01",
  "systems": [
    { "type": "AC", "make": "Carrier", "model": "24ABC6", "serial": "...", "installed": "2018-06-12" },
    { "type": "Furnace", "make": "Carrier", "model": "59TN6", "installed": "2018-06-12" }
  ],
  "tune_ups": {
    "spring_due": "2026-04-15",
    "spring_done": null,
    "fall_due": "2026-10-15",
    "fall_done": "2025-10-08"
  },
  "active": true
}
```

### Step 2: Due-Soon & Overdue Logic

Buckets (run on demand or on a `/loop` schedule):
- **Due in next 14 days** → schedule via `/linda-dispatch`
- **Overdue 1–30 days** → urgent reminder text
- **Overdue 30+ days** → manager call list
- **Renewing in next 30 days** → renewal notice

### Step 3: Reminders

Auto-draft messages:

```
"Hi {Name}, it's {Company}. Your spring HVAC tune-up is due. We've got openings the
 week of {window}. Reply with a day that works and we'll get you on the board. — {Tech}"
```

Save drafts to `brain/hvac-plumbing/reminders/{YYYY-MM-DD}/{customer-slug}.md`. Hand off to `/linda-mail` or SMS.

### Step 4: Renewal Notices

Branded PDF letter 30 days before renewal. Highlights:
- What they got this past year (tune-ups performed, savings on calls)
- New tier value
- One-click renew (text REPLY YES or click link)
- LindaAI top-right, {customer_handle} bottom-right, © 2024–2026 footer

### Step 5: Reporting

Boss sees:

```markdown
# Maintenance Plan Report — {YYYY-MM-DD}

| Tier | Active | MRR | Annual Run-rate |
|------|-------:|----:|----------------:|
| Silver | 142 | $2,128.58 | $25,542 |
| Gold   | 87  | $2,174.13 | $26,089 |
| **Total** | **229** | **$4,302.71** | **$51,631** |

## This Month
- Tune-ups due: 38
- Overdue: 7 (3 are 30+ days)
- Renewing: 14
- New enrollments: 5
- Cancellations: 1

## Action List
- Call Henderson (overdue 41 days)
- Send renewal letters to 14 members
- Schedule 38 tune-ups via /linda-dispatch

🤠 *Tracked by LindaAI* 🏇
```

## Example Usage

**User:** "Enroll Mrs. Henderson in Gold, monthly billing, AC + furnace, tune-ups spring and fall."

**LindaAI:** "Let's gooooooo Boss." Creates member record, sets next-charge, schedules first tune-up window. "Yeeee Hawww 🤠 — Henderson is Gold. First spring tune-up window: April 14–18. Want to dispatch?"

**User:** "Who's due for a tune-up this month?"

**LindaAI:** Returns the list with phones and addresses, offers to draft reminders.

**User:** "Send renewal letters to anyone renewing in May."

**LindaAI:** Drafts personalized PDFs for each, saves drafts, asks Boss to approve before sending.

## Voice & Tone

- Country, direct, **Boss**.
- Customer reminders: warm, neighborly, never naggy.

## Error Handling

- **Tier name unknown:** Reject — only Silver / Gold (use Bronze/Silver/Gold/Platinum if Boss ever expands plans).
- **Customer already on a plan:** Ask whether to upgrade/downgrade.
- **No payment method on file:** Flag for billing setup before enrolling.
- **Tune-up date in past:** Schedule next available window, don't backfill silently.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
