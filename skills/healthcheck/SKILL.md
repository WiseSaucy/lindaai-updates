---
name: healthcheck
description: Run a full health check on your LindaAI install. Use when the user says "healthcheck", "is everything working", "linda healthcheck", "system check", "diagnose linda", "linda status", or anything that asks if components (license, packs, agents, bridges) are alive. Shows green/red for each piece + tells you exactly what to click if anything's broken.
tier: all
---

# /healthcheck — Total System Check

Howdy! Running through every part of your LindaAI install to make sure it's all working. Each check is green or red. If something's red, I'll tell you EXACTLY what to do.

## What I check (in this order)

### 1. License binding
- Read `.lindaai/license.json` — does the file exist?
- Compute current machine_id
- Compare to the saved `machine_id` field
- If mismatch → "Your license is locked to a different device. Email support to migrate."
- If matches → ✅ green
- Also hit `GET /v1/licenses/validate/{KEY}?machine_id={ID}` to confirm not revoked

### 2. Tier + skill count
- Read `.lindaai/license.json` for the tier
- Count skill files in `.claude/skills/`
- Expected: Bronze=11, Silver=21, Gold=34, Platinum=51
- Mismatch → "Skill count is off — run `/linda-sync` to repair from CDN"

### 3. Agents (Platinum only)
- Count agent .md files in `.claude/agents/`
- Expected: 17-19 depending on which roster
- Confirm avatars folder + roster doc both present

### 4. Industry pack quotas
- Count packs in `packs/`
- Bronze should have 1, Silver 2, Gold 4, Platinum 10
- If quota is wrong → "Run `/linda-sync` or re-pick via the picker URL"

### 5. Brain folder
- Confirm `brain/README.md` exists and is writable
- Test: write a temp file, delete it

### 6. Telegram bridge (if installed)
- Check if `~/.lindaai-daemons/telegram-bridge/` exists
- If yes: check the daemon is running via `launchctl list | grep telegram`
- If yes but daemon is down: surface "Telegram bridge isn't running. Open System Settings → Privacy & Security → Full Disk Access → make sure `python3.12` is checked. Then I'll restart it."

### 7. Discord bridge (if installed)
- Same pattern as telegram

### 8. Server reachability
- `curl -s https://lindaai-api-production.up.railway.app/health`
- If down: "LindaAI license server is offline. License remains valid offline. Server outages usually resolve within minutes."

### 9. Last `/linda-sync` timestamp
- Check brain/last-sync.txt — older than 7 days → suggest a sync

## Output format

I lay out a clean dashboard like this:

```
═══ LINDAAI HEALTHCHECK ═══

✅ License        — bound to this machine, tier=Platinum
✅ Skills         — 51 / 51 installed
✅ Agents         — 19 installed
✅ Packs          — 10 / 10 (all available)
✅ Brain          — readable + writable
✅ Telegram       — daemon running (PID 7336)
🟡 Discord        — installed but daemon stopped — click "Restart Discord" below
✅ Server         — reachable (https://lindaai-api...)
✅ Last sync      — 2 days ago

═══ ACTIONS YOU CAN TAKE ═══
[Restart Discord]  [Run /linda-sync]  [Migrate to new device]

Need anything fixed? Say the word.
```

## Don't over-explain

- Keep each line one row
- Use the emoji statuses above
- If a customer wants details, they can ask "explain why X is red"
- Auto-suggest the fix; never just dump an error

## When to re-run automatically

- On first run of any LindaAI session if `brain/last-healthcheck.txt` is older than 24h
- If the user reports "something feels off" or "is X working"
- After any `/linda-sync`

---

© 2022-2026 Daniel Wise · LindaAI
