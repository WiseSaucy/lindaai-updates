---
name: linda-weekly
description: This skill should be used when the user asks for a "weekly review", "week in review", "what got done this week", "what slipped this week", "end of week review", "review my week", "weekly recap", "weekly report", "what happened this week", "plan next week", "weekly planning", "reflect on the week", "weekly retro", "weekly retrospective", "wrap up the week", "Friday review", "Sunday planning", "what did I accomplish this week", "weekly accountability check", "weekly goal check", or anything related to reviewing the past week's work, assessing goal progress, and planning the upcoming week.
version: 1.0.0
---

# Weekly Review

## Overview

A structured end-of-week review process powered by LindaAI that examines what happened over the past 7 days, assesses progress against goals, identifies what slipped and why, and builds a focused plan for the next week. LindaAI reads daily logs, project files, and goals to generate a comprehensive but concise weekly review document. Saved to `brain/daily/` for historical reference.

## When This Skill Applies

- User asks for a weekly review or recap
- User wants to reflect on what got done and what did not
- User asks "what slipped this week?"
- User wants to plan priorities for next week
- End of week (Friday/Saturday) or start of week (Sunday/Monday) planning
- User asks for a weekly retrospective or accountability check
- User says "wrap up the week" or "plan next week"
- User wants to check weekly progress against quarterly/monthly goals

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

### Step 1: Determine the Review Period

- Default: Past 7 days (Monday through Sunday of the current or just-ended week)
- If today is Monday-Wednesday, review the prior week (Mon-Sun)
- If today is Thursday-Sunday, review the current week (Mon through today)
- User can override with a specific date range

Calculate the dates: `{start_date}` through `{end_date}`.

### Step 2: Read Daily Logs

Read all daily log files from the review period:

```
brain/daily/{YYYY-MM-DD}.md
```

For each day that has a log, extract:
- What was accomplished
- What was worked on
- Decisions made
- Blockers encountered
- Notes and learnings

If some days have no logs, note those gaps (they often indicate untracked work or days off).

### Step 3: Read Project Status

Read `brain/projects/README.md` and any individual project files that were updated during the review period.

For each active project, note:
- Status change from beginning to end of week
- Milestones hit or missed
- New blockers that appeared
- Progress made

### Step 4: Read Goals

Read `brain/goals.md` to extract:
- Current quarterly objectives
- Monthly focus items
- Weekly priorities (if defined for this week)

### Step 5: Assess What Got Done

Compile a list of all accomplishments from daily logs and project updates:
- Group by project or category
- Note if each item was planned (in weekly priorities) or unplanned (reactive/ad-hoc)
- Highlight wins and breakthroughs

### Step 6: Assess What Slipped

Identify items that were planned or expected but did not get done:
- Check weekly priorities from goals.md against what actually happened
- Check project milestones that were due this week
- Check any deadlines from the calendar
- For each slipped item, try to identify WHY (blocked, deprioritized, time ran out, forgotten)

### Step 7: Goal Alignment Check

For each active quarterly goal:
- Did any work this week directly advance this goal?
- If not, is that acceptable (some goals are future-quarter) or is it a warning sign?
- Calculate a rough "time allocation" — what % of the week went to which goals?

Flag:
- Goals getting zero attention that should be active
- Disproportionate time on low-priority items
- Goals that are on track vs. at risk

### Step 8: Build Next Week's Plan

Based on everything above, draft priorities for next week:

1. **Carry-forward items** — Things that slipped and still matter
2. **Goal-driven items** — Work that directly advances quarterly objectives
3. **Deadlines** — Anything due next week
4. **Quick wins** — Small items that can be knocked out to build momentum
5. **Stretch items** — Nice to do if time allows

Limit to 3-5 top priorities. More than that means nothing is truly prioritized.

### Step 9: Energy and Pattern Check

Look for patterns across the week:
- Were certain days more productive than others?
- Did reactive work (fires, interruptions) dominate?
- Is there a recurring blocker or friction point?
- Was there scope creep or context-switching?
- Any personal notes about energy, motivation, or wellbeing?

### Step 10: Save the Review

Save to `brain/daily/weekly-review-{YYYY-MM-DD}.md` where the date is the review date (today).

Also update `brain/goals.md` weekly priorities section if the user approves.

## Output Format

```markdown
# Weekly Review: {Start Date} to {End Date}

> **Review Date:** {today}
> **Days Logged:** {X} of 7
> **Overall Assessment:** {Strong / Solid / Mixed / Rough}

---

## What Got Done

### {Project/Category 1}
- {accomplishment} [planned/unplanned]
- {accomplishment} [planned/unplanned]

### {Project/Category 2}
- {accomplishment}
- {accomplishment}

### Wins
- {notable win or breakthrough}
- {notable win or breakthrough}

---

## What Slipped

| Item | Was Due | Why It Slipped | Still Relevant? |
|------|---------|---------------|-----------------|
| {item} | {date/this week} | {reason} | Yes / No |
| {item} | {date} | {reason} | Yes / No |

---

## Goal Alignment

| Quarterly Goal | Work This Week | Status | Risk |
|---------------|---------------|--------|------|
| {goal 1} | {what was done} | On Track / At Risk / No Progress | {notes} |
| {goal 2} | {what was done} | {status} | {notes} |

### Time Allocation (approximate)
- {Goal/Category 1}: {X}%
- {Goal/Category 2}: {X}%
- Reactive/Unplanned: {X}%
- Admin/Overhead: {X}%

---

## Patterns and Observations

- {observation about the week's rhythm, energy, blockers, or habits}
- {observation}

---

## Next Week: {Date Range}

### Top 3 Priorities
1. **{Priority 1}** — {why, what "done" looks like}
2. **{Priority 2}** — {why, what "done" looks like}
3. **{Priority 3}** — {why, what "done" looks like}

### Carry-Forward
- {item from this week that still needs doing}

### Upcoming Deadlines
- {deadline} — {date}

### Stretch Goals (if time allows)
- {item}

---

## Accountability Score

| Metric | Score |
|--------|-------|
| Planned items completed | {X}/{Y} ({Z}%) |
| Goal-aligned work | {high/medium/low} |
| Days logged | {X}/7 |
| Overall week grade | {A/B/C/D/F} |

---

🤠 *Generated by LindaAI* 🏇
```

## Example Usage

**User:** "Weekly review"

**AI:** Reads all daily logs from the past 7 days, project files, and goals. Generates a full review showing 4 of 6 planned items completed, SellFi behind schedule, content creation slipping for the 3rd consecutive week. Plans next week with SellFi launch as the only top priority. Saves to `brain/daily/weekly-review-2026-03-02.md`.

**User:** "What slipped this week?"

**AI:** Focused review on just the "What Slipped" section — items that were planned but did not get done, with reasons.

**User:** "Plan next week"

**AI:** Reads current state from projects and goals, skips the backward-looking review, and drafts next week's priorities. Still checks what slipped to ensure carry-forward items are captured.

**User:** "Am I on track for Q1?"

**AI:** Reads goals.md Q1 objectives, compares against project progress and weekly output, gives an honest assessment of whether Q1 targets will be hit at the current pace.

**User:** "Wrap up the week and tell me what to focus on Monday"

**AI:** Quick review plus a focused "Monday morning" action list -- the 3 things to do first when the new week starts.

## Error Handling

- **If no daily log files exist for the review period:** Tell the user: "No daily logs found for {date range}. Either work wasn't logged this week, or the days were off. I'll ride with what I've got -- project file changes and goals only." Proceed with available data.
- **If `brain/goals.md` does not exist:** Skip the goal alignment check and note: "No goals file found. I can't assess alignment without it. Create `brain/goals.md` to enable goal tracking in future reviews."
- **If `brain/projects/README.md` does not exist or has no projects:** Skip project status and note: "No active projects found. The review covers daily logs and goals only."
- **If `brain/daily/` directory does not exist:** Create it before attempting to save the weekly review file. Report: "No daily log directory existed. I created `brain/daily/` and saved the weekly review there."
- **If a weekly review file already exists for this date:** Ask: "A weekly review already exists for {date}. Should I overwrite it with a fresh review, or create a supplemental review (e.g., `weekly-review-{date}-v2.md`)?"
- **If the user asks for a review of a specific date range that has no data:** Report honestly: "I found no logs, project updates, or activity for the period {start} to {end}. This could mean the week was untracked or the dates are wrong. Want me to try a different date range?"
- **If updating `brain/goals.md` weekly priorities section fails (malformed file):** Save the proposed next-week priorities in the weekly review file itself and note: "I couldn't update goals.md directly — it may need reformatting. The proposed priorities are saved in the review file."
- **If the user asks to "plan next week" without doing the backward review:** Skip Steps 2-6 (what got done, what slipped) and jump directly to building next week's plan from current project states and goals. Note: "Skipping the backward review — just planning forward. Run a full `/weekly-review` later if you want the complete picture."


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
