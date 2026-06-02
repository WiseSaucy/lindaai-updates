---
name: linda-sync
description: Check LindaAI servers for new skills, commands, or agents and install any updates for the customer's tier. Honors picker selections. Use when the user says "update LindaAI", "/lindaai-update", "/linda-sync", "check for updates", "new skills", "update my skills", "pull updates", "refresh LindaAI", "sync LindaAI".
tier: all
---

# /linda-sync — LindaAI Auto-Update

Pulls the latest skills, commands, and agents from the LindaAI servers and installs **only** what the user's tier and picker selections allow.

## When to run
- User types `/linda-sync` or asks to update
- First run of the day (optional auto-trigger via hook)
- After a fresh install, to ensure correct bundle
- After the user picks skills in the web picker

## What it does

1. Reads the user's license key from `~/.claude/lindaai/license.json`
2. Calls the LindaAI API's `allowed-skills` endpoint — **the API is the source of truth**
3. Compares local `~/.claude/skills/` against allowed_skills:
   - **Missing skills that ARE allowed** → download + install
   - **Installed skills that are NOT allowed** (picker changed, trial expired) → remove
4. Reports added / removed / updated to the user

## Workflow for the assistant

### Step 1 — Read local license

```bash
cat ~/.claude/lindaai/license.json
```

If missing, tell user: "No LindaAI license found. Run the bootstrap install or enter your key."

### Step 1.5 — Founder bypass (LindaAI owner only)

Before calling the server, check for founder status. The bypass fires when:

- `license.json` contains `"founder": true` (this flag is set only on the owner's own machine — no email or other PII is checked)

When the bypass fires, skip Step 2 and treat the user as having full Platinum-equivalent access:

- `tier` = whatever is in `license.json` (default to `platinum` if absent)
- `allowed_skills` = the full skill catalog (every file in this repo's `skills/` folder)
- `selected_skills` = same as `allowed_skills`
- `locked` = `false`
- Jump to Step 3 with that synthetic response.

Discover the full skill catalog by listing the `lindaai-updates` repo's `skills/` directory:
```
GET https://api.github.com/repos/WiseSaucy/lindaai-updates/contents/skills
```
Each `.md` file in the result corresponds to one skill (filename without `.md` is the skill name).

Print a short note when the bypass fires: `🔑 Founder bypass active — installing full catalog.` Do not call the Railway API at all in this path.

**Additive-only under bypass:** NEVER remove a locally installed `linda-*` skill just because it's missing from the catalog. Skip the removal half of Step 3 when bypass is active — the owner's machine commonly has dev skills not in the public catalog.

### Step 2 — Call the allowed-skills endpoint

(Only reached if Step 1.5 did not fire.)

```
GET https://lindaai-api-production.up.railway.app/v1/licenses/{key}/allowed-skills
```

Response:
```json
{
  "valid": true,
  "tier": "gold",
  "allowed_skills": ["linda-brief", "linda-mail", "linda-deals", ...],
  "selected_skills": ["linda-deals", "linda-rents", ...],
  "locked": false,
  "locks_at": "2026-05-07T12:00:00"
}
```

If `valid: false` → tell user the reason (expired, not found) and exit.

### Step 3 — Compute diff

- Get currently installed skill folder names from `~/.claude/skills/`
- For EVERY skill in `allowed_skills` → download the latest from CDN and save it (OVERWRITE if it already exists). This makes `/linda-sync` a true refresh — the customer always gets the newest version of every skill they're entitled to, not just brand-new ones:
  ```
  GET https://raw.githubusercontent.com/WiseSaucy/lindaai-updates/main/skills/{skill}.md
  ```
  Save to `~/.claude/skills/{skill}/SKILL.md` (create folder first).

- Any skill installed but NOT in `allowed_skills` (and starts with `linda-`) → remove its folder.
  Don't touch non-linda skills (user's personal stuff).

### Step 3.5 — Sync the AGENT-ANNOUNCE rule into root CLAUDE.md

LindaAI brand standard: every response leads with the named agent on the job (Bandit/Tally/Pony/etc.). This block must live in the customer's root `CLAUDE.md`.

1. Determine tier from license response (`tier` field): one of `bronze`, `silver`, `gold`, `platinum`.
2. Fetch the tier-specific block:
   ```
   GET https://raw.githubusercontent.com/WiseSaucy/lindaai-updates/main/agent-announce/{tier}.md
   ```
3. Locate the customer's root `CLAUDE.md` (in the LindaAI install folder — the same folder containing `.claude/skills/`).
4. Check for the marker `<!-- AGENT-ANNOUNCE-RULE v1 -->`:
   - **Missing** → append the fetched block to the end of `CLAUDE.md`. Report: `✅ Installed agent-announce rule ({tier}).`
   - **Present** → no-op (idempotent). If a `v2` ships later, replace the `v1` block in place.
5. Never duplicate; never strip the user's other content.

### Step 3.6 — Sync agent files (agents flow through the CDN now, just like skills)

This is what lets a NEW agent (e.g. 🔥 Forge) reach customers on `/linda-sync` — no re-install, no re-baked zip.

1. Fetch the tier → agents map from the CDN:
   ```
   GET https://raw.githubusercontent.com/WiseSaucy/lindaai-updates/main/tier-manifest.json
   ```
   Read `tiers.<tier>.agents` — the agent names this tier receives. (Founder bypass = every `.md` in the repo's `agents/` folder.)
2. The customer's agents live in `<install>/.claude/agents/` (same install folder as `.claude/skills/`).
3. For EVERY agent name in the tier's list:
   - Download `agents/<name>.md` from the CDN → save to `<install>/.claude/agents/<name>.md` (overwrite — keeps it current).
   - Best-effort: download `agents/avatars/<name>.png` → `<install>/.claude/agents/avatars/<name>.png` (skip on 404).
   - Refresh the roster: download `agents/_AGENT_ROSTER.md` → `<install>/.claude/agents/_AGENT_ROSTER.md`.
4. Remove any installed `agents/<name>.md` that is BOTH (a) NOT in the tier's allowed list AND (b) listed under `remove` in `deprecated-content.json` (clears internal-only agents like Mender/Ledger). Never remove a non-deprecated agent.
5. Report agents added / updated / removed.

### Step 3.7 — Install the agent-name enforcement hook (the HARD BLOCK)

Every LindaAI customer gets the same enforcement: a response that doesn't lead with a named agent is blocked and re-done. This is the brand standard — a TEAM, not a faceless chatbot.

1. Download the hook:
   ```
   GET https://raw.githubusercontent.com/WiseSaucy/lindaai-updates/main/hooks/check-agent-name.sh
   ```
   Save to `<install>/.claude/hooks/check-agent-name.sh` and make it executable (`chmod +x`).
2. Register it as a Stop hook in `<install>/.claude/settings.json` — **MERGE, never clobber** the user's other settings. Ensure this entry is present:
   ```json
   { "hooks": { "Stop": [ { "hooks": [ { "type": "command", "command": ".claude/hooks/check-agent-name.sh" } ] } ] } }
   ```
   If `settings.json` exists, add the Stop-hook entry while preserving everything else; if not, create it with this content.
3. Report: `✅ Agent-name enforcement hook installed (hard block active).`

### Step 4 — Report

```
🤠 LindaAI Sync — Tier: GOLD
✅ Installed: linda-telegram-setup, linda-discord-setup
🗑️  Removed: linda-weekly (no longer in your selection)
⚠ Lock countdown: selections lock on 2026-05-07

Done. 3 changes applied.
```

## Locked keys behavior

If `locked: true`, tell the user: "Your skill selections are permanently locked. To swap, upgrade to Platinum for full access."

## Error handling

- Network failure → "Couldn't reach LindaAI servers. Check internet and try again."
- Invalid license → "License inactive. Contact support@send.lindaai-brain.com."
- Picker URL: If user asks how to change skills, point them to `https://app.lindaai-brain.com/picker/`

---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
