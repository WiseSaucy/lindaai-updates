---
name: linda-kpi
description: This skill should be used when the user asks to "check my KPIs", "show my dashboard", "KPI dashboard", "restaurant KPIs", "my key metrics", "how are my numbers", "deep dive on labor", "food cost analysis", "prime cost report", "table turn analysis", "revenue per seat", "rev per seat hour", "covers analysis", "average check trend", "comp sales", "comp sales report", "year over year sales", "YoY", "monthly KPIs", "MTD numbers", "track my metrics", "set KPI targets", "set my targets", "update targets", "scorecard", "restaurant scorecard", or any request for a deep restaurant KPI dashboard (food cost %, labor %, prime cost, table turn, rev/seat, RevPASH, average check, covers, retention, marketing ROAS).
tags: [restaurant, kpi, dashboard, metrics, finance]
version: 1.0.0
---

# Restaurant KPI Dashboard

## Overview

📊 **Tally** (Data Analyst) at the console. The deep version of `/linda-pulse`. Where the pulse is the 60-second weekly heartbeat, the KPI dashboard is the full-physical: prime cost breakdown, table turn, revenue per available seat hour (RevPASH), guest retention, marketing return, every benchmark vs industry, every trend line, every leak called out by dollar amount.

This is what you pull up before a partner meeting, a bank meeting, or a serious sit-down about whether to expand.

## When to Use (Trigger Phrases)

- "Show my KPI dashboard"
- "Restaurant KPIs"
- "How are my numbers?"
- "Deep dive on labor"
- "Food cost analysis for the month"
- "What's my prime cost?"
- "Revenue per seat this month"
- "RevPASH"
- "Comp sales YoY"
- "Average check trend"
- "Set my KPI targets"
- "Build my scorecard"

## How It Works

### License Check

Verify `~/.claude/linda-license.json` (file exists, not expired, status active, optional server tamper check via `{api_url}/v1/licenses/validate/{license_key}`). On failure, halt with the country-voice license message.

### Step 0: Inputs

| Input | Required | Example |
|-------|----------|---------|
| Restaurant name | Yes | "Smokey's BBQ" |
| Reporting period | Yes | week / month / quarter / YTD / custom range |
| Sales by daypart (lunch / dinner / brunch / bar) | Yes | from POS export or manual |
| Covers by daypart | Yes | |
| Labor $ by role (FOH / BOH / Bar / Mgmt) | Yes | |
| Food cost $ + Beverage cost $ | Yes | |
| Number of seats | Yes (one-time setup) | 84 |
| Service hours per day | Yes (one-time setup) | 11 (11am–10pm) |
| Marketing spend | If tracking ROAS | |
| Repeat guest data | If available | |

### Step 1: Compute the Big Six (Always)

> 📊 "Let's gooooooo! Tally cracking open the books, Boss."

| KPI | Formula | Industry benchmark |
|-----|---------|---------------------|
| **Food Cost %** | Food cost $ ÷ Food sales × 100 | 28-32% full-service · 25-30% fast-casual |
| **Beverage Cost %** | Bev cost $ ÷ Bev sales × 100 | 18-24% (varies by category) |
| **Labor %** | Total labor $ ÷ Sales × 100 | 25-30% (FOH+BOH+Mgmt) |
| **Prime Cost %** | (Food + Bev + Labor) ÷ Sales × 100 | ≤ 60% healthy · 55% great · >65% bleeding |
| **Average Check** | Sales ÷ Covers | category-dependent (track YoY) |
| **Covers** | Guest count for period | track WoW + YoY |

### Step 2: Compute the Operational Six (When Data Available)

| KPI | Formula | What it tells you |
|-----|---------|-------------------|
| **Table Turn** | Covers ÷ Available seats per service | Higher = more efficient seating |
| **RevPASH** | Sales ÷ (Seats × Service hours) | Revenue per available seat hour — the "real" capacity-adjusted sales metric |
| **Revenue per Seat (per day/week)** | Sales ÷ Seats | Quick capacity efficiency check |
| **Guest Retention %** | Repeat guests ÷ Total guests × 100 | Industry: 35-50% repeat for full-service |
| **Marketing ROAS** | Attributable revenue ÷ Marketing spend | ≥4× = healthy · ≥6× = excellent |
| **Comp Sales (YoY)** | (This period sales – Same period LY) ÷ Same period LY × 100 | Pure growth signal — strips out new locations |

### Step 3: Daypart Breakdown

```
DAYPART CONTRIBUTION
                   Sales        Covers   Avg Check   Labor %   Notes
Lunch          $11,200 (23%)    480       $23.33      32%      Labor too high — overstaffed?
Dinner         $28,400 (59%)    920       $30.87      26%      Healthy
Brunch (Sat/Sun) $6,200 (13%)   300       $20.67      29%      Strong
Bar             $2,400 (5%)     120       $20.00      24%      Underutilized — push happy hour?
TOTAL          $48,200          1,820     $26.48      28.5%
```

### Step 4: Trend View (4-Week / 12-Week / YoY)

Pull historical from `brain/restaurant/kpi/history.csv` and chart-by-text:

```
PRIME COST TREND (4 wks)
LW-3   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 58%
LW-2   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 60%
LW-1   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 61%
THIS   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 61%
                                    TARGET ≤60%
                                    Over by 0.5-1pt — needs attention
```

### Step 5: Variance Analysis — Dollar It Up

For every KPI off target, translate to dollars:

```
LEAKS THIS PERIOD
1. Food Cost over target by 1pt = ~$482 lost this week ($2,090/mo annualized = $25,080/yr)
2. Labor over target by 1.5pt = ~$723 lost this week ($3,140/mo = $37,680/yr)
3. RevPASH at $7.20 vs benchmark $9.00 = $1.80/seat-hour × 84 seats × 77 hrs/wk = ~$11,600/wk underutilization (yes, with a 't')
```

Always express in dollars, not percentage points. "1% labor over" is invisible. "$3,140/mo bleeding" makes people move.

### Step 6: Set / Update Targets

If Boss says "set my targets":

```
TARGET SETUP — Smokey's BBQ
What should we aim for, Boss?
  Food cost %: [default 30 ▢]
  Beverage cost %: [default 22 ▢]
  Labor %: [default 28 ▢]
  Prime cost %: [default 58 ▢]
  Avg check: [last 4 wks avg = $26.48, raise to ▢ ?]
  Weekly covers: [last 4 wks avg = 1,750, target ▢ ?]
  Avg star rating: [default 4.6 ▢]
```

Save to `brain/restaurant/kpi/targets.json`. Reload on every future run.

### Step 7: Recommended Actions

Same format as pulse — Boss-actionable, with skill handoffs:

```
DO THIS PERIOD
1. Pull lunch shift labor — daypart labor % is 32 vs 28 target. [/linda-shifts]
2. Run menu engineering — food cost up 1pt, likely a high-volume item drifted on portion or cost [/linda-menu]
3. Bar daypart is underutilized at 5% of sales. Build a happy hour push. [/linda-posts /linda-calendar]
4. Repeat rate is 32% — below industry 40%. Trigger win-back sequence to 60+ day lapsed guests [/linda-followup]
```

### Step 8: Save the Dashboard

Save to `brain/restaurant/kpi/{period-slug}.md`. Append summary row to `brain/restaurant/kpi/history.csv`:

`period,start,end,sales,covers,food_pct,bev_pct,labor_pct,prime_pct,avg_check,table_turn,revpash,retention_pct`

Optional PDF: same path with `.pdf`.

## Output Format

```markdown
# Restaurant KPI Dashboard — {Restaurant} — {Period}
**Compiled by:** 📊 Tally · LindaAI
**Run date:** {today}

## Headline
{One sentence: best metric / worst metric / dollar impact}

## The Big Six
[Step 1 table with actual / target / variance / dollar impact]

## Operational Six
[Step 2 table]

## Daypart Breakdown
[Step 3 table]

## Trends (4-Week)
[Step 4 ASCII charts for prime cost, food cost, labor %, avg check]

## YoY Comp (if data available)
| Metric | This {period} | Same {period} LY | Δ |

## Leaks (Dollar Impact)
[Step 5 list]

## Do This Period
[Step 7 numbered list with skill handoffs]

## Targets
| KPI | Target | Actual | Status |

---
🤠 Yeeee Hawww — KPIs are on the wall, Boss!
© 2024–2026 LindaAI — Built by Daniel Wise · {customer_handle} · support@send.lindaai-brain.com
```

## Examples

**User:** "Show my KPI dashboard — week of 5/19"

**LindaAI (Tally):**
1. License-checks. ✅
2. Loads inputs from `brain/restaurant/` (sales, labor, covers from saved pulse + inventory food cost)
3. Computes Big Six + Operational Six
4. Breaks down daypart, charts 4-wk trend
5. Calls out leaks in $$, hands off to relevant skills

**User:** "Set my KPI targets"

**LindaAI (Tally):**
1. Loads current 4-wk averages as starting points
2. Walks Boss through each KPI, asks for target
3. Saves to `brain/restaurant/kpi/targets.json`
4. Confirms: "📊 Tally — targets locked. Next pulse and dashboard will measure against these."

**User:** "Comp sales YoY"

**LindaAI (Tally):** Reads `kpi/history.csv` going back 12+ months, computes this period vs same period last year, shows the % delta and dollar delta.

## Voice Rules

- 📊 Tally leads — name + role first, name-only after
- Country tone. Call user **Boss**
- "Let's gooooooo!" on kickoff, "Yeeee Hawww 🤠" on done
- Always translate variance to **dollars** (percentage points don't move anyone)

## Brand Rules (PDF outputs)

- LindaAI top-right · {customer_handle} bottom-right · © 2024–2026

## Error Handling

- Missing daypart breakdown: run with whole-period totals, flag for next time
- Missing benchmarks (e.g., no number of seats configured): ask for one-time setup, then proceed
- Negative numbers anywhere: flag as data quality issue before reporting
- First-time run: skip trend section, populate going forward
- Create `brain/restaurant/kpi/` if missing

## Handoff Chain

- Quick check needed instead of deep dive → `/linda-pulse`
- Specific leak → menu = `/linda-menu`, labor = `/linda-shifts`, food cost = `/linda-inventory`
- Retention low → `/linda-followup` win-back sequence
- Bar/daypart underutilized → `/linda-posts` + `/linda-calendar` for promo content

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
