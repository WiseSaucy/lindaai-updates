---
name: deal-analyzer
description: This skill should be used when the user asks to "analyze a deal", "run the numbers", "underwrite a property", "is this a good deal", "evaluate this investment", "what's the cash flow", "calculate cap rate", "what's the cash-on-cash return", "DSCR on this deal", "should I buy this property", "deal analysis", "run deal numbers", "break down this deal", "compare financing options", "creative finance analysis", "subject-to analysis", "seller finance deal", "hard money deal analysis", "BRRRR numbers", "rental property analysis", "multi-family underwriting", "commercial deal analysis", or any request involving evaluating whether a real estate deal makes financial sense.
version: 1.0.0
---

# Deal Analyzer

## Overview

Analyzes any real estate deal — residential, multi-family, or commercial — and delivers a comprehensive financial breakdown with a clear go/no-go recommendation. The user provides property details, purchase price, estimated rents, and financing terms. LindaAI runs the numbers on every metric that matters: cash-on-cash return, cap rate, DSCR, monthly cash flow, ROI, break-even occupancy, and more. Supports multiple financing scenarios side by side (conventional, FHA, hard money, creative finance, subject-to, seller finance). Uses web search to pull comparable sales and rental data when an address is provided.

## When This Skill Applies

- User provides a property address and asks "is this a good deal?"
- User gives purchase price, rents, and financing terms and wants analysis
- User asks to compare conventional vs. creative financing on a deal
- User wants to know cash flow, cap rate, or cash-on-cash return
- User says "run the numbers on this"
- User asks "should I buy this property?"
- User wants to underwrite a multi-family or commercial property
- User provides a deal and wants a go/no-go recommendation
- User mentions subject-to, seller finance, or wrap mortgage analysis
- User asks about DSCR, break-even, or debt coverage on a deal

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

### Step 0: Gather Deal Inputs

Parse what the user provided. Required inputs (ask for anything missing):

| Input | Required | Example |
|-------|----------|---------|
| Property address or description | Yes | "123 Main St, Dallas TX" or "3/2 SFR in Dallas" |
| Purchase price | Yes | $150,000 |
| Estimated monthly rent (gross) | Yes | $1,800/mo |
| Financing type | Yes | Conventional, FHA, hard money, seller finance, subject-to, cash |
| Down payment or cash to close | Yes (unless cash) | 20% or $30,000 |
| Interest rate | Yes (unless cash) | 7.5% |
| Loan term | Yes (unless cash) | 30 years |
| Estimated rehab cost | If applicable | $25,000 |
| After-repair value (ARV) | If applicable | $200,000 |

If the user provides an address but not comps/rents, use WebSearch to find estimated values.

### Step 1: Research (if address provided)

> 🤠 "Hold tight — heading over yonder to gather up the details."

Use WebSearch to pull:
- Recent comparable sales in the area (within 0.5 mi, last 6 months)
- Current rental listings for similar properties
- Property tax estimates for the area
- Insurance cost estimates
- Any active listings or recent sale history for the subject property

Search queries to run:
- `"{address}" property records sale price`
- `"homes sold near {address}" {year}`
- `"{city} {state} {bedrooms} bedroom rental rates"`
- `"{zip code} property tax rate"`
- `"{city} {state} landlord insurance cost"`

### Step 2: Set Expense Assumptions

Use researched data or these conservative defaults:

| Expense | Default | Notes |
|---------|---------|-------|
| Property taxes | 1.2% of purchase price/yr | Adjust by state/county from research |
| Insurance | 0.5% of purchase price/yr | Adjust for flood zone, state, property type |
| Vacancy | 8% of gross rent | 5% in hot markets, 10%+ in soft markets |
| Maintenance/repairs | 10% of gross rent | Higher for older properties |
| CapEx reserves | 5% of gross rent | Roof, HVAC, water heater fund |
| Property management | 10% of gross rent | Even if self-managing, include for scalability |
| HOA | $0 unless specified | Ask if condo/townhouse |

### Step 3: Calculate Core Metrics

**Gross Rent Multiplier (GRM)**
```
GRM = Purchase Price / (Monthly Rent x 12)
```
- Below 8 = Strong buy signal
- 8-12 = Market dependent
- Above 12 = Weak or appreciation play

**1% Rule Check**
```
Monthly Rent / Purchase Price >= 1%
```
- Meets 1% = Cash flow likely positive
- Below 1% = Tighter margins, scrutinize expenses

**Net Operating Income (NOI)**
```
NOI = Gross Annual Rent - Vacancy - Operating Expenses (no debt service)
```

**Cap Rate**
```
Cap Rate = NOI / Purchase Price x 100
```
- 4-6% = A/B class, appreciation markets
- 6-8% = Solid cash flow markets
- 8%+ = High cash flow, possibly higher risk

**Debt Service (Monthly P&I)**
Calculate using standard amortization formula:
```
M = P[r(1+r)^n] / [(1+r)^n - 1]
Where:
  P = loan amount
  r = monthly interest rate
  n = total number of payments
```

**Monthly Cash Flow**
```
Cash Flow = (Monthly Rent - Vacancy Allowance - Monthly Expenses - Monthly Debt Service)
```

**Annual Cash Flow**
```
Annual Cash Flow = Monthly Cash Flow x 12
```

**Cash-on-Cash Return (CoC)**
```
CoC = Annual Cash Flow / Total Cash Invested x 100
Total Cash Invested = Down Payment + Closing Costs + Rehab (if any)
```
- Below 5% = Weak return for effort
- 5-8% = Acceptable depending on appreciation
- 8-12% = Good deal
- 12%+ = Strong deal

**DSCR (Debt Service Coverage Ratio)**
```
DSCR = NOI / Annual Debt Service
```
- Below 1.0 = Negative cash flow (deal loses money)
- 1.0-1.2 = Tight, risky
- 1.2-1.5 = Healthy
- 1.5+ = Strong

**Break-Even Occupancy**
```
Break-Even = (Operating Expenses + Debt Service) / Gross Potential Rent x 100
```
- Below 75% = Very safe
- 75-85% = Acceptable
- Above 85% = Tight, little room for vacancies

**Total ROI (Year 1)**
```
ROI = (Cash Flow + Principal Paydown + Appreciation) / Total Cash Invested
```
- Estimate appreciation at 3% unless market data suggests otherwise
- Include principal paydown from amortization schedule

### Step 4: Run Multiple Financing Scenarios (if requested)

Create a comparison table with the same property under different financing:

| Metric | Conventional 20% | FHA 3.5% | Seller Finance | Subject-To | Cash |
|--------|------------------|-----------|----------------|------------|------|
| Cash to close | | | | | |
| Monthly payment | | | | | |
| Monthly cash flow | | | | | |
| Cash-on-cash | | | | | |
| DSCR | | | | | |

For creative finance scenarios:
- **Subject-To:** Use existing mortgage terms (lower rate = advantage). Cash to close = purchase price minus existing loan balance.
- **Seller Finance:** User-defined terms. Often interest-only or balloon. Calculate both P&I and interest-only cash flows.
- **Hard Money:** Short-term (6-18 months). Higher rates (10-14%). Include points as upfront cost. This is a bridge, not a hold strategy.
- **Wrap Mortgage:** Underlying loan + seller's spread. Show all-in effective rate.

### Step 5: Generate Go/No-Go Recommendation

Apply this decision matrix:

| Signal | Green (Go) | Yellow (Caution) | Red (No-Go) |
|--------|-----------|-------------------|-------------|
| Cash-on-Cash | 8%+ | 5-8% | Below 5% |
| Monthly Cash Flow | $200+/door | $100-200/door | Below $100/door |
| Cap Rate | 7%+ | 5-7% | Below 5% |
| DSCR | 1.25+ | 1.0-1.25 | Below 1.0 |
| 1% Rule | Meets or exceeds | Within 0.1% | Far below |
| Break-Even | Below 75% | 75-85% | Above 85% |

**Scoring:**
- 5-6 Green = STRONG BUY
- 3-4 Green, rest Yellow = GOOD DEAL with noted risks
- Mix of Green/Yellow/Red = PROCEED WITH CAUTION (specify what needs to change)
- 2+ Red = PASS (explain why and what price/terms would make it work)

Always include: "What would make this deal work" — the purchase price, rent, or terms needed to hit target returns.

### Step 6: Save Analysis

Save the complete analysis to a markdown file:
```
~/Desktop/lindaai/output/deal-analyses/{address-slug}-{date}.md
```

## Output Format

```markdown
# Deal Analysis: {Address}
**Date:** {date}
**Analyzed by:** LindaAI 🤠

---

## Property Overview
| Detail | Value |
|--------|-------|
| Address | |
| Property Type | |
| Beds/Baths | |
| Year Built | |
| Square Footage | |
| Purchase Price | |
| Estimated ARV | |

## Financing Terms
| Term | Value |
|------|-------|
| Financing Type | |
| Down Payment | |
| Loan Amount | |
| Interest Rate | |
| Loan Term | |
| Monthly P&I | |
| Total Cash to Close | |

## Income & Expenses (Monthly)
| Item | Amount |
|------|--------|
| Gross Rent | |
| - Vacancy (X%) | |
| - Property Tax | |
| - Insurance | |
| - Maintenance | |
| - CapEx Reserve | |
| - Property Management | |
| - HOA | |
| **= Net Operating Income** | |
| - Debt Service | |
| **= Monthly Cash Flow** | |

## Key Metrics
| Metric | Value | Rating |
|--------|-------|--------|
| Monthly Cash Flow | | |
| Annual Cash Flow | | |
| Cash-on-Cash Return | | |
| Cap Rate | | |
| DSCR | | |
| GRM | | |
| 1% Rule | | |
| Break-Even Occupancy | | |
| Year 1 Total ROI | | |

## Recommendation
**Verdict: [STRONG BUY / GOOD DEAL / PROCEED WITH CAUTION / PASS]**

[Explanation with specific reasoning]

### What Would Make This Deal Work
[If not a strong buy, specify the price, rent, or terms that would get it there]

## Comparable Data (from research)
[Comps found via web search, if any]

---
🤠 *Generated by LindaAI* 🏇
```

## Example Usage

**User:** "Analyze this deal: 3/2 SFR at 4521 Elm Street, Dallas TX 75216. Purchase price $165,000. Rents should be around $1,650/mo. I'm looking at conventional financing with 20% down at 7.25% for 30 years."

**LindaAI runs the numbers:**
- Down payment: $33,000
- Loan: $132,000 at 7.25% / 30yr = $900.72/mo P&I
- Taxes: $165,000 x 1.8% (Texas) / 12 = $247.50/mo
- Insurance: $165,000 x 0.5% / 12 = $68.75/mo
- Vacancy: $1,650 x 8% = $132/mo
- Maintenance: $1,650 x 10% = $165/mo
- CapEx: $1,650 x 5% = $82.50/mo
- Management: $1,650 x 10% = $165/mo
- Total expenses: $1,761.47/mo
- Cash flow: $1,650 - $1,761.47 = **-$111.47/mo** (negative)
- Cash-on-cash: Negative
- Verdict: **PASS at this price. Deal works at $135,000 or rents of $1,900+.**

**User:** "Now show me what it looks like with seller finance at 0% down, 5% interest, 30 year amortization with a 5-year balloon."

**AI recalculates with new terms and compares side by side.**

## Error Handling

- **If the user does not provide a purchase price:** Ask specifically: "What is the purchase price (or asking price)? I need this to run the numbers."
- **If the user does not provide estimated rents:** Attempt to research rents via WebSearch using the address or area. If research fails, ask: "I couldn't find rental data for this area. What do you estimate the monthly rent to be?"
- **If the user does not provide financing terms:** Ask: "How are you financing this? I need: financing type (conventional, FHA, hard money, seller finance, subject-to, cash), down payment, interest rate, and loan term."
- **If WebSearch is unavailable for comp/rent research:** Proceed with user-provided data only and note: "Web search is unavailable. The analysis uses only the data you provided. Comps and market data are not included — consider verifying rent and value estimates independently."
- **If WebSearch returns no comparable sales or rental data for the area:** Note: "I could not find recent comps or rental data for this specific area via web search. The analysis uses your provided estimates. I recommend verifying with a local realtor or property manager."
- **If the deal produces negative cash flow:** Do not just say "pass." Calculate and show: "This deal loses ${X}/month at these terms. To break even, you would need: rent of ${Y}/mo, OR purchase price of ${Z}, OR interest rate of {W}%. Here is what each scenario looks like."
- **If the user provides incomplete expense data:** Use the conservative defaults listed in Step 2. Note which assumptions were used: "I used default expense assumptions for: {list}. Adjust these if you have actual numbers."
- **If the output directory does not exist:** Create `~/Desktop/lindaai/output/deal-analyses/` automatically before saving.
- **If the user provides a subject-to deal but does not know the existing loan terms:** Flag: "For a subject-to analysis, I need the existing loan balance, interest rate, monthly payment, and remaining term. Can you find these from the seller or title company?"
- **If calculations produce unusual results (e.g., 500% cash-on-cash, or negative cap rate):** Double-check the inputs and flag: "These numbers seem unusual — {metric} is {value}. Double-check that the inputs are correct: {list key inputs}."


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
