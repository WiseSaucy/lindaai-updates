---
name: linda-submittal
description: This skill should be used when the user asks to "log a submittal", "submittal log", "submittal tracker", "shop drawings", "product data", "submittal status", "what submittals are pending", "what submittals are overdue", "submit shop drawings", "approve a submittal", "reject a submittal", "submittal due date", "spec section submittal", or any request involving construction submittals tracking.
version: 1.0.0
tags: [construction, submittals, shop-drawings, tracking]
---

# Submittals Tracker

## Overview

Tracks every submittal on every active project — shop drawings, product data, samples, mock-ups — through its lifecycle: required → submitted → under review → approved / approved-as-noted / revise-and-resubmit / rejected. LindaAI flags what's overdue, what's blocking the schedule, and what needs a chase email. Pair it with `/linda-mail` to draft the chase.

## When This Skill Applies

- User wants to log a new submittal or update one
- User asks "what submittals are pending / overdue?"
- User says "approve submittal {N}" or "reject submittal {N}"
- User wants the submittal log for a project
- User wants to know which submittals are blocking work

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Determine Action

| User Says | Action |
|-----------|--------|
| "Log a submittal" | Create new entry |
| "Update submittal {N}" | Modify status / dates |
| "Show submittals" / "submittal log" | Read and report |
| "What's overdue?" | Filter for overdue |
| "Chase {N}" | Generate chase email via `/linda-mail` |

### Step 2: Submittal Schema

Stored at `brain/projects/{slug}/submittals/_log.json`:
```json
{
  "submittals": [
    {
      "number": "03-300-001",
      "spec_section": "03 30 00 — Cast-in-Place Concrete",
      "title": "Concrete mix design 4000psi",
      "submitted_by": "ABC Concrete Co",
      "date_required_by": "2026-03-15",
      "date_submitted": "2026-03-12",
      "date_returned": "2026-03-18",
      "status": "approved-as-noted",
      "reviewer": "Architect",
      "blocks": ["Foundation pour"],
      "notes": "Reduce slump per architect note 2",
      "current_revision": 1
    }
  ]
}
```

Status values: `required` · `submitted` · `under-review` · `approved` · `approved-as-noted` · `revise-and-resubmit` · `rejected`

### Step 3: Auto-Number

Format: `{spec-section}-{NNN}`. Example: `26-05-00-003` for the 3rd submittal under Common Work Results for Electrical.

### Step 4: Overdue Logic

A submittal is overdue if:
- `status` ∈ {required, submitted, under-review} **and**
- today > `date_required_by`

A submittal is "blocking" if it has any value in `blocks` and isn't `approved` / `approved-as-noted`.

### Step 5: Reporting

When asked for the log:

```markdown
# Submittal Log — {Project} (as of {date})

## Open / Pending
| # | Spec | Title | Status | Required By | Days | Blocks |
|---|------|-------|--------|-------------|------|--------|
| 03-300-002 | Concrete | Reinforcing shop dwgs | submitted | 2026-04-25 | 5 over 🔴 | Foundation pour |
| 26-05-001 | Electrical | Panelboards | under-review | 2026-05-10 | 10 to go | — |

## Recently Closed
| # | Title | Status | Returned |
|---|-------|--------|----------|
| 03-300-001 | Concrete mix | approved-as-noted | 2026-03-18 |

## Flags
- 🔴 03-300-002 is 5 days overdue and blocks the foundation pour
- 🟡 09-650-001 has been "under-review" for 18 days

🤠 *Tracked by LindaAI* 🏇
```

### Step 6: Cross-Skill Hooks

- Overdue submittal → offer `/linda-mail` to draft a chase
- Blocking submittal → flag in `/linda-jobhealth`
- New submittal → optionally append to `/linda-projecttrack` schedule notes

## Example Usage

**User:** "Log a submittal — Maple Ridge, spec 09 65 00 resilient flooring, product data, due 5/15."

**LindaAI:** "Let's gooooooo Boss." Creates `09-65-00-001`, status=required, saves to log. "Yeeee Hawww 🤠 — logged. Reminder will fire if we hit 5/15 without submission."

**User:** "What's overdue on Westside Plaza?"

**LindaAI:** Reads log, filters, replies with the overdue table and recommends chase emails.

**User:** "Approve 26-05-001 with notes — clarify circuit IDs."

**LindaAI:** Updates status to `approved-as-noted`, saves return date, appends note.

## Voice & Tone

- Country, direct. **Boss.**
- Urgent voice on overdue/blocking — Boss has a schedule to protect.

## Error Handling

- **Spec section unknown:** Ask Boss for the section number, accept free-text fallback.
- **Submittal already exists:** Ask if this is a resubmission (increment `current_revision`).
- **No project:** Ask which project.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
