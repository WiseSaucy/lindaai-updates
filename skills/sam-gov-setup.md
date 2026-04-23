---
name: sam-gov-setup
description: This skill should be used when the user asks to "register on SAM.gov", "SAM.gov setup", "get a UEI", "UEI number", "register for federal grants", "SAM.gov walkthrough", "how do I register on SAM.gov", "what's a UEI", "federal grant registration", "prerequisites for federal grants", or needs guidance on getting registered to apply for federal grants.
version: 1.0.0
---

# SAM.gov Setup — Federal Grant Prerequisites Walkthrough

## Overview

SAM.gov (System for Award Management) registration with a UEI (Unique Entity ID) is a HARD PREREQUISITE for EVERY federal grant. No UEI = no federal funding. Period.

This LindaAI skill walks Boss47 through the exact steps to get registered, saves progress, and flags the gotchas that trip people up. LindaAI keeps it simple so you can saddle up for federal funding.

## When This Skill Applies

- "Get me registered on SAM.gov"
- "What do I need to apply for federal grants?"
- "SAM.gov walkthrough"
- "Do I have a UEI?"
- "Why is `/grant-eligibility` blocking me on SAM.gov?"
- First-time federal grant applicant

## What Boss47 Needs Before Starting

Checklist — gather ALL of this BEFORE touching SAM.gov:

- [ ] **Legal entity name** (exactly as on IRS records)
- [ ] **EIN** (Employer Identification Number)
- [ ] **Physical address** (no P.O. boxes — must match IRS records)
- [ ] **Date of incorporation**
- [ ] **State of incorporation**
- [ ] **NAICS codes** (primary business activity)
- [ ] **Bank account info** (for electronic funds transfer)
- [ ] **Authorized signatory** (usually Boss47 as owner)
- [ ] **MPIN** (Marketing Partner ID — he'll create this)
- [ ] **login.gov account** (required to access SAM.gov)

## The Process (2026 Current)

### Step 1: Get a login.gov Account (5 min)
- Go to login.gov
- Sign up with Boss47's email
- Enable 2FA (required)

### Step 2: Request a UEI (10 min)
- Go to sam.gov
- Sign in with login.gov
- Click "Get Started" → "Get Unique Entity ID"
- Enter legal business name + address EXACTLY as on IRS records
- The system validates against D&B's database
- UEI is issued INSTANTLY if everything matches

### Step 3: Complete Full Entity Registration (30–60 min)
If he wants to RECEIVE federal grants (not just have a UEI), he must complete full registration:
- Core Data (entity info, TIN validation)
- Assertions (business types, NAICS, size metrics)
- Representations & Certifications (federal compliance attestations)
- Points of Contact
- Banking / EFT info

### Step 4: IRS TIN Validation (24–72 hours)
- SAM validates the EIN against IRS records
- Must match EXACTLY — name, address, EIN
- If it doesn't match, gets stuck here (common issue)

### Step 5: Wait for Active Status (1–10 business days)
- Full registration becomes "Active"
- Must be renewed ANNUALLY
- Active status is required on the date grant application is submitted

## Common Gotchas (SAVE BOSS47 TIME)

1. **Name mismatch** — Even one period, comma, or "LLC" vs "L.L.C." can cause IRS validation to fail
2. **Address mismatch** — Must be the IRS address, not the operating address
3. **No physical address** — P.O. boxes are rejected
4. **Notarized letter** — Sometimes required for name changes or new entities
5. **Annual renewal** — Registration EXPIRES after 365 days. Set a calendar reminder.
6. **Multiple entities** — Each entity (Real Estate LLC, LindaAI LLC) needs its OWN registration

## How This Skill Works

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

### Step 1: Assess Current Status
Ask Boss47:
1. Do you already have a UEI for [entity]? (If unsure, we can check)
2. Which entity are we registering? (Real Estate / LindaAI / both)
3. Do you have a login.gov account?
4. What's the legal name and EIN?

### Step 2: Run the Prerequisite Checklist
Go through the "What Boss47 Needs" list above. Identify gaps.

### Step 3: Build a Personalized Action Plan
Output as `brain/grants/sam-gov-setup-[entity].md`:

```markdown
# SAM.gov Setup — [Entity Name]

## Status: [NOT STARTED / IN PROGRESS / COMPLETE]

## Your Info (verified)
- Legal Name: [X]
- EIN: [X]
- Address: [X]
- NAICS: [X]

## Action Steps
- [ ] Create login.gov account
- [ ] Submit UEI request at sam.gov
- [ ] Record UEI: _______________
- [ ] Complete full entity registration
- [ ] Wait for IRS TIN validation
- [ ] Confirm "Active" status
- [ ] Set renewal reminder for [date + 1 year]

## Estimated Time: 1–10 business days
## Deadline Pressure: [YES/NO — any grant deadlines coming up?]
```

### Step 4: Offer to Walk Through Each Step
Break the work into 15-minute chunks. Don't dump the whole thing on him at once.

### Step 5: Record the UEI
Once issued, save to `brain/grants/credentials.md` (NEVER to a shared file):
```markdown
## [Entity Name]
- UEI: [12-char code]
- CAGE Code: [if applicable]
- Registration Date: [date]
- Expiration: [date] ← RENEW BEFORE THIS
- SAM.gov Status: Active
```

### Step 6: Set Renewal Reminder
Use `anthropic-skills:schedule` to create a reminder 11 months out to renew.

## Important Notes

- **NEVER pay a third party to do this.** SAM.gov is FREE. Companies that charge $500+ to register for you are scams.
- **The `.gov` domain matters.** sam.gov is real. sam.com, samregistration.com, etc. are scams.
- **Do NOT share UEI publicly.** It's not a secret like an SSN, but it's also not broadcast.
- **Annual renewal is CRITICAL.** Expired registration = all pending applications rejected.
- **If Boss47 doesn't have an LLC yet** for his RE or LindaAI business, stop and tell him to form the entity first. You can't register a sole prop on SAM.gov the same way.
- **Tone:** country, direct, patient — that LindaAI way. "Boss47, this ain't fun but it's a one-time setup that unlocks federal money. Let's knock it out."

🤠 *Generated by LindaAI* 🏇


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
