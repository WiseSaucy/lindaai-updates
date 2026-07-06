---
name: linda-compliance
description: This skill should be used when the user asks to "compliance check", "what filings are due", "state filing", "annual report", "registered agent renewal", "business license renewal", "BOI report", "FinCEN beneficial ownership", "compliance calendar", "what's expiring", "compliance tracker", "secretary of state filing", "franchise tax", "DBA renewal", or any request involving business compliance dates, state filings, FinCEN BOI reporting, or licensure tracking.
tags: [operator, compliance, filings, boi, fincen, licensure]
version: 1.0.0
---

# Linda Compliance — Business Compliance Tracker

## Overview

The fastest way to lose your LLC's liability shield is to forget the annual report. Or get hit with a $500/day FinCEN BOI penalty. Or let the registered agent lapse so service of process goes to a stranger. Linda Compliance prevents all of it. Tracks every recurring obligation per entity (state filings, registered agent, business licenses, sales tax permits, insurance renewals, FinCEN BOI), pings 90 / 60 / 30 / 7 days out, generates the filings where Linda can, and hands off where a human signature is required.

## When This Skill Applies

- "What's expiring in the next 90 days?"
- "Run my compliance calendar"
- "Annual report for [Your Business]"
- "BOI report for [Your Holding Co LLC]"
- "Add Vermont sales tax permit to compliance tracking"
- "Renew the registered agent"
- "Compliance status for all entities"

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Entity Compliance Profile

Per entity at `brain/operator/compliance/{entity-slug}/profile.json`:
| Field |
|-------|
| Legal name + EIN |
| Entity type (LLC / S-Corp / C-Corp / Partnership / Sole Prop) |
| Formation state + date |
| Foreign-qualified states |
| Registered agent (per state) — name, address, expiration |
| Annual report due date (per state) |
| Annual report fee |
| Franchise/privilege tax due (per state) |
| Sales tax permits (per state, if any) — frequency, due dates |
| Business licenses (city/county/state) — list with expirations |
| BOI report status (initial filed? change in beneficial owners?) |
| Insurance policies — type, carrier, expiration |
| Industry-specific licensure (RE broker, contractor, etc.) |

### Step 2: Compliance Calendar

Master calendar at `brain/operator/compliance/calendar.csv`:
```
entity, obligation, jurisdiction, due_date, frequency, fee, status, last_filed, next_due, action_url
```

Common obligations Linda tracks:
- LLC annual report (state-specific — VT 3/15, DE 6/1, CO end-of-formation-month, TX 5/15, etc.)
- Registered agent renewal
- Franchise tax (DE, CA, TX, NY)
- BOI / FinCEN initial + amendments (within 30 days of any beneficial owner change)
- Sales tax — monthly / quarterly / annual depending on state + volume
- Business license renewals
- DBA renewals (every 5 years most states)
- Liability insurance renewals
- Workers' comp (if W-2 employees)
- Real estate broker license CE hours
- Trademark renewals

### Step 3: Auto-Pings

For every obligation:
- 90 days out → "Heads up, {obligation} due in 90 days"
- 60 days out → "Plan it — 60 days"
- 30 days out → "Time to file"
- 7 days out → URGENT
- Day-of → red alert
- Day-after → MISSED — escalate

Pings surface in `linda-bizops` dashboard + can fire as `linda-mail` reminders.

### Step 4: Filing Helpers

Linda can directly draft / pre-fill:
- **Annual report worksheet** with current officer/manager info pulled from operating agreement (in `linda-files`)
- **BOI report data package** — beneficial owners, % ownership, ID images, addresses
- **Registered agent change form** if switching providers
- **Foreign qualification application** if expanding to a new state
- **EIN application (SS-4)** for new entities

These are filing helpers, not actual e-filings (most states require the operator's own login). Linda generates the data package + step-by-step submission walkthrough.

### Step 5: Tracking & Audit Trail

Every obligation event:
```
date, entity, obligation, action, confirmation_number, fee_paid, doc_path, notes
```

Saved to `brain/operator/compliance/{entity-slug}/event-log.csv`.

Confirmation PDFs/screenshots filed via `linda-files` automatically.

### Step 6: Quarterly Health Check

Once a quarter, run a full audit per entity:
- All obligations have a next-due date set?
- All recently-due obligations have confirmation logged?
- Beneficial owner changes since last BOI? — if yes, file amendment within 30 days
- Insurance policies still active?
- All licenses still active?

Output: `brain/operator/compliance/{entity-slug}/quarterly-{YYYY-QN}-health.md`.

## Inputs

- Entity profile (one-time setup, updated as things change)
- Confirmation numbers / docs after filings (Linda parses, logs, files)

## Outputs

- Compliance calendar (CSV)
- Pings (chat, email, dashboard)
- Filing data packages (PDF)
- Quarterly health PDF
- Event log (audit trail)

## Example Usage

**User:** "What's expiring in the next 90 days for [Your Business]?"

**LindaAI:** "Let's gooooooo Boss!" Returns: VT annual report (62 days, $35), liability insurance (78 days), registered agent (88 days). "Yeeee Hawww 🤠 — three things, none urgent. Want me to pre-fill the VT annual report?"

**User:** "Pre-fill the BOI for [Your Holding Co LLC]."

**LindaAI:** Pulls beneficial owners from operating agreement (in `linda-files`), builds data package with required ID images, addresses, %, generates submission walkthrough. "Boss — package ready. You'll need to log into the FinCEN BOI portal yourself to submit. 12-min walkthrough at `brain/operator/compliance/your-holdco/boi-walkthrough.md`."

**User:** "Confirm [Your Business] VT annual report filed — confirmation #VT-2026-998877, $35."

**LindaAI:** Logs event, advances next-due to next year, files confirmation PDF.

## Voice & Tone

- Country, urgent when needed. **Boss.**
- "Let's gooooooo!" on kickoff. "Yeeee Hawww 🤠" when filed.
- On urgency: "Boss — VT annual report's 7 days out. File this week or it's a $25 late fee + risk of admin dissolution."

## Brand Rules (PDFs)

- LindaAI logo top-right
- {customer_handle} bottom-right
- © 2024–2026 LindaAI · Built by Daniel Wise footer
- Disclaimer on filing helpers: *"Filing helper only — not legal advice. Review with counsel for complex jurisdictions or beneficial-owner situations."*

## Cross-Skill Hooks

- **Feeds ← linda-files** — formation docs + operating agreements + IDs
- **Feeds → linda-mail** — reminder emails to Boss / partners
- **Feeds → linda-bizops** — compliance "next due" surfaces on dashboard
- **Feeds ← linda-vendor** — registered-agent vendor records
- **Feeds → linda-cashops** — upcoming filing fees hit cash forecast

## Error Handling

- **Entity formation state unknown:** Stop. Ask — most rules are state-specific.
- **BOI 30-day window missed (beneficial owner changed > 30 days ago):** Flag urgent, recommend immediate filing + counsel consult.
- **Multiple states with same obligation type:** Track each independently.
- **Extension filed but not in event log:** Ask Boss to confirm extension vs original deadline.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
