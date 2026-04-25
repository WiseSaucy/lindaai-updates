---
name: linda-hire
description: This skill should be used when the user asks to "hire someone", "hiring screener", "write a job description", "create a job posting", "interview questions", "screening questions", "hiring workflow", "build a hiring process", "I need to hire a", "help me hire", "find a [role]", "job description for", "interview scorecard", "onboarding checklist", "new hire onboarding", "offer letter template", "candidate profile", "ideal candidate", "red flags in hiring", "green flags in hiring", "hiring plan", "recruitment process", "hiring pipeline", "screen candidates", "vet candidates", "interview prep for hiring", "what to ask in an interview", "build a job post", "write a listing", "role description", "hire a VA", "hire an assistant", "hire a contractor", or wants to create any part of a hiring workflow from job description through onboarding.
version: 1.0.0
---

# Hiring Screener — Full Hiring Workflow Builder

## Overview

Hiring Screener is LindaAI's full-service hiring toolkit. It builds the complete hiring pipeline for any role. The user describes the position they need to fill — in as much or as little detail as they want — and LindaAI generates a professional job description, ideal candidate profile, 10 tailored screening questions, interview scorecard, red and green flags to watch for, offer letter template, and a new-hire onboarding checklist. Designed for entrepreneurs and small business owners who do not have an HR department but need to hire like they do.

## When This Skill Applies

- User says "I need to hire a [role]" or "help me hire"
- User says "write a job description" or "create a job posting"
- User says "interview questions for [role]"
- User says "screening questions" or "hiring screener"
- User says "interview scorecard" or "candidate evaluation"
- User says "onboarding checklist" or "new hire onboarding"
- User says "offer letter" or "offer letter template"
- User says "ideal candidate profile" or "what should I look for in a [role]"
- User says "red flags in hiring" or "green flags"
- User says "hiring plan" or "hiring workflow" or "recruitment process"
- User says "hire a VA" or "hire a contractor" or "hire an assistant"
- User says "build a job post" or "write a listing"
- User mentions needing to fill a role or grow their team

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

### Step 1: Define the Role

Gather from the user's request:

1. **Role title:** What is the position called?
2. **Role type:** Full-time, part-time, contract, freelance, internship?
3. **Remote/on-site:** Where does this person work?
4. **Responsibilities:** What will they actually DO day-to-day?
5. **Reports to:** Who manages them?
6. **Budget:** Salary range or hourly rate (if the user is willing to share)
7. **Urgency:** When do they need someone by?
8. **Industry context:** What does the user's business do? (Check brain/goals.md and brain/projects/)
9. **Team size:** How big is the current team? Is this the first hire, or adding to an existing team?
10. **Must-haves vs. nice-to-haves:** What is non-negotiable versus what would be a bonus?

If the user gives a short description ("I need a VA to handle my inbox and calendar"), expand it into a full role spec using industry standards for that position.

### Step 2: Generate the Job Description

```markdown
## Job Description

### [Role Title]

**Company:** [Company name from brain context or user input]
**Location:** [Remote / On-site / Hybrid — City, State]
**Type:** [Full-time / Part-time / Contract / Freelance]
**Compensation:** [Range or "Competitive, based on experience"]
**Reports To:** [Title]

---

#### About Us
[2-3 sentences about the company. Pull from brain/knowledge-base/ if available. If not, draft from user context. Focus on mission and culture, not a Wikipedia entry.]

#### The Role
[2-3 sentences describing WHY this role exists and what success looks like. Not a task list — the big picture.]

#### What You Will Do
- [Responsibility 1 — action verb, specific, outcome-oriented]
- [Responsibility 2]
- [Responsibility 3]
- [Responsibility 4]
- [Responsibility 5]
- [Responsibility 6 — stretch goal or growth area]

#### What You Bring
**Required:**
- [Requirement 1 — specific skill or experience]
- [Requirement 2]
- [Requirement 3]
- [Requirement 4]

**Preferred (Nice-to-Haves):**
- [Nice-to-have 1]
- [Nice-to-have 2]
- [Nice-to-have 3]

#### What We Offer
- [Benefit 1 — compensation, equity, bonuses]
- [Benefit 2 — flexibility, remote work, schedule]
- [Benefit 3 — growth opportunity, mentorship, learning]
- [Benefit 4 — culture, team, mission-driven work]

#### How to Apply
[Instructions — email, application link, what to include (resume, portfolio, cover letter, specific task)]
```

Job description principles:
- Lead with what the candidate gets, not what you demand
- Avoid buzzwords ("rockstar", "ninja", "guru", "wear many hats")
- Be specific — "manage social media" is vague, "create and schedule 20 posts/week across Instagram and TikTok" is clear
- Include compensation range if possible — it attracts better candidates and saves time
- Keep requirements honest — do not list 10 years of experience for a junior role

### Step 3: Build the Ideal Candidate Profile

```markdown
## Ideal Candidate Profile

### The Person (Not Just the Resume)

**Background:** [Career trajectory that would prepare someone for this role. What kind of experience matters most?]

**Mindset:** [What kind of thinker are they? Self-starter? Detail-oriented? Big-picture? Scrappy?]

**Work Style:** [How do they work best? Independently? Collaboratively? Fast-paced? Methodical?]

**Communication:** [How should they communicate? Written-first? Phone-friendly? Comfortable with async?]

**Motivation:** [What drives them? Money? Mission? Growth? Flexibility? Autonomy?]

### Hard Skills (Can Be Tested)
1. [Skill — how to verify it]
2. [Skill — how to verify it]
3. [Skill — how to verify it]
4. [Skill — how to verify it]
5. [Skill — how to verify it]

### Soft Skills (Must Be Observed)
1. [Soft skill — what it looks like in practice]
2. [Soft skill — what it looks like in practice]
3. [Soft skill — what it looks like in practice]

### Non-Negotiables
- [Absolute requirement 1 — if they do not have this, do not hire them]
- [Absolute requirement 2]
- [Absolute requirement 3]

### Bonus Points
- [Bonus 1 — would accelerate their impact]
- [Bonus 2]
```

### Step 4: Create 10 Screening Questions

Develop 10 questions across four categories: experience, situational, behavioral, and culture fit.

```markdown
## Screening Questions

### Experience (Do they have the skills?)
1. **[Question about relevant experience]**
   - *What a great answer sounds like:* [Description]
   - *Red flag answer:* [Description]

2. **[Question about specific technical skill]**
   - *What a great answer sounds like:* [Description]
   - *Red flag answer:* [Description]

3. **[Question about industry knowledge]**
   - *What a great answer sounds like:* [Description]
   - *Red flag answer:* [Description]

### Situational (Can they think on their feet?)
4. **"You are given [realistic scenario for this role]. What do you do first?"**
   - *What a great answer sounds like:* [Description]
   - *Red flag answer:* [Description]

5. **"A client/customer is unhappy about [common problem]. Walk me through how you handle it."**
   - *What a great answer sounds like:* [Description]
   - *Red flag answer:* [Description]

6. **"You realize you are going to miss a deadline. What steps do you take?"**
   - *What a great answer sounds like:* [Description]
   - *Red flag answer:* [Description]

### Behavioral (How have they actually performed?)
7. **"Tell me about a time you [relevant challenge for this role]."**
   - *What a great answer sounds like:* [Description]
   - *Red flag answer:* [Description]

8. **"Describe a project or task you are most proud of. What made it successful?"**
   - *What a great answer sounds like:* [Description]
   - *Red flag answer:* [Description]

### Culture Fit (Will they thrive here?)
9. **"What kind of work environment brings out your best work?"**
   - *What a great answer sounds like:* [Description]
   - *Red flag answer:* [Description]

10. **"What does accountability mean to you?"**
    - *What a great answer sounds like:* [Description]
    - *Red flag answer:* [Description]

### Bonus Question (The Differentiator)
11. **"If I gave you this job today, what would you do in the first 30 days?"**
    - *What a great answer sounds like:* [They have a plan, have researched the company, show initiative]
    - *Red flag answer:* [Vague, no preparation, waits to be told what to do]
```

Question design principles:
- Never ask "What is your greatest weakness?" or other cliche interview questions
- Situational questions must use realistic scenarios for THIS specific role
- Behavioral questions use "tell me about a time" format — past behavior predicts future behavior
- Include what a great answer AND a red flag answer look like so the interviewer knows how to evaluate
- The bonus question separates good candidates from great ones

### Step 5: Build the Interview Scorecard

```markdown
## Interview Scorecard

**Candidate Name:** _______________
**Role:** [Role Title]
**Interview Date:** _______________
**Interviewer:** _______________

### Scoring Scale
- **1** — Does not meet requirements
- **2** — Partially meets requirements
- **3** — Meets requirements
- **4** — Exceeds requirements
- **5** — Exceptional — top-tier candidate

### Evaluation

| Category | Criteria | Score (1-5) | Notes |
|----------|----------|:-----------:|-------|
| **Experience** | Relevant background for the role | | |
| **Technical Skills** | [Specific skill 1] | | |
| **Technical Skills** | [Specific skill 2] | | |
| **Problem Solving** | Handles situational questions well | | |
| **Communication** | Clear, articulate, listens well | | |
| **Culture Fit** | Aligns with team values and work style | | |
| **Initiative** | Shows proactivity, asks good questions | | |
| **Reliability Signals** | Punctual, prepared, professional | | |

### Overall Assessment

| | Score |
|---|:---:|
| **Total Points** | ___/40 |
| **Average Score** | ___/5 |

### Recommendation

- [ ] **Strong Hire** — Move to offer immediately
- [ ] **Hire** — Good candidate, proceed to next step
- [ ] **Maybe** — Has potential, needs second interview or skills test
- [ ] **No Hire** — Does not meet the bar
- [ ] **Strong No Hire** — Significant concerns, do not proceed

### Notes
[Free-form notes from the interview — specific things that stood out, concerns, quotes]

### Decision
**Hire / No Hire:** _______________
**Reasoning:** _______________
**Next Step:** _______________
```

### Step 6: Define Red and Green Flags

```markdown
## Red Flags & Green Flags

### Green Flags (Signs of a Great Hire)
1. **[Green flag]** — What it indicates about the candidate
2. **[Green flag]** — What it indicates
3. **[Green flag]** — What it indicates
4. **[Green flag]** — What it indicates
5. **[Green flag]** — What it indicates
6. **[Green flag]** — What it indicates
7. **[Green flag]** — What it indicates

### Red Flags (Proceed with Caution)
1. **[Red flag]** — What it might indicate (and when to disqualify vs. investigate further)
2. **[Red flag]** — What it might indicate
3. **[Red flag]** — What it might indicate
4. **[Red flag]** — What it might indicate
5. **[Red flag]** — What it might indicate
6. **[Red flag]** — What it might indicate
7. **[Red flag]** — What it might indicate

### Immediate Disqualifiers
- [Disqualifier 1 — non-negotiable reason to stop the process]
- [Disqualifier 2]
- [Disqualifier 3]
```

### Step 7: Create Offer Letter Template

```markdown
## Offer Letter Template

---

**[Company Name]**
[Date]

Dear [Candidate Name],

We are pleased to extend an offer of employment for the position of **[Role Title]** at [Company Name].

**Position Details:**
- **Title:** [Role Title]
- **Start Date:** [Proposed start date]
- **Employment Type:** [Full-time / Part-time / Contract]
- **Location:** [Remote / On-site / Hybrid]
- **Reports To:** [Manager Title]
- **Compensation:** [$X per year / $X per hour]
- **Payment Schedule:** [Bi-weekly / Monthly / Per project]

**Additional Benefits:**
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

**Conditions of Employment:**
- [Condition 1 — background check, NDA, non-compete, probation period, etc.]
- [Condition 2]

This offer is contingent upon [any conditions — background check completion, reference verification, etc.].

Please confirm your acceptance by signing below and returning this letter by **[deadline date]**.

We are excited about the possibility of you joining our team.

Sincerely,

_______________
[Your Name]
[Your Title]
[Company Name]

**ACCEPTANCE**

I, [Candidate Name], accept the offer of employment as described above.

Signature: _______________
Date: _______________

---

*Note: This is a template. Consult with an attorney for employment agreements in your specific jurisdiction, especially regarding non-compete clauses, IP assignment, and at-will employment terms.*
```

### Step 8: Build Onboarding Checklist

```markdown
## New Hire Onboarding Checklist

### Before Day 1 (Admin Prep)
- [ ] Send signed offer letter and confirm start date
- [ ] Set up company email / accounts
- [ ] Set up payroll
- [ ] Prepare welcome packet or orientation materials
- [ ] Add to relevant tools: [Slack/Teams, project management, CRM, etc.]
- [ ] Assign a buddy or point of contact for questions
- [ ] Prepare Day 1 agenda
- [ ] Order equipment if needed (laptop, phone, etc.)

### Day 1 — Welcome & Orientation
- [ ] Welcome call or meeting with manager
- [ ] Company overview: mission, values, how things work here
- [ ] Role expectations walkthrough (use the job description)
- [ ] Introductions to team members
- [ ] Tour of tools and systems
- [ ] Share standard operating procedures (brain/sops/)
- [ ] Set up first week goals
- [ ] Confirm communication norms (when to Slack vs. email, response times, meeting cadence)

### Week 1 — Getting Up to Speed
- [ ] Daily check-ins with manager (15 min)
- [ ] Complete any required training or reading
- [ ] Shadow key processes or meetings
- [ ] Start first real task or project (low-stakes, high-learning)
- [ ] Document questions and blockers
- [ ] End-of-week review: What did you learn? What is confusing? What do you need?

### Days 8-30 — Ramp-Up
- [ ] Transition from shadowing to independent work
- [ ] Weekly 1:1 with manager
- [ ] Complete first meaningful deliverable
- [ ] Give and receive feedback
- [ ] Mid-point check: Are expectations aligned on both sides?

### Day 30 — Performance Check
- [ ] 30-day review meeting
- [ ] Are they meeting expectations? (Use the scorecard criteria)
- [ ] Are they happy? (Retention starts on Day 1)
- [ ] Adjust role, responsibilities, or support as needed
- [ ] Decide: Continue, extend probation, or part ways

### Day 60-90 — Full Integration
- [ ] Operating independently in the role
- [ ] Contributing to goals and projects
- [ ] Embedded in team communication and culture
- [ ] 90-day formal review with performance discussion
- [ ] Set goals for next quarter
```

### Step 9: Compile and Save

Assemble everything into a single document:

```markdown
# Hiring Package: [Role Title]

> **Date:** YYYY-MM-DD
> **Company:** [Company Name]
> **Role:** [Role Title]
> **Status:** [Drafting / Posting / Screening / Interviewing / Offer Sent / Filled]
> **Prepared By:** LindaAI

---

## Job Description
[From Step 2]

## Ideal Candidate Profile
[From Step 3]

## Screening Questions
[From Step 4]

## Interview Scorecard
[From Step 5]

## Red Flags & Green Flags
[From Step 6]

## Offer Letter Template
[From Step 7]

## Onboarding Checklist
[From Step 8]

---

🤠 *Generated by LindaAI* 🏇
*This is a complete hiring package — adjust based on your specific needs, industry, and jurisdiction. For legal documents (offer letters, NDAs, non-competes), have an attorney review before sending.*
```

Save to: `brain/drafts/hiring-{role-slug}-{YYYY-MM-DD}.md`

### Step 10: Present to User

Give the user:
1. The job description (ready to post)
2. The ideal candidate summary (who to look for)
3. The top 3 screening questions (most revealing)
4. Key red and green flags
5. Where the full package was saved
6. Suggestion: "Where are you posting this? I can adjust the tone for LinkedIn, Indeed, a freelancer platform, or your own network."

## Quality Standards

1. **Role-specific, not generic.** Every section must be tailored to the actual role described. A job description for a VA should read nothing like one for a sales director.
2. **Entrepreneur-friendly.** Written for business owners who do not have HR. No jargon, no overcomplicated process. Clear, direct, usable.
3. **Legally aware.** Include disclaimers where relevant (offer letters, employment type). Flag when the user should consult an attorney.
4. **Bias-conscious.** Job descriptions and questions should not include language that discriminates by age, gender, race, disability, or other protected characteristics.
5. **Practical.** The screening questions, scorecard, and checklists should be printable and usable in a real interview without further modification.
6. **Complete.** Every section of the hiring package is filled in. No "[TBD]" or empty sections.

## Output Format

A single comprehensive markdown file containing the full hiring package (job description, candidate profile, screening questions, scorecard, red/green flags, offer letter template, onboarding checklist). Typically 3,000-5,000 words. Saved to `brain/drafts/hiring-{role-slug}-{YYYY-MM-DD}.md`.

## Example Usage

**User:** "I need to hire a virtual assistant to manage my inbox, calendar, and social media scheduling"

**AI executes:**
- Expands "virtual assistant" into a full role spec based on the described responsibilities
- Generates: job description for a remote VA, candidate profile (organized, tech-savvy, proactive), 10 screening questions focused on organization and communication, scorecard, red/green flags for VA hiring, offer letter for a contractor, onboarding checklist for a remote hire
- Saves to `brain/drafts/hiring-virtual-assistant-2026-03-03.md`

**User:** "Hiring screener for a transaction coordinator in real estate"

**AI executes:**
- Builds a TC-specific package: industry knowledge requirements, real estate transaction experience, coordination and communication skills
- Screening questions focus on deal pipeline management, document handling, deadline tracking
- Red flags include poor attention to detail, inability to handle multiple transactions simultaneously
- Saves to `brain/drafts/hiring-transaction-coordinator-2026-03-03.md`

**User:** "I need to hire a content creator — someone who can shoot TikToks and Reels for me 3x per week"

**AI executes:**
- Builds a creative role package: portfolio requirements, platform knowledge, content calendar management
- Screening questions include "show me 3 videos you're proud of", "how do you stay on top of trends"
- Offer letter template set up as a freelance/contractor agreement
- Saves to `brain/drafts/hiring-content-creator-2026-03-03.md`

## Error Handling

- **If the user does not specify the role:** Ask: "What role are you hiring for? Give me a title and a rough description of what they'd do, and I'll build the full package."
- **If the user gives a very vague description:** Build the package with reasonable assumptions for the role, but flag: "I made some assumptions based on industry norms for this role. Review the responsibilities section and adjust anything that doesn't match your needs."
- **If the user asks for just one section (e.g., only interview questions):** Provide that section, but note: "I've generated the screening questions. Want me to build the full hiring package (job description, scorecard, offer letter, onboarding checklist) too?"
- **If `brain/drafts/` does not exist:** Create it automatically before saving.
- **If a hiring file already exists for the same role and date:** Overwrite — the user is likely refining. Note: "Updated your existing hiring package for [role]."
- **If the user asks about salary ranges and does not provide one:** Research market rates via WebSearch for the role, location, and experience level. Present a range with sources. Note: "These are market rates — adjust based on your budget and the candidate's experience."
- **If the user wants to hire internationally or for a specific jurisdiction:** Add a note: "Employment laws vary by jurisdiction. The offer letter and employment terms in this package are general templates. Have a local attorney or HR consultant review before sending, especially for non-US hires."

---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
