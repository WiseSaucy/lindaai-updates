---
name: linda-subs
description: This skill should be used when the user asks to "add a subcontractor", "sub directory", "subcontractor management", "track sub insurance", "COI tracking", "certificate of insurance", "lien waiver", "sub scope", "subcontract", "sub performance", "vet a sub", "is my sub's insurance current", "sub contact list", "subcontractor agreement", "track my subs", or any request involving managing subcontractors, their compliance documents, scopes, or performance on a construction project.
version: 1.0.0
tags: [construction, subcontractors, compliance, insurance, lien-waivers]
---

# Subcontractor Manager

## Overview

Keeps your subs organized and — more importantly — keeps you protected. LindaAI maintains a subcontractor directory, tracks each sub's scope and contract value, watches insurance (COI) expiration dates, manages lien waivers through each payment, and logs performance. The two things that sink GCs are an uninsured sub having an accident and paying a sub without a lien waiver — this skill is built to stop both.

## When This Skill Applies

- User says "add a sub" or "set up my subcontractor list"
- User wants to track COIs / certificates of insurance and expiration
- User needs lien waivers tied to payments
- User wants to record a subcontract scope or value
- User asks "is anyone's insurance expiring" or wants a sub performance note

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Sub Directory
Capture per sub:
| Field | Example |
|-------|---------|
| Company | ABC Plumbing LLC |
| Trade | Plumbing |
| Contact | Joe Rivera — (555) 123-4567 |
| License # | PL-44821 |
| EIN / W-9 | on file Y/N |

### Step 2: Scope & Contract
| Field | Example |
|-------|---------|
| Project | Maple Ridge |
| Scope | Rough + finish plumbing, all 24 units |
| Contract value | $148,000 |
| Retainage | 10% |

### Step 3: Insurance (COI) Tracking — the protector
Track per sub: General Liability, Workers' Comp, Auto — carrier, policy #, limits, and **expiration date**.
- On request ("any insurance expiring?"), list every COI expiring in the next 30 days, soonest first.
- **Hard flag:** never let a sub work or get paid with an expired/missing COI — surface it loudly.

### Step 4: Lien Waivers
Match a waiver to each payment:
- **Conditional progress** (before a progress payment) · **Unconditional progress** (after it clears)
- **Conditional final** (before final) · **Unconditional final** (after final clears)
Track which waiver is needed/received for each pay app. **Rule: no waiver, no payment.**

### Step 5: Performance Log
Quick notes per sub (on-time, quality, callbacks, punch performance). Feeds future hire/award decisions.

## Hard Rules
- **No current COI on file → flag and block** "ready to pay/work." Protecting the GC comes first.
- **No signed lien waiver → do not mark a payment ready.**
- LindaAI tracks and drafts; it does not provide legal advice — for contract disputes, recommend the GC's attorney.

## Handoffs
- Pay a sub → confirm COI current + waiver received, then **linda-invoice / linda-books (operator pack)**
- Recurring quality issues → cross-reference **linda-punchlist**
- New scope for a sub → **linda-changeorder**

---
*LindaAI Construction PM Pack — Built by Daniel Wise*
