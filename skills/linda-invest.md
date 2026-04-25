---
name: linda-invest
description: This skill should be used when the user asks to "calculate investment returns", "BRRRR analysis", "BRRRR calculator", "flip analysis", "flip profit calculator", "buy and hold projections", "refinance analysis", "seller finance amortization", "amortization table", "amortization schedule", "lease option analysis", "lease-option calculator", "equity build up", "30 year projection", "compare investment scenarios", "side by side comparison", "what if analysis", "run different scenarios", "mortgage calculator", "payment calculator", "tax benefits of real estate", "depreciation calculation", "cost segregation estimate", "principal paydown", "loan payoff schedule", "balloon payment calculator", "wrap mortgage calculator", "subject-to payment analysis", "real estate ROI over time", "wealth building projection", "net worth projection from real estate", "compare buying vs renting", or any request involving running detailed financial projections, amortization schedules, or multi-scenario comparisons for real estate investments.
version: 1.0.0
---

# Investment Calculator

## Overview

A comprehensive real estate investment calculator that handles every scenario an investor encounters. Not just simple mortgage math — this produces full financial models with amortization tables, equity build-up curves, tax benefit estimates, and multi-year projections. Supports: BRRRR analysis, flip profit/loss, buy-and-hold projections (5/10/30 year), refinance analysis, seller finance amortization, lease-option analysis, wrap mortgage calculations, subject-to payment analysis, and side-by-side scenario comparisons. The user describes what they want to analyze, and LindaAI builds a detailed financial model with every number they need to make a decision.

## When This Skill Applies

- User asks for BRRRR analysis on a property
- User wants to know flip profit/loss on a deal
- User asks for buy-and-hold projections over multiple years
- User needs a refinance analysis (current vs. new terms)
- User wants an amortization table or schedule
- User asks about seller finance terms and payment breakdowns
- User needs lease-option analysis
- User wants to compare two or more investment scenarios side by side
- User asks "what are my returns over 10 years?"
- User wants to see equity build-up over time
- User asks about tax benefits, depreciation, or cost segregation estimates
- User needs a balloon payment or payoff calculation
- User wants wrap mortgage or subject-to payment math
- User asks "which deal is better?" comparing two properties or financing options

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

### Core Calculation Engine

Before any specific analysis, LindaAI uses these standard formulas:

**Monthly Payment (P&I — fully amortizing)**
```
M = P × [r(1+r)^n] / [(1+r)^n - 1]
Where:
  P = principal (loan amount)
  r = monthly interest rate (annual rate / 12)
  n = total payments (years × 12)
```

**Monthly Payment (Interest-Only)**
```
M = P × r
Where:
  P = principal
  r = monthly interest rate
```

**Remaining Balance at Month X**
```
B(x) = P × [(1+r)^n - (1+r)^x] / [(1+r)^n - 1]
```

**Principal Paid in Month X**
```
Principal(x) = M - [B(x-1) × r]
```

**Interest Paid in Month X**
```
Interest(x) = B(x-1) × r
```

**Total Interest Over Life of Loan**
```
Total Interest = (M × n) - P
```

---

### Analysis Type 1: BRRRR (Buy, Rehab, Rent, Refinance, Repeat)

User provides: purchase price, rehab cost, ARV, rent, refinance terms.

**Phase 1 — Buy & Rehab**
```
Total Acquisition Cost = Purchase Price + Rehab + Closing Costs (buy) + Holding Costs
  Closing costs (buy): ~2-3% of purchase price
  Holding costs: Monthly carrying cost × rehab timeline (months)
    Carrying cost = insurance + taxes + utilities + loan payment (if financed)
```

**Phase 2 — Rent**
```
Monthly Cash Flow = Rent - Vacancy - Expenses - Debt Service
  (Use deal-analyzer expense model)
Stabilized NOI = annual cash flow before debt service
```

**Phase 3 — Refinance**
```
Refinance Amount = ARV × LTV% (typically 70-80%)
Cash Recouped = Refinance Amount - Original Loan Payoff - Refi Closing Costs
Cash Left in Deal = Total Acquisition Cost - Cash Recouped
```

**Phase 4 — Repeat Assessment**
```
New Monthly Payment = amortized payment on refinance amount
New Monthly Cash Flow = Rent - Vacancy - Expenses - New Payment
Cash-on-Cash (on cash left in deal) = Annual Cash Flow / Cash Left in Deal
Infinite Return? = Did you pull out ALL your cash? (Cash Left in Deal <= 0)
```

**BRRRR Summary Table:**

| Phase | Amount |
|-------|--------|
| Purchase Price | $XXX,XXX |
| Rehab Cost | $XX,XXX |
| Closing Costs (buy) | $X,XXX |
| Holding Costs | $X,XXX |
| **Total Investment** | **$XXX,XXX** |
| After-Repair Value (ARV) | $XXX,XXX |
| Refinance LTV | XX% |
| Refinance Loan Amount | $XXX,XXX |
| Payoff Original Loan | $XXX,XXX |
| Refi Closing Costs | $X,XXX |
| **Cash Back at Refi** | **$XX,XXX** |
| **Cash Left in Deal** | **$XX,XXX** |
| Monthly Rent | $X,XXX |
| Monthly Expenses + New Payment | $X,XXX |
| **Monthly Cash Flow** | **$XXX** |
| **Cash-on-Cash Return** | **XX.X%** |
| **Infinite Return?** | **Yes/No** |

---

### Analysis Type 2: Flip Profit/Loss

User provides: purchase price, rehab cost, ARV, holding period, selling costs.

```
ACQUISITION COSTS
Purchase Price:                    $XXX,XXX
Closing Costs (buy — 2-3%):       $X,XXX
Financing Points (if hard money):  $X,XXX
Total Acquisition:                 $XXX,XXX

REHAB COSTS
Construction/Labor:                $XX,XXX
Materials:                         $XX,XXX
Permits:                           $X,XXX
Contingency (10-15%):              $X,XXX
Total Rehab:                       $XX,XXX

HOLDING COSTS (over X months)
Loan Payments:                     $X,XXX
Insurance:                         $XXX
Taxes:                             $XXX
Utilities:                         $XXX
Total Holding:                     $X,XXX

SELLING COSTS
Realtor Commission (5-6%):         $XX,XXX
Seller Closing Costs (1-2%):       $X,XXX
Staging/Marketing:                 $X,XXX
Total Selling:                     $XX,XXX

PROFIT / LOSS
Sale Price (ARV):                  $XXX,XXX
- Total Acquisition:               $XXX,XXX
- Total Rehab:                     $XX,XXX
- Total Holding:                   $X,XXX
- Total Selling:                   $XX,XXX
═══════════════════════════════════
NET PROFIT:                        $XX,XXX
ROI:                               XX.X%
Annualized ROI:                    XX.X%
Profit per Month:                  $X,XXX
```

**The 70% Rule Check:**
```
Maximum Offer = ARV × 70% - Rehab Cost
Is purchase price at or below this? [Yes = Good / No = Tight margins]
```

---

### Analysis Type 3: Buy-and-Hold Projections (5/10/30 Year)

User provides: purchase price, financing terms, rent, expenses.

Build year-by-year projection table:

| Year | Rent (3% growth) | Expenses | NOI | Debt Service | Cash Flow | Property Value (3% appr.) | Loan Balance | Equity | Total Return |
|------|------------------|----------|-----|-------------|-----------|--------------------------|-------------|--------|-------------|
| 1 | | | | | | | | | |
| 2 | | | | | | | | | |
| 3 | | | | | | | | | |
| ... | | | | | | | | | |
| 30 | | | | | | | | | |

**Assumptions (adjustable):**
- Annual rent growth: 3% (conservative) / 4% (moderate) / 5% (aggressive)
- Annual appreciation: 3% (conservative) / 4% (moderate) / 5% (aggressive)
- Annual expense growth: 2% (tied to inflation)
- Tax bracket for depreciation benefit: user-specified or 24% default

**Wealth Building Summary at Year X:**

| Metric | Year 5 | Year 10 | Year 20 | Year 30 |
|--------|--------|---------|---------|---------|
| Property Value | | | | |
| Loan Balance | | | | |
| Equity | | | | |
| Total Cash Flow (cumulative) | | | | |
| Total Principal Paid (cumulative) | | | | |
| Total Appreciation | | | | |
| Total Depreciation Tax Savings | | | | |
| **Total Wealth Created** | | | | |
| **Annualized Total Return** | | | | |

---

### Analysis Type 4: Refinance Analysis

User provides: current loan terms, proposed new terms, property value.

```
CURRENT LOAN
Original Amount:        $XXX,XXX
Current Balance:        $XXX,XXX
Interest Rate:          X.XX%
Monthly Payment:        $X,XXX
Remaining Term:         XX years
Monthly Interest:       $XXX
Monthly Principal:      $XXX

PROPOSED REFINANCE
New Loan Amount:        $XXX,XXX (balance + cash-out if any)
New Interest Rate:      X.XX%
New Term:               XX years
New Monthly Payment:    $X,XXX
Closing Costs:          $X,XXX

COMPARISON
Monthly Savings:        $XXX
Break-Even Point:       XX months (closing costs / monthly savings)
Total Interest (current remaining): $XXX,XXX
Total Interest (new):              $XXX,XXX
Interest Savings Over Life:        $XXX,XXX

CASH-OUT ANALYSIS (if applicable)
Cash Out Amount:        $XX,XXX
New LTV:               XX%
Net Cash After Costs:   $XX,XXX
Use of Funds:           [reinvest / rehab / acquire another property]
```

---

### Analysis Type 5: Seller Finance Amortization

User provides: sale price, down payment, interest rate, term, balloon (if any).

**Generate Full Amortization Schedule:**

| Payment # | Date | Payment | Principal | Interest | Balance |
|-----------|------|---------|-----------|----------|---------|
| 1 | | $X,XXX | $XXX | $XXX | $XXX,XXX |
| 2 | | $X,XXX | $XXX | $XXX | $XXX,XXX |
| ... | | | | | |
| Balloon | | $XXX,XXX | $XXX,XXX | $XXX | $0 |

**Summary:**
```
Sale Price:                 $XXX,XXX
Down Payment:               $XX,XXX
Loan Amount:                $XXX,XXX
Interest Rate:              X.XX%
Amortization:               XX years
Balloon Due:                Year X (if applicable)
Monthly Payment:            $X,XXX
Total Interest Paid:        $XXX,XXX (over full term or to balloon)
Balance at Balloon:         $XXX,XXX
Total Paid to Seller:       $XXX,XXX (down + payments + balloon)
Seller's Total Return:      $XXX,XXX (total paid - sale price = seller's interest profit)
Buyer's Effective Cost:     $XXX,XXX
```

For seller finance deals, also calculate:
- Buyer's cash-on-cash return if renting the property
- Buyer's monthly spread (rent minus payment minus expenses)
- Refinance-ability at balloon date (estimated future equity vs. balance)

---

### Analysis Type 6: Lease-Option Analysis

User provides: option price, option fee, monthly rent, rent credit, lease term, estimated future value.

**For the Buyer (Tenant-Buyer):**
```
Option Price (purchase price):          $XXX,XXX
Option Fee (upfront, non-refundable):   $X,XXX
Monthly Rent:                           $X,XXX
Monthly Rent Credit:                    $XXX
Lease Term:                             XX months
Estimated Value at Exercise:            $XXX,XXX

Total Rent Paid:                        $XX,XXX
Total Rent Credits:                     $XX,XXX
Effective Down Payment at Exercise:     $XX,XXX (option fee + rent credits)
Remaining Balance to Finance:           $XXX,XXX
Built-in Equity at Exercise:            $XX,XXX (value - option price)
```

**For the Seller (Investor doing lease-option):**
```
Current Property Value:                 $XXX,XXX
Your Basis (what you paid/owe):         $XXX,XXX
Option Fee Received:                    $X,XXX
Monthly Rent Received:                  $X,XXX
Your Monthly Costs (PITI + expenses):   $X,XXX
Monthly Spread:                         $XXX
Total Spread Over Term:                 $XX,XXX

If Tenant-Buyer Exercises:
  Sale Price:                           $XXX,XXX
  Your Basis:                           $XXX,XXX
  Gross Profit:                         $XX,XXX
  Plus Cash Flow During Term:           $XX,XXX
  Plus Option Fee:                      $X,XXX
  Total Return:                         $XX,XXX

If Tenant-Buyer Does NOT Exercise:
  Option Fee Kept:                      $X,XXX
  Cash Flow During Term:                $XX,XXX
  Property Retained (current value):    $XXX,XXX
  Total Return:                         $XX,XXX (keep everything + property)
  Re-list with new lease-option and repeat.
```

---

### Analysis Type 7: Side-by-Side Scenario Comparison

When the user wants to compare two or more deals or financing structures.

| Metric | Scenario A | Scenario B | Scenario C |
|--------|-----------|-----------|-----------|
| Property | | | |
| Purchase Price | | | |
| Cash Required | | | |
| Monthly Payment | | | |
| Monthly Cash Flow | | | |
| Annual Cash Flow | | | |
| Cash-on-Cash Return | | | |
| Cap Rate | | | |
| DSCR | | | |
| 5-Year Equity | | | |
| 10-Year Wealth Created | | | |
| Break-Even Occupancy | | | |
| Risk Level | | | |
| **Winner?** | | | |

Include a written analysis explaining which scenario wins and why, with consideration for risk tolerance, cash availability, and timeline.

---

### Tax Benefit Calculations (Included When Relevant)

**Depreciation (Residential)**
```
Depreciable Basis = Purchase Price - Land Value (typically 20% of price)
                   + Improvements (rehab that extends useful life)
Annual Depreciation = Depreciable Basis / 27.5 years
Monthly Depreciation = Annual / 12
Tax Savings = Annual Depreciation × Marginal Tax Rate
```

**Depreciation (Commercial)**
```
Annual Depreciation = Depreciable Basis / 39 years
```

**Cost Segregation Estimate (accelerated depreciation)**
```
Estimated components reclassifiable to 5/7/15 year:
  Personal property (5-year): ~15-25% of building value
  Land improvements (15-year): ~5-15% of building value
  Building (27.5/39-year): remaining

Year 1 Bonus Depreciation Impact:
  Without cost seg: $XX,XXX depreciation
  With cost seg: $XX,XXX depreciation (XX% increase)
  Additional tax savings Year 1: $XX,XXX
```

**Note:** Always include disclaimer that tax estimates are illustrative and the user should consult a CPA. Never position AI calculations as tax advice.

### Save Analysis

Save to:
```
~/Desktop/lindaai/output/investment-calcs/{description-slug}-{date}.md
```

## Output Format

Varies by analysis type. Each analysis includes:
1. Summary of inputs and assumptions
2. Detailed calculations with formulas shown
3. Results tables (clean, formatted)
4. Amortization schedules where applicable (can be truncated to annual summaries for 30-year loans, with option for full monthly detail)
5. Visual indicators (metrics rated as strong/acceptable/weak)
6. Written recommendation or comparison verdict
7. Sensitivity analysis ("if rent drops 10%, cash flow becomes $XXX")

## Example Usage

**User:** "Run a BRRRR analysis. I can buy this duplex for $120K, it needs $40K in rehab, ARV is $210K. Each side rents for $900. I'll use hard money at 12% interest-only for the purchase and rehab, then refi into a 30-year conventional at 7.5% and 75% LTV."

**LindaAI calculates:**
- Total acquisition: $120K + $40K + $4.8K closing + $8K holding (5 months at 12% on $160K) = $172,800
- Hard money payment during rehab: $160K x 12% / 12 = $1,600/mo
- Refi amount: $210K x 75% = $157,500
- Cash recouped: $157,500 - $160K payoff - $4,725 refi closing = -$7,225 (still owe)
- Wait — refi doesn't cover the full amount. Cash left in deal: $172,800 - $152,775 = $20,025
- New payment: $157,500 at 7.5% / 30yr = $1,101/mo
- Gross rent: $1,800/mo
- Expenses (vacancy 8%, taxes, insurance, maintenance, CapEx, management): ~$558/mo
- Cash flow: $1,800 - $558 - $1,101 = $141/mo ($1,692/yr)
- Cash-on-cash on $20,025 left in deal: 8.4%
- Infinite return: No (still have $20K in the deal)
- Verdict: "Solid BRRRR but not infinite return. You'd need ARV of $230K+ or purchase at $105K to pull all cash out. Still a strong 8.4% CoC with forced equity of $52.5K built through rehab."

**User:** "Now compare that to just buying it at $120K with 25% down conventional and renting it as-is for $750/side without rehab."

**LindaAI builds side-by-side comparison showing both scenarios with all metrics.**

## Error Handling

- **If the user does not specify which analysis type they want:** Infer from context. If they mention "rehab" and "refi", it's BRRRR. If they mention "ARV" and "sell", it's a flip. If they give rent and financing, it's buy-and-hold. If ambiguous, ask: "What type of analysis do you need? BRRRR, flip, buy-and-hold projection, refinance, seller finance amortization, lease-option, or side-by-side comparison?"
- **If the user does not provide enough inputs for the chosen analysis type:** List the specific missing inputs: "To run a BRRRR analysis, I still need: rehab cost, ARV, and refi terms (LTV, rate, term). Can you provide these?"
- **If calculations produce negative cash flow or negative returns:** Do not just report the negative number. Also show: (1) what price would make it work, (2) what rent would make it work, (3) what terms would make it work. Give the user actionable alternatives.
- **If the user provides inputs that seem unrealistic (e.g., 2% interest rate on conventional, 150% LTV refi):** Flag: "These terms seem unusual — {specific concern}. If they're accurate, I'll run the numbers as-is. If not, here are typical market terms for {scenario}: {typical ranges}."
- **If the output directory does not exist:** Create `~/Desktop/lindaai/output/investment-calcs/` automatically before saving.
- **If a calculation file already exists with the same description:** Append the date to create a unique filename: `{description-slug}-{YYYY-MM-DD}.md`.
- **If the user asks for a 30-year amortization table:** Provide annual summaries by default (30 rows) rather than 360 monthly rows. Offer: "I've shown annual summaries. Want the full monthly amortization table? It'll be 360 rows."
- **If tax benefit calculations are included:** Always include the disclaimer: "Tax estimates are illustrative only. Consult a CPA or tax professional before making tax-related decisions. These calculations do not constitute tax advice."
- **If the user compares scenarios with different property types or markets:** Note: "These scenarios involve different properties/markets, so the comparison reflects both the deal terms AND the market differences. For a pure financing comparison, use the same property with different terms."
- **If the user provides a balloon payment scenario but does not specify what happens at the balloon date:** Calculate and present the balloon payment amount and remaining balance, then flag: "At the balloon date, the remaining balance will be ${X}. The buyer will need to refinance, pay off the balance, or negotiate an extension. Factor refinance-ability into your decision."


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
