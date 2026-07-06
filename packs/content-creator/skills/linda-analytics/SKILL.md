---
name: linda-analytics
description: This skill should be used when the user asks to "import analytics", "import TikTok export", "import IG insights", "import YouTube analytics", "analytics rollup", "weekly analytics", "trend report", "creator analytics", "cross-platform analytics", "what's my CTR", "follower growth", "best post this week", "analyze my content performance", or any request to ingest CSV exports from social platforms and roll up cross-platform performance.
tags: [content-creator, analytics, reporting, growth]
version: 1.0.0
---

# Cross-Platform Analytics Rollup

## Overview

Eats the CSV exports TikTok, Instagram, and YouTube hand out and spits back a clean weekly trend report — views, CTR, follower growth, watch time, top posts, dead posts, and the patterns the creator can't see when they're staring at three different dashboards. One number, one direction arrow, one recommendation. Stop guessing what's working.

## When to Use (Trigger Phrases)

- "Linda, import this TikTok analytics CSV"
- "Roll up my analytics for the week"
- "Cross-platform performance report"
- "What's my best post this week?"
- "Follower growth trend"
- "Analyze last month's content"

## How It Works

### Step 0: License Check
Standard LindaAI license verification. Country-voice halt on failure.

### Step 1: Inputs

| Input | Required |
|-------|----------|
| CSV exports (TikTok / IG / YouTube) | At least 1 |
| Reporting window (week / month / custom) | Yes |
| Goal metric (views / follows / engagement / clicks) | Optional |

Accepted exports:
- **TikTok Studio** — Overview + Content + Followers exports
- **IG Insights** — Reach + Content + Audience exports
- **YouTube Studio** — Channel Analytics + Top Videos export

### Step 2: Normalize the Data

> 🤠 "Let's gooooooo — crunchin' the numbers!"

Map every platform's columns into a common schema:

| Field | Notes |
|-------|-------|
| date | YYYY-MM-DD |
| platform | tiktok / ig / youtube |
| post_id | platform native id |
| post_type | reel / short / video / photo / carousel / story |
| views | impressions where applicable |
| watch_time_sec | total |
| avg_view_duration | sec |
| likes | |
| comments | |
| shares | |
| saves | |
| follows_from_post | when available |
| ctr | clicks/views (where avail) |

Save normalized data to `brain/content-creator/analytics/raw/{week}.csv`.

### Step 3: Compute the Rollup

Calculate per platform AND combined:
- Total views (and Δ vs prior period)
- Total watch time
- Avg engagement rate (likes+comments+shares+saves / views)
- Follower growth (start → end)
- Top 5 posts by views
- Top 5 posts by engagement rate
- Bottom 3 posts (what flopped)
- CTR if link-bearing post

### Step 4: Surface the Trend

Look for patterns:
- Hook-style → views correlation
- Posting time → reach correlation
- Length buckets (under 15s, 15-30, 30-60) → completion rate
- Pillar (education / story / entertainment / promo) → follow rate

Pick the **ONE biggest insight** and the **ONE thing to do more of**.

### Step 5: Save the Report

```
brain/content-creator/analytics/
  ├── raw/{week}.csv
  └── reports/{YYYY-WW}-rollup.md
```

## Output Format

```markdown
# Analytics Rollup — Week of {YYYY-MM-DD}

## Headline
{one-sentence summary of the week}

## Totals
| Platform | Views | Δ | Watch hrs | Engagement | Follows |
|----------|-------|---|-----------|------------|---------|
| TikTok | {N} | {±%} | {hrs} | {%} | {±N} |
| Instagram | {N} | {±%} | {hrs} | {%} | {±N} |
| YouTube | {N} | {±%} | {hrs} | {%} | {±N} |
| **Total** | **{N}** | **{±%}** | **{hrs}** | **{%}** | **{±N}** |

## Top 5 posts
1. [{platform}] {hook} — {views} views, {engagement}%
2. ...

## Bottom 3 (what flopped)
- [{platform}] {hook} — {views} views — likely cause: {note}

## Pattern of the week
{one biggest insight backed by data}

## Do more of
{ONE specific recommendation}

## Cut
{ONE thing to stop doing}

---
🤠 Yeeee Hawww — week's tape is broken down, Boss!
© 2024–2026 LindaAI — Built by Daniel Wise · {customer_handle}
```

## Examples

**User:** "Linda, import these 3 CSVs — TikTok, IG, YouTube — and roll up the week."

**LindaAI:** "Let's gooooooo!" Normalizes, computes deltas, finds top/bottom posts, surfaces pattern. "Yeeee Hawww 🤠 — TikTok up 38%, IG flat, YouTube down 12%. Pattern: 22-second posts crushed 60-second ones. Do more of: short-form education hooks. Cut: long talking-head intros."

**User:** "What was my best post last month?"

**LindaAI:** Reads `brain/content-creator/analytics/raw/`, computes top by views and by engagement, returns both with the hook line.

## Voice Rules

- Country tone in chat. **Boss** / customer name.
- Reports stay clean and data-first — country flavor in chat / headlines, not in the tables.
- "Let's gooooooo" on kickoff. "Yeeee Hawww 🤠" on save.

## Brand Rules (PDF outputs)

- LindaAI top-right · {customer_handle} bottom-right · © 2024–2026

## Error Handling

- CSV columns don't match known schemas: ask the user which platform / show first 3 rows.
- Missing prior period for delta: report current only and note "no baseline yet."
- Empty CSV: bail, ask for re-export.
- `brain/content-creator/analytics/` missing: create it with `raw/` and `reports/` subfolders.
- Numbers off by 10x (decimal mis-parse): re-parse with locale fallback.

## 🤝 Handoff to `/linda-post-walkthrough`

After this skill produces post-ready content (best-post-of-the-week screenshot, milestone announcement, "we hit X views" social proof graphic), hand off to **`/linda-post-walkthrough`** so 📣 Holler can walk Boss through posting it to TikTok/IG/FB/YT/X step-by-step in real time. No app-switching, no API setup — Holler opens the right URL, copies the caption to clipboard, reveals the file in Finder, and tells Boss exactly what to do.

Trigger phrase: **"walk me through posting this"** or just **"post this"**.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
