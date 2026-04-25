---
name: linda-contract
description: This skill should be used when the user asks to "review a contract", "check this contract", "read this agreement", "review this lease", "review this NDA", "what does this contract say", "is this contract fair", "contract analysis", "legal review", "review these terms", "what am I signing", "break down this contract", "what are the risks in this contract", "contract red flags", "negotiation points", "what should I push back on", "review this proposal", "review this SOW", "review this MSA", "review this operating agreement", "check the terms", "is this agreement standard", "what are the termination clauses", "review this vendor contract", "review this partnership agreement", "service agreement review", "employment contract review", "licensing agreement review", "review this LOI", "letter of intent review", or any request involving reviewing, analyzing, summarizing, or flagging risks in a contract, agreement, or legal document.
version: 1.0.0
---

# Contract Reviewer

## Overview

LindaAI reviews any contract or legal document with the precision of a $500/hour attorney and the clarity of a trusted advisor who speaks plain English. Hand over your contract text (pasted directly or as a file path) and LindaAI delivers: an executive summary (what this contract actually does, in one paragraph), a key terms table, all financial obligations mapped out, termination and exit clauses isolated, risk flags for anything unusual or unfavorable, negotiation leverage points, and recommended changes — all formatted as a document you can share with your attorney or keep for reference. This is not legal advice. This is the intelligence layer that makes your attorney billable hours 10x more efficient because you walk in already knowing what matters.

## When This Skill Applies

- User says "review this contract" or "check this agreement"
- User pastes contract text and wants it analyzed
- User provides a file path to a PDF, text, or markdown contract
- User asks "is this contract fair?" or "what are the risks?"
- User wants to understand what they are signing before signing
- User asks for negotiation points or leverage in a contract
- User wants termination clauses identified
- User asks "what does this contract actually say in plain English?"
- User is comparing two contracts or versions
- User wants a contract summary to share with their team or attorney
- User mentions any type of agreement: NDA, LOI, MSA, SOW, lease, partnership, operating agreement, licensing, vendor, employment, service agreement

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

### Step 0: Get the Contract Text

The user will provide the contract in one of these ways:

1. **Pasted text** — Contract text directly in the message
2. **File path** — Path to a `.txt`, `.md`, or `.pdf` file
3. **Multiple files** — Comparing two versions or related documents

If the user says "review a contract" with no text or file:
- Ask: "Paste the contract text here, or give me the file path. I'll break it down — executive summary, key terms, financial obligations, risks, and negotiation points."

If a file path is provided:
- Read the file using the Read tool
- If it is a PDF, use the PDF reading capability
- If the file does not exist, report the error and ask for the correct path

### Step 1: Initial Read and Classification

Read the entire contract and identify:

| Field | What to Extract |
|-------|----------------|
| Document Type | NDA, MSA, SOW, lease, operating agreement, LOI, employment, vendor, licensing, partnership, other |
| Parties | Who is involved (Party A, Party B, etc.) — names and roles |
| Effective Date | When the contract starts |
| Term/Duration | How long it lasts |
| Governing Law | Which state/jurisdiction governs disputes |
| Total Pages/Length | Approximate size of the document |
| Complexity | Simple (< 5 pages, standard terms) / Moderate (5-20 pages) / Complex (20+ pages, custom terms) |

### Step 2: Executive Summary

Write a plain-English summary of the contract in one paragraph. No legalese. Answer these questions:

- What does this contract do?
- Who does what?
- How much money changes hands?
- How long does it last?
- How do you get out of it?

This should be readable by anyone — your business partner, your spouse, your assistant. If they read this one paragraph and nothing else, they should understand the deal.

### Step 3: Key Terms Table

Extract every material term into a structured table:

| Term | Details | Section/Page |
|------|---------|-------------|
| Effective Date | {date} | {section ref} |
| Term/Duration | {X months/years, auto-renew?} | {ref} |
| Payment Amount | ${amount, frequency} | {ref} |
| Payment Terms | {Net 30, due on signing, milestone-based, etc.} | {ref} |
| Deliverables | {what each party is required to deliver} | {ref} |
| Exclusivity | {Yes/No — scope of exclusivity} | {ref} |
| Non-Compete | {Yes/No — scope, duration, geography} | {ref} |
| Confidentiality | {scope, duration, carve-outs} | {ref} |
| IP Ownership | {who owns what, work-for-hire, licensing} | {ref} |
| Liability Cap | {$ amount or formula} | {ref} |
| Indemnification | {who indemnifies whom, scope} | {ref} |
| Insurance Requirements | {types, minimum coverage amounts} | {ref} |
| Assignment | {can rights be transferred? conditions?} | {ref} |
| Dispute Resolution | {litigation, arbitration, mediation — where?} | {ref} |
| Governing Law | {state/jurisdiction} | {ref} |
| Notice Requirements | {how to give formal notice, to whom, method} | {ref} |

Skip any row that does not apply. Add any material terms not listed above that are specific to this contract type.

### Step 4: Financial Obligations

Map out every financial commitment in the contract:

```markdown
## Financial Obligations

### What You Pay
| Obligation | Amount | Frequency | Conditions | Section |
|-----------|--------|-----------|-----------|---------|
| {description} | ${amount} | {one-time/monthly/annual/milestone} | {what triggers it} | {ref} |

### What You Receive
| Obligation | Amount | Frequency | Conditions | Section |
|-----------|--------|-----------|-----------|---------|
| {description} | ${amount} | {frequency} | {conditions} | {ref} |

### Total Financial Exposure
- **Year 1 cost:** ${calculated total}
- **Full term cost:** ${calculated total over the contract duration}
- **Maximum liability:** ${cap if specified, "unlimited" if not capped}
- **Exit cost:** ${early termination fees, penalties, remaining obligations}

### Hidden Costs to Watch
- {Any costs that are not obvious — auto-escalation clauses, expense pass-throughs, change order rates, late fees, interest on overdue payments}
```

### Step 5: Termination and Exit Analysis

This section answers the most important question: "How do I get out of this if I need to?"

```markdown
## Termination & Exit Clauses

### How to End This Contract
| Method | Notice Required | Penalty/Cost | Conditions | Section |
|--------|----------------|-------------|-----------|---------|
| Expiration | None (term ends) | None | Contract runs its course | {ref} |
| Termination for Convenience | {X} days written notice | ${amount or formula} | {any conditions} | {ref} |
| Termination for Cause | {X} days written notice + cure period | None (if cause is valid) | {what constitutes "cause"} | {ref} |
| Mutual Agreement | Both parties agree in writing | Negotiable | {conditions} | {ref} |
| Non-Renewal | {X} days before renewal date | None | {must give notice or auto-renews} | {ref} |

### Auto-Renewal Warning
- **Does it auto-renew?** {Yes/No}
- **Renewal term:** {same term / month-to-month / other}
- **Opt-out window:** {X days before renewal date — CALENDAR THIS}
- **What happens if you miss the window:** {locked in for another full term}

### Post-Termination Obligations
- {Any obligations that survive termination: non-compete, confidentiality, IP transfer, final payments, transition assistance}
- **Survival period:** {how long post-termination obligations last}
```

### Step 6: Risk Flags

Identify anything in the contract that is unusual, unfavorable, aggressive, or non-standard. Rate each flag:

```markdown
## Risk Flags

| # | Risk | Severity | Section | Why It Matters |
|---|------|----------|---------|---------------|
| 1 | {description} | HIGH / MEDIUM / LOW | {ref} | {plain-English explanation of the real-world impact} |
| 2 | {description} | {severity} | {ref} | {explanation} |
```

**Common risk flags to check:**

- **Unlimited liability** — No cap on damages you could owe
- **One-sided indemnification** — You indemnify them but they don't indemnify you
- **Broad IP assignment** — You give away IP rights beyond what's necessary
- **Non-compete that's too broad** — Geographic scope, duration, or industry scope that limits your business
- **Auto-renewal with no easy out** — Locked in with a narrow opt-out window
- **Liquidated damages** — Pre-set penalty amounts that seem disproportionate
- **Unilateral amendment rights** — They can change terms without your consent
- **Vague termination for "cause"** — Cause is defined so broadly that almost anything qualifies
- **Personal guarantee** — You are personally liable, not just your entity
- **Confession of judgment** — You waive the right to defend yourself in court
- **Mandatory arbitration in their jurisdiction** — You have to travel to their city for disputes
- **Assignment without consent** — They can sell/transfer the contract without asking you
- **Most favored nation (MFN) clause** — You can't offer better terms to anyone else
- **Audit rights with no limits** — They can audit your books at any time with broad scope
- **Force majeure that excludes pandemics** — Post-COVID, this matters
- **Waiver of jury trial** — You give up the right to a jury

### Step 7: Negotiation Leverage Points

Identify specific areas where the user has room to negotiate:

```markdown
## Negotiation Leverage Points

### Must-Change (High Priority)
1. **{Clause/term}** — {what it currently says} → **Recommend:** {what it should say and why}
2. **{Clause/term}** — {current} → **Recommend:** {change}

### Should-Change (Medium Priority)
1. **{Clause/term}** — {current} → **Recommend:** {change}

### Nice-to-Have (Low Priority)
1. **{Clause/term}** — {current} → **Recommend:** {change}

### Suggested Redline Language
For the must-change items, provide exact replacement language:

**Original:** "{exact contract language}"
**Proposed:** "{replacement language}"
**Rationale:** "{why this is fairer/more standard}"
```

### Step 8: Generate and Save the Full Review

Compile all sections into a single document:

```markdown
# Contract Review: {Contract Type} — {Parties}

> **Reviewed:** {date}
> **Document:** {filename or "pasted text"}
> **Type:** {contract type}
> **Parties:** {Party A} and {Party B}
> **Complexity:** {Simple / Moderate / Complex}

---

## IMPORTANT DISCLAIMER
This is an AI-generated contract analysis for informational purposes only. It is NOT legal advice. Before signing, have a licensed attorney in your jurisdiction review any contract involving significant financial commitments, liability exposure, or business-critical terms. This analysis is designed to make your attorney's review faster and your questions sharper — not to replace legal counsel.

---

## Executive Summary

{one paragraph, plain English}

---

## Key Terms
{table from Step 3}

---

## Financial Obligations
{from Step 4}

---

## Termination & Exit Clauses
{from Step 5}

---

## Risk Flags
{from Step 6}

---

## Negotiation Leverage Points
{from Step 7}

---

## Questions to Ask Before Signing

1. {Specific question raised by a risk flag or ambiguous term}
2. {Question about financial implications}
3. {Question about exit/termination scenario}
4. {Question about a vague or undefined term}
5. {Question about enforceability or jurisdiction}

---

## Verdict

**Overall Assessment:** {FAVORABLE / MOSTLY FAIR / NEEDS NEGOTIATION / UNFAVORABLE / DO NOT SIGN}

**Summary:** {2-3 sentences — is this a standard deal, a good deal, or a deal with problems? What is the single most important thing to address before signing?}

**Risk Level:** {LOW / MODERATE / HIGH / CRITICAL}

**Recommended Next Step:** {Sign as-is / Negotiate the {X} items flagged above / Have an attorney review Section {Y} / Walk away and here's why}

---

🤠 *Generated by LindaAI* 🏇
*This is not legal advice. Consult a licensed attorney before signing.*
```

Save to: `brain/research/contract-review-{type-slug}-{YYYY-MM-DD}.md`

If the contract type is ambiguous, use the counterparty name: `contract-review-{counterparty-slug}-{YYYY-MM-DD}.md`

## Example Usage

**User:** "Review this contract" {pastes 3 pages of a vendor service agreement}

**AI:** Analyzes the full document. Executive summary: "This is a 12-month service agreement where XYZ Agency provides marketing services for $5,000/month. They own all creative work product, you can't terminate without 90 days notice and a $10,000 early termination fee, and they can raise rates with 30 days notice." Flags IP ownership as HIGH risk, termination fee as MEDIUM risk, and unilateral rate increase as MEDIUM risk. Provides specific redline language to fix the IP clause and make termination more balanced. Saves to `brain/research/contract-review-xyz-agency-2026-03-03.md`.

**User:** "/contract-review ~/Documents/lease-agreement.pdf"

**AI:** Reads the PDF. Identifies it as a commercial lease. Flags the personal guarantee clause, the auto-renewal with only a 30-day opt-out window, and the triple-net expense pass-through with no cap. Provides negotiation language for each. Verdict: NEEDS NEGOTIATION on 3 key points.

**User:** "Is this NDA standard?" {pastes NDA text}

**AI:** Reviews the NDA. Confirms most terms are standard (2-year confidentiality, mutual obligations, standard carve-outs for public information). Flags one issue: the non-solicitation clause is unusually broad (covers any employee or contractor, not just those the user worked with directly). Recommends narrowing it. Verdict: MOSTLY FAIR.

**User:** "Compare these two versions" {pastes or provides two files}

**AI:** Reads both versions. Creates a side-by-side comparison of every term that differs. Highlights which changes favor which party. Recommends which version to sign or which specific changes to push back on.

## Error Handling

- **If no contract text or file is provided:** Ask: "Paste the contract text below, or give me the file path (txt, md, or pdf). I'll produce an executive summary, key terms, risk flags, and negotiation points."
- **If the file path does not exist:** Report: "File not found at {path}. Double-check the path and try again. I can also analyze text pasted directly into the conversation."
- **If the contract is extremely short (< 100 words):** Note: "This appears to be a very brief document. It may be a summary, term sheet, or excerpt rather than the full contract. I'll analyze what's here, but flag that key clauses may be missing. Do you have the full document?"
- **If the contract is extremely long (> 50 pages):** Note: "This is a long document ({X} pages). I'll focus on the most material terms, financial obligations, and risk flags. If you want me to deep-dive on a specific section, tell me which one."
- **If the text is not a contract (user pasted something else):** Report: "This doesn't appear to be a contract or legal agreement. It looks like {what it is}. If you meant to paste a contract, try again. If you want me to analyze this document differently, let me know."
- **If the contract is in a language other than English:** Note: "This contract appears to be in {language}. I'll do my best to analyze it, but my review will be most accurate on English-language contracts. Consider having a bilingual attorney review the original language version."
- **If the contract references external documents (exhibits, schedules, addenda) not provided:** Flag: "This contract references {X} external documents ({list}) that were not included. My review covers only what was provided. These attachments could contain material terms — request them before signing."
- **If the `brain/research/` directory does not exist:** Create it before saving.


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
