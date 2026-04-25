---
name: linda-outreach
description: This skill should be used when the user asks to "write a letter to a seller", "draft seller outreach", "seller letter", "direct mail", "cold call script", "voicemail script for sellers", "text message to seller", "email to seller", "seller outreach", "draft outreach for motivated sellers", "pre-foreclosure letter", "probate letter", "absentee owner letter", "tired landlord outreach", "driving for dollars follow-up", "handwritten letter template", "yellow letter", "seller lead follow-up", "wholesale outreach", "acquisition outreach", "reach out to this property owner", "write something to send this seller", "batch outreach for seller list", "seller communication", "how to approach this seller", or any request involving drafting personalized communication to property owners/sellers to acquire real estate.
version: 1.0.0
---

# Seller Outreach Drafter

## Overview

LindaAI drafts personalized outreach to property sellers across every communication channel: physical letter, text message, voicemail drop script, email, and cold call script. Each piece is tailored to the seller's specific situation (pre-foreclosure, probate, absentee owner, tired landlord, divorce, code violations, tax delinquent, estate, etc.) with empathy, a clear value proposition, and a soft call to action. No sleazy "We Buy Houses" templates -- LindaAI crafts situation-aware communications that build trust and get responses. Supports batch generation for multiple properties on a list.

## When This Skill Applies

- User wants to reach out to a specific property owner about buying their property
- User has a list of seller leads and needs outreach drafted
- User says "write a letter to this seller" or "draft outreach"
- User needs a cold call script for motivated sellers
- User wants a voicemail script to leave for property owners
- User needs text/SMS messages for seller leads
- User is doing driving for dollars and needs follow-up material
- User has pre-foreclosure, probate, or tax-delinquent leads
- User asks for a "yellow letter" or direct mail piece
- User wants batch outreach for a list of addresses

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

### Step 0: Gather Seller Information

Parse what the user provided:

| Input | Required | Example |
|-------|----------|---------|
| Property address | Yes | 4521 Elm St, Dallas TX |
| Owner name | Helpful (not required) | "John Smith" or unknown |
| Seller situation | Yes | Pre-foreclosure, probate, absentee, tired landlord, tax delinquent, code violation, vacant, divorce, estate, inherited, downsizing, relocating |
| Communication channel | Helpful | Letter, text, voicemail, email, cold call, or "all" |
| Buyer identity | Yes | User's name, company, phone, credibility points |
| Tone preference | Optional | Professional, friendly, direct, compassionate |
| Batch mode? | Optional | Single property or list of multiple |

If seller situation is unknown, ask. The situation drives the entire tone and angle. If truly unknown, default to a general "exploring options" approach.

### Step 1: Research the Situation (if address provided)

> 🤠 "Hold tight — heading over yonder to gather up the details."

Use WebSearch to gather context:

**Search queries:**
- `"{full address}" property records owner`
- `"{full address}" foreclosure` (if pre-foreclosure)
- `"{full address}" code violation {city}"`
- `"{full address}" tax delinquent"`
- `"{county} {state} probate records"` (if probate)
- `"{full address}" vacant property"`

**Context to gather:**
- Owner name (if not provided)
- How long they've owned the property
- Any liens, judgments, or lis pendens
- Estimated equity position
- Last sale price and date
- Current condition indicators
- Any public records that reveal motivation

### Step 2: Determine Outreach Angle

Each seller situation requires a different emotional and strategic approach:

**Pre-Foreclosure**
- Tone: Urgent but compassionate. No judgment.
- Angle: "I may be able to help you avoid foreclosure and protect your credit."
- Key: Emphasize speed, discretion, and credit protection. They feel shame — be gentle.
- Avoid: Using the word "foreclosure" in texts/letters (can feel like an attack). Use "situation with your property" or "I noticed your home may need attention."

**Probate / Inherited**
- Tone: Respectful, patient, helpful.
- Angle: "I understand you inherited a property and may not want the burden of managing it."
- Key: Acknowledge the loss. Don't rush. Offer to handle everything.
- Avoid: Appearing opportunistic. Never mention "profiting from their loss."

**Absentee Owner**
- Tone: Casual, curious, opportunity-focused.
- Angle: "I'm interested in properties in this neighborhood. Would you consider selling yours?"
- Key: They own but don't live there. Might be tired of managing from a distance.
- Avoid: Assuming they want to sell. Ask, don't tell.

**Tired Landlord**
- Tone: Empathetic, relatable.
- Angle: "Being a landlord isn't always what people expect. If you're ready for a break, I buy properties as-is."
- Key: Mirror their frustration. Tenant horror stories are real. Offer relief.
- Avoid: Belittling their situation. Validate, then offer the exit.

**Tax Delinquent**
- Tone: Helpful, informational, no judgment.
- Angle: "I help property owners resolve tax situations. There may be options you haven't considered."
- Key: They may not know they're at risk of tax sale. Be the informer, not the predator.
- Avoid: Threatening language or urgency that feels like pressure.

**Code Violations**
- Tone: Neighborly, solution-oriented.
- Angle: "I noticed your property at [address] and I work with properties in this area. I'd be happy to take it off your hands as-is."
- Key: They may be facing fines and overwhelmed. Position as relief.
- Avoid: Mentioning specific violations (feels like surveillance).

**Vacant Property**
- Tone: Curious, low-pressure.
- Angle: "I drive through this neighborhood regularly and noticed your property appears unoccupied. I'm always looking for opportunities in this area."
- Key: Imply local presence and genuine interest. They may have forgotten about it.

**Divorce**
- Tone: Sensitive, practical.
- Angle: "I work with families going through transitions who need to sell property quickly and fairly."
- Key: Both parties may need to agree. Offer simplicity in a complex time.
- Avoid: Mentioning divorce directly unless they do first. Use "life transition" or "change in circumstances."

**General / Unknown Situation**
- Tone: Friendly, exploratory.
- Angle: "I'm an active buyer in your area and I'm reaching out to see if you've ever considered selling [address]."
- Key: Simple, no assumptions. Let them reveal their situation.

### Step 3: Draft Physical Letter

Two styles available:

**Professional Letter (typed, on letterhead)**

```
[Your Name]
[Your Company]
[Your Address]
[Your Phone] | [Your Email]

[Date]

[Owner Name]
[Owner Mailing Address — may differ from property address]

RE: [Property Address]

Dear [Owner Name / "Property Owner"],

[OPENING — 1-2 sentences that acknowledge their situation without being
presumptuous. Create connection.]

[BODY — 2-3 sentences about who you are, what you do, and how you can
help. Be specific to their situation. Include a credibility marker:
"I've worked with XX families in [city]" or "I've been investing in
this neighborhood for X years."]

[VALUE PROPOSITION — What makes working with you different:
- Buy as-is, no repairs needed
- Flexible closing timeline (their schedule)
- No commissions or fees
- Handle all paperwork
- Discreet and private
- Cash or creative terms available]

[SOFT CTA — Not "call me NOW" but "if you'd ever like to explore your
options, I'm a quick phone call away." Leave the door open.]

[SIGN-OFF]

Sincerely,

[Your Name]
[Phone Number]
[Email]

P.S. [A P.S. always gets read. Put your strongest hook here.
Example: "Even if you're not ready now, I'm happy to give you a
no-obligation estimate of what your property is worth today."]
```

**Handwritten-Style Letter (yellow letter / personal note)**

```
[Date]

Hi [Owner Name / "Neighbor"],

I hope this letter finds you well. My name is [Name]
and I've been looking at properties in [neighborhood/area].

I came across your property at [address] and I wanted
to reach out personally to see if you'd ever consider
selling.

I'm not a big corporation — I'm a local [investor/buyer]
who [credibility statement]. I buy properties in any
condition and I work on YOUR timeline.

No pressure at all. If you're even a little curious,
give me a call or text at [phone]. I'm happy to chat.

Thanks for your time,
[Name]
[Phone]
```

### Step 4: Draft Text Message / SMS

Short, personal, non-spammy. Texts get the highest response rates.

**First touch:**
```
Hi [Name], this is [Your Name]. I was looking at properties in [neighborhood/area] and came across [address]. Would you ever consider an offer on it? No pressure either way — just thought I'd ask. Thanks!
```

**Follow-up #1 (3-5 days later, no response):**
```
Hey [Name], just circling back on [address]. I know you're busy — just wanted to see if selling is something you'd ever consider. I buy in any condition and can close on your timeline. Let me know either way!
```

**Follow-up #2 (7-10 days later, still no response):**
```
Hi [Name], last time I'll bug you about [address]. If the timing isn't right, totally understand. If things ever change, feel free to reach out — my number's always open. Have a great week!
```

**If they respond with interest:**
```
Great to hear from you! I'd love to learn more about the property. Would it be easier to chat on the phone for a few minutes, or would you prefer I send over some info first? Whatever works best for you.
```

**If they respond "not interested":**
```
Totally understand, [Name]. Appreciate you letting me know. If anything changes down the road, don't hesitate to reach out. Wishing you all the best!
```

### Step 5: Draft Voicemail Script

30-45 seconds max. Warm, human, not robotic.

```
"Hi [Name], this is [Your Name] — I'm a local real estate buyer
in [city/area]. I'm reaching out because I was looking at
properties in your neighborhood and I came across [address].

I wanted to see if you'd ever consider selling. I buy properties
in any condition, and I can work on whatever timeline works for you.

No pressure at all — just thought it was worth a conversation.

If you're open to chatting, you can reach me at [phone number].
That's [repeat phone number].

Thanks, [Name]. Have a great [day/evening]."
```

Keep it natural. Pause between sentences. Smile while you talk (it changes your tone).

### Step 6: Draft Email

```
Subject: Quick question about [Property Address]

Hi [Name],

My name is [Your Name] and I'm a real estate buyer active in [city/area].

I came across your property at [address] and I wanted to reach out to see if you'd ever consider selling — either now or in the future.

A little about how I work:
• I buy properties as-is (no repairs or cleaning needed)
• I cover all closing costs
• Flexible timeline — we close when it works for YOU
• No realtor commissions or hidden fees
• I can offer cash or creative financing terms

[Situation-specific paragraph: tailor to their circumstance]

I understand if the timing isn't right. But if you're even a little curious about what your property might be worth or what your options look like, I'm happy to have a no-obligation conversation.

You can reply to this email, call or text me at [phone], or just let me know and I'll reach out at a time that's convenient.

Thanks for your time, [Name].

Best,
[Your Name]
[Phone]
[Email]
[Website — e.g., sellfi.io]
```

### Step 7: Draft Cold Call Script

Conversational framework, not a word-for-word script. Natural flow.

```
OPENING (first 10 seconds — make or break):
"Hi, is this [Name]? Hey [Name], this is [Your Name].
I'm calling about your property at [address] — do you have
just a minute?"

[If YES, continue. If "who is this?" — re-introduce warmly.
If "not interested" — "Totally understand. If anything changes,
I'm always just a phone call away. Have a great day!"]

RAPPORT (15-20 seconds):
"I appreciate you taking my call. I'm a [local investor / real estate
buyer] in [city] and I've been looking at properties in your area.
I came across [address] and just wanted to reach out to see if
selling is something you've ever thought about."

[LISTEN. Let them talk. Their response tells you everything.]

QUALIFY (ask questions, don't pitch):
"How long have you owned the property?"
"Are you living there currently or is it [rented/vacant]?"
"Is there anything going on with the property that's been a headache?"
"Have you thought about what you'd want for it?"
"Is there a timeline you're working with?"

[Key: Ask questions. The more they talk, the more you learn.
Mirror their language. If they say "I'm just tired of dealing with it,"
say "Yeah, I hear that a lot — being a landlord isn't easy."]

TRANSITION (if they show interest):
"Based on what you're telling me, I think there might be a way
I can help. Here's what I typically do — I'd take a look at the
property, look at the numbers, and make you a fair offer.
No obligation, no pressure. If it works for both of us, great.
If not, no hard feelings."

CLOSE (set next step):
"Would it make sense for me to come take a look at the property
this [day]? Or if you prefer, I can put together a preliminary
offer based on what I know and send it over for you to look at."

[Always end with a specific next step. Never end with "I'll follow up."]

OBJECTION HANDLING:
- "I need to think about it" → "Of course. Can I check back with you
  [specific day]? I don't want to be a pest, but I also don't want
  you to miss out if the timing works."
- "I'm working with a realtor" → "No problem! If that doesn't work
  out, keep my number. I can close faster and with fewer hassles."
- "Your offer is too low" → "I understand. What number would work for
  you? Let me see if I can make it work on my end."
- "I'm not interested" → "Totally get it. Mind if I ask — is it the
  timing, or you just don't want to sell at all? [If timing:] Would
  it be okay if I checked back in a few months?"
```

### Step 8: Save All Outreach Materials

Save to a property-specific folder:

```
~/Desktop/lindaai/output/seller-outreach/{address-slug}/
├── letter-professional.md
├── letter-handwritten.md
├── text-messages.md
├── voicemail-script.md
├── email.md
├── cold-call-script.md
└── README.md
```

For batch mode (multiple properties), create a subfolder for each:
```
~/Desktop/lindaai/output/seller-outreach/batch-{date}/
├── 123-main-st/
├── 456-oak-ave/
└── 789-elm-blvd/
```

## Output Format

Each file is a standalone markdown document ready to use. The README indexes everything:

```markdown
# Seller Outreach Package: {Address}
**Created:** {date}
**Owner:** {name if known}
**Situation:** {pre-foreclosure, probate, etc.}
**Channels:** Letter, Text, Voicemail, Email, Cold Call

## Files
1. letter-professional.md — Formal typed letter
2. letter-handwritten.md — Personal handwritten-style note
3. text-messages.md — Initial text + 2 follow-ups + response templates
4. voicemail-script.md — 30-second voicemail drop script
5. email.md — Professional email outreach
6. cold-call-script.md — Conversational cold call framework

---
🤠 *Generated by LindaAI* 🏇
```

## Example Usage

**Single property:**
"Draft outreach for 1422 Maple Dr, Memphis TN 38108. Owner is Patricia Williams. She's an absentee owner — lives in California, property has been vacant for 8 months. I want all channels. My info: Mike Davis, TOP Wheels, 555-123-4567, mike@sellfi.io"

**Batch mode:**
"I've got 5 pre-foreclosure leads. Draft text messages and letters for all of them:
1. 204 Pine St, Atlanta GA — owner James Brown
2. 891 Cedar Ln, Atlanta GA — owner unknown
3. 1547 Birch Ave, Decatur GA — owner Maria Santos
4. 322 Spruce Dr, College Park GA — owner Dwayne Mitchell
5. 610 Willow Ct, East Point GA — owner unknown"

**AI generates personalized outreach for each property**, adjusting tone for pre-foreclosure (compassionate, time-sensitive, helpful) and personalizing with owner names where available. Unknown owners get "Property Owner" with slightly more exploratory language.

## Error Handling

- **If the user does not provide a property address:** Ask: "What property address are you targeting? I need at least a street address and city/state."
- **If the user does not provide the seller's situation:** Ask: "What is the seller's situation? (Pre-foreclosure, probate, absentee owner, tired landlord, tax delinquent, vacant, divorce, or unknown) This determines the tone and angle of every communication piece."
- **If the owner's name is unknown:** Use "Property Owner" in all materials. Adjust language to be more exploratory and less personal. Note: "Using 'Property Owner' since the name is unknown. If you can find the owner's name through county records or a skip trace service, the response rate will be significantly higher."
- **If the user does not provide their own contact info (name, phone, email):** Ask: "I need your contact info for the outreach materials. At minimum: your name and phone number. Company name and email are helpful too."
- **If WebSearch is unavailable for property/owner research:** Skip the research step and proceed with user-provided data only. Note: "I couldn't research the property online. The outreach is based on the info you provided. If you have additional details (ownership length, estimated equity, liens), share them and I'll personalize further."
- **If the output directory does not exist:** Create `~/Desktop/lindaai/output/seller-outreach/{address-slug}/` automatically before saving files.
- **If outreach materials already exist for this address:** Ask: "Outreach materials already exist for this address. Should I overwrite them (maybe the situation changed), or create a follow-up sequence that builds on the first round?"
- **If batch mode has more than 20 properties:** Process in batches of 10 and inform: "Processing {total} properties in batches. Batch 1 of {N} complete. Continuing..." This prevents overwhelming output.
- **If the seller's situation is sensitive (divorce, probate, pre-foreclosure) and the user requests aggressive language:** Push back: "I've softened the tone for this outreach. {Situation} sellers respond much better to empathy and patience than pressure. Aggressive tactics in this situation will likely get zero responses and could damage your reputation."
- **If the user asks to actually send the messages (text, email):** Tell the user: "I wrangle up the outreach -- but sending ain't my rodeo. Copy the texts into your phone, the emails into your client, and print the letters. For batch texting, consider a platform like Launch Control or BatchLeads."


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
