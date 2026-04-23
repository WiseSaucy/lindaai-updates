---
name: networking-intel
description: This skill should be used when the user asks to "research attendees", "prep for a networking event", "who should I meet at", "event prep", "networking prep", "conference prep", "who's going to", "research these people", "prepare for this event", "event intelligence", "pre-event research", "who should I talk to", "attendee research", "networking strategy", "event strategy", "who are the key people at", "prep my networking", "conference intelligence", "summit prep", "build target profiles", "who should I prioritize meeting", "networking targets", "conversation starters for", "follow-up templates", "post-event follow-up", "event planning", "who to meet at this event", "research these attendees", "attendee profiles", "event brief", "networking brief", "pre-event intel", or any request involving preparing for a networking event, researching attendees, creating target profiles, building event strategies, or generating follow-up communications for people met at events.
version: 1.0.0
---

# Networking Intel

## Overview

LindaAI's pre-event intelligence preparation turns you from "another person in the room" into the most prepared person at the event. Provide an event name and an attendee list (or event URL), and the AI researches key attendees, builds target profiles (who they are, what they do, mutual connections, conversation starters), prioritizes who to meet based on your goals, creates a full event strategy (arrival timing, session recommendations, after-party positioning), and generates personalized follow-up templates for each target. This is how executives with $180K/year chiefs of staff walk into every room knowing exactly who matters and what to say — and now LindaAI brings that same firepower to you.

## When This Skill Applies

- User is attending a conference, summit, meetup, or networking event
- User has an attendee list and wants profiles on key people
- User asks "who should I meet at {event}?"
- User wants conversation starters for specific people
- User asks for event strategy or conference prep
- User wants post-event follow-up templates
- User says "prep me for {event}" or "research these people"
- User provides a list of names and wants intel on each
- User mentions an upcoming event and wants to maximize their time there
- User asks "how should I work the room at {event}?"

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

### Step 0: Gather Event Details

Parse what the user provided. Required inputs (ask for anything missing):

| Input | Required | Example |
|-------|----------|---------|
| Event name | Yes | "Squad Up Summit", "RE Investors Meetup", "TechCrunch Disrupt" |
| Event date(s) | Yes | "March 11", "March 11-13" |
| Event location | Helpful | "Los Angeles", "Marriott Downtown Phoenix" |
| Attendee info | Yes (one of these) | List of names, event URL, speaker list, attendee PDF |
| User's goals for the event | Helpful | "Find investors", "recruit students", "close 3 deals", "build brand visibility" |
| User's business context | Auto-loaded | From `brain/goals.md`, CLAUDE.md, user identity files |

If the user provides an event URL:
- Use WebSearch/WebFetch to pull the event page
- Extract: speakers, sponsors, agenda/schedule, attendee companies (if listed), registration info

If the user provides a list of names:
- Research each name individually

If the user provides nothing but the event name:
- Search for the event online, pull whatever public info exists (speakers, sponsors, past attendees)
- Note: "I found {X} public names associated with this event. For a more targeted prep, share the attendee list if you have access to it."

### Step 1: Research Key Attendees

> 🤠 "Hold tight — heading over yonder to gather up the details."
For each target person, research using WebSearch:

**Search queries per person:**
- `"{full name}" {company or role}` — identity confirmation
- `"{full name}" LinkedIn` — professional background
- `"{full name}" {industry keywords}` — industry presence
- `"{full name}" interview OR podcast OR keynote` — public appearances and viewpoints
- `"{full name}" {event name}` — their connection to this specific event

**Build a profile for each person:**

| Field | What to Find |
|-------|-------------|
| Full Name | Confirmed spelling and pronunciation notes if unusual |
| Title / Role | Current position and company |
| Company | What their company does, size, stage |
| Background | Career trajectory (2-3 sentences) |
| Notable | What they are known for (awards, media, deals, thought leadership) |
| Online Presence | LinkedIn, Twitter/X, website, podcast, YouTube |
| Recent Activity | Last 90 days: posts, news, interviews, announcements |
| Mutual Connections | Anyone in `brain/people/` who knows them or works in the same space |
| Relevance to You | Why this person matters for the user's goals (be specific) |
| Conversation Starters | 3 specific, non-generic openers based on their recent activity |
| What They Want | Best guess at their goals/pain points based on research |
| How You Can Help | What the user can offer them (based on user's business and expertise) |

### Step 2: Prioritize Targets

Not everyone at the event is equally worth your time. Rank attendees into tiers:

**Tier 1 — Must Meet (3-5 people)**
These are the people you came for. Meeting them alone makes the event worth attending.

Criteria for Tier 1:
- Direct alignment with your top quarterly goal
- Decision-maker level (can write checks, sign deals, or open doors)
- Mutual value exchange is clear (you can help them AND they can help you)
- Time-sensitive opportunity (they are launching something, hiring, investing)

**Tier 2 — Should Meet (5-10 people)**
Strong networking targets with clear potential value.

Criteria for Tier 2:
- Aligned with your business but not an immediate deal
- Potential referral source or strategic connection
- Industry influencer or community leader
- Could become Tier 1 with one good conversation

**Tier 3 — Nice to Meet (everyone else)**
Worth a handshake and a card exchange if the opportunity arises.

### Step 3: Build the Event Strategy

```markdown
## Event Strategy

### Your Mission
{One sentence: what does success look like when you leave this event?}
**Goal:** {specific, measurable: "Leave with 3 investor meetings scheduled" or "Sign up 5 new students"}

### Before the Event
- [ ] Review all Tier 1 profiles (this document)
- [ ] Connect with Tier 1 targets on LinkedIn with a personal note before the event
- [ ] Post on social media that you're attending (attracts inbound connections)
- [ ] Prepare your 30-second intro: who you are, what you do, what you're looking for
- [ ] Prepare your "ask" for each Tier 1 target (specific, not vague)
- [ ] Bring: business cards, phone charged, portable charger, breath mints

### Arrival Strategy
- **Arrive:** {15-30 min early — first impressions happen in the lobby, not the main room}
- **Position:** {Near the registration/check-in area — meet people as they arrive}
- **First 30 min:** {Scan the room, identify Tier 1 targets, approach the most accessible one}
- **Body language:** Open stance, no phone, make eye contact, smile

### Session Strategy (if conference)
| Session | Time | Why Attend | Target Connection |
|---------|------|-----------|-------------------|
| {session name} | {time} | {reason — speaker is Tier 1, topic aligns with pitch, networking before/after} | {who to connect with here} |

**Skip sessions where:** The content is available online later OR no target connections are in the room. Use that time for 1:1 conversations instead.

### Networking Blocks
| Time | Strategy | Who to Target |
|------|----------|--------------|
| Registration/check-in | Work the line, introduce yourself to people waiting | Anyone — warm up |
| Morning coffee/breaks | Position near the coffee — everyone goes there | Tier 2 targets |
| Lunch | Sit at a table with people you don't know — introduce yourself | Tier 1 if possible |
| Afternoon breaks | Follow up with morning connections, trade contact info | Tier 1 and 2 |
| Happy hour/after-party | This is where real deals happen. Stay. | Tier 1 — alcohol loosens gatekeeping |
| Dinner (if applicable) | Organize or join a small group dinner | Tier 1 targets + 2-3 warm connections |

### Conversation Playbook

**Opening (pick one per target — see individual profiles for personalized versions):**
- "I saw your {recent post/talk/article} on {topic} — {specific observation or question}."
- "I'm working on {your thing} and I think there's overlap with what you're doing at {their company}."
- "{Mutual connection} mentioned I should find you here."
- "What brought you to {event}?" (simple but opens the door)

**Bridging to business (after 2-3 min of personal connection):**
- "What are you working on right now that you're most excited about?"
- "What's the biggest challenge you're facing with {their area}?"
- "I'm building {your thing} — I'd love to get your perspective on {specific question}."

**Closing (always leave with a next step):**
- "I'd love to continue this conversation — can I grab your number/email?"
- "Let me send you {that resource/article/intro I mentioned}. What's the best email?"
- "Would you be open to a 15-minute call next week to explore {specific topic}?"
- Exchange cards, take a photo together (creates a memory anchor and social proof content)

**Exit gracefully (when a conversation should end):**
- "I don't want to monopolize your time — great meeting you. Let's connect after the event."
- "I need to catch {speaker/session} — let me grab your info before I go."
```

### Step 4: After-Party and Evening Intel

If the event has evening activities:

```markdown
### After-Hours Intel
- **Official after-party:** {venue, time, dress code, who's likely there}
- **Unofficial gatherings:** {common spots — hotel lobby bar, nearby restaurants where attendees congregate}
- **VIP/speaker dinner:** {if known — how to get an invite or adjacent to it}
- **Strategy:** {where to go and why — this is where the real deals happen}
```

### Step 5: Generate Follow-Up Templates

Create a personalized follow-up template for each Tier 1 and Tier 2 target:

```markdown
## Follow-Up Templates

### Follow-Up Protocol
- **Within 24 hours:** Send initial follow-up to everyone you exchanged info with
- **Within 48 hours:** Send the personalized Tier 1 follow-ups below
- **Within 1 week:** Connect on LinkedIn with a personal note
- **Within 2 weeks:** Schedule any promised calls or meetings

### Tier 1 Follow-Ups

#### {Person Name} — {Company}
**Subject:** Great connecting at {event} — {specific reference}

{First name},

{Reference something specific from your conversation — proves you were paying attention.}

{Brief value proposition — what you mentioned you could help with or share.}

{Specific next step — "Would Thursday at 2pm work for a quick call?" or "Here's the link to {resource} I mentioned."}

Looking forward to it.

{Your name}
{Your title}
{Your phone}

---

#### {Next Person}...

### Tier 2 Follow-Up (General Template)

**Subject:** Good to meet you at {event}

{First name},

Great connecting at {event}. {One specific thing you discussed or found interesting about their work.}

{One sentence about what you do — keep it brief, they may not remember details.}

Would love to stay connected — {specific, low-commitment next step: "feel free to reach out if you ever need help with X" or "I'll keep you in mind if I come across Y"}.

Best,
{Your name}

### LinkedIn Connection Note (Universal)

Hi {first name} — great meeting you at {event}! {One line reference to your conversation.} Let's stay connected.
```

### Step 6: Compile and Save the Event Brief

```markdown
# Networking Intel: {Event Name}

> **Event:** {name}
> **Date(s):** {dates}
> **Location:** {venue, city}
> **Your Goal:** {specific mission}
> **Prepared:** {today's date}

---

## Target Profiles

### Tier 1 — Must Meet

#### 1. {Full Name}
| Field | Details |
|-------|---------|
| Title | {title at company} |
| Company | {company — what they do} |
| Background | {2-3 sentences} |
| Notable | {what they're known for} |
| Online | {LinkedIn, Twitter, website} |
| Recent Activity | {last 90 days — posts, news, deals} |
| Mutual Connections | {anyone in brain/people/ or industry} |
| Relevance to You | {specific reason to connect} |
| What They Want | {their likely goals/pain points} |
| How You Can Help | {your value proposition for them} |

**Conversation Starters:**
1. "{Opener based on their recent activity}"
2. "{Opener based on mutual interest/connection}"
3. "{Opener based on their known challenge/goal}"

**Your Ask:** {What specifically do you want from this interaction?}

---

#### 2. {Full Name}...

### Tier 2 — Should Meet

{Same format, slightly condensed}

### Tier 3 — Nice to Meet (Brief List)

| Name | Title | Company | Why |
|------|-------|---------|-----|

---

## Event Strategy
{From Step 3}

---

## Session Recommendations
{From Step 3 — which sessions to attend and which to skip}

---

## After-Hours Intel
{From Step 4}

---

## Follow-Up Templates
{From Step 5}

---

## Post-Event Checklist
- [ ] Send Tier 1 follow-ups within 24 hours
- [ ] Send Tier 2 follow-ups within 48 hours
- [ ] Connect on LinkedIn with everyone (within 1 week)
- [ ] Add new contacts to `brain/people/` CRM
- [ ] Schedule all promised calls/meetings
- [ ] Post event recap on social media (within 24 hours — tag new connections)
- [ ] Debrief: What worked? What would you do differently? (log to `brain/daily/`)
- [ ] Update `brain/goals.md` with any new opportunities or connections that shift priorities

---

🤠 *Generated by LindaAI* 🏇
```

Save to: `brain/research/networking-{event-slug}-{YYYY-MM-DD}.md`

## Example Usage

**User:** "Prep me for the Squad Up Summit on March 11 — here's the attendee list: Pace Morby, Jamil Damji, Mike Banks, Brent Daniels, Jerry Green"

**AI:** Researches each person. Pace Morby — SubTo community founder, real estate educator, 2M+ social following, recently launched a new mastermind. Prioritizes based on user's goals from goals.md (SellFi launch, T.O.P. Method). Creates Tier 1/2/3 rankings, conversation starters specific to each person's recent activity, event strategy for the Summit, and personalized follow-up emails. Saves to `brain/research/networking-squad-up-summit-2026-03-03.md`.

**User:** "/networking-intel RE Investors Meetup https://www.meetup.com/phoenix-re-investors/events/12345"

**AI:** Fetches the event page, pulls the RSVP list and organizer info. Researches the organizer and any notable RSVPs. Creates a lighter-weight briefing (fewer targets for a meetup vs. a major conference) focused on who to introduce yourself to and what to say. Generates follow-up templates.

**User:** "Research these 3 people for me: John Smith (ABC Capital), Sarah Lee (XYZ Ventures), Tom Jackson (123 Properties)"

**AI:** Not tied to a specific event, but builds the same target profiles. Researches each person, finds their background, recent activity, and relevance to the user's business. Provides conversation starters and outreach templates. Saves as a networking intel file.

**User:** "Who should I meet at TechCrunch Disrupt this year?"

**AI:** Searches for TechCrunch Disrupt speaker list, sponsor companies, and notable attendees from prior years. Cross-references against user's goals (AI, SaaS, fintech). Builds target profiles for the top 10 most relevant people to seek out.

**User:** "I met these people at the event — help me follow up: Pace Morby (talked about SubTo partnership), Mike Banks (interested in SellFi demo)"

**AI:** Generates highly personalized follow-up emails for each person, referencing the specific conversation topic. Suggests timing and channel (email vs. text vs. LinkedIn) for each follow-up. Creates brain/people/ entries for each new contact.

## Error Handling

- **If no event name is provided:** Ask: "What event are you preparing for? Give me the name, date, and any attendee info you have."
- **If no attendee info is provided:** Search for the event online and pull any public attendee/speaker lists. Note: "I found {X} speakers/sponsors publicly listed. For a more targeted prep, share the attendee list — even a partial one helps."
- **If the event URL does not load or has no useful data:** Report: "I couldn't pull attendee data from that URL. It may require a login or the data isn't public. Can you copy-paste the attendee names directly?"
- **If WebSearch returns no results for a person:** Note: "I couldn't find public information on {name}. They may have a low online presence. If you have their company or LinkedIn URL, that would help. Otherwise, I'll prepare a general icebreaker for them."
- **If the user provides a very large attendee list (50+ names):** Focus research on the top 15-20 based on title/company relevance to the user's goals. Note: "That's a big list. I've prioritized the top {X} based on alignment with your goals. Want me to research anyone specific I may have deprioritized?"
- **If `brain/goals.md` does not exist:** Ask the user directly: "What are your goals for this event? I need this to prioritize who you should meet." Proceed with their stated goals.
- **If `brain/people/` does not exist:** Create it when adding post-event contacts. Skip the mutual connections check during pre-event research.
- **If `brain/research/` directory does not exist:** Create it before saving.
- **If the event is today or tomorrow (short notice):** Skip the "1 week before" prep items. Focus on target profiles, conversation starters, and the event strategy. Note: "Short notice — I've focused on the most actionable intel. Review the Tier 1 profiles and conversation starters before you walk in."


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
