---
name: linda-compete
description: This skill should be used when the user asks to "analyze competitors", "competitor analysis", "competitive landscape", "who are my competitors", "what's the competition like", "competitive research", "competitor breakdown", "who else does this", "compare us to competitors", "competitive intel", "find competitors", "competitor pricing", "how do we stack up", "market positioning", "SWOT analysis", "competitive audit", "who are we up against", "competitor review", "landscape analysis", "battle card", or wants to understand the competitive environment for any business, product, or market.
version: 1.0.0
---

# Competitor Analysis — Competitive Landscape Intelligence

## Overview

Competitor Analysis performs a structured investigation of the competitive landscape for any business, product, or market. LindaAI identifies direct and indirect competitors, maps their pricing, features, positioning, strengths, and weaknesses, and produces an actionable competitive intelligence document. The output highlights gaps you can exploit, threats to watch, and strategic positioning recommendations. LindaAI pulls it all from current web data so you know exactly who you are up against.

## When This Skill Applies

- User says "analyze my competitors" or "competitor analysis"
- User says "who are my competitors?" or "who else does this?"
- User says "competitive landscape" or "competitive research"
- User says "how do we stack up against [competitor]?"
- User says "competitor pricing" or "what do they charge?"
- User says "SWOT analysis" or "competitive audit"
- User says "battle card" or "competitive intel"
- User mentions a specific competitor and wants to understand them
- User is launching a product and needs to know the landscape
- User asks "what makes us different?" or "what's our edge?"
- User says "find competitors for [product/service]"

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

### Step 1: Define the Competitive Frame

Determine from the user's request:

1. **The Business/Product:** What is being analyzed? (e.g., SellFi, TOP Wheels, T.O.P. Method Academy, or any other business)
2. **The Market:** What space does it operate in? (e.g., creative finance platforms, vehicle seller financing, online education)
3. **Known Competitors:** Has the user already named specific competitors?
4. **Analysis Depth:** Quick overview (top 5 competitors) or comprehensive (10-15+ with deep feature comparison)?
5. **Focus Area:** All-around analysis or focused on pricing, features, marketing, or positioning?

If analyzing the user's own business, check the brain for existing knowledge:
- `brain/research/competitor-intelligence.md` (if it exists)
- `brain/knowledge-base/sellfi-ecosystem/` (for SellFi context)
- `brain/projects/` (for current project details)

### Step 2: Identify Competitors

> 🤠 "Hold tight -- heading over yonder to gather up the details."

Run targeted web searches to find competitors across three tiers:

**Tier 1 — Direct Competitors** (same product/service, same target customer)
- Search: "[product type] platforms" or "[service] companies"
- Search: "[product name] alternatives" or "[product name] competitors"
- Search: "best [product category] 2026"

**Tier 2 — Indirect Competitors** (different approach, same customer problem)
- Search: "[customer problem] solutions"
- Search: "how to [what the product does] without [product type]"

**Tier 3 — Emerging/Adjacent Competitors** (entering the space or could pivot in)
- Search: "[industry] startups 2025 2026"
- Search: "[adjacent industry] expanding into [target market]"

For each identified competitor, note:
- Company name and URL
- One-line description of what they do
- Why they are a competitor (direct, indirect, or emerging)

### Step 3: Research Each Competitor

For the top 5-10 competitors, investigate:

| Data Point | How to Find It |
|-----------|---------------|
| **Pricing** | Search "[company] pricing", visit their pricing page via WebFetch |
| **Features** | Search "[company] features", check their product pages |
| **Target Market** | Who do they market to? Check their homepage copy and about page |
| **Positioning** | What is their tagline/value prop? How do they describe themselves? |
| **Strengths** | What do reviews and users praise? Search "[company] reviews" |
| **Weaknesses** | What do users complain about? Search "[company] complaints" or "[company] vs" |
| **Funding/Scale** | Search "[company] funding" or "[company] revenue" for size context |
| **Marketing Approach** | Check their social media presence, content strategy, ad spend clues |
| **Technology** | What tech stack or approach? Any unique technical advantages? |
| **Recent Moves** | Search "[company] news 2026" for recent product launches or changes |

### Step 4: Build Comparison Frameworks

Create three core comparison assets:

#### A. Feature Comparison Matrix

```markdown
| Feature | Your Product | Competitor A | Competitor B | Competitor C |
|---------|-------------|-------------|-------------|-------------|
| Feature 1 | Yes | Yes | No | Partial |
| Feature 2 | Yes | No | Yes | Yes |
| Pricing (entry) | $X/mo | $Y/mo | $Z/mo | Free |
| Target Market | [Desc] | [Desc] | [Desc] | [Desc] |
| Unique Feature | [What] | [What] | [What] | [What] |
```

#### B. Positioning Map

Describe where each competitor sits along two key dimensions relevant to the market (e.g., price vs. feature depth, consumer vs. enterprise, self-serve vs. full-service):

```
High Price
    |
    |  [Enterprise Player A]     [Premium Player B]
    |
    |         [Mid-Market C]
    |
    |  [Budget Player D]    [YOUR PRODUCT - positioned here]
    |
Low Price
    Self-Serve ————————————————————————— Full-Service
```

#### C. SWOT for Each Major Competitor

For the top 3-5 direct competitors:

```markdown
### [Competitor Name]
| | Helpful | Harmful |
|---|---------|---------|
| Internal | **Strengths:** [list] | **Weaknesses:** [list] |
| External | **Opportunities:** [for them] | **Threats:** [to them] |
```

### Step 5: Identify Strategic Insights

Synthesize the research into actionable intelligence:

1. **Gaps in the Market:** What are competitors NOT doing that customers want?
2. **Your Competitive Advantages:** Based on the analysis, where does the user's product/service win?
3. **Threats to Watch:** Which competitors could become a problem? What moves could hurt the user?
4. **Pricing Insights:** Where is the user positioned relative to competitors? Is there a pricing opportunity?
5. **Positioning Recommendation:** How should the user differentiate? What messaging beats the competition?
6. **Quick Wins:** Tactical things the user can do right now to gain an edge

### Step 6: Compile the Document

```markdown
# Competitive Analysis: [Market/Product]

> **Date:** YYYY-MM-DD
> **Analyzed For:** [User's product/business name]
> **Market:** [The competitive space]
> **Competitors Analyzed:** [Count]

---

## Executive Summary

[3-5 bullet points. The most important takeaways for decision-making.]

---

## Competitive Landscape Overview

[1-2 paragraphs describing the overall competitive environment. How mature is the market? Is it crowded or open? Growing or contracting?]

## Competitor Profiles

### 1. [Competitor Name] — [One-line description]
- **URL:** [website]
- **Founded/Size:** [Year, employee count or funding if available]
- **What They Do:** [2-3 sentences]
- **Pricing:** [Tiers and prices]
- **Target Customer:** [Who they serve]
- **Strengths:** [Bullet list]
- **Weaknesses:** [Bullet list]
- **Key Differentiator:** [What makes them unique]
- **Threat Level:** Low / Medium / High

[Repeat for each competitor]

## Feature Comparison Matrix

[Table comparing key features across all competitors]

## Pricing Comparison

| Competitor | Entry Price | Mid Tier | Top Tier | Free Option |
|-----------|------------|---------|---------|-------------|
| [Name] | $X/mo | $Y/mo | $Z/mo | Yes/No |

## Positioning Map

[Visual or text description of where each competitor sits]

## Strategic Insights

### Market Gaps (Opportunities)
1. [Gap 1 — what no one is doing well]
2. [Gap 2]
3. [Gap 3]

### Your Competitive Advantages
1. [Advantage 1]
2. [Advantage 2]

### Threats to Watch
1. [Threat 1]
2. [Threat 2]

### Positioning Recommendation
[How should the user position against this landscape? What messaging wins?]

### Quick Wins
1. [Tactical action the user can take immediately]
2. [Tactical action]
3. [Tactical action]

---

## Sources

1. [Source Title](URL) — accessed YYYY-MM-DD
...

---

🤠 *Generated by LindaAI* 🏇
*Markets shift -- revisit this analysis quarterly.*
```

### Step 7: Save and Report

Save to: `brain/research/{product-or-market}-competitive-analysis.md`

If a competitor analysis file already exists for this product, either update it or create a versioned file with the current date.

Present to the user:
- Executive summary (the key competitive takeaways)
- The biggest opportunity and biggest threat
- Where the document was saved
- Recommendation for how often to refresh this analysis

## Quality Standards

1. **Real data, not assumptions.** Every competitor profile is based on what was actually found online, not guesses.
2. **Pricing verified.** If pricing is not publicly available, note "pricing not public — contact required" rather than guessing.
3. **Fair assessment.** Do not trash competitors or inflate the user's advantages. Honest analysis is more useful than cheerleading.
4. **Actionable.** The document must answer "so what do I DO with this information?"
5. **Current.** Prioritize 2025-2026 data. Flag if a competitor's info might be outdated.
6. **Sourced.** Every factual claim includes a source URL.

## Output Format

A single comprehensive markdown file (typically 2,000-5,000 words for a full analysis) saved to `brain/research/` with competitor profiles, comparison tables, positioning insights, and source citations.

## Example Usage

**User:** "Competitor analysis for SellFi"

**AI executes:**
- Identifies competitors in creative finance platforms, vehicle seller financing, and dealership software
- Profiles 8-10 competitors with pricing, features, strengths, weaknesses
- Builds feature comparison matrix and positioning map
- Identifies market gaps SellFi can exploit
- Saves to `brain/research/sellfi-competitive-analysis.md`

**User:** "Who are the competitors for an AI agent OS product?"

**AI executes:**
- Searches AI agent platforms, AI operating systems, AI assistants for business
- Profiles players like Lindy, Relevance AI, CrewAI, AgentGPT, AutoGen, etc.
- Compares pricing, capabilities, target markets
- Identifies positioning opportunities
- Saves to `brain/research/ai-agent-os-competitive-analysis.md`

**User:** "How does TOP Wheels compare to Carvana and Vroom?"

**AI executes:**
- Deep dives on Carvana, Vroom, and other online vehicle platforms
- Compares business models (traditional vs. creative finance)
- Highlights where TOP Wheels' seller finance model has advantages
- Saves to `brain/research/top-wheels-competitive-analysis.md`

## Error Handling

- **If WebSearch is unavailable or returns errors:** Inform the user: "Web search is not available right now. LindaAI can provide a competitive analysis based on training data, but pricing and recent developments may not be current. Want me to proceed?"
- **If web search returns no pricing data for a competitor:** Note in the profile: "Pricing not publicly available — requires contacting their sales team or signing up for a demo." Do not guess or fabricate pricing.
- **If the user does not specify what product or market to analyze:** Ask: "What product, service, or market do you want LindaAI to scout the competitive landscape for? For example: 'creative finance platforms', 'AI OS products', or 'online course platforms'."
- **If no competitors can be found (very niche market):** Report honestly: "I could not find direct competitors for this specific niche. This could mean: (1) it's a whitespace opportunity, (2) the market uses different terminology, or (3) competitors exist but have low online visibility. I identified {N} adjacent or indirect competitors instead." Then show indirect competitors.
- **If a competitor analysis file already exists:** Ask: "A competitive analysis for '{market}' already exists (dated {date}). Should I update the existing file with fresh data, or create a new version?"
- **If `brain/research/` directory does not exist:** Create it automatically before saving.
- **If the user names a specific competitor but it cannot be found online:** Note: "I could not find reliable information on '{competitor name}'. They may be very new, very small, or operating under a different name. If you have a URL or more details, share them and I'll dig deeper."
- **If WebFetch fails on a competitor's website:** Note in that competitor's profile: "Could not access {competitor}.com for detailed feature/pricing data. Analysis based on search snippets and third-party reviews." Continue with available data.

🤠 *Generated by LindaAI* 🏇


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
