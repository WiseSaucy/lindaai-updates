---
name: rv-park-underwriting
description: This skill should be used when the user asks to "underwrite an RV park", "RV park analysis", "RV park underwriting", "campground underwriting", "analyze an RV park deal", "is this RV park a good deal", "RV park cash flow", "RV park deal analysis", "RV park pro forma", "campground deal analysis", "underwrite a campground", "RV park cap rate", "RV park DSCR", "RV park NOI", "normalize RV park financials", "RV park T12 analysis", "RV park offer structure", "seller carry on an RV park", "maximum allowable offer RV park", "RV park stress test", "screen an RV park deal", "RV park 1% rule", "RV park GRM", "RV park expense ratio", "should I buy this RV park", "RV park value-add", "how much should I offer on this campground", "RV park underwriting spreadsheet", "build an RV park underwriting sheet", or any request involving evaluating, screening, normalizing, or structuring an offer on an RV park or campground investment.
version: 1.0.0
---

# RV Park / Campground Underwriting

## Overview

Full-stack underwriting for RV parks and campgrounds, built on a single one-page spreadsheet layout that holds the entire deal in one place — property info, the five key metrics, the seller's numbers, three structured offers side by side, screening hacks, adjustable levers, the full income and expense stack from the T12, NOI normalization, and a two-lien debt stack. LindaAI takes any RV park listing, OM, or P&L, rebuilds a realistic NOI, runs the five-second screening hacks, stress-tests the deal on a bad day, and produces three offers (conventional, partial seller carry, full seller carry) so you walk into any negotiation knowing exactly what to offer, how to structure it, and why. Every metric at the top recalculates the instant a lever changes, so you can stress test a deal in 30 seconds. The output answers: "Is this RV park a true money-maker, and what's the most I can pay and still hit my targets?"

## When This Skill Applies

- User provides an RV park or campground deal and asks "is this a good deal?"
- User gives an asking price, T12/P&L, or OM and wants it underwritten
- User wants to screen a campground listing fast (1% rule, 10x rule, expense ratio)
- User wants to normalize a seller's NOI / catch financial manipulation
- User asks for cap rate, DSCR, cash-on-cash, or NOI on an RV park
- User wants a maximum allowable offer (MAO) or an offer structure
- User asks about seller financing / seller carry to make a deal pencil
- User wants to stress-test an RV park deal
- User wants to find value-add upside on a campground
- User says "build me an RV park underwriting sheet" or "run the numbers on this park"

## How It Works

### License Check

Before proceeding, verify the LindaAI license:

1. Read `~/.claude/linda-license.json`
2. If the file does not exist, stop and tell the user:
   > 🤠 "Whoa there, partner — no LindaAI license found on this machine. You'll need a valid license to use LindaAI skills. Reach out to get set up and we'll have you in the saddle in no time."
   Do not proceed with any other steps.
3. If today's date is past the `expiration_date`, stop and tell the user:
   > 🤠 "Whoa there, partner — your LindaAI license expired on [expiration_date]. Reach out to renew and we'll get you back in the saddle." 🏇
   Do not proceed with any other steps.
4. If `status` is not `"active"`, stop and tell the user:
   > 🤠 "Whoa there, partner — your LindaAI license is currently [status]. Reach out to get this sorted and we'll have you riding again in no time."
   Do not proceed with any other steps.
5. **Server Verification (tamper check):** If the license file contains an `api_url` field, use WebFetch to check `{api_url}/v1/licenses/validate/{license_key}`. Parse the JSON response.
   - If the server responds with `"valid": false`, the local license has been tampered with. Stop and tell the user:
     > 🤠 "Hold up, partner — your license didn't check out with the server. Something's not matching up. Reach out to support to get this straightened out."
     Then use WebFetch to POST a tamper alert to `{api_url}/v1/licenses/tamper-alert` with JSON body: `{"license_key": "[key]", "local_expiration": "[local expiration_date]", "server_expiration": "[server expires from response]", "local_status": "[local status]", "details": "Local file passed but server validation failed"}`. Do not proceed.
   - If the server is unreachable or returns an error, proceed anyway (allow offline use — don't block paying customers because of a server hiccup).
   - If the server responds with `"valid": true`, proceed.
6. If all checks pass, proceed.

### The Spreadsheet Layout

LindaAI builds the deal on a single one-page underwriting sheet so the whole picture — property info, formulas, metrics, hacks, levers, and offers — is in front of you at once. The layout works identically in Excel or Google Sheets. Build it top to bottom, left to right, in this exact order:

**Column structure** — one column per scenario, same rows across all of them:

| Column | Scenario | What it holds |
|--------|----------|---------------|
| **A** | Line item labels | Section headers and row names |
| **B** | **Seller's numbers** | Exactly as presented in the OM/T12 — do not touch |
| **C** | **Offer 1 — Conventional** | Your offer with bank financing only (the MAO) |
| **D** | **Offer 2 — Partial Seller Carry** | Bank + partial seller carry |
| **E** | **Offer 3 — Full Seller Carry** | Seller as the bank (use when 1 & 2 don't work) |

Every metric at the top recalculates instantly off the levers, so changing one input restress-tests the entire deal.

### Section 1 — Property Information (top of sheet)

Capture the basics. Ask for anything missing:

| Field | Example placeholder |
|-------|---------------------|
| Park name / address | [Park Name, City ST] |
| Number of sites | [# of sites] |
| Site mix (RV / cabins / tent / storage) | [# RV / # cabins / # tent / # storage] |
| Occupancy (current) | [__%] |
| Avg site rate | [$__/night] or [$__/month] |
| Asking price | [$_________] |
| Year built / infrastructure age | [year / age] |
| Utilities (city vs. private septic/well) | [city / private — flag private septic or well as risk] |
| Amenities (laundry, store, etc.) | [list amenities] |

### Section 2 — Five Key Metrics (at a glance, top of sheet)

These five sit right under the property info and recalc off everything below. Show them for every column (seller vs. each offer):

| Metric | Formula | Target / Read |
|--------|---------|---------------|
| **NOI** | EGI − operating expenses (no debt service) | The heartbeat — if NOI is wrong, everything is wrong |
| **Cap Rate** | NOI ÷ purchase price | Buy high, sell low; tied to risk |
| **DSCR** | NOI ÷ annual total debt service | **≥ 1.35** minimum (lender floor, not comfort) |
| **Net Profit** | NOI − all loan payments | What you actually pocket |
| **Cash-on-Cash Return** | Net profit ÷ down payment (cash invested) | **≥ 10%** target (or beat your cost of capital) |

**Metric definitions (build the formulas from these):**
- **GPI (Gross Potential Income):** sites × rate × full occupancy — the theoretical max nobody hits.
- **EGI (Effective Gross Income):** GPI − vacancy + other income (laundry, storage, store). The real top line. *In this sheet, "gross income" = EGI.*
- **NOI:** EGI − operating expenses. Operating expenses do **not** include debt service, depreciation, sales tax, or the owner's personal expenses.
- **DSCR** is calculated on **total** debt service (both liens), not just one loan — that's the number lenders care about.

### Section 3 — Quick Hacks (reference block)

Keep these on the sheet for fast screening — they tell you in under two minutes whether a deal is worth a real look. All five run off the seller's numbers straight from the listing/OM:

| Hack | Formula | Read |
|------|---------|------|
| **1% Rule** | Monthly gross income ÷ price ≥ 1% (cross off the last two zeros of the price) | Pass = likely a good deal. Works only in a 5–12% rate environment. |
| **10x Rule (GRM)** | Price ÷ annual gross income; want **< 10** (add a zero to annual gross — if price is higher, it's pricey) | Tells you if it's overpriced |
| **DSCR Estimate** | NOI ÷ (price × interest rate) | ≥1.5 breathing room; 1.25–1.5 closer look; <1.25 lending risk |
| **Expense Ratio Flag** | Operating expenses ÷ gross income | **<30% = something's missing** (mgmt/capex/R&M cut — NOI is fiction); 35–65% normal; >70% mismanagement or value-add opportunity |
| **Cap vs. Rate (Negative Leverage)** | Compare cap rate to loan interest rate | Cap < rate = losing money day one (negative leverage); cap > rate = positive leverage / your cushion |

### Section 4 — Levers (the adjustable inputs)

These are the knobs. Change one and every metric at the top recalculates instantly:

| Lever | Notes |
|-------|-------|
| **Purchase price** | Ratchet down to find the MAO |
| **Down payment** | Higher down → DSCR up, cash-on-cash down |
| **LTV** | Loan-to-value |
| **Interest rate (1st loan)** | Bank rate |
| **Amortization** | Years |
| **Seller carry %** | Portion seller finances |
| **Seller carry interest rate** | Usually below market |

### Section 5 — Income (broken out the way RV parks actually earn)

| Income Line | Seller (B) | Offer 1 (C) | Offer 2 (D) | Offer 3 (E) |
|-------------|------------|-------------|-------------|-------------|
| Site rent | | | | |
| Utility bill-back | | | | |
| Storage | | | | |
| Other income (laundry, store, etc.) | | | | |
| **Gross Potential Income (GPI)** | | | | |
| − Vacancy | | | | |
| **= Effective Gross Income (EGI)** | | | | |

### Section 6 — Operating Expenses (every line from the T12)

Pull each line straight from the T12. When the user attaches the T12/P&L, LindaAI reads the line items and fills these in automatically — no manual re-entry.

| Expense Line | Seller (B) | Offer 1 (C) | Offer 2 (D) | Offer 3 (E) |
|--------------|------------|-------------|-------------|-------------|
| Management | | | | |
| Payroll | | | | |
| Repairs & Maintenance | | | | |
| Utilities | | | | |
| Insurance | | | | |
| Property Taxes | | | | |
| CapEx | | | | |
| Other (admin, marketing, etc.) | | | | |
| **Total Operating Expenses** | | | | |
| **Expense Ratio** | | | | |

### Section 7 — NOI Normalization (rebuild the seller's NOI)

The seller's NOI is almost always optimistic — sometimes by 50%. Owner-operators leave out management, defer maintenance before listing, never book capex, and understate taxes. Your job is to rebuild the NOI to what it would cost **you** to run it. Run these four substitutions on every deal:

| Adjustment | Normalize To | Why |
|------------|--------------|-----|
| **Management fee** | **10% of income** | Owner self-managed; the day you close, you pay a manager |
| **Repairs & Maintenance** | Prior-year number **or 5% of gross** | Pre-sale deferred maintenance makes R&M look artificially low |
| **CapEx** | **~3% of income** | Never on owner financials, but septic/AC/roof costs are coming |
| **Property Taxes** | Increase for reassessment (e.g. **+20%**) | Often understated; many counties reassess at the purchase price |

Show the **normalized NOI** alongside the seller's NOI and quantify the gap. Translate that gap into overpayment risk at the deal's cap rate — i.e. `NOI cut ÷ cap rate = $ overpayment risk` — so the user sees what an inflated NOI would have cost them.

### Section 8 — Debt Stack (models both liens)

| Item | Inputs | Notes |
|------|--------|-------|
| **1st Loan** | Principal, interest rate, amortization; P&I **or** interest-only | Bank financing |
| **2nd Loan (Seller Carry)** | Principal, interest rate, amortization; P&I **or** interest-only | Seller financing |
| **Total Annual Debt Service** | 1st + 2nd | DSCR is calculated off **this** total, not one loan |
| **Cost of Capital (optional)** | If borrowing the down payment | Adds to debt service and lowers DSCR accordingly |

### Section 9 — The Bad Day Test (stress test)

Deals don't fall apart on good days. Before making an offer, break it on purpose:

1. **Cut occupancy 10–15%** → watch DSCR. A park that still pencils at a lower occupancy survives a slow season; one that only works at near-full occupancy is one bad summer from out-of-pocket.
2. **Add 1–2% to interest rate** → critical for ARMs or a balloon/refi in 3 years.
3. **Raise expenses 10–15%** → insurance and R&M creep up every year.

### Section 10 — The Two-Question Go/No-Go

After normalizing, two metrics must clear **at the same time**:

1. **DSCR ≥ 1.35** (normalized NOI ÷ annual debt service) — your floor, not the lender's.
2. **Cash-on-Cash ≥ 10%** (net profit ÷ down payment) — or whatever your target is.

- Both clear → **GO**
- One fails → **ON THE FENCE** (restructure — see offers)
- Both fail → **likely NO-GO** (but try the three offer structures first)

### Section 11 — The Three Offers (Columns C, D, E)

A conditional deal isn't dead — it's a restructure. You have three levers: lower price, seller financing, more down payment. Build all three offers side by side:

| Offer | Structure | When to use |
|-------|-----------|-------------|
| **Offer 1 — Conventional (Col C)** | Ratchet price down until DSCR & CoC clear with bank financing (25–30% down). This is the **Maximum Allowable Offer (MAO)**. | Default. Seller may balk if it's far below ask. |
| **Offer 2 — Partial Seller Carry (Col D)** | Bank covers [__%] @ [__%] + seller carries [__%] @ [__%] → blended rate drops below market, DSCR clears, CoC jumps. | Fails bank-only but seller is motivated (e.g. wants monthly income). |
| **Offer 3 — Full Seller Carry (Col E)** | Seller is the bank; negotiate rate and interest-only terms. No bank, no appraisal risk; max DSCR & CoC. | Seller wants full price but will work on terms; needs steady income or wants to defer cap gains. |

If none work and the seller won't budge, the underwriting just saved you from an expensive mistake.

### Section 12 — Value-Add / Upside (don't pay for it)

List the upside separately — it's your return and your exit, not the seller's. Don't pay the seller for value you intend to create.

| Lever | How to value it |
|-------|-----------------|
| **Rate increases to market** | `# sites × $/site/mo below market × 12 ÷ cap rate = $ of created value` |
| **Occupancy improvement** | Closing an occupancy gap is usually a management problem, not a real-estate one |
| **Expense reduction** | Convert owner-paid utilities to ratio/bill-back — moves cost to guests |
| **Additional revenue** | Laundry, self-storage, covered parking, camp store |

## Output Format

Reproduce the sheet as a markdown table (Seller vs. the three offers), then summarize. Structure:

```markdown
# RV Park Underwriting: {Park Name}
**Date:** {date} · **Analyzed by:** LindaAI 🤠

## Property Snapshot
{sites, mix, occupancy, rate, asking price, utilities, infrastructure}

## Five Key Metrics
| Metric | Seller | Offer 1 (Conv) | Offer 2 (Partial Carry) | Offer 3 (Full Carry) |
|--------|--------|----------------|--------------------------|----------------------|
| NOI | | | | |
| Cap Rate | | | | |
| DSCR | | | | |
| Net Profit | | | | |
| Cash-on-Cash | | | | |

## Quick Hacks (Seller's Numbers)
{1% rule · 10x/GRM · DSCR estimate · expense ratio flag · cap vs. rate}

## Income & Expenses (Seller vs. Normalized)
{full income + expense stack, normalized NOI, NOI gap / overpayment risk}

## Levers & Debt Stack
{purchase price, down, LTV, rates, amort, seller carry; both liens + total debt service}

## Bad Day Test
{occupancy −10–15%, rate +1–2%, expenses +10–15% → DSCR/CoC under stress}

## The Three Offers
{Offer 1 MAO · Offer 2 partial carry · Offer 3 full carry — price + structure each}

## Value-Add Upside
{rate-to-market, occupancy, expense reduction, added revenue — kept separate}

## Recommendation
**Verdict: [GO / CONDITIONAL GO / NO-GO]**
{top reasons, biggest red flags (e.g. expense ratio <30%, high occupancy, private septic),
 which offer to lead with, and what terms make it work}
```

### Step — Save & Present

Save the full underwriting package to `brain/research/rv-park-underwriting-[park-name]-[date].md`.

Present in chat:
1. Executive summary (is it a money-maker, and the most you should pay)
2. Five key metrics (seller vs. normalized/offers)
3. The three offers with price and structure
4. Top red flags and value-add upside
5. GO / CONDITIONAL GO / NO-GO with the lead offer

Tell the user: "The full sheet — seller numbers, normalized NOI, three offers, debt stack, and the bad-day test — is corralled and saved to brain/research/. LindaAI ran every number; now it's your call, partner."

## Error Handling

- **No asking price:** Ask — "What's the asking price? I need it to run the hacks and the offers."
- **No T12 / P&L:** Run the screening hacks off the listing's gross income, flag that the NOI is unverified, and ask for the T12 before producing offers.
- **Expense ratio under 30%:** Do not trust the NOI. Flag it loudly, normalize (management, R&M, capex, taxes), and show the corrected NOI and the overpayment risk.
- **Seller carry terms unknown:** Ask whether the seller will carry and at what rate/term before building Offers 2 and 3; otherwise model reasonable assumptions and label them.
- **Cap rate below interest rate:** Flag negative leverage explicitly — "You'd be losing money from day one at this price/financing."
- **Unusually high cap rate:** Ask why nobody else bought it — dig for deferred maintenance, aging infrastructure, or priced-in problems.

## Example Usage

**User:** "Underwrite this RV park: [# sites], [$__/night], [__%] occupancy, asking [$____]. Seller says NOI is [$____]. Here's the T12 [attached]."

**LindaAI:** Drops the seller's numbers in Column B, runs the five hacks (1% rule, 10x/GRM, DSCR estimate, expense ratio flag, cap vs. rate — flagging any expense ratio under 30%), normalizes the NOI (adds 10% management, 5% R&M, 3% capex, +20% taxes), rebuilds the five metrics, stress-tests occupancy/rate/expenses, then produces Offer 1 (the conventional MAO), Offer 2 (partial seller carry), and Offer 3 (full carry) — and recommends which offer to lead with based on which structure clears the 1.35 DSCR and the cash-on-cash target.

**Disclaimer:**
> "This RV park underwriting is based on the documents and assumptions provided and standard normalization. Verify the T12, utilities (septic/well), occupancy, and tax reassessment independently before proceeding. This is not legal or financial advice."

🤠 *Generated by LindaAI* 🏇


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
