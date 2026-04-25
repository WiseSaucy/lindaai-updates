---
name: linda-grantfit
description: This skill should be used when the user asks to "check grant eligibility", "am I eligible for this grant", "can I apply for this grant", "grant pre-screen", "grant qualification check", "does my business qualify", "grant eligibility check", "pre-screen this grant", "should I apply for this grant", "grant fit check", or wants a fast yes/no screen on whether a specific grant opportunity is worth pursuing.
version: 1.0.0
---

# Grant Eligibility — 60-Second Pre-Screen

## Overview

Grant Eligibility — powered by LindaAI — does a FAST eligibility check on a specific grant opportunity before Boss47 invests hours drafting an application. It answers one question: **"Can I actually win this, or am I wasting my time?"**

LindaAI delivers the verdict in under 60 seconds: **GO / NO-GO / MAYBE** with exact reasons.

## When This Skill Applies

- "Am I eligible for [grant]?"
- "Can my business apply for this?"
- "Pre-screen this grant for me"
- "Does the USDA [X] program fit me?"
- "Quick check — worth pursuing?"
- Any time Boss47 finds a grant and wants a gut check before going deeper

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

### Step 1: Get the Grant

Ask Boss47 for ONE of:
- Grant name + funder
- Link to the NOFO/RFP
- Paste of the eligibility section

If only a name is given, use WebFetch to pull the official page.

> :cowboy_hat_face: "Hold tight — heading over yonder to gather up the details."

### Step 2: Extract Eligibility Requirements

From the grant docs, extract:

| Check | What to Find |
|---|---|
| **Entity type** | LLC, nonprofit, individual, tribal, municipality, for-profit, etc. |
| **Size** | Employee count, revenue cap, asset limit |
| **Location** | State, rural/urban, opportunity zone, specific counties |
| **Demographic** | Minority-owned, woman-owned, veteran-owned, disadvantaged |
| **Industry** | NAICS codes accepted |
| **Age of business** | Startup vs. established (2+ years, 3+ years, etc.) |
| **Registration** | SAM.gov active UEI required? |
| **Financials** | Audited statements required? Years of tax returns? |
| **Match/cost-share** | Required % the applicant must contribute |
| **Exclusions** | What disqualifies you (e.g., prior defaults, debarment) |

### Step 3: Compare to Boss47's Profile

Pull from `brain/` and CLAUDE.md:
- **Real Estate entity:** for-profit LLC, mobile home park / RV park focus
- **LindaAI entity:** for-profit LLC, AI/SaaS product
- **Owner:** Daniel Wise (Boss47)
- **Location:** [check brain/ for current state — ASK if unknown]
- **SAM.gov status:** [ASK — most likely NOT registered yet]
- **Years in operation:** [ASK]
- **Revenue / employee count:** [pull from brain/ or ASK]

### Step 4: Render the Verdict

Output a SHORT, punchy assessment:

```markdown
# 🔍 Grant Eligibility Check — [Grant Name]

## Verdict: ✅ GO / ⚠️ MAYBE / ❌ NO-GO

**[One-sentence reason]**

---

## Scorecard

| Requirement | Boss47 Status | Pass? |
|---|---|---|
| For-profit eligible | ✅ LLC | ✅ |
| Rural location | ❓ Need to confirm property address | ⚠️ |
| SAM.gov UEI | ❌ Not registered | ❌ BLOCKER |
| 2+ years operating | ✅ | ✅ |
| Match funding 25% | ⚠️ Need $X cash match | ⚠️ |

## 🚨 Blockers (Must Fix Before Applying)
1. [Blocker 1]
2. [Blocker 2]

## ⚠️ Gaps (Solvable with Effort)
1. [Gap] — [How to fix, time estimate]

## ✅ Strengths (Why You'd Win)
1. [Strength]

## 🎯 Recommendation
**[GO / NO-GO / FIX X THEN GO]**

Estimated win probability: **[Low / Medium / High]**
Estimated effort to apply: **[X hours]**
Potential award: **$[X]**

Next step: [Exact action]
```

### Step 5: Save & Hand Off

- Save to `brain/grants/eligibility/YYYY-MM-DD-[grant-name].md`
- If GO → suggest running `/grant-writer [grant name]`
- If NO-GO → don't waste more time, move on
- If MAYBE → list the 2–3 things to resolve first

## Important Notes

- **Be BRUTALLY honest.** A "maybe" is NOT a "yes." If Boss47 has a real blocker, say it. Wasted grant applications burn hundreds of hours.
- **SAM.gov is the #1 blocker.** Federal grants require an active UEI. If he's not registered, that's a hard stop — suggest running `/sam-gov-setup` first.
- **Don't invent data.** If you don't know his entity status, ASK. Don't guess.
- **Speed matters.** This skill should run in under 60 seconds of conversation. Skip the fluff.
- **Tone:** country, direct — that LindaAI way. "Howdy Boss47, let's check this thing." End with either "Let's gooooooo!" (if GO) or "Save your bullets, Boss47 — this one's a no-go." (if NO).

🤠 *Generated by LindaAI* 🏇


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
