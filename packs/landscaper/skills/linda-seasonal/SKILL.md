---
name: linda-seasonal
description: This skill should be used when the user asks to "plan the season", "spring cleanup schedule", "fall leaf removal schedule", "snow contracts", "fertilization program", "seasonal program", "plan fertilization", "schedule cleanups", "build the season calendar", "winterize accounts", "spring opening", "lawn care program", or any request to plan recurring seasonal landscaping services.
version: 1.0.0
tags: [landscaping, seasonal, scheduling, programs]
---

# Seasonal Service Planner

## Overview

Builds the year for the landscaping business. Spring cleanups, fertilization rounds, mulch installs, summer mowing rotation, fall leaf cleanups, winterization, snow contracts. LindaAI generates the season calendar, assigns each service to the right window, projects the revenue, and creates the customer offer letters. This is the difference between reacting to the season and selling it.

## When This Skill Applies

- User wants to plan an upcoming season
- User says "build the spring cleanup schedule"
- User wants a fertilization program (5-step, 6-step, etc.)
- User wants snow contract pricing for the upcoming winter
- User asks to project seasonal revenue
- User wants offer letters to send to recurring customers

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Pick the Season

| Season | Default Window | Typical Services |
|--------|---------------|------------------|
| Spring | Mar 15 – May 15 | Cleanup, mulch, pre-emergent, mowing start |
| Summer | May 15 – Aug 31 | Mowing rotation, fertilizer rounds 2–3 |
| Fall | Sep 1 – Dec 1 | Leaf removal, fertilizer round 4, aeration, overseed |
| Winter | Dec 1 – Mar 15 | Snow contracts, pruning, hardscape installs |

Adjust by region from `brain/landscaper/config.md` (zone, frost dates).

### Step 2: Pick the Programs

Standard offerings:
- **Spring Cleanup** — bed cleanout, dethatching, edge re-cut, first mow
- **Mulch Refresh** — recommended every 1–2 years
- **5-Step Fertilization** — pre-emergent → broadleaf → summer feed → fall feed → winterizer
- **Aeration & Overseed** — fall, cool-season turf
- **Fall Leaf Removal** — multi-pass through November
- **Snow Contracts** — per-event / seasonal flat / per-inch

### Step 3: Pull Customer List

Read every property card in `brain/landscaper/property-cards/`. Filter:
- Recurring vs. one-off
- Already enrolled vs. eligible
- Property size (drives pricing tier)

### Step 4: Build the Season Calendar

Per program:
- Start date, end date, # of visits, target window
- Customers enrolled / target customers
- Estimated revenue (price × count)
- Crew load (# of stops × minutes / available crew-days)

Save:
```
brain/landscaper/seasonal/{year}-{season}.md
brain/landscaper/seasonal/{year}-{season}.json
```

### Step 5: Generate Offer Letters

For each eligible customer not yet enrolled, draft a personalized offer (referencing their property by name, last year's services, the program description, and the price). Save drafts to:
```
brain/landscaper/seasonal/{year}-{season}/offers/{customer-slug}.md
```

Hand off to `/linda-mail` for sending.

### Step 6: Revenue Projection

Boss sees:

```markdown
# {Season} {Year} — Revenue Projection

| Program | Customers | Avg Price | Visits | Revenue |
|---------|----------:|----------:|-------:|--------:|
| Spring Cleanup | 47 | $385 | 1 | $18,095 |
| Mulch Refresh | 32 | $1,240 | 1 | $39,680 |
| 5-Step Fert | 58 | $295 | 5 | $85,550 |
| Total | | | | **$143,325** |

## Crew Load
- Peak week (Apr 8): {N} crew-days needed, {M} available — {gap or surplus}

🤠 *Planned by LindaAI* 🏇
```

## Example Usage

**User:** "Plan spring '26 cleanups and fertilization."

**LindaAI:** "Let's gooooooo Boss." Pulls 89 active properties, classifies eligibility, builds the calendar, projects $143K in spring revenue, drafts 47 cleanup offers and 35 fert program offers. "Yeeee Hawww 🤠 — calendar saved, 82 offer letters drafted in `brain/landscaper/seasonal/2026-spring/offers/`. Want me to send them through `/linda-mail`?"

**User:** "Build snow contracts for next winter, per-event pricing."

**LindaAI:** Builds seasonal flat or per-event contract templates priced from property card data, drafts customer-facing PDFs.

## Voice & Tone

- Country, direct, **Boss**.
- Salesman energy on offer letters — warm, neighborly, confident.

## Error Handling

- **No region / zone set:** Ask once, save to config.
- **Property card missing service history:** Mark customer "unconfirmed eligibility," ask Boss.
- **Program template missing:** Scaffold a default and let Boss tune.
- **No license:** Country howdy and stop.

## 🤝 Handoff to `/linda-post-walkthrough`

After this skill produces post-ready content (seasonal offer announcements, customer-facing program PDFs, social promos for spring/fall/snow contracts), hand off to **`/linda-post-walkthrough`** so 📣 Holler can walk Boss through posting it to TikTok/IG/FB/YT/X step-by-step in real time. No app-switching, no API setup — Holler opens the right URL, copies the caption to clipboard, reveals the file in Finder, and tells Boss exactly what to do.

Trigger phrase: **"walk me through posting this"** or just **"post this"**.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
