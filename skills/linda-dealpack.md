---
name: linda-dealpack
description: This skill should be used when the user asks to "create marketing for a deal", "build a deal package", "marketing package", "deal flyer", "one-pager for a deal", "social media post for a property", "investor pitch", "listing description", "write a deal summary", "email blast for a deal", "property marketing", "market this deal", "create deal materials", "deal presentation", "buyer marketing", "investor marketing", "wholesale deal marketing", "flip marketing", "creative finance marketing", "property listing copy", "IG post for a deal", "Facebook post for a property", "deal promotion", "blast this deal out", "make a deal flyer", or any request involving generating marketing content to sell, assign, or promote a real estate deal to buyers, investors, or the public.
version: 1.0.0
---

# Deal Marketing Package

## Overview

Generates a complete set of marketing materials for any real estate deal. The user provides property details and deal terms, and LindaAI creates everything needed to market the deal: a professional one-page deal summary, social media posts for Instagram, Facebook, and X (Twitter), an email blast template, an investor pitch narrative, and a polished listing description. All materials are tailored to the deal type (wholesale, creative finance, rental, flip, subject-to, seller finance) and the target audience (cash buyers, investors, owner-occupants, landlords). Everything is formatted and ready to copy-paste, post, or send. Saved to a deal-specific folder for easy access.

## When This Skill Applies

- User has a deal and needs marketing materials created
- User asks for a "one-pager" or "deal summary" for a property
- User wants social media posts for a deal
- User needs an email blast to send to a buyer list
- User wants an investor pitch or presentation
- User asks for listing copy or property description
- User says "market this deal" or "blast this out"
- User needs wholesale deal marketing
- User wants creative finance deal marketing
- User has a property to promote and wants all channels covered

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

### Step 0: Gather Deal Information

Parse what the user provided. Required inputs:

| Input | Required | Example |
|-------|----------|---------|
| Property address | Yes | 4521 Elm St, Dallas TX 75216 |
| Property type | Yes | SFR, duplex, condo, land |
| Beds / baths | Yes | 3/2 |
| Square footage | Helpful | 1,450 sqft |
| Lot size | Helpful | 0.18 acres |
| Year built | Helpful | 1985 |
| Purchase/asking price | Yes | $165,000 |
| Estimated ARV or market value | Helpful | $210,000 |
| Estimated rents | Helpful | $1,650/mo |
| Deal type | Yes | Wholesale, flip, buy-and-hold, creative finance, subject-to, seller finance |
| Rehab estimate | If applicable | $25,000 |
| Financing terms | If creative | $0 down, 5% interest, 30yr amort, 5yr balloon |
| Target audience | Helpful | Cash buyers, investors, owner-occupants, landlords |
| Unique selling points | Helpful | New roof, large backyard, Section 8 ready |
| Photos available | Optional | User can provide photo paths |
| Contact info for inquiries | Yes | Phone, email, or "DM me" |

If key details are missing, ask. Don't guess on price, address, or deal terms.

### Step 1: Create One-Page Deal Summary

This is the cornerstone document. Professional, scannable, fact-forward.

**Structure:**

```
INVESTMENT OPPORTUNITY
[Property Address]
[City, State ZIP]

━━━━━━━━━━━━━━━━━━━━━━━━━

PROPERTY DETAILS
Type:           [SFR / Duplex / etc.]
Beds/Baths:     [X/X]
SqFt:           [X,XXX]
Lot Size:       [X.XX acres]
Year Built:     [XXXX]
Condition:      [Turnkey / Light Rehab / Full Gut]

━━━━━━━━━━━━━━━━━━━━━━━━━

DEAL TERMS
Asking Price:       $XXX,XXX
ARV / Market Value: $XXX,XXX
Estimated Rehab:    $XX,XXX
Estimated Rent:     $X,XXX/mo

[If creative finance:]
Financing Available: [Seller finance / Subject-to / Wrap]
Down Payment:       $XX,XXX
Interest Rate:      X.XX%
Monthly Payment:    $X,XXX
Term:              XX years / XX month balloon

━━━━━━━━━━━━━━━━━━━━━━━━━

THE NUMBERS
Monthly Rent:           $X,XXX
Monthly Payment:        $X,XXX
Estimated Expenses:     $XXX
Monthly Cash Flow:      $XXX
Cash-on-Cash Return:    XX.X%
Cap Rate:              X.X%

━━━━━━━━━━━━━━━━━━━━━━━━━

WHY THIS DEAL
• [Bullet 1 — strongest selling point]
• [Bullet 2 — financial advantage]
• [Bullet 3 — location/market advantage]
• [Bullet 4 — unique feature]

━━━━━━━━━━━━━━━━━━━━━━━━━

COMPS / MARKET DATA
[2-3 comparable sales or rental comps if available]

━━━━━━━━━━━━━━━━━━━━━━━━━

CONTACT
[Name]
[Phone]
[Email]
[Website — e.g., sellfi.io]
```

### Step 2: Create Social Media Posts

Generate platform-specific posts. Each post should be self-contained and designed for engagement.

**Instagram Post (Feed)**

Format: Strong hook line, key deal details, call to action. Use line breaks for readability. Include relevant hashtags.

```
[HOOK LINE — attention-grabbing, deal-specific]

[Property type] in [City, State]
[Beds/Baths] | [SqFt] sqft | Built [Year]

[Deal type-specific pitch — 2-3 sentences]

[Key numbers — price, rent, cash flow, returns]

[Call to action]

[10-15 relevant hashtags]
```

Example hooks by deal type:
- Wholesale: "DEAL ALERT: Under-market property just hit my desk."
- Cash flow: "Cash flow from day one. Here's the breakdown."
- Creative finance: "No bank needed. Seller financing available."
- Subject-to: "Take over payments. No qualifying."
- Flip: "Built-in equity. $XX,XXX spread on this one."
- BRRRR: "Buy, rehab, rent, refi, repeat. This one checks every box."

**Instagram Story / Reel Script (optional)**

Short-form script if user wants video content:
```
[Opening hook — 3 seconds]
"I just locked up a deal in [City] that you need to see."

[The deal — 10 seconds]
"[Property type], [beds/baths], asking [price]."
"Rents for [rent]. That's [cash flow] a month cash flow."

[The punch — 5 seconds]
"[Unique selling point or creative finance hook]"

[CTA — 3 seconds]
"DM me 'DEAL' for the full breakdown."
```

**Facebook Post**

Longer format. More narrative. Groups-friendly.

```
[HOOK — question or bold statement]

I've got a [property type] in [City, State] that [primary selling point].

Here's the quick breakdown:
[Address]
[Beds/Baths] | [SqFt] sqft
Asking: $XXX,XXX
[Rent / ARV / Cash flow details]

[2-3 sentences on why this is a good deal — speak to the target buyer]

[Deal type specifics — financing terms, assignment fee, etc.]

[Call to action — DM, comment, call]

[3-5 relevant hashtags]
```

**X (Twitter) Post**

Concise. Punchy. Numbers-forward.

```
[Deal type] alert — [City, State]

[Property type] | [Beds/Baths] | $XXX,XXX
Rent: $X,XXX/mo | Cash flow: $XXX/mo
[Key metric: XX% CoC / $XXK equity / creative terms]

[One-line hook or unique angle]

DM for details.

#RealEstate #[DealType] #[City] #Investing
```

### Step 3: Create Email Blast

Professional email template for buyer list distribution.

```
Subject: [DEAL ALERT] [Property Type] in [City, State] — [Key Hook]

---

Hi [First Name / Investor],

New deal just hit my desk and I wanted to get it to you first.

**[Property Address]**
[City, State ZIP]

**Property Details:**
• Type: [SFR / Duplex / etc.]
• Beds/Baths: [X/X]
• SqFt: [X,XXX]
• Year Built: [XXXX]
• Condition: [Turnkey / Needs Work]

**Deal Terms:**
• Price: $XXX,XXX
• [ARV: $XXX,XXX / Estimated Rent: $X,XXX/mo]
• [Financing details if creative]

**Why This Deal:**
[2-3 bullet points — strongest selling points]

**The Numbers:**
[Cash flow, returns, equity — whatever matters most for this deal type]

[If wholesale: "Assignment fee: $XX,XXX. Proof of funds required."]
[If seller finance: "Terms: $XX,XXX down, X.XX% interest, XX-year amortization."]
[If rental: "Cash-on-cash: XX.X%. Cap rate: X.X%. Cash flow positive from day 1."]

This one won't last. If you're interested, reply to this email or call/text me at [phone number].

Talk soon,
[Name]
[Phone]
[Email]
[Website]
```

### Step 4: Create Investor Pitch

A narrative pitch for presenting to investors, partners, or JV prospects.

```markdown
## Investment Opportunity: [Address]

### The Opportunity
[2-3 paragraphs telling the story of this deal. Why does it exist? Why is it
undervalued? What's the play? This should read like you're sitting across the
table from an investor explaining why this is worth their time and money.]

### Market Context
[1-2 paragraphs on the local market. Why is this area good for this strategy?
Population growth, job market, rent growth, supply constraints, etc.
Pull from web search if available.]

### The Numbers
[Clean financial summary — purchase price, total investment, projected returns,
timeline to realize gains, exit strategy]

### Risk Mitigation
[Address the obvious risks and how they're mitigated:
- What if rents don't hit projections? (conservative underwriting)
- What if vacancy is higher? (break-even analysis)
- What if the market dips? (bought below market, equity cushion)
- What if repairs cost more? (contingency built in)]

### Exit Strategies
[Multiple paths to profit:
1. Primary exit: [hold for cash flow, flip, refinance, etc.]
2. Backup exit: [sell at market, assign contract, lease-option, etc.]
3. Worst case: [even in downside scenario, here's the floor]]

### Ask
[What you need from the investor:
- Capital: $XX,XXX
- Timeline: XX months
- Return projection: XX%
- Structure: [JV split, preferred return, equity share, etc.]]
```

### Step 5: Create Listing Description

Polished MLS-style listing description. Two versions: short (200 words) and long (400+ words).

**Short version (social media, quick posts):**
```
[Compelling opening line that captures the property's best feature]

[Key details: beds/baths, sqft, lot, year built]

[Top 3-4 features in flowing prose, not a list]

[Location highlights: proximity to schools, shopping, transit, employers]

[Call to action with urgency]
```

**Long version (MLS, listing sites, deal packages):**
```
[Evocative opening paragraph — paint a picture, create desire]

[Detailed property description — room by room flow, upgrades, materials,
 finishes. Be specific: "granite countertops" not "updated kitchen"]

[Outdoor space, lot, garage, parking description]

[Neighborhood and location paragraph — walkability, nearby amenities,
 commute times, school district]

[Investment angle paragraph if applicable — rental income, equity,
 development potential]

[Closing paragraph with urgency and call to action]
```

### Step 6: Save Everything

Create a deal-specific folder and save all materials:

```
~/Desktop/lindaai/output/deal-marketing/{address-slug}/
├── one-pager.md
├── social-media-posts.md
├── email-blast.md
├── investor-pitch.md
├── listing-description.md
└── README.md (index of all files)
```

## Output Format

All files are saved as markdown in the deal folder. The README.md serves as the index:

```markdown
# Deal Marketing Package: {Address}
**Created:** {date}

## Contents
1. **one-pager.md** — Professional one-page deal summary
2. **social-media-posts.md** — Posts for IG, FB, X (ready to copy-paste)
3. **email-blast.md** — Email template for buyer list
4. **investor-pitch.md** — Narrative pitch for investors/partners
5. **listing-description.md** — Short and long listing descriptions

## Deal Quick Reference
| Detail | Value |
|--------|-------|
| Address | |
| Price | |
| Deal Type | |
| Target Audience | |

---
🤠 *Generated by LindaAI* 🏇
```

## Example Usage

**User:** "Create a marketing package for this deal: 2847 Westfield Blvd, Indianapolis IN 46205. 3/2 brick ranch, 1,600 sqft, built 1955. I'm selling it seller-finance: $175,000, $10,000 down, 6% interest, 30-year amortization with a 7-year balloon. Rents for $1,500/mo. ARV is around $195,000. New roof 2024, updated kitchen, fenced yard. Target: investors and owner-occupants who can't get bank financing. Contact: Mike Davis, 555-123-4567, mike@sellfi.io"

**LindaAI creates the full package:**

- **One-pager** with all terms, numbers (cash flow of ~$385/mo for buyer), and selling points
- **Instagram post** with hook: "Own this home with just $10K down. No bank needed." + hashtags
- **Facebook post** targeting creative finance groups with full narrative
- **X post** punchy: "Seller finance deal - Indianapolis. 3/2 brick ranch, $175K. $10K down, 6%, 30yr. Rents $1,500/mo. New roof. DM for terms."
- **Email blast** for buyer list with urgency angle
- **Investor pitch** framing it as a passive income play with built-in equity
- **Listing descriptions** in short and long format

All saved to `~/Desktop/lindaai/output/deal-marketing/2847-westfield-blvd-indianapolis/`

## Error Handling

- **If the user does not provide a property address:** Ask: "What is the property address? I need it for the marketing materials."
- **If the user does not provide a purchase/asking price:** Ask: "What is the asking price or sale price? I can't build the numbers section without it."
- **If the user does not provide deal type (wholesale, seller finance, etc.):** Ask: "What type of deal is this? (Wholesale, seller finance, subject-to, buy-and-hold, flip, etc.) This determines how I position the marketing."
- **If the user does not provide contact info for inquiries:** Ask: "What contact info should I include on the marketing materials? (Phone, email, or 'DM me' for social posts)"
- **If the user provides incomplete property details (missing beds/baths, sqft):** Create materials with available info and note placeholders: "[BEDS/BATHS TBD]". Flag: "I'm missing some property details. Fill in beds/baths and square footage to strengthen the marketing package."
- **If the output directory does not exist:** Create `~/Desktop/lindaai/output/deal-marketing/{address-slug}/` automatically before saving files.
- **If a marketing package already exists for this address:** Ask: "Marketing materials already exist for this address. Should I overwrite them, or create a new version (e.g., `{address-slug}-v2/`)?"
- **If the user provides photos or photo paths:** Reference them in the media notes sections but do not embed images in the markdown files. Note: "I've referenced your photos in the media notes. Attach them when posting to social media or sending the email blast."
- **If deal numbers do not look attractive (negative cash flow, low returns):** Still create the marketing materials but adjust the angle. Focus on equity, appreciation, location, or creative financing advantages rather than cash flow. Flag to user: "The cash flow numbers are tight. I've angled the marketing toward {alternative selling point} instead."
- **If the user asks for formats not covered (e.g., video script, podcast talking points):** Adapt the investor pitch narrative into the requested format and note: "I adapted the investor pitch into a {format}. Review and adjust for the specific medium."


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
