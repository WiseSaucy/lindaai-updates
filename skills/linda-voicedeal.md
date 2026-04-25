---
name: linda-voicedeal
description: This skill should be used when the user asks to "turn a voice note into a contract", "voice to contract", "transcribe and send a contract", "voice memo to agreement", "record deal terms and send contract", "voice note contract", "send a contract from my voice note", "transcribe this and make a contract", "audio to contract", "turn this recording into an agreement", "voice deal to contract", "dictate a contract", "contract from voice memo", "send agreement from recording", "make a contract from this audio", or any request involving transcribing a voice note or audio recording, extracting deal terms, filling a contract template, and sending it.
version: 1.0.0
---

# Voice Note to Contract

## Overview

Takes a voice note or audio transcription containing deal terms and turns it into a professional contract ready to send. The user records or provides a voice memo where they talk through the key terms of a deal — who the parties are, what's being done, how much, when, payment terms, etc. LindaAI extracts every deal term from the transcription, fills a contract template, generates a polished agreement document, and drafts an email to send it to the counterparty. One voice note in, signed-ready contract out — LindaAI gets the handshake on paper before the dust settles.

## When This Skill Applies

- User provides a voice note file or transcription with deal terms
- User says "I just recorded the deal terms, turn it into a contract"
- User wants to go from verbal agreement to written contract fast
- User dictates deal terms and wants them formalized
- User says "send a contract" after providing audio or transcribed terms
- User wants to capture a handshake deal in writing immediately
- User provides meeting notes or call notes with deal terms and wants a contract generated

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

### Step 0: Get the Voice Input

The user will provide input in one of these ways:

1. **Audio file path** — Path to a voice memo (.m4a, .mp3, .wav, .ogg, etc.)
2. **Transcription text** — Already-transcribed text pasted in the message
3. **Meeting notes** — Written notes from a call or meeting with deal terms

If the user says "voice to contract" with no input:

> "Drop your voice note file path, paste a transcription, or type out the deal terms from your conversation. LindaAI will pull every term and wrangle it into a ready-to-send contract."

**For audio files:** If the user provides an audio file, let them know:
> "I can't directly transcribe audio files, but you can get a quick transcription using your phone's voice memo app (most have built-in transcription), or paste the audio into a transcription service. Drop the text here and I'll handle the rest."

If the user has a transcription tool or service available, guide them to use it and come back with the text.

### Step 1: Extract Deal Terms

Parse the transcription or notes and extract every deal term mentioned. People speak casually — they don't say "the term shall be 12 months." They say things like "so we'll do this for a year" or "I told him fifty grand." Your job is to catch it all.

**Terms to extract:**

| Term | What to Look For | Example from Speech |
|------|-----------------|-------------------|
| Parties | Names, companies, roles | "So me and John from Apex Properties..." |
| Scope of Work | What's being done | "He's gonna handle all the renovation..." |
| Compensation | Price, amount, fee | "We agreed on fifty thousand" |
| Payment Schedule | When payments happen | "Half up front, half when it's done" |
| Timeline/Duration | How long, start/end dates | "Starting next Monday, should take about 8 weeks" |
| Deliverables | Specific outputs expected | "He'll deliver the finished plans and permits" |
| Expenses | Who covers costs | "Materials are on him, I'm just paying labor" |
| Termination | How to exit the deal | "Either of us can walk with 30 days notice" |
| Warranty/Guarantee | Quality assurances | "He guarantees the work for a year" |
| Liability/Insurance | Risk allocation | "He's carrying his own insurance" |
| Exclusivity | Non-compete or exclusive terms | "He won't take other jobs in my area" |
| Confidentiality | NDA-type terms | "Obviously none of this gets shared" |
| Dispute Resolution | How conflicts are handled | "If there's a problem we'll mediate first" |
| Governing Law | Jurisdiction | "Everything under Texas law" |
| Special Conditions | Anything else mentioned | "If the inspection fails, the whole thing's off" |

**After extraction, present the terms back to the user:**

> "Here's what I pulled from your voice note. Confirm these are right, and let me know if anything's missing or needs to change:"

Show a clean table of all extracted terms. Wait for confirmation before generating the contract.

### Step 2: Identify Contract Type

Based on the terms, determine the most appropriate contract type:

| Contract Type | When to Use |
|--------------|-------------|
| Service Agreement | One party performing services for another |
| Independent Contractor Agreement | Hiring a contractor for specific work |
| Partnership Agreement | Joint venture or profit-sharing deal |
| Real Estate Purchase Agreement | Buying/selling property |
| Lease Agreement | Renting property or equipment |
| Consulting Agreement | Advisory or consulting engagement |
| General Business Agreement | Catch-all for other deal types |
| Scope of Work (SOW) | Detailed deliverables under an existing relationship |
| Memorandum of Understanding (MOU) | Non-binding agreement of intent |

Tell the user which type you're using and why.

### Step 3: Generate the Contract

Create a professional contract document using the extracted terms. The contract should be:

- **Clear and readable** — Plain English, no unnecessary legalese
- **Complete** — Every extracted term has a corresponding clause
- **Professional** — Formatted like a real contract with proper sections
- **Protective** — Include standard protective clauses even if not mentioned in the voice note

**Standard contract structure:**

```
[CONTRACT TYPE]

This [Contract Type] ("Agreement") is entered into as of [Date] by and between:

**[Party A Full Name/Entity]** ("Party A")
[Address if provided]

AND

**[Party B Full Name/Entity]** ("Party B")
[Address if provided]

Collectively referred to as the "Parties."

---

## 1. PURPOSE
[What this agreement covers]

## 2. SCOPE OF WORK / SERVICES
[Detailed description of what's being done]

## 3. COMPENSATION
[Payment amount, structure, schedule]

## 4. PAYMENT TERMS
[When and how payments are made, late fees if applicable]

## 5. TIMELINE AND MILESTONES
[Start date, end date, key milestones]

## 6. DELIVERABLES
[Specific outputs or results expected]

## 7. EXPENSES AND COSTS
[Who pays for what]

## 8. TERMINATION
[How either party can end the agreement]

## 9. WARRANTIES AND GUARANTEES
[Quality assurances, workmanship guarantees]

## 10. LIABILITY AND INSURANCE
[Risk allocation, insurance requirements]

## 11. CONFIDENTIALITY
[Non-disclosure obligations]

## 12. DISPUTE RESOLUTION
[Mediation, arbitration, or litigation path]

## 13. GOVERNING LAW
[Which state/jurisdiction]

## 14. GENERAL PROVISIONS
- Entire Agreement clause
- Amendment clause (changes must be in writing)
- Severability (if one clause is invalid, others survive)
- Assignment (can't transfer without consent)
- Notices (how formal communications are sent)
- Force Majeure

## 15. SIGNATURES

_________________________          Date: __________
[Party A Name]
[Party A Title]

_________________________          Date: __________
[Party B Name]
[Party B Title]
```

Only include sections that are relevant to the deal. Don't pad with unnecessary boilerplate that doesn't apply.

### Step 4: Create the Document

Generate the contract as a clean markdown document. Save it to the working directory:

`[contract-type]-[party-names]-[date].md`

Example: `service-agreement-smith-apex-2026-04-06.md`

If the user needs it as a .docx file, use the docx skill to convert it.

### Step 5: Draft the Send Email

Create a draft email to send the contract to the counterparty.

**Ask the user:**
- "Who should I send this to? Give me their email address."
- "Any message you want included, or should I write a standard cover email?"

**Default cover email:**

```
Subject: [Contract Type] — [Brief Description] — For Your Review

Hi [Counterparty First Name],

Following up on our conversation — attached is the [contract type] covering [brief description of the deal].

Please review the terms and let me know if you have any questions or changes. Once we're both aligned, we can sign and get started.

Looking forward to working together.

[User's name]
```

Use the Gmail draft tool to create the draft with the contract content included. Let the user review before sending.

### Step 6: Confirm and Present

Tell the user:

> "Your contract is drawn up and ready to ride. LindaAI also drafted an email to [counterparty name] — check your Gmail drafts to review and send when you're good to go."

Present a summary:
- Contract type generated
- Key terms included
- File saved to [path]
- Email drafted to [recipient]
- Any terms that were unclear or missing that the user should add

**Important disclaimer to include:**
> "This contract was wrangled together by LindaAI from your voice note — it is not legal advice. For big-ticket deals, get your attorney to give it a once-over before sending."

🤠 *Generated by LindaAI* 🏇


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
