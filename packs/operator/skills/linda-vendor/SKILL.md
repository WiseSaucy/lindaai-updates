---
name: linda-vendor
description: This skill should be used when the user asks to "track a vendor", "vendor management", "add a new vendor", "vendor file", "vendor performance", "rate this vendor", "vendor renewal", "send an RFQ", "request for quote", "vendor contract", "vendor list", "who do I use for [service]", "vendor scorecard", "drop a vendor", or any request involving vendor records, performance tracking, RFQ generation, or renewal management.
tags: [operator, vendors, contracts, procurement, performance]
version: 1.0.0
---

# Linda Vendor — Vendor Management

## Overview

Operators run with a stable of vendors — landscaper, plumber, HOA mgmt, accountant, software stack, marketing freelancers, contractors. Most operators can't remember who fixed what last time, what they paid, or whose contract auto-renews next month. Linda Vendor is the single source of truth: per-vendor file with contact info, contract terms, payment history, performance scores, last service date, renewal alerts, and an RFQ generator when it's time to shop alternatives.

## When This Skill Applies

- "Add Mike's HVAC as a vendor"
- "What did I pay Comcast last year?"
- "Rate the cleaning service 3 stars — they missed the kitchen"
- "Send an RFQ for landscaping bids"
- "Who's coming up for renewal this quarter?"
- "Drop the IT firm — too many issues"
- "Pull the vendor file for Acme Plumbing"

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Vendor Profile Schema

Each vendor at `brain/operator/vendors/{vendor-slug}.md` + JSON twin at `brain/operator/vendors/{vendor-slug}.json`:

| Field | Notes |
|-------|-------|
| Legal name | |
| DBA | |
| Contact (primary + backup) | name, role, email, phone |
| Address | |
| Service category | HVAC / Plumbing / Landscaping / Legal / Accounting / Software / etc. |
| Entity served | Your business / Personal / Other |
| W-9 on file? | yes/no — link to `linda-files` |
| 1099-NEC eligible? | bool |
| COI (insurance) on file? | yes/no + expiration |
| Contract on file? | yes/no + start/end dates |
| Payment terms | NET 30 / NET 15 / on receipt / retainer |
| Default payment method | ACH / check / card |
| Renewal date | If contract |
| Auto-renew? | bool |
| Performance score | 1–5 stars rolling |
| Performance notes | dated list |
| YTD spend | rollup from `linda-books` |
| Lifetime spend | rollup from `linda-books` |

### Step 2: Performance Tracking

Per service event log row:
```
date, service_description, amount, on_time (Y/N), quality (1-5), would_use_again (Y/N), notes
```

Rolling avg is the vendor's score. Drop below 3.0 → flag for replacement consideration.

### Step 3: Renewal Alerts

For every vendor with a contract end date, register reminders via `linda-compliance`:
- 90 days before → "Time to evaluate"
- 60 days before → "Decide renew vs RFQ"
- 30 days before → "Notify or auto-renews"
- Day-of → "Renewed today"

If `auto-renew = true` and Boss47 hasn't actioned 60 days out, escalate.

### Step 4: RFQ Generator

When Boss47 says "shop the X service":
1. Pull current vendor's terms (baseline)
2. Surface 3–5 alternative vendors via WebSearch (NARPM, Yelp, Google, BBB)
3. Build RFQ doc with:
   - Scope of work (what current vendor does)
   - Volume (frequency, properties, units)
   - Performance expectations
   - Required: COI, W-9, references
   - Bid deadline (default 14 days)
4. Save to `brain/operator/vendors/rfq/{service}-{YYYY-MM-DD}/rfq.pdf`
5. Optional: fire emails via `linda-mail` to candidate list

### Step 5: Side-by-Side Bid Comparison

When bids return:
- Total cost annualized
- Service inclusions / exclusions
- Response time SLA
- Payment terms
- Contract length + cancellation
- References checked
- Recommendation

### Step 6: Save & Sync

- Vendor files: `brain/operator/vendors/{vendor-slug}.{md,json}`
- Master vendor index: `brain/operator/vendors/index.csv`
- Service log per vendor: `brain/operator/vendors/{vendor-slug}/service-log.csv`
- RFQ docs: `brain/operator/vendors/rfq/{service}-{YYYY-MM-DD}/`

Spend rollups computed nightly from `linda-books` ledger (vendor-name match).

## Inputs

- Vendor info (manual add) OR transaction in `linda-books` (auto-prompt to add)
- Service event note
- RFQ scope request

## Outputs

- Vendor file (MD + JSON)
- Service log entry
- (On request) RFQ PDF
- Renewal alerts via `linda-compliance`
- Vendor scorecard (on demand)

## Example Usage

**User:** "Add Acme Plumbing — primary Mike Jones, mike@acmeplumb.com, 555-2334, NET 30, no contract."

**LindaAI:** "Let's gooooooo Boss47!" Creates file, sets up service log. "Yeeee Hawww 🤠 — Acme's in the rolodex."

**User:** "Rate Mike's last visit — 5 stars, fixed the leak in 30 minutes, $180."

**LindaAI:** Logs service, updates rolling score (now 4.6), notes the win.

**User:** "Send an RFQ for landscaping — fire 4 candidates."

**LindaAI:** Pulls current scope from existing landscaper, builds RFQ, finds 4 alternatives, drafts emails, confirms before fire.

**User:** "Who's renewing in the next 90 days?"

**LindaAI:** Returns 3 vendors with renewal dates + auto-renew flags + scores.

## Voice & Tone

- Country, practical. **Boss47.**
- "Let's gooooooo!" on kickoff. "Yeeee Hawww 🤠" when filed / sent.
- On bad vendor: "Boss47 — Mike's at 2.4 stars. Want me to RFQ his replacement?"

## Brand Rules (PDFs)

- LindaAI logo top-right
- {customer_handle} bottom-right
- © 2024–2026 LindaAI · Built by Daniel Wise footer

## Cross-Skill Hooks

- **Feeds ← linda-books** — payee names auto-detected as vendor candidates
- **Feeds → linda-compliance** — renewal dates registered
- **Feeds → linda-mail** — RFQs and renewal notices
- **Feeds → linda-files** — contracts + W-9s + COIs filed in cabinet
- **Feeds → linda-payroll** — 1099-eligible vendors flagged for year-end
- **Feeds → linda-bizops** — count of expiring vendors / underperforming vendors on dashboard

## Error Handling

- **Duplicate vendor (same EIN or fuzzy name match):** Ask Boss47 to confirm before creating second record.
- **Missing W-9 for 1099-eligible vendor:** Auto-flag, prompt collection workflow.
- **Vendor has no service log but YTD spend > $0:** Reconcile with `linda-books` — likely miscategorization.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
