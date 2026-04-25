---
name: linda-pipeline
description: This skill should be used when the user asks to "check my pipeline", "pipeline report", "pipeline sync", "deal pipeline", "show me my deals", "how many deals are in my pipeline", "deal velocity", "stale deals", "revenue forecast", "what's closing this week", "pipeline intelligence", "CRM sync", "CRM report", "pipeline summary", "deal stages", "show pipeline by stage", "which deals are stuck", "projected revenue", "deal forecast", "what deals are closing soon", "pipeline health", "deal flow report", "sales pipeline", "where are my deals", "top deals", "pipeline status", "sync my CRM", "pull pipeline data", "pipeline overview", "how is deal flow", "any stale deals", "deals with no activity", or any request related to viewing, analyzing, or reporting on their deal pipeline and CRM data.
version: 1.0.0
---

# CRM Pipeline Sync

## Overview

LindaAI delivers pipeline intelligence on demand. It pulls your deal pipeline data, analyzes it, and puts a report on your desk that a $180K/year chief of staff would be proud of every Monday morning. Total deals by stage, deal velocity (average days in each stage), stale deals flagged (no activity in X days), projected close dates, revenue forecast for the month and quarter, and the top 3 deals most likely to close this week. Works with deal data stored in `brain/pipeline/leads/` or can be extended to pull from Pipedrive, HubSpot, or any CRM with API access.

## When This Skill Applies

- User asks "how is my pipeline?" or "show me my deals"
- User wants to know which deals are closing soon
- User asks about stale deals or stuck deals
- User wants a revenue forecast
- User asks "what's my deal velocity?"
- User says "pipeline report" or "pipeline sync"
- User asks "which deals should I focus on this week?"
- User wants deals grouped by stage
- User asks for a CRM sync or CRM report
- User mentions Pipedrive, HubSpot, or any CRM data
- User asks "how many deals am I working?"
- User wants projected revenue for the month or quarter

## How It Works

### License Check

Before proceeding, verify the LindaAI license:

1. Read `~/.claude/linda-license.json`
2. If the file does not exist, stop and tell the user:
   > 🤠 "Whoa there, partner — no LindaAI license found on this machine. You'll need a valid license to use LindaAI skills. Reach out to get set up and we'll have you in the saddle in no time."
   Do not proceed with any other steps.
3. If today's date is past the `expiration_date`, stop and tell the user:
   > 🤠 "Whoa there, partner — your LindaAI license expired on [expiration_date]. Reach out to renew and we'll get you back in the saddle." 🏇
   Do not proceed with any other steps.
4. If `status` is not `"active"`, stop and tell the user:
   > 🤠 "Whoa there, partner — your LindaAI license is currently [status]. Reach out to get this sorted and we'll have you riding again in no time."
   Do not proceed with any other steps.
5. **Server Verification (tamper check):** If the license file contains an `api_url` field, use WebFetch to check `{api_url}/v1/licenses/validate/{license_key}`. Parse the JSON response.
   - If the server responds with `"valid": false`, the local license has been tampered with. Stop and tell the user:
     > 🤠 "Hold up, partner — your license didn't check out with the server. Something's not matching up. Reach out to support to get this straightened out."
     Then use WebFetch to POST a tamper alert to `{api_url}/v1/licenses/tamper-alert` with JSON body: `{"license_key": "[key]", "local_expiration": "[local expiration_date]", "server_expiration": "[server expires from response]", "local_status": "[local status]", "details": "Local file passed but server validation failed"}`. Do not proceed.
   - If the server is unreachable or returns an error, proceed anyway (allow offline use — don't block paying customers because of a server hiccup).
   - If the server responds with `"valid": true`, proceed.
6. If all checks pass, proceed.

### Step 0: Determine the Pipeline Source

Check for available data in this order:

1. **Local pipeline data:** `brain/pipeline/leads/` — individual lead/deal files (primary source)
2. **Pipeline summary:** `brain/pipeline/README.md` — dashboard overview
3. **KPI data:** `brain/pipeline/kpis.md` — for metric cross-referencing
4. **External CRM (if configured):** Check for CRM API credentials or MCP server connections

If a specific pipeline name is provided (e.g., `/pipeline-sync real-estate`), filter leads to that category.

### Step 1: Gather All Deal Data

Read ALL files in `brain/pipeline/leads/`. For each deal, extract:

| Field | Where to Find It | Fallback |
|-------|------------------|----------|
| Name | File header / `# Name` | Filename |
| Company | Contact Info table | "Unknown" |
| Stage | `> **Stage:**` line | "Unknown" |
| Deal Value | Deal Info → Estimated Value | $0 |
| Created Date | `> **Created:**` line | File creation date |
| Last Updated | `> **Last Updated:**` line | File modification date |
| Follow-Up Date | `> **Follow-Up Date:**` line | None |
| Next Action | Notes section (latest entry) | "None defined" |
| Source | Contact Info → Source | "Unknown" |
| Interaction Count | Count rows in Interaction History table | 0 |

### Step 2: Stage Analysis

Group deals by stage and calculate metrics for each:

**Standard Stages:**
| Stage | Definition |
|-------|-----------|
| New | Lead identified, no contact yet |
| Contacted | Initial outreach made, waiting for response |
| Qualified | Confirmed interest, fits criteria, worth pursuing |
| Negotiating | Active negotiation on terms, pricing, or scope |
| Proposal Sent | Formal proposal/offer submitted, awaiting decision |
| Closed-Won | Deal closed successfully |
| Closed-Lost | Deal did not close |

For each stage:
```
Count: {X} deals
Total Value: ${Y}
Average Days in Stage: {Z} days
Longest in Stage: {deal name} — {N} days
```

### Step 3: Deal Velocity Analysis

Calculate how fast deals move through your pipeline:

```
Average Time: New → Contacted: {X} days
Average Time: Contacted → Qualified: {X} days
Average Time: Qualified → Negotiating: {X} days
Average Time: Negotiating → Closed: {X} days
Full Cycle (New → Closed-Won): {X} days average
```

Compare against benchmarks:
- If full cycle > 60 days: "Your sales cycle is long. Look for friction points in {slowest stage}."
- If full cycle < 14 days: "Fast pipeline. Make sure you're not leaving money on the table by rushing deals."
- If any single stage averages > 50% of total cycle: "Deals are getting stuck in {stage}. This is your bottleneck."

### Step 4: Stale Deal Detection

A deal is stale if:
- **No activity** (Last Updated) in 7+ days for active stages (Contacted, Qualified, Negotiating)
- **No activity** in 3+ days for Proposal Sent stage
- **Follow-up date is past** and no update has been logged
- **Been in the same stage** for more than 2x the average time for that stage

For each stale deal, flag it with:
- Deal name and value
- Days since last activity
- Current stage
- Recommended action (follow up, re-qualify, or drop)

### Step 5: Revenue Forecast

Calculate projected revenue for current month and quarter:

**This Month:**
```
Already Closed (this month): ${X}
Weighted Pipeline:
  - Negotiating deals × 60% probability: ${Y}
  - Proposal Sent deals × 40% probability: ${Z}
  - Qualified deals × 20% probability: ${W}
Projected Total: ${X + Y + Z + W}
vs. Monthly Target (from kpis.md): ${target}
Gap/Surplus: ${difference}
```

**This Quarter:**
Apply the same weighted calculation, extending to the quarter. Factor in deal velocity to estimate how many current New/Contacted leads could convert by quarter end.

**Probability weights (conservative defaults):**
| Stage | Close Probability |
|-------|------------------|
| New | 5% |
| Contacted | 10% |
| Qualified | 20% |
| Negotiating | 60% |
| Proposal Sent | 40% |

### Step 6: Top Deals — Most Likely to Close This Week

Identify the 3 deals most likely to close in the next 7 days:

**Scoring criteria (weighted):**
| Factor | Weight | How to Score |
|--------|--------|-------------|
| Stage (further = higher) | 30% | Proposal Sent = 10, Negotiating = 7, Qualified = 4 |
| Recent activity | 25% | Updated today = 10, last 3 days = 7, last 7 days = 4, older = 1 |
| Deal value | 15% | Higher value = higher score |
| Follow-up is imminent | 15% | Today/tomorrow = 10, this week = 7, next week = 4 |
| Interaction density | 15% | More interactions = higher score |

Rank all active deals by composite score. Present the top 3 with:
- Deal name, value, stage
- Why it is likely to close (specific signals)
- Recommended next action to push it over the line

### Step 7: Generate the Pipeline Intelligence Report

```markdown
# Pipeline Intelligence Report — {Date}

> **Total Active Deals:** {count}
> **Total Pipeline Value:** ${amount}
> **Weighted Forecast (this month):** ${amount}
> **Pipeline Health:** {STRONG / HEALTHY / ATTENTION NEEDED / CRITICAL}

---

## Executive Summary

{3-4 sentences: pipeline health, biggest opportunity, biggest risk, one recommended action.}

---

## Pipeline by Stage

| Stage | Deals | Value | Avg Days | Longest |
|-------|-------|-------|----------|---------|
| New | {X} | ${Y} | {Z} days | {name} ({N} days) |
| Contacted | | | | |
| Qualified | | | | |
| Negotiating | | | | |
| Proposal Sent | | | | |
| **Active Total** | **{X}** | **${Y}** | | |
| Closed-Won (this month) | {X} | ${Y} | | |
| Closed-Lost (this month) | {X} | ${Y} | | |

---

## Top 3 Deals to Close This Week

### 1. {Deal Name} — ${Value}
- **Stage:** {stage}
- **Last Activity:** {date} ({days} ago)
- **Why it's hot:** {specific signals}
- **Next Action:** {what to do right now}

### 2. {Deal Name} — ${Value}
...

### 3. {Deal Name} — ${Value}
...

---

## Stale Deals (Need Attention)

| Deal | Value | Stage | Days Since Activity | Recommended Action |
|------|-------|-------|--------------------|--------------------|
| {name} | ${value} | {stage} | {days} | {follow up / re-qualify / drop} |

**Total value at risk from stale deals: ${amount}**

---

## Deal Velocity

| Transition | Average Days | Benchmark | Status |
|-----------|-------------|-----------|--------|
| New → Contacted | {X} | < 2 days | {OK / SLOW} |
| Contacted → Qualified | {X} | < 7 days | {OK / SLOW} |
| Qualified → Negotiating | {X} | < 14 days | {OK / SLOW} |
| Negotiating → Closed | {X} | < 21 days | {OK / SLOW} |
| **Full Cycle** | **{X}** | **< 45 days** | **{OK / SLOW}** |

**Bottleneck Stage:** {stage with highest average days}

---

## Revenue Forecast

### This Month
| Source | Amount |
|--------|--------|
| Closed-Won | ${X} |
| Weighted Pipeline | ${Y} |
| **Projected Total** | **${Z}** |
| Monthly Target | ${target} |
| **Gap/Surplus** | **${difference}** |

### This Quarter
| Source | Amount |
|--------|--------|
| Closed-Won (QTD) | ${X} |
| Weighted Pipeline | ${Y} |
| Velocity-Adjusted New Leads | ${Z} |
| **Projected Total** | **${W}** |
| Quarterly Target | ${target} |
| **Gap/Surplus** | **${difference}** |

---

## Recommendations

1. **{Highest priority action}** — {specific, tied to the biggest revenue opportunity or risk}
2. **{Second action}** — {specific}
3. **{Third action}** — {specific}

---

## Pipeline Trends (if historical data available)

| Metric | 4 wks ago | 3 wks ago | 2 wks ago | Last wk | This wk |
|--------|-----------|-----------|-----------|---------|---------|
| Active Deals | | | | | |
| Pipeline Value | | | | | |
| Deals Closed | | | | | |
| Revenue Closed | | | | | |
| Win Rate | | | | | |

---

🤠 *Generated by LindaAI* 🏇
*Next recommended sync: {date}.*
```

### Step 8: Save and Report

1. Display the full report in terminal
2. Save the report to `brain/research/pipeline-report-{YYYY-MM-DD}.md`
3. If `brain/pipeline/kpis.md` exists and has pipeline KPIs, update them with the latest numbers
4. Append a condensed summary to today's daily log at `brain/daily/{YYYY-MM-DD}.md`:

```markdown
## Pipeline Sync — {time}

**Active Deals:** {count} totaling ${value}
**Weighted Forecast (month):** ${amount} vs. ${target} target
**Top Deal:** {name} — ${value} — {stage}
**Stale Deals:** {count} — ${value} at risk
**Action:** {#1 recommendation}
```

## Example Usage

**User:** "Show me my pipeline"

**AI:** Reads all deal files from `brain/pipeline/leads/`, generates the full Pipeline Intelligence Report. Shows 12 active deals totaling $87K, 3 stale deals worth $22K that need follow-up, and identifies a $15K deal in negotiation as the #1 deal to close this week.

**User:** "/pipeline-sync"

**AI:** Same as above — full pipeline intelligence report with all metrics.

**User:** "Which deals are stuck?"

**AI:** Runs the stale deal detection (Step 4) and presents just the stale deals with recommended actions for each.

**User:** "What's my revenue forecast for this month?"

**AI:** Runs the revenue forecast (Step 5) and presents projected revenue from closed deals plus weighted pipeline, compared against the monthly target from kpis.md.

**User:** "What should I focus on this week?"

**AI:** Identifies the top 3 deals most likely to close (Step 6) and presents them with specific next actions. Also flags any stale deals that could be quick wins with a follow-up.

**User:** "/pipeline-sync real-estate"

**AI:** Filters deals to only those in the real estate category/pipeline and generates a focused report for that vertical.

## Error Handling

- **If `brain/pipeline/leads/` does not exist or is empty:** Report: "No deal data found. Your pipeline is empty. Use `/lead-tracker add [name]` to start tracking deals, or tell me about your current deals and I'll set up the pipeline."
- **If `brain/pipeline/leads/` exists but has no deals in active stages:** Report: "All deals are either closed or no active deals exist. Here's the closed deal history: {summary}. Time to fill the pipeline — what leads are you working on?"
- **If `brain/pipeline/kpis.md` does not exist:** Skip KPI cross-referencing. Note: "No KPI file found. Revenue forecasts won't be compared against targets. Run `/kpi-dashboard setup` to define targets."
- **If deal files are in inconsistent formats:** Parse what you can. For fields you can't extract, use fallback values (listed in Step 1). Note which deals have incomplete data: "Heads up: {X} deal files are missing key data (value, stage, or dates). Here's what needs cleaning up: {list}."
- **If no deals have been updated in 14+ days:** Lead with a warning: "WARNING: No pipeline activity in {X} days. Either you're not logging updates or deal flow has stalled. If deals are happening, update them. If they're not, that's the real problem."
- **If the user asks to sync with an external CRM (Pipedrive, HubSpot, etc.) but no integration exists:** Report: "External CRM sync is not configured. To connect Pipedrive/HubSpot, you'll need to add the relevant MCP server or API credentials. For now, I can work with local deal data in `brain/pipeline/leads/`. Want me to analyze what's there?"
- **If the user references a pipeline name that doesn't match any leads:** List the available categories/pipelines: "I didn't find any deals in a '{name}' pipeline. Your current deals span these categories: {list}. Which one did you mean?"


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
