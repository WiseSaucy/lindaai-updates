---
name: rv-park-autofill
description: This skill should be used when the user wants to auto-fill the RV park underwriting workbook from a deal's documents — "underwrite this RV park", "run this T-12 / P&L", "analyze this offering memorandum", "fill the spreadsheet from this rent roll", "drop this deal into the model", "auto-fill the underwriting sheet", or any time they hand over a seller's financials (PDF, Excel, image, or pasted text) for an RV park or mobile home park and want the numbers loaded, normalized, and scored.
version: 1.0.0
min_tier: gold
---

# RV Park Auto-Fill

## Overview

Reads a seller's deal documents (T-12 / P&L / offering memorandum / rent roll),
extracts the numbers, and writes them into the RV park underwriting workbook —
**normalizing the NOI with Linda's rules along the way**. The seller's raw
figures land in the Normalization tab; the normalized figures drive the engine,
so the Deal Scorecard, NOI, and Offer Structures all reflect YOUR numbers, not
the seller's best case. Turns a folder of PDFs into a scored deal in minutes.

Works for RV parks and mobile home parks (same lot-rent math).

## When This Skill Applies

- User attaches/pastes a T-12, P&L, OM, or rent roll and says "underwrite this"
- "Run the numbers on this deal", "drop this into the model", "auto-fill the sheet"
- User wants the seller's financials normalized and scored without typing cells

## How It Works

### License Check

Before proceeding, verify the LindaAI license (read `~/.claude/linda-license.json`):
missing → stop and tell the user no license was found; past `expiration_date` →
stop (expired, renew); `status` not `"active"` → stop (state the status). If an
`api_url` field exists, WebFetch `{api_url}/v1/licenses/validate/{license_key}`:
`"valid": false` → stop (tamper) and POST a tamper alert; unreachable → proceed
(don't block paying customers); `"valid": true` → proceed. Otherwise proceed.

### Step 1 — Locate the template & install deps

The workbook template is `RV_Park_Underwriting.xlsx` (generate it with
`build_rv_underwriting.py` if it's not present). Then:

```bash
pip install -r requirements.txt   # openpyxl
```

### Step 2 — Extract the deal into JSON

Read every document the user provided and fill out the schema in
`deal_input.example.json`. Be rigorous and honest — this is the heart of the job:

- **Prefer the T-12** over the OM/Pro Forma. Linda: the OM is the seller's best case;
  the Pro Forma is fantasy; the T-12 is your real starting point. If both an OM and
  a T-12 are given and they disagree, use the T-12 and note the gap to the user.
- Capture **seller-reported expenses exactly as stated** (do NOT pre-normalize —
  the script does that). If a line is missing (common: management, capex, payroll),
  enter `0` — the normalization rules will backfill it.
- Pull `sites`, `asking_price`, annual site rent (gross potential), other income,
  and vacancy/occupancy. If only occupancy is given, vacancy = 1 − occupancy.
- Leave `normalization` at Linda's defaults (mgmt 10%, R&M 5%, capex 3%, tax +20%)
  unless the user specifies otherwise.

**Show the user the extracted numbers and let them correct anything before you
run it.** Linda's rule: the human always makes the final call.

### Step 3 — Fill the workbook

```bash
python3 fill_template.py deal.json --template RV_Park_Underwriting.xlsx --out "Deal - <Name>.xlsx"
```

The script writes basics/income/financing + normalized expenses to the
Underwriting tab, the seller's raw expenses to the Normalization tab, and seeds
the Offer Structures asking price. It prints a JSON summary (EGI, seller NOI,
normalized NOI, both expense ratios, NOI haircut) — relay the highlights.

### Step 4 — Review & report

Open the filled workbook and read the results to the user:

- **Normalization tab** — the NOI haircut and overpayment risk. Flag it loudly if
  the seller's expense ratio is **under 30%** (Linda: the numbers are "fiction").
- **Deal Scorecard** — the GOOD/OK/BAD ratings and the GO / CONDITIONAL / NO-GO verdict.
- **Offer Structures** — the auto-solved MAO and which of the conventional / partial-carry
  / full-carry structures clear. If CONDITIONAL, walk Linda's 3 levers (lower price to the
  MAO, ask for a seller carry, add down payment).

Deliver the filled `.xlsx` as the report. Offer to adjust any normalization
assumption and re-run — every metric recalculates live.

## Notes

- Formulas aren't evaluated by the fill script (openpyxl writes values, Excel
  computes). The printed NOI/ratio summary is computed independently for a sanity
  check; the workbook itself recalculates on open.
- If the script warns that a template label moved, the template was edited — verify
  the filled cells or regenerate the template before trusting the output.
- Pairs with the `youtube-transcribe` skill: transcribe a deal walkthrough, then
  auto-fill from the financials.
