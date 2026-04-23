---
name: personal-brand-audit
description: This skill should be used when the user asks to "audit my brand", "brand audit", "personal brand audit", "review my online presence", "how does my brand look", "brand analysis", "brand check", "social media audit", "audit my social media", "review my positioning", "brand gap analysis", "brand consistency check", "what does my brand say about me", "brand snapshot", "brand health check", "improve my brand", "personal branding", "brand strategy", "brand positioning", "how am I perceived online", "audit my profiles", "review my content strategy", "brand improvement plan", "30-day brand plan", "content pillars", "bio suggestions", "tagline suggestions", "brand messaging", "brand identity audit", "digital presence review", "brand perception", "online reputation check", "brand refresh", or wants a comprehensive analysis of their personal or business brand across digital channels.
version: 1.0.0
---

# Personal Brand Audit — Comprehensive Brand Intelligence

## Overview

Personal Brand Audit performs a full analysis of the user's personal or business brand across digital channels. LindaAI examines social media presence, content strategy, positioning, messaging consistency, and competitive landscape. The output includes a current brand snapshot, gap analysis, competitor positioning comparison, a 30-day improvement plan, content pillar recommendations, and bio/tagline suggestions. No more guessing -- LindaAI tells you exactly where your brand stands and what to fix.

## When This Skill Applies

- User says "audit my brand" or "brand audit"
- User says "personal brand audit" or "review my online presence"
- User says "how does my brand look?" or "brand health check"
- User says "social media audit" or "audit my profiles"
- User says "brand gap analysis" or "brand consistency check"
- User says "improve my brand" or "brand improvement plan"
- User says "brand positioning" or "how am I perceived online?"
- User says "30-day brand plan" or "brand strategy"
- User says "content pillars" or "content strategy review"
- User says "bio suggestions" or "tagline suggestions"
- User says "brand snapshot" or "digital presence review"
- User mentions wanting to strengthen, refresh, or understand their brand

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

### Step 1: Gather Brand Context

Determine from the user's request:

1. **Who:** The person or business being audited
2. **Handles/URLs:** Social media handles, website URL, any online profiles
3. **Industry/Niche:** What space are they in?
4. **Target Audience:** Who are they trying to reach?
5. **Current Goals:** What is the brand supposed to accomplish? (lead generation, thought leadership, deal flow, community building, product sales)
6. **Self-perception:** How does the user think their brand is perceived vs. how they WANT it to be perceived?

**Internal context:** Check the brain for existing brand information:
- `brain/knowledge-base/` for brand voice, identity, and content style files
- `brain/goals.md` for business objectives
- `brain/projects/` for brand-related projects
- `brain/research/` for prior brand or competitor research

### Step 2: Audit the Digital Presence

> 🤠 "Hold tight -- heading over yonder to gather up the details."

Research each channel where the user has a presence:

#### Website Audit
- Search for the user's website and fetch key pages
- Evaluate: messaging clarity, value proposition, design impression, CTA strength, mobile-friendliness (inferred from search results and page structure)
- Note: Is the website doing its job? Does it convert visitors into action-takers?

#### Social Media Audit

For each platform (Instagram, Twitter/X, LinkedIn, Facebook, TikTok, YouTube), research:

| Audit Point | What to Evaluate |
|------------|------------------|
| **Profile Setup** | Photo, bio, handle consistency, link in bio, highlights/pinned content |
| **Content Quality** | Visual consistency, writing quality, value delivery, professionalism |
| **Posting Frequency** | How often do they post? Is it consistent? |
| **Engagement** | Comments, likes, shares relative to follower count (engagement rate) |
| **Content Mix** | Educational vs. promotional vs. personal vs. entertainment ratio |
| **Audience Fit** | Does the content attract the RIGHT audience for their goals? |
| **Calls to Action** | Are they driving followers somewhere? (Website, product, DMs, email list) |
| **Messaging Consistency** | Does the brand message match across platforms? |
| **Visual Identity** | Color consistency, font usage, photo style, brand cohesion |
| **Bio/Tagline** | Clear, compelling, tells people what you do and why they should care |

For each platform, produce a score and summary:

```markdown
### [Platform Name]

**Handle:** @[handle]
**Followers:** [count if discoverable]
**Posting Frequency:** [X posts per week/month]
**Content Focus:** [What they mostly post about]

**Strengths:**
- [What is working]
- [What is working]

**Weaknesses:**
- [What needs improvement]
- [What needs improvement]

**Score:** [X/10]
**Priority Fix:** [The single most impactful change for this platform]
```

#### Search Presence Audit
- Search the user's name and brand name on Google
- What comes up first? (LinkedIn, website, social, press, nothing?)
- Is there any negative or outdated content?
- Are they showing up for relevant keywords?
- Note the "digital first impression" — what does someone see when they Google this person?

### Step 3: Build the Brand Snapshot

```markdown
## Current Brand Snapshot

### Who You Are (Based on What the Internet Says)
[2-3 paragraph honest assessment of how the user's brand currently reads to a stranger. This is not what they WANT to be perceived as — this is what actually comes through.]

### Brand Identity Summary
| Element | Current State | Assessment |
|---------|-------------|------------|
| **Core Message** | [What their brand is currently saying] | [Clear / Unclear / Missing] |
| **Value Proposition** | [What value they promise] | [Strong / Weak / Nonexistent] |
| **Target Audience** | [Who their content speaks to] | [Well-defined / Vague / Confused] |
| **Visual Identity** | [Logo, colors, style consistency] | [Cohesive / Inconsistent / Missing] |
| **Tone of Voice** | [How they communicate] | [Consistent / Varies / Undefined] |
| **Credibility Signals** | [Proof, testimonials, results, press] | [Strong / Moderate / Weak] |
| **Differentiation** | [What makes them different] | [Clear / Unclear / Generic] |

### Platform Presence Overview
| Platform | Active? | Score | Top Issue |
|----------|---------|:-----:|-----------|
| Website | [Yes/No] | [X/10] | [Issue] |
| Instagram | [Yes/No] | [X/10] | [Issue] |
| Twitter/X | [Yes/No] | [X/10] | [Issue] |
| LinkedIn | [Yes/No] | [X/10] | [Issue] |
| Facebook | [Yes/No] | [X/10] | [Issue] |
| TikTok | [Yes/No] | [X/10] | [Issue] |
| YouTube | [Yes/No] | [X/10] | [Issue] |
| Google Search | — | [X/10] | [Issue] |

### Overall Brand Score: [X/100]
```

### Step 4: Gap Analysis

Compare where the brand IS versus where it NEEDS TO BE:

```markdown
## Gap Analysis

### Perception vs. Reality

| Dimension | Where You Are | Where You Need to Be | Gap Size |
|-----------|-------------|---------------------|:--------:|
| **Authority** | [Current level of perceived expertise] | [Where your goals require you to be] | [Small/Medium/Large] |
| **Visibility** | [Current reach and discovery] | [Required reach for goals] | [Small/Medium/Large] |
| **Trust** | [Current credibility signals] | [What your audience needs to see] | [Small/Medium/Large] |
| **Clarity** | [How clear your message is now] | [Crystal clear positioning] | [Small/Medium/Large] |
| **Consistency** | [How consistent across channels] | [Unified brand experience] | [Small/Medium/Large] |
| **Engagement** | [Current audience interaction] | [Active community interaction] | [Small/Medium/Large] |
| **Conversion** | [Brand → business results] | [Brand drives revenue] | [Small/Medium/Large] |

### Top 5 Gaps (Ranked by Impact)
1. **[Gap 1]** — [Why it matters for business goals] — [What to do about it]
2. **[Gap 2]** — [Why it matters] — [What to do]
3. **[Gap 3]** — [Why it matters] — [What to do]
4. **[Gap 4]** — [Why it matters] — [What to do]
5. **[Gap 5]** — [Why it matters] — [What to do]
```

### Step 5: Competitor Positioning Comparison

Identify 3-5 people or brands in the same space and compare positioning:

```markdown
## Competitive Positioning

### Your Competitors (Personal Brand Space)

| Competitor | Platform Focus | Positioning | Audience Size | What They Do Well | Where You Beat Them |
|-----------|---------------|------------|:-------------:|------------------|-------------------|
| [Name 1] | [Platform] | [How they position] | [Rough size] | [Strength] | [Your edge] |
| [Name 2] | [Platform] | [How they position] | [Rough size] | [Strength] | [Your edge] |
| [Name 3] | [Platform] | [How they position] | [Rough size] | [Strength] | [Your edge] |

### Positioning Map

**[Dimension 1 axis — e.g., "Educational vs. Entertaining"]**
**[Dimension 2 axis — e.g., "Beginner vs. Advanced Audience"]**

[Text-based positioning map showing where the user sits relative to competitors]

### Positioning Recommendation
[2-3 paragraphs on how the user should position relative to competitors. What space is open? What angle is underserved? What makes them genuinely different?]
```

### Step 6: 30-Day Brand Improvement Plan

```markdown
## 30-Day Brand Improvement Plan

### Week 1: Foundation (Fix the Basics)
| Day | Task | Platform | Time Needed |
|:---:|------|----------|:-----------:|
| 1 | [Update all bios to match new positioning] | All | 1 hour |
| 2 | [Fix profile photos for consistency] | All | 30 min |
| 3 | [Update website messaging / hero section] | Website | 1 hour |
| 4 | [Create or update link-in-bio page] | All | 30 min |
| 5 | [Pin/highlight best content on each platform] | All | 30 min |
| 6-7 | [Content batch: create 5 posts following content pillars] | Primary platforms | 2 hours |

### Week 2: Content Machine (Start Posting Consistently)
| Day | Task | Platform | Time Needed |
|:---:|------|----------|:-----------:|
| 8 | [Post #1 — educational content from pillar 1] | [Platform] | 30 min |
| 9 | [Post #2 — personal story / behind-the-scenes] | [Platform] | 30 min |
| 10 | [Post #3 — authority content from pillar 2] | [Platform] | 30 min |
| 11 | [Engage with 20 accounts in your niche for 30 min] | [Platform] | 30 min |
| 12 | [Post #4 — value post from pillar 3] | [Platform] | 30 min |
| 13-14 | [Content batch for next week + engage with audience] | All | 2 hours |

### Week 3: Authority Building (Get Visible)
| Day | Task | Platform | Time Needed |
|:---:|------|----------|:-----------:|
| 15 | [Publish longer-form content (article, video, thread)] | [Platform] | 1 hour |
| 16 | [Comment thoughtfully on 10 posts from bigger accounts] | [Platform] | 30 min |
| 17 | [Post #5 — social proof / results / testimonial] | [Platform] | 30 min |
| 18 | [Reach out to 3 people for collaboration or features] | DMs/Email | 30 min |
| 19 | [Post #6 — controversial or bold take from pillar 1] | [Platform] | 30 min |
| 20-21 | [Review analytics from first 2 weeks + adjust] | All | 1 hour |

### Week 4: Optimize and Scale (Double Down on What Works)
| Day | Task | Platform | Time Needed |
|:---:|------|----------|:-----------:|
| 22 | [Repurpose best-performing content to other platforms] | Cross-platform | 1 hour |
| 23 | [Post #7 — expand on what got the most engagement] | [Platform] | 30 min |
| 24 | [Post #8 — audience question / poll / engagement driver] | [Platform] | 30 min |
| 25 | [Create an email opt-in or lead magnet if none exists] | Website | 1-2 hours |
| 26 | [Post #9 — call to action post (drive traffic somewhere)] | [Platform] | 30 min |
| 27-28 | [Month-end review: what worked, what didn't, plan next month] | All | 1 hour |

### Total Time Investment: ~20-25 hours over 30 days (~45 min/day)
```

### Step 7: Content Pillar Recommendations

```markdown
## Content Pillar Recommendations

Content pillars are the 3-5 core topics your brand consistently creates around. Every post should tie back to one of these.

### Recommended Pillars

**Pillar 1: [Topic]** — "[One-line description]"
- Why: [How this serves your business goals]
- Content types: [Educational posts, how-to videos, case studies, etc.]
- Example posts: [3 specific post ideas]

**Pillar 2: [Topic]** — "[One-line description]"
- Why: [How this serves your business goals]
- Content types: [Behind-the-scenes, stories, day-in-the-life, etc.]
- Example posts: [3 specific post ideas]

**Pillar 3: [Topic]** — "[One-line description]"
- Why: [How this serves your business goals]
- Content types: [Results, testimonials, proof, data, etc.]
- Example posts: [3 specific post ideas]

**Pillar 4: [Topic]** — "[One-line description]" (optional)
- Why: [How this serves your business goals]
- Content types: [Hot takes, industry commentary, trends, etc.]
- Example posts: [3 specific post ideas]

**Pillar 5: [Personal/Lifestyle]** — "[One-line description]" (optional)
- Why: [People buy from people — humanize the brand]
- Content types: [Personal stories, values, hobbies, wins, failures]
- Example posts: [3 specific post ideas]

### Content Mix Ratio
- [X]% Pillar 1 (Educational / Value)
- [X]% Pillar 2 (Personal / Storytelling)
- [X]% Pillar 3 (Proof / Authority)
- [X]% Pillar 4 (Industry / Commentary)
- [X]% Pillar 5 (Lifestyle / Human)
```

### Step 8: Bio and Tagline Suggestions

```markdown
## Bio & Tagline Suggestions

### Universal Bio (Adapt per platform)

**Option 1 (Authority-led):**
[Title/Role] | [Key achievement or credential] | [What you help people do] | [CTA]

**Option 2 (Value-led):**
[What you do for people] | [Proof point] | [Brand slogan or philosophy] | [CTA]

**Option 3 (Story-led):**
[From X to Y] | [What you teach/share/build now] | [CTA]

### Platform-Specific Bios

**Instagram:** [150 chars max — punchy, emoji-light, link mention]
**Twitter/X:** [160 chars max — personality-forward, no hashtags]
**LinkedIn:** [Professional headline — title + what you do + who you help]
**TikTok:** [80 chars max — casual, direct, curiosity-driven]

### Tagline Options
1. "[Tagline — 5-8 words max, memorable, positions the brand]"
2. "[Tagline option 2]"
3. "[Tagline option 3]"
4. "[Tagline option 4]"
5. "[Tagline option 5]"

### Evaluation Criteria
A great tagline or bio:
- Answers "what do you do?" in under 10 words
- Speaks to the AUDIENCE's desire, not your resume
- Is memorable enough to repeat to someone else
- Differentiates you from everyone else in your space
```

### Step 9: Compile and Save

Assemble everything into a single document:

```markdown
# Personal Brand Audit: [Name/Brand]

> **Date:** YYYY-MM-DD
> **Subject:** [Person or brand audited]
> **Industry/Niche:** [Space]
> **Overall Brand Score:** [X/100]
> **Prepared By:** LindaAI

---

## Current Brand Snapshot
[From Step 3]

## Gap Analysis
[From Step 4]

## Competitive Positioning
[From Step 5]

## 30-Day Improvement Plan
[From Step 6]

## Content Pillar Recommendations
[From Step 7]

## Bio & Tagline Suggestions
[From Step 8]

---

🤠 *Generated by LindaAI* 🏇
*Revisit this audit quarterly to track progress and adjust strategy.*
```

Save to: `brain/research/brand-audit-{YYYY-MM-DD}.md`

### Step 10: Present to User

Give the user:
1. The overall brand score (X/100) with a one-line verdict
2. The top 3 gaps ranked by impact
3. The positioning recommendation (how to differentiate)
4. The 30-day plan summary (Week 1 priorities)
5. The top bio/tagline suggestion
6. Where the full audit was saved

## Quality Standards

1. **Honest, not flattering.** The audit is only useful if it tells the truth. If the brand is weak, say so with specifics and solutions.
2. **Evidence-based.** Scores and assessments are based on what was actually found online, not assumptions. If a platform could not be found or assessed, say so.
3. **Actionable over analytical.** Every finding comes with a recommendation. "Your bio is unclear" is useless without "Here's a better bio."
4. **Goal-aligned.** The improvement plan and recommendations tie directly back to the user's business goals, not generic brand advice.
5. **Platform-current.** Recommendations reflect how each platform works TODAY (algorithms, formats, best practices), not two years ago.
6. **Respectful of time.** The 30-day plan must be achievable — 30-60 minutes per day max. Entrepreneurs do not have time for a full-time brand-building schedule.

## Output Format

A single comprehensive markdown file containing the full brand audit (snapshot, gap analysis, competitive comparison, 30-day plan, content pillars, bio/tagline suggestions). Typically 3,000-5,000 words. Saved to `brain/research/brand-audit-{YYYY-MM-DD}.md`.

## Example Usage

**User:** "Brand audit — @mikedavis on Instagram and @mikedavis on Twitter, website is sellfi.io"

**AI executes:**
- Researches all three channels plus Google search presence
- Scores each platform, identifies gaps in messaging consistency
- Compares positioning to 4 competitors in the creative finance space
- Builds a 30-day plan focused on Instagram and Twitter growth
- Generates 5 content pillars tied to SellFi and the T.O.P. Method
- Creates 3 bio options and 5 tagline suggestions
- Saves to `brain/research/brand-audit-2026-03-03.md`

**User:** "How does my LinkedIn profile look? Quick brand check."

**AI executes:**
- Focuses the audit on LinkedIn specifically (lighter scope)
- Evaluates: headline, about section, experience, content posting, engagement
- Provides LinkedIn-specific improvement plan (7-day instead of 30-day)
- Saves to `brain/research/brand-audit-2026-03-03.md`

**User:** "Brand audit for my real estate business — Rivera Capital Properties"

**AI executes:**
- Audits the business brand (not personal brand)
- Researches website, social channels, Google Business Profile, review sites
- Compares to local competitor real estate brands
- Content pillars focus on deal types, market insights, success stories
- Saves to `brain/research/brand-audit-2026-03-03.md`

## Error Handling

- **If the user does not provide social handles or a website:** Ask: "What are your social media handles and/or website URL? LindaAI needs at least one channel to audit. If you don't have any online presence yet, we can build a brand strategy from scratch instead."
- **If social profiles are private or cannot be accessed:** Note: "Your [Platform] profile appears to be private or could not be accessed. I'm auditing based on what's publicly visible. If you want a deeper audit, share screenshots or export your analytics."
- **If the user has no social presence:** Pivot to a brand-building plan instead of an audit: "Couldn't find an existing online presence for [name/brand]. Instead of an audit, LindaAI built a brand launch plan -- how to set up your profiles, what to post first, and how to build from zero."
- **If WebSearch returns very limited results:** Note which channels could and could not be assessed. Proceed with available data. Flag: "Limited public data was available for this audit. The scores reflect what I could find — your actual brand strength may be higher if you have engagement, clients, or reputation that isn't visible online."
- **If `brain/research/` does not exist:** Create it automatically before saving.
- **If a brand audit file already exists for this date:** Overwrite — the user is likely re-running. Note: "Updated your existing brand audit."
- **If the user asks for a competitor brand audit (not their own):** Proceed, but adjust the framing -- it becomes competitive intelligence rather than self-improvement. Note: "This is a brand audit of [competitor], not your own brand. Want LindaAI to audit your brand too and compare?"

🤠 *Generated by LindaAI* 🏇

---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
