---
name: linda-rfi
description: This skill should be used when the user asks to "create an RFI", "log an RFI", "request for information", "RFI for {project}", "track RFIs", "RFI log", "ball in court", "RFI response", "submit RFI to architect", "RFI status", "open RFIs", "answer an RFI", "RFI cost impact", "draft an RFI", or any request involving construction Request for Information documentation and tracking.
version: 1.0.0
tags: [construction, rfi, project-management, documentation]
---

# RFI Tracker

## Overview

Creates and tracks Requests for Information (RFIs) — the formal questions a contractor sends the architect or engineer when drawings, specs, or field conditions don't line up. LindaAI drafts a clean, numbered RFI, logs it, tracks whose court the ball is in, flags cost or schedule impact, and keeps a running RFI log so nothing falls through the cracks (which is exactly how change orders and delays sneak up on a job).

## When This Skill Applies

- User says "create an RFI" or "draft an RFI for {project}"
- A drawing conflict, spec gap, or field condition needs an official answer
- User wants to log, track, or check the status of open RFIs
- User asks "whose court is it in" / "ball in court"
- User wants to record an answer and close an RFI

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Gather RFI Inputs

Required:
| Field | Example |
|-------|---------|
| Project | Maple Ridge Apartments |
| RFI number | auto: next sequential per project (RFI-015) |
| Subject | Conflict between structural and MEP at Grid C-4 |
| Question | Plumbing riser at C-4 conflicts with beam per S-201. Reroute or revise beam? |
| Reference | Drawing S-201, A-301; Spec 22 11 00 |
| Discipline | Structural / MEP / Architectural / Civil |
| Date submitted | today |
| Date response needed by | (ask — drives the schedule-impact flag) |

Optional but valuable:
- Suggested solution (contractors who propose a fix get faster, cheaper answers)
- Cost impact: Yes / No / TBD
- Schedule impact: Yes / No / TBD

### Step 2: Draft the RFI
Produce a professional RFI document with: project + RFI number, to/from, subject, the question stated clearly and neutrally, references, suggested solution, and impact flags. Save it to the project and produce a branded PDF ready to send.

### Step 3: Log It
Append to the project RFI log:
| RFI # | Subject | Submitted | Needed By | Ball in Court | Status | Cost? | Sched? |
|-------|---------|-----------|-----------|---------------|--------|-------|--------|
| 015 | C-4 conflict | 06/14 | 06/21 | Architect | Open | TBD | TBD |

### Step 4: Track & Close
- "Whose court?" → report all open RFIs grouped by ball-in-court, oldest first, with days outstanding.
- "Answer RFI 15" → record the response, attach it, set Status = Answered/Closed, and **flag if the answer creates a change** ("This answer adds scope — want me to start a Change Order? See linda-changeorder").

## Hard Rules
- Never invent an answer to an RFI — RFIs are questions TO the design team; LindaAI drafts and tracks them, it does not answer on the architect's behalf.
- Always flag cost/schedule impact so nothing becomes a surprise CO.
- Keep the question neutral and factual — no blame, just the conflict and the ask.

## Handoffs
- Answer adds scope → **linda-changeorder** (turn it into a CO)
- Delay from a slow answer → **linda-schedule** (log the impact)
- Send the RFI → **linda-mail**

---
*LindaAI Construction PM Pack — Built by Daniel Wise*
