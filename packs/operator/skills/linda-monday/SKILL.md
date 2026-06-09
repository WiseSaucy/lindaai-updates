---
name: linda-monday
description: This skill should be used when the user asks to "sync Monday.com", "pull my Monday boards", "Monday weekly digest", "what moved on Monday this week", "Monday status update", "sync to Monday", "post update to Monday", "create Monday item", "update Monday status", "Monday board pulse", "what's stuck on Monday", or any request involving Monday.com board synchronization, item updates, or weekly digest reporting.
tags: [operator, monday, integration, project-management, api]
version: 1.0.0
---

# Linda Monday — Monday.com Sync

## Overview

Most operators run Monday.com as their project board, but they don't actually look at it daily. Linda Monday closes that loop. Bidirectional sync via Monday's GraphQL API: Linda pulls boards, items, statuses, owners, and timelines; generates a weekly digest of what moved / what stalled / what's coming due; and writes back updates Boss47 dictates ("mark task 432 done", "move the Burlington lead to negotiation"). Now Monday is actually the source of truth — and Boss47 sees it without opening the app.

## When This Skill Applies

- "Pull my Monday boards"
- "Run my Monday weekly digest"
- "What moved on Monday this week?"
- "What's stuck on Monday?"
- "Mark Monday item 4321 as done"
- "Create a new task on the Acquisitions board"
- "Sync Monday to my pipeline"

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: API Setup (First Run)

If `brain/operator/integrations/monday.json` doesn't exist:
1. Walk Boss47 through generating a Monday.com API token (Profile → Admin → API → Generate)
2. Save to `brain/operator/integrations/monday.json`:
```json
{
  "api_token": "{token}",
  "api_url": "https://api.monday.com/v2",
  "default_board_ids": [],
  "last_sync": null
}
```
3. Test connection with `me { id name email }` query
4. Optionally pull all boards once for board_id discovery

### Step 2: Pull Boards & Items

GraphQL query for each watched board:
```graphql
query {
  boards(ids: [{board_id}]) {
    name
    items_page(limit: 500) {
      items {
        id
        name
        state
        updated_at
        column_values { id text value column { title type } }
        subitems { id name state }
      }
    }
  }
}
```

Cache locally at `brain/operator/integrations/monday-cache/{board_id}-{YYYY-MM-DD}.json`.

### Step 3: Diff Since Last Sync

Compare current pull vs last_sync snapshot:
- **Moved** — items whose status column changed
- **New** — items created since last sync
- **Closed** — items moved to Done / Canceled
- **Stuck** — items with no update in 14+ days that aren't Done
- **Coming due** — date column within 7 days, not Done
- **Overdue** — date column past, not Done

### Step 4: Build Weekly Digest

Generate `brain/operator/integrations/monday-digest-{YYYY-WW}.md`:

```markdown
# Monday.com Weekly Digest — Week {N}, {YYYY}

## Movement This Week
- ✅ {N} items closed
- 🚀 {N} items moved forward
- ➕ {N} new items created

## Top Closes
- [Acquisitions] Burlington duplex LOI accepted — closed by Liz
- [Operations] Q1 books closed — closed by Linda

## Stuck (no movement 14+ days)
- [Marketing] Launch landing page rebuild — owner: Drew — last update 23 days ago
- [Acquisitions] Cold-call list build — owner: Boss47 — last update 17 days ago

## Coming Due (next 7 days)
- [Compliance] Annual filing for [Your Business LLC] — due Tue
- [Operations] Q1 estimated tax payment — due Fri

## Overdue
- [Recruiting] PM interview round 2 — was due 3 days ago
```

### Step 5: Write Back (On Command)

Boss47 dictates updates; Linda issues mutations:
- Update status: `change_simple_column_value` mutation
- Create item: `create_item` mutation
- Add update note: `create_update` mutation
- Move group: `move_item_to_group` mutation

Always confirm before write-back: "Boss47 — gonna mark item 4321 'Done' on Acquisitions board. Confirm?"

### Step 6: Save & Notify

- Digest saved to `brain/operator/integrations/monday-digest-{YYYY-WW}.md`
- Sync log appended to `brain/operator/integrations/monday-sync-log.csv`
- If `linda-bizops` is invoked, digest summary is pulled into operator dashboard

## Inputs

- Monday API token (one-time setup)
- Board IDs to watch (or "all my boards")
- Action command (pull / digest / update / create)

## Outputs

- Cached board snapshots (JSON)
- Weekly digest (MD)
- Sync log (CSV)
- Confirmation messages on writes

## Example Usage

**User:** "Run my Monday weekly digest."

**LindaAI:** "Let's gooooooo Boss47!" Pulls 4 watched boards, diffs against last week. "Yeeee Hawww 🤠 — 12 closed, 7 moved forward, 4 stuck. Big stuck one: Drew's landing page, 23 days. Want me to ping him via linda-mail?"

**User:** "Mark item 4321 as done on the Acquisitions board."

**LindaAI:** Confirms item name + current status, executes mutation, returns confirmation.

**User:** "Create a new task on Operations: 'Q2 estimated tax payment', due June 15, owner me."

**LindaAI:** Creates item with column values populated.

## Voice & Tone

- Country, fast. **Boss47.**
- "Let's gooooooo!" on sync kickoff. "Yeeee Hawww 🤠" when digest is locked.
- On stuck items: "Boss47 — Drew's been stuck on that landing page 23 days. Want me to nudge him?"

## Brand Rules

- Digest PDFs (when generated): LindaAI top-right, {customer_handle} bottom-right, © 2024–2026

## Cross-Skill Hooks

- **Feeds → linda-bizops** — digest summary surfaces on operator dashboard
- **Feeds → linda-mail** — auto-draft pings to stuck-item owners
- **Feeds ← linda-actions** — meeting action items can post to Monday boards
- **Feeds ↔ linda-pipeline** — RE pipeline stages can mirror to a Monday board

## Error Handling

- **API token rejected (401):** Stop, ask Boss47 to regenerate token.
- **Rate limit hit (429):** Back off + retry with exponential delay (Monday limit 10 req/sec).
- **Board ID unknown:** Pull all boards, ask Boss47 to pick.
- **GraphQL error on mutation:** Show full error, do not silently skip.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
