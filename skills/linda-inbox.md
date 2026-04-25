---
name: linda-inbox
description: This skill should be used when the user says "inbox triage", "triage my inbox", "sort my emails", "process my emails", "help with emails", "email triage", "inbox zero", "clear my inbox", "go through my messages", "prioritize my emails", "what should I respond to", "urgent emails", "email prioritization", "message triage", "sort these messages", "process these messages", "which emails matter", "inbox management", "email management", "help me with my inbox", "what needs a response", "batch my emails", "email batch", "DM triage", "message prioritization", or wants to process a batch of emails, messages, or communications and have them categorized by urgency with draft responses for the most important ones.
version: 1.0.0
---

# Inbox Triage — Executive-Level Communication Processing

## Overview

Inbox Triage takes the chaos of your inbox and turns it into an ordered action plan in minutes. You paste in emails, describe your messages, or provide inbox context -- LindaAI categorizes each item by urgency, drafts responses for the critical ones, creates action items for the important ones, and tells you what to ignore. This is what a world-class executive assistant does every morning before you even look at your phone: LindaAI filters signal from noise so you only spend time on what actually matters.

## When This Skill Applies

- User says "inbox triage" or "triage my inbox" or "sort my emails"
- User says "process my emails" or "help with emails" or "email triage"
- User says "inbox zero" or "clear my inbox" or "inbox management"
- User says "go through my messages" or "prioritize my emails"
- User says "what should I respond to" or "what needs a response"
- User says "DM triage" or "message triage" or "sort these messages"
- User says "batch my emails" or "email batch"
- User triggers the `/inbox-triage` command
- User pastes email content and asks for help prioritizing or responding

## Category

Never Drop a Ball

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

### Step 1: Receive the Inbox

The user provides inbox content in one of these ways:

**Option A: Pasted emails/messages**
User copies and pastes one or more emails directly. May include headers (From, Subject, Date) or just the body text.

**Option B: Described inbox state**
User describes what's in their inbox: "I have 15 unread emails — 3 from clients, one from my CPA, a bunch of newsletters, and something from a lawyer about the LLC."

**Option C: MCP email integration**
If Gmail or other email MCP is connected, AI can read the inbox directly. (Note: This requires the MCP server to be configured.)

**Option D: Screenshot/forwarded summary**
User shares a screenshot or summarized list of subjects and senders.

If the user just says "inbox triage" with no content, tell the user: "Paste your emails or describe what's in your inbox, and I'll sort 'em by priority and wrangle up draft responses for the urgent ones."

### Step 2: Gather Context

Before triaging, check the brain for context:

1. `brain/people/README.md` — Are any senders in the CRM? If yes, read their files for relationship context.
2. `brain/goals.md` — What are the current priorities? Emails aligned with goals get priority boost.
3. `brain/projects/README.md` — Are any emails related to active projects?
4. `brain/pipeline/follow-ups.md` — Are any emails responses to follow-ups you're tracking?

This context transforms triage from generic sorting into priority-aware filtering tuned to the user's actual business.

### Step 3: Categorize Each Item

Sort every email/message into one of four categories:

| Category | Symbol | Criteria | Action Required |
|----------|--------|----------|----------------|
| **URGENT** | 🔴 | Revenue at stake, deadline within 24h, key relationship, time-sensitive opportunity, legal/financial risk | Respond NOW — AI drafts response |
| **IMPORTANT** | 🟡 | Needs response today, active project related, client communication, partner/investor contact | Respond TODAY — AI creates action item |
| **LOW PRIORITY** | 🟢 | Can wait 2-3 days, informational, not time-sensitive, batch-processable | Batch later — brief note on what to do |
| **IGNORE** | 🗑️ | Newsletters you don't read, spam, irrelevant notifications, marketing from services | Delete or unsubscribe — no action needed |

**Categorization rules (in order of priority):**
1. Money on the table (deal closing, invoice, payment) → 🔴 URGENT
2. Key relationship communication (investors, partners, top clients) → 🔴 or 🟡
3. Deadline-driven (something expires, closes, or is due) → 🔴 URGENT
4. Active project related → 🟡 IMPORTANT
5. General business correspondence → 🟡 or 🟢
6. Informational only (no response needed) → 🟢 LOW
7. Marketing, newsletters, automated notifications → 🗑️ IGNORE
8. If sender is in brain/people/ with 🔴 priority → bump up one category

### Step 4: Draft Responses for URGENT Items

For every 🔴 URGENT item, draft a complete response:

**Response principles:**
- Match the sender's tone and formality level
- Be direct — get to the point in the first sentence
- Include a clear next step or call to action
- Keep it concise — busy people appreciate brevity
- If a decision is needed, present it clearly
- If the user's brain has context on this person/project, use it

**Response format:**
```
DRAFT RESPONSE — [Subject]
To: [Sender]
───────────────────────────
[Draft response body]
───────────────────────────
Notes: [Any context the user should know before sending]
```

### Step 5: Create Action Items for IMPORTANT Items

For every 🟡 IMPORTANT item, create a specific action item:

- What to do
- Who it involves
- Suggested deadline
- Whether it should become a follow-up in `brain/pipeline/follow-ups.md`

### Step 6: Generate the Triage Report

Compile the complete triage report in the output format below.

### Step 7: Offer Next Actions

After presenting the triage:
- "Want me to save these action items to your follow-up tracker?"
- "Want me to adjust any of the draft responses?"
- "Should I flag any of these people for your CRM (brain/people/)?"

## Output Format

```
================================================================
  INBOX TRIAGE — [Today's Date]
  [X] items processed | [X] urgent | [X] important | [X] low | [X] ignore
================================================================

🔴 URGENT — Respond Now
═══════════════════════

1. FROM: [Sender Name] — [Subject/Topic]
   WHY URGENT: [One sentence explaining why this is urgent]

   DRAFT RESPONSE:
   ─────────────────────────────────────────
   [Complete draft response ready to send]
   ─────────────────────────────────────────
   NOTES: [Any context — e.g., "This person is in your CRM as a key investor"]

2. FROM: [Sender Name] — [Subject/Topic]
   WHY URGENT: [Reason]

   DRAFT RESPONSE:
   ─────────────────────────────────────────
   [Draft response]
   ─────────────────────────────────────────

🟡 IMPORTANT — Respond Today
═════════════════════════════

3. FROM: [Sender Name] — [Subject/Topic]
   ACTION: [Specific action to take]
   DEADLINE: [When to respond by]

4. FROM: [Sender Name] — [Subject/Topic]
   ACTION: [Specific action]
   DEADLINE: [When]

🟢 LOW PRIORITY — Batch Later
══════════════════════════════

5. FROM: [Sender Name] — [Subject/Topic]
   NOTE: [Brief note on what to do, if anything]

6. FROM: [Sender Name] — [Subject/Topic]
   NOTE: [Brief note]

🗑️ IGNORE — Delete or Unsubscribe
═══════════════════════════════════

7. [Sender] — [Subject] — [Reason to skip: newsletter, spam, irrelevant]
8. [Sender] — [Subject] — [Reason]

────────────────────────────────────
ACTION ITEMS CREATED:
────────────────────────────────────
- [ ] [Action from item #1]
- [ ] [Action from item #3]
- [ ] [Action from item #4]

FOLLOW-UPS TO ADD:
- [Person] — [Commitment] — due [date]

PEOPLE TO ADD TO CRM:
- [New contact] — [Role/context]
════════════════════════════════════
```

## Handling Different Input Formats

### Raw pasted emails (with headers)
Parse From, Subject, Date, and Body. Group threads together if multiple emails are from the same thread.

### Summarized descriptions
"3 from clients, 1 from CPA, bunch of newsletters"
Work with what's given. Ask follow-up questions only if the urgent items need more detail: "What did the CPA email say? That might be urgent depending on timing."

### Mixed formats
If the user pastes some emails and describes others, process all of them together. The output format stays the same regardless of input format.

### Screenshots
If the user describes what they see in a screenshot, work with the subject lines and sender names to categorize.

## Triage Modifiers

The user can customize the triage:

- **"Triage for this morning only"** — Focus on what needs response before noon
- **"Just the urgent stuff"** — Skip 🟢 and 🗑️ categories in the output
- **"Draft all responses"** — Draft responses for 🟡 items too, not just 🔴
- **"Focus on [client/project]"** — Filter to emails related to a specific person or project
- **"Mark everything from [sender] as important"** — Override categorization for specific senders

## Error Handling

- **If no emails/content provided:** Ask: "Paste your emails or describe what's in your inbox. I'll sort by priority and draft responses for the urgent ones."
- **If the content is too vague to categorize:** Ask targeted questions: "You mentioned an email from a lawyer — what's the subject? That could be urgent." Don't guess on potentially critical items.
- **If an email references a deal, person, or project not in the brain:** Process it anyway with a note: "This mentions [name/project] which isn't in your brain yet. Want me to add them?"
- **If the inbox is extremely large (30+ items):** Process in batches of 10. Show the 🔴 URGENT items first: "I've found [X] urgent items — here are those first. Want me to continue processing the rest?"
- **If all items are low priority:** Tell the user straight: "Nothing urgent in the corral. [X] items can be batched. [X] can be deleted. Your inbox is clean -- no action needed right now."
- **If the user's email tone/brand voice is known (from brain/knowledge-base/):** Match it in draft responses. If not, default to professional but direct.
- **If an email seems like phishing or a scam:** Flag it: "This looks suspicious — [reason]. Do NOT click any links or respond. Mark as spam."

## Example Usage

**User:** "Inbox triage — here are my unread emails:

1. From: David Park — Subject: 'Ready to close on Oak Street' — says he has proof of funds ready, wants to know when we can schedule signing
2. From: LinkedIn — 3 connection requests
3. From: Sarah Chen — Subject: 'Q1 numbers look good' — sharing preliminary fund performance, asks for your input by end of week
4. From: QuickBooks — Your subscription is renewing March 15
5. From: Unknown sender — Subject: 'Exclusive investment opportunity' — wants me to invest in some crypto fund
6. From: Marcus (CPA) — Subject: 'Need your Q4 receipts ASAP' — says extension deadline is approaching, needs docs by March 7"

**AI checks brain:**
- David Park is in people/ as active buyer
- Sarah Chen is in people/ as business partner (🔴 priority)
- Marcus is in people/ as CPA

**AI output:**

```
================================================================
  INBOX TRIAGE — March 3, 2026
  6 items processed | 2 urgent | 1 important | 1 low | 2 ignore
================================================================

🔴 URGENT — Respond Now
═══════════════════════

1. FROM: David Park — "Ready to close on Oak Street"
   WHY URGENT: Active buyer ready to close. Money on the table. Delay = risk of losing the deal.

   DRAFT RESPONSE:
   ─────────────────────────────────────────
   David,

   Great news on the proof of funds. Let's get this scheduled.

   I'm available [Wednesday or Thursday] this week for signing.
   Does either work on your end? I'll coordinate with the title
   company once we lock a date.

   Talk soon,
   [Your Name]
   ─────────────────────────────────────────
   NOTES: David is in your CRM — active buyer, Oak Street deal. This is revenue. Respond within the hour.

2. FROM: Marcus (CPA) — "Need your Q4 receipts ASAP"
   WHY URGENT: Tax deadline approaching. March 7 is 4 days out. Financial/legal risk if missed.

   DRAFT RESPONSE:
   ─────────────────────────────────────────
   Marcus,

   On it. I'll have Q4 receipts organized and sent over by
   Wednesday (March 5) at the latest. If there are specific
   categories you need first, let me know and I'll prioritize those.

   Thanks for the heads up.
   ─────────────────────────────────────────
   NOTES: This is also in your follow-ups as overdue. Block 1 hour tomorrow to gather receipts.

🟡 IMPORTANT — Respond Today
═════════════════════════════

3. FROM: Sarah Chen — "Q1 numbers look good"
   ACTION: Review the Q1 performance data she shared. Send thoughtful input by end of week (March 7).
   DEADLINE: Respond by Thursday March 6 (gives buffer before her Friday deadline)

🟢 LOW PRIORITY — Batch Later
══════════════════════════════

4. QuickBooks — Subscription renewing March 15
   NOTE: No action unless you want to cancel or change plan. File and forget.

🗑️ IGNORE — Delete or Unsubscribe
═══════════════════════════════════

5. LinkedIn — 3 connection requests — Batch process next time you're on LinkedIn
6. Unknown sender — "Exclusive investment opportunity" — Likely spam/scam. Do not engage. Delete.

────────────────────────────────────
ACTION ITEMS CREATED:
────────────────────────────────────
- [ ] Respond to David Park re: Oak Street closing — TODAY
- [ ] Gather and send Q4 receipts to Marcus — by March 5
- [ ] Review Sarah's Q1 numbers and send input — by March 6

FOLLOW-UPS TO ADD:
- Marcus (CPA) — Send Q4 receipts — due March 5
- Sarah Chen — Send Q1 input — due March 6
════════════════════════════════════
```

## Cost Estimate

| Scenario | Estimated Cost |
|----------|---------------|
| Triage 5-10 items with draft responses | $0.08–$0.20 |
| Triage 10-20 items with drafts | $0.15–$0.40 |
| Large inbox (30+ items, full drafts) | $0.30–$0.75 |

## What Makes This Premium

A CEO's time is worth $500-$2,000/hour. Spending 45 minutes sorting through emails, deciding what matters, and writing responses is a $500-$1,500 waste of that time. A $180K/year executive assistant's core daily function is inbox management: categorizing, prioritizing, drafting responses, and only escalating what actually needs the boss's brain. This skill does that job in under 2 minutes. It doesn't just sort — it thinks about your priorities, checks your CRM, considers your goals, and drafts responses that sound like you. The difference between spending an hour in your inbox and spending 5 minutes reviewing pre-sorted, pre-drafted communications is the difference between a reactive operator and a strategic CEO.

---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
