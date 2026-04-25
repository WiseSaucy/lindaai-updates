---
name: linda-swot
description: This skill should be used when the user says "SWOT analysis", "SWOT", "strengths weaknesses opportunities threats", "strategic analysis", "analyze this opportunity", "should I do this", "what are the risks", "pros and cons", "evaluate this business", "evaluate this market", "strategic assessment", "risk analysis", "opportunity analysis", "market assessment", "competitive analysis", "is this a good idea", "what could go wrong", "what are the upsides", "analyze this decision", "business analysis", "strategic review", or wants a structured strategic assessment of any business decision, market opportunity, product idea, partnership, investment, career move, or competitive position.
version: 1.0.0
---

# SWOT Analysis — Strategic Intelligence Assessment

## Overview

SWOT Analysis is LindaAI's strategic powerhouse — a comprehensive assessment for any business decision, opportunity, market, or initiative. It goes far beyond a basic four-quadrant chart. Each section includes evidence-based analysis, specific examples, and — most importantly — concrete action items. The final output includes a strategic recommendation with a clear go/no-go/conditional verdict. Think of it as what a McKinsey consultant charges $50K to deliver in a PowerPoint, except LindaAI gets it done in minutes, customized to your exact situation.

## When This Skill Applies

- User says "SWOT analysis" or "SWOT" or "strengths weaknesses opportunities threats"
- User says "strategic analysis" or "strategic assessment" or "strategic review"
- User says "analyze this opportunity" or "evaluate this business" or "evaluate this market"
- User says "should I do this" or "is this a good idea"
- User says "what are the risks" or "what could go wrong" or "pros and cons"
- User says "risk analysis" or "opportunity analysis" or "market assessment"
- User says "competitive analysis" or "analyze this decision"
- User triggers the `/swot-analysis` command
- User is weighing a significant business decision and needs structured thinking

## Category

See Around Corners

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

### Step 1: Define the Subject

Clarify exactly what's being analyzed. Ask the user (if not already provided):

1. **What are we analyzing?** — A business idea, market entry, partnership, product, investment, hire, pivot, expansion, etc.
2. **What's the context?** — Your current position, resources, timeline, constraints
3. **What decision does this inform?** — Go/no-go, invest/pass, enter/avoid, build/buy, etc.
4. **Who are the key competitors or alternatives?** — What else is in the landscape

If the user gives a one-liner like "SWOT on starting a YouTube channel," that's enough to start. Ask follow-ups only if genuinely needed.

### Step 2: Research (If Web Search Available)

> 🤠 "Hold tight — heading over yonder to gather up the details."

- Search for market data, industry reports, and trends related to the subject
- Research competitors and their positioning
- Look for recent news, shifts, or disruptions in the space
- Find relevant statistics (market size, growth rates, failure rates)
- Check for regulatory or legal considerations

If web search is unavailable, work with the user's context and general domain knowledge. Note where additional research would strengthen the analysis.

### Step 3: Check the Brain

- Read `brain/goals.md` — Does this align with the user's stated vision and priorities?
- Read `brain/projects/README.md` — Does this conflict with or complement active projects?
- Search `brain/research/` — Any existing research on this topic or related markets?
- Search `brain/knowledge-base/` — Any domain expertise relevant to this analysis?

### Step 4: Build the SWOT

For each quadrant, identify 5-8 specific, evidence-based points. Not generic observations — specific, actionable intelligence tied to the user's situation.

**Strengths (Internal, Positive)**
- What advantages does the user/business have?
- What unique resources, skills, or assets exist?
- What's working well right now?
- What competitive edge exists?

**Weaknesses (Internal, Negative)**
- What's missing? Resources, skills, team, capital?
- Where is the user/business vulnerable?
- What patterns of failure or underperformance exist?
- What would a competitor exploit?

**Opportunities (External, Positive)**
- What market trends favor this move?
- What gaps exist in the market?
- What external changes create openings?
- What timing advantages exist right now?

**Threats (External, Negative)**
- What competitors are in the way?
- What market/economic risks exist?
- What regulatory or legal risks?
- What could go wrong that's outside your control?

### Step 5: Cross-Quadrant Analysis

This is what separates a $50K strategy engagement from a college assignment. Analyze the intersections:

- **Strength + Opportunity (SO Strategies):** How to use strengths to capture opportunities
- **Strength + Threat (ST Strategies):** How to use strengths to mitigate threats
- **Weakness + Opportunity (WO Strategies):** How to fix weaknesses to unlock opportunities
- **Weakness + Threat (WT Strategies):** How to address weaknesses before threats exploit them

### Step 6: Action Items

For each quadrant, generate 2-3 specific, time-bound action items:
- **Leverage** — Actions to capitalize on strengths
- **Fix** — Actions to address weaknesses
- **Capture** — Actions to seize opportunities
- **Defend** — Actions to mitigate threats

### Step 7: Strategic Recommendation

Deliver a clear verdict:
- **GO** — The opportunity is strong, risks are manageable, move forward
- **NO-GO** — Risks outweigh benefits, threats are too severe, pass on this
- **CONDITIONAL GO** — Proceed only if [specific conditions] are met first

Support the verdict with 2-3 sentences of reasoning.

### Step 8: Save the Analysis

Save to `brain/research/swot-{topic-slug}-{YYYY-MM-DD}.md`

## Output Format

```markdown
# SWOT Analysis: [Subject]
> **Date:** [YYYY-MM-DD]
> **Decision:** [What decision this informs]
> **Verdict:** [GO / NO-GO / CONDITIONAL GO]
> **Prepared by:** LindaAI Strategic Advisor

---

## Executive Summary

[3-5 sentences: what was analyzed, key finding, recommendation, and the single biggest factor in the decision]

---

## Context

[Brief description of the subject, the user's current position, and why this analysis was requested]

---

## STRENGTHS (Internal, Positive)

| # | Strength | Impact | Evidence |
|---|----------|--------|----------|
| 1 | [Specific strength] | [High/Med/Low] | [Why this is real — data, experience, assets] |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

**Key Strength:** [The single biggest advantage and how to exploit it]

### Action: Leverage These Strengths
- [ ] [Specific action to capitalize on strength #X — by when]
- [ ] [Specific action]
- [ ] [Specific action]

---

## WEAKNESSES (Internal, Negative)

| # | Weakness | Severity | Mitigation |
|---|----------|----------|-----------|
| 1 | [Specific weakness] | [High/Med/Low] | [What can be done about it] |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

**Critical Weakness:** [The one that could sink this if not addressed]

### Action: Fix These Weaknesses
- [ ] [Specific action to address weakness #X — by when]
- [ ] [Specific action]
- [ ] [Specific action]

---

## OPPORTUNITIES (External, Positive)

| # | Opportunity | Timeline | Probability |
|---|-------------|----------|-------------|
| 1 | [Specific opportunity] | [When it's available] | [High/Med/Low chance of capturing] |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

**Biggest Opportunity:** [The one with the highest upside and how to capture it]

### Action: Capture These Opportunities
- [ ] [Specific action to seize opportunity #X — by when]
- [ ] [Specific action]
- [ ] [Specific action]

---

## THREATS (External, Negative)

| # | Threat | Severity | Probability | Early Warning |
|---|--------|----------|-------------|---------------|
| 1 | [Specific threat] | [High/Med/Low] | [Likely/Possible/Unlikely] | [Signal to watch for] |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

**Biggest Threat:** [The one most likely to cause damage and how to defend]

### Action: Defend Against These Threats
- [ ] [Specific defensive action — by when]
- [ ] [Specific action]
- [ ] [Specific action]

---

## Cross-Quadrant Strategies

### SO: Use Strengths to Capture Opportunities
- [Strategy 1: How strength X positions you to seize opportunity Y]
- [Strategy 2]

### ST: Use Strengths to Counter Threats
- [Strategy 1: How strength X defends against threat Y]
- [Strategy 2]

### WO: Fix Weaknesses to Unlock Opportunities
- [Strategy 1: Addressing weakness X would unlock opportunity Y]
- [Strategy 2]

### WT: Shore Up Weaknesses Before Threats Exploit Them
- [Strategy 1: Weakness X is most dangerous because of threat Y — fix this first]
- [Strategy 2]

---

## Risk Matrix

| Risk | Probability | Impact | Priority | Response |
|------|------------|--------|----------|----------|
| [Risk 1] | [H/M/L] | [H/M/L] | [1-5] | [Accept/Mitigate/Avoid/Transfer] |
| [Risk 2] | | | | |
| [Risk 3] | | | | |

---

## Strategic Recommendation

### Verdict: [GO / NO-GO / CONDITIONAL GO]

[2-3 paragraph analysis supporting the verdict. What tips the balance? What's the biggest risk if you proceed? What's the cost of inaction? What conditions would change the recommendation?]

### If GO: Next Steps
1. [First thing to do — this week]
2. [Second priority — this month]
3. [Third priority — this quarter]

### If NO-GO: What Would Change the Answer
- [Condition 1 that would make this a GO]
- [Condition 2]

### If CONDITIONAL: Required Conditions
- [ ] [Condition 1 — must be true before proceeding]
- [ ] [Condition 2]
- [ ] [Condition 3]

---

🤠 *Generated by LindaAI* 🏇
*Analysis completed: [YYYY-MM-DD] | Review quarterly or when conditions change significantly.*
```

## Error Handling

- **If the user's request is too vague:** Ask one clarifying question: "What specifically should I analyze? A business idea, a market, a decision you're weighing?" Don't ask 10 questions. Get enough to start and refine as you go.
- **If web search is unavailable:** Produce the analysis using user context and general knowledge. Clearly label any assumptions: "Based on general market knowledge — verify with current data." The analysis is still valuable without web research.
- **If the subject conflicts with the user's stated goals in goals.md:** Flag it prominently: "Note: This opportunity appears to conflict with your stated Q1 priority of [X]. Proceeding would split focus. Factor this into the decision."
- **If the analysis reveals a clear NO-GO:** Don't soften it. Say it directly: "This is a no-go. Here's why." The user is paying for honest strategic advice, not validation.
- **If the analysis is genuinely balanced (could go either way):** Say so. Use CONDITIONAL GO and list the specific conditions that would tip it one direction. Don't manufacture a verdict.
- **If the output directory doesn't exist:** Create `brain/research/` before saving.
- **If a SWOT on this topic already exists:** Read the previous analysis, note it, and ask: "You did a SWOT on this topic on [date]. Want me to update that analysis or create a fresh one?"

## Example Usage

**User:** "/swot-analysis launching a YouTube channel focused on creative finance education"

**AI:**
1. Reads goals.md (content creation is a stated goal, YouTube is mentioned)
2. Searches web for: creative finance YouTube channels, market size, competition, content gaps
3. Builds full SWOT with the user's specific strengths (domain expertise, existing brand) and weaknesses (no existing audience, time constraints)
4. Cross-quadrant analysis: expertise + market gap = huge opportunity; time constraint + competitive space = needs a content system
5. Verdict: CONDITIONAL GO — proceed only if a batched content workflow is built first to prevent it from consuming all available time
6. Saves to `brain/research/swot-youtube-creative-finance-2026-03-03.md`

## Cost Estimate

| Scenario | Estimated Cost |
|----------|---------------|
| SWOT without web research | $0.10–$0.25 |
| SWOT with market research | $0.25–$0.60 |
| Complex multi-factor SWOT (new market entry, partnership) | $0.40–$1.00 |

## What Makes This Premium

A McKinsey strategy engagement for a SWOT-level analysis runs $50K-$150K and takes 4-8 weeks. A freelance consultant charges $2K-$10K. Most entrepreneurs skip strategic analysis entirely because they can't afford it — they go on gut feel and learn through expensive mistakes. This skill delivers the same structured thinking framework, customized to your exact situation, with action items and a clear verdict, in minutes. It doesn't replace a McKinsey team's depth — but for 95% of the decisions an entrepreneur faces, it's more than enough to make a smarter call.

---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
