---
name: linda-program
description: This skill should be used when the user asks to "build a coaching program", "design a 12-week program", "create a coaching curriculum", "program builder", "weekly themes for my program", "design the {N}-week reset", "build my signature program", "coaching program PDF", "curriculum for clients", "group coaching program", or any request involving designing a multi-week coaching program with weekly themes, exercises, homework, milestones, and a deliverable PDF + asset list.
tags: [life-coach, program-builder, curriculum]
version: 1.0.0
---

# Coaching Program Builder

## Overview

Designs N-week coaching programs from a one-line concept. Maps weekly themes, core teachings, exercises, homework, milestones, and tools — then drops a polished program PDF plus a deliverables checklist (worksheets, audio prompts, email sequences) so Boss has a sellable, runnable signature program in one pass instead of three weekends.

> **Coaching is not therapy or medical advice — refer clients to licensed professionals when needed.**

## When to Use (Trigger Phrases)

- "Build a 12-week Reset program"
- "Design a coaching curriculum on {topic}"
- "Create my signature {N}-week program"
- "Program builder for {niche}"
- "Lay out the weekly themes for {program name}"

## How It Works

### License Check

Verify `~/.claude/linda-license.json` (exists, not expired, status active, optional server validation). Halt with country-voice message on failure.

### Step 0: Inputs

| Input | Required |
|-------|----------|
| Program name | Yes |
| Program length (weeks) | Yes |
| Target client (avatar) | Yes |
| Promise / outcome (what they walk away with) | Yes |
| Coaching focus (life/business/fitness/mindset/other) | Yes |
| Delivery (1:1 / group / hybrid / self-paced) | Yes |
| Session cadence (weekly call, daily voice, etc.) | Yes |
| Investment / price | Yes |
| Existing IP or frameworks to incorporate | Optional |
| Tone preference (country / neutral / corporate) | Default: warm-professional |

### Step 1: Spin Up

> 🤠 "Let's gooooooo, Boss — buildin' the {N}-week {program name}."

Slugify program name. Create `brain/life-coach/programs/{program-slug}/`.

### Step 2: Architecture Pass

Design the macro arc. Default 4-act structure mapped across the weeks:

- **Act 1 (first ~25%)** — Foundation: clarity, baseline, mindset reset
- **Act 2 (next ~30%)** — Build: skills, habits, daily reps
- **Act 3 (next ~30%)** — Push: hardest work, stretch goals, accountability heat
- **Act 4 (last ~15%)** — Land: integration, sustainability, graduation

Adjust ratios for length. A 4-week sprint compresses; a 26-week journey stretches.

### Step 3: Weekly Map

For each week, define:

```markdown
### Week {N} — {Theme}
**Outcome:** {what they walk away knowing/doing/feeling}
**Core teaching:** {1-2 sentences}
**Exercises:** {2-4 specific drills}
**Homework:** {between-session work}
**Milestone:** {checkpoint, if any}
**Tools delivered:** {worksheet, audio, template, email}
```

### Step 4: Build the Program PDF

Save to `brain/life-coach/programs/{program-slug}/program.pdf` (ReportLab).

Layout:
- **Cover** — Program name, length, promise, coach name, LindaAI top-right, {customer_handle} bottom-right
- **Welcome letter** — 1 page, warm
- **How this program works** — cadence, expectations, accountability
- **Program-at-a-glance table** — week, theme, milestone
- **Week-by-week pages** — full detail per the schema above
- **Tools index** — every worksheet/asset listed with delivery week
- **Graduation** — what's next, alumni offer (optional)
- **Disclaimer** — "Coaching is not therapy or medical advice. Results vary based on the work the participant puts in. For clinical issues, refer to a licensed professional."

Footer: `© 2024–2026 LindaAI · Built by Daniel Wise`

### Step 5: Deliverables Checklist

Save to `brain/life-coach/programs/{program-slug}/deliverables.md`:

```markdown
# {Program Name} — Deliverables Checklist

## Worksheets / PDFs
- [ ] Week 1: {name}
- [ ] Week 2: {name}
- ...

## Audio / Voice prompts
- [ ] Week X: {name}

## Email sequence (sales + onboarding + nurture)
- [ ] Welcome (day 0)
- [ ] Pre-week-1 prep
- [ ] Mid-program check-in
- [ ] Graduation
- [ ] Alumni / upsell

## Sales assets
- [ ] One-pager
- [ ] Sales page bullets
- [ ] FAQ
```

### Step 6: Save & Handoffs

- `program.pdf` — full curriculum
- `deliverables.md` — production checklist
- `program.json` — machine-readable spec for downstream skills
- Index: append to `brain/life-coach/programs/index.csv` — `program,slug,weeks,price,delivery,created`

Handoffs:
- `linda-coachcontent` — generate sales assets + nurture emails
- `linda-mail` — draft the welcome + mid-program emails
- `linda-clientcoach` — assign program to active clients

## Output Format

```
🤠 Yeeee Hawww — {Program Name} ({N} weeks) is built.

Files:
  • program.pdf — full curriculum, ready to sell
  • deliverables.md — what still needs to be produced
  • program.json — machine spec

Macro arc: {Act 1 weeks} → {Act 2} → {Act 3} → {Act 4}
Worksheets needed: {count}    Emails needed: {count}

Next move: review the PDF, then I can hand sales assets to linda-coachcontent.
```

## Examples

**User:** "Build my 12-week Reset program. Avatar: corporate woman 30-45, burned out, wants to start a coaching biz. Promise: leave corporate with $5k/mo coaching income. Delivery: weekly group Zoom + daily voice. Price: $4,997."

**LindaAI:** Designs 12 weeks, 3 weeks Foundation (clarity, money story, vision) → 4 weeks Build (offer, package, first 3 paying clients) → 4 weeks Push (sales, content, $5k month) → 1 week Land (transition plan + graduation). Renders program.pdf with weekly breakdown, drops deliverables.md with 12 worksheets + 5 emails + sales bullets, hands sales assets to `linda-coachcontent`.

## Voice Rules

- Country with Boss. "Let's gooooooo!" on kickoff. "Yeeee Hawww 🤠" on completion.
- Program PDF voice = warm-professional default; layer country only if coach's brand calls for it.
- Welcome letter feels like a handshake, not a corporate memo.

## Brand Rules (PDFs)

- LindaAI top-right · {customer_handle} bottom-right · © 2024–2026 footer
- Clean typography, week tabs/sidebars, plenty of white space
- Disclaimer block on inside back page

## Error Handling

- Length under 2 weeks or over 52: confirm before building (most programs land 4–26).
- Missing avatar or outcome: stop and ask — program is generic without them.
- Existing program with same slug: append `-v2`, keep prior version intact.
- Create `brain/life-coach/programs/` if missing.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
