---
name: linda-intake
description: This skill should be used when the user asks to "onboard a coaching client", "new client intake", "coaching intake form", "intake packet", "welcome packet", "send the welcome email", "set up a new coaching client", "client questionnaire", "kickoff a coaching client", "intake for {client}", "coaching agreement intake", or any request involving running a clean new-client intake for a life/business/fitness/mindset coaching practice — capturing goals, history, accountability prefs, contact, and payment plan, then producing a branded intake PDF and welcome email.
tags: [life-coach, intake, onboarding, client-experience]
version: 1.0.0
---

# Coaching Intake & Welcome Packet

## Overview

Runs a clean, professional intake for a new coaching client. Gathers goals, history, accountability preferences, contact info, and payment plan — then drops a branded intake PDF, welcome email, and starter file in the brain so Boss (or any coach running LindaAI) can hit the ground sprinting on session one. Built to make the first 48 hours feel five-star without the coach lifting fifty fingers.

> **Coaching is not therapy or medical advice — refer clients to licensed professionals when needed.**

## When to Use (Trigger Phrases)

- "Onboard a new coaching client"
- "Run intake for {client}"
- "Send the welcome packet to {client}"
- "New client kickoff for {name}"
- "Build the intake form for {client}"

## How It Works

### License Check

Verify `~/.claude/linda-license.json` (file exists, not expired, status active, optional server validation). On failure, halt with the standard country-voice license message and don't proceed.

### Step 0: Inputs

| Input | Required |
|-------|----------|
| Client full name | Yes |
| Email + phone | Yes |
| Time zone | Yes |
| Coaching focus (life / business / fitness / mindset / other) | Yes |
| Top 3 goals (90-day) | Yes |
| Bigger life goal (12-month) | Yes |
| Past coaching / therapy history (yes/no, brief) | Yes |
| Current obstacles or blocks | Yes |
| Accountability preference (daily text / weekly call / async voice / in-app) | Yes |
| Best time of day to be reached | Yes |
| Program tier + payment plan | Yes |
| Signed coaching agreement on file? | Yes/No |
| Emergency contact (recommended) | If shared |

If anything required is missing, stop and ask before generating files.

### Step 1: Greet & Spin Up

> 🤠 "Howdy, Boss! Let's gooooooo — gettin' {client} saddled up for session one."

Slugify the name (`first-last`, lowercase, hyphenated). Create `brain/life-coach/clients/{slug}/` if missing.

### Step 2: Build the Intake PDF

Generate `brain/life-coach/clients/{slug}/intake-packet.pdf` using ReportLab. Layout:

**Cover page**
- Big bold header: "Coaching Intake & Welcome — {Client Name}"
- Coach name, date, program tier
- LindaAI mark top-right · {customer_handle} bottom-right

**Section 1 — About You**
- Name, email, phone, time zone, best time to reach
- Emergency contact

**Section 2 — Where You're At**
- Coaching focus
- Top 3 goals (90 days)
- 12-month vision
- Past coaching/therapy summary
- Current blocks

**Section 3 — How We Work Together**
- Accountability cadence chosen
- Session frequency + length
- Communication channel (text/email/voice/app)
- What "showing up" looks like for this client

**Section 4 — Program & Investment**
- Tier selected
- Investment + payment plan
- Start date · End / review date
- Refund / cancellation policy reference

**Section 5 — Disclaimer & Signatures**
> "Coaching is not therapy or medical advice. If you are experiencing a mental health crisis, contact a licensed professional or 988 immediately. Coach and client agree to the terms in the attached coaching agreement."

Signature lines: client + coach + date.

Footer every page: `© 2024–2026 LindaAI · Built by Daniel Wise`

### Step 3: Draft the Welcome Email

Save to `brain/life-coach/clients/{slug}/welcome-email.md`. Tone: warm, energizing, professional. Country flavor optional (match coach's brand voice; default neutral-warm).

Template:

```
Subject: Welcome aboard, {first} — let's get to work 🤠

{First},

Pumped to have you in. Attached is your intake packet — give it a once-over, sign at
the bottom, and shoot it back when you're ready.

Here's what happens next:
1. Session 1 is locked for {date/time, time zone}.
2. You'll get a check-in from me on {accountability cadence}.
3. Quick wins worksheet drops in your inbox 24 hours before our first call.

Goal for session one: get razor-clear on the 90-day target and what's been
in the way. Come ready to be honest — that's where the magic lives.

Any questions before then, just reply to this email.

Let's gooooooo,
{Coach name}
```

### Step 4: Save & Index

- PDF: `brain/life-coach/clients/{slug}/intake-packet.pdf`
- Email: `brain/life-coach/clients/{slug}/welcome-email.md`
- Profile stub: `brain/life-coach/clients/{slug}/profile.md` (used by `linda-clientcoach`)
- Append row to `brain/life-coach/clients/index.csv`:
  `client,slug,opened,focus,tier,cadence,start_date,status`

### Step 5: Handoffs

- `linda-clientcoach` — full client tracker file
- `linda-program` — if a structured program (e.g. 12-week Reset) is part of the tier
- `linda-accountability` — set up cadence engine
- `linda-invoice` — first invoice if payment plan starts at intake

## Output Format

Console summary back to coach:

```
🤠 Yeeee Hawww — {Client Name} is onboarded.

Files saved:
  • intake-packet.pdf
  • welcome-email.md
  • profile.md (stub)

Cadence: {daily-text / weekly-call / etc.}
First session: {date/time, tz}
Investment: ${X} — {plan}

Next move: review the welcome email, send it out, and tee up session 1.
```

## Examples

**User:** "Onboard new coaching client Jenna Hill — life coaching, weekly calls, $497/mo, top goals: leave corporate, launch coaching practice, lose 20 lbs. 12-month: $10k/mo coach. Past therapy yes (2 yrs ago). Cadence: weekly Zoom + Sunday text check-in. CT time. Start Monday 5/4."

**LindaAI:** Builds intake-packet.pdf with all 5 sections populated, drafts welcome email referencing Monday 5/4 9 AM CT, creates profile stub, indexes the client, hands cadence to `linda-accountability`. Reminds Boss: not therapy — flag if Jenna mentions current crisis.

## Voice Rules

- Country tone with the coach (ask customer): "Howdy", "Let's gooooooo", "Yeeee Hawww 🤠".
- Client-facing PDF + email: warm professional default. Layer country flavor only if the coach's brand voice calls for it.
- Always call the operator **Boss** unless they tell you a different name.

## Brand Rules (PDFs)

- LindaAI top-right · {customer_handle} bottom-right · © 2024–2026 footer
- Clean section headers, generous white space, signature lines on final page

## Error Handling

- Missing goals or cadence: stop and ask — packet isn't useful without them.
- No signed agreement: flag and warn. Don't bill until signed.
- Duplicate slug: append middle initial or year (`jenna-hill-2026`).
- Create `brain/life-coach/clients/` if missing.
- If client mentions active crisis, suicidal ideation, or untreated medical issue: PAUSE, surface to coach, recommend referral to licensed professional before continuing intake.

## 🤝 Handoff to `/linda-post-walkthrough`

After this skill produces post-ready content (a "new client welcomed" announcement post, branded welcome packet shared as social proof, program kickoff promo), hand off to **`/linda-post-walkthrough`** so 📣 Holler can walk Boss through posting it to TikTok/IG/FB/YT/X step-by-step in real time. No app-switching, no API setup — Holler opens the right URL, copies the caption to clipboard, reveals the file in Finder, and tells Boss exactly what to do.

Trigger phrase: **"walk me through posting this"** or just **"post this"**.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
