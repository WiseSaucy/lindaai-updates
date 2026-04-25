---
name: linda-onboard
description: This skill should be used when the user asks to "onboard a new client", "set up a new client", "new client", "onboard client", "client onboarding", "set up {name} as a client", "new client intake", "add a new client", "bring on a new client", "client setup", "start working with a new client", "welcome a new client", "new client checklist", "onboarding workflow", "client intake", "prepare for a new client", "set up everything for a new client", or anything related to initiating a new client relationship — including creating their contact record, project file, welcome materials, and onboarding checklist.
version: 1.0.0
---

# Client Onboarding

## Overview

LindaAI handles the full new client onboarding workflow -- just hand over the basic client information and everything gets set up for a successful working relationship. In one pass, LindaAI creates: a contact entry in the people directory, a project file for their work, a welcome email draft, an onboarding checklist, and an initial meeting agenda. Everything is cross-linked so client context is always a quick lookup away.

## When This Skill Applies

- User signs a new client and needs to set everything up
- User says "onboard {client name}" or "new client: {name}"
- User asks to set up files for a new client
- User needs a welcome email drafted for a new client
- User wants to create an onboarding checklist
- User mentions client intake or client setup
- User says "I'm starting to work with {name}" in a client context

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

### Step 1: Gather Client Information

Extract from the user's message (ask for essentials if missing, skip non-essentials):

**Essential:**
| Field | Description |
|-------|-------------|
| Client Name | Full name of the primary contact |
| Company/Entity | Business name (if applicable) |
| Service/Engagement | What you are doing for them |

**Helpful but Optional:**
| Field | Description | Default |
|-------|-------------|---------|
| Email | Primary email | "TBD — ask during first call" |
| Phone | Primary phone | "TBD" |
| Address | Mailing/billing address | "TBD" |
| How They Found You | Referral, social, website, etc. | "Not specified" |
| Engagement Value | Dollar value of the deal/contract | "TBD" |
| Start Date | When the engagement begins | Today's date |
| Key Dates | Any important deadlines | None |
| Special Notes | Preferences, requirements, context | None |

### Step 2: Create Contact Entry

Create `brain/people/{firstname-lastname}.md` using this structure:

```markdown
# {Full Name}

> **Role:** Client
> **Company:** {company}
> **Status:** Active
> **Since:** {YYYY-MM-DD}
> **Priority:** {High if active engagement}

## Contact Info

| Field | Value |
|-------|-------|
| Email | {email} |
| Phone | {phone} |
| Address | {address} |
| Preferred Contact | {email/phone/text} |

## Relationship Context

- **How they found us:** {source}
- **Engagement:** {what we are doing for them}
- **Value:** ${amount}
- **Start Date:** {date}

## Key Notes

- {any special notes, preferences, or context}

## Interaction History

| Date | Type | Summary |
|------|------|---------|
| {today} | Onboarding | Client onboarded. Files created. |

## Linked Files

- Project: `brain/projects/{project-slug}.md`
- Invoices: `brain/invoices/{client-slug}/`
```

Update `brain/people/README.md` index to include the new contact.

### Step 3: Create Project File

Create `brain/projects/{client-slug}-{engagement-type}.md`:

```markdown
# {Client Name} — {Engagement Type}

> **Status:** In Progress
> **Priority:** High
> **Client:** {name} (`brain/people/{firstname-lastname}.md`)
> **Start Date:** {YYYY-MM-DD}
> **Target Completion:** {date or "Ongoing"}
> **Value:** ${amount}

## Scope

{Description of what is being delivered, key deliverables, and boundaries}

## Milestones

| # | Milestone | Target Date | Status |
|---|-----------|-------------|--------|
| 1 | Onboarding complete | {date} | In Progress |
| 2 | {milestone} | {date} | Not Started |
| 3 | {milestone} | {date} | Not Started |
| 4 | Final delivery / Close | {date} | Not Started |

## Tasks

- [ ] Complete onboarding checklist
- [ ] Send welcome email
- [ ] Schedule kickoff call
- [ ] {task specific to engagement}
- [ ] {task specific to engagement}

## Notes

- {date}: Client onboarded. Engagement initiated.

## Blockers

None currently.
```

Update `brain/projects/README.md` dashboard to include the new project.

### Step 4: Generate Welcome Email Draft

Create a professional welcome email saved to `brain/drafts/welcome-{client-slug}.md`:

```markdown
# Welcome Email — {Client Name}

> **To:** {client email}
> **Subject:** Welcome! Here's what to expect working with us

---

Hi {First Name},

Welcome aboard! I'm excited to start working together on {brief description of engagement}.

Here's what happens next:

**1. Kickoff Call**
We'll schedule a {30/60}-minute call to align on goals, timeline, and expectations. I'll send a calendar invite shortly.

**2. Information I'll Need From You**
To get started, I'll need a few things:
{bulleted list of items needed — documents, access, info, etc. Customize based on engagement type}

**3. How We'll Communicate**
{Communication preferences — email for formal, text/call for urgent, weekly check-ins, etc.}

**4. Timeline**
{Brief overview of key dates and milestones}

If you have any questions in the meantime, don't hesitate to reach out. Looking forward to getting results.

Best,
{User's name}
{User's title/company}
{Contact info}
```

### Step 5: Generate Onboarding Checklist

Create `brain/projects/{client-slug}-onboarding-checklist.md`:

```markdown
# Onboarding Checklist — {Client Name}

> **Created:** {date}
> **Target Completion:** {7-14 days from start}

## Pre-Kickoff

- [ ] Contact entry created in brain/people/
- [ ] Project file created in brain/projects/
- [ ] Welcome email sent
- [ ] Kickoff call scheduled
- [ ] Client info collected (email, phone, address)

## During Kickoff

- [ ] Goals and expectations aligned
- [ ] Timeline and milestones confirmed
- [ ] Communication preferences established
- [ ] Key contacts identified (if company has multiple stakeholders)
- [ ] Required documents/access requested

## Post-Kickoff

- [ ] Meeting notes filed
- [ ] Action items documented in project file
- [ ] First deliverable/milestone scheduled
- [ ] Follow-up email sent with meeting summary
- [ ] Invoice configuration set up (if applicable)

## Engagement-Specific Items

- [ ] {Custom item based on service type}
- [ ] {Custom item based on service type}
- [ ] {Custom item based on service type}

## Handoff to Active Work

- [ ] All onboarding items complete
- [ ] Client confirmed ready to proceed
- [ ] Project status updated to "Active"
- [ ] First milestone work initiated
```

### Step 6: Generate Initial Meeting Agenda

Create `brain/drafts/kickoff-agenda-{client-slug}.md`:

```markdown
# Kickoff Meeting Agenda — {Client Name}

> **Date:** {TBD — to be scheduled}
> **Duration:** 30-60 minutes
> **Attendees:** {User}, {Client Name}

---

## 1. Introductions and Context (5 min)
- Quick personal intros (if not already acquainted)
- How they found us / what prompted the engagement

## 2. Goals and Expectations (10 min)
- What does success look like for them?
- Primary goals for this engagement
- Any concerns or past experiences to be aware of

## 3. Scope and Deliverables (10 min)
- Confirm what is being delivered
- Clarify what is NOT included (boundaries)
- Walk through milestones and timeline

## 4. Process and Communication (10 min)
- How we will work together (tools, frequency, style)
- Preferred communication channel and response time expectations
- Who are the decision makers / points of contact
- How we handle changes or scope adjustments

## 5. Information and Access Needed (10 min)
- Documents, credentials, or data needed from the client
- Any third-party introductions required
- Timeline for providing these items

## 6. Next Steps (5 min)
- Confirm immediate action items for both sides
- Set the next check-in or milestone date
- Any questions?

---

## Post-Meeting Action Items

| # | Action | Owner | Due |
|---|--------|-------|-----|
| 1 | {action} | {who} | {when} |
| 2 | {action} | {who} | {when} |
| 3 | {action} | {who} | {when} |
```

### Step 7: Cross-Link Everything

Ensure all created files reference each other:
- Contact file links to project file and invoice folder
- Project file links to contact file
- Welcome email references are in the onboarding checklist
- All files use consistent client slug naming

### Step 8: Report What Was Created

Present a summary of everything created to the user.

## Output Format

```
CLIENT ONBOARDING COMPLETE — {Client Name}
============================================

Files Created:
  1. Contact:   brain/people/{firstname-lastname}.md
  2. Project:   brain/projects/{client-slug}-{type}.md
  3. Checklist: brain/projects/{client-slug}-onboarding-checklist.md
  4. Welcome:   brain/drafts/welcome-{client-slug}.md
  5. Agenda:    brain/drafts/kickoff-agenda-{client-slug}.md

Indexes Updated:
  - brain/people/README.md (contact added)
  - brain/projects/README.md (project added)

Next Steps:
  1. Review and send the welcome email
  2. Schedule the kickoff call
  3. Collect required info from the client
  4. Work through the onboarding checklist

Client Summary:
  - Name: {name}
  - Company: {company}
  - Engagement: {type}
  - Value: ${amount}
  - Start Date: {date}
```

## Example Usage

**User:** "Onboard John Martinez from Rivera Auto Group. He wants TC services for 3 vehicles. $2,000 per vehicle. His email is john@riveraauto.com."

**AI:** Creates all 5 files: contact entry with full info, project file scoped to 3 vehicle TCs at $6,000 total, welcome email referencing TC services, onboarding checklist customized for TC deals (adding items like "collect vehicle info sheets", "verify titles", "confirm buyer details"), and a kickoff agenda focused on vehicle details and timeline. Updates both README indexes. Reports everything created.

**User:** "New client: Sarah Chen, SellFi consulting engagement, $5K/month retainer"

**AI:** Creates full onboarding package for a consulting client. Adapts the checklist and agenda for a retainer-style engagement. Welcome email references monthly deliverables and check-in cadence.

**User:** "I just closed a deal with Marcus Thompson. Set everything up for him."

**AI:** Asks for minimal missing info (company, engagement type, contact details) then runs the full onboarding workflow.

**User:** "Bring on ABC Corp as a client — they need a full deal package"

**AI:** Creates contact entry for the company, project file for deal package work, and all onboarding materials. Adapts checklist to include deal-specific items (property info, seller details, financial docs).

## Files Created Summary

Every client onboarding creates exactly 5 files and updates 2 indexes:

| # | File | Location | Purpose |
|---|------|----------|---------|
| 1 | Contact Entry | `brain/people/{firstname-lastname}.md` | Full contact record with relationship context |
| 2 | Project File | `brain/projects/{client-slug}-{engagement-type}.md` | Scope, milestones, tasks, timeline |
| 3 | Welcome Email Draft | `brain/drafts/welcome-{client-slug}.md` | Ready-to-send welcome email (reads brand voice from CLAUDE.md) |
| 4 | Onboarding Checklist | `brain/projects/{client-slug}-onboarding-checklist.md` | Pre-kickoff, during kickoff, post-kickoff items |
| 5 | Kickoff Meeting Agenda | `brain/drafts/kickoff-agenda-{client-slug}.md` | Structured agenda for the first meeting |

**Indexes Updated:**
- `brain/people/README.md` — new contact added to index table
- `brain/projects/README.md` — new project added to dashboard table

## Onboarding Checklist Detail

The checklist includes these universal items (plus engagement-specific items added dynamically):

### Pre-Kickoff
- [ ] Contact entry created in brain/people/
- [ ] Project file created in brain/projects/
- [ ] Contract signed (or agreement in place)
- [ ] Payment received (initial deposit or first invoice)
- [ ] Access granted (any tools, portals, or shared resources)
- [ ] Kickoff call scheduled
- [ ] Welcome email sent
- [ ] Intro email sent to relevant team members

### During Kickoff
- [ ] Goals and expectations aligned
- [ ] Timeline and milestones confirmed
- [ ] Communication preferences established
- [ ] Key contacts identified
- [ ] Required documents/access requested

### Post-Kickoff
- [ ] Meeting notes filed
- [ ] Action items documented in project file
- [ ] First deliverable/milestone scheduled
- [ ] Follow-up email sent with meeting summary
- [ ] Invoice configuration set up (if applicable)

## Error Handling

- **If `brain/people/` or `brain/projects/` directories do not exist:** Create them automatically along with their README.md index files using the standard templates. Do not error — initialize silently.
- **If `brain/drafts/` directory does not exist:** Create it automatically before writing the welcome email and agenda files.
- **If user does not provide a client name:** Ask specifically: "What is the client's name? I need at least a first and last name to create their files."
- **If user does not provide an engagement type or service description:** Ask: "What type of work are you doing for this client? (e.g., consulting, TC services, deal coordination, etc.) This helps me customize the onboarding materials."
- **If a contact file already exists for this person:** Do not overwrite. Read the existing file and inform the user: "A contact entry already exists for {name}. I'll update their existing record with the new client engagement info rather than creating a duplicate." Then update the existing file to add the new engagement context.
- **If a project file already exists with the same slug:** Append a date or number suffix: `{client-slug}-{engagement-type}-2.md` or `{client-slug}-{engagement-type}-2026-03.md`. Inform the user.
- **If CLAUDE.md cannot be read for brand voice:** Fall back to a professional, direct tone for the welcome email. Note to user: "I couldn't read your CLAUDE.md for brand voice, so I used a professional default. Feel free to adjust the tone."
- **If the user provides partial info (missing email, phone, etc.):** Proceed with what is available. Fill missing fields with "TBD" in the contact entry. Note in the onboarding checklist: "[ ] Collect missing contact info: {list of missing fields}."
- **If `brain/people/README.md` or `brain/projects/README.md` cannot be updated (malformed, etc.):** Create the individual files anyway and warn: "I created all 5 files but couldn't update the {file} index. You may need to add the entry manually or run the command again."
- **If the user wants to onboard a company (not an individual):** Create the contact file using the company name as the filename (e.g., `abc-corp.md`) with a "Primary Contact" field. Adjust the welcome email salutation to address the primary contact person if known, or use the company name.
- **If the user cancels midway or asks to redo:** Any files already created remain in place. The user can re-run the command to regenerate specific files, or manually delete what they do not want.


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
