---
name: property-research
description: This skill should be used when the user asks to "research a property", "look up this address", "property research", "what can you find on this property", "pull property data", "property dossier", "due diligence on a property", "who owns this property", "when was this property last sold", "what's the tax assessment", "property details", "neighborhood analysis", "school ratings near", "flood zone check", "crime stats for area", "property history", "comps for this property", "comparable sales", "what's this property worth", "estimated value", "property profile", "deep dive on this address", or any request involving gathering comprehensive data about a specific property address.
version: 1.0.0
---

# Property Research

## Overview

Performs a comprehensive deep dive on any property address. Uses web search to compile everything available about a property into a single research dossier: last sale price and date, estimated current value, tax assessment, lot size, year built, bedrooms/baths, square footage, any recent or current listings, neighborhood demographics, school ratings, crime statistics, flood zone information, nearby amenities, and comparable sales. This is the research you do before making an offer, before a meeting with a seller, or before presenting a deal to a buyer or investor. LindaAI pulls it all together in one place, sourced and cited.

## When This Skill Applies

- User provides a property address and wants to know everything about it
- User asks "what can you find on this property?"
- User wants pre-offer due diligence research
- User asks about property value, tax records, or sale history
- User wants comparable sales for an address
- User asks about neighborhood quality, schools, or crime
- User needs a property profile to present to a buyer or investor
- User says "research this address" or "pull up property data"
- User wants flood zone, HOA, or zoning information
- User is preparing for a seller meeting and needs property intel

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

### Step 0: Parse the Address

Extract and standardize:
- Street address
- City
- State
- Zip code
- County (look up if not provided)

If the user provides a partial address, use WebSearch to find the full address.

### Step 1: Property Details & Records

> 🤠 "Hold tight — heading over yonder to gather up the details."

Search for core property data:

**Search queries:**
- `"{full address}" property records`
- `"{full address}" Zillow`
- `"{full address}" Redfin`
- `"{full address}" Realtor.com`
- `"{full address}" county assessor`
- `"{full address}" tax records`
- `"{county} {state} property appraiser {street address}"`

**Data to capture:**

| Detail | Source | Value |
|--------|--------|-------|
| Full legal address | County records | |
| Property type | Assessor / Zillow | SFR, multi-family, condo, etc. |
| Bedrooms | Listings / assessor | |
| Bathrooms | Listings / assessor | |
| Square footage | Assessor | |
| Lot size | Assessor | |
| Year built | Assessor | |
| Stories | Assessor / listing | |
| Garage | Assessor / listing | |
| Pool | Assessor / listing | |
| Construction type | Assessor | Frame, block, brick, etc. |
| Roof type | Assessor | Shingle, tile, metal, etc. |
| Heating/cooling | Assessor / listing | Central, window, none |
| Zoning | County / city | Residential, commercial, mixed |
| Parcel number / APN | Assessor | |
| Legal description | Assessor | |

### Step 2: Valuation & Sale History

**Search queries:**
- `"{full address}" sold price history`
- `"{full address}" Zestimate`
- `"{full address}" estimated value {year}"`
- `"{county} {state} recorder deeds {street address}"`

**Data to capture:**

| Date | Event | Price | Buyer/Seller | Source |
|------|-------|-------|-------------|--------|
| | Last sale | | | |
| | Previous sale | | | |
| | Current listing | | | |
| | Tax assessed value | | | |
| | Zillow Zestimate | | | |
| | Redfin Estimate | | | |

**Calculate:**
- Annual appreciation rate from last sale to current estimate
- Price per square foot vs. area average
- Assessment-to-market ratio

### Step 3: Tax Information

**Search queries:**
- `"{full address}" property tax amount`
- `"{county} {state} property tax rate"`
- `"{full address}" tax assessment {year}"`

**Data to capture:**

| Tax Detail | Value |
|-----------|-------|
| Annual property tax | |
| Tax assessed value (land) | |
| Tax assessed value (improvement) | |
| Tax assessed value (total) | |
| Effective tax rate | |
| Exemptions (homestead, etc.) | |
| Tax year | |
| Any delinquent taxes | |
| Special assessments | |

### Step 4: Current/Recent Listings

**Search queries:**
- `"{full address}" for sale`
- `"{full address}" for rent`
- `"{full address}" listing history`
- `"{full address}" MLS"`

**Data to capture:**
- Is it currently listed? (for sale or rent)
- Current list price / rent price
- Days on market
- Price changes (reductions = motivated seller signal)
- Listing agent and brokerage
- Listing photos or description highlights
- Previous listing attempts (expired, withdrawn = potential motivation)

### Step 5: Neighborhood Analysis

**Search queries:**
- `"{zip code} neighborhood demographics"`
- `"{city} {state} {neighborhood name} livability"`
- `"AreaVibes {city} {state} {zip code}"`
- `"Niche.com {zip code} review"`
- `"{zip code} median household income"`
- `"{zip code} population growth"`

**Data to capture:**

| Neighborhood Metric | Value | Rating |
|--------------------|-------|--------|
| Median household income | | |
| Median home value | | |
| Population | | |
| Population growth trend | | |
| Livability score | | |
| Cost of living index | | |
| Walkability score | | |
| Owner-occupied vs. renter % | | |
| Median age | | |

### Step 6: School Ratings

**Search queries:**
- `"schools near {full address}" ratings`
- `"GreatSchools {city} {state} {zip code}"`
- `"{zip code} school district rating"`

**Data to capture:**

| School | Type | Grade Range | Rating | Distance |
|--------|------|-------------|--------|----------|
| | Elementary | | /10 | |
| | Middle | | /10 | |
| | High | | /10 | |

- School district name and overall rating
- Note: School ratings directly impact property values and rental demand

### Step 7: Crime & Safety

**Search queries:**
- `"crime rate {zip code} {year}"`
- `"CrimeGrade {zip code}"`
- `"{city} {state} crime statistics {neighborhood}"`
- `"NeighborhoodScout {zip code} crime"`

**Data to capture:**

| Crime Metric | Value | vs. National Average |
|-------------|-------|---------------------|
| Overall crime grade | | |
| Violent crime rate | | Above/Below |
| Property crime rate | | Above/Below |
| Crime trend | | Increasing/Decreasing/Stable |
| Sex offender count (0.5 mi) | | |

### Step 8: Flood Zone & Environmental

**Search queries:**
- `"FEMA flood zone {full address}"`
- `"flood map {full address}"`
- `"{full address}" flood zone`
- `"{county} {state} flood zone map"`

**Data to capture:**

| Environmental Factor | Status |
|---------------------|--------|
| FEMA flood zone | Zone X (minimal) / A / AE / V / VE |
| Flood insurance required | Yes/No |
| Estimated flood insurance cost | |
| Wildfire risk | Low/Medium/High |
| Earthquake risk | Low/Medium/High |
| Environmental hazards nearby | |
| Superfund sites nearby | |

### Step 9: Comparable Sales

**Search queries:**
- `"recently sold homes near {full address}" {year}`
- `"comparable sales {zip code} {bedrooms} bedroom"`
- `"Redfin sold {city} {state} {zip code} {bedrooms} bed"`

**Build comp table:**

| # | Address | Beds/Baths | SqFt | Sale Price | $/SqFt | Sale Date | Distance |
|---|---------|------------|------|-----------|--------|-----------|----------|
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |

**Comp analysis:**
- Average sale price of comps
- Average price per square foot
- Subject property estimated value based on comps
- How subject compares (above/below market)

### Step 10: Compile the Dossier

Assemble all data into a formatted property research dossier and save it.

Save to:
```
~/Desktop/lindaai/output/property-research/{address-slug}-{date}.md
```

## Output Format

```markdown
# Property Research Dossier: {Address}
**Date:** {date}
**Compiled by:** LindaAI 🤠

---

## Property Summary
| Detail | Value |
|--------|-------|
| Address | |
| Property Type | |
| Beds / Baths | |
| Square Footage | |
| Lot Size | |
| Year Built | |
| Zoning | |
| Parcel / APN | |

## Valuation
| Estimate Source | Value |
|----------------|-------|
| Last Sale ({date}) | $XXX,XXX |
| Tax Assessed Value | $XXX,XXX |
| Zillow Zestimate | $XXX,XXX |
| Redfin Estimate | $XXX,XXX |
| Comp-Based Estimate | $XXX,XXX |
| **Estimated Market Value** | **$XXX,XXX** |

## Sale History
[Sale history table]

## Tax Information
[Tax detail table]

## Current Listing Status
[Active listing details or "Not currently listed"]

## Comparable Sales
[Comp table with analysis]

## Neighborhood Profile
[Demographics, income, livability scores]

## Schools
[School ratings table]

## Crime & Safety
[Crime stats table]

## Flood Zone & Environmental
[Environmental risk table]

## Investment Snapshot
| Metric | Value |
|--------|-------|
| Price/SqFt vs. Area Average | |
| Estimated Rent Range | |
| Gross Rent-to-Price Ratio | |
| Annual Property Tax | |
| School District Quality | |
| Crime Level | |
| Flood Risk | |

## Key Findings & Flags
- [Positive finding 1]
- [Positive finding 2]
- [Risk/concern 1]
- [Risk/concern 2]

## Sources
- [URL 1]
- [URL 2]
- [URL 3]

---
🤠 *Generated by LindaAI* 🏇
```

## Example Usage

**User:** "Research 3221 Brighton St, Baltimore MD 21216"

**LindaAI runs all research steps and compiles:**

- **Property:** 3BR/1BA, 1,200 sqft, built 1925, row home, lot 1,440 sqft
- **Last sale:** $47,000 in 2019
- **Tax assessed:** $52,000 (land: $8,000 / improvement: $44,000)
- **Zillow Zestimate:** $68,000
- **Taxes:** $1,248/yr (2.4% effective rate)
- **Listing status:** Not currently listed. Last listed in 2019 at $54,900, sold at $47,000.
- **Comps:** 5 recent sales nearby, average $58,000 ($48/sqft)
- **Schools:** 3/10 elementary, 2/10 middle, 3/10 high (below average)
- **Crime:** Grade D+, violent crime 2.1x national average, property crime 1.8x
- **Flood zone:** Zone X (minimal risk), no flood insurance required
- **Key flags:** Below-average schools and higher crime = lower appreciation but higher cap rates. Strong Section 8 market. Rent estimate $1,000-$1,150/mo = excellent rent-to-price ratio.

**User:** "Now run a deal analysis on it" (triggers deal-analyzer skill with this data pre-loaded)

## Error Handling

- **If the user does not provide a full address:** Ask: "I need a complete property address (street, city, state, zip) for accurate research. What is the full address?"
- **If the user provides a partial address:** Use WebSearch to attempt to resolve the full address. If multiple matches, present options: "I found multiple properties matching that description: {list}. Which one?"
- **If WebSearch is unavailable:** Inform: "Web search is not available. I cannot pull property records, tax data, or neighborhood information without it. Try again later, or provide the data manually and I'll organize it into a dossier format."
- **If web search returns no property records for the address:** Try alternative search queries (county assessor, different listing sites). If still no results: "I couldn't find public records for this address. It may be a new construction, a rural property with limited online records, or the address may be incorrect. Try checking the county assessor's website directly."
- **If comparable sales data is sparse (fewer than 3 comps):** Expand the search radius and timeframe. Note: "Only {N} comparable sales found within 0.5 miles / 6 months. I expanded to {radius} / {timeframe} to find {N} total comps. Accuracy is lower with fewer comps."
- **If flood zone data cannot be determined:** Flag as an open item: "Could not determine the FEMA flood zone for this property. Check fema.gov/flood-maps directly. If the property is in a flood zone, factor in flood insurance costs ($500-$3,000+/year)."
- **If the output directory does not exist:** Create `~/Desktop/lindaai/output/property-research/` automatically before saving.
- **If school, crime, or neighborhood data is unavailable for the area:** Note each gap: "School ratings not available for this area" or "Crime data not found for this zip code." Proceed with whatever data is available rather than blocking the entire dossier.
- **If a property research dossier already exists for this address:** Ask: "A property dossier for this address already exists (dated {date}). Should I refresh it with current data, or keep the existing one?"
- **If WebFetch fails on county assessor or listing sites:** Note: "Could not access {site} for detailed data. Results are based on search snippets and other available sources." Continue with available data.


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
