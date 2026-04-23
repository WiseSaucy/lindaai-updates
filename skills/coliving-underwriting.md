---
name: coliving-underwriting
description: This skill should be used when the user asks to "underwrite a co-living deal", "co-living analysis", "co-living underwriting", "room by room rental analysis", "rent by the room", "house hacking analysis", "co-living feasibility", "sober living underwriting", "student housing analysis", "room rental strategy", "per-room rent analysis", "co-living cash flow", "co-living deal", "is this property good for co-living", "how much can I make renting by the room", "co-living vs traditional rental", "analyze this for room rentals", "co-living pro forma", "boarding house analysis", "shared housing underwriting", "co-living conversion", "room-by-room breakdown", "co-living market research", "co-living comps", or any request involving analyzing a property for co-living, rent-by-the-room, sober living, student housing, or shared housing strategies.
version: 1.0.0
---

# Co-Living Underwriting

## Overview

Full-stack underwriting for co-living and rent-by-the-room strategies. LindaAI takes any property — single-family, multi-family, or large home — and analyzes it through the co-living lens: room-by-room rental projections, co-living market comps, full deal underwriting (acquisition, renovation, operating expenses, NOI, cash-on-cash, cap rate), feasibility assessment, and multiple exit scenarios. Covers traditional co-living, sober living, student housing, corporate housing, and hybrid models. The output is an investor-ready underwriting package that answers: "How much more can I make renting this property by the room instead of as a whole unit?" LindaAI runs the numbers so you can make the call.

## When This Skill Applies

- User provides a property and wants to know if it works for co-living
- User asks "how much can I make renting by the room?"
- User wants to compare co-living revenue vs. traditional rental
- User asks for room-by-room rental breakdown
- User wants to underwrite a sober living or student housing property
- User asks about co-living market demand in a specific area
- User says "analyze this for co-living" or "co-living pro forma"
- User wants a co-living conversion cost estimate
- User is evaluating a property for house hacking with room rentals
- User wants exit scenarios for a co-living property

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

### Step 0: Gather Property Details

Parse what the user provided. Ask for anything missing:

| Input | Required | Example |
|-------|----------|---------|
| Property address or description | Yes | "123 Main St, Austin TX" or "5bd/3ba SFR near UT campus" |
| Purchase price | Yes | $350,000 |
| Bedrooms | Yes | 5 |
| Bathrooms | Yes | 3 |
| Square footage | Helpful | 2,400 sqft |
| Current condition | Helpful | Turnkey, needs light rehab, needs full renovation |
| Financing details | Yes | Conventional 25% down at 7%, seller finance, cash, etc. |
| Target co-living model | Helpful | Traditional co-living, sober living, student housing, corporate |
| Estimated rehab budget | If applicable | $40,000 |

If the user provides an address, use WebSearch to fill in missing property details (bed/bath, sqft, lot size, year built, etc.).

### Step 1: Market Research & Comps

> 🤠 "Hold tight — heading over yonder to gather up the details."

Research the local co-living and room rental market. This is critical — co-living economics vary dramatically by market.

**Search queries to run:**
- `"rooms for rent" "{city}" "{zip code}" site:roomies.com OR site:rooms.com OR site:spareroom.com`
- `"room for rent" near "{address}" Craigslist`
- `"co-living" "{city}" "{state}" pricing`
- `"sober living" "{city}" rates` (if sober living model)
- `"student housing" "{city}" per room rates` (if student model)
- `"furnished room rental" "{city}" monthly`
- `"{city}" "{state}" average rent {bedrooms} bedroom`
- `"co-living spaces" "{city}" competitors`

**Data to capture:**

| Metric | Source | Value |
|--------|--------|-------|
| Average room rental rate (furnished) | Room listing sites | $/month |
| Average room rental rate (unfurnished) | Craigslist, FB Marketplace | $/month |
| Traditional whole-unit rent (comp) | Zillow, Rentometer | $/month |
| Co-living competitors in area | Google, listing sites | Names, pricing |
| Occupancy/demand signals | Listing activity, wait lists | High/Medium/Low |
| Student population nearby | University data | If applicable |
| Major employers nearby | Google | Corporate housing demand |
| Furnished room premium | Comp analysis | % above unfurnished |

### Step 2: Room-by-Room Rental Analysis

This is the core of co-living underwriting — what makes it different from traditional rental analysis.

**For each bedroom, assess and assign a rental rate:**

| Room | Size | Features | Condition | Private Bath? | Rate |
|------|------|----------|-----------|---------------|------|
| Room 1 (Master) | Large | Walk-in closet, en-suite bath | Good | Yes | $X |
| Room 2 | Medium | Standard closet | Good | No (shared) | $X |
| Room 3 | Medium | Window, good light | Good | No (shared) | $X |
| Room 4 | Small | Compact but functional | Fair | No (shared) | $X |
| Room 5 | Large | Could be converted to 2 | Good | Yes | $X |

**Pricing factors:**
- **Private bathroom** = 15-25% premium over shared bath rooms
- **Room size** = Large rooms command $50-150/mo more than small rooms
- **Master suite** = Highest rate, typically 20-30% above smallest room
- **Natural light / windows** = Slight premium
- **Closet space** = Factor for furnished vs. unfurnished
- **Floor level** = Ground floor may be less desirable in some markets

**Calculate total gross room revenue:**
```
Room 1: $____/mo
Room 2: $____/mo
Room 3: $____/mo
Room 4: $____/mo
Room 5: $____/mo
─────────────────
Total Monthly Room Revenue: $____/mo
Total Annual Room Revenue: $____/yr
```

**Compare to traditional rental:**
```
Co-Living Gross Monthly: $____
Traditional Whole-Unit Rent: $____
Co-Living Premium: $____ (+__%)
```

### Step 3: Co-Living Conversion Costs (if applicable)

If the property needs work to be co-living ready, estimate conversion costs:

| Item | Cost Range | Notes |
|------|-----------|-------|
| Add bedroom door locks (keyed) | $50-150/door | Required — every room needs a lock |
| Furnish each room (bed, desk, dresser, nightstand) | $500-1,500/room | Mid-range furnished |
| Common area furniture (living room, kitchen) | $1,000-3,000 | Durable, commercial-grade |
| Add bathroom (if converting a room) | $8,000-15,000 | Major value-add for premium rooms |
| Kitchen upgrades (durability) | $500-2,000 | Commercial-grade appliances if high turnover |
| Laundry (washer/dryer) | $1,000-2,500 | Essential for co-living |
| WiFi setup (mesh/commercial) | $200-500 | Must be reliable — non-negotiable |
| Security cameras (exterior) | $200-800 | Required for liability/safety |
| Storage solutions | $200-500 | Shelving, bins for each room |
| Smart locks (keyless entry) | $150-300/door | Reduces key management headaches |
| Deep clean & paint | $500-2,000 | Between every turnover too |
| Signage / house rules | $50-100 | Posted expectations reduce issues |

**Total estimated conversion cost:** $______

### Step 4: Operating Expense Breakdown

Co-living has different expense profiles than traditional rentals because the operator covers utilities and common area costs.

| Expense | Monthly | Annual | Notes |
|---------|---------|--------|-------|
| **Mortgage (P&I)** | $ | $ | Based on financing terms |
| **Property Taxes** | $ | $ | Research county rate |
| **Insurance** | $ | $ | Need landlord policy — may need commercial if 5+ tenants |
| **Utilities - Electric** | $ | $ | Operator-paid in co-living |
| **Utilities - Water/Sewer** | $ | $ | Operator-paid |
| **Utilities - Gas** | $ | $ | If applicable |
| **Internet/WiFi** | $ | $ | High-speed, non-negotiable |
| **Trash/Recycling** | $ | $ | Operator-paid |
| **Lawn Care** | $ | $ | Weekly service |
| **Cleaning (common areas)** | $ | $ | Weekly or bi-weekly — $100-200/visit |
| **Repairs & Maintenance** | $ | $ | Higher turnover = higher maintenance |
| **CapEx Reserves** | $ | $ | 5-8% of gross revenue |
| **Vacancy/Turnover** | $ | $ | Per-room vacancy, not whole-unit — typically 10-15% |
| **Property Management** | $ | $ | 10-15% if managed; co-living PM is more work than traditional |
| **Furnishing Replacement** | $ | $ | Budget $50-100/room/month for wear and tear |
| **Supplies (TP, paper towels, cleaning)** | $ | $ | $50-100/month |
| **Marketing/Listing Fees** | $ | $ | Room listing sites, FB ads |
| **Tenant Screening** | $ | $ | Background checks per applicant |
| **Legal/Compliance** | $ | $ | Lease review, local regulations |

**Total Monthly Expenses:** $______
**Total Annual Expenses:** $______

### Step 5: Financial Metrics

Calculate every metric that matters:

**Net Operating Income (NOI)**
```
Gross Room Revenue (annual): $______
- Vacancy Allowance (____%): -$______
= Effective Gross Income: $______
- Total Operating Expenses: -$______
= NOI: $______
```

**Cash Flow**
```
NOI: $______
- Annual Debt Service: -$______
= Annual Cash Flow: $______
Monthly Cash Flow: $______
Cash Flow Per Room: $______/room/month
```

**Return Metrics**
```
Cap Rate: NOI / Purchase Price = ____%
Cash-on-Cash Return: Annual Cash Flow / Total Cash Invested = ____%
Gross Rent Multiplier: Purchase Price / Annual Gross Rent = ____
DSCR: NOI / Annual Debt Service = ____
Break-Even Occupancy: (Expenses + Debt Service) / Gross Potential Rent = ____%
```

**Total Cash Invested**
```
Down Payment: $______
Closing Costs (est. 3%): $______
Conversion/Rehab Costs: $______
Furnishing Costs: $______
Operating Reserve (3 months): $______
= Total Cash Required: $______
```

### Step 6: Co-Living vs. Traditional Comparison

Side-by-side comparison to quantify the co-living premium:

| Metric | Traditional Rental | Co-Living (By Room) | Delta |
|--------|-------------------|-------------------|-------|
| Gross Monthly Revenue | $ | $ | +$____ (+___%) |
| Annual Gross Revenue | $ | $ | +$ |
| Monthly Expenses | $ | $ | +$ (higher for co-living) |
| Monthly Cash Flow | $ | $ | +$ |
| Annual Cash Flow | $ | $ | +$ |
| Cash-on-Cash Return | ____% | ____% | +____% |
| Cap Rate | ____% | ____% | +____% |
| Break-Even Occupancy | ____% | ____% | |
| Management Intensity | Low | High | More work |

**Key insight:** Co-living generates higher gross revenue but also higher expenses (utilities, cleaning, turnover, furnishing). The spread between the two is the co-living premium. A good co-living deal should generate at least 30-50% more net cash flow than the traditional rental to justify the extra management overhead.

### Step 7: Sensitivity Analysis

Test how the deal holds up under different scenarios:

| Scenario | Occupancy | Avg Room Rate | Monthly Cash Flow | CoC Return |
|----------|-----------|--------------|-------------------|------------|
| **Best Case** | 95% | $____ (market high) | $ | ____% |
| **Base Case** | 85% | $____ (market avg) | $ | ____% |
| **Worst Case** | 70% | $____ (market low) | $ | ____% |
| **Break Even** | ____% | $____ | $0 | 0% |

### Step 8: Exit Scenarios

| Exit Strategy | When | Projected Value | ROI |
|--------------|------|----------------|-----|
| **Hold & Operate** | Ongoing | Cash flow $____/yr | ____% CoC |
| **Sell as Co-Living Business** | 3-5 years | NOI x ____ cap = $____ | ____% total |
| **Convert to Traditional Rental** | Anytime | Value at ____ GRM = $____ | Fallback plan |
| **Sell Property** | 3-5 years | ARV/appreciation = $____ | ____% total |
| **Refinance & Hold** | 12-24 months | New loan at ____% LTV, pull $____ | Recycle capital |

### Step 9: Feasibility Assessment & Risk Flags

**Go / Proceed with Caution / No-Go Assessment:**

Check each factor:

| Factor | Status | Notes |
|--------|--------|-------|
| **Zoning/Legality** | Check local rules on unrelated occupants, rooming houses, max occupancy per bedroom | CRITICAL |
| **HOA Restrictions** | If HOA exists, likely prohibits room rentals | Deal-killer if HOA restricts |
| **Parking** | Enough parking for all tenants? | 1 spot per room minimum |
| **Bathroom Ratio** | Ideal: 1 bath per 2 rooms minimum | Below 1:3 is problematic |
| **Kitchen Capacity** | Can the kitchen handle X people? | May need upgrades |
| **Neighborhood Fit** | Will neighbors complain about multiple tenants? | Suburban SFR = higher risk |
| **Insurance** | Can you get proper coverage for room rentals? | Some insurers won't cover |
| **Local Demand** | Is there actual demand for room rentals here? | No demand = no deal |
| **Management Plan** | Who manages day-to-day? | Co-living is hands-on |

**Provide a clear recommendation:**
- **GO** — Strong co-living fundamentals, good market demand, numbers work
- **PROCEED WITH CAUTION** — Numbers work but there are risk factors to mitigate
- **NO-GO** — Doesn't pencil, legal issues, or market doesn't support it

### Step 10: Generate the Report

Save the full underwriting package to `brain/research/coliving-underwriting-[address]-[date].md`.

Present in chat:
1. Executive Summary (2-3 sentences: does this work for co-living? How much more do you make?)
2. Room-by-Room Revenue Table
3. Co-Living vs. Traditional Comparison Table
4. Key Financial Metrics (CoC, cap rate, monthly cash flow)
5. Go / Caution / No-Go recommendation with top 3 reasons

Tell the user: "The full underwriting package — sensitivity analysis, exit scenarios, expense breakdown, and market comps — is roped up and saved to brain/research/. LindaAI did the heavy lifting; now it's your call, partner."

**Disclaimer:**
> "This underwriting analysis is based on estimated market data and standard assumptions. Verify local zoning laws, occupancy limits, and insurance requirements before proceeding. This is not legal or financial advice."

🤠 *Generated by LindaAI* 🏇


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
