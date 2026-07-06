---
name: linda-taxprep
description: This skill should be used when the user asks to "prep my taxes", "tax prep package", "year-end tax package", "build my CPA package", "tax season prep", "aggregate 1099s", "compile W-2s", "Schedule C income", "depreciation schedule", "mileage log for taxes", "year-end tax summary", "tax-ready report", "send to my CPA", or any request involving year-end tax preparation, CPA hand-off package generation, or aggregating tax documents.
tags: [operator, taxes, year-end, cpa, schedule-c, 1099, depreciation]
version: 1.0.0
---

# Linda TaxPrep — Year-End CPA Package

## Overview

Tax season ain't a panic season when Linda's runnin' the books. Linda TaxPrep aggregates a full year of categorized transactions (from `linda-books`), 1099-NECs received and issued (from `linda-payroll`), W-2 data, mileage logs (from `linda-deductions`), depreciation schedules for fixed assets, home office allocation, and entity ownership info — then produces a single CPA-ready PDF package the operator hands to their accountant. No more Drive folder of "stuff" — one clean package, indexed, totals-tied, and footnoted.

## When This Skill Applies

- "Build my year-end tax package for 2025"
- "Aggregate my 1099s and Schedule C income"
- "Generate my depreciation schedule"
- "I need a CPA-ready package"
- "Tax season prep for [Your Business]"

## How It Works

### Step 0: License Check
Standard LindaAI license verification. Halt with country howdy on failure.

### Step 1: Confirm Entity & Year

Inputs:
| Field | Notes |
|-------|-------|
| Entity legal name | Pull from `brain/operator/compliance/{entity}/profile.md` |
| EIN | Same |
| Tax year | Default = prior calendar year |
| Filing form | 1040 Sch C / 1065 / 1120-S / 1120 |
| State | For state-level summary |
| Owner / member info | Names, % ownership, SSN/EIN last 4 |

### Step 2: Pull the Year's Books

Read all monthly ledgers from `brain/operator/books/{entity}/transactions-{YYYY-MM}.csv` for the tax year. Roll up by IRS category:
- **Gross Receipts** (Sch C Line 1)
- **Returns & Allowances** (Line 2)
- **Cost of Goods Sold** (Part III)
- **Expense lines** mapped to Sch C Part II (Lines 8-27): Advertising, Car/Truck, Commissions, Contract Labor, Depletion, Depreciation, Employee Benefits, Insurance, Interest (mortgage / other), Legal & Professional, Office, Pension, Rent (vehicles / other), Repairs, Supplies, Taxes & Licenses, Travel, Meals (50%), Utilities, Wages, Other

### Step 3: 1099 & W-2 Aggregation

Pull from `linda-payroll`:
- 1099-NEC issued list (every contractor paid > $600)
- 1099-NEC received list (income reported by clients)
- W-2 wages issued (if entity runs payroll)
- 1099-K from Stripe / payment processors
- 1099-INT from bank

Reconcile total 1099 income reported vs entity gross receipts — flag deltas.

### Step 4: Mileage & Vehicle

Pull from `linda-deductions`:
- Total business miles for the year
- Personal miles (for mixed-use vehicles)
- Standard mileage deduction calc (IRS rate × business miles)
- Actual expense alternative if records support it
- Vehicle on the books with depreciation? — pull depreciation schedule

### Step 5: Depreciation Schedule

For every fixed asset:
| Asset | Date Placed | Cost Basis | Method | Life | Prior Depreciation | Current Year | Accumulated | Book Value |

Methods supported: MACRS 5-yr (vehicles, computers), 7-yr (office furniture), 27.5-yr (residential rental), 39-yr (commercial), Section 179 expense, Bonus depreciation per current rules.

### Step 6: Home Office (if applicable)

If Sch C with home office:
- Square footage of dedicated space / total home sqft
- Total home expenses (rent or mortgage interest, utilities, insurance, repairs)
- Allocated portion to business
- Simplified method alternative ($5/sqft up to 300 sqft cap) — show both, recommend the better one

### Step 7: Build the CPA Package PDF

Sections:
1. Cover page — entity, EIN, tax year, package generation date, owner info
2. Executive summary — top-line numbers (revenue, expenses, net, taxable income before deductions)
3. Profit & Loss for the year
4. Balance Sheet at year-end
5. Schedule C / K-1 mapping table (Linda's category → IRS line number)
6. 1099-NEC issued list
7. 1099-NEC / 1099-K received list
8. Mileage log summary
9. Depreciation schedule
10. Home office worksheet (if applicable)
11. Estimated tax payment log (4 quarters)
12. Open questions for CPA (Linda's flags)

### Step 8: Save & Hand Off

- Master PDF: `brain/operator/taxes/{entity}/{YYYY}-cpa-package.pdf`
- Backup MD: `brain/operator/taxes/{entity}/{YYYY}-cpa-package.md`
- Supporting CSVs: `brain/operator/taxes/{entity}/{YYYY}/`
  - `1099-issued.csv`, `1099-received.csv`, `mileage-log.csv`, `depreciation.csv`, `pnl.csv`, `balance.csv`

If Boss says "send it to my CPA," hand off to `linda-mail` with the package attached.

## Inputs

- Entity name + EIN + tax year
- Filing form type
- Owner / member info
- (Optional) home office sqft
- (Optional) vehicle business-use percent

## Outputs

- One master CPA-package PDF (40-80 pages)
- Supporting CSVs (1099s, mileage, depreciation, statements)
- Open-questions worksheet for CPA review

## Example Usage

**User:** "Boss — build my 2025 tax package for [Your Business LLC]. Filing 1065."

**LindaAI:** "Let's gooooooo Boss!" Pulls 12 months of books, 7 contractor 1099-NECs, mileage (4,820 business miles), 3 fixed assets on depreciation schedule, generates 62-page CPA package. "Yeeee Hawww 🤠 — package ready at `brain/operator/taxes/your-business/2025-cpa-package.pdf`. Net income $87,420. 4 questions flagged for your CPA — review page 51."

**User:** "Get my Schedule C ready for personal taxes."

**LindaAI:** Runs the same flow but maps to Sch C lines instead of K-1.

## Voice & Tone

- Country, direct. **Boss.**
- "Let's gooooooo!" on kickoff. "Yeeee Hawww 🤠" when package is locked.
- Encouraging on tax stress: "We got it Boss. Books are clean. CPA's gonna love this."

## Brand Rules (PDFs)

- LindaAI logo top-right
- {customer_handle} bottom-right
- © 2024–2026 LindaAI · Built by Daniel Wise footer
- Disclaimer page: *"This package is a recordkeeping summary, not a tax return or tax advice. Always review with a licensed CPA or tax professional."*

## Cross-Skill Hooks

- **Feeds ← linda-books** — entire year's categorized ledger
- **Feeds ← linda-payroll** — 1099-NEC issued list
- **Feeds ← linda-deductions** — mileage log + categorized deductions
- **Feeds ← linda-files** — pulls scanned tax docs (W-2s, 1099s received) from filing cabinet
- **Feeds → linda-mail** — sends package to CPA on command
- **Feeds → linda-bizops** — tax-readiness status on dashboard

## Error Handling

- **Books not closed for year:** Stop and run `linda-books` Q4 close first.
- **1099-NEC reported income > books gross receipts:** Flag — likely missing income on books.
- **Depreciation conflicts:** If asset method changed mid-year, ask Boss to confirm with prior CPA.
- **Missing entity profile:** Ask once, save to `brain/operator/compliance/{entity}/profile.md`.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
