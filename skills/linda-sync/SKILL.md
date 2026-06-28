---
name: linda-sync
description: Check LindaAI servers for new skills, commands, or agents and install any updates for the customer's tier. Honors picker selections. Use when the user says "update LindaAI", "/linda-sync", "check for updates", "new skills", "update my skills", "pull updates", "refresh LindaAI", "sync LindaAI".
tier: all
---

# /linda-sync — LindaAI Auto-Update

Pulls the latest skills (and Platinum agents) from the LindaAI server and installs **only** what the user's tier allows. License-gated end-to-end — no public CDN, no IP leak.

## When to run
- User types `/linda-sync` or asks to update
- First run of the day (optional auto-trigger)
- After fresh install
- After a tier upgrade

## Workflow for the assistant

### Step 1 — Read the local license

```bash
cat ~/.claude/lindaai/license.json
```

Extract the `key` field. If file missing or no key: tell user "No LindaAI license found. Re-extract your delivery zip and try again." STOP.

### Step 2 — Fetch the skill manifest (license-gated)

```bash
curl -s "https://lindaai-api-production.up.railway.app/v1/sync/manifest/$KEY"
```

Response shape:
```json
{
  "tier": "platinum",
  "count": 51,
  "skills": [
    {"name": "linda-brief", "sha256": "abc123…", "size": 18723},
    {"name": "linda-mail",  "sha256": "def456…", "size": 21055},
    …
  ],
  "fetched_at": "2026-05-28T17:00:00"
}
```

Error responses:
- `401` → "Missing or invalid license key. Re-extract your delivery zip."
- `403` → "License revoked. Email support@send.lindaai-brain.com to restore."
- `404` → "License not found. Re-extract your delivery zip."

### Step 3 — Diff local vs server

For each skill in the manifest:
1. Check if `.claude/skills/<skill-name>/SKILL.md` exists locally
2. If exists, compute its sha256
3. If hash matches server → ✅ up to date, skip
4. If hash differs → mark for update
5. If file missing locally → mark for install

For each local skill NOT in the server manifest:
- Mark for removal (user's tier no longer includes it, e.g. picker change or revocation)

### Step 4 — Fetch & write each changed skill

```bash
for skill in $UPDATE_LIST; do
  curl -s "https://lindaai-api-production.up.railway.app/v1/sync/skill/$KEY/$skill" \
    > ".claude/skills/$skill/SKILL.md"
done
```

If `mkdir -p .claude/skills/$skill/` is needed for new installs, create it first.

### Step 5 — Platinum: same flow for agents

If `license.tier == "platinum"`:

```bash
curl -s "https://lindaai-api-production.up.railway.app/v1/sync/agents/$KEY"
```

Returns the same shape as skills manifest. For each agent:

```bash
curl -s "https://lindaai-api-production.up.railway.app/v1/sync/agent/$KEY/$agent_name" \
  > ".claude/agents/$agent_name.md"
```

### Step 6 — Report to user (COUNTRY-VOICE — Boss47 SOP 2026-06-09)

After applying updates, ALWAYS:

1. **Fetch the latest changelog:**
```bash
curl -s "https://raw.githubusercontent.com/WiseSaucy/lindaai-updates/main/CHANGELOG.md"
```
Pull the TOP entry (most recent dated section above the next `---`).

2. **Build the country-voice report — use this exact format:**

```
🤠 Howdy partner! Linda just rode out and grabbed the latest from the barn.

What landed in your install:
  ✨ NEW: [skill-name] — [pulled from frontmatter `description` field, kept to 1 line]
  🔄 UPDATED: [skill-name] — sharper/faster than before
  📦 Same crew (X agents, Y skills total) — all current

[INSERT TOP CHANGELOG ENTRY HERE — strip the date header, keep the bullets]

Yeeee Hawww 🤠 — you're riding the latest. Try the new stuff anytime.
— LindaAI Crew · support@send.lindaai-brain.com
```

3. **If NOTHING changed** (already current):
```
🤠 Howdy partner! Linda checked the barn — you're already riding the latest.
   ✓ X skills · Y agents · all current.
   Holler if anything's missing.
```

4. **Use the BRAND VOICE always** — Howdy, partner, Yeeee Hawww, barn, crew. Never corporate.

5. **For each NEW skill**, pull its `description` from frontmatter and trim to 1 line so customer knows what they got + how to use it.



## Endpoints reference

All under `https://lindaai-api-production.up.railway.app`:

| Endpoint | Purpose |
|---|---|
| `GET /v1/sync/manifest/{key}` | List skills + hashes for this tier |
| `GET /v1/sync/skill/{key}/{name}` | Fetch one skill's SKILL.md |
| `GET /v1/sync/agents/{key}` | List agents + hashes (Platinum only) |
| `GET /v1/sync/agent/{key}/{name}` | Fetch one agent .md (Platinum only) |

No admin key required — the customer's license key authenticates.

## Locked picker behavior

If `locked: true` on the license response, tell the user: "Your skill selections are locked for this billing period. To swap, upgrade to Platinum for full access — the in-app picker."

## Error handling

- Network failure → "Couldn't reach LindaAI servers. Check internet and try again."
- Server error (5xx) → "LindaAI servers are temporarily down. Try again in a few minutes."
- Picker URL: If user asks how to change skills, point them to `https://app.lindaai-brain.com/picker/`

---

© 2022-2026 Daniel Wise · LindaAI
All rights reserved · support@send.lindaai-brain.com
