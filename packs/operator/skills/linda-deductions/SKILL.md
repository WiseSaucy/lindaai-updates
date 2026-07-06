---
name: linda-deductions
description: This skill should be used when the user asks to "track a deduction", "log this receipt", "photo of receipt", "snap this receipt", "log mileage", "track mileage", "add a business expense", "categorize this deduction", "running deduction total", "how much have I deducted", "deduction tracker", "tax deduction log", "business expense log", "mileage tracker", or any request involving real-time business expense / deduction capture and categorization.
tags: [operator, deductions, receipts, mileage, taxes, irs]
version: 1.0.0
---

# Linda Deductions — Real-Time Tracker

## Overview

Operators leave money on the IRS table because nobody logs receipts in the moment. Linda Deductions kills that. Snap a photo of a receipt, paste a transaction, dictate a mileage trip — Linda categorizes against IRS deduction categories (vehicle, meals, home office, supplies, software, travel, etc.), tallies running totals per category, warns on red-flag categories (meals > 5% revenue, home office > 10% revenue), and feeds clean data straight into `linda-taxprep` at year-end. No spreadsheet wrangling. No shoebox of receipts.

## When This Skill Applies

- "Snap this Home Depot receipt — $284 for property repairs"
- "Log 47 miles round trip to the property today"
- "Add a meal deduction — lunch with Liz $68"
- "How much have I deducted in vehicle so far this year?"
- "Show my running deduction totals"
- "Log this software subscription"

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Capture Mode

Linda accepts:
- **Photo of receipt** — OCR extracts vendor, date, total (Boss confirms category)
- **Text entry** — "Lunch with Liz, Texas Roadhouse, $68.40, 4/22, business development"
- **Mileage entry** — "47 miles, property visit at 123 Main, 4/22"
- **Bulk transaction tag** — point at a row in `linda-books` and tag as deductible
- **Voice memo** — transcribe and parse

### Step 2: Categorize (IRS Schedule C Categories)

Map to one of:

| Category | Sch C Line | Notes |
|----------|------------|-------|
| Advertising | 8 | Ads, marketing, branding |
| Car & Truck | 9 | Mileage OR actual expenses |
| Commissions | 10 | Paid to others |
| Contract Labor | 11 | 1099-NEC |
| Insurance (non-health) | 15 | Liability, errors-omissions |
| Interest (other) | 16b | Loan interest, credit card biz |
| Legal & Professional | 17 | Lawyers, CPAs, consultants |
| Office Expense | 18 | Paper, ink, small supplies |
| Rent — Other (real prop) | 20b | Office space |
| Repairs & Maintenance | 21 | Property fixes |
| Supplies | 22 | Job materials |
| Taxes & Licenses | 23 | Business licenses, sales tax |
| Travel | 24a | Out-of-town business travel |
| Meals (50%) | 24b | Business meals — auto-halved |
| Utilities | 25 | Office utilities |
| Wages | 26 | W-2 employees |
| Software / SaaS | 27a Other | Notion, Adobe, etc. |
| Home Office | Form 8829 | Separate worksheet |
| Education | 27a Other | Books, courses (business) |
| Bank / Merchant Fees | 27a Other | Stripe, processor fees |

### Step 3: Build the Receipt Record

For each entry write to `brain/operator/deductions/{entity}/{YYYY}/log.csv`:
```
date, vendor, amount, category, sch_c_line, description, receipt_path, business_purpose, attendees, miles, deductible_amount, notes
```

For receipts: store the image at `brain/operator/deductions/{entity}/{YYYY}/receipts/{YYYY-MM-DD}-{vendor-slug}.jpg`

For meals: capture business purpose + attendees (IRS audit defense). Auto-halve to 50% deductible.

For mileage: log start/end addresses, business purpose, miles. Update yearly mileage running total. Apply current IRS standard mileage rate (default 67¢/mi 2024 — pull current via WebFetch IRS.gov on first run of new year).

### Step 4: Tally & Alert

Running totals updated in `brain/operator/deductions/{entity}/{YYYY}/totals.json`:
```json
{
  "ytd_by_category": { "vehicle": 3214.40, "meals": 842.00, ... },
  "ytd_total_deductions": 18420.50,
  "ytd_business_miles": 4820,
  "ytd_meals_pct_revenue": 1.7,
  "ytd_home_office_pct_revenue": 8.4,
  "alerts": ["Meals at 1.7% — healthy", "Home office at 8.4% — okay; >10% draws audit risk"]
}
```

Red-flag thresholds:
- Meals > 5% of revenue
- Home office > 10% of revenue
- Vehicle > 30% of revenue
- Travel > 8% of revenue (without supporting calendar)
- Any single deduction > $5,000 without receipt → urgent flag

### Step 5: Periodic Reports

On request:
- "Show my Q1 deductions" → quarterly summary by category, PDF + MD
- "Year-to-date total" → quick text summary
- "Audit-ready PDF" → polished report with receipts indexed, business purposes documented

Save reports to `brain/operator/deductions/{entity}/{YYYY}/reports/`.

## Inputs

- Receipt photo OR text description OR mileage trip
- Entity (defaults to active entity)
- Business purpose (required for meals + travel)

## Outputs

- Single log row appended
- Receipt image stored
- Updated running totals JSON
- (On request) period summary PDF

## Example Usage

**User:** "Snap this — Home Depot $284.16, drywall and paint for the duplex." (attaches photo)

**LindaAI:** "Let's gooooooo Boss!" OCRs receipt, confirms vendor + amount, categorizes as Repairs & Maintenance (Sch C Line 21), saves image, logs row. "Yeeee Hawww 🤠 — booked. YTD repairs at $4,210."

**User:** "Log 47 miles to the Burlington property today, due diligence walk."

**LindaAI:** Logs mileage, business purpose "DD walkthrough — Burlington property". "$31.49 deductible at 67¢/mi. YTD business miles: 1,847."

**User:** "How much have I deducted so far this year?"

**LindaAI:** Returns YTD total + breakdown by top 5 categories + any active red flags.

## Voice & Tone

- Country, fast, encouraging. **Boss.**
- "Let's gooooooo!" on kickoff. "Yeeee Hawww 🤠" when logged.
- Celebrate the savings: "That's another $94.50 the IRS ain't gettin'."

## Brand Rules (PDFs)

- LindaAI logo top-right
- {customer_handle} bottom-right
- © 2024–2026 LindaAI · Built by Daniel Wise footer

## Cross-Skill Hooks

- **Feeds → linda-taxprep** — entire log rolls into year-end CPA package
- **Feeds → linda-books** — every deduction tagged in books gets cross-marked here
- **Feeds → linda-bizops** — YTD deduction total appears on operator dashboard
- **Feeds ← linda-files** — receipts can be filed via filing cabinet too
- **Feeds → linda-cashops** — cash-out impact on operating outflows

## Error Handling

- **OCR can't read receipt:** Ask Boss for vendor + amount, save image anyway.
- **Meal without business purpose:** Stop and ask — IRS requires it. Log only after answer.
- **Personal expense slipped in:** Catch with category sanity check, ask before logging.
- **Mileage round-trip detected (same start/end + return):** Auto-double if Boss said "round trip".
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
