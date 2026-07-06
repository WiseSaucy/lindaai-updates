---
name: linda-changeorder
description: This skill should be used when the user asks to "create a change order", "build a CO", "draft a change order", "PCO", "potential change order", "scope change", "owner directed change", "change order request", "extra work order", "additional services", "CO for {project}", "log a change order", "approve a change order", "issue a CO", or any request involving construction change order documentation.
version: 1.0.0
tags: [construction, change-orders, contracts, project-management]
---

# Change Order Builder

## Overview

Drafts contractor-grade change orders fast. Boss describes the scope change in plain English and LindaAI builds the CO document with scope description, cost breakdown (labor / materials / equipment / sub / markup), schedule impact, and a signature block. Saves the CO to the project, updates the CO log, and produces a branded PDF ready to send to the owner or GC.

## When This Skill Applies

- User says "build a CO" or "create a change order"
- User wants to draft a PCO (potential change order) or CRR
- User describes scope creep or owner-directed extra work
- User says "issue a CO for {project}"
- User wants to log an approved CO into project records

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Gather CO Inputs

Required:
| Field | Example |
|-------|---------|
| Project | Maple Ridge |
| CO number | auto: next sequential per project |
| Reason / type | Owner-directed / Field condition / Design change / Code |
| Scope description | Add 12 LF of foundation drain on north wall |
| Source | RFI #14, Architect SI #3, owner email |

Cost breakdown (ask if not given):
| Category | Amount |
|----------|--------|
| Labor (hours × rate × burden) | |
| Materials | |
| Equipment | |
| Subcontractor | |
| Subtotal | |
| Overhead % | typically 10% |
| Profit % | typically 5–10% |
| Bond / insurance % | per contract |
| **Total CO Value** | |

Schedule impact:
| Field | Value |
|-------|-------|
| Days requested | |
| Critical path? | yes/no |

### Step 2: Auto-Number

Read `brain/projects/{slug}/change-orders/_log.md`. Next number = highest existing + 1, format `CO-{NNN}`. PCOs use `PCO-{NNN}`. If user is converting a PCO to CO, preserve traceability ("Converted from PCO-007").

### Step 3: Pull Project + Owner Info

From `brain/projects/{slug}/_meta.md`:
- Owner / GC name & address
- Original contract value
- Sum of approved COs
- Revised contract value (post this CO)

### Step 4: Generate the CO Document

Save markdown + branded PDF:
```
brain/projects/{slug}/change-orders/CO-{NNN}.md
brain/projects/{slug}/change-orders/CO-{NNN}.pdf
```

### Step 5: Update Log & Budget

Append a row to `change-orders/_log.md` (number, date, status=Pending, amount, days, summary). If status flips to Approved later, update the contract sum on `_meta.md` and re-run `/linda-wip` if requested.

## Output Format

```markdown
# CHANGE ORDER {CO-NNN}

**Project:** {Project Name}
**Date Issued:** {YYYY-MM-DD}
**To:** {Owner / GC name + address}
**From:** {Contractor name from brain/invoices/config.md}

---

## Reference
- Original Contract Value: ${original}
- Sum of Previous Approved COs: ${prev}
- This Change Order: ${this}
- New Revised Contract Value: ${new}

## Reason for Change
{Type — owner-directed / field condition / design / code}

## Source Documents
- {RFI #, ASI #, email date, etc.}

## Scope of Change
{Plain-language description of work added or deleted}

## Cost Breakdown
| Category | Amount |
|----------|-------:|
| Labor | ${X} |
| Materials | ${X} |
| Equipment | ${X} |
| Subcontractor | ${X} |
| Subtotal | ${X} |
| Overhead ({%}) | ${X} |
| Profit ({%}) | ${X} |
| Bond / Ins ({%}) | ${X} |
| **TOTAL** | **${X}** |

## Schedule Impact
- Additional calendar days: {N}
- Critical path: {yes/no}
- New substantial completion date: {YYYY-MM-DD}

## Approval

Contractor: ______________________  Date: __________

Owner / GC: ______________________  Date: __________

Architect (if required): ______________________  Date: __________

---
🤠 *Drafted by LindaAI* 🏇
```

## PDF Branding

- **LindaAI** logo top-right
- **{customer_handle}** bottom-right
- Footer: `© 2024–2026 LindaAI — Built by Daniel Wise`

## Example Usage

**User:** "Build a CO on Maple Ridge — owner wants 12 LF of foundation drain on the north wall, $4,200 materials, 16 labor hours at $85, 10% OH, 5% profit, 2 days schedule."

**LindaAI:** "Let's gooooooo Boss." Generates CO-012 with full breakdown ($4,200 + $1,360 + 15% markup = $6,440 total, 2 days), saves markdown + PDF, updates log. "Yeeee Hawww 🤠 — CO-012 ready to send. Revised contract $1,256,440."

**User:** "Mark CO-012 approved as of today."

**LindaAI:** Updates log status, updates `_meta.md` revised contract sum, asks if Boss wants to refresh WIP.

## Voice & Tone

- Country, direct. **Boss.**
- Always remind to get the signature before starting the work — Boss's mandatory underwriting protocol equivalent for COs.

## Error Handling

- **Missing cost detail:** Ask line-by-line — labor, materials, equipment, sub.
- **No project meta:** Ask Boss for owner name and original contract sum.
- **Duplicate CO number on disk:** Increment past it and inform.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
