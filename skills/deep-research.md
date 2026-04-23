---
name: deep-research
description: This skill should be used when the user asks to "research", "deep dive", "look into", "find out about", "investigate", "deep research", "research report", "find data on", "what's the market for", "market research", "industry analysis", "trend analysis", "find statistics", "research this topic", "compile research on", "I need to understand", "give me a breakdown of", "analyze this market", "what do we know about", "dig into", "explore this topic", "research brief", "intelligence report", or wants a comprehensive, web-sourced research document on any topic.
version: 1.0.0
---

# Deep Research — Comprehensive Topic Research & Analysis

## Overview

Deep Research is LindaAI's intelligence-gathering workhorse — a thorough investigation of any topic using web search to find current data, statistics, trends, competitors, market sizing, expert opinions, and key insights. It compiles everything into a well-organized, citation-rich markdown research document saved to the brain/research/ directory. This is not surface-level Googling — LindaAI runs structured, multi-angle research that produces an actionable intelligence document.

## When This Skill Applies

- User says "research [topic]" or "deep dive on [topic]"
- User says "look into [something]" or "find out about [something]"
- User says "what's the market for [X]?"
- User says "give me a breakdown of [industry/topic]"
- User asks for statistics, trends, or data on a subject
- User says "I need to understand [topic] before making a decision"
- User says "compile research on [topic]"
- User says "intelligence report on [topic]"
- User says "dig into [topic]" or "investigate [topic]"
- User wants current, web-sourced information (not just AI knowledge)
- User needs data to make a business decision
- User asks "what do we know about [X]?"

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

### Step 1: Define the Research Scope

Parse the user's request to determine:

1. **Core Topic:** The primary subject to research
2. **Research Angle:** What perspective matters? (market size, competitors, trends, how-to, risks, opportunities)
3. **Depth Level:** Quick brief (1-2 pages) or deep dive (5-10 pages)?
4. **Decision Context:** Why does the user need this? What decision will it inform?
5. **Time Sensitivity:** Is current data critical, or is evergreen info acceptable?

If the user did not specify, default to deep dive with all angles.

### Step 2: Build the Research Framework

Structure the investigation around these dimensions (include all that are relevant):

| Dimension | What to Find |
|-----------|-------------|
| Market Overview | Size, growth rate, key players, TAM/SAM/SOM |
| Current State | What is happening right now in this space |
| Key Trends | Where is this heading? What is changing? |
| Major Players | Who are the leaders? What are they doing? |
| Data & Statistics | Hard numbers, percentages, dollar figures |
| Opportunities | Gaps, underserved segments, whitespace |
| Risks & Challenges | What could go wrong? What are the barriers? |
| Expert Opinions | What are thought leaders saying? |
| Case Studies | Real examples of success or failure |
| Actionable Takeaways | What should the user DO with this information? |

### Step 3: Execute Web Research

> 🤠 "Hold tight — heading over yonder to gather up the details."

Use the WebSearch tool to run multiple search queries. Do NOT rely on a single search. Run at least 5-8 targeted searches to build a complete picture:

**Search Strategy:**
1. **Broad overview search:** "[topic] overview 2026" or "[topic] market size"
2. **Statistics search:** "[topic] statistics data 2025 2026"
3. **Trend search:** "[topic] trends 2026" or "future of [topic]"
4. **Player/competitor search:** "top [topic] companies" or "[topic] market leaders"
5. **Problem/challenge search:** "[topic] challenges risks"
6. **Opportunity search:** "[topic] opportunities gaps underserved"
7. **Expert opinion search:** "[topic] expert analysis" or "[topic] thought leadership"
8. **Recent news search:** "[topic] news latest"

For each search, extract:
- Key facts and figures (with source URLs)
- Quotes or claims from credible sources
- Data points that support or challenge assumptions

Use WebFetch to pull deeper detail from particularly valuable pages when a search result looks promising but needs more context.

### Step 4: Synthesize Findings

Do NOT just list search results. Synthesize the information into a coherent narrative:

1. **Cross-reference data points** — If multiple sources cite different numbers, note the range and cite both
2. **Identify patterns** — What themes emerge across multiple sources?
3. **Separate facts from opinions** — Label which is which
4. **Highlight contradictions** — If sources disagree, surface the tension
5. **Connect to user's context** — How does this relate to their business, goals, or decision?

### Step 5: Compile the Research Document

Write the document in this structure:

```markdown
# Research: [Topic Title]

> **Date:** YYYY-MM-DD
> **Requested by:** [User]
> **Purpose:** [What decision or understanding this serves]
> **Depth:** Deep Dive / Quick Brief

---

## Executive Summary

[3-5 bullet points capturing the most important findings. A busy person should be able to read ONLY this section and get 80% of the value.]

---

## Market Overview

[Size, scope, growth trajectory. Hard numbers.]

## Current Landscape

[What is happening right now. Key players, recent developments.]

## Key Trends

[Where this is heading. What is changing. Emerging patterns.]

## Data & Statistics

| Metric | Value | Source |
|--------|-------|--------|
| [Market size] | [$X billion] | [Source name + URL] |
| [Growth rate] | [X% CAGR] | [Source name + URL] |
| [Key stat] | [Value] | [Source name + URL] |

## Opportunities

[Gaps in the market. Underserved segments. Whitespace.]

## Risks & Challenges

[What could go wrong. Barriers to entry. Headwinds.]

## Competitive Landscape

| Player | What They Do | Strength | Weakness |
|--------|-------------|----------|----------|
| [Company] | [Description] | [Strength] | [Weakness] |

## Expert Perspectives

[What credible voices are saying. Named quotes with attribution.]

## Actionable Takeaways

1. [What should the user DO based on this research]
2. [Specific next step]
3. [Strategic recommendation]

---

## Sources

1. [Source Title](URL) — accessed YYYY-MM-DD
2. [Source Title](URL) — accessed YYYY-MM-DD
...

---

🤠 *Generated by LindaAI* 🏇
*Verify critical data points before making major decisions.*
```

### Step 6: Save the Document

Save to: `brain/research/{topic-slug}.md`

Naming convention:
- Use kebab-case: `electric-vehicle-market-research.md`
- Include the subject, not the date (date is in the document header)
- If a file with that name already exists, append `-v2` or the current date

### Step 7: Report to User

Present:
1. The executive summary (the key takeaways)
2. The most surprising or actionable finding
3. Where the full document was saved
4. Any gaps in the research that could not be filled (and suggestions for how to fill them)

## Research Quality Standards

1. **Cite everything.** Every data point gets a source. No unattributed claims.
2. **Current data preferred.** 2025-2026 data beats 2023 data. Flag when only older data is available.
3. **Multiple sources.** Never rely on a single source for a key claim. Cross-reference.
4. **Separate fact from opinion.** If a consultant says the market will grow 20%, that is an opinion. If revenue data shows 20% growth, that is a fact.
5. **Actionable output.** End with "so what?" — what should the user DO with this information.
6. **Acknowledge gaps.** If you could not find data on something, say so. Do not fabricate statistics.
7. **No fluff.** Every paragraph should contain information density. Cut filler.

## Output Format

A single comprehensive markdown file (typically 1,000-3,000 words for a deep dive, 500-1,000 for a quick brief) saved to `brain/research/` with full source citations and an executive summary.

## Example Usage

**User:** "Research the seller finance vehicle market"

**AI executes:**
- 8+ web searches across market size, players, trends, regulations, opportunities
- Synthesizes into a structured document
- Saves to `brain/research/seller-finance-vehicle-market.md`
- Reports executive summary + location

**User:** "Deep dive on AI agent platforms — who are the competitors?"

**AI executes:**
- Searches for AI agent platforms, competitors, pricing, features, funding
- Builds competitive landscape table
- Identifies gaps and opportunities
- Saves to `brain/research/ai-agent-platforms-competitive-landscape.md`

**User:** "What's the market for online course platforms in 2026?"

**AI executes:**
- Market sizing, growth data, key players (Kajabi, Teachable, Thinkific, etc.)
- Pricing comparison, feature analysis
- Trend analysis (AI integration, community features, cohort models)
- Saves to `brain/research/online-course-platforms-market-2026.md`

## Error Handling

- **If WebSearch is unavailable or returns errors:** Inform the user: "Web search is currently unavailable. I can still provide analysis based on my training data (up to my knowledge cutoff), but the results will not include the most current data. Want me to proceed, or try again later?"
- **If web search returns no results for a specific query:** Try 2-3 alternative query phrasings. If still no results, note the gap in the document: "Data not found for: {query topic}. This may require manual research or access to a paid industry database."
- **If the user does not specify a topic:** Ask: "What topic do you want me to research? The more specific you are, the better the output — for example, 'AI agent platforms for small business' is better than just 'AI'."
- **If `brain/research/` directory does not exist:** Create it automatically before saving the research document.
- **If a research file already exists with the same name:** Ask: "A research file for '{topic}' already exists (dated {date}). Should I update the existing file, or create a new version with today's date?"
- **If sources contradict each other on key data points:** Do not pick one arbitrarily. Present both data points with their sources and note: "Sources disagree on this metric — {Source A} reports {X} while {Source B} reports {Y}. The range is {X to Y}. Cross-reference with additional sources before using these figures for critical decisions."
- **If the research topic is too broad (e.g., "research technology"):** Ask the user to narrow it: "That's a very broad topic. Can you narrow it down? For example: 'AI SaaS market size', 'EV charging station trends', or 'creative finance regulation changes in 2026'."
- **If WebFetch fails on a specific URL:** Skip that source and note: "Could not access {URL} for deeper detail. The search snippet has been included instead." Continue with other sources.


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
