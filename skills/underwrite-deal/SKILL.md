---
name: underwrite-deal
description: This skill should be used when the user wants to underwrite an RV park (or mobile home park) deal end to end — "underwrite this deal", "run this deal", "analyze this RV park", "is this a good deal", "should I buy this park", "run the numbers and make me a report", or hands over a listing, T-12/P&L, offering memorandum, rent roll, or a deal walkthrough video. This is the master skill: it transcribes (if a video is given), extracts and normalizes the numbers, scores the deal, and produces a branded Wise Certified PDF + PowerPoint — the whole chain in one pass.
version: 1.0.0
min_tier: gold
---

# Underwrite This Deal  (master)

## Overview

The one-shot RV-park underwriting pipeline. Hand Linda a deal — a video, a P&L,
an OM, or just the numbers — and she runs the whole chain: transcribe → extract →
normalize the NOI → score GO / CONDITIONAL / NO-GO → build offer structures with
the Maximum Allowable Offer → deliver a branded Wise Certified PDF and slide deck.
Built on the LindaAI underwriting framework. Works for RV parks and mobile home
parks (same lot-rent math).

This skill orchestrates three component skills:
`youtube-transcribe` → `rv-park-autofill` → `deal-report`.

## When This Skill Applies

- "Underwrite this deal", "run this deal", "is this a good deal?", "should I buy this?"
- User shares a listing, T-12 / P&L, OM, rent roll, or a deal walkthrough video
- User wants the numbers run AND a shareable report in one go

## How It Works

### License Check

Verify the LindaAI license (`~/.claude/linda-license.json`) exactly as the other
LindaAI skills do: missing / expired / not `active` → stop with the matching
message; if an `api_url` is present, server-validate and POST a tamper alert on
`"valid": false`; unreachable → proceed. Otherwise proceed.

### Step 0 — Install deps

```bash
pip install -r requirements.txt   # openpyxl, reportlab, python-pptx, yt-dlp, faster-whisper
```

Ensure the template exists: `RV_Park_Underwriting.xlsx` at the repo root
(generate with `build_rv_underwriting.py` if missing).

### Step 1 — (Optional) Transcribe a walkthrough video

If the user gave a video link, run the `youtube-transcribe` skill (Whisper SOP)
to pull context. If the environment blocks YouTube (403), say so once and ask the
user to paste the transcript or the numbers — do not retry.

### Step 2 — Extract the deal into JSON

Read every document/number the user provided and fill out the schema in
`../rv-park-autofill/deal_input.example.json`. Follow the rv-park-autofill rules:
prefer the T-12 over the OM/Pro Forma; capture seller expenses **exactly as
stated** (don't pre-normalize — the pipeline does that); missing lines = `0`.
**Show the user the extracted numbers and let them correct anything before
running.** The human always makes the final call.

Save it as `deal.json`.

### Step 3 — Run the pipeline (one command)

```bash
python3 run_pipeline.py deal.json
# options: --template <path>  --out-dir <dir>  --logo <png>  --no-report
```

This fills + normalizes the workbook, then renders the branded PDF + PPTX. It
prints the deliverable paths and a summary (EGI, seller vs normalized NOI, ratios,
NOI haircut). Outputs land as `Wise Certified - <Name>.xlsx / .pdf / .pptx`.

### Step 4 — Present & deliver

Read the verdict to the user and deliver all three files with `SendUserFile`:

- **NOI haircut & overpayment risk** — flag loudly if the seller's expense ratio is
  under 30% (the numbers are likely inflated — "fiction").
- **Verdict** — GO / CONDITIONAL / NO-GO (DSCR ≥ 1.35 and Cash-on-Cash ≥ 10%).
- **Offer Structures** — the auto-solved MAO and which structures clear. If
  CONDITIONAL, walk Linda's 3 levers: lower price to the MAO, ask the seller to
  carry a slice, or add down payment.

Then offer to tweak any assumption and re-run — everything recalculates live.

## Notes

- Branding: outputs carry the Wise Certified Home Buyers logo when
  `../deal-report/assets/wise-certified-logo.png` exists (text wordmark otherwise).
- The pipeline runner is thin glue over the component skills — run any stage
  standalone if you only need part of the chain.
- This is a screening system, not investment advice. Verify every number against
  the T-12 and the property's condition.
