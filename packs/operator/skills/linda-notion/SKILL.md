---
name: linda-notion
description: This skill should be used when the user asks to "sync Notion", "pull my Notion database", "Notion workspace", "update Notion", "create Notion page", "search Notion", "Notion as my second brain", "read from Notion", "write to Notion", "Notion calendar sync", "post to Notion", "find in Notion", or any request involving Notion API integration, database sync, or page creation/update.
tags: [operator, notion, integration, second-brain, api]
version: 1.0.0
---

# Linda Notion — Workspace Integration

## Overview

Notion is where a lot of operators keep their second brain — CRM, content calendar, deal pipeline, SOPs, meeting notes, all of it. Linda Notion plugs the operator's LindaAI brain into their Notion workspace via the official API. Read databases, write new pages, update existing pages, query by filter, sync calendars. Now your `brain/` and your Notion workspace are the same thing — change one, the other reflects.

## When This Skill Applies

- "Pull my Notion CRM database"
- "Add a new page to my Deals database"
- "Search Notion for everything tagged 'Liz'"
- "Sync my Notion calendar"
- "Update the status on Notion deal {name}"
- "Push this meeting notes to Notion"
- "Find my SOP for tenant onboarding"

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: API Setup (First Run)

If `brain/operator/integrations/notion.json` doesn't exist:
1. Walk Boss47 through creating a Notion internal integration at notion.so/my-integrations
2. Boss47 shares each target database/page with the integration (Notion permission model)
3. Save to `brain/operator/integrations/notion.json`:
```json
{
  "api_token": "{secret_token}",
  "api_version": "2022-06-28",
  "watched_databases": [
    {"id": "{db_id}", "name": "Deals", "purpose": "RE pipeline"},
    {"id": "{db_id}", "name": "CRM", "purpose": "Contacts"}
  ],
  "last_sync": null
}
```

### Step 2: Discover Databases & Pages

API call: `POST /v1/search` with empty query — returns all shared content.
Cache database schemas at `brain/operator/integrations/notion-schemas/{db_id}.json` so Linda knows column types (title, select, multi-select, date, person, relation, formula, rollup).

### Step 3: Read Database

`POST /v1/databases/{db_id}/query` with filter + sort. Translate Notion property values → flat dict per row. Save snapshot to `brain/operator/integrations/notion-cache/{db_name}-{YYYY-MM-DD}.json`.

Common queries:
- "All open deals" → filter `Status != Closed`
- "Tagged Liz" → filter `Tags contains Liz`
- "Coming up this week" → filter `Date is_within next_week`

### Step 4: Write Page

`POST /v1/pages` with parent = `database_id` and properties matching schema:
```json
{
  "parent": {"database_id": "{id}"},
  "properties": {
    "Name": {"title": [{"text": {"content": "Burlington Duplex LOI"}}]},
    "Status": {"select": {"name": "Negotiation"}},
    "Owner": {"people": [{"id": "{user_id}"}]},
    "Date": {"date": {"start": "2026-04-30"}}
  },
  "children": [
    {"object": "block", "type": "paragraph",
     "paragraph": {"rich_text": [{"text": {"content": "Body content"}}]}}
  ]
}
```

Confirm before write: "Boss47 — gonna create a new Deal page 'Burlington Duplex LOI' in your Deals DB. Confirm?"

### Step 5: Update Page

`PATCH /v1/pages/{page_id}` to change properties. `PATCH /v1/blocks/{block_id}/children` to append content.

### Step 6: Calendar Sync

If a watched DB has a Date property + a Status property, surface on operator's calendar:
- Pull all upcoming events with `Date >= today`
- Add to `brain/operator/calendar/notion-events.md`
- Cross-link with `linda-bizops` dashboard "Coming Up" section

### Step 7: Save & Log

- Cached snapshots: `brain/operator/integrations/notion-cache/`
- Sync log: `brain/operator/integrations/notion-sync-log.csv` (timestamp, action, target, result)

## Inputs

- Notion integration token (one-time)
- Database IDs to watch
- Action: read / write / update / search

## Outputs

- Cached DB snapshots (JSON)
- Confirmation messages on writes
- Sync log entries
- (On request) cross-skill data feeds

## Example Usage

**User:** "Pull my Notion Deals database and show me what's in negotiation."

**LindaAI:** "Let's gooooooo Boss47!" Queries DB, returns 4 deals in Negotiation stage with key fields. "Yeeee Hawww 🤠 — Burlington duplex farthest along, due-diligence due Friday."

**User:** "Push my last meeting notes to Notion under the Liz database."

**LindaAI:** Pulls last meeting from `linda-actions` output, formats as Notion page, confirms target DB, creates page.

**User:** "Find me everything in Notion tagged 'Liz'."

**LindaAI:** Cross-DB search across watched databases, returns matches with page links.

## Voice & Tone

- Country, helpful. **Boss47.**
- "Let's gooooooo!" on kickoff. "Yeeee Hawww 🤠" when synced.

## Brand Rules

- Notion content stays as Notion content (don't re-brand)
- Any PDF Linda generates summarizing Notion data: LindaAI top-right, {customer_handle} bottom-right, © 2024–2026

## Cross-Skill Hooks

- **Feeds ↔ linda-pipeline** — RE deals can mirror between Notion and `brain/leads/`
- **Feeds ↔ linda-actions** — meeting action items can post into Notion task DB
- **Feeds → linda-bizops** — Notion calendar events surface on dashboard
- **Feeds ↔ linda-files** — Notion-stored docs can register in filing cabinet
- **Feeds ← linda-pulse** — project pulse can read project status from Notion

## Error Handling

- **401 unauthorized:** Token expired or DB not shared with integration — guide Boss47 to re-share.
- **Schema mismatch on write:** Show what Linda expected vs what's there, do not silently skip.
- **Rate limit (429):** Notion limit ~3 req/sec — back off and retry.
- **Database too large (>100 pages):** Paginate with cursor.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
