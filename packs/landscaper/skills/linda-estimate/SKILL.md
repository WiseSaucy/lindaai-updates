---
name: linda-estimate
description: This skill should be used when the user asks to "estimate a job", "build an estimate", "price a job", "quote landscaping work", "mowing estimate", "mulch estimate", "sod estimate", "hardscape estimate", "tree work estimate", "patio quote", "fence quote", "leaf removal quote", "lawn install quote", "what should I charge for", "build a proposal", or any request to price a landscaping or hardscape job.
version: 1.0.0
tags: [landscaping, estimating, quoting, sales]
---

# Job Estimator

## Overview

Builds a clean, profitable estimate for any landscaping job — mowing, mulch, sod, hardscape, tree work, irrigation, leaf removal, snow contracts. LindaAI prices materials, labor, equipment, dump fees, and applies the user's markup, then renders a branded customer-facing quote PDF. Saves to the customer's folder and logs in the estimate book.

## When This Skill Applies

- User wants a price on a specific job
- User says "build an estimate for {customer}"
- User wants a customer-facing quote PDF
- User asks "what should I charge for {service}?"
- User mentions mulch, sod, hardscape, mowing contract, etc.

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Gather Job Inputs

| Field | Required | Notes |
|-------|----------|-------|
| Customer name | Yes | Look up in `brain/landscaper/customers/` |
| Property address | Yes | |
| Service type | Yes | Mow / mulch / sod / hardscape / tree / irrigation / leaf / snow / other |
| Scope | Yes | Square footage, linear feet, # plants, # trees, etc. |
| Season | optional | Affects pricing on mulch (peak), sod (peak), snow (contract month) |

### Step 2: Pull Pricing from Catalog

Read `brain/landscaper/pricing.json` (create with sensible defaults if missing):

```json
{
  "labor_rate_per_hour": 65,
  "crew_min_size": 2,
  "markup_materials": 1.40,
  "dump_fee": 65,
  "mobilization_min": 75,
  "services": {
    "mowing": { "rate_per_1000_sqft": 12, "min_charge": 45 },
    "mulch_install": { "labor_yd": 0.75, "material_yd": 38, "min_yards": 2 },
    "sod": { "labor_sqft": 0.45, "material_sqft": 0.95, "prep_sqft": 0.20 },
    "leaf_removal": { "rate_per_1000_sqft": 35, "min_charge": 175 },
    "tree_removal": { "by_size": { "small": 350, "medium": 850, "large": 1800, "xl": 3500 } },
    "paver_patio": { "labor_sqft": 14, "material_sqft": 9, "base_sqft": 4 }
  }
}
```

### Step 3: Calculate

Generic formula:
```
Materials Cost   = Σ (qty × unit cost)
Materials Sell   = Materials Cost × markup_materials
Labor Hours      = scope ÷ production rate
Labor Sell       = Hours × labor_rate × crew_size
Equipment        = day rate or per-job
Dump / Disposal  = per load
Mobilization     = min charge if small job
Subtotal         = sum
Tax (if applies) = per state
TOTAL            = subtotal + tax
```

Always show a "Job Margin %" internally so Boss can see profitability before sending.

### Step 4: Render Quote

Two outputs:
- Markdown: `brain/landscaper/estimates/{customer-slug}/EST-{YYYYMMDD}-{NNN}.md`
- Branded PDF: same path, `.pdf`

PDF must show **LindaAI top-right**, **{customer_handle} bottom-right**, footer `© 2024–2026 LindaAI`.

### Step 5: Update Log

Append to `brain/landscaper/estimates/_log.md`: number, date, customer, scope, total, status (Sent / Accepted / Declined).

## Output Format (Customer-Facing)

```markdown
# {Company Name} — Estimate {EST-YYYYMMDD-NNN}

**Customer:** {Name}
**Property:** {Address}
**Date:** {YYYY-MM-DD}
**Valid for:** 30 days

## Scope of Work
{Plain-language description}

| # | Item | Qty | Unit | Price | Amount |
|---|------|-----|------|------:|-------:|
| 1 | Hardwood mulch — installed | 12 | yd | $95 | $1,140 |
| 2 | Bed prep / edging | 1 | lump | $250 | $250 |
| 3 | Haul-off | 1 | load | $85 | $85 |

| | |
|---|--:|
| **Subtotal** | $1,475 |
| Tax | $0 |
| **TOTAL** | **$1,475** |

## Inclusions
- ...

## Exclusions
- ...

## Terms
- 50% deposit to schedule, balance due upon completion
- Estimate valid 30 days from date above

🤠 *Prepared by LindaAI on behalf of {Company}* 🏇
```

## Example Usage

**User:** "Estimate for Mrs. Henderson, 789 Elm — install 12 yards of hardwood mulch in beds, edge them, haul off old mulch."

**LindaAI:** "Let's gooooooo Boss." Builds 3-line estimate, calculates $1,475 (margin 38%), renders PDF, saves. "Yeeee Hawww 🤠 — EST-20260430-007 ready. Margin's healthy at 38%. Want me to fire it off?"

**User:** "Quote a 600 sqft paver patio for Smith Residence."

**LindaAI:** Calculates labor + materials + base, applies markup, renders quote.

## Voice & Tone

- Country, direct, **Boss**.
- Show the margin to Boss internally before sending — no skinny jobs.

## Error Handling

- **No pricing catalog yet:** Scaffold `pricing.json` with defaults and tell Boss to review.
- **Scope unclear:** Ask for square footage, yards, count — the specifics that drive price.
- **Margin under 25%:** Flag and ask: "Margin's tight at {X}%. Bump price or proceed?"
- **No license:** Country howdy and stop.

## 🤝 Handoff to `/linda-post-walkthrough`

After this skill produces post-ready content (estimate one-pager, win announcement, before/after install showcase), hand off to **`/linda-post-walkthrough`** so 📣 Holler can walk Boss through posting it to TikTok/IG/FB/YT/X step-by-step in real time. No app-switching, no API setup — Holler opens the right URL, copies the caption to clipboard, reveals the file in Finder, and tells Boss exactly what to do.

Trigger phrase: **"walk me through posting this"** or just **"post this"**.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
