---
name: linda-pmfind
description: This skill should be used when the user asks to "find a property manager", "PM search", "vetted property managers", "property manager outreach", "PM in [city]", "find a PM for my rental", "property management companies", "PM interview", "screen property managers", "PM vetting", "property manager comparison", or any request involving sourcing, vetting, or outreach to property management companies.
tags: [operator, property-manager, real-estate, sourcing, outreach]
version: 1.0.0
---

# Linda PMFind — Property Manager Finder

## Overview

Wrong property manager will torch your portfolio faster than a tenant from hell. Linda PMFind hunts the market, pulls vetted candidates, runs the reviews, builds a personalized outreach sequence, and tracks responses. By the time Boss47 takes a call, the field is narrowed to 3-5 PMs who actually fit the asset class (mobile home park, RV park, SFR, small multifamily, or commercial). No more "first PM who answers the phone."

## When This Skill Applies

- "Find me a PM in Burlington for the duplex"
- "Search for MHP property managers in Texas"
- "Vet these 3 PMs"
- "Build outreach to property managers in {market}"
- "Compare these PM proposals"
- "Track PM responses"

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Define the Search

Inputs:
| Field | Notes |
|-------|-------|
| Market (city + state, or zip) | Required |
| Asset class | SFR / small multi / large multi / MHP / RV park / commercial |
| Number of units | Affects which PMs will take the gig |
| Service level | Full management / Tenant placement only / Lease-up only |
| Budget | Typical 8–12% gross or flat fee — set ceiling |
| Special needs | Section 8, military housing, evictions specialist, etc. |

### Step 2: Source Candidates

Cast a wide net via WebSearch + WebFetch:
- IREM-certified PMs (irem.org chapter directories)
- NARPM members (narpm.org member search)
- Google "property management {city} {asset_class}"
- Yelp + Google Maps reviews
- BiggerPockets PM marketplace
- For MHP/RV — MHCommunity Owners Council list, IRPCM

For each candidate capture:
| Field |
|-------|
| Company name |
| Founder / lead PM name |
| Office address |
| Phone, email, website |
| Asset classes managed |
| Door count / portfolio size |
| Years in business |
| License number (state real estate broker required in most states) |
| Average review rating + count (Google + Yelp) |
| Any complaints filed (BBB, state RE commission) |

### Step 3: Score & Vet

100-point rubric:
- Asset-class fit 25 (specialty match = 25, related = 15, generalist = 8)
- Door count 20 (1,000+ = 20, 250-999 = 15, 50-249 = 10, <50 = 5 — sometimes the boutique wins, weight subjective)
- Reviews 20 (4.5+ stars 50+ reviews = 20, scaling down)
- Years in business 10 (10+ = 10, 5-9 = 7, 2-4 = 4, <2 = 1)
- Licensure & insurance 10 (verified active = 10)
- Complaints 10 (zero = 10, 1-2 minor = 6, serious = 0 — disqualifier)
- Local market knowledge 5 (HQ in market = 5)

Top 5 by score → outreach list.

### Step 4: Outreach Build

Personalized email + voicemail script per candidate. Lead with:
- Boss47 / entity name
- Property profile (location, units, asset class)
- Specific reason this PM fits ("saw you manage 220 units in Chittenden County" / "5-star reviews from MHP owners")
- Three direct questions:
  1. Do you currently manage {asset class} of {N} units in this market?
  2. What's your fee structure for this scope?
  3. When can we hop on a 20-minute call this week?

Save outreach drafts to `brain/operator/pmfind/{market-slug}/outreach/{pm-slug}.md`. Send via `linda-mail` on confirmation.

### Step 5: Tracking

Pipeline CSV at `brain/operator/pmfind/{market-slug}/tracker.csv`:
```
pm_name, score, contact, outreach_sent, response_date, fee_structure, fit_score, status, notes
```

Stages: Not Contacted → Outreach Sent → Responded → Call Scheduled → Proposal Received → Selected / Passed.

### Step 6: Comparison Matrix (When 2+ Proposals In)

Side-by-side proposal compare PDF:
- Fee structure (% gross, leasing fee, eviction fee, maintenance markup, late fee split)
- Term + cancellation
- Software stack (AppFolio, Buildium, Propertyware, Yardi)
- Owner reporting cadence
- Eviction handling
- After-hours coverage
- Recommendation with reasoning

Save to `brain/operator/pmfind/{market-slug}/comparison-{YYYY-MM-DD}.pdf`.

## Inputs

- Market + asset class + size
- (Optional) candidate names to add manually
- (Optional) proposal PDFs to compare

## Outputs

- Sourced candidate list (CSV)
- Top-5 outreach drafts (MD)
- Tracker CSV (pipeline)
- Comparison matrix PDF (when multi-proposal)

## Example Usage

**User:** "Find a PM in Burlington VT for a 2-unit duplex, SFR-grade."

**LindaAI:** "Let's gooooooo Boss47!" Searches NARPM + Google + Yelp. Returns 11 candidates. Scores → top 5: Northeast Property Mgmt (85), Burlington Rentals (78), Champlain PM (72), 2 more. "Yeeee Hawww 🤠 — outreach drafts ready for top 5. Want me to fire 'em via linda-mail?"

**User:** "Compare these 3 proposals." (drops PDFs)

**LindaAI:** Parses, builds matrix, recommends one with reasoning.

**User:** "Update tracker — Northeast PM responded, wants a call Thursday 2pm."

**LindaAI:** Updates row, optionally creates calendar event.

## Voice & Tone

- Country, sharp. **Boss47.**
- "Let's gooooooo!" on kickoff. "Yeeee Hawww 🤠" when outreach is fired.
- Direct on red flags: "Boss47 — this one's got 3 BBB complaints. Pass."

## Brand Rules (PDFs)

- LindaAI logo top-right
- {customer_handle} bottom-right
- © 2024–2026 LindaAI · Built by Daniel Wise footer

## Cross-Skill Hooks

- **Feeds → linda-mail** — fires outreach emails
- **Feeds → linda-files** — signed PM agreement files into cabinet
- **Feeds ↔ linda-tenants** — once PM hired, tenant ops route through PM
- **Feeds → linda-vendor** — selected PM gets vendor record
- **Feeds → linda-bizops** — PM status by property on dashboard

## Error Handling

- **No PMs found in market:** Widen radius, suggest virtual / out-of-area PMs with on-site boots-on-ground.
- **All candidates have <3 reviews:** Surface anyway with "thin data" warning.
- **Proposal PDF unparseable:** Ask Boss47 to paste fee schedule manually.
- **No license:** Country howdy and stop.

## 🤝 Handoff to `/linda-post-walkthrough`

After this skill produces post-ready content (a "now under PM" property update, a referral-request post asking the network for PM recommendations, a vendor spotlight when you find a great one), hand off to **`/linda-post-walkthrough`** so 📣 Holler can walk Boss47 through posting it to TikTok/IG/FB/YT/X step-by-step in real time. No app-switching, no API setup — Holler opens the right URL, copies the caption to clipboard, reveals the file in Finder, and tells Boss47 exactly what to do.

Trigger phrase: **"walk me through posting this"** or just **"post this"**.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
