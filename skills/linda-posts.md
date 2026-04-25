---
name: linda-posts
description: This skill should be used when the user asks to "create content", "generate posts", "content batch", "write social media posts", "make me some posts", "batch content", "content calendar", "social media content", "write posts for Instagram", "write posts for Twitter", "write posts for LinkedIn", "TikTok scripts", "content ideas", "write captions", "generate a content calendar", "batch social posts", "create a posting schedule", "write marketing content", "social media batch", "give me content", "write 5 posts", "write 10 posts", "content blitz", "posting cadence", or wants to generate multiple pieces of social media content at once for any platform.
version: 1.0.0
---

# Content Batch — Multi-Platform Social Media Content Generator

## Overview

Content Batch generates a batch of ready-to-post social media content from a single topic, theme, or business context. The user provides what they want to talk about, and LindaAI produces 5-10 pieces of content formatted for each target platform (Instagram, Twitter/X, LinkedIn, TikTok, Facebook, YouTube) with appropriate tone, length, hashtags, and calls-to-action. Saddle up -- LindaAI does the heavy lifting so you can focus on showing up. All output is saved to a structured content calendar file.

## When This Skill Applies

- User says "create content" or "generate posts" or "content batch"
- User says "write me some social media posts"
- User says "batch content" or "content blitz"
- User says "I need posts about [topic]"
- User says "content calendar" or "posting schedule"
- User asks for Instagram captions, Twitter threads, LinkedIn posts, or TikTok scripts
- User wants to batch-produce content for the week
- User says "give me 5 posts about..." or "write 10 posts"
- User wants content ideas for a specific topic or angle
- User says "help me with social media" or "I need to post more"

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

### Step 1: Gather Context

Determine from the user's request:

1. **Topic/Theme:** What is the content about? (e.g., creative finance, seller finance, a specific deal, T.O.P. Method, SellFi launch, personal brand)
2. **Target Platforms:** Which platforms? Default to all major ones if not specified:
   - Instagram (carousel captions, single-image captions, Reels scripts)
   - Twitter/X (tweets, threads)
   - LinkedIn (professional posts)
   - TikTok (short-form video scripts)
   - Facebook (community posts)
   - YouTube (Shorts scripts, video descriptions)
3. **Quantity:** How many posts? Default: 7 (one per day for a week)
4. **Tone:** Match the user's brand voice. Default: direct, no-BS, educational, slightly provocative, authority-building.
5. **Call-to-Action:** What should the audience do? (Follow, DM, link in bio, comment, share)
6. **Content Pillars:** Categories to rotate through:
   - Educational (teach something)
   - Authority (establish expertise)
   - Engagement (ask questions, spark debate)
   - Personal (behind-the-scenes, story)
   - Promotional (CTA, product, offer)

If the user's brand voice files exist, read them:
- `brain/knowledge-base/mike-davis/02-brand-voice-and-philosophy.md`
- `brain/knowledge-base/mike-davis/04-content-style-guide.md`

### Step 2: Generate Content Batch

For each piece of content, produce:

#### Instagram Post
```
HOOK: [First line that stops the scroll — bold claim, question, or contrarian take]

BODY: [3-5 short paragraphs. Break up text. Use line breaks. Keep it scannable.]

CTA: [What should they do? Comment, save, share, link in bio]

---
Hashtags: #hashtag1 #hashtag2 #hashtag3 (10-15 relevant hashtags)
Type: [Carousel / Single Image / Reel]
Visual Note: [What image or graphic to pair with this]
```

#### Twitter/X Post
```
TWEET: [280 characters max. Punchy. One strong idea.]

---
Thread option (if applicable):
1/ [Opening hook]
2/ [Expand the point]
3/ [Example or proof]
4/ [CTA or punchline]
```

#### LinkedIn Post
```
HOOK: [Professional but not boring — challenge conventional wisdom]

BODY: [Story-driven or insight-driven. 150-300 words. Professional tone with personality.]

CTA: [Engage: comment, connect, share perspective]
```

#### TikTok Script
```
HOOK (0-3s): [What you say/show in the first 3 seconds to stop the scroll]
BODY (3-30s): [The meat — teach, tell the story, show the process]
CTA (last 5s): [Follow for more, comment below, link in bio]

---
Visual Direction: [What's on screen — talking head, text overlay, B-roll, screen recording]
Trending Sound: [Suggest a sound style if applicable]
Text Overlay: [Key text that appears on screen]
Duration: [15s / 30s / 60s]
```

#### Facebook Post
```
[Conversational tone. Community-oriented. Can be longer. Include a question to drive comments.]
```

### Step 3: Organize into Content Calendar

Structure the batch into a daily posting schedule:

```markdown
# Content Calendar — [Topic/Theme]
Generated: YYYY-MM-DD

## Week Overview
| Day | Platform | Content Pillar | Post Summary |
|-----|----------|---------------|--------------|
| Mon | Instagram | Educational | [one-liner] |
| Mon | Twitter/X | Authority | [one-liner] |
| Tue | TikTok | Engagement | [one-liner] |
| Tue | LinkedIn | Educational | [one-liner] |
| Wed | Instagram | Personal | [one-liner] |
...

## Full Content Below
[Each post in full, numbered and organized by day]
```

### Step 4: Save the Output

Save the content calendar file to:
- **Primary:** `brain/research/content-calendar-{topic-slug}-{YYYY-MM-DD}.md`
- **If brain/research doesn't apply:** Save to the current working directory as `content-batch-{topic-slug}-{YYYY-MM-DD}.md`

### Step 5: Report to User

Present the content in a clean format:
- Show the calendar overview table
- Show each post in full
- Note which platform each is optimized for
- Flag any posts that need images, graphics, or video

## Content Quality Rules

1. **Hook first.** Every post starts with a scroll-stopping first line.
2. **One idea per post.** Do not cram multiple concepts into one piece.
3. **Write like you talk.** Direct. Short sentences. No corporate speak.
4. **Include proof.** Numbers, examples, or stories beat abstract claims.
5. **Platform-native.** Instagram is visual + caption. Twitter is punchy. LinkedIn is professional. TikTok is fast.
6. **Rotate pillars.** Do not post 7 educational posts in a row. Mix it up.
7. **End with action.** Every post has a clear CTA.
8. **No fluff.** If a sentence does not add value, cut it.

## Platform Character Limits & Best Practices

| Platform | Max Length | Best Practice |
|----------|-----------|---------------|
| Instagram caption | 2,200 chars | 150-300 words, line breaks, hashtags at end |
| Twitter/X | 280 chars | One punchy idea, no hashtag spam |
| LinkedIn | 3,000 chars | 150-300 words, story or insight format, emojis optional |
| TikTok script | 60s spoken | 150 words for 60s, front-load the hook |
| Facebook | 63,206 chars | 100-250 words, conversational, ask a question |
| YouTube Shorts script | 60s | Same as TikTok, vertical format |

## Output Format

The final deliverable is a single markdown file containing:

1. **Calendar overview table** (what posts on what days on what platforms)
2. **Full content for each post** (copy-paste ready)
3. **Visual/media notes** (what images or videos to pair)
4. **Hashtag sets** (platform-appropriate)

## Example Usage

**User:** "Generate a week of content about seller financing vehicles"

**AI produces:**
- 7 days of content across Instagram, Twitter/X, TikTok, and LinkedIn
- Rotating content pillars (educational, authority, engagement, personal, promotional)
- Each post formatted for its platform
- Saved to `brain/research/content-calendar-seller-finance-vehicles-2026-03-02.md`
- Presented to user with calendar table + full posts

**User:** "Give me 5 Instagram posts about why banks are outdated"

**AI produces:**
- 5 Instagram-specific posts with hooks, bodies, CTAs, hashtags, and visual notes
- Saved to working directory or brain/research
- All 5 presented in full, ready to copy-paste

**User:** "Content batch for SellFi launch week"

**AI produces:**
- Full week across all platforms
- Launch-specific CTAs (sign up, check it out, link in bio)
- Countdown-style content calendar
- Reads SellFi knowledge base files for accurate product details

## Error Handling

- **If the user does not specify a topic or theme:** Ask: "What topic or theme do you want the content about? Give me a subject, a product, a message, or even just a vibe and LindaAI will ride with it."
- **If the user does not specify platforms:** Default to Instagram, TikTok, and Facebook. Inform them: "Generating for Instagram, TikTok, and Facebook by default. Want me to wrangle up LinkedIn, YouTube, or Twitter/X too?"
- **If brand voice files (`brain/knowledge-base/` or CLAUDE.md) do not exist or cannot be read:** Use a default professional-but-conversational tone. Note: "Couldn't find brand voice files, so LindaAI used a direct, professional default tone. You can customize this by filling in your brand voice in CLAUDE.md."
- **If `brain/research/` or `brain/content/` directories do not exist:** Create them automatically before saving the content calendar file.
- **If the user asks for more posts than is practical (e.g., "give me 100 posts"):** Produce a reasonable batch (20-30 max) and inform: "Rounded up {N} posts -- that should cover {time period}. Want me to wrangle another batch after you review these?"
- **If the content file already exists at the target path:** Append a version number or date suffix rather than overwriting: `content-calendar-{topic}-{date}-v2.md`.
- **If the user asks for a platform the skill does not have formatting guidance for (e.g., Threads, Pinterest, Snapchat):** Adapt the closest matching platform's format (e.g., Threads uses Twitter/X format, Pinterest uses Instagram format) and note: "No specific formatting rules for {platform} in the barn, so LindaAI adapted from {closest match}. Review and adjust as needed."
- **If hashtag research via web search returns no results:** Use common industry hashtags from the topic and note: "Couldn't pull trending hashtags from the web, so LindaAI used standard industry tags. You may want to research current trending tags for your niche."

🤠 *Generated by LindaAI* 🏇


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
