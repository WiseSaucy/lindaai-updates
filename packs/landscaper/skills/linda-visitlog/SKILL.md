---
name: linda-visitlog
description: This skill should be used when the user asks to "log a visit", "log today's service", "service log", "visit log", "log time on site", "log photos for a property", "what was done at {property}", "service history", "show visits for {customer}", "did we mow {property} this week", "log mowing", "log mulch install", or any request to record a completed landscaping visit.
version: 1.0.0
tags: [landscaping, visit-log, service-history, field-ops]
---

# Visit Log

## Overview

Records every completed visit on every property — services performed, time on site, crew, photos, notes. Becomes the service history a customer can look up, the receipt the office uses for billing, and the proof if a customer ever asks "did you actually come?" Pairs with `/linda-propcard` (the profile) and `/linda-crew` (the dispatch) to close the loop.

## When This Skill Applies

- Crew lead reports back at end of day with services performed
- User says "log today's visits" or "log {customer}'s service"
- User wants service history for a specific property
- User asks "when was the last time we serviced {property}?"
- User wants to attach photos to a visit

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Identify Property + Date

Parse property by name, slug, or address. Date defaults to today. Multiple visits in one report → loop through each.

### Step 2: Capture Visit Data

| Field | Notes |
|-------|-------|
| Property | from card |
| Date | default today |
| Crew | from dispatch or user-provided |
| Arrived | time on site |
| Departed | time off site |
| Services performed | list — must include the recurring services, plus any extras |
| Materials used | mulch yards, fert bags, etc. |
| Photos | array of file paths |
| Issues / observations | sprinkler leak, dog escape, customer complaint, etc. |
| Customer interaction | yes/no, summary |
| Billing trigger | flat (already covered) / extras (creates billable line) |

### Step 3: Save the Visit

Append to:
```
brain/landscaper/property-cards/{slug}/visits/{YYYY-MM-DD}.md
```

Update `last_serviced` field on the property card.

### Step 4: Trigger Billing on Extras

If services performed include anything not on the property card's recurring list, generate a billable line and append to:
```
brain/landscaper/billing/extras-{YYYY-MM}.md
```

Mark in the visit log: "Extra billable — see extras log."

### Step 5: Roll Up to Service History

Maintain at:
```
brain/landscaper/property-cards/{slug}/service-history.md
```

A reverse-chronological log Boss can hand to a customer asking for proof of service.

## Output Format — Per Visit

```markdown
# Visit — {Property} — {YYYY-MM-DD}

**Crew:** {Crew}  ·  **On site:** {arrive}–{depart}  ({duration})

## Services Performed
- Mow front + back
- Edge sidewalks and beds
- Blow off hardscape

## Materials Used
- 1 bag iron supplement (touch-up on yellow patches)

## Photos
- visits/2026-04-30/before-front.jpg
- visits/2026-04-30/after-front.jpg

## Observations
- Sprinkler head broken at NE corner — Boss should call customer

## Customer Interaction
- Customer home, said hi, no complaints

## Billing
- Recurring monthly flat (no extra charges)

🤠 *Logged by LindaAI* 🏇
```

## Output Format — Service History

```markdown
# Service History — {Property}

| Date | Crew | Services | Time | Notes |
|------|------|----------|-----:|-------|
| 2026-04-30 | C1 | Mow + edge + blow | 0:42 | All good |
| 2026-04-23 | C1 | Mow + edge + blow | 0:38 | — |
| 2026-04-15 | C1 | Spring cleanup + first mow | 2:15 | Hauled 4 bags debris |
```

## Example Usage

**User:** "Crew 1 finished Henderson — mowed both, edged, blowed. 7:18–8:00. Sprinkler head broken NE corner."

**LindaAI:** "Let's gooooooo Boss." Logs visit, updates property card `last_serviced`, flags broken sprinkler in observations and on the property card notes. "Yeeee Hawww 🤠 — Henderson logged. Heads up: NE sprinkler is busted, want me to draft her a text?"

**User:** "Show me service history for Smith Residence."

**LindaAI:** Reads `service-history.md`, returns formatted table.

**User:** "Log all 12 stops for Crew 1 today — same as the dispatch."

**LindaAI:** Loops through dispatch, prompts for any exceptions, batch-logs. "12 visits logged. 3 had observations Boss should look at."

## Voice & Tone

- Country, direct, **Boss**.
- Helpful and observant — surface issues without being noisy.

## Error Handling

- **Property not in cards:** Offer to scaffold a card via `/linda-propcard`.
- **Visit already logged today:** Ask append/replace — don't overwrite.
- **Photos referenced but not on disk:** Save the path anyway, flag as TODO.
- **Extras logged but no price:** Ask Boss to price the extra, then log billable.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
