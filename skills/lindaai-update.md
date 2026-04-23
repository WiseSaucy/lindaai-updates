---
name: lindaai-update
description: Check LindaAI servers for new skills, commands, or agents and install any updates for the customer's tier. Use when the user says "update LindaAI", "/lindaai-update", "check for updates", "new skills", "update my skills", "pull updates", "refresh LindaAI".
tier: all
---

# /lindaai-update — LindaAI Auto-Update

This skill pulls the latest skills, commands, and agents from the LindaAI update server and installs only what the user's tier and license allow.

## When to run
- User types `/lindaai-update` or asks to update LindaAI
- First run of the day (optional auto-trigger via hook)
- After a fresh install, to ensure the customer has the latest bundle

## What it does
1. Reads the user's license key from `~/.claude/lindaai/license.json`
2. Validates the license against the LindaAI API: `POST https://api.lindaai.com/v1/licenses/validate`
3. Fetches the current manifest: `GET https://updates.lindaai.com/manifest.json`
4. Compares local skill versions against the manifest
5. For each skill the license allows AND is newer on the server:
   - Downloads the SKILL.md from the updates CDN
   - Writes to `~/.claude/skills/<skill-name>/SKILL.md`
6. For skills the license NO LONGER allows (trial expired, picker changed):
   - Removes the skill folder from `~/.claude/skills/`
7. Prints a changelog of what was added, updated, or removed

## Workflow for the assistant

When this skill triggers:

1. **Read license:** `cat ~/.claude/lindaai/license.json`
   - If missing, tell user: "No LindaAI license found. Run /lindaai-activate first."

2. **Validate with server (POST):**
   ```
   POST https://api.lindaai.com/v1/licenses/validate
   Headers: Content-Type: application/json
   Body: { "license_key": "<key>", "machine_id": "<machine_id>" }
   ```
   Expected response:
   ```json
   {
     "valid": true,
     "tier": "platinum",
     "selected_skills": ["..."],
     "expires_at": "2027-04-21T00:00:00Z",
     "locked": true
   }
   ```

3. **Fetch update manifest:**
   `GET https://updates.lindaai.com/manifest.json`

4. **Compute diff:** For each skill in the manifest where `tier_requirement <= user_tier` AND `(not in allowed_skills OR local_version < remote_version)`:
   - Queue for install or removal

5. **Apply changes:** Download new/updated skill files, remove revoked ones.

6. **Report to user:**
   ```
   LindaAI Update Complete
   ✅ Added: <skill-name> (v<version>)
   🔄 Updated: <skill-name> (v<old> → v<new>)
   🗑️  Removed: <skill-name> (no longer in your plan)
   ```

## Hosting notes (for Boss47)

The update server is two static endpoints:
- `https://updates.lindaai.com/manifest.json` — version ledger
- `https://updates.lindaai.com/skills/<name>/SKILL.md` — raw skill files

Easiest hosting: GitHub public repo with GitHub Pages OR Cloudflare Pages. When a skill changes in LindaAI-Master, bump its version in `updates/manifest.json` and push. Customers' next `/lindaai-update` pulls the change.

## Error handling
- Network failure → "Couldn't reach LindaAI servers. Check your internet and try again."
- Invalid license → "License expired or revoked. Contact support@lindaai.com."
- Trial expired → "Your 5-day trial ended. Upgrade at wisecertified.gumroad.com to keep your skills."

## Example run

User: `/lindaai-update`

Output:
```
Howdy Boss47 — checking for updates...

✅ Added: bandit agent (v1.0.0)
🔄 Updated: deal-analyzer (v2.1.0 → v2.2.0)
🔄 Updated: morning-briefing (v1.3.0 → v1.4.0)

All set — 3 changes applied. Yeee Hawww! 🤠
```

---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
