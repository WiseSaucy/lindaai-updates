---
name: deal-report
description: Background engine for /rv-park-underwriting — it runs this automatically when a report is wanted; the user does not call it directly. Turns a filled RV park workbook into a branded PDF + PowerPoint. Only invoke on its own if the user EXPLICITLY asks for ONLY the report off an already-filled workbook — e.g. "just make the PDF from this workbook", "rebuild the slide deck". Normal "underwrite this park and give me a report" requests go to /rv-park-underwriting.
version: 1.0.0
min_tier: gold
---
> ⚙️🤠 **Engine part of `/rv-park-underwriting` — works in the background.** The underwriting skill calls this to print your branded one-pager + deck. Documented here only for a standalone report off an existing workbook.

# Deal Report

## Overview

Turns a filled `RV_Park_Underwriting.xlsx` into a **branded one-page PDF** and a
**PowerPoint deck** in Linda's report style: 5 key metrics, property snapshot,
normalized-vs-seller NOI, the offer comparison with the MAO, red flags, and
value-add upside. The report engine **recomputes every metric in Python** (Excel
formulas aren't evaluated by the reader), so the output is correct without opening
Excel. Auto-brands with the Wise Certified Home Buyers logo when present.

## When This Skill Applies

- "Make the PDF / one-pager / report / investor packet for this deal"
- "Build the PowerPoint", "export this deal", "something I can hand a partner"
- After `rv-park-autofill` fills a deal — the natural next step

## How It Works

### License Check

Verify the LindaAI license (`~/.claude/linda-license.json`) exactly as the other
LindaAI skills do: missing / expired / not `active` → stop with the matching
message; if an `api_url` is present, server-validate and POST a tamper alert on
`"valid": false`; unreachable → proceed. Otherwise proceed.

### Step 1 — Install deps

```bash
pip install -r requirements.txt   # openpyxl, reportlab, python-pptx
```

### Step 2 — Brand it (logo)

Place the logo at `assets/wise-certified-logo.png` (transparent PNG preferred).
It's auto-embedded in the PDF header and on the title slide. Without it, a clean
"WISE CERTIFIED · HOME BUYERS" wordmark is used. Override with `--logo /path.png`.

### Step 3 — Generate

```bash
python3 make_report.py "Deal - <Name>.xlsx" --pdf --pptx --out "Wise Certified - <Name>"
# --pdf only / --pptx only also work; with neither flag it makes both.
```

It prints the output paths and a one-line verdict/metrics summary. Deliver the
files to the user with `SendUserFile`.

### Step 4 — Sanity check

The printed summary (Verdict · NOI · Cap · DSCR · CoC) should match the workbook's
Deal Scorecard. If they differ, the workbook inputs changed — regenerate. Render a
page to an image to eyeball layout if a deal has unusually long names/locations.

## Notes

- One page by design (PDF). Content scales to whichever tabs exist in the workbook
  (Normalization and Offer Structures sections are included only if those tabs are present).
- Brand color is Wise Certified royal blue (#1D3FAE). Verdict badges are color-coded
  GO / CONDITIONAL / NO-GO.
- Pairs with `rv-park-autofill` (fill from a P&L) and `youtube-transcribe`
  (mine a deal walkthrough) for a full intake-to-report pipeline.
