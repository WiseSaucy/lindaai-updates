---
name: linda-calendar
description: This skill should be used when the user asks to "create a content calendar", "plan social media posts", "generate a posting schedule", "content calendar for the week", "content calendar for the month", "plan my posts", "social media plan", "what should I post", "content ideas", "content schedule", "posting calendar", "plan content for Instagram", "plan content for TikTok", "plan content for YouTube", "plan content for Facebook", "plan content for LinkedIn", "plan content for Twitter/X", "social media strategy", "batch content", "content batching plan", "2 week content plan", "monthly content plan", "weekly content plan", "multi-platform content", "post ideas", "caption ideas", "hashtag strategy", or anything related to planning, scheduling, or generating social media content across platforms.
version: 1.0.0
---

# Social Media Calendar

## Overview

Plans and generates a multi-platform content calendar with post ideas, captions, hashtags, and optimal posting times. The user specifies duration, platforms, and themes -- LindaAI builds a complete, actionable calendar. No guesswork, no staring at a blank screen. LindaAI maps out every post so you can just show up and execute. Output is saved as a structured markdown file that can be referenced daily for execution.

## When This Skill Applies

- User wants to plan social media content for any time period
- User asks for post ideas, caption ideas, or hashtag suggestions
- User wants a content calendar for specific platforms
- User says "what should I post this week?"
- User mentions content batching or batch planning
- User wants a multi-platform content strategy
- User asks for a posting schedule with times
- User wants help systematizing their content creation
- User mentions any combination of: Instagram, TikTok, YouTube, Facebook, LinkedIn, Twitter/X, Threads

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

### Step 1: Gather Requirements

Ask the user (or extract from their message) the following. Use sensible defaults if not provided:

| Input | Default |
|-------|---------|
| Duration | 1 week |
| Platforms | Instagram, TikTok, Facebook |
| Posting frequency | 1 post/day per platform |
| Themes/Topics | Derived from user's business or goals |
| Tone/Voice | Professional but conversational |
| Content types | Mix of educational, promotional, engagement, behind-the-scenes |

If `brain/goals.md` or `brain/knowledge-base/` exist, read them to understand the user's business, brand voice, and priorities for smarter content suggestions.

### Step 2: Research Current Trends (Optional)

If the user wants trend-aware content or asks for "what's working right now":

> 🤠 "Hold tight -- heading over yonder to gather up the details."

1. Use WebSearch to research current trends for their industry
2. Search for trending hashtags and content formats for each platform
3. Note any timely events, holidays, or cultural moments during the calendar period

### Step 3: Build the Calendar Structure

For each day in the specified duration, generate:

| Field | Description |
|-------|-------------|
| Date | YYYY-MM-DD and day of week |
| Platform | Which platform this post is for |
| Content Type | Educational, promotional, engagement, behind-the-scenes, story, reel, carousel, etc. |
| Topic/Idea | Specific post concept |
| Caption | Ready-to-use caption (or detailed draft) |
| Hashtags | 5-15 relevant hashtags (platform-appropriate) |
| Best Time | Optimal posting time for the platform |
| Media Notes | What visual/video is needed (photo, graphic, video clip, screen recording, etc.) |
| CTA | Call-to-action for the post |

### Step 4: Apply Platform-Specific Best Practices

**Instagram:**
- Reels: 15-60 seconds, trending audio, hook in first 2 seconds
- Carousels: 5-10 slides, educational or storytelling
- Stories: Behind-the-scenes, polls, questions, casual
- Feed posts: High-quality imagery, longer captions
- Best times: 11am-1pm, 7pm-9pm (user's timezone)
- Hashtags: 5-15 per post, mix of broad and niche

**TikTok:**
- 15-60 second videos, hook in first 1-2 seconds
- Trending sounds and formats
- Raw/authentic over polished
- Best times: 7am-9am, 12pm-3pm, 7pm-11pm
- Hashtags: 3-5 targeted hashtags

**YouTube:**
- Shorts: Under 60 seconds, vertical, hook immediately
- Long-form: 8-15 minutes, structured with chapters
- Thumbnails: Bold text, expressive face, contrasting colors
- Best times: Thursday-Saturday, 2pm-4pm
- Tags: 5-10 relevant tags

**Facebook:**
- Mix of text posts, images, videos, links
- Groups engagement alongside page posts
- Best times: 1pm-4pm weekdays
- Conversational tone, questions that prompt comments

**LinkedIn:**
- Professional insights, industry commentary, personal stories
- Text posts perform well (no link in initial post)
- Best times: Tuesday-Thursday, 8am-10am
- Hashtags: 3-5 professional hashtags

**Twitter/X:**
- Short, punchy takes (under 280 chars for engagement)
- Threads for longer content
- Best times: 8am-10am, 6pm-9pm
- Hashtags: 1-2 max

### Step 5: Organize Content Mix

Apply the content pillar framework across the calendar:

| Pillar | % of Content | Purpose |
|--------|-------------|---------|
| Educational | 40% | Teach something, share expertise, how-to |
| Engagement | 20% | Questions, polls, challenges, community interaction |
| Promotional | 20% | Products, services, offers, CTAs |
| Behind-the-Scenes | 10% | Day-in-the-life, process, team, personality |
| Trending/Timely | 10% | Current events, trending formats, cultural moments |

### Step 6: Save the Calendar

Save to `brain/content/calendar-{YYYY-MM-DD}-to-{YYYY-MM-DD}.md` with the full calendar.

If `brain/content/` does not exist, create it.

## Output Format

```markdown
# Content Calendar: {Start Date} to {End Date}

> **Platforms:** {list}
> **Frequency:** {X posts/day per platform}
> **Themes:** {themes}
> **Generated:** {date}

---

## Week 1: {Date Range}

### Monday, {Date}

**Instagram — Reel (Educational)**
- **Topic:** {specific post idea}
- **Caption:** {ready-to-post caption with line breaks and formatting}
- **Hashtags:** #tag1 #tag2 #tag3 #tag4 #tag5
- **Post Time:** 12:00 PM
- **Media:** {what to film/create}
- **CTA:** {call to action}

**TikTok — Video (Trending)**
- **Topic:** {specific post idea}
- **Caption:** {caption}
- **Hashtags:** #tag1 #tag2 #tag3
- **Post Time:** 7:00 PM
- **Media:** {what to film/create}
- **CTA:** {call to action}

---

### Tuesday, {Date}
{... same format ...}

---

## Content Summary

| Platform | Total Posts | Content Types |
|----------|-----------|---------------|
| Instagram | {N} | {breakdown} |
| TikTok | {N} | {breakdown} |

## Media Production Checklist

- [ ] {List of all media that needs to be created}
- [ ] {Grouped by type for batch production}

## Hashtag Bank

### Core Hashtags (use on every post)
{hashtags}

### Rotating Hashtags (mix and match)
{hashtags by category}
```

## Example Usage

**User:** "Create a 2-week content calendar for Instagram and TikTok. Themes: creative finance, entrepreneurship, and car deals."

**AI:** Generates 14 days of content across both platforms with specific post ideas, captions, hashtags, posting times, and media notes. Saves to `brain/content/calendar-2026-03-02-to-2026-03-15.md`.

**User:** "Plan my posts for next week"

**AI:** Reads goals and business context, generates a 7-day calendar for default platforms with relevant content. Saves to `brain/content/`.

**User:** "I need a month of LinkedIn content about AI in business"

**AI:** Generates 30 days of LinkedIn-optimized content with professional tone, thought leadership posts, and strategic hashtags.

**User:** "Give me content ideas for this week, I want to promote my course launch"

**AI:** Generates a promotional-heavy calendar with launch countdown posts, testimonials, behind-the-scenes, and CTA-driven content across platforms.

## Error Handling

- **If the user does not specify a duration:** Default to 1 week (7 days) and inform: "Building a 1-week calendar. Want LindaAI to stretch it out to 2 weeks or a full month?"
- **If the user does not specify platforms:** Default to Instagram, TikTok, and Facebook. Inform which platforms are included and offer to adjust.
- **If the user does not specify topics or themes:** Read `brain/goals.md` and `brain/projects/README.md` for context on current priorities. If those do not exist, ask: "What topics should the content focus on? Give me 2-3 themes (e.g., 'creative finance education', 'behind the scenes', 'product launch')."
- **If `brain/content/` directory does not exist:** Create it automatically before saving the calendar file.
- **If a content calendar file already exists for the same date range:** Ask: "A content calendar already exists for this period. Should I overwrite it, or create a supplementary calendar (e.g., `calendar-{date}-v2.md`)?"
- **If trend research via WebSearch returns no results:** Proceed without trend data and note: "Couldn't pull current trending data from out yonder. The content uses evergreen best practices. You may want to check trending audio/formats on each platform before posting."
- **If the user asks for a platform that is not covered in the best practices section:** Adapt the closest matching format and note: "I don't have specific optimization rules for {platform}. I adapted from {closest match} — review and adjust the format for platform-specific requirements."
- **If the user provides a very high posting frequency (e.g., 5 posts/day across 5 platforms):** Flag the volume: "That's {N} total posts for the period -- a serious content load. Want me to proceed, or rein it back to a more sustainable cadence?"

🤠 *Generated by LindaAI* 🏇


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
