---
name: linda-clientcoach
description: This skill should be used when the user asks to "show me {client}'s file", "client tracker", "coaching client file", "list my coaching clients", "update {client}'s status", "what program is {client} on", "{client} payment status", "client breakthroughs", "next session for {client}", "churn risk", "who's at risk of churning", "client snapshot", or any request involving managing per-client coaching files including program assignment, sessions completed, payment status, breakthroughs, next session, and churn-risk score.
tags: [life-coach, client-tracking, retention]
version: 1.0.0
---

# Master Client Tracker

## Overview

The single source of truth for every coaching client. One file per client, kept warm by every other skill in the pack — intake bumps it open, sessions log into it, accountability flags it, content asks permission through it. Pull up any client in seconds and know exactly where they stand: program, sessions completed, payment, breakthroughs, next session, and churn-risk score.

> **Coaching is not therapy or medical advice — refer clients to licensed professionals when needed.**

## When to Use (Trigger Phrases)

- "Show me {client}'s file"
- "Update {client}'s status"
- "List all my coaching clients"
- "Who's at churn risk?"
- "What's {client}'s payment status?"
- "Pull up {client}"

## How It Works

### License Check

Verify `~/.claude/linda-license.json` (exists, not expired, status active, optional server validation). Country-voice halt on failure.

### Step 0: Inputs

For new file: handed off from `linda-intake`.
For update: client name + what changed (status, program, payment, session, breakthrough, churn signal).
For view: client name (or "all").

### Step 1: Spin Up

> 🤠 "Let's gooooooo — pullin' up {client}'s file."

Locate `brain/life-coach/clients/{slug}/profile.md`. Create from intake template if missing and prompt for missing fields.

### Step 2: Standard Profile Schema

`brain/life-coach/clients/{slug}/profile.md`:

```markdown
# Client File — {Client Name}
**Opened:** {date} · **Status:** Active / Paused / Graduated / Churned
**Focus:** {life/business/fitness/mindset/other}
**Coach:** {name}

## Contact
- Email · Phone · Time zone · Best window
- Emergency contact (if shared)

## Program
- Program: {linked program slug or "1:1 custom"}
- Tier: {tier}
- Cadence: {cadence}
- Started: {date} · Target end: {date}

## Goals
- 90-day: {goals}
- 12-month: {vision}

## Session Stats
- Sessions completed: {N}
- Last session: {date}
- Next session: {date/time, tz}
- No-shows: {count}

## Payment
- Plan: ${X}/{period}
- Total contracted: ${Y}
- Paid to date: ${Z}
- Outstanding: ${W}
- Last payment: {date}
- Status: 🟢 current / 🟡 late / 🔴 delinquent

## Breakthroughs Log
- {date} — {breakthrough}

## Risk Flags
- {date} — {flag — coach action taken}

## Churn-Risk Score
**{0-100}** — {🟢 low / 🟡 med / 🔴 HIGH}
Inputs: missed check-ins, missed sessions, payment lateness, flat progress, energy in last session.
Last computed: {date}

## Activity Log
- {date} — {event}
```

### Step 3: Update Routines

Each event type bumps the right field + appends to Activity Log:

- New session logged → session count, last/next session dates, recompute churn risk
- Payment received → payment fields, status
- Missed check-in (from `linda-accountability`) → recompute churn risk
- Breakthrough recorded → Breakthroughs Log
- Risk flag from session → Risk Flags + alert coach
- Status change (pause/graduate/churn) → Status field + Activity Log

### Step 4: Churn-Risk Calculation

Simple weighted score (0-100, higher = more risk):

| Signal | Points |
|--------|--------|
| 2+ missed check-ins in row | +25 |
| 1 no-show session | +20 |
| Payment late >7 days | +20 |
| No progress on goals 3+ sessions | +15 |
| Low energy / disengaged language flagged | +10 |
| Asked about pause / refund | +30 |
| Hit a breakthrough this month | -15 |
| Paid in full / on time | -10 |

Bands: 0-29 🟢 low · 30-59 🟡 med · 60+ 🔴 HIGH (coach should personally reach out).

### Step 5: Snapshot / Roster Views

**Single client snapshot:**

```
🤠 {Client Name} — Snapshot

Status: Active   Program: 12-Week Reset (week 6/12)
Sessions: 5 done · Next: 2026-05-04 9 AM CT
Payment: 🟢 current — $2,498 of $4,997 paid
Last breakthrough: signed first paying client (2026-04-22)
Churn risk: 🟢 18

Recent: {last 3 activity log entries}
```

**Roster view (`list all`):**

```
Client          Status   Program            Sessions  Next       Pay   Risk
-----------------------------------------------------------------------------
Jenna Hill      Active   12-Week Reset 6/12 5         5/4 9am    🟢    🟢 18
Mark Chen       Active   1:1 Custom         12        5/3 7pm    🟡    🟡 42
Lisa Park       Paused   12-Week Reset 4/12 4         —          🔴    🔴 71
```

### Step 6: Save & Handoffs

- Profile: `brain/life-coach/clients/{slug}/profile.md`
- Roster CSV: `brain/life-coach/clients/index.csv` — `client,slug,status,program,sessions,next_session,pay_status,risk_score`
- Snapshot PDF on demand (LindaAI top-right, {customer_handle} bottom-right, © footer)

Handoffs:
- `linda-mail` — draft a re-engagement email for HIGH risk clients
- `linda-invoice` — chase delinquent payments
- `linda-followup` — schedule personal coach reach-out

## Output Format

See Step 5 — single snapshot or roster table. Always end with a coach next-move suggestion when something needs attention.

## Examples

**User:** "Show me Jenna Hill's file."

**LindaAI:** Renders single-client snapshot with all fields populated, surfaces last 3 activity entries, flags any open coach action items.

**User:** "Who's at churn risk?"

**LindaAI:** Filters roster to risk_score >= 60, shows coach exactly which clients need a personal touch this week, suggests `linda-mail` for re-engagement drafts.

## Voice Rules

- Country tone with Boss / coach. "Let's gooooooo" on pull-up, "Yeeee Hawww 🤠" on save.
- Snapshot text = professional, scannable. Country flavor in the header line only.
- Never share private coach notes in any client-facing export.

## Brand Rules (PDFs)

- LindaAI top-right · {customer_handle} bottom-right · © 2024–2026 footer
- Snapshot PDFs: 1 page, clean, includes coach name + practice brand line

## Error Handling

- Missing profile: route to `linda-intake`.
- Roster CSV out of sync: rebuild from individual profiles.
- Risk flag containing crisis language: surface IMMEDIATELY to coach, recommend referral to licensed professional. Coaching is not therapy.
- Client name collision: use middle initial + year in slug.
- Create `brain/life-coach/clients/` if missing.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
