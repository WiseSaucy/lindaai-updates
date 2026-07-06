---
name: linda-route
description: This skill should be used when the user asks to "optimize a route", "plan today's route", "route my crew", "best order for stops", "route optimizer", "fastest route", "drive time", "stop order", "build a daily route", "morning route", "Monday route", "landscape route", "mowing route", "snow route", or any request to optimize a sequence of property stops for a service crew.
version: 1.0.0
tags: [landscaping, routing, dispatch, field-ops]
---

# Route Optimizer

## Overview

Takes a list of properties (or a service day from the recurring property cards) and builds an optimized stop order with drive times and total route duration. Reduces windshield time, fits more stops in a day, and gets the crew home before dark. Output is a clean stop list the crew can follow on their phones — and feeds straight into `/linda-crew` for dispatch.

## When This Skill Applies

- User wants to plan a daily route for a crew
- User says "what's the best order for these stops?"
- User asks to optimize a service day (Monday, Tuesday, etc.)
- User wants drive time totals for a list of properties
- User says "route my crew" or "build today's route"

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Gather Stops

Inputs accepted:
- Pasted list of addresses
- A service day name (e.g., "Tuesday route") — pull from `brain/landscaper/property-cards/` where `service_day = Tuesday`
- A crew name — pull every active stop assigned to that crew

For each stop capture:
| Field | Source |
|-------|--------|
| Property name / nickname | property card |
| Address | property card |
| On-site time estimate | property card (default 30 min) |
| Time window | property card (e.g., "after 9am — gate locked till then") |
| Special notes | gate code, dog, side gate, etc. |

### Step 2: Choose Starting Point

Default starting point: the shop / yard address from `brain/landscaper/config.md`. If absent, ask Boss once and save it. Optional ending point (yard or "last stop wins").

### Step 3: Optimize Order

Use a nearest-neighbor heuristic, then refine with a 2-opt swap pass for ≤25 stops. Use WebSearch / WebFetch against a maps service to get pairwise drive times if available; otherwise use straight-line distance × 1.4 fudge factor.

Respect constraints:
- Time-window stops sequenced inside their window
- Sticky pairs (e.g., "do these two together — same complex")
- Hard last stop (a property the crew always closes at)

### Step 4: Build Day Plan

Calculate:
- Departure time (default 7:00 AM, configurable)
- Arrival, on-site, depart times for each stop
- Total drive time
- Total on-site time
- Estimated end-of-day time

### Step 5: Save & Share

```
brain/landscaper/routes/{YYYY-MM-DD}-{crew}.md
```

If Boss says "send it," hand off to `/linda-crew` to dispatch.

## Output Format

```markdown
# Daily Route — {Crew} — {YYYY-MM-DD}

**Depart yard:** 7:00 AM
**Yard:** {address}
**Total stops:** {N}
**Total drive time:** {hh:mm}
**Total on-site:** {hh:mm}
**Estimated finish:** {time}

| # | Time | Property | Address | Service | On-site | Notes |
|---|------|----------|---------|---------|---------|-------|
| 1 | 7:18 | Maple HOA | 123 Main | Mow + edge | 0:45 | Gate code 1234 |
| 2 | 8:08 | Smith Residence | 456 Oak | Mow only | 0:30 | Dog in back, knock first |
| ... |

## Map Order
1 → 2 → 3 → 4 → ... → yard

🤠 *Routed by LindaAI* 🏇
```

## Example Usage

**User:** "Build Tuesday's route for Crew 2."

**LindaAI:** "Let's gooooooo Boss." Pulls all Tuesday properties assigned to Crew 2, optimizes, writes the file. "Yeeee Hawww 🤠 — 14 stops, 1h 47m driving, 6h 30m mowing. Should be done by 3:17."

**User:** "Optimize these 6 addresses: {list}. Start at 1100 W Main."

**LindaAI:** Optimizes from given start, returns the ordered list with drive times.

**User:** "Add Mrs. Henderson at 789 Elm to today's route — fit her in."

**LindaAI:** Re-optimizes, finds the best insertion point, updates the file, tells Boss the new finish time.

## Voice & Tone

- Country, direct. **Boss.**
- "Let's gooooooo" on kickoff. "Yeeee Hawww 🤠" when route is locked.

## Error Handling

- **No yard / starting point set:** Ask once, save to `brain/landscaper/config.md`.
- **Address won't geocode:** Flag the stop, leave it un-routed at the end of the list, ask Boss to correct.
- **Maps service unavailable:** Fall back to straight-line × 1.4, note in the output.
- **Stop with hard time-window can't fit:** Flag — recommend dropping a different stop or adding overtime.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
