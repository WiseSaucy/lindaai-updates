---
name: linda-accountability
description: This skill should be used when the user asks to "set up accountability check-ins", "daily check-in for {client}", "weekly accountability", "send check-in messages", "track client commitments", "who missed check-ins this week", "accountability cadence", "send the Sunday check-in", "missed check-ins report", "client adherence", or any request involving setting and running an accountability cadence for coaching clients — generating check-in messages, tracking completions, and flagging missed weeks for coach attention.
tags: [life-coach, accountability, check-ins, retention]
version: 1.0.0
---

# Accountability Check-In Engine

## Overview

Sets the cadence (daily / weekly / custom), generates the check-in messages, tracks who responded, and flags clients who've gone quiet so the coach can intervene before churn. The thing every coach SAYS they do — actually done.

> **Coaching is not therapy or medical advice — refer clients to licensed professionals when needed.**

## When to Use (Trigger Phrases)

- "Set up accountability for {client}"
- "Send today's check-ins"
- "Who missed check-ins this week?"
- "Adherence report"
- "Change {client}'s cadence to weekly"
- "Sunday check-in for everyone"

## How It Works

### License Check

Verify `~/.claude/linda-license.json` (exists, not expired, status active, optional server validation). Country-voice halt on failure.

### Step 0: Inputs

| Input | Required |
|-------|----------|
| Action: setup / send / report / change | Yes |
| Client name(s) | Yes (or "all" for batch) |
| Cadence (daily / weekday / weekly / custom) | Yes for setup |
| Day-of-week + time (for weekly) | Yes for setup |
| Channel (text/email/voice/Telegram/in-app) | Yes for setup |
| Active commitments (from latest session) | Auto-pull from latest `sessions/*.md` |

### Step 1: Spin Up

> 🤠 "Let's gooooooo — kickin' off the check-in run."

Load the client(s) profile and most recent session file(s).

### Step 2: Setup (if action = setup)

Write to `brain/life-coach/clients/{slug}/cadence.json`:

```json
{
  "client": "{name}",
  "cadence": "weekly",
  "day": "Sunday",
  "time": "18:00",
  "tz": "America/Chicago",
  "channel": "text",
  "active": true,
  "started": "{date}"
}
```

Confirm to coach + offer to schedule first send.

### Step 3: Generate Check-In Message (if action = send)

Pull from latest session: action items + homework. Tone: warm, specific, never robotic. Default template:

```
Hey {first} — quick check-in 🤠

How'd this week land?

1. {action 1} — done? what got in the way?
2. {action 2} — done?
3. {action 3} — done?

Homework: {summary} — how'd it feel?

One word for the week. Hit me back when you can.

— {Coach name}
```

For daily cadence — shorter:

```
{First} — daily nudge:
- Did you do the rep? (Y/N)
- One word for the day.
- Anything blocking tomorrow?
```

Save outgoing message to `brain/life-coach/clients/{slug}/checkins/{YYYY-MM-DD}-out.md`.

### Step 4: Track Responses

When coach forwards a client reply (or pastes it):

- Save to `brain/life-coach/clients/{slug}/checkins/{YYYY-MM-DD}-in.md`
- Mark commitments done/missed in a per-client `adherence.csv`:
  `date,action,status (done/partial/missed),note`
- If 2+ consecutive misses → bump churn-risk in `linda-clientcoach`
- If client reports a crisis or red flag → STOP, surface to coach, recommend licensed pro

### Step 5: Adherence Report (action = report)

For "who missed this week" / weekly adherence:

```
🤠 Adherence Report — {date range}

Client            Cadence   Sent   Replied   Done   Missed   Risk
-----------------------------------------------------------------
Jenna Hill        weekly    1      1         3/3    0        🟢 low
Mark Chen         daily     7      5         4/7    3        🟡 med
Lisa Park         weekly    1      0         0/3    3        🔴 HIGH

Coach action items:
- Lisa Park — 3 weeks no response. Personal call recommended.
- Mark Chen — slipping on workouts; check the block.
```

### Step 6: Save & Handoffs

- All artifacts under `brain/life-coach/clients/{slug}/checkins/`
- Per-client `adherence.csv`
- Master `brain/life-coach/accountability/weekly-report-{date}.md` for batch reports

Handoffs:
- `linda-clientcoach` — bump churn-risk score on 2+ misses
- `linda-followup` — schedule next check-in send
- `linda-mail` — if coach wants a personal "are you okay" email drafted for high-risk clients

## Output Format

For send:
```
🤠 Yeeee Hawww — check-ins drafted for {N} clients.

Saved to checkins/{date}-out.md (per client).
Channel: {text/email/etc.}
Send window: {time, tz}
```

For report: see Step 5 table.

## Examples

**User:** "Set up weekly Sunday 6pm CT text check-ins for Jenna Hill, channel text. Pull her last session action items."

**LindaAI:** Reads latest `sessions/*.md` for jenna-hill, writes `cadence.json`, drafts the Sunday template populated with her 3 action items + homework, saves preview to `checkins/2026-05-04-out.md`, confirms to coach.

**User:** "Who missed check-ins this week?"

**LindaAI:** Scans every active client's adherence.csv for the past 7 days, renders the adherence table, surfaces high-risk clients with a recommended next move.

## Voice Rules

- Country with Boss / coach. "Let's gooooooo" on start, "Yeeee Hawww 🤠" on send.
- Client-facing check-in: warm and specific. Country flavor only if matches coach brand.
- Never shame a missed week — always lead with curiosity ("what got in the way") not judgment.

## Brand Rules (PDFs)

- LindaAI top-right · {customer_handle} bottom-right · © 2024–2026 (when adherence reports get exported)

## Error Handling

- No latest session file: route to `linda-session` first — can't check in on actions you haven't logged.
- Missing cadence.json: prompt for setup.
- Crisis language detected in reply: PAUSE, surface to coach, recommend referral to licensed professional. Coaching is not therapy.
- Channel = text/iMessage/Telegram: this skill drafts only — handoff to send is the coach's job (or `linda-mail` for email).
- Create `brain/life-coach/accountability/` if missing.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
