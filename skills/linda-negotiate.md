---
name: linda-negotiate
description: This skill should be used when the user says "negotiation prep", "prepare for a negotiation", "I'm negotiating with", "help me negotiate", "negotiation strategy", "prep me for this deal", "what's my leverage", "BATNA analysis", "how should I negotiate", "negotiation plan", "deal strategy", "prepare my position", "counterparty research", "what should I ask for", "how do I approach this negotiation", "negotiation playbook", "prep me for this meeting", "salary negotiation", "vendor negotiation", "contract negotiation", "price negotiation", "partnership negotiation", or wants to prepare a comprehensive strategy for any negotiation — business deals, contracts, partnerships, pricing, hiring, vendor terms, or any situation where two parties need to reach agreement.
version: 1.0.0
---

# Negotiation Prep — Complete Negotiation Strategy Builder

## Overview

Negotiation Prep is LindaAI's deal-closing war room. It builds a comprehensive, battle-tested negotiation strategy for any scenario. You provide who you're negotiating with, what's at stake, and your ideal outcome. LindaAI researches the counterparty (web search if available), analyzes your leverage, builds a BATNA (Best Alternative to Negotiated Agreement), identifies pressure points, prepares opening positions, predicts every objection the other side will raise, and writes word-for-word response scripts. This is what a $2,000/hour negotiation consultant delivers — prepared in minutes.

## When This Skill Applies

- User says "negotiation prep" or "prepare for a negotiation"
- User says "I'm negotiating with [someone]" or "help me negotiate"
- User says "what's my leverage" or "BATNA analysis"
- User says "prep me for this deal" or "prep me for this meeting"
- User says "negotiation strategy" or "negotiation plan" or "deal strategy"
- User says "how should I negotiate" or "how do I approach this"
- User says "what should I ask for" or "prepare my position"
- User says "salary negotiation" or "vendor negotiation" or "contract negotiation"
- User triggers the `/negotiation-prep` command
- User is about to enter any situation where terms need to be agreed upon

## Category

Clone Your Decision-Making

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

### Step 1: Gather Context

Ask the user for the following (if not already provided):

**Required information:**
1. **Who are you negotiating with?** — Name, company, role, relationship
2. **What's at stake?** — What's being negotiated (price, terms, contract, partnership, salary, etc.)
3. **What's your ideal outcome?** — Best-case scenario if everything goes your way
4. **What's your walk-away point?** — The minimum acceptable outcome before you walk

**Helpful but optional:**
5. **What's your relationship with them?** — New contact, existing partner, repeat customer, adversarial
6. **Any known constraints on their side?** — Timeline pressure, budget limits, competing offers
7. **What leverage do you have?** — Unique value you bring, alternatives they don't have, information edge
8. **When is this happening?** — Date/time of the negotiation (affects urgency analysis)

If the user provides all context upfront, skip the questions and proceed directly.

### Step 2: Research the Counterparty

> 🤠 "Hold tight — heading over yonder to gather up the details."

**If web search is available:**
- Search for the counterparty's company, recent news, financial situation
- Look for public information about their negotiation patterns, recent deals
- Check for any leverage indicators (layoffs, funding rounds, market pressure, expansion)
- Research industry standard terms/pricing for comparable deals

**If web search is not available:**
- Work with the information the user provided
- Note what additional research might strengthen the position
- Ask the user if they have any additional intel on the counterparty

**Check the brain:**
- Search `brain/people/` for any existing file on the counterparty
- Search `brain/research/` for relevant market data
- Check `brain/daily/` for any previous interactions or notes about this party

### Step 3: Build the BATNA Analysis

BATNA (Best Alternative to Negotiated Agreement) is the most important concept in negotiation. Analyze both sides:

**Your BATNA:**
- What happens if this deal falls through?
- What are your alternatives? How strong are they?
- How urgent is this deal for you?
- Rate your BATNA strength: Strong / Moderate / Weak

**Their BATNA:**
- What are the counterparty's alternatives if they don't deal with you?
- How easily can they replace what you offer?
- What's their time pressure?
- Rate their BATNA strength: Strong / Moderate / Weak

**Power dynamics conclusion:**
- Who needs this deal more?
- Where does leverage actually sit?
- What can shift the power balance in your favor?

### Step 4: Identify Leverage Points

Catalog every source of leverage:

| Leverage Type | Your Leverage | Their Leverage |
|--------------|---------------|----------------|
| **Information** | What you know that they don't | What they know that you don't |
| **Time** | Your urgency level | Their urgency level |
| **Alternatives** | Your other options | Their other options |
| **Expertise** | Unique skills/knowledge you bring | What they bring that's hard to replace |
| **Relationship** | Trust/history/reputation | Their leverage through relationship |
| **Market** | Market conditions favoring you | Market conditions favoring them |
| **Scarcity** | What's scarce that you control | What's scarce that they control |

### Step 5: Prepare Positions

Define three positions:

1. **Opening Position (Ambitious):** Your first offer. Aggressive but defensible. Leaves room to concede while still landing above your target.
2. **Target Position (Realistic):** Where you actually want to land. The outcome you'd be genuinely satisfied with.
3. **Walk-Away Point (Floor):** The absolute minimum. Below this, you walk. No exceptions.

For each position, prepare the rationale — why it's fair, what data supports it, how to frame it.

### Step 6: Predict Objections and Write Scripts

Identify the top 5-10 objections the counterparty is likely to raise. For each one, write:
- The objection (their exact words, predicted)
- Why they're raising it (their underlying concern)
- Your response (word-for-word script)
- A follow-up question to redirect the conversation

### Step 7: Design the Negotiation Flow

Map out the conversation structure:
1. **Opening:** How to set the tone and frame the discussion
2. **Information gathering:** Questions to ask that reveal their position
3. **Presenting your position:** How and when to make your first offer
4. **Handling pushback:** Concession strategy (what to give, in what order)
5. **Closing:** How to lock in agreement and prevent buyer's remorse
6. **If stalled:** How to break a deadlock or table and revisit

### Step 8: Generate the Final Document

Compile everything into the output format below and save to `brain/research/negotiation-prep-{counterparty-slug}-{YYYY-MM-DD}.md`.

## Output Format

```markdown
# Negotiation Prep: [Counterparty Name]
> **Date:** [YYYY-MM-DD]
> **Negotiation Date:** [When it's happening, if known]
> **Stakes:** [One-line summary of what's being negotiated]
> **Prepared by:** LindaAI Executive Assistant

---

## Executive Summary

[3-5 sentence summary: who, what, your leverage position, recommended strategy, expected outcome]

---

## Counterparty Profile

| Detail | Info |
|--------|------|
| Name | |
| Company | |
| Role | |
| Relationship | |
| Known Constraints | |
| Negotiation Style (if known) | |

### Counterparty Research
[Everything found via web search or brain files. Recent news, financial situation, market position, relevant history.]

---

## BATNA Analysis

### Your BATNA
- **Alternatives if no deal:** [List]
- **Strength:** [Strong / Moderate / Weak]
- **Implication:** [What this means for your approach]

### Their BATNA
- **Their alternatives:** [List]
- **Strength:** [Strong / Moderate / Weak]
- **Implication:** [What this means for their flexibility]

### Power Balance
[Who needs this deal more? Where does leverage sit? 1-2 paragraph analysis.]

---

## Leverage Map

| Leverage Type | Yours | Theirs |
|--------------|-------|--------|
| Information | | |
| Time | | |
| Alternatives | | |
| Expertise | | |
| Relationship | | |
| Market | | |
| Scarcity | | |

**Key Leverage Insight:** [The single most important leverage point and how to use it]

---

## Positions

### Opening Position (Ambitious)
- **What to ask for:** [Specific terms]
- **Rationale:** [Why it's fair — data, comps, market]
- **How to present it:** [Framing language]

### Target Position (Realistic)
- **Where to land:** [Specific terms]
- **Why this is a win:** [What makes this satisfactory]

### Walk-Away Point (Floor)
- **Absolute minimum:** [Specific terms]
- **Walk-away trigger:** [The moment you stand up and leave]
- **Walk-away script:** "[Exact words to say when walking away]"

---

## Concession Strategy

| Order | What You Can Give | What You Get in Return | Notes |
|-------|-------------------|----------------------|-------|
| 1st | [Smallest concession] | [Something you want] | Give this early to build goodwill |
| 2nd | [Medium concession] | [Something more valuable] | Only if they reciprocate |
| 3rd | [Larger concession] | [Must be matched equally] | Final movement |

**Rule:** Never concede without getting something in return. Every "give" has a "get."

---

## Predicted Objections & Response Scripts

### Objection 1: "[Their likely words]"
**Their concern:** [What's really driving this]
**Your response:** "[Word-for-word script]"
**Redirect question:** "[Question to move the conversation forward]"

### Objection 2: "[Their likely words]"
**Their concern:** [What's really driving this]
**Your response:** "[Word-for-word script]"
**Redirect question:** "[Question]"

### Objection 3: "[Their likely words]"
[Same format — continue for all predicted objections]

---

## Negotiation Flow

### 1. Opening (First 5 minutes)
- **Goal:** Set collaborative tone, establish agenda
- **Script:** "[How to open the conversation]"
- **Body language:** [Confident, open, unhurried]

### 2. Information Gathering (Minutes 5-15)
- **Questions to ask:**
  - [Question that reveals their priorities]
  - [Question that reveals their constraints]
  - [Question that reveals their timeline]
  - [Question that reveals their alternatives]
- **Listen for:** [Key signals that indicate flexibility or firmness]

### 3. Present Your Position (Minutes 15-25)
- **Lead with:** [Frame the value before stating numbers]
- **Anchor:** [Your opening position, stated confidently]
- **Silence:** [After stating your position, stop talking. Let them respond.]

### 4. Handle Pushback (Minutes 25-40)
- **Expected pushback:** [What they'll say]
- **Concession order:** [Follow the concession strategy above]
- **Key phrase:** "I can move on [X] if you can move on [Y]"

### 5. Close (Minutes 40-50)
- **Summarize:** Restate all agreed terms verbally
- **Lock in:** "Let's get this in writing by [specific date]"
- **Prevent regression:** "We've agreed on X, Y, and Z — I'll send a summary today"

### 6. If Stalled
- **Deadlock breaker:** "What if we [creative alternative]?"
- **Table and revisit:** "Let's both think on this and reconnect [specific time]"
- **Escalation:** "Would it help to involve [decision-maker] to move this forward?"

---

## Strategic Notes

### Do's
- [Specific tactical advice for this negotiation]
- [What to emphasize]
- [How to build rapport with this specific counterparty]

### Don'ts
- [Specific things to avoid]
- [Topics that could derail the conversation]
- [Concessions that would be too costly]

### Wild Cards
- [Unexpected things that could happen and how to handle them]

---

🤠 *Generated by LindaAI* 🏇
*Prepared: [YYYY-MM-DD] | Review before negotiation and practice key scripts out loud.*
```

## Error Handling

- **If the user doesn't provide enough context:** Ask targeted questions. Minimum needed: who, what's at stake, ideal outcome. Don't generate a strategy with insufficient information — a bad strategy is worse than no strategy.
- **If web search is unavailable:** Still produce a complete strategy using user-provided information. Note which sections would be stronger with additional research and suggest the user gather that intel independently.
- **If the counterparty is someone in `brain/people/`:** Pull their file for relationship context, communication preferences, and history. This is gold — use it to personalize the approach.
- **If the negotiation is adversarial vs. collaborative:** Adjust tone and tactics accordingly. Ask the user: "Is this a one-time transaction or an ongoing relationship?" This fundamentally changes the approach.
- **If the user's walk-away point is too close to their ideal outcome:** Flag it: "Your walk-away is very close to your target. This leaves almost no room to negotiate. Are you sure about these numbers?" Help them pressure-test their positions.
- **If the stakes are very high (>$100K or career-defining):** Recommend the user also consult with a human advisor (attorney, mentor, experienced negotiator). AI prep is powerful but not a replacement for human judgment on life-changing deals.
- **If the output directory doesn't exist:** Create `brain/research/` before saving. Never error on a missing directory.

## Example Usage

**User:** "/negotiation-prep Marcus Williams — he's our CPA and wants to raise his annual retainer from $8K to $12K. I think $9.5K is fair. I'll walk at $10.5K."

**AI:**
1. Checks `brain/people/` for Marcus Williams file
2. Searches web for Marcus Williams CPA firm (if search available)
3. Researches CPA market rates in the user's area
4. Builds full strategy: BATNA (we can switch CPAs vs. he'd lose a good client), leverage (long-term relationship, referral potential), positions ($8.5K opening, $9.5K target, $10.5K walk), objections ("My costs have gone up", "I'm bringing you more value now"), response scripts
5. Saves to `brain/research/negotiation-prep-marcus-williams-2026-03-03.md`

## Cost Estimate

| Scenario | Estimated Cost |
|----------|---------------|
| Strategy without web research | $0.10–$0.25 |
| Strategy with counterparty web research | $0.20–$0.50 |
| Complex multi-party negotiation | $0.30–$0.75 |

## What Makes This Premium

Professional negotiation consultants charge $500-$5,000 per engagement to do exactly this: research the counterparty, analyze leverage, prepare positions, predict objections, and write response scripts. Most people walk into negotiations with a number in their head and nothing else. This skill means you walk in with a complete playbook — every objection anticipated, every response practiced, every leverage point identified. The difference between "I think I'll ask for..." and "Here's my opening position, backed by market data, with three concession layers and scripts for their top 8 objections."

---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
