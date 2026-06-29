---
name: linda-postiz-post
description: This skill should be used when the user asks to "post via Postiz", "schedule with Postiz", "post my pack via Postiz", "postiz schedule", "schedule the reel through Postiz", "blast via Postiz", "auto-schedule postiz", "queue this in Postiz", "send to Postiz", "publish via Postiz", "Postiz cross-post", "post the [name] pack to Postiz", "schedule [pack name] across all platforms", or wants finished content auto-scheduled to TikTok, Instagram, Facebook, YouTube Shorts, and Twitter/X via the connected Postiz Cloud account at per-platform optimal MDT times — no manual clicking, no Ayrshare, no walkthrough.
version: 1.0.0
---
> ⚙️🤠 **Publishing engine (Postiz) — the content skills call me to auto-schedule finished posts** at per-platform optimal times. Works behind `content-batch`, `content-repurpose`, `social-media-calendar`, and `deal-marketing-package`. Callable directly too.

# Linda Postiz Post — Automated Multi-Platform Publisher (via Postiz Cloud API)

## Overview

📣 **Holler** (Social Media) drives this one. The user has Postiz Cloud connected via API key (stored in `~/.lindaai/postiz.json`). This skill reads a finished content pack — captions in `PUBLISH_PACK.md`, MP4s on disk — uploads the media to Postiz, then schedules a separate post to each of the 5 connected channels at that platform's optimal MDT slot. One command. Zero manual clicks.

**No Ayrshare. No walkthrough. No clipboard juggling.** This is the fully-automated path for users who took the time to wire Postiz into LindaAI.

## When This Skill Applies

- "Postiz, post the wife reel"
- "Holler, schedule the Hustling pack via Postiz"
- "Auto-post the latest sauce-cuts project through Postiz"
- "Blast today's pack via Postiz"
- "Schedule the Tono skit to all platforms in Postiz"
- "Postiz-schedule the LeBron-Wade reel for tonight"
- Any request where the user wants Postiz to do the work AND has a finished pack ready

> Use `/linda-post-walkthrough` instead when the user wants manual click-through coaching with no API.
> Use `/linda-social-post` instead when the user has Ayrshare set up (not Postiz).

## License + Postiz Setup Check (Required First Step)

Before doing anything:

1. **License check** — Read `~/.claude/linda-license.json`. If missing / expired / inactive → halt with friendly message (same as other LindaAI skills).
2. **Postiz creds check** — Read `~/.lindaai/postiz.json`. Required keys: `api_url`, `api_key`. If file missing → halt:
   > 📣 Holler — I can't find your Postiz creds at `~/.lindaai/postiz.json`. Run the Postiz hookup first — drop me your Postiz Cloud API key and I'll wire it in. Until then, try `/linda-post-walkthrough` for the manual path.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Project folder OR pack name | Yes | Either an absolute path OR a fuzzy pack name ("Hustling", "wife reel", "Tono") |
| Platforms (comma list) | No | Default: all 5 — tiktok,instagram,facebook,youtube,x — plus `youtube-long` auto-included if pack supports it |
| Schedule mode | No | `auto` (default — per-platform optimal MDT times) · `now` · explicit ISO 8601 |
| `--no-youtube-long` | No | Opt out of auto-adding the YT long-form when pack has `archive/*.mp4` + long-form caption |
| `--reset` | No | Delete previously-queued posts for this pack (from history) before rescheduling — useful when retrying with edits |

If the user provides a pack name (e.g. "Hustling"), search common content directories:
- `~/Desktop/Sauce and Family Content/` (Boss47's personal — case-sensitive!)
- `~/Desktop/Sauce and Family content/` (lowercase variant)
- `~/Desktop/LindaAI-OG/content-packs/`
- Current working directory

Match the most recent folder whose name contains the keyword (case-insensitive). If multiple matches, ask the user to pick.

## Auto-Time Schedule (Boss47 MDT — UTC-6)

Same windows as `/linda-post-walkthrough` and `/linda-social-post` — kept identical so behavior is predictable regardless of skill used:

| Platform | Default pick (MDT) | UTC equivalent |
|---|---|---|
| TikTok | **8:23 PM** | 02:23 next-day |
| Instagram Reels | **8:47 PM** | 02:47 next-day |
| Facebook Reels | **7:33 PM** | 01:33 next-day |
| YouTube Shorts | **6:17 PM** | 00:17 next-day |
| Twitter/X | **1:43 PM** | 19:43 same-day |
| YouTube Long-Form | **next Saturday 10:00 AM** | next Saturday 16:00 UTC |

## YouTube Long-Form Auto-Detection

If a pack includes BOTH:
1. An `archive/*.mp4` file (the long-form cut — typically 1:00 — 3:00 min) AND
2. A `### YouTube Long-Form` heading in PUBLISH_PACK.md

…then the skill auto-queues a SECOND YouTube post (long-form, separate from the Shorts) for next Saturday morning. Uses the long-form title from the heading section. Opt out via `--no-youtube-long`.

Off-minute picks (`:17`, `:23`, `:33`, `:43`, `:47`) avoid the `:00/:30` traffic spike.

If today's optimal slot for a platform has already passed in MDT, schedule for **tomorrow** at that slot.

## Caption Parser

Same parser as `/linda-post-walkthrough` so packs work either way. Looks for these headings in `PUBLISH_PACK.md` (variants allowed — heading just needs to contain the keyword):

| Heading keyword | Platform |
|---|---|
| `### TikTok` | tiktok |
| `### Instagram Reels` or `### Instagram` | instagram |
| `### Facebook Reels` or `### Facebook` | facebook |
| `### YouTube Shorts` | youtube |
| `### YouTube Long-Form` or `### Long-Form` | youtube-long (special) |
| `### Twitter/X` or `### Twitter` or `### X` | x |

Caption body = lines between that `###` and the next `###` (or EOF).
Strip leading/trailing code fences (` ``` `) — common in the packs.
Strip "**Pin comment:**" footers (those are not the post body).

**Twitter/X length guard:** trim to 280 chars before scheduling. Log a warning if the original was longer.

## Media File Resolution

Look in the project folder for platform-specific MP4s (with fallback hierarchy):

| Platform | Primary | Fallback chain |
|---|---|---|
| TikTok | `TIKTOK.mp4` | `master.mp4` |
| Instagram | `IG.mp4` → `INSTAGRAM.mp4` → `FB-IG.mp4` | `TIKTOK.mp4` → `master.mp4` |
| Facebook | `FB.mp4` → `FACEBOOK.mp4` → `FB-IG.mp4` | `TIKTOK.mp4` → `master.mp4` |
| YouTube | `YOUTUBE.mp4` | `TIKTOK.mp4` → `master.mp4` |
| Twitter/X | `TWITTER.mp4` → `X.mp4` | `TIKTOK.mp4` → `master.mp4` |

If a platform's MP4 is missing AND no fallback exists, **skip that platform** with a warning in the report.

## How It Works (Step-by-Step)

### Step 1 — Verify setup
- License check
- Read `~/.lindaai/postiz.json`
- Extract `api_url`, `api_key`

### Step 2 — Resolve pack
- Find folder by name or use absolute path
- Confirm `PUBLISH_PACK.md` exists → halt with helpful message if not
- List MP4 files in the folder

### Step 3 — Parse captions
- Read PUBLISH_PACK.md
- Extract per-platform captions using the parser above
- Trim Twitter to 280 chars

### Step 4 — Fetch Postiz integrations
- `GET {api_url}/integrations` with `Authorization: {api_key}` header
- Build a map from platform identifier (`tiktok`, `instagram-standalone`, `facebook`, `youtube`, `x`) to integration `id`
- If a platform is in the user's request but not in their Postiz integrations → skip with a warning

### Step 5 — Show plan, ask for "go"

```
📣 Holler — Postiz schedule plan for "{pack name}":

  1. TikTok        → {customer_handle}        → 8:23 PM MDT (tonight)  → TIKTOK.mp4
  2. Instagram     → {customer_handle}        → 8:47 PM MDT (tonight)  → FB-IG.mp4
  3. Facebook      → Daniel Wise       → 7:33 PM MDT (tonight)  → FB-IG.mp4
  4. YouTube Shorts→ Daniel Wise       → 6:17 PM MDT (tomorrow) → YOUTUBE.mp4
  5. Twitter/X     → {customer_handle}        → 1:43 PM MDT (tomorrow) → TIKTOK.mp4

5 posts will be queued in Postiz. Say "go" to schedule, "preview" to see captions first, or "skip x" to drop a platform.
```

Wait for explicit `go`. Do not auto-publish.

### Step 6 — Upload media (one upload per unique file)

For each unique MP4 referenced in the plan:
- `POST {api_url}/upload` with multipart form-data (field: `file`)
- Capture the response `{id, path, ...}` for that file
- Cache in-memory so the same MP4 isn't uploaded twice (e.g. FB-IG.mp4 used for both IG and FB)

### Step 7 — Schedule each post

For each platform in the plan, send a **separate** `POST {api_url}/posts` (because each has its own scheduled time):

```json
{
  "type": "schedule",
  "date": "2026-05-28T02:23:00.000Z",
  "shortLink": false,
  "tags": [],
  "posts": [
    {
      "integration": { "id": "<integration_id_for_this_platform>" },
      "value": [
        {
          "content": "<platform-specific caption>",
          "image": [{ "id": "<upload_id>", "path": "<upload_path>" }]
        }
      ],
      "settings": { "__type": "<platform_identifier>" }
    }
  ]
}
```

Notes:
- `__type` matches the platform identifier from `/integrations` exactly: `tiktok`, `instagram-standalone`, `facebook`, `youtube`, `x`.
- `date` MUST be UTC ISO 8601 with `Z` suffix. Convert from MDT (UTC-6) by adding 6 hours.
- For `now` mode, set `type: "now"` and use current UTC time for `date`.
- Capture each response's post `id` for the success report.

### Step 8 — Verify queue

After all POSTs land, hit `GET {api_url}/posts?startDate=...&endDate=...` covering the schedule window to confirm everything actually queued. Cross-check returned post IDs against what we just created.

### Step 9 — Log + report

Append a record to `~/.lindaai/postiz-history.jsonl`:

```json
{"project":"03-Hustling-For-Family","scheduled_at":"2026-05-27T21:30:00-06:00","platforms":["tiktok","instagram","facebook","youtube","x"],"post_ids":{"tiktok":"...","instagram":"...","facebook":"...","youtube":"...","x":"..."},"mode":"auto"}
```

Final wrap-up message:

```
📣 Holler — Yeeee Hawww! 🤠 Pack scheduled via Postiz!

  ✅ TikTok        @ 8:23 PM MDT  (post id: cmpqz...)
  ✅ Instagram     @ 8:47 PM MDT  (post id: cmpqz...)
  ✅ Facebook      @ 7:33 PM MDT  (post id: cmpqz...)
  ✅ YouTube Shorts@ 6:17 PM MDT  (post id: cmpqz...)
  ✅ Twitter/X     @ 1:43 PM MDT  (post id: cmpqz...)

Logged to ~/.lindaai/postiz-history.jsonl
View the queue at platform.postiz.com/launches

Want me to draft engagement replies for after the first hour, or queue another pack?
```

If anything failed, mark it with ❌ and the error message, and tell the user how to retry just that platform.

## Implementation

The main entrypoint is `scripts/postiz_post.py`:

```
python3 scripts/postiz_post.py \
  --project "/path/to/pack" \
  --platforms tiktok,instagram,facebook,youtube,x \
  --schedule-mode auto
```

Or by pack name:
```
python3 scripts/postiz_post.py \
  --pack-name "Hustling" \
  --platforms all \
  --schedule-mode auto
```

The script handles everything in Steps 1-9. Holler narrates the plan/result; the script does the API work.

## What to NEVER Do

- **NEVER** auto-publish without explicit "go" from the user (Step 5 gate).
- **NEVER** post to a Facebook page you do NOT own — always confirm the FB integration is "Daniel Wise" (or the user's primary page name).
- **NEVER** truncate a caption silently — if Twitter is over 280, trim and warn in the plan output.
- **NEVER** upload a file if it's already been uploaded in this run (use the in-memory cache to avoid wasted bytes).
- **NEVER** schedule a post for a time that's already passed — bump to the same slot tomorrow.

## Errors & Fallbacks

| Issue | Holler's response |
|---|---|
| `~/.lindaai/postiz.json` missing | "No Postiz creds. Run the Postiz hookup first or use `/linda-post-walkthrough`." |
| `PUBLISH_PACK.md` missing | "Can't find the pack file in `{folder}`. Run `/sauce-cuts` first." |
| Integration for a requested platform not in `/integrations` | Skip that platform, list it in the warning section of the plan. |
| MP4 missing AND no fallback | Skip platform, warn in plan. |
| Upload returns non-200 | Retry once with 2s backoff, then halt with the error. |
| `POST /posts` returns 4xx | Show the response body verbatim — Postiz error messages are usually specific (e.g. "video must be 9:16"). |
| Twitter caption > 280 | Trim, warn in plan output. |
| Today's slot already passed | Bump to same slot tomorrow, note it in the plan ("→ tomorrow"). |

## Example Usage

**User:** "Holler, schedule the Hustling pack via Postiz"

**Holler:**
1. License + Postiz cred check ✅
2. Finds `~/Desktop/Sauce and Family Content/1-Sauce-Skits/03-Hustling-For-Family/`
3. Parses PUBLISH_PACK.md → 4 captions found (no Twitter — will fall back to TikTok caption trimmed to 280)
4. Fetches Postiz integrations → maps 5 channels
5. Shows plan, asks "go"
6. User: "go"
7. Uploads TIKTOK.mp4, FB-IG.mp4, YOUTUBE.mp4 (3 unique files)
8. Schedules 5 posts at MDT optimal slots
9. Reports IDs + logs to history

**User:** "Postiz, blast the Tono skit but skip YouTube"

**Holler:** runs with `--platforms tiktok,instagram,facebook,x`, leaves YT alone.

**User:** "Postiz-schedule the latest pack for 9pm tonight on all platforms"

**Holler:** uses `--schedule-mode 2026-05-27T21:00:00-06:00` — same time on every platform.

---

📣 *Holler — Social Media* · LindaAI · Built by Daniel Wise

© 2022-2026 Daniel Wise · LindaAI · support@send.lindaai-brain.com · lindaai-brain.com
