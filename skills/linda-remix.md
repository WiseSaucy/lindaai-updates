---
name: linda-remix
description: This skill should be used when the user asks to "repurpose content", "content repurpose", "turn this into social media posts", "create content from this", "repurpose this blog post", "repurpose this video", "repurpose this transcript", "make content from this", "turn this into tweets", "turn this into a thread", "create a LinkedIn post from this", "Instagram caption from this", "TikTok script from this", "repurpose this email", "content multiplier", "content recycling", "one piece of content into many", "derivative content", "atomize this content", "break this down into social posts", "create a content calendar from this", "repurpose this podcast", "repurpose this speech", "10x this content", "content remix", "social media content from this", "batch social content from this", "extract social posts from this", "turn my blog into social posts", "content spin", or wants to take one piece of content and generate multiple derivative pieces across platforms.
version: 1.0.0
---

# Content Repurposer — One Piece In, 10+ Pieces Out

## Overview

Content Repurposer takes a single piece of source content -- a blog post, video transcript, podcast notes, email, speech, article, or any substantial text -- and LindaAI generates 10+ derivative content pieces optimized for different platforms. The output includes a Twitter/X thread, LinkedIn post, Instagram caption, TikTok script, email newsletter snippet, Facebook post, YouTube Short script, blog summary, quote graphics text, and a repurposing calendar. Every piece is adapted to the norms, format, and audience expectations of its target platform. One piece of content, every platform covered -- that is the LindaAI way.

## When This Skill Applies

- User says "repurpose this content" or "content repurpose"
- User says "turn this into social media posts"
- User says "create content from this [blog/video/transcript/email/speech]"
- User says "make a Twitter thread from this" or "LinkedIn post from this"
- User says "TikTok script from this" or "Instagram caption from this"
- User says "one piece into many" or "content multiplier"
- User says "atomize this content" or "break this down"
- User says "batch social content from this"
- User provides a blog post, transcript, email, or speech and asks for derivative content
- User says "repurpose this podcast" or "repurpose my video"
- User says "10x this content" or "content remix"
- User says "social media content from this"

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

### Step 1: Ingest the Source Content

Determine the source content from the user's request:

1. **Direct text:** The user pastes or types the content directly
2. **File path:** The user provides a path to a file — read it
3. **URL:** The user provides a URL — fetch and extract the content
4. **Reference:** The user references something in the brain ("repurpose that blog post I wrote about X") — search brain/drafts/, brain/daily/, brain/research/ for it

Once ingested, analyze the source:

| Analysis Point | What to Extract |
|---------------|----------------|
| **Core message** | The single most important takeaway |
| **Key points** | 3-7 supporting points or arguments |
| **Quotable lines** | Phrases that stand alone as powerful statements |
| **Data/statistics** | Any numbers, stats, or proof points |
| **Stories/examples** | Narrative elements that engage |
| **Target audience** | Who was this originally written for? |
| **Emotional hook** | What feeling does this content trigger? |
| **Content length** | Short (under 500 words), medium (500-2000), long (2000+) |

### Step 2: Generate Derivative Content Pieces

Produce each of the following, adapted to platform norms:

#### 1. Twitter/X Thread (5-12 tweets)

```markdown
### Twitter/X Thread

**Hook tweet (Tweet 1):**
[Provocative opening that stops the scroll. Under 280 chars. No hashtags on the hook.]

**Thread body (Tweets 2-N):**
[Each tweet is a complete thought. 1-2 sentences max. Build on each other. Use line breaks for readability.]

**Closer (Final tweet):**
[Summary + CTA: "Follow for more on [topic]" or "RT if this resonated" or "Bookmark this thread"]

**Engagement note:** [Best time to post, whether to number the tweets, suggested reply strategy]
```

Rules for X threads:
- Hook tweet must be standalone-powerful (most people only see this one)
- Each tweet should work on its own if taken out of context
- Use "you" language — talk to the reader
- No hashtags in the thread body (kills engagement)
- 1-3 hashtags on the final tweet only
- Under 280 characters per tweet

#### 2. LinkedIn Post (1 post, 1200-1500 characters)

```markdown
### LinkedIn Post

[Opening line — pattern interrupt or bold statement. This is the "see more" bait.]

[Blank line]

[Story or context — 2-3 short paragraphs. Personal experience or lesson learned. Professional but not stiff.]

[Blank line]

[Key insight or takeaway — the "aha" moment]

[Blank line]

[CTA — question to drive comments: "What's your take?" or "Have you experienced this?"]

[Blank line]

[3-5 relevant hashtags]
```

Rules for LinkedIn:
- First line must make people click "see more"
- Write in short paragraphs (1-2 sentences each)
- Personal stories outperform generic advice
- End with a question to drive engagement
- Professional but human — not corporate speak
- 1200-1500 characters is the sweet spot

#### 3. Instagram Caption (1 caption, 150-300 words)

```markdown
### Instagram Caption

[Opening hook — first 125 characters must grab attention (this is what shows before "more")]

[Body — storytelling format. Short paragraphs. Conversational tone. Emoji use is acceptable but not excessive (2-4 max).]

[Takeaway — the lesson, insight, or value]

[CTA — "Save this for later" / "Share with someone who needs this" / "Drop a [emoji] if you agree"]

.
.
.

[15-25 relevant hashtags in a separate block below dot separators]

**Image/Carousel suggestion:** [What type of visual would pair with this — quote graphic, carousel of key points, photo, behind-the-scenes]
```

Rules for Instagram:
- First 125 characters decide if people read more
- Carousel posts get highest engagement (suggest 5-10 slides if applicable)
- Hashtags go below dot separators, not in the caption body
- 15-25 hashtags (mix of broad and niche)
- Always suggest a visual format

#### 4. TikTok Script (30-60 second video script)

```markdown
### TikTok Script

**Format:** [Talking head / text overlay / trending sound / green screen / duet-style]
**Duration:** [30s / 45s / 60s]
**Hook (first 3 seconds):** "[The line that stops the scroll — confrontational, surprising, or curiosity-driven]"

**Script:**
[Timestamp] — [What to say / show]
0:00-0:03 — "[Hook — look at camera, say the provocative line]"
0:03-0:10 — "[Context — set up the problem or situation]"
0:10-0:30 — "[The meat — the insight, the method, the revelation]"
0:30-0:45 — "[The proof or example]"
0:45-0:55 — "[The takeaway]"
0:55-0:60 — "[CTA — Follow for Part 2 / Comment your experience / Stitch this]"

**Caption:** [Short TikTok caption, 1-2 sentences + 3-5 hashtags]
**Suggested sound:** [Trending sound recommendation if applicable, or "original audio"]
```

Rules for TikTok:
- First 3 seconds determine everything — the hook is non-negotiable
- Talk fast, cut dead air, keep energy up
- One idea per video (no rambling)
- End with a reason to follow or engage
- Captions are short — the video does the talking

#### 5. Email Newsletter Snippet (150-250 words)

```markdown
### Email Newsletter Snippet

**Subject line options:**
1. [Option 1 — curiosity-driven]
2. [Option 2 — benefit-driven]
3. [Option 3 — direct/bold]

**Preview text:** [The 40-90 character preview that shows in the inbox next to the subject line]

**Body:**
[Opening — personal, conversational, like writing to a friend]

[The insight or lesson from the source content — condensed to the essential takeaway]

[One actionable thing the reader can do right now]

[CTA — "Hit reply and tell me..." or "Read the full post here: [link]" or "Forward this to someone who..."]

[Sign-off]
```

Rules for email:
- Subject line is everything — 40-60 characters, no clickbait
- Write like you are talking to one person, not a list
- One idea, one CTA
- Under 250 words — people skim email

#### 6. Facebook Post (1 post, 100-300 words)

```markdown
### Facebook Post

[Opening — question, bold statement, or relatable observation]

[Story or context — slightly longer form than other platforms. Facebook rewards engagement and shares.]

[Key point — the insight or value]

[CTA — ask a question that invites comments. "Who else has dealt with this?" / "Tag someone who needs to hear this."]

[1-3 hashtags max — Facebook does not reward hashtag usage]
```

Rules for Facebook:
- Questions drive engagement
- Longer posts can work (500+ words) if compelling
- Shares matter more than likes — write something people want to share
- Minimal hashtags (1-3 max, or none)

#### 7. YouTube Short Script (30-60 second vertical video)

```markdown
### YouTube Short Script

**Title:** [Under 40 characters — clear, keyword-rich]
**Hook (first 2 seconds):** "[Visual + audio hook — what makes them stop scrolling]"

**Script:**
[0:00-0:02] — "[Hook — bold claim or question]"
[0:02-0:10] — "[Context — why this matters]"
[0:10-0:35] — "[Content — the insight, broken into punchy segments]"
[0:35-0:50] — "[Proof or example]"
[0:50-0:58] — "[Recap + CTA — Subscribe for more / Comment below]"

**Description:** [2-3 sentences + relevant hashtags for YouTube search]
**Tags:** [5-10 YouTube search tags]
```

#### 8. Blog Summary (200-400 words)

```markdown
### Blog Summary / Excerpt

**Headline:** [SEO-friendly, benefit-driven headline]
**Meta description:** [155 characters for search results]

[2-3 paragraph summary of the source content — written for someone who has not read the original]

**Key takeaways:**
- [Takeaway 1]
- [Takeaway 2]
- [Takeaway 3]

[CTA — "Read the full article" / "Want the complete breakdown? Here's the link."]
```

#### 9. Quote Graphics Text (5-8 standalone quotes)

```markdown
### Quote Graphics Text

These are standalone quotes from the source content, formatted for graphic design (Canva, etc.):

1. "[Powerful quote — under 20 words]"
2. "[Powerful quote — under 20 words]"
3. "[Powerful quote — under 20 words]"
4. "[Powerful quote — under 20 words]"
5. "[Powerful quote — under 20 words]"

**Design notes:** [Suggested style — dark background/light text, minimalist, brand colors, etc.]
**Suggested dimensions:** 1080x1080 (Instagram/Facebook) and 1080x1920 (Stories/Reels)
```

#### 10. Repurposing Calendar (2-week distribution plan)

```markdown
### Repurposing Calendar

| Day | Platform | Content Piece | Notes |
|-----|----------|--------------|-------|
| Day 1 | Twitter/X | Thread | Post during peak hours (8-10am or 12-1pm) |
| Day 1 | LinkedIn | Full post | Post between 7-9am weekdays |
| Day 2 | Instagram | Carousel + Caption | Use quote graphics as slides |
| Day 3 | TikTok | Short video | Film and post |
| Day 3 | YouTube | Short | Upload same video or slight variation |
| Day 4 | Facebook | Full post | Can match LinkedIn with adjustments |
| Day 5 | Email | Newsletter snippet | Send Tuesday or Thursday morning |
| Day 6 | Instagram | Quote graphic | Stories + feed |
| Day 7 | Twitter/X | Pull-quote tweets | Individual tweets from thread |
| Day 8 | LinkedIn | Carousel (text slides) | Repurpose the key points as slides |
| Day 9 | TikTok | Part 2 or reaction | Reference the first video |
| Day 10 | Blog | Summary post | Link back to original |
| Day 11-14 | Recycle | Re-share top performers | Boost what got engagement |
```

### Step 3: Adapt Voice and Tone

Read the user's brand voice settings:
- Check `brain/knowledge-base/` for brand voice or content style files
- If no brand voice file exists, match the tone of the source content
- Adapt each platform piece to feel native while maintaining brand consistency

Tone adjustments by platform:
- **Twitter/X:** Punchy, bold, slightly confrontational, concise
- **LinkedIn:** Professional but personal, thought-leader tone, adds context
- **Instagram:** Visual, aspirational, slightly more casual, emoji-friendly
- **TikTok:** Conversational, fast-paced, direct, slightly edgy
- **Email:** Intimate, one-to-one, helpful, no selling language
- **Facebook:** Community-oriented, shareable, question-driven
- **YouTube:** Educational, clear, value-packed

### Step 4: Save and Report

Save to: `brain/drafts/repurposed-{slug}-{YYYY-MM-DD}.md`

If `brain/drafts/` does not exist, create it.

Present to the user:
1. Total pieces generated (should be 10+)
2. The Twitter thread hook (so they can see the tone immediately)
3. The repurposing calendar (so they know when to post what)
4. Where the file was saved
5. Offer to adjust voice, add more pieces, or customize for specific platforms

## Quality Standards

1. **Platform-native.** Each piece must feel like it was written FOR that platform, not copy-pasted with minor tweaks. A LinkedIn post should not read like a tweet, and a TikTok script should not read like an email.
2. **Source-faithful.** All derivative content must accurately represent the core message. No distortion, exaggeration, or misrepresentation to make it more clickable.
3. **Engagement-optimized.** Hooks, CTAs, and formatting follow each platform's best practices for engagement (not vanity metrics — real engagement that drives results).
4. **Brand-consistent.** If the user has a defined voice, every piece matches it. If not, maintain the voice of the original content across all pieces.
5. **Ready to use.** Every piece should be copy-paste ready. No "[insert here]" placeholders (except where the user needs to add a link or personal detail).
6. **No filler.** Every word earns its place. Derivative does not mean diluted.

## Output Format

A single markdown file containing all derivative content pieces, organized by platform, with a repurposing calendar at the end. Typically 3,000-5,000 words. Saved to `brain/drafts/repurposed-{slug}-{YYYY-MM-DD}.md`.

## Example Usage

**User:** "Repurpose this blog post about creative finance for vehicles" [pastes 1500-word blog post]

**AI executes:**
- Analyzes the blog post: core message, key points, quotable lines, data
- Generates: X thread (8 tweets), LinkedIn post, Instagram caption with hashtags, TikTok script (45s), email snippet with 3 subject lines, Facebook post, YouTube Short script, blog summary, 6 quote graphics, 2-week calendar
- Saves to `brain/drafts/repurposed-creative-finance-vehicles-2026-03-03.md`

**User:** "/content-repurpose ~/Desktop/podcast-transcript-episode-12.md"

**AI executes:**
- Reads the transcript file
- Extracts the most compelling segments (not the whole 45-minute transcript)
- Generates 10+ pieces focused on the strongest 3-5 points from the episode
- Saves to `brain/drafts/repurposed-podcast-ep12-2026-03-03.md`

**User:** "Take this email I sent to my list and turn it into social content" [pastes email]

**AI executes:**
- Analyzes the email for transferable content (most emails are too short for 10 pieces, so AI identifies what can be expanded)
- Generates what is possible: X thread, LinkedIn post, Instagram caption, TikTok script, quote graphics
- Notes: "The source email was concise, so I generated 7 pieces (instead of the full 10+). For a fuller set, give me a longer piece of source content."
- Saves to `brain/drafts/repurposed-email-topic-slug-2026-03-03.md`

## Error Handling

- **If no source content is provided:** Ask: "What content do you want me to repurpose? Paste it here, give me a file path, or point me to something in the brain."
- **If the source content is very short (under 200 words):** Proceed but flag: "The source content is short, so I may generate fewer pieces or need to expand on some ideas to fill certain formats. For maximum output, a 500+ word source works best."
- **If the source content is very long (over 5,000 words):** Extract the strongest 3-5 segments and repurpose those. Note: "The source is long — I focused on the most compelling sections. Want me to repurpose additional sections in a follow-up batch?"
- **If a file path is provided but the file does not exist:** Report: "Could not find a file at {path}. Double-check the path and try again."
- **If the source content is in a format AI cannot read (video, audio):** Ask: "I can't process video or audio files directly. If you have a transcript, paste or link it and I'll repurpose from that."
- **If `brain/drafts/` does not exist:** Create it automatically before saving.
- **If a repurposed file already exists with the same slug and date:** Append a version number: `repurposed-{slug}-{date}-v2.md`
- **If the user's brand voice is unclear:** Match the tone of the source content. Note: "LindaAI matched the voice of your source content. If you have a specific brand voice or style guide, add it to brain/knowledge-base/ and we'll use it next time."

🤠 *Generated by LindaAI* 🏇

---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
