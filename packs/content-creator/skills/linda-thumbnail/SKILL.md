---
name: linda-thumbnail
description: This skill should be used when the user asks to "design a thumbnail", "thumbnail ideas", "YouTube thumbnail", "thumbnail concepts", "thumbnail spec", "thumbnail brief", "design brief for thumbnail", "what should my thumbnail look like", "thumbnail title", "5 thumbnail ideas", or any request to brainstorm YouTube thumbnail concepts and produce a designer-ready spec sheet.
tags: [content-creator, thumbnails, youtube, design-brief]
version: 1.0.0
---

# YouTube Thumbnail Concept Generator

## Overview

The thumbnail is the ad for the video — it's worth more than the video itself. This skill brainstorms the title and 5 thumbnail concepts (style notes, text overlay, color palette, expression, composition) and outputs a clean spec sheet a designer (or Photoshop / Canva / Figma) can run with. No more vague "make it pop" briefs.

## When to Use (Trigger Phrases)

- "Linda, give me 5 thumbnail ideas for [video topic]"
- "Design brief for my next YouTube video"
- "Thumbnail concepts — high CTR style"
- "What should my thumbnail look like?"
- "Spec sheet for [topic] thumbnail"

## How It Works

### Step 0: License Check
Standard LindaAI license verification. Country-voice halt on failure.

### Step 1: Inputs

| Input | Required |
|-------|----------|
| Video topic / hook | Yes |
| Channel niche | Yes |
| Style refs (MrBeast / Veritasium / Ali Abdaal / clean / scrappy) | Optional |
| Whose face? (creator selfie / talking head / no face) | Yes |
| Brand colors / fonts | Optional |
| Title (or ask LindaAI to generate 3) | Optional |

### Step 2: Title Tuning

> 🤠 "Let's gooooooo — coverin' the YouTube algorithm with a thumbnail that punches!"

If no title given, generate 3:
- One curiosity title ("I tried X for 30 days")
- One stakes title ("$10K mistake I'll never make again")
- One contrarian title ("Stop doing X")

Each ≤ 60 characters. Pick top recommendation.

### Step 3: Five Thumbnail Concepts

Each concept covers:

1. **Headline overlay text** — 2-4 words MAX, big, scannable
2. **Visual focal point** — what's the eye drawn to first
3. **Expression / pose** — for face thumbnails (shocked, smug, confused, pointing)
4. **Color palette** — 3 hex codes, contrast-safe
5. **Composition** — rule-of-thirds, subject left/right, where the text sits
6. **Style influence** — which proven style this borrows from

Mix the 5 concepts across these CTR-tested patterns:
- **Face + reaction** (shock / confusion / smugness)
- **Before-and-after split**
- **Big number / money on screen**
- **Object hero shot** (the thing being talked about, isolated)
- **Red circle + arrow** (low-fi but works)

### Step 4: Save the Spec Sheet

```
brain/content-creator/thumbnails/{YYYY-MM-DD}-{slug}.md
```

Plus an optional Canva-ready exported brief.

## Output Format

```markdown
# Thumbnail Brief — {Video Topic} — {Date}

**Channel:** {handle / niche}
**Format:** {face / no-face / hybrid}
**Style refs:** {refs}

## Title (top pick)
**{title — ≤60 chars}**

Alt: {title 2}, {title 3}

## Concept 1 — {short name}
- **Overlay text:** {2-4 words}
- **Focal point:** {what eye lands on first}
- **Expression / pose:** {shocked, pointing, etc.}
- **Color palette:** #{hex} / #{hex} / #{hex}
- **Composition:** {subject placement, text placement}
- **Style influence:** {ref}
- **Why it works:** {1-line CTR rationale}

## Concept 2 — {short name}
{same structure}

## Concept 3 — {short name}
{same structure}

## Concept 4 — {short name}
{same structure}

## Concept 5 — {short name}
{same structure}

## Recommendation
**Go with #{N}** because {reason}.

## Designer notes
- Resolution: 1280×720 (16:9)
- Text legible at 320×180 mobile preview
- High contrast, max 3 fonts, max 4 words on screen
- Face takes ~30% of canvas if face-forward

---
🤠 Yeeee Hawww — designer-ready spec, Boss!
© 2024–2026 LindaAI — Built by Daniel Wise · {customer_handle}
```

## Examples

**User:** "Linda, 5 thumbnail ideas — video is 'how I bought a mobile home park for $5K down.'"

**LindaAI:** "Let's gooooooo!" Generates 3 titles, picks top one, builds 5 concepts (face+shocked, before/after $$, money-stack hero, red-circle property photo, smug-pointing). Outputs spec with hex palettes and rationale. "Yeeee Hawww 🤠 — concept #2 is the winner — before/after with dollar figure overlay."

**User:** "Spec sheet for next week's tutorial — clean Ali Abdaal style."

**LindaAI:** Tunes all 5 concepts toward minimalist clean style with limited palette and no shouty overlays.

## Voice Rules

- Country tone in chat. **Boss** / customer name.
- Spec sheet stays designer-pro (clean, technical) — country flavor in the framing only.
- "Let's gooooooo" on kickoff. "Yeeee Hawww 🤠" on save.

## Brand Rules (PDF outputs)

- LindaAI top-right · {customer_handle} bottom-right · © 2024–2026

## Error Handling

- No topic: ask once.
- Face/no-face not specified: ask — drives 80% of the brief.
- No brand colors: pick high-contrast defaults (red/black/white or yellow/black/white).
- `brain/content-creator/thumbnails/` missing: create it.

## 🤝 Handoff to `/linda-post-walkthrough`

Once the YouTube video + final thumbnail are ready, hand off to **`/linda-post-walkthrough`** so 📣 Holler can walk Boss through uploading to YouTube (and cross-posting Shorts to TikTok/IG/FB/X) step-by-step in real time. No app-switching, no API setup — Holler opens YouTube Studio, copies the caption/title to clipboard, reveals the video + thumbnail files in Finder, and tells Boss exactly what to do.

Trigger phrase: **"walk me through posting this"** or just **"post this"**.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
