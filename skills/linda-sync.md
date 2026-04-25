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

### Step 2 — Call the allowed-skills endpoint

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
- Any skill in `allowed_skills` but NOT installed → download from CDN:
  ```
  GET https://raw.githubusercontent.com/WiseSaucy/lindaai-updates/main/skills/{skill}.md
  ```
  Save to `~/.claude/skills/{skill}/SKILL.md` (create folder first).

- Any skill installed but NOT in `allowed_skills` (and starts with `linda-`) → remove its folder.
  Don't touch non-linda skills (user's personal stuff).

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
- Invalid license → "License inactive. Contact support@lindaai.com."
- Picker URL: If user asks how to change skills, point them to `https://wisesaucy.github.io/lindaai-updates/picker/`

---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
