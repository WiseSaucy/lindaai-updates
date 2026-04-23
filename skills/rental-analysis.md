---
name: rental-analysis
description: This skill should be used when the user asks to "analyze rents", "what should I charge for rent", "rental market analysis", "what are rents in this area", "rent comps", "rental comps", "compare rental strategies", "Airbnb vs long-term rental", "STR analysis", "midterm rental analysis", "section 8 rents", "fair market rent", "rent-to-price ratio", "vacancy rates", "co-living analysis", "room rental strategy", "what's the best rental strategy", "rental income estimate", "how much can I rent this for", "rent survey", "rental demand", "rental market research", or any request involving understanding what a property can earn as a rental and which rental strategy maximizes income.
version: 1.0.0
---

# Rental Analysis

## Overview

Performs a deep rental market analysis for any property or area. Uses web search to gather current market rents by bedroom count, vacancy rates, rent-to-price ratios, Section 8 Fair Market Rents, and short-term/midterm rental potential. Compares multiple rental strategies head-to-head — long-term, midterm (furnished), short-term (Airbnb/VRBO), co-living (rent by the room), and Section 8 — then recommends the optimal strategy based on the property type, location, and investor goals. This is not a surface-level estimate. LindaAI produces a data-backed rental analysis that an investor can use to make real decisions.

## When This Skill Applies

- User asks "what can I rent this property for?"
- User wants to compare Airbnb vs. long-term rental income
- User asks about rental rates in a specific city, zip code, or neighborhood
- User wants Section 8 Fair Market Rent (FMR) for an area
- User asks about vacancy rates in a market
- User says "rental analysis" or "rent comps"
- User is deciding between rental strategies for a property
- User wants to know if a property meets the 1% rule based on actual rents
- User asks about midterm rental or travel nurse housing potential
- User wants co-living or rent-by-the-room analysis
- User provides a property and asks "how should I rent this?"
- User wants rent-to-price ratios for a market

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

### Step 0: Parse User Input

Determine what the user provided:

| Input | Required | Example |
|-------|----------|---------|
| Property address OR city/zip | Yes | "4521 Elm St, Dallas TX" or "Dallas TX 75216" |
| Property type | Helpful | SFR, duplex, triplex, quad, condo, townhouse |
| Bedrooms/bathrooms | Helpful | 3 bed / 2 bath |
| Purchase price (if owned/buying) | Optional | $165,000 |
| Current condition | Optional | Turnkey, needs rehab, furnished |
| Preferred strategy | Optional | "I'm thinking Airbnb" |

If the user only provides an address, research the property details first.

### Step 1: Research Market Rents (Long-Term)

> 🤠 "Hold tight — heading over yonder to gather up the details."

Use WebSearch to find current long-term rental rates:

**Search queries:**
- `"{city} {state} {bedrooms} bedroom house for rent {year}"`
- `"{zip code} average rent {year}"`
- `"rent prices {neighborhood} {city} {state}"`
- `"{city} {state} rental market report {year}"`
- `"Zillow rent estimate {address}"` (Zestimate Rent)
- `"Rentometer {city} {state} {bedrooms} bedroom"`

**Data to capture:**
- Average rent for matching property type and bedroom count
- Rent range (low / median / high)
- Rent trends (increasing, flat, declining)
- Days on market for rentals
- Rent-to-price ratio for the area

**Build rent comp table:**

| Comp | Address/Area | Beds/Baths | Rent | Condition | Distance |
|------|-------------|------------|------|-----------|----------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

### Step 2: Research Section 8 / Fair Market Rent

Use WebSearch to find HUD Fair Market Rents:

**Search queries:**
- `"HUD fair market rent {county} {state} {year}"`
- `"Section 8 payment standard {city} {state} {year}"`
- `"FMR {zip code} {year}"`

**Data to capture:**
- FMR by bedroom count (0BR through 4BR)
- Payment standard percentage (usually 90-110% of FMR)
- Section 8 waitlist status (open/closed)
- Voucher utilization rate in the area

**Section 8 Rent Table:**

| Bedrooms | FMR | Payment Standard (100%) | Your Property |
|----------|-----|------------------------|---------------|
| 0 BR | | | |
| 1 BR | | | |
| 2 BR | | | |
| 3 BR | | | |
| 4 BR | | | |

### Step 3: Research Short-Term Rental (STR) Potential

Use WebSearch to find Airbnb/VRBO market data:

**Search queries:**
- `"Airbnb average daily rate {city} {state} {year}"`
- `"short term rental regulations {city} {state}"`
- `"Airbnb occupancy rate {city} {state}"`
- `"AirDNA {city} {state} market data"`
- `"VRBO {city} {state} {bedrooms} bedroom nightly rate"`
- `"{city} short term rental permit requirements"`

**Data to capture:**
- Average daily rate (ADR) for matching property type
- Average occupancy rate
- Estimated monthly revenue (ADR x occupancy x 30)
- STR regulations (permit required? banned? restricted zones?)
- Seasonality patterns (peak vs. off-season rates)
- Cleaning and turnover costs per stay
- Platform fees (Airbnb ~3% host, VRBO ~3-5%)

**STR Legality Check:**
- Is STR legal in this jurisdiction?
- Permit/license required? Cost?
- Minimum stay requirements?
- Zoning restrictions?
- HOA restrictions?
- Tax implications (occupancy tax, hotel tax)?

### Step 4: Research Midterm Rental Potential

Use WebSearch to find midterm rental data:

**Search queries:**
- `"furnished rental {city} {state} monthly rate"`
- `"travel nurse housing {city} {state}"`
- `"corporate housing {city} {state} rates"`
- `"Furnished Finder {city} {state}"`
- `"{city} {state} hospitals near {address}"` (for travel nurse demand)
- `"military base near {city} {state}"` (for military housing demand)

**Midterm rental demand drivers near property:**
- Hospitals (travel nurses — 13-week contracts)
- Military bases (PCS moves, TDY assignments)
- Universities (visiting professors, grad students)
- Corporate offices (relocations, project assignments)
- Construction projects (traveling workers)
- Insurance claims (displaced families — 3-12 months)

**Data to capture:**
- Monthly furnished rental rate
- Typical lease length (1-6 months)
- Occupancy rate for midterm
- Furniture cost estimate ($3,000-$8,000 for full setup)
- Premium over unfurnished long-term rent (typically 30-75%)

### Step 5: Analyze Co-Living / Rent-by-the-Room

Calculate room rental potential:

**Per-room rent estimation:**
- Research individual room rental rates in the area
- Search: `"room for rent {city} {state} {zip code}"`
- Search: `"co-living {city} {state}"`

**Calculate:**
- Number of rentable bedrooms
- Estimated per-room rent (typically 60-80% of a 1BR apartment rate)
- Total gross rent if all rooms rented individually
- Shared utility cost structure
- Common area maintenance cost increase
- Higher management intensity factor (+5% of gross)
- Higher turnover/vacancy factor (+3-5%)

### Step 6: Build Strategy Comparison

Compare all strategies head-to-head:

| Metric | Long-Term | Section 8 | Midterm | STR (Airbnb) | Co-Living |
|--------|-----------|-----------|---------|--------------|-----------|
| Monthly Gross Revenue | | | | | |
| Vacancy Rate | | | | | |
| Operating Expenses | | | | | |
| Net Monthly Income | | | | | |
| Annual Net Income | | | | | |
| Startup Cost | | | | | |
| Management Intensity | | | | | |
| Tenant Quality Risk | | | | | |
| Regulatory Risk | | | | | |
| Scalability | | | | | |

**Expense adjustments by strategy:**
- **Long-term:** Baseline expenses. Lowest management intensity.
- **Section 8:** Similar to long-term. Add annual inspection prep. Guaranteed rent portion.
- **Midterm:** Add furniture ($3K-$8K upfront), utilities ($150-$300/mo), higher cleaning. 30-75% rent premium.
- **STR:** Add furniture, utilities, cleaning ($75-$150/turnover), supplies ($50-$100/mo), platform fees (3-5%), higher insurance, occupancy taxes. Highest revenue potential but highest expense and effort.
- **Co-Living:** Add shared utilities, higher maintenance, more frequent turnover per room, potentially higher insurance. Total rent often 30-50% higher than single-tenant.

### Step 7: Generate Recommendation

Score each strategy on a 1-5 scale across these dimensions:

| Dimension | Weight | Long-Term | Section 8 | Midterm | STR | Co-Living |
|-----------|--------|-----------|-----------|---------|-----|-----------|
| Net Income | 30% | | | | | |
| Ease of Management | 20% | | | | | |
| Reliability/Consistency | 20% | | | | | |
| Startup Cost | 15% | | | | | |
| Regulatory Safety | 15% | | | | | |
| **Weighted Score** | 100% | | | | | |

**Recommendation format:**
- PRIMARY strategy (highest weighted score)
- BACKUP strategy (second highest)
- Why the primary wins
- What would change the recommendation (e.g., "If STR regulations loosen, STR becomes the clear winner")
- Specific action steps to implement the recommended strategy

### Step 8: Save Analysis

Save to:
```
~/Desktop/lindaai/output/rental-analyses/{address-or-area-slug}-{date}.md
```

## Output Format

```markdown
# Rental Market Analysis: {Address or Area}
**Date:** {date}
**Analyzed by:** LindaAI 🤠

---

## Property / Area Overview
| Detail | Value |
|--------|-------|
| Address/Area | |
| Property Type | |
| Beds/Baths | |
| Square Footage | |
| Purchase Price | |
| Year Built | |

## Long-Term Rental Market
### Rent Comps
[Comp table]

### Market Summary
- Median rent for {beds}BR: $X,XXX
- Rent range: $X,XXX - $X,XXX
- Vacancy rate: X%
- Rent trend: [Increasing/Flat/Declining]
- Rent-to-price ratio: X.XX%

## Section 8 / Fair Market Rent
[FMR table by bedroom count]
- Waitlist status: [Open/Closed]
- Payment reliability: [Assessment]

## Short-Term Rental (Airbnb/VRBO)
- Average daily rate: $XXX
- Estimated occupancy: XX%
- Estimated monthly gross: $X,XXX
- STR legal status: [Legal/Restricted/Banned]
- Permit required: [Yes ($XX) / No]
- Seasonality: [Notes]

## Midterm Rental (Furnished)
- Estimated monthly rate: $X,XXX
- Demand drivers: [List nearby hospitals, bases, etc.]
- Furniture startup cost: $X,XXX
- Premium over long-term: XX%

## Co-Living / Rent by the Room
- Rooms available: X
- Per-room rate: $XXX
- Total gross if full: $X,XXX
- Premium over single-tenant: XX%

## Strategy Comparison
[Full comparison table]

## Recommendation
**Primary Strategy: [Strategy Name]**
**Estimated Monthly Net: $X,XXX**

[Detailed reasoning]

### Implementation Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

---
🤠 *Generated by LindaAI* 🏇
```

## Example Usage

**User:** "What's the best rental strategy for a 4/2 house I'm buying at 1847 Oak Park Ave, Memphis TN 38127? Purchase price is $85,000."

**LindaAI researches and finds:**
- Long-term rent: $950-$1,100/mo for 4BR in 38127
- Section 8 FMR: $1,147 for 4BR in Shelby County
- STR: Memphis allows with permit ($500/yr). ADR ~$95, occupancy ~55%. Monthly gross ~$1,568.
- Midterm: Regional One Health and St. Jude nearby. Furnished 4BR ~$1,600-$2,000/mo.
- Co-living: 4 rooms at $400/each = $1,600/mo gross, but 38127 is not a strong co-living market.

**Recommendation:** "Section 8 is your primary strategy. At $1,147/mo guaranteed by HUD against a $85K purchase price, that's a 1.35% rent-to-price ratio. Consistent payment, long-term tenants, and minimal vacancy. Midterm is your backup if you're willing to furnish -- the hospital proximity supports travel nurse demand at $1,600-$2,000/mo. STR is viable but the 55% occupancy in this zip makes it volatile. Co-living doesn't match the neighborhood demographics."

## Error Handling

- **If the user does not provide a property address or area:** Ask: "What property address or area do you want me to analyze? I need at least a city and state, or a specific address for the most accurate data."
- **If the user does not provide property type or bedroom count:** Ask: "How many bedrooms and bathrooms? And what's the property type (single family, duplex, condo, etc.)? This significantly affects rental estimates."
- **If WebSearch is unavailable:** Inform: "Web search is not available. I can discuss rental strategy concepts and provide general guidance, but I cannot pull current market data, FMR rates, or Airbnb comps. Try again later for a data-backed analysis."
- **If web search returns no rental data for the specific area:** Expand the search radius (from the immediate zip code to the city level) and note: "I couldn't find rental comps for the exact area. Using city-wide data as a proxy — actual rents in your specific neighborhood may differ. Verify with local property managers."
- **If HUD Fair Market Rent data cannot be found:** Note: "I couldn't find current FMR data for this county. Check huduser.gov directly for the latest Fair Market Rent tables." Proceed with other strategies.
- **If STR regulations cannot be determined:** Flag as a critical unknown: "I could not confirm whether short-term rentals are legal in this jurisdiction. DO NOT pursue an STR strategy until you verify local regulations, permits, and zoning. Check with the city planning department."
- **If the output directory does not exist:** Create `~/Desktop/lindaai/output/rental-analyses/` automatically before saving.
- **If the user asks about a strategy that does not apply to their property type (e.g., co-living for a 1-bedroom):** Skip that strategy and note: "Co-living/rent-by-the-room is not applicable for a 1-bedroom property. Analysis covers the remaining strategies."
- **If midterm rental demand drivers (hospitals, bases, etc.) cannot be found near the property:** Note: "I did not find strong midterm rental demand drivers (hospitals, military bases, universities) near this property. Midterm may still work for insurance displacement or corporate housing, but demand will be lower than properties near these anchors."


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
