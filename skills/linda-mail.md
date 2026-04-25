---
name: linda-mail
description: This skill should be used when the user asks to "draft an email", "write an email", "email drafter", "compose an email", "write a message to", "email [name]", "send an email to", "draft a reply", "follow-up email", "cold email", "outreach email", "write a proposal email", "thank you email", "negotiation email", "introduction email", "professional email", "batch emails", "write multiple emails", "email template", "draft a cold outreach", "write a pitch email", "investor email", "partnership email", "help me email", or wants to draft any kind of professional email communication.
version: 1.0.0
---

# Email Drafter — Professional Email Composition

## Overview

Email Drafter writes professional, well-crafted emails for any business context. Powered by LindaAI, you describe who you're emailing, why, and the desired outcome -- and LindaAI produces a ready-to-send email matching the appropriate tone, length, and structure. Supports cold outreach, follow-ups, proposals, negotiations, introductions, thank-yous, deal communications, and more. Can batch-draft multiple emails in one session. Checks the brain for recipient context to personalize automatically.

## When This Skill Applies

- User says "draft an email" or "write an email" or "compose an email"
- User says "email [name] about [topic]"
- User says "write a follow-up to [name]"
- User says "cold email to [description of person]"
- User says "write an outreach email"
- User says "draft a proposal" or "write a pitch email"
- User says "thank you email" or "negotiation email"
- User says "introduction email" or "partnership email"
- User says "write a reply to [this email]"
- User says "batch emails" or "write multiple emails"
- User says "help me email [someone]"
- User says "investor email" or "sponsor email"
- User says "email template for [scenario]"

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

### Step 1: Gather Context

Determine from the user's request:

1. **Recipient:** Who is this going to? Name, role, company, relationship.
2. **Purpose:** What is the email trying to accomplish?
3. **Tone:** What tone is appropriate? (See tone guide below)
4. **Background:** What has happened before this email? (previous conversations, meetings, context)
5. **Desired Outcome:** What do you want the recipient to DO after reading? (reply, schedule a call, sign something, make a decision)
6. **Constraints:** Word count, formality level, specific things to include or avoid.

**Auto-personalization:** Check `brain/people/` for the recipient:
- If a file exists for this person, read it for:
  - Communication preferences ("hates long emails", "prefers bullet points")
  - Relationship context (how you know them, last interaction)
  - Current status (active deal, pending decision, new contact)
- If no file exists, use the context the user provides

### Step 2: Determine Email Type and Template

| Email Type | When to Use | Key Characteristics |
|-----------|-------------|-------------------|
| Cold Outreach | First contact, no prior relationship | Short, value-first, clear CTA, respect their time |
| Warm Outreach | Mutual connection or prior touchpoint | Reference the connection, personal, specific ask |
| Follow-Up | After meeting, call, or previous email | Reference the prior interaction, add value, advance the conversation |
| Proposal | Presenting an offer or partnership | Structured, clear terms, professional, benefits-focused |
| Negotiation | Discussing terms, pricing, deal structure | Firm but fair, clear position, leave room, professional |
| Thank You | Post-meeting, post-deal, appreciation | Genuine, specific (not generic), brief, forward-looking |
| Introduction | Connecting two people | Brief context for both sides, explain why, make it easy |
| Update/Status | Keeping someone informed | Clear, organized, no fluff, next steps |
| Request | Asking for something | Specific ask, easy to say yes, respectful of their time |
| Investor/Pitch | Seeking funding or partnership | Concise, traction-focused, clear ask, professional |
| Apology/Recovery | Handling a mistake or delay | Own it, explain briefly, state the fix, move forward |

### Step 3: Draft the Email

Structure every email with these components:

```
SUBJECT LINE: [Clear, specific, not clickbait. 5-10 words max.]

[Greeting — match the relationship. "Hey [First name]" for casual, "Hi [Name]" for professional, "[Name]," for direct]

[HOOK — First 1-2 sentences. Why should they keep reading? Reference something specific to them or the context.]

[BODY — The substance. Keep paragraphs short (2-3 sentences max). Use line breaks. Get to the point fast.]

[CTA — One clear ask. What should they do next? Make it easy to respond.]

[SIGN-OFF — Match the tone. "Best," / "Talk soon," / "—[Name]" / "Looking forward to it,"]
```

### Step 4: Apply Tone Rules

| Tone | When | How |
|------|------|-----|
| **Direct** | Colleagues, team, people who know you | Short sentences. No fluff. Get to the point. Sign off casual. |
| **Professional** | Business contacts, partners, formal contexts | Structured. Complete sentences. Polite but not stiff. |
| **Warm** | People you like, relationship-building | Personal touch. Reference shared context. Genuine closing. |
| **Authoritative** | Negotiations, establishing expertise | Confident language. Facts over feelings. Clear position. |
| **Deferential** | Investors, mentors, people above your level | Respectful of their time. Concise. Value-first. Easy CTA. |
| **Casual** | Friends, close contacts, informal | Conversational. Can be short. Personality shows. |

Default tone (when not specified): **Direct + Professional** — no-BS, clear, gets to the point but maintains professionalism.

### Step 5: Quality Check

Before presenting, verify:

- [ ] Subject line is specific and clear (not "Quick question" or "Following up")
- [ ] First sentence hooks them (not "I hope this email finds you well")
- [ ] Body is scannable (short paragraphs, line breaks)
- [ ] One clear CTA (not three competing asks)
- [ ] Length matches the context (cold emails: 50-150 words, proposals: 200-400 words)
- [ ] Tone matches the relationship
- [ ] No typos, no filler phrases, no corporate jargon
- [ ] Personalization is specific (not "I love what you're doing" — say what specifically)

### Step 6: Present the Email

Display the draft clearly:

```
---
**To:** [Recipient name and email if known]
**Subject:** [Subject line]
---

[Full email body]

---
**Type:** [Cold Outreach / Follow-Up / etc.]
**Tone:** [Direct / Professional / etc.]
**Word Count:** [X words]
**CTA:** [What you're asking them to do]
---
```

### Step 7: Handle Revisions

If the user wants changes:
- "Make it shorter" — Cut to essential points only
- "Make it warmer" — Add personal touches, soften language
- "More professional" — Remove casual language, add structure
- "Add [specific point]" — Weave it in naturally
- "Different subject line" — Provide 3 alternatives

### Step 8: Batch Mode

When the user needs multiple emails:
1. List all recipients and purposes
2. Draft each email separately
3. Present them numbered with clear labels
4. Allow individual revisions
5. Optionally save to a file for later reference

## Email Length Guidelines

| Scenario | Target Length | Why |
|----------|-------------|-----|
| Cold outreach | 50-100 words | Respect their time, earn the reply |
| Follow-up | 75-150 words | Brief, reference prior context, advance |
| Proposal | 200-400 words | Enough detail to decide, not a novel |
| Negotiation | 150-300 words | Clear position without rambling |
| Thank you | 50-100 words | Genuine and brief |
| Introduction | 75-150 words | Context for both sides, make it easy |
| Status update | 100-250 words | Organized, scannable, next steps |
| Investor pitch | 150-300 words | Traction, ask, next step |

## Phrases to NEVER Use

These are filler that weakens every email. The drafter avoids them:
- "I hope this email finds you well"
- "Just wanted to touch base"
- "Per my last email"
- "Just checking in"
- "I wanted to reach out"
- "Don't hesitate to reach out"
- "At the end of the day"
- "Synergy" / "leverage" / "circle back" (unless used very intentionally)
- "As per our conversation" (just reference what was discussed)

## Phrases That Work

- "Quick question about [specific thing]" (subject line)
- "Saw that you [specific observation]" (hook)
- "Here's what I'm thinking:" (transition to proposal)
- "Would [specific time/action] work?" (concrete CTA)
- "No pressure if the timing is off" (removes friction)
- "Three things to know:" (scannable structure)

## Output Format

The drafted email is presented inline, ready to copy-paste. For batch emails, all drafts are presented numbered. Emails are not saved to files unless the user requests it — they are presented in the conversation for immediate use.

If the user wants them saved: write to `brain/daily/{YYYY-MM-DD}.md` under a "Drafted Emails" section, or to a standalone file.

## Example Usage

**User:** "Draft an email to Marcus about the TC agreement — he needs to sign it by Friday"

**AI checks:** `brain/people/marcus.md` for context (TC candidate, $500/deal fee, interested)

**AI drafts:**
```
Subject: TC Agreement Ready — Need Your Signature by Friday

Hey Marcus,

Good talking yesterday. The TC agreement is ready for your signature.

I'm sending it through Dropbox Sign — you should see it in your inbox shortly. Three key points:
- $500/deal fee structure (as we discussed)
- Standard TC responsibilities and timeline expectations
- 30-day trial period to make sure it's a fit for both of us

Need your signature by Friday so we can get you started next week.

Any questions, shoot me a text.

—Mike
```

**User:** "Cold email to a car dealership owner about seller financing through SellFi"

**AI drafts:** A short, value-first outreach explaining how seller financing could increase their sales volume, with a clear CTA to schedule a 15-minute call.

**User:** "Write 3 follow-up emails — one for the investor I met at the conference, one for the event organizer about the demo slot, and one for John about the AV setup"

**AI drafts:** Three separate emails, each personalized with context from the brain if available, appropriate tone for each relationship.

## Error Handling

- **If the user does not specify a recipient:** Ask: "Who is this email going to? I need at least a name (and ideally their email address and context)."
- **If the user does not specify the purpose or desired outcome:** Ask: "What's the goal of this email? What do you want them to DO after reading it? (Reply, schedule a call, sign something, make a decision, etc.)"
- **If the recipient has no entry in `brain/people/`:** Proceed with whatever context the user provides. Do not block on missing CRM data. Tell the user: "I don't have {name} in the ol' contacts roundup, so I'm working with what you gave me. Want me to saddle up a new contact entry?"
- **If the user asks to "send" the email:** Clarify that this skill drafts emails only -- it does not send them. Tell the user: "I've wrangled up that draft for you. Copy it into your email client and fire it off when you're ready. Sending ain't in my wheelhouse just yet."
- **If the user wants to reply to an existing email but does not provide the original:** Ask: "Can you paste the email you're replying to? I need to see it to write a relevant response."
- **If the user asks for a tone that conflicts with the context (e.g., "casual" for an investor pitch):** Draft it as requested but flag: "You asked for a casual tone, but this is an investor pitch — usually those work better with a professional tone. I drafted it casual as you asked. Want a professional version too?"
- **If the user provides contradictory instructions (e.g., "keep it short" and then lists 10 points to include):** Prioritize the most important points and note: "You asked me to keep it short, but you gave me 10 points. I included the top 5 for a tight email. The remaining points could go in a follow-up or attachment. Want me to include everything instead?"
- **If the user wants emails saved to a file:** Save to `brain/drafts/email-{recipient-slug}-{YYYY-MM-DD}.md`. Create `brain/drafts/` if it does not exist.


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
