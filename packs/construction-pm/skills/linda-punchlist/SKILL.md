---
name: linda-punchlist
description: This skill should be used when the user asks to "create a punch list", "punch list", "punchlist", "walkthrough list", "deficiency list", "snag list", "punch items", "close out punch", "assign punch items", "punch list for {project}", "final walkthrough", "punch status", "% punch complete", "verify punch items", or any request involving construction punch list / closeout deficiency tracking.
version: 1.0.0
tags: [construction, punch-list, closeout, quality, project-management]
---

# Punch List Manager

## Overview

Builds and runs the punch list — the running list of deficiencies and unfinished items found on a walkthrough that have to be fixed before a job closes out and final payment is released. LindaAI captures items by area, assigns each to the right trade or sub, tracks open → fixed → verified, reports percent complete, and generates a clean closeout report. A tight punch list is the difference between getting paid on time and chasing retainage for months.

## When This Skill Applies

- User says "create a punch list" or "start the punch for {project}"
- After a walkthrough, owner/architect review, or pre-final inspection
- User wants to assign deficiency items to subs/trades
- User asks for punch status, % complete, or a closeout report
- User wants to verify/close items as they're fixed

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Set Up the List
Capture: Project, walkthrough date, who walked it (owner / architect / PM / inspector).

### Step 2: Capture Items
For each deficiency (ask or accept a dump and structure it):
| # | Location | Trade | Description | Severity | Photo Ref | Assigned To | Due |
|---|----------|-------|-------------|----------|-----------|-------------|-----|
| 1 | Unit 204 bath | Plumbing | Faucet leaks at base | Medium | IMG_2207 | ABC Plumbing | 06/20 |
| 2 | Lobby | Paint | Touch-up scuffs east wall | Low | — | In-house | 06/19 |

Severity: **High** (blocks occupancy/safety) · **Medium** (must-fix) · **Low** (cosmetic).

### Step 3: Assign by Trade
Group items by trade/sub and produce a per-sub punch sheet they can work from. ("Send ABC Plumbing their 6 items" → linda-mail.)

### Step 4: Track to Closeout
- Status per item: **Open → Fixed (by trade) → Verified (by PM)**.
- "Punch status" → % complete overall + by trade, open High-severity items first.
- An item is only **Closed** when verified by the PM, not when the sub says it's done.

### Step 5: Closeout Report
When all items are Verified, generate a branded Punch List Completion Report (project, date opened, date closed, total items, sign-off line) — the document that supports releasing retainage / final payment.

## Hard Rules
- "Done" by a sub ≠ closed. Only PM verification closes an item.
- Always surface open **High-severity** items loudly — those block occupancy or final.
- Keep photo references so disputes get settled by evidence, not memory.

## Handoffs
- Send trade their items → **linda-mail**
- All verified → trigger final invoice / retainage release → **linda-invoice**
- Recurring defect from one sub → note it in **linda-subs** (performance)

---
*LindaAI Construction PM Pack — Built by Daniel Wise*
