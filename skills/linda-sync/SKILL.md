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

### Step 1 — Find the license (self-healing — never dead-end the customer)

Look for the license file in THIS ORDER (first hit wins):

```bash
cat .lindaai/license.json          # 1. project folder (where every baked zip puts it)
cat ~/.claude/lindaai/license.json # 2. legacy home location (older installs)
```

Extract the key: accept EITHER the `key` field OR the legacy `license_key` field.
A file that exists but carries neither field is treated as missing — self-heal it.

**If NO license file exists anywhere** — do NOT stop. Self-heal:
1. Ask the customer: "What's your LindaAI license key? It's in your purchase email — looks like `LINDA-2026-XXXX-XXXX`."
2. Recreate the file from the server (the key itself is the auth). Fill in the key, run it as written —
   it only replaces `license.json` when the server accepts the key, so a bad key can never clobber a file:
```bash
KEY="PASTE-THE-KEY-THE-CUSTOMER-GAVE-YOU"
mkdir -p .lindaai && curl -fsS --proto '=https' --tlsv1.2 --max-time 20 \
  "https://lindaai-api-production.up.railway.app/v1/licenses/download/$KEY" -o .lindaai/license.json.new \
  && mv -f .lindaai/license.json.new .lindaai/license.json && echo "LICENSE: restored" \
  || { rm -f .lindaai/license.json.new; echo "LICENSE: key not accepted"; }
```
3. `LICENSE: restored` → confirm it (`cat .lindaai/license.json` shows their key + tier) and continue to Step 2.
4. `LICENSE: key not accepted` → the key is wrong or revoked (or the server is unreachable) — have them
   double-check the purchase email, or contact support@lindaai-brain.com. Nothing on disk was changed.

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
    {"name": "morning-briefing", "sha256": "abc123…", "size": 18723},
    {"name": "linda-mail",  "sha256": "def456…", "size": 21055},
    …
  ],
  "fetched_at": "2026-05-28T17:00:00"
}
```

Error responses:
- `401` → "Missing or invalid license key. Re-extract your delivery zip."
- `403` → "License revoked. Email support@lindaai-brain.com to restore."
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

**REMOVAL SAFETY GUARD (never mass-delete):**
- If the server manifest is EMPTY or has fewer than 5 skills → remove NOTHING. Say:
  *"Server sent an unusually small skill list — skipping removals to protect your install.
  Installs/updates still applied. If your tier really changed, run me again tomorrow or
  email support."* (An empty manifest usually means a server hiccup, not a real downgrade.)
- If more than 3 skills would be removed in one run → remove NOTHING automatically.
  List them and ask the owner to confirm first.
- NEVER remove: skills under a pack folder, anything the owner built themselves
  (not server-delivered), or this sync skill itself.

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

### Step 5.5 — Brain-file update (CLAUDE.md over sync — v1.8)

The tier CLAUDE.md (first-run flow, Rooster's Daily Crow, agent rules) also updates
over sync so product improvements reach existing installs:

```bash
curl -s "https://lindaai-api-production.up.railway.app/v1/sync/claudemd/$KEY"
```

Returns `{"tier", "sha256", "content", ...}`.

1. Compute the sha256 of the local `CLAUDE.md`. If it MATCHES the server's → skip (up to date).
2. If it DIFFERS:
   - **Back up first:** copy the current file to `.lindaai/CLAUDE.md.bak-<YYYY-MM-DD>`.
   - Write the server `content` to `CLAUDE.md` (full replace — personalization lives in
     `license.json`, never in this file).
   - Add to the report: *"🧠 Brain-file updated — restart me (fresh session) so the new
     behavior loads, partner."*
3. **Safety rails:** if the fetch fails, returns 404, or content is empty/suspiciously
   small (< 2,000 chars) → change NOTHING, keep the local file, note it in the report.
   Never leave the customer without a working CLAUDE.md.

### Step 5.7 — Runner refresh (Rooster's daily script)

Rooster's scheduled runner lives OUTSIDE the skills folder, so skill sync never reaches
it. This step brings it current — **only if Rooster is already set up on this machine.**
It replaces one file at one fixed path and nothing else.

**Hard rules:**
- Run the block for this OS **exactly as written**. The only thing you fill in is the license key.
- NEVER touch the schedule — no `launchctl`, no `crontab`, no Task Scheduler. The path doesn't
  change, so the customer's existing schedule keeps working.
- The block fails closed: on ANY problem it keeps the current script. Do not "fix" a failure by
  skipping a check, writing the file yourself, or fetching it from anywhere else.
- Never install the runner here if it isn't already there — that's `/rooster-setup`'s job.

**macOS / Linux:**

```bash
refresh_runner() {
  KEY="PASTE-LICENSE-KEY-FROM-STEP-1"
  API="https://lindaai-api-production.up.railway.app"
  NAME="rooster-daily.sh"                       # fixed name — never taken from the server
  DEST="$HOME/.claude/lindaai/$NAME"            # fixed destination
  TMP="$DEST.new.$$"
  sha() { if command -v shasum >/dev/null 2>&1; then shasum -a 256 "$1"; else sha256sum "$1"; fi | awk '{print $1}'; }
  ver() { head -n 20 "$1" | sed -n 's/^# RUNNER_V=\([0-9]\{1,6\}\)[[:space:]]*$/\1/p' | head -1; }
  keep() { rm -f "$TMP" "$DEST.bak.new"; echo "RUNNER: kept current ($1)"; }

  [ -f "$DEST" ] || { echo "RUNNER: not installed - skip"; return 0; }
  [ -L "$DEST" ] && { echo "RUNNER: left alone (it is a link the owner manages)"; return 0; }
  rm -f "$DEST".new.* "$DEST.bak.new" 2>/dev/null          # leftovers from an interrupted run
  command -v shasum >/dev/null 2>&1 || command -v sha256sum >/dev/null 2>&1 \
    || { keep "no sha256 tool on this machine"; return 0; }
  MANIFEST=$(curl -fsS --proto '=https' --tlsv1.2 --max-time 20 "$API/v1/sync/scripts/$KEY") \
    || { keep "could not reach server"; return 0; }
  WANT=$(printf '%s' "$MANIFEST" | tr -d '\n\r' | tr '{' '\n' \
    | grep -E "\"name\"[[:space:]]*:[[:space:]]*\"$NAME\"" \
    | sed -E -n 's/.*"sha256"[[:space:]]*:[[:space:]]*"([0-9a-f]{64})".*/\1/p' | head -1)
  [ ${#WANT} -eq 64 ] || { keep "server sent no valid hash"; return 0; }
  [ "$(sha "$DEST")" = "$WANT" ] && { echo "RUNNER: already current"; return 0; }

  curl -fsS --proto '=https' --tlsv1.2 --max-time 30 -o "$TMP" "$API/v1/sync/script/$KEY/$NAME" \
    || { keep "download failed"; return 0; }
  [ "$(sha "$TMP")" = "$WANT" ] || { keep "hash mismatch"; return 0; }
  SIZE=$(wc -c < "$TMP" | tr -d ' ')
  { [ "$SIZE" -ge 1000 ] && [ "$SIZE" -le 200000 ]; } || { keep "unexpected size $SIZE"; return 0; }
  [ "$(head -c 2 "$TMP")" = "#!" ] || { keep "not a script"; return 0; }
  bash -n "$TMP" 2>/dev/null || { keep "failed syntax check"; return 0; }
  NEWV=$(ver "$TMP"); OLDV=$(ver "$DEST")
  [ -n "$NEWV" ] || { keep "server copy carries no version"; return 0; }
  [ "$NEWV" -ge "${OLDV:-0}" ] \
    || { rm -f "$TMP"; echo "RUNNER: already current (yours is newer than the server copy)"; return 0; }

  cp -p "$DEST" "$DEST.bak.new" || { keep "could not back up"; return 0; }
  chmod 755 "$TMP" && mv -f "$TMP" "$DEST" || { keep "could not replace"; return 0; }
  mv -f "$DEST.bak.new" "$DEST.bak" || { rm -f "$DEST.bak.new"; echo "RUNNER: updated (no backup copy could be saved)"; return 0; }
  echo "RUNNER: updated (previous copy saved as $NAME.bak)"
}
refresh_runner
```

**Windows (run in PowerShell):**

```powershell
function Update-LindaRunner {
  $Key  = "PASTE-LICENSE-KEY-FROM-STEP-1"
  $Api  = "https://lindaai-api-production.up.railway.app"
  $Name = "rooster-daily.ps1"                   # fixed name - never taken from the server
  $Dest = Join-Path (Join-Path (Join-Path $env:USERPROFILE ".claude") "lindaai") $Name   # fixed destination
  $Tmp  = "$Dest.new.$PID"
  function Keep($why) { Remove-Item -LiteralPath $Tmp, "$Dest.bak.new" -Force -ErrorAction SilentlyContinue; "RUNNER: kept current ($why)" }
  function Ver($p) {
    $hit = Get-Content -LiteralPath $p -TotalCount 20 | Select-String -Pattern '^# RUNNER_V=(\d{1,6})\s*$' | Select-Object -First 1
    if ($hit) { [int]$hit.Matches[0].Groups[1].Value } else { $null }
  }

  if (-not (Test-Path -LiteralPath $Dest -PathType Leaf)) { return "RUNNER: not installed - skip" }
  $link = $null; try { $link = (Get-Item -LiteralPath $Dest -Force).LinkType } catch {}
  if ($link -in 'SymbolicLink','Junction') { return "RUNNER: left alone (it is a link the owner manages)" }
  Get-ChildItem -LiteralPath (Split-Path -Parent $Dest) -Filter "$Name.new.*" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue   # leftovers from an interrupted run
  Remove-Item -LiteralPath "$Dest.bak.new" -Force -ErrorAction SilentlyContinue
  try { [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12 } catch {}
  try { $m = Invoke-RestMethod -Uri "$Api/v1/sync/scripts/$Key" -TimeoutSec 20 -MaximumRedirection 0 -ErrorAction Stop }
  catch { return (Keep "could not reach server") }
  $want = "$(($m.scripts | Where-Object { $_.name -eq $Name } | Select-Object -First 1).sha256)".ToLower()
  if ($want -notmatch '^[0-9a-f]{64}$') { return (Keep "server sent no valid hash") }
  if ((Get-FileHash -LiteralPath $Dest -Algorithm SHA256).Hash.ToLower() -eq $want) { return "RUNNER: already current" }

  try { Invoke-WebRequest -Uri "$Api/v1/sync/script/$Key/$Name" -OutFile $Tmp -UseBasicParsing -TimeoutSec 30 -MaximumRedirection 0 -ErrorAction Stop }
  catch { return (Keep "download failed") }
  if ((Get-FileHash -LiteralPath $Tmp -Algorithm SHA256).Hash.ToLower() -ne $want) { return (Keep "hash mismatch") }
  $size = (Get-Item -LiteralPath $Tmp).Length
  if ($size -lt 1000 -or $size -gt 200000) { return (Keep "unexpected size $size") }
  $errs = $null
  [void][System.Management.Automation.Language.Parser]::ParseFile($Tmp, [ref]$null, [ref]$errs)
  if ($errs -and $errs.Count -gt 0) { return (Keep "failed syntax check") }
  $newV = Ver $Tmp; $oldV = Ver $Dest
  if ($null -eq $newV) { return (Keep "server copy carries no version") }
  if ($null -ne $oldV -and $newV -lt $oldV) {
    Remove-Item -LiteralPath $Tmp -Force -ErrorAction SilentlyContinue
    return "RUNNER: already current (yours is newer than the server copy)"
  }

  try {
    Copy-Item -LiteralPath $Dest -Destination "$Dest.bak.new" -Force -ErrorAction Stop
    Move-Item -LiteralPath $Tmp -Destination $Dest -Force -ErrorAction Stop
  } catch { return (Keep "could not replace") }
  try { Move-Item -LiteralPath "$Dest.bak.new" -Destination "$Dest.bak" -Force -ErrorAction Stop }
  catch { Remove-Item -LiteralPath "$Dest.bak.new" -Force -ErrorAction SilentlyContinue; return "RUNNER: updated (no backup copy could be saved)" }
  "RUNNER: updated (previous copy saved as $Name.bak)"
}
Update-LindaRunner
```

Read the one `RUNNER:` line it prints and carry it into the report. Match on how the line STARTS —
anything in parentheses after it is detail, not a new case:
- `RUNNER: updated…` → *"🐓 Rooster's runner updated — he crows on the same schedule as before."*
- `RUNNER: already current…` or `RUNNER: not installed - skip…` → say nothing (no news is good news).
- `RUNNER: left alone…` → one calm line: *"🐓 Your Rooster runner is a link you manage yourself, so I left it
  alone, partner."*
- `RUNNER: kept current (…)` → one calm line: *"🐓 Couldn't refresh Rooster's runner this time (<reason>) — your
  current one is untouched and still works. I'll try again next sync."* Never alarm the customer, never retry in a loop.
- No `RUNNER:` line at all (the block itself errored) → treat it as `kept current`: say the calm line, change nothing.

To roll back an update by hand, copy `rooster-daily.sh.bak` (or `.ps1.bak`) back over the script in
`~/.claude/lindaai/`.

### Step 6 — Report to user

```
🔄 LindaAI Sync Report

Tier: Platinum
✓ 47 skills up to date
+ 3 new skills added: linda-coliving, linda-reviews, personal-brand-audit
~ 1 skill updated: linda-deals (improved cap-rate logic)
- 0 skills removed

Platinum agents:
✓ 17 agents up to date
+ 1 new agent added: Bullhorn

🐓 Rooster's runner updated — he crows on the same schedule as before.

Done! Yeee Hawww 🤠
```

If `linda-sync` itself was one of the skills updated in this run, add one line: *"I just got new sync
instructions too, partner — start a fresh session and run `/linda-sync` once more so they take effect."*
(The steps you are following right now are the OLD ones; the new ones only load next session.)

If nothing changed:
```
🔄 LindaAI Sync — already up to date. All 51 skills + 18 agents current. 🤠
```

## Endpoints reference

All under `https://lindaai-api-production.up.railway.app`:

| Endpoint | Purpose |
|---|---|
| `GET /v1/sync/manifest/{key}` | List skills + hashes for this tier |
| `GET /v1/sync/skill/{key}/{name}` | Fetch one skill's SKILL.md |
| `GET /v1/sync/agents/{key}` | List agents + hashes (Platinum only) |
| `GET /v1/sync/agent/{key}/{name}` | Fetch one agent .md (Platinum only) |
| `GET /v1/sync/scripts/{key}` | List runner scripts + hashes for this tier |
| `GET /v1/sync/script/{key}/{name}` | Fetch one runner script (exact bytes) |

No admin key required — the customer's license key authenticates.

## Locked picker behavior

If `locked: true` on the license response, tell the user: "Your skill selections are locked for this billing period. To swap, upgrade to Platinum for full access."

## Error handling

- Network failure → "Couldn't reach LindaAI servers. Check internet and try again."
- Server error (5xx) → "LindaAI servers are temporarily down. Try again in a few minutes."
- Picker URL: If user asks how to change skills, point them to `https://app.lindaai-brain.com/picker/`

---

© 2022-2026 Daniel Wise · LindaAI
All rights reserved · support@lindaai-brain.com
