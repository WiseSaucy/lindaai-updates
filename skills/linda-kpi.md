---
name: linda-kpi
description: This skill should be used when the user asks to "check my KPIs", "show my dashboard", "how are my numbers", "KPI report", "KPI dashboard", "track my metrics", "set up KPIs", "define my KPIs", "update KPIs", "what metrics should I track", "how is the business doing", "performance dashboard", "are we on track", "scorecard", "business scorecard", "weekly numbers", "monthly metrics", "revenue tracking", "conversion rate", "lead metrics", "content output tracking", "deal metrics", "am I hitting my targets", "metric report", "business health check", "numbers check", "how are we performing", "update my targets", "set new KPI targets", "what's trending up", "what's trending down", or any request related to defining, tracking, or reporting on key performance indicators across their business.
version: 1.0.0
---

# KPI Dashboard

## Overview

LindaAI defines, tracks, and reports on Key Performance Indicators across all your businesses and revenue streams. You set up your KPIs once — revenue targets, deal counts, content output, lead conversion rates, customer metrics, whatever matters — and then `/kpi-dashboard` lets LindaAI pull the current status, show trend arrows (up/down/flat), highlight what is on track vs. off track, and deliver specific recommendations for any metric that is underperforming. This is how a $180K/year executive assistant keeps you informed: you never have to ask "how are we doing?" — you already know.

## When This Skill Applies

- User wants to set up KPIs for the first time
- User asks "how are my numbers?" or "check my KPIs"
- User wants a business performance dashboard
- User says "update my KPIs" with new data
- User asks if they are on track for their goals
- User wants to define new metrics to track
- User asks for a weekly or monthly metrics report
- User wants to know which areas of the business are underperforming
- User says "scorecard" or "business health check"
- User wants to change their targets or add a new KPI
- User asks "what should I be tracking?"

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

### Step 0: Determine the Action

Parse the user's request into one of three modes:

- **`setup`** — First-time KPI definition or adding new KPIs
- **`update`** — Logging new data points for existing KPIs
- **`report`** — Generating the current dashboard (default if no action specified)

If no arguments are provided, default to `report`. If `brain/pipeline/kpis.md` does not exist, automatically switch to `setup`.

### Step 1: Setup — Define KPIs (first run or adding new ones)

If this is the first time, guide the user through KPI definition. Start by reading `brain/goals.md` to understand their objectives, then suggest KPIs aligned to those goals.

**Default KPI categories (propose these, let user customize):**

| Category | Example KPIs |
|----------|-------------|
| Revenue | Monthly revenue, MRR/ARR, average deal size, revenue per client |
| Pipeline | Total leads, qualified leads, deals in negotiation, close rate |
| Sales Activity | Outreach calls/emails per week, proposals sent, follow-ups completed |
| Content & Marketing | Posts per week, followers gained, engagement rate, email list size, CTR |
| Client/Customer | Active clients, churn rate, NPS/satisfaction, referrals received |
| Operations | Tasks completed per week, SOP compliance, response time |
| Financial Health | Cash runway, profit margin, accounts receivable, burn rate |
| Personal/Growth | Hours worked, gym sessions, learning hours, networking events |

For each KPI the user wants to track, capture:

| Field | Description | Example |
|-------|-------------|---------|
| Name | What the metric is called | "Monthly Revenue" |
| Category | Which category it falls under | "Revenue" |
| Current Value | Where the metric stands today | "$12,500" |
| Target | What they are aiming for | "$25,000" |
| Frequency | How often it gets updated | Weekly / Monthly / Daily |
| Source | Where the data comes from | "Stripe dashboard", "manual count", "analytics" |
| Priority | How critical this KPI is | High / Medium / Low |

Save the KPI definitions to `brain/pipeline/kpis.md` using this format:

```markdown
# KPI Dashboard

> **Last Updated:** {YYYY-MM-DD}
> **Review Cadence:** {Weekly / Bi-weekly / Monthly}
> **Total KPIs Tracked:** {count}

---

## Active KPIs

### Revenue

| KPI | Target | Current | Trend | Status | Last Updated |
|-----|--------|---------|-------|--------|-------------|
| Monthly Revenue | $25,000 | $12,500 | -- | Off Track | {date} |
| Average Deal Size | $5,000 | $4,200 | -- | Approaching | {date} |

### Pipeline

| KPI | Target | Current | Trend | Status | Last Updated |
|-----|--------|---------|-------|--------|-------------|
| Active Leads | 50 | 23 | -- | Off Track | {date} |
| Close Rate | 25% | 18% | -- | Off Track | {date} |

### {Category}...

---

## History Log

| Date | KPI | Previous | New Value | Change | Notes |
|------|-----|----------|-----------|--------|-------|
| {date} | {name} | {old} | {new} | {+/-/%} | {context} |
```

### Step 2: Update — Log New Data

When the user provides new numbers:

1. Read `brain/pipeline/kpis.md`
2. Parse which KPIs the user is updating (match by name, fuzzy if needed)
3. For each KPI being updated:
   - Record the previous value
   - Set the new current value
   - Calculate the change (absolute and percentage)
   - Determine the trend arrow:
     - **up arrow** (moving toward target and improving)
     - **down arrow** (moving away from target or declining)
     - **right arrow** (flat, less than 2% change)
   - Update the status:
     - **On Track** — current value is at or above target, or trending to hit target by deadline
     - **Approaching** — within 80% of target and trending positively
     - **Off Track** — below 60% of target or trending negatively
     - **Critical** — below 40% of target or declining for 3+ consecutive periods
     - **Exceeded** — above target
4. Append each change to the History Log with timestamp
5. Update `> **Last Updated:**` to today
6. Save the file
7. Report what changed and flag any KPIs that flipped status (e.g., went from Approaching to Off Track)

**Accepting bulk updates:**

The user can say things like:
- "Revenue hit $18K this month, closed 4 deals, posted 12 times this week"
- Parse all numbers and match them to the closest KPIs

### Step 3: Report — Generate the Dashboard

1. Read `brain/pipeline/kpis.md`
2. Read `brain/goals.md` for context on what matters most right now
3. Read today's daily log (`brain/daily/{YYYY-MM-DD}.md`) if it exists

Generate the dashboard in this format:

```markdown
# KPI Dashboard — {Date}

> **Period:** {Week of / Month of} {date range}
> **Overall Health:** {STRONG / SOLID / MIXED / CRITICAL}
> **KPIs On Track:** {X} of {Y} ({Z}%)

---

## Executive Summary

{2-3 sentences: What is going well, what needs attention, and the single most important thing to focus on this week to move the needle.}

---

## Scorecard

### Revenue & Financial
| KPI | Target | Current | Trend | Status | Gap |
|-----|--------|---------|-------|--------|-----|
| {name} | {target} | {value} | {arrow} | {status} | {how far from target} |

### Pipeline & Sales
| KPI | Target | Current | Trend | Status | Gap |
|-----|--------|---------|-------|--------|-----|

### Content & Marketing
| KPI | Target | Current | Trend | Status | Gap |
|-----|--------|---------|-------|--------|-----|

### Operations & Growth
| KPI | Target | Current | Trend | Status | Gap |
|-----|--------|---------|-------|--------|-----|

---

## Highlights

### What is Working (On Track or Exceeded)
- {KPI}: {value} vs {target} — {why it is working, what to keep doing}

### What Needs Attention (Off Track or Critical)
- {KPI}: {value} vs {target} — {specific diagnosis of why and what to do about it}

---

## Recommendations

1. **{Highest priority recommendation}** — {specific action, tied to the most impactful off-track KPI}
2. **{Second recommendation}** — {specific action}
3. **{Third recommendation}** — {specific action}

---

## Week-over-Week Trend (last 4 periods)

| KPI | 4 wks ago | 3 wks ago | 2 wks ago | Last wk | This wk | Direction |
|-----|-----------|-----------|-----------|---------|---------|-----------|
| {name} | {val} | {val} | {val} | {val} | {val} | {arrow} |

---

## Goal Alignment Check

| Goal (from goals.md) | Related KPIs | Combined Status | Risk |
|----------------------|-------------|-----------------|------|
| {quarterly goal} | {KPI names} | {On Track / At Risk / Off Track} | {notes} |

---

🤠 *Generated by LindaAI* 🏇
*Next recommended update: {date based on cadence}.*
```

4. Display the full dashboard in the terminal
5. Append a summary to today's daily log at `brain/daily/{YYYY-MM-DD}.md`
6. If the daily log does not exist, create it with the KPI summary as the first entry

### Step 4: Intelligent Recommendations

For every Off Track or Critical KPI, generate a specific recommendation. Not generic advice — specific to the user's numbers and context.

**Recommendation framework:**

1. **Diagnose:** Why is this metric underperforming? (Look at related KPIs, recent history, patterns)
2. **Prescribe:** What specific action would move this number? (One action, not five)
3. **Quantify:** If they do X, the expected impact is Y
4. **Timeline:** When should they see improvement if they start now?

Example:
- "Monthly revenue is at $12,500 vs. target of $25,000 (50%). Your close rate dropped from 22% to 18% while lead volume stayed flat. The fastest lever is follow-up speed — your pipeline shows 8 leads in 'contacted' stage with no activity in 7+ days. Work those 8 leads this week. If you close 2, that adds approximately $8,400 at your current average deal size."

## Output Format

The dashboard is displayed directly in the terminal. A condensed version is also saved to the daily log.

**Terminal output:** Full dashboard as shown in Step 3 above.

**Daily log entry:**

```markdown
## KPI Check — {time}

**Overall:** {STRONG/SOLID/MIXED/CRITICAL} — {X}/{Y} KPIs on track
**Top Win:** {best performing KPI and value}
**Top Risk:** {worst performing KPI and gap}
**Action:** {#1 recommendation}
```

## Example Usage

**User:** "Set up my KPIs"

**AI:** Reads goals.md, proposes KPIs aligned to their quarterly objectives. Asks the user to confirm, modify, or add. Saves the initial KPI definitions to `brain/pipeline/kpis.md` with current values and targets.

**User:** "Update my numbers — revenue was $18K this month, I closed 6 deals, and I posted 15 times on social media"

**AI:** Matches "revenue" to Monthly Revenue, "6 deals" to Deals Closed, "15 posts" to Content Output. Updates each, calculates trends and status changes, saves to kpis.md with history log, and reports what moved.

**User:** "/kpi-dashboard"

**AI:** Generates the full dashboard, shows trend arrows, highlights 2 off-track KPIs with specific recommendations, notes goal alignment, and appends summary to today's daily log.

**User:** "Am I on track for Q1?"

**AI:** Cross-references KPI actuals against goals.md quarterly targets. Shows which goals are supported by on-track KPIs and which are at risk based on current trajectory. Provides a projected end-of-quarter estimate for each goal.

**User:** "Add a new KPI for email list subscribers"

**AI:** Adds the KPI to the Content & Marketing category in kpis.md, asks for current value and target, sets it up with the appropriate tracking cadence.

## Error Handling

- **If `brain/pipeline/kpis.md` does not exist:** Automatically switch to setup mode. Tell the user: "No KPIs defined yet. Let me help you set up your dashboard. I'll start by reading your goals to suggest relevant metrics."
- **If `brain/pipeline/` directory does not exist:** Create it automatically before proceeding.
- **If the user provides numbers but no KPIs match:** List the defined KPIs and ask: "I couldn't match '{input}' to an existing KPI. Here are your current KPIs: {list}. Which one should I update? Or should I create a new KPI for this?"
- **If `brain/goals.md` does not exist during setup:** Proceed without goal alignment. Note: "No goals file found. I'm setting up KPIs based on your input only. Create `brain/goals.md` to enable automatic goal-to-KPI alignment."
- **If the user asks for a trend report but there is only one data point:** Show the current values without trends. Note: "This is your first data point — trends will appear after your next update. I recommend updating {cadence} to build a useful trend line."
- **If KPI data is stale (last updated more than 2x the stated cadence):** Flag it prominently: "WARNING: {X} KPIs haven't been updated in {Y} days. Stale data means blind spots. Here's what needs refreshing: {list}."
- **If the daily log directory does not exist:** Create `brain/daily/` before saving.
- **If a KPI has been Critical for 3+ consecutive updates:** Escalate: "ESCALATION: {KPI name} has been in Critical status for {X} consecutive periods. This is no longer a dip — it is a pattern. Recommend: {specific structural change, not just 'try harder'}."


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
