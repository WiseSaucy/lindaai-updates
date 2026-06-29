---
name: linda-social-post
description: This skill should be used when the user asks to "post to social", "post my content", "schedule social post", "publish to TikTok / Instagram / Facebook / YouTube / Twitter", "post the reel", "schedule the reel", "push to socials", "blast to all platforms", "cross-post", "post everywhere", "auto-post", "queue up a post", "send this to my socials", or wants a finished video/image/caption pushed to one or more social platforms now or at an optimal time. Integrates with sauce-cuts output and Ayrshare API.
version: 1.0.0
---
> ⚙️🤠 **Publishing engine (Ayrshare) — the content skills call me to push finished posts to your platforms.** Works behind `content-batch`, `content-repurpose`, `social-media-calendar`, and `deal-marketing-package`. Callable directly too.

# Linda Social Post — Multi-Platform Publisher (via Ayrshare)

## Overview

📣 **Holler** (Social Media) handles every post-to-social request. One command sends finished content to TikTok, Instagram Reels, Facebook Reels, YouTube Shorts, and Twitter/X — either NOW or auto-scheduled at the optimal time per platform.

Powered by Ayrshare (single API for all five). No more switching apps. No more forgetting to post.

## When This Skill Applies

- "Post the wife reel to TikTok and IG"
- "Holler, post this everywhere"
- "Schedule today's post for prime time"
- "Push the LindaAI promo to all platforms"
- "Cross-post the deal-analysis short"
- "Queue up 3 posts for this week"
- "Post this to TikTok, IG, FB tonight at 8pm"

## Required Setup (one-time)

User must have a config file at `~/.lindaai/ayrshare.json`:

```json
{
  "api_key": "<their_ayrshare_api_key>",
  "default_profile_key": "<optional_if_multiple_brand_profiles>"
}
```

If the file is missing → STOP and tell user:
> 📣 Holler — I need your Ayrshare API key first. Sign up at https://www.ayrshare.com, copy your key, then save it to `~/.lindaai/ayrshare.json` in this format: `{"api_key": "YOUR_KEY"}`. Once that's there, I can post anywhere for you.

## Inputs

| Input | Required | Default |
|-------|----------|---------|
| Media file path (video MP4 or image) | One of media OR text | — |
| Caption / post text | Yes | — |
| Platforms (comma list) | Yes | — |
| Schedule time (ISO 8601) | No | Auto-optimal per platform |
| Hashtags | No | Pulled from caption |

## Auto-Time Schedule (Boss47 MDT — UTC-6)

When no explicit time is given, schedule per platform's sweet spot **in local MDT**:

| Platform | Optimal window | Default pick |
|---|---|---|
| TikTok | 6:00-10:00 PM MDT | **8:23 PM** |
| Instagram Reels | 7:00-10:00 PM MDT | **8:47 PM** |
| Facebook Reels | 6:00-9:00 PM MDT | **7:33 PM** |
| YouTube Shorts | 5:00-8:00 PM MDT | **6:17 PM** |
| Twitter/X | 12:00-3:00 PM MDT | **1:43 PM** |

Off-minute picks (`:17`, `:23`, `:33`, `:43`, `:47`) intentionally avoid the `:00/:30` traffic spike.

If user says "post now" → bypass scheduler, post immediately.

## How It Works

### Step 1 — Verify setup
- Check `~/.lindaai/ayrshare.json` exists
- Read api_key
- If missing → halt with friendly message (see Required Setup)

### Step 2 — Upload media (if video/image given)
- Run `scripts/upload_media.py <file>` → returns Ayrshare media URL
- Caches uploads in `~/.lindaai/ayrshare-cache/` to avoid re-uploading same file

### Step 3 — Build caption + hashtag block per platform
- TikTok: caption + 3-5 hashtags
- Instagram: caption + 15-25 hashtags
- Facebook: caption + 2-5 brand tags
- YouTube Shorts: title (≤60 chars) + 3-15 hashtags in description
- Twitter/X: ≤280 chars, 1-3 hashtags

If the user provided a PUBLISH_PACK.md (e.g. from sauce-cuts), pull the per-platform caption directly from it.

### Step 4 — Schedule or post
- For each requested platform, build the Ayrshare post payload:
```json
{
  "post": "<platform-tuned caption>",
  "platforms": ["<platform>"],
  "mediaUrls": ["<uploaded_url>"],
  "scheduleDate": "<ISO timestamp with -06:00 offset, or omitted for immediate>",
  "hashTags": ["..."]
}
```
- POST to `https://app.ayrshare.com/api/post`
- Capture the returned `id` per post for status tracking

### Step 5 — Report back
- Single message like:
```
📣 Holler — queued 5 posts:
  ✅ TikTok @ 8:23 PM MDT (post id: abc123)
  ✅ Instagram Reels @ 8:47 PM MDT (post id: def456)
  ✅ Facebook Reels @ 7:33 PM MDT (post id: ghi789)
  ✅ YouTube Shorts @ 6:17 PM MDT (post id: jkl012)
  ✅ Twitter @ 1:43 PM MDT (post id: mno345)
View / edit in Ayrshare dashboard → https://app.ayrshare.com
```

### Step 6 — Save to history
Append the post details to `~/.lindaai/social-history.jsonl` so we can track what was posted when, and pull engagement metrics later (see `/linda-social-stats` future skill).

## Integration with sauce-cuts

When the user has a finished cut in `~/Desktop/Sauce and Family Content/<category>/<project>/`:
1. Read `PUBLISH_PACK.md` from that project folder
2. Pick the platform variant file (TIKTOK.mp4 / FB-IG.mp4 / YOUTUBE.mp4)
3. Use per-platform caption from PUBLISH_PACK.md
4. Schedule or post

Example user flow:
> "Holler, post the wife reel to all platforms at optimal times"

LindaAI:
1. Find latest project folder under `~/Desktop/Sauce and Family Content/`
2. Read its PUBLISH_PACK.md
3. Upload TIKTOK.mp4 + FB-IG.mp4 + YOUTUBE.mp4 to Ayrshare
4. Schedule all 5 platforms per auto-time table
5. Report

## What to NEVER do

- **NEVER** post without showing the caption + scheduled time first → user confirms "go"
- **NEVER** post to a platform the user didn't list
- **NEVER** post a video that's still encoding (check file size stable for 5s)
- **NEVER** assume which Meta Page is active — always show "Will post as: [Page Name]" before scheduling FB/IG, and confirm the connected page with the user before posting
- **NEVER** post without an active Ayrshare account verification (the API will reject anyway, but check first)

## Errors & Fallbacks

| Error | Response |
|---|---|
| 401 Unauthorized | API key invalid → tell user to regenerate at https://app.ayrshare.com/api-keys |
| 402 Payment required | Free trial expired → upgrade Ayrshare plan |
| 429 Rate limited | Wait 60s, retry once |
| Media upload fails | Check file size (<400MB), format (mp4/mov/jpg/png), try once more |
| Platform not connected | Open Ayrshare dashboard → Social Accounts → connect that platform first |

## Future Companion Skills (roadmap)

- `/linda-social-stats` — pull engagement metrics across all 5 platforms
- `/linda-social-bulk` — schedule a full week's content in one shot
- `/linda-social-respond` — Holler watches comments and drafts replies for approval

---

© 2022-2026 Daniel Wise · LindaAI
