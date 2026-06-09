---
name: linda-payroll
description: This skill should be used when the user asks to "track contractor hours", "pay contractors", "payroll run", "1099 summary", "year-end 1099-NEC", "ACH payment run", "contractor payroll", "W-9 collection", "send a W-9 request", "payroll pulse", "contractor pay summary", "payroll export", "bank ACH file", or any request involving contractor payment tracking, 1099 management, W-9 collection, or payroll runs.
tags: [operator, payroll, 1099, contractors, w9, ach]
version: 1.0.0
---

# Linda Payroll — Contractor & Payroll Pulse

## Overview

Most operators run on contractors, not W-2 employees, and that means 1099-NEC season hits like a freight train every January. Linda Payroll keeps the train slow and clean: tracks contractor hours and project work, holds W-9s on file, runs scheduled pay runs (export-to-bank ACH file or check list), and produces 1099-NEC year-end summaries ready to file (or hand to a CPA / Track1099 / Tax1099). Includes W-9 collection workflow with auto-reminders.

## When This Skill Applies

- "Add contractor hours for Drew this week"
- "Run today's contractor pay run"
- "Build the ACH export for Mercury"
- "Send Drew a W-9 request"
- "Generate 1099-NEC summaries for 2025"
- "How much have I paid Drew YTD?"
- "Payroll pulse for Q1"

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Contractor Roster

Each contractor record at `brain/operator/payroll/contractors/{slug}.json`:
| Field | Notes |
|-------|-------|
| Legal name | |
| Business name | If LLC |
| EIN or SSN (encrypted at rest) | |
| Address | For 1099-NEC mailing |
| Contact | email, phone |
| Pay rate | $/hr or flat / project |
| Pay schedule | Weekly / Bi-weekly / Per-project / On-completion |
| Payment method | ACH / check / Zelle / PayPal |
| ACH info | routing + account (encrypted) |
| W-9 on file? | bool + link to `linda-files` |
| 1099-NEC eligible? | usually yes if >$600/yr |
| Backup withholding? | bool — if no W-9, withhold 24% |
| Active? | bool |
| Engaged date | |

### Step 2: W-9 Collection Workflow

For any new contractor or any contractor without a W-9 on file:
1. Generate fillable W-9 PDF (Form W-9 Rev October 2018)
2. Send via `linda-mail` with clear instructions ("required by IRS before payment")
3. Track status in `brain/operator/payroll/w9-tracker.csv`:
   `contractor, sent_date, received_date, w9_path, status`
4. Auto-remind at 7 / 14 / 21 days if not received
5. If contractor refuses W-9 → flip backup withholding ON in record

### Step 3: Hours / Project Logging

Capture work units:
```
date, contractor, project, hours_or_units, rate, amount, description, approved_by
```

Saved to `brain/operator/payroll/timesheets/{YYYY-MM}.csv`.

### Step 4: Pay Run

When Boss47 says "run payroll":
1. Pull all unpaid timesheet rows for active contractors
2. Aggregate per contractor: total hours / units, gross pay
3. Apply backup withholding if flagged
4. Build pay run summary:
   ```
   contractor, gross, withholding, net, method, ach_routing, ach_account
   ```
5. Output formats:
   - **ACH NACHA file** (CCD or PPD format) — for upload to Mercury / Chase / etc.
   - **Check list** — printable for paper checks
   - **Per-contractor pay stub PDF** — gross / withholding / net / YTD totals
6. Save pay run to `brain/operator/payroll/runs/{YYYY-MM-DD}/`
7. After Boss47 confirms upload to bank, mark timesheet rows as Paid + book entries to `linda-books` (Contract Labor expense)

### Step 5: 1099-NEC Year-End

In January for prior tax year:
1. Pull all paid amounts per contractor for the year from `linda-books` Contract Labor + `linda-payroll` runs
2. Filter contractors with total ≥ $600 (1099-NEC threshold)
3. For each: generate Form 1099-NEC PDF with:
   - Payer info (entity name, EIN, address)
   - Recipient info (from W-9 — name, EIN/SSN, address)
   - Box 1: Nonemployee compensation
   - Box 4: Federal income tax withheld (if backup withholding)
4. Generate Form 1096 transmittal summary
5. Output package: `brain/operator/payroll/1099/{YYYY}/{contractor-slug}.pdf`
6. Hand off to CPA OR Track1099/Tax1099 e-file service (Linda generates the import CSV)

### Step 6: Save & Roll Up

- Contractor files: `brain/operator/payroll/contractors/`
- Timesheets: `brain/operator/payroll/timesheets/{YYYY-MM}.csv`
- Pay runs: `brain/operator/payroll/runs/{YYYY-MM-DD}/`
- W-9 tracker: `brain/operator/payroll/w9-tracker.csv`
- 1099 packages: `brain/operator/payroll/1099/{YYYY}/`

## Inputs

- Contractor info on add
- Hours / project work entries
- Pay run command
- (Year-end) tax year for 1099-NEC

## Outputs

- W-9 PDFs sent + tracked
- Pay-run NACHA file + check list + pay stub PDFs
- 1099-NEC + 1096 PDFs at year-end
- Booked entries in `linda-books`

## Example Usage

**User:** "Add Drew as a contractor — bi-weekly, $50/hr, ACH to {routing}/{account}, W-9 needed."

**LindaAI:** "Let's gooooooo Boss47!" Creates record, generates W-9 request via `linda-mail`. "Yeeee Hawww 🤠 — Drew's in the system. W-9 request fired."

**User:** "Drew worked 18 hours this week on the marketing site rebuild."

**LindaAI:** Logs 18 × $50 = $900 to current period. Confirms.

**User:** "Run today's pay run."

**LindaAI:** Aggregates unpaid hours: Drew $900, Liz $1,200, Mike (no W-9) $400 with $96 backup withholding → net $304. Builds NACHA file. "Yeeee Hawww 🤠 — pay run ready. NACHA at `brain/operator/payroll/runs/2026-04-30/mercury-ach.txt`. Upload to Mercury and confirm."

**User:** "Build my 2025 1099-NECs."

**LindaAI:** Pulls 2025 ledger, identifies 4 contractors over $600, generates 1099-NEC PDFs + 1096, and CSV import for Track1099.

## Voice & Tone

- Country, careful. **Boss47.**
- "Let's gooooooo!" on kickoff. "Yeeee Hawww 🤠" when run is locked.
- On compliance: "Boss47 — no W-9 from Mike yet. Backup withholding's on. Get the W-9 or IRS gets the cut."

## Brand Rules (PDFs)

- LindaAI logo top-right (pay stubs, 1099 cover sheet — NOT the actual IRS form which uses official format)
- {customer_handle} bottom-right
- © 2024–2026 LindaAI · Built by Daniel Wise footer

## Cross-Skill Hooks

- **Feeds → linda-books** — every paid run posts as Contract Labor expense
- **Feeds → linda-taxprep** — 1099-NEC summaries roll into year-end CPA package
- **Feeds → linda-files** — W-9s + signed contracts file in cabinet
- **Feeds ↔ linda-vendor** — contractor records cross-link with vendor records
- **Feeds → linda-mail** — W-9 requests, pay stubs to contractors
- **Feeds → linda-bizops** — payroll due / W-9 missing alerts on dashboard
- **Feeds → linda-cashops** — upcoming pay runs hit the cash forecast

## Error Handling

- **No W-9 + payment > $600:** Apply backup withholding 24%, alert Boss47.
- **ACH info missing:** Cannot build NACHA — fall back to check list.
- **Duplicate timesheet entry:** Detect by contractor+date+hours, ask before adding.
- **1099-NEC threshold edge case (exactly $600):** File anyway — IRS rule.
- **Foreign contractor (W-8 not W-9):** Branch to W-8BEN flow + 1042-S not 1099-NEC, flag for CPA.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
