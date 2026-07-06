---
name: linda-propcard
description: This skill should be used when the user asks to "create a property card", "property profile", "customer property card", "set up recurring service", "log gate code", "log dog notes", "service profile", "what services does {customer} get", "show me property card for", "update property card", "lawn size", "billing cadence for {customer}", or any request involving recurring landscaping property profiles.
version: 1.0.0
tags: [landscaping, properties, customers, recurring]
---

# Recurring Property Card

## Overview

Every recurring property gets one card. It's the source of truth: lawn size, services, cadence, billing terms, gate codes, dog notes, sprinkler shutoff location, where to dump clippings, the customer's preferences. When the crew rolls up, they know everything they need. When billing runs, the rate is right. When a new lead comes in, Boss has a template.

## When This Skill Applies

- User wants to create or update a property card
- User asks "what services does {customer} get?"
- User wants gate codes, pet notes, or special instructions for a property
- User wants to change service cadence or billing terms
- User says "show me the card for {address}"

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Identify the Property

By customer name, nickname, or address. If new, scaffold a card. If existing, load the existing JSON + markdown pair.

### Step 2: Card Schema

Stored as both JSON (for crews/dispatch) and markdown (human-readable):

```
brain/landscaper/property-cards/{property-slug}.json
brain/landscaper/property-cards/{property-slug}.md
```

```json
{
  "property": "Henderson Residence",
  "address": "789 Elm St, Springfield",
  "customer": "Mrs. Linda Henderson",
  "phone": "555-0102",
  "email": "linda.h@example.com",
  "billing": {
    "method": "monthly_flat",
    "amount": 285,
    "send_day": 1,
    "terms": "Net 15",
    "method_of_payment": "ACH on file"
  },
  "lawn": {
    "front_sqft": 4200,
    "back_sqft": 5600,
    "total_sqft": 9800,
    "fenced": true,
    "slope": "moderate"
  },
  "services": [
    { "service": "Mow + edge + blow", "cadence": "weekly", "season": "Apr-Oct", "price": 65 },
    { "service": "Fertilization 5-step", "cadence": "5x annual", "season": "year", "price": 295 },
    { "service": "Spring cleanup", "cadence": "annual", "season": "Apr", "price": 385 },
    { "service": "Fall leaf removal", "cadence": "3x", "season": "Oct-Nov", "price": 175 }
  ],
  "service_day": "Tuesday",
  "crew": "C1",
  "access": {
    "gate_code": "5567",
    "side_gate": "left of house, latch only",
    "key_safe": null
  },
  "pets": "Golden retriever 'Buddy' — friendly, in back yard. Knock first.",
  "notes": [
    "Don't blow into the koi pond",
    "Sprinkler shutoff is in garage, north wall",
    "Customer prefers Tuesday afternoons"
  ],
  "active": true,
  "started": "2023-04-12",
  "last_serviced": null
}
```

### Step 3: Generate the Markdown Card

Pretty version for the office:

```markdown
# {Property} — Property Card

**Customer:** {Name}  ·  {Phone}  ·  {Email}
**Address:** {Address}
**Service Day:** {Day}  ·  **Crew:** {Crew}

## Billing
- Method: {monthly flat / per-visit}
- Amount: ${X}
- Send day: {day of month}
- Terms: {Net X}
- Payment: {ACH / card on file / invoice}

## Lawn
- Total turf: {sqft}  ({front} front / {back} back)
- Fenced: {yes/no}
- Slope: {flat / moderate / steep}

## Services
| Service | Cadence | Season | Price |
|---------|---------|--------|------:|
| Mow + edge + blow | weekly | Apr–Oct | $65 |
| 5-step fert | 5x | year | $295 |

## Access
- Gate code: {code}
- Side gate: {note}
- Key safe: {if any}

## Pets
{notes}

## Notes
- ...

🤠 *Card maintained by LindaAI* 🏇
```

### Step 4: Cross-Skill Links

- Routing: cards drive `/linda-route` daily routes via `service_day`
- Dispatch: cards feed scope and notes into `/linda-crew` job sheets
- Visit log: cards link to `/linda-visitlog` history
- Estimating: cards seed pricing in `/linda-estimate`
- Seasonal: cards drive eligibility in `/linda-seasonal`

### Step 5: Update / Lookup

Standard updates:
- Change service day
- Add or remove a recurring service
- Update gate code (also append to a dated note so crews see "code changed {date}")
- Mark inactive (don't delete — `active: false` and date)

## Example Usage

**User:** "Create a property card for Mrs. Henderson, 789 Elm. Weekly mowing $65, 5-step fert $295, side gate has a code 5567, golden retriever in back."

**LindaAI:** "Let's gooooooo Boss." Builds JSON + markdown, prompts for billing terms, defaults service day to next available, saves both. "Yeeee Hawww 🤠 — Henderson card saved. She's on Tuesday with Crew 1."

**User:** "Update Henderson — gate code is now 9921."

**LindaAI:** Updates code, appends "code changed 2026-04-30" to notes, alerts dispatch.

**User:** "Show me the card for Smith Residence."

**LindaAI:** Reads markdown, returns it.

## Voice & Tone

- Country, direct, **Boss**.
- Treat each card like the customer is a neighbor — warm details matter.

## Error Handling

- **Slug collision:** Append a digit, never overwrite (`henderson-residence-2`).
- **Missing billing info on first save:** Ask Boss once.
- **Lawn sqft unknown:** Save without it, flag as TODO — needed for accurate `/linda-estimate`.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
