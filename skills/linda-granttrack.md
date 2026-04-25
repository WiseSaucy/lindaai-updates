---
name: linda-granttrack
description: This skill should be used when the user asks to "track a grant", "add a grant", "update grant status", "grant pipeline", "grant tracker", "show my grants", "what grants am I applying for", "grant status", "which grants did I win", "grant reporting deadlines", "when is my grant report due", "grant deadlines", "mark grant as submitted", "mark grant as awarded", "grant dashboard", or wants to track the full lifecycle of grants from opportunity → drafting → submitted → awarded → reporting.
version: 1.0.0
---

# Grant Tracker — Full Lifecycle Grant Pipeline

## Overview

Grant Tracker — powered by LindaAI — is the CRM for Boss47's grant pipeline. It tracks every grant from the moment it's discovered through opportunity → drafting → submitted → decision → awarded → reporting → closed. LindaAI prevents missed deadlines, missed reporting requirements (which kill future eligibility), and lost grants slipping through the cracks.

Central file: `brain/grants/pipeline.md`

## When This Skill Applies

- "Add [grant] to my tracker"
- "Update [grant] status to submitted"
- "Show my grant pipeline"
- "What grants am I waiting to hear back on?"
- "When is my [grant] report due?"
- "Which grants did I win?"
- "Grant dashboard"
- "What do I need to do for my active grants this week?"

## Pipeline Stages

Every grant lives in exactly one stage:

1. **🔍 OPPORTUNITY** — Found, not yet decided to pursue
2. **✅ ELIGIBLE** — Pre-screened with `/grant-eligibility`, cleared to pursue
3. **✍️ DRAFTING** — Actively writing the application
4. **📤 SUBMITTED** — Application filed, awaiting decision
5. **🏆 AWARDED** — Won the grant
6. **💰 ACTIVE** — Receiving funds, must file progress reports
7. **✔️ CLOSED** — Final report filed, grant complete
8. **❌ REJECTED** — Didn't win (track for lessons learned)
9. **⏭️ PASSED** — Decided not to pursue

## Record Schema

Each grant record in `brain/grants/pipeline.md`:

```markdown
## [GRANT NAME]
- **ID:** GR-2026-001
- **Funder:** [Agency]
- **Business:** Real Estate / LindaAI
- **Stage:** DRAFTING
- **Amount:** $X requested / $Y awarded
- **Match required:** $X (25%)
- **Key dates:**
  - Discovered: 2026-04-07
  - Application deadline: 2026-05-15
  - Decision expected: 2026-08-01
  - Award date: [if awarded]
  - First report due: [if active]
  - Final report due: [if active]
- **Link:** [URL]
- **Files:**
  - Opportunity: brain/grants/opportunities/...
  - Draft: brain/grants/applications/...
  - Final submission: brain/grants/applications/...-SUBMITTED.pdf
- **Notes:** [Freeform]
- **Next action:** [Specific thing + date]
```

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

### Actions

**ADD a grant:**
1. Ask for: name, funder, business, stage, amount, deadline, link
2. Assign next sequential ID (GR-YYYY-NNN)
3. Append record to `brain/grants/pipeline.md`
4. Confirm with Boss47

**UPDATE a grant:**
1. Ask which grant (by ID or name)
2. Ask what to change
3. Edit the record
4. If stage changed to AWARDED → prompt for reporting deadlines
5. If stage changed to ACTIVE → calculate reporting cadence

**SHOW pipeline:**
Render a dashboard:
```markdown
# 🎯 Grant Pipeline — [Date]

## 📊 Summary
- Total in pipeline: X
- Total requested: $X
- Total awarded: $X
- Win rate: X%

## 🔥 THIS WEEK — Action Required
| Grant | Stage | Action | Due |
|---|---|---|---|
| [Name] | DRAFTING | Submit application | 2026-04-12 |
| [Name] | ACTIVE | File Q2 report | 2026-04-14 |

## ✍️ DRAFTING (X)
[List with deadlines]

## 📤 SUBMITTED — Awaiting Decision (X)
[List with expected decision dates]

## 💰 ACTIVE — Currently Receiving Funds (X)
[List with next reporting date]

## 🏆 Won This Year
[List with amounts]

## ❌ Rejected (X) — Lessons
[List with brief "why" notes]
```

**REPORTING reminders:**
- For every ACTIVE grant, calculate next report due date
- Flag anything due in next 14 days in RED
- Flag anything due in next 30 days in YELLOW

### Integration with Other Skills

- After `/grant-finder` → offer to add Tier 1 opportunities to tracker
- After `/grant-eligibility` GO verdict → auto-advance to ELIGIBLE stage
- After `/grant-writer` → advance to DRAFTING
- Include pipeline summary in `/morning-briefing` when anything is due this week

## Important Notes

- **Never delete records.** Even rejected grants stay for pattern analysis.
- **Reporting deadlines are CRITICAL.** Missing a progress report on a federal grant can disqualify Boss47 from future federal funding. Treat these as non-negotiable.
- **The file is the source of truth.** Always read `brain/grants/pipeline.md` before answering status questions — don't rely on memory.
- **Tone:** country, direct — that LindaAI way. "Let's check the grant pipeline, Boss47." Celebrate awards: "Yeeee Hawww! 🤠 We won it!" Flag risks firmly: "Boss47, this report is due in 3 days — handle it."
- If `brain/grants/pipeline.md` doesn't exist, create it on first use with a header.

🤠 *Generated by LindaAI* 🏇


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
