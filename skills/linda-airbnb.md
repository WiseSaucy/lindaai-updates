---
name: linda-airbnb
description: This skill should be used when the user asks to "underwrite an Airbnb", "Airbnb analysis", "Airbnb underwriting", "short-term rental underwriting", "STR underwriting", "is this a good Airbnb", "Airbnb cash flow", "Airbnb deal analysis", "how much can I make on Airbnb", "Airbnb pro forma", "VRBO analysis", "short-term rental deal", "Airbnb numbers", "run the Airbnb numbers", "STR pro forma", "Airbnb revenue estimate", "Airbnb occupancy estimate", "should I Airbnb this property", "Airbnb vs long-term rental", "vacation rental underwriting", "Airbnb investment analysis", "STR cash-on-cash", "Airbnb ROI", "Airbnb feasibility", "furnishing budget for Airbnb", "Airbnb startup costs", "Airbnb expense breakdown", "short-term rental regulations", "can I Airbnb this property", "Airbnb market research", "Airbnb comp analysis", or any request involving analyzing whether a property works as an Airbnb or short-term rental investment.
version: 1.0.0
---

# Airbnb / Short-Term Rental Underwriting

## Overview

Full-stack underwriting for Airbnb and short-term rental investments. LindaAI takes any property and runs a complete STR analysis: market research (ADR, occupancy, seasonality, regulations), revenue projections by season, full startup cost budget (furnishing, permits, photography, supplies), month-by-month operating expenses, cash flow projections, and return metrics (cash-on-cash, cap rate, ROI). Compares STR revenue against long-term rental as a baseline to quantify the Airbnb premium — and whether the extra work is worth it. Includes a regulatory check, sensitivity analysis across occupancy scenarios, and a clear go/no-go recommendation. The output is an investor-ready underwriting package that answers: "Will this property make money on Airbnb, and how much more than a traditional rental?" LindaAI runs every number so you can decide with confidence.

## When This Skill Applies

- User provides a property and asks "should I Airbnb this?"
- User wants to know estimated Airbnb revenue for a property
- User asks "how much can I make on Airbnb with this property?"
- User wants to compare Airbnb income vs. long-term rental
- User asks for STR cash-on-cash return or ROI
- User wants to know Airbnb startup costs and furnishing budget
- User asks about STR regulations or legality in an area
- User says "run the Airbnb numbers" or "Airbnb pro forma"
- User wants seasonal revenue projections for a vacation rental
- User is evaluating a property specifically as an STR investment
- User asks about Airbnb occupancy rates or ADR in a market
- User wants a VRBO or vacation rental feasibility analysis

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
| Property address or description | Yes | "456 Beach Dr, Destin FL" or "3/2 condo near the beach in Destin" |
| Purchase price | Yes | $425,000 |
| Bedrooms | Yes | 3 |
| Bathrooms | Yes | 2 |
| Square footage | Helpful | 1,600 sqft |
| Property type | Helpful | SFR, condo, townhouse, cabin, etc. |
| Financing details | Yes | Conventional 25% down at 7.5%, cash, etc. |
| Current condition | Helpful | Turnkey, needs rehab, already furnished |
| Unique features | Helpful | Pool, hot tub, ocean view, lake access, ski-in/out, etc. |
| Target guest type | Helpful | Families, couples, business travelers, groups |

If the user provides an address, use WebSearch to fill in missing property details.

### Step 1: Regulatory & Legality Check

This comes first because if STR is illegal or heavily restricted, the rest of the analysis is moot.

> 🤠 "Hold tight — heading over yonder to gather up the details."

**Search queries:**
- `"short term rental regulations {city} {state} {year}"`
- `"Airbnb laws {city} {state}"`
- `"short term rental permit {city} {state}"`
- `"vacation rental ordinance {city} {county}"`
- `"{city} {state} STR license requirements"`
- `"HOA short term rental restrictions {address or community name}"`

**Regulatory checklist:**

| Requirement | Status | Details |
|------------|--------|---------|
| STR Legal in Jurisdiction? | Yes / No / Restricted | |
| Permit/License Required? | Yes / No | Cost: $____ |
| Zoning Allows STR? | Yes / No / Conditional | Zone: ____ |
| Owner-Occupied Requirement? | Yes / No | |
| Maximum Nights per Year? | Unlimited / ____ nights | |
| Minimum Stay Requirement? | None / ____ nights | |
| HOA Allows STR? | Yes / No / Unknown | |
| Business License Required? | Yes / No | Cost: $____ |
| Occupancy Tax / Hotel Tax? | ____% | Collected by platform or host? |
| Safety Requirements? | Fire extinguishers, smoke detectors, etc. | |
| Insurance Requirements? | Additional STR coverage needed? | |
| Neighbor Notification? | Required / Not required | |

**If STR is illegal or banned:** Stop and tell the user immediately. Provide the specific regulation and suggest alternatives (midterm rental, long-term, etc.). Don't waste time running numbers on an illegal strategy.

**If restricted:** Note the restrictions clearly and factor them into projections (e.g., max 90 nights/year means you need a hybrid strategy).

### Step 2: Market Research — Revenue Data

Research what comparable Airbnb listings earn in the area.

**Search queries:**
- `"AirDNA {city} {state} average daily rate {year}"`
- `"Airbnb average nightly rate {city} {state} {bedrooms} bedroom"`
- `"Airbnb occupancy rate {city} {state} {year}"`
- `"VRBO {city} {state} {bedrooms} bedroom nightly rate"`
- `"short term rental revenue {city} {state}"`
- `"Airbnb market data {city} {state}"`
- `"Mashvisor {city} {state} Airbnb"`
- `"{city} {state} vacation rental average income"`

**Data to capture:**

| Metric | Value | Source |
|--------|-------|--------|
| Average Daily Rate (ADR) | $____ | |
| Median Occupancy Rate | ____% | |
| Revenue Per Available Night (RevPAN) | $____ | ADR x Occupancy |
| Average Monthly Revenue (gross) | $____ | |
| Average Annual Revenue (gross) | $____ | |
| Number of Active Listings (market size) | ____ | |
| Supply Growth Trend | Increasing / Stable / Declining | |
| Demand Trend | Increasing / Stable / Declining | |
| Top-Performing Property Types | ____ | |
| Average Guest Rating in Area | ____/5 | |

### Step 3: Seasonality Analysis

STR revenue is not flat — it fluctuates significantly by season. This is critical for accurate projections.

**Research seasonal patterns for the market.** Search for:
- `"Airbnb peak season {city} {state}"`
- `"vacation rental seasonality {city} {state}"`
- `"{city} tourism seasons"`

**Build seasonal revenue projection:**

| Season | Months | ADR | Occupancy | Monthly Revenue | Notes |
|--------|--------|-----|-----------|----------------|-------|
| **Peak** | | $____ | ____% | $____ | Highest demand period |
| **Shoulder** | | $____ | ____% | $____ | Moderate demand |
| **Off-Season** | | $____ | ____% | $____ | Lowest demand |
| **Holidays/Events** | | $____ | ____% | $____ | Premium pricing windows |

**Annual revenue projection (month by month):**

| Month | ADR | Occupancy | Nights Booked | Revenue |
|-------|-----|-----------|---------------|---------|
| January | $____ | ____% | ____ | $____ |
| February | $____ | ____% | ____ | $____ |
| March | $____ | ____% | ____ | $____ |
| April | $____ | ____% | ____ | $____ |
| May | $____ | ____% | ____ | $____ |
| June | $____ | ____% | ____ | $____ |
| July | $____ | ____% | ____ | $____ |
| August | $____ | ____% | ____ | $____ |
| September | $____ | ____% | ____ | $____ |
| October | $____ | ____% | ____ | $____ |
| November | $____ | ____% | ____ | $____ |
| December | $____ | ____% | ____ | $____ |
| **TOTAL** | | | | **$____** |

### Step 4: Startup Cost Budget

Airbnb requires significant upfront investment beyond the property itself.

**Furnishing budget (per room method):**

| Category | Items | Budget | Notes |
|----------|-------|--------|-------|
| **Living Room** | Sofa, coffee table, TV + mount, media console, decor, throw pillows, blankets, lamps | $2,000-$4,000 | Go durable — guests are harder on furniture than tenants |
| **Kitchen** | Cookware set, dishes, glasses, utensils, knife set, small appliances (coffee maker, toaster, blender), dish towels | $500-$1,000 | Don't skimp on coffee maker — #1 guest complaint when bad |
| **Master Bedroom** | Queen/King bed + frame, nightstands, dresser, linens (2 sets), pillows, lamps, hangers, luggage rack | $1,500-$3,000 | |
| **Guest Bedroom (each)** | Queen bed + frame, nightstands, dresser, linens (2 sets), pillows, lamps | $1,000-$2,000 | Multiply by number of guest rooms |
| **Bathroom (each)** | Towel sets (3 per bath), bath mat, shower curtain, toiletry dispenser, mirror, storage | $200-$400 | White towels — bleachable |
| **Outdoor** | Patio furniture, grill (if applicable), outdoor lighting | $500-$2,000 | Huge differentiator for listings |
| **Tech** | Smart lock (keyless entry), WiFi router/mesh, smart TV streaming, noise monitor | $300-$600 | Smart lock is non-negotiable — no key exchanges |
| **Safety** | Fire extinguishers, first aid kit, smoke/CO detectors, safe | $100-$300 | Required and reviewed in Airbnb safety section |
| **Supplies Starter Kit** | Toilet paper, paper towels, soap, shampoo, cleaning supplies, laundry detergent, trash bags | $100-$200 | First 3 months of consumables |
| **Photography** | Professional listing photos | $150-$400 | Biggest ROI item — do not skip this |
| **Decor & Staging** | Wall art, mirrors, plants, coffee table books, welcome signage | $300-$800 | Makes the difference between 4.5 and 4.9 stars |

**Total furnishing estimate:** $____

**Other startup costs:**

| Item | Cost | Notes |
|------|------|-------|
| STR Permit/License | $____ | From regulatory research |
| Business License | $____ | If required |
| LLC Formation (if applicable) | $100-$500 | Recommended for liability |
| STR Insurance Policy | $____ | Short-term rental rider or dedicated policy |
| Listing Setup & Optimization | $0-$500 | DIY or hire a listing optimizer |
| Channel Manager Software | $0-$50/mo | If listing on multiple platforms |
| Dynamic Pricing Tool | $0-$30/mo | PriceLabs, Wheelhouse, Beyond Pricing |
| Cleaning Team Onboarding | $0 | But need to find and vet cleaners |

**Total Startup Investment:**
```
Furnishing: $______
Permits & Licenses: $______
Insurance (first year): $______
Tech & Tools: $______
Photography: $______
Other: $______
─────────────────────
Total Startup: $______
```

### Step 5: Operating Expense Breakdown

STR expenses are significantly higher than long-term rental. Break them down clearly.

**Monthly operating expenses:**

| Expense | Monthly | Annual | Notes |
|---------|---------|--------|-------|
| **Mortgage (P&I)** | $____ | $____ | Based on financing terms |
| **Property Taxes** | $____ | $____ | Research local rate |
| **Insurance** | $____ | $____ | STR policy — typically 20-40% more than standard landlord |
| **Utilities - Electric** | $____ | $____ | Host-paid, higher than rental (AC/heat for guests) |
| **Utilities - Water/Sewer** | $____ | $____ | Host-paid |
| **Utilities - Gas** | $____ | $____ | If applicable |
| **Internet/WiFi** | $____ | $____ | High-speed required — $60-$100/mo |
| **Trash** | $____ | $____ | May need upgraded service |
| **Lawn Care / Snow Removal** | $____ | $____ | Curb appeal matters for reviews |
| **Cleaning (per turnover)** | $____ | $____ | $75-$200/clean x estimated turnovers/mo |
| **Supplies (consumables)** | $____ | $____ | TP, soap, coffee, etc. — $50-$150/mo |
| **Platform Fees** | $____ | $____ | Airbnb ~3% host-only, VRBO 3-5% |
| **Occupancy/Hotel Tax** | $____ | $____ | ___% if not collected by platform |
| **Dynamic Pricing Tool** | $____ | $____ | PriceLabs, Wheelhouse |
| **Channel Manager** | $____ | $____ | If multi-platform |
| **Property Management** | $____ | $____ | 15-25% of gross if using STR PM |
| **Maintenance/Repairs** | $____ | $____ | Higher than LTR — more wear, faster fixes needed |
| **CapEx Reserves** | $____ | $____ | 5% of gross revenue |
| **Furnishing Replacement** | $____ | $____ | $100-$200/mo — things break, wear out |
| **Linen Laundry** | $____ | $____ | If not included in cleaning fee |
| **Guest Amenities Refresh** | $____ | $____ | Seasonal decor, welcome baskets, etc. |

**Total Monthly Expenses:** $______
**Total Annual Expenses:** $______

**Cleaning fee strategy:** Most hosts charge a cleaning fee to guests ($75-$200 depending on size). This offsets but doesn't always fully cover cleaning costs. Factor the net cleaning cost (cost minus fee collected) into expenses.

### Step 6: Financial Projections & Return Metrics

**Revenue Summary:**
```
Gross Annual Revenue (from seasonal projection): $______
- Platform Fees (3%): -$______
- Occupancy Tax (if host-collected): -$______
= Net Booking Revenue: $______
+ Cleaning Fees Collected: +$______
= Total Revenue: $______
```

**Net Operating Income:**
```
Total Revenue: $______
- Total Operating Expenses (excl. debt service): -$______
= NOI: $______
```

**Cash Flow:**
```
NOI: $______
- Annual Debt Service: -$______
= Annual Cash Flow: $______
Monthly Cash Flow: $______
```

**Return Metrics:**

| Metric | Value | Rating |
|--------|-------|--------|
| **Gross Annual Revenue** | $____ | |
| **NOI** | $____ | |
| **Monthly Cash Flow** | $____ | |
| **Annual Cash Flow** | $____ | |
| **Cap Rate** | ____% | NOI / Purchase Price |
| **Cash-on-Cash Return** | ____% | Cash Flow / Total Cash Invested |
| **DSCR** | ____ | NOI / Debt Service |
| **Revenue per Bedroom** | $____/yr | Revenue efficiency metric |
| **Cost per Booked Night** | $____ | Total expenses / nights booked |
| **Break-Even Occupancy** | ____% | Minimum occupancy to cover all costs |
| **Year 1 Total ROI** | ____% | (Cash Flow + Principal Paydown + Appreciation) / Cash Invested |

**Total Cash Invested:**
```
Down Payment: $______
Closing Costs (3%): $______
Rehab (if any): $______
Furnishing & Startup: $______
Operating Reserve (3 months): $______
= Total Cash Required: $______
```

### Step 7: STR vs. Long-Term Comparison

This is the key decision framework — is the Airbnb premium worth the extra work?

**Research long-term rental rate for the same property:**
- Search: `"{city} {state} {bedrooms} bedroom house for rent"`
- Search: `"rent estimate {address}"`

| Metric | Long-Term Rental | Airbnb / STR | Delta |
|--------|-----------------|--------------|-------|
| Gross Annual Revenue | $____ | $____ | +$____ (+___%) |
| Annual Expenses | $____ | $____ | +$____ (STR is higher) |
| Annual Cash Flow | $____ | $____ | +$____ |
| Cash-on-Cash Return | ____% | ____% | +____% |
| Startup Cost | $____ (minimal) | $____ (furnishing etc.) | +$____ |
| Management Hours/Month | 2-3 hrs | 10-20 hrs | Much higher |
| Vacancy Risk | Low (annual lease) | Variable (seasonal) | Higher |
| Regulatory Risk | Very low | Moderate-High | |
| Scalability | Easy | Harder | |

**The Airbnb Premium:** Calculate the incremental cash flow from STR over LTR, then divide by the extra startup investment. This gives you the return on the marginal investment in the STR strategy.

```
Airbnb Premium Cash Flow: $____ (STR CF - LTR CF)
Extra Startup Investment: $____ (furnishing, permits, etc.)
Return on STR Premium: ____% (premium CF / extra investment)
Breakeven on Extra Investment: ____ months
```

**Hourly rate analysis:** Estimate the extra management hours STR requires vs. LTR. Divide the premium cash flow by the extra hours. This tells the user their effective hourly rate for the additional STR work.

```
Extra Annual Cash Flow from STR: $______
Extra Hours per Year (STR vs LTR): ____
Effective Hourly Rate for STR Work: $____/hr
```

If the effective hourly rate is below $30-$50/hr, the user should seriously consider whether STR is worth the effort vs. hiring a property manager or just doing long-term.

### Step 8: Sensitivity Analysis

Test the deal under different scenarios:

| Scenario | Occupancy | ADR | Annual Revenue | Cash Flow | CoC |
|----------|-----------|-----|----------------|-----------|-----|
| **Best Case** | 80%+ | Market high | $____ | $____ | ____% |
| **Base Case** | 60-70% | Market avg | $____ | $____ | ____% |
| **Conservative** | 50% | Market avg | $____ | $____ | ____% |
| **Worst Case** | 40% | Below avg | $____ | $____ | ____% |
| **Break Even** | ____% | Market avg | $____ | $0 | 0% |

**Scenario notes:**
- **Year 1 reality:** Most new listings take 3-6 months to build reviews and optimize. Year 1 revenue is typically 60-75% of a mature listing. Factor this into projections.
- **Superhost impact:** Achieving Superhost status (after ~1 year) can increase bookings by 10-20%.
- **Regulation risk:** What happens if the city bans or restricts STR? Show the fallback to LTR.

### Step 9: Competitive Positioning

What makes this listing stand out (or not)?

**Listing strengths to highlight:**
- Unique features (pool, hot tub, views, walkability, proximity to attractions)
- Bedroom count advantage (larger homes = fewer competitors)
- Property type advantage (entire home vs. shared space)

**Competitive threats:**
- Number of competing listings in the immediate area
- New supply entering the market
- Hotel competition and pricing
- Regulation changes on the horizon

**Revenue optimization opportunities:**
- Dynamic pricing tool (PriceLabs, Beyond Pricing) — typically increases revenue 10-20%
- Midweek discounts for business travelers
- Monthly stay discounts (for shoulder/off-season)
- Pet-friendly option (10-15% more bookings in many markets)
- Event-based pricing (concerts, festivals, sports, conferences)
- Gap night pricing (fill 1-2 night gaps between bookings)

### Step 10: Exit Scenarios

| Exit Strategy | Timeline | Projected Value | Notes |
|--------------|----------|----------------|-------|
| **Hold & Operate STR** | Ongoing | Cash flow $____/yr | Requires active management |
| **Sell as Turnkey STR** | 2-5 years | Premium for furnished + booking history | Can sell with furnishings and reviews |
| **Convert to Long-Term** | Anytime | Rent at $____/mo | Fallback — sell furniture or keep furnished |
| **Convert to Midterm** | Anytime | $____/mo furnished | Lower effort than STR, higher than LTR |
| **Sell Property** | 3-5 years | $____ (appreciation) | Standard residential sale |
| **Refinance & Hold** | 12-24 months | Pull $____ in equity | Only if enough appreciation/value-add |

### Step 11: Go / No-Go Recommendation

**Decision matrix:**

| Signal | Green (Go) | Yellow (Caution) | Red (No-Go) |
|--------|-----------|-------------------|-------------|
| STR Legal & Permitted | Fully legal, no restrictions | Legal with restrictions | Banned or moratorium |
| Cash-on-Cash Return | 12%+ | 8-12% | Below 8% |
| Airbnb Premium over LTR | 50%+ more cash flow | 25-50% more | Below 25% (not worth the effort) |
| Break-Even Occupancy | Below 45% | 45-55% | Above 55% |
| Market Occupancy Rate | 65%+ | 50-65% | Below 50% |
| Year 1 Ramp Risk | Low (proven market) | Moderate (emerging) | High (unproven/oversaturated) |
| Effective Hourly Rate | $75+/hr | $40-$75/hr | Below $40/hr |

**Verdict: [STRONG BUY / GOOD DEAL / PROCEED WITH CAUTION / PASS]**

Include:
- Top 3 reasons for the recommendation
- Biggest risk and how to mitigate it
- What would make this deal better (price, ADR, occupancy needed)
- Specific next steps if proceeding

### Step 12: Save & Present

Save the full underwriting package to `brain/research/airbnb-underwriting-[address]-[date].md`.

Present in chat:
1. Regulatory status (legal or not — this is #1)
2. Projected annual revenue and monthly cash flow
3. STR vs. LTR comparison table
4. Key return metrics (CoC, cap rate, break-even occupancy)
5. Go / Caution / No-Go recommendation with top reasons

Tell the user: "The full underwriting package — month-by-month projections, startup budget, expense breakdown, sensitivity analysis, and exit scenarios — is corralled and saved to brain/research/. LindaAI ran the numbers; now it's your move, partner."

**Disclaimer:**
> "This Airbnb underwriting is based on market research and estimated data. Actual performance depends on listing quality, reviews, pricing strategy, seasonality, and market conditions. Verify local STR regulations with the city/county before purchasing. This is not legal or financial advice."

🤠 *Generated by LindaAI* 🏇


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
