---
name: linda-warranty
description: This skill should be used when the user asks to "log a warranty", "track warranty", "warranty tracker", "check warranty status", "is this still under warranty", "manufacturer warranty", "labor warranty", "install date", "warranty claim", "register equipment warranty", "extended warranty", "warranty for {customer}", or any request involving HVAC or plumbing equipment warranty tracking.
version: 1.0.0
tags: [hvac, plumbing, warranty, install-tracking]
---

# Warranty Tracker

## Overview

Logs every install with the dates that matter: the company labor warranty (typically 1 year), the manufacturer parts warranty (5–10 years registered), and any extended warranties the customer paid up for. LindaAI surfaces "still under warranty" answers in seconds, generates RGA / claim packets, and reminds the office to register new installs within the manufacturer's window so customers don't lose coverage.

## When This Skill Applies

- A new install was completed and needs to be registered
- User asks "is {customer}'s system still under warranty?"
- User wants to file a warranty claim (RGA)
- User wants the warranty status report
- User wants to remind techs about install registration deadlines

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Warranty Schema

`brain/hvac-plumbing/warranties/{customer-slug}/{install-id}.json`:
```json
{
  "install_id": "INST-20260315-003",
  "customer": "Henderson Residence",
  "address": "789 Elm St",
  "installed_date": "2026-03-15",
  "tech": "Mike",
  "equipment": [
    {
      "type": "AC condenser",
      "make": "Carrier",
      "model": "24ABC6",
      "serial": "1234ABC",
      "manufacturer_parts_warranty_years": 10,
      "registered": true,
      "registered_date": "2026-03-18",
      "registration_deadline": "2026-06-13",
      "manufacturer_expires": "2036-03-15"
    }
  ],
  "labor_warranty_years": 1,
  "labor_expires": "2027-03-15",
  "extended_purchased": false,
  "notes": ["Permit closed 2026-03-22"]
}
```

### Step 2: Registration Reminders

For any equipment with `registered = false`:
- 30 days from install: green reminder
- 60 days: yellow
- 80 days: red — "register today or customer loses 5 years of parts coverage"

Many manufacturers (Carrier, Trane, Lennox, Goodman) require registration within 60–90 days of install to grant the full 10-year parts warranty.

### Step 3: Status Lookup

Boss asks "is Henderson's system still under warranty?":

```markdown
# Warranty Status — Henderson Residence

| Item | Type | Installed | Labor | Parts | Status |
|------|------|-----------|-------|-------|--------|
| Carrier 24ABC6 condenser | AC | 2026-03-15 | until 2027-03-15 | until 2036-03-15 | ✅ Both |
| Carrier 59TN6 furnace | Furnace | 2026-03-15 | until 2027-03-15 | until 2036-03-15 | ✅ Both |

🤠 *Checked by LindaAI* 🏇
```

### Step 4: Claim Packet (RGA)

When Boss says "file a claim on Henderson's compressor":
- Pulls install record (model, serial, install date, registration confirmation)
- Pulls failure ticket (`/linda-ticket`) for symptom + diagnosis
- Generates claim packet PDF with all required fields for the manufacturer's RGA portal
- LindaAI top-right, {customer_handle} bottom-right, © 2024–2026 footer

Save to:
```
brain/hvac-plumbing/warranties/{customer-slug}/claims/RGA-{YYYYMMDD}-{NNN}.pdf
```

### Step 5: Reporting

```markdown
# Warranty Pulse — {YYYY-MM-DD}

## Registration Action List
| Customer | Install | Days Since | Deadline | Status |
|----------|---------|-----------:|----------|--------|
| Smith | 2026-03-22 | 39 | 2026-06-20 | 🟡 |
| Garcia | 2026-04-01 | 29 | 2026-06-30 | 🟢 |
| Lee | 2026-02-10 | 79 | 2026-05-11 | 🔴 register today |

## Active Coverage
- 247 customers have active labor coverage
- 312 systems under manufacturer parts warranty

## Expiring This Quarter
- 18 labor warranties (target for renewal upsell)

🤠 *Tracked by LindaAI* 🏇
```

## Example Usage

**User:** "Log Henderson install — 3/15, Carrier 24ABC6 serial 1234ABC, Mike was tech, 1-year labor."

**LindaAI:** "Let's gooooooo Boss." Creates install record, calculates registration deadline (90 days), saves. "Yeeee Hawww 🤠 — INST logged. Reminder set: must register with Carrier by June 13 to lock the 10-year parts warranty."

**User:** "Is Henderson's compressor under warranty?"

**LindaAI:** Returns status table — both labor and parts active.

**User:** "File a claim on Henderson's compressor."

**LindaAI:** Pulls failure ticket, generates RGA packet PDF.

## Voice & Tone

- Country, direct, **Boss**.
- Urgent voice on registration deadlines — money on the line.

## Error Handling

- **Serial number missing:** Save without it, flag — many manufacturers reject claims without serial.
- **Install pre-dates the system in place:** Ask Boss to confirm before back-dating.
- **Manufacturer warranty terms unknown:** Default to 5-year parts, ask Boss to confirm.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
