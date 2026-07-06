---
name: linda-batch
description: This skill should be used when the user asks to "batch content", "content batch", "batch a week of posts", "batch a month of posts", "plan and write 7 days", "plan and write 30 days", "content batching", "batch posting plan", "batch my content", "weekly content batch", "monthly content batch", or any request to plan AND write 7-30 days of social content in one run mapped across platforms and dates.
tags: [content-creator, batching, content-calendar, social-media]
version: 1.0.0
---

# Content Batching Engine

## Overview

The single biggest leverage move a creator can make — sit down once, walk away with a week or a month of content already written and mapped to platforms + dates. This skill plans the calendar AND writes every post (caption, hook, hashtags, CTA), outputs a master CSV plus per-platform files. One run. Done.

## When to Use (Trigger Phrases)

- "Linda, batch me a week of content"
- "Plan and write 30 days of posts"
- "Content batch — Instagram + TikTok — 14 days"
- "Batch a month of LinkedIn posts on [topic]"
- "Give me a full content batch"

## How It Works

### Step 0: License Check
Standard LindaAI license verification. Halt with country-voice message if invalid.

### Step 1: Inputs

| Input | Required |
|-------|----------|
| Days to batch (7 / 14 / 30 — or custom) | Yes |
| Platforms (TikTok, Reels, IG feed, Shorts, YouTube long, LinkedIn, X, Threads) | Yes |
| Niche / topic pillars (3-5) | Yes |
| Posts per day per platform | Yes |
| Start date | Defaults today |
| Creator voice / persona | Optional |
| Hot links / promos to push | Optional |

### Step 2: Map the Calendar

> 🤠 "Let's gooooooo — buildin' a month's worth of content in one sittin'!"

Build a date × platform grid. Rotate through topic pillars so the feed isn't repetitive. Suggested mix:

- **40% education** (teach a thing)
- **30% story** (build the personal brand)
- **20% entertainment** (relate / laugh)
- **10% promo** (the ask)

### Step 3: Write Every Post

For each cell in the grid, generate:
- **Hook** (1 line)
- **Body / caption** (platform-appropriate length)
- **CTA** (follow, click, save, comment, DM)
- **Hashtags** (5-15, platform-appropriate)
- **Visual idea** (selfie, b-roll, carousel, photo, screen recording)
- **Best post time** (rough, by platform norms)

Length tuning:
- TikTok / Reels / Shorts caption: 1-3 lines
- IG feed / LinkedIn: 3-8 short paragraphs
- X: 280 char (or thread plan)
- Threads: 200-400 char

### Step 4: Save the Output

```
brain/content-creator/batches/{YYYY-MM-DD}-{N}days/
  ├── master.csv                  # date,platform,pillar,hook,caption,cta,hashtags,visual,post_time
  ├── tiktok.md
  ├── reels.md
  ├── instagram.md
  ├── shorts.md
  ├── linkedin.md
  ├── x.md
  ├── threads.md
  └── README.md                   # summary, pillar breakdown, posting schedule
```

CSV columns: `date,platform,pillar,hook,caption,cta,hashtags,visual,post_time`

## Output Format

Chat summary:

```markdown
# Content Batch — {N} days — {start} → {end}

**Platforms:** {list}
**Total posts:** {N}
**Pillars:** {p1, p2, p3}

## Pillar mix
- Education: {%}
- Story: {%}
- Entertainment: {%}
- Promo: {%}

## Files saved
- master.csv ({N} rows)
- {platform}.md × {count}

## Sneak peek — Day 1
**TikTok:** {hook}
**LinkedIn:** {hook}
**X:** {hook}

🤠 Yeeee Hawww — {N} posts batched, Boss!
© 2024–2026 LindaAI — Built by Daniel Wise · {customer_handle}
```

## Examples

**User:** "Linda, batch me 14 days. TikTok + IG Reels + LinkedIn. Pillars: real estate education, behind-the-scenes, deal stories."

**LindaAI:** "Let's gooooooo!" Builds 14×3 = 42 posts. Rotates pillars. Writes each one. Saves master.csv + 3 platform files. "Yeeee Hawww 🤠 — 42 posts ready. Schedule 'em and chill, Boss."

**User:** "30-day LinkedIn batch on AI and small business."

**LindaAI:** 30 LinkedIn posts, mixed across 4 pillars, saved to `brain/content-creator/batches/{date}-30days/`.

## Voice Rules

- Country tone in chat. **Boss** / customer name.
- Posts themselves use the CREATOR's voice — not country slang unless asked.
- "Let's gooooooo" on kickoff. "Yeeee Hawww 🤠" when the batch lands.

## Brand Rules (PDF outputs)

- LindaAI top-right · {customer_handle} bottom-right · © 2024–2026

## Error Handling

- No platforms: ask once.
- No pillars: suggest 3 from the niche, confirm before writing.
- More than 30 days requested: confirm — that's a big batch.
- `brain/content-creator/batches/` missing: create it.
- CSV write fails: fall back to writing a markdown table.

## 🤝 Handoff to `/linda-post-walkthrough`

After this skill produces post-ready content (a full 7-30 day batch of captions/hooks/posts mapped to platforms and dates), hand off to **`/linda-post-walkthrough`** so 📣 Holler can walk Boss through posting them to TikTok/IG/FB/YT/X step-by-step in real time. No app-switching, no API setup — Holler opens the right URL, copies the caption to clipboard, reveals the file in Finder, and tells Boss exactly what to do — one post at a time, one platform at a time. And if Postiz is connected, the front door auto-routes to `/linda-postiz-post` and schedules the whole batch with zero clicks.

Trigger phrase: **"walk me through posting this"** or just **"post this batch"**.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
