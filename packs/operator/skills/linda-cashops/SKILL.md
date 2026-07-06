---
name: linda-cashops
description: This skill should be used when the user asks for a "cash flow forecast", "13-week cash flow", "rolling cash forecast", "AR aging", "AP aging", "accounts receivable aging", "accounts payable aging", "low cash alert", "cash position", "cash runway", "what-if hire", "what-if expense", "scenario model", "operational cash flow", or any request involving operational cash forecasting, AR/AP aging, or scenario modeling.
tags: [operator, cash-flow, forecast, ar, ap, scenarios]
version: 1.0.0
---

# Linda CashOps — Operational Cash Flow

## Overview

Most operators look at last month's P&L and call it cash management. Linda CashOps runs the actual operator playbook: a 13-week rolling cash forecast that shows next quarter day-by-day, AR aging on what's owed to you, AP aging on what you owe, low-cash alerts before you blow the bank, and scenario modeling (what happens if I hire a $5k/mo VA? if Comcast doubles? if the duplex sits vacant 3 months?). This is the difference between "running a business" and "operating a business."

## When This Skill Applies

- "Run my 13-week cash forecast"
- "What's my AR aging?"
- "What's my AP aging?"
- "Show me cash position"
- "What if I hire a $5k/mo VA?"
- "Model the duplex going vacant for 3 months"
- "How many weeks of runway?"

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Pull Current State

From `linda-books`:
- Current cash balance per account
- Last 90 days of inflows / outflows by category
- Recurring patterns (recognized via cadence detection — same vendor, similar amount, repeating ~30/14/7 days)

From `linda-payroll`:
- Upcoming pay runs

From `linda-compliance`:
- Filing fees coming due

From `linda-vendor`:
- Recurring vendor payments

### Step 2: Build the 13-Week Forecast

Day-by-day projection for 91 days:

| Week | Date | Opening Cash | Inflows | Outflows | Closing Cash | Notes |

Inflow types:
- AR collections (with aging probability — 0-30 days = 95%, 31-60 = 80%, 61-90 = 60%, 90+ = 30%)
- Recurring rents (if landlord)
- Recurring services revenue
- Confirmed contracts coming due

Outflow types:
- Recurring vendor payments (rent, software, insurance)
- Pay runs (fixed cadence)
- Filing fees from `linda-compliance`
- Estimated tax payments (4 quarters)
- Loan payments (per amortization)
- Discretionary buffer (5% default)

### Step 3: AR Aging

Pull all unpaid customer invoices from `linda-books`:
| Customer | Invoice # | Amount | Issue Date | Days Outstanding | Aging Bucket |
|----------|-----------|--------|------------|------------------|--------------|

Buckets: Current (0-30), 31-60, 61-90, 90+. Total per bucket. Flag accounts > 60 days for follow-up via `linda-mail`.

### Step 4: AP Aging

All unpaid vendor bills:
| Vendor | Bill # | Amount | Bill Date | Due Date | Days to Due / Days Overdue |

Highlight overdue + due-this-week. Recommend pay order (oldest first vs critical-vendor-first).

### Step 5: Low-Cash Alerts

Forecast detects:
- Any week where closing cash < 4-week trailing avg outflow → AMBER alert
- Any week where closing cash < 0 → RED alert
- Any week where closing cash < 1.5× pay run → "payroll risk"

Alerts surface in chat, on `linda-bizops` dashboard, and via `linda-mail` if user opted in.

### Step 6: Scenario Modeler

Boss says: "What if I hire a $5k/mo VA starting next month?"

Linda:
1. Clones baseline forecast
2. Inserts new $5k recurring outflow on the 1st of each month for 12 months
3. Recomputes 13-week forecast
4. Compares: baseline week-13 cash $X vs scenario $Y
5. Surfaces any new amber/red weeks
6. Recommends: "You can absorb. Closing-week-13 drops from $42k to $27k. No red weeks. Greenlight."

OR

"Boss — that hire pushes you red on week 8 (closing $-2,400). You'd need to either delay 60 days, cut $X elsewhere, or have a backstop. Don't sign yet."

Save scenarios to `brain/operator/cashops/scenarios/{name}-{YYYY-MM-DD}.md`.

### Step 7: Save Outputs

- 13-week forecast: `brain/operator/cashops/forecast-{YYYY-MM-DD}.{md,csv,pdf}`
- AR aging: `brain/operator/cashops/ar-aging-{YYYY-MM-DD}.{md,csv}`
- AP aging: `brain/operator/cashops/ap-aging-{YYYY-MM-DD}.{md,csv}`
- Scenarios: `brain/operator/cashops/scenarios/`

## Inputs

- (Auto) current state from `linda-books`, `linda-payroll`, `linda-compliance`, `linda-vendor`
- Scenario question from Boss

## Outputs

- 13-week cash forecast (PDF + CSV)
- AR aging report
- AP aging report
- Scenario comparison docs
- Alerts (chat + dashboard + email)

## Example Usage

**User:** "Run my 13-week forecast."

**LindaAI:** "Let's gooooooo Boss!" Builds forecast from current state. "Yeeee Hawww 🤠 — looks healthy. Lowest week is week 9 at $18k closing (Q1 estimated tax hits). No red weeks. AR is $24k, $8k of that is over 60 days — want me to fire follow-ups?"

**User:** "What if I hire a $5k/mo VA starting in 30 days?"

**LindaAI:** Models scenario, returns side-by-side. "You can absorb it. Week-13 cash drops from $42k to $27k. No red weeks. Greenlight."

**User:** "Show me AR aging."

**LindaAI:** Returns table + total by bucket + recommended next actions per stale invoice.

## Voice & Tone

- Country, blunt. **Boss.**
- "Let's gooooooo!" on kickoff. "Yeeee Hawww 🤠" when forecast is locked.
- On red alert: "Boss — week 8 goes red. Don't make new commitments till we fix this."

## Brand Rules (PDFs)

- LindaAI logo top-right
- {customer_handle} bottom-right
- © 2024–2026 LindaAI · Built by Daniel Wise footer
- Disclaimer: *"Forecast based on current data and recurring patterns. Real outcomes vary — review weekly."*

## Cross-Skill Hooks

- **Feeds ← linda-books** — current cash, recurring patterns, ledger
- **Feeds ← linda-payroll** — upcoming pay runs
- **Feeds ← linda-compliance** — filing fees + tax payments
- **Feeds ← linda-vendor** — recurring vendor payments
- **Feeds → linda-mail** — AR follow-ups + low-cash alerts
- **Feeds → linda-bizops** — cash position + alerts on dashboard

## Error Handling

- **Books not current:** Run `linda-books` import first, halt forecast.
- **No recurring patterns detected (new business):** Use last-90-day raw average + Boss-confirmed forward commitments.
- **AR / AP not tagged in books:** Auto-detect by category + counterparty, ask Boss to confirm a few uncertain ones.
- **Scenario assumes data Linda doesn't have:** Ask once, save to scenario file.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
