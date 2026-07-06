---
name: discord-setup
description: Set up the LindaAI Discord bridge so the user can chat with LindaAI via Discord slash commands. Walks them through creating a Discord bot, generating a Claude Code OAuth token (Max sub - no API charges) or API key fallback, grabbing Discord IDs, and starting the bridge. Use when user says "/discord-setup", "set up discord", "connect discord", "discord bridge", "discord bot", "chat from discord", "lindaai on discord".
---

# /discord-setup — Connect LindaAI to Discord (slash-command bot)

Walks the customer through creating their Discord bot + wiring it to their Claude Max subscription (or API key fallback) so they can chat with LindaAI from Discord using `/linda` slash commands.

**Target time: 10-15 minutes.** Every step below was field-tested during Boss's own install — every gotcha that bit him has a patch in here so it never bites a customer.

---

## Why this setup looks the way it does (do not deviate)

Lessons baked in from real customer pain:

1. **NO Privileged Intents.** Bot uses slash commands ONLY — never `on_message` and never Message Content Intent. Customer never has to flip any toggle in the Discord developer portal.
2. **CLAUDE CODE OAUTH (default) — NO API CHARGES.** Bot subprocess'es the local `claude` CLI with `CLAUDE_CODE_OAUTH_TOKEN`. Authenticates against the customer's Claude Max subscription. Messages don't cost extra — they're covered by Max.
3. **API key is a fallback only.** Customers who don't have Max sub can paste an `ANTHROPIC_API_KEY` instead. ~$0.003/message.
4. **Instant slash-command sync.** First run syncs to the customer's specific server via `DISCORD_GUILD_ID` — slash commands appear immediately (no 1-hour global propagation wait).
5. **Discord moved their menus.** Copy User ID + Copy Server ID are accessed via **LEFT-CLICK**, not right-click. (Discord changed the UX — old docs everywhere are wrong.)
6. **macOS Python ships without SSL certs.** Discord bot won't connect on a fresh Mac until Install Certificates.command runs once.
7. **Empty shell env var bug.** Bot's env loader uses conditional override — if shell has `ANTHROPIC_API_KEY=""` set (common from prior installs), the file value wins. Old `setdefault` quietly broke this.
8. **Unbuffered logs.** `python3 -u` so startup output flushes immediately — customers see `online` instead of an empty log.

Walk the user through the steps IN ORDER. Confirm at each gate before moving on.

---

## Prerequisites (10 sec each — skip and they bite later)

### P1. macOS users — Install Python SSL certificates (one-time)

> "Open Finder -> Applications -> 'Python 3.12' folder -> double-click **Install Certificates.command**. A terminal window flashes, says 'update complete', and closes. Done."

(Without this, the bot fails with `SSLCertVerificationError` when it tries to connect to Discord. Bites every fresh-Mac customer.)

### P2. Discord account + a server YOU own

> "Open Discord. Look at the far-left vertical strip of server icons. If you DON'T already own a server: click the **`+`** button at the bottom -> **Create My Own** -> **For me and my friends** -> name it `LindaAI HQ` (or similar) -> **Create**. You need to be the server owner so you can invite a bot."

(Most customers don't own a server yet. This is the #1 stuck point. Address upfront.)

### P3. Claude Code installed + logged in

> "Open Terminal:  `claude --version`. You should see `2.x.x (Claude Code)`. If not, install:  `npm install -g @anthropic-ai/claude-code`, then run `claude` once and complete the login flow."

---

## Step 1 — Create the Discord bot application

> "Open `https://discord.com/developers/applications`. Log in. Click **New Application** (top-right). Name it 'My LindaAI' or similar -> check the dev terms box -> **Create**."

Wait for confirmation that they're inside the new app's dashboard.

## Step 2 — Get the bot token

> "Left sidebar -> **Bot**. Scroll to the **Token** section. Click **Reset Token** -> confirm with password/2FA -> click **Copy**. Save it somewhere safe (Notes, password manager). **Discord shows it ONLY ONCE.**"

Tell them to save it but NOT paste it in chat yet — we'll write it to discord.env later in one swoop.

## Step 3 — Invite the bot to your server

> "Left sidebar -> **OAuth2**. Scroll to **OAuth2 URL Generator**. Under **Scopes** check `bot` AND `applications.commands`. A **Bot Permissions** section appears below — check `Send Messages` and `Use Slash Commands`. Copy the **Generated URL** at the bottom -> open in new browser tab -> pick your server from the dropdown -> **Continue -> Authorize -> captcha**."

Confirm the bot shows up in the server's member list (greyed out / offline is normal — we haven't started it yet).

## Step 4 — Get the Claude Code OAuth token (RECOMMENDED — NO CHARGES)

> "In Terminal:  `claude setup-token`.
>
> Your browser opens to a Claude OAuth flow. Sign in if needed. Click **Authorize**. Terminal prints a long token starting with `sk-ant-oat01-...`. **Save it.**
>
> (This token authenticates the bot against YOUR Claude Max subscription. Bot messages don't cost extra — they're covered by Max. NO API charges.)"

**If they don't have Claude Max:** they can use an Anthropic API key instead. Go to `console.anthropic.com/settings/keys` -> Create Key -> save it. They also need to add at least $5 at `console.anthropic.com/settings/billing`. ~$0.003 per `/linda` message.

## Step 5 — Get your Discord User ID + Server ID

> "In Discord: gear icon (bottom-left) -> **Advanced** -> toggle **Developer Mode** ON. Close settings.
>
> Then **LEFT-CLICK your own avatar** (bottom-left mini-profile, next to your name) -> scroll down the menu -> **Copy User ID**. Save it (just digits, ~18 chars).
>
> **LEFT-CLICK your server icon** (far-left strip) -> scroll down -> **Copy Server ID**. Save it.
>
> ⚠️ LEFT-click, NOT right-click. Discord moved the menu — most online docs are out of date."

## Step 6 — Write discord.env

```bash
mkdir -p ~/.claude/lindaai
nano ~/.claude/lindaai/discord.env
```

Paste this, fill in the blanks (no quotes, no spaces around `=`):

```env
DISCORD_BOT_TOKEN=<token-from-step-2>
DISCORD_ALLOWED_USER_ID=<user-id-from-step-5>
DISCORD_GUILD_ID=<server-id-from-step-5>
CLAUDE_CODE_OAUTH_TOKEN=<oauth-from-step-4>
# Leave ANTHROPIC_API_KEY blank if using OAuth above.
ANTHROPIC_API_KEY=
```

Save (Ctrl+O, Enter, Ctrl+X for nano) and lock it down:

```bash
chmod 600 ~/.claude/lindaai/discord.env
```

## Step 7 — Install dependencies + launch the bot

```bash
pip3 install --user discord.py
mkdir -p ~/.claude/lindaai/discord-bridge
# Copy the bridge files from the LindaAI install:
cp <LINDAAI_INSTALL>/bridges/discord/bot.py ~/.claude/lindaai/discord-bridge/
cp <LINDAAI_INSTALL>/bridges/discord/run-bot.sh ~/.claude/lindaai/discord-bridge/
cp <LINDAAI_INSTALL>/bridges/discord/stop-bot.sh ~/.claude/lindaai/discord-bridge/
chmod +x ~/.claude/lindaai/discord-bridge/*.sh
bash ~/.claude/lindaai/discord-bridge/run-bot.sh
```

The bot prints:
```
LindaAI Discord Bridge online as <BotName>#XXXX
  Auth: Claude Max subscription (ANTHROPIC_API_KEY stripped)
  Synced 2 commands to guild <ID> (instant)
```

## Step 8 — Test it

> "Open Discord -> your server -> any text channel. Type `/` — `/linda` and `/howdy` should appear in autocomplete. Try `/howdy` first (quickest test). Wait ~10-15 sec on first call — claude CLI cold start. Bot replies as LindaAI."

To stop: `bash ~/.claude/lindaai/discord-bridge/stop-bot.sh`

---

## Step 9 (recommended) — Make the bot auto-start at login (launchd daemon)

For an always-on bot that survives reboot + auto-restarts on crash (like the Telegram bridge), use a launchd daemon. **One-time setup, ~60 seconds:**

```bash
# 1. Build a venv so launchd's python has discord.py available
#    (system /usr/bin/python3 doesn't see --user pip installs)
python3 -m venv ~/.claude/lindaai/discord-bridge/venv
~/.claude/lindaai/discord-bridge/venv/bin/pip install discord.py

# 2. Copy the plist template:
cp <LINDAAI_INSTALL>/bridges/discord/com.lindaai.discord-bridge.plist.template \
   ~/Library/LaunchAgents/com.lindaai.discord-bridge.plist

# 3. Edit the plist with TextEdit:
open -a TextEdit ~/Library/LaunchAgents/com.lindaai.discord-bridge.plist
```

**In the plist, replace:**
- `PASTE_YOUR_OAUTH_TOKEN_HERE` → your token from Step 4
- Every occurrence of `/Users/Saucy` → your actual home dir (e.g. `/Users/yourname`)
  - Tip: Cmd+F in TextEdit → find `/Users/Saucy` → "Replace All"

**Save (Cmd+S) and load it:**

```bash
launchctl load ~/Library/LaunchAgents/com.lindaai.discord-bridge.plist
```

**Verify:**
```bash
launchctl list | grep com.lindaai.discord
# Should show PID + 0 exit code
tail ~/.claude/lindaai/discord-bridge.out.log
# Should show "LindaAI Discord Bridge online"
```

**To stop/disable:**
```bash
launchctl unload ~/Library/LaunchAgents/com.lindaai.discord-bridge.plist
```

## Troubleshooting (paste these if a customer reports issues)

| Symptom | Fix |
|---|---|
| Bot online but no slash commands visible | `DISCORD_GUILD_ID` missing or wrong in discord.env. Fix + restart. |
| `Application did not respond` in Discord | Auth issue. Check bot log for 401 — re-run `claude setup-token` and replace `CLAUDE_CODE_OAUTH_TOKEN`. |
| `This LindaAI is bound to its owner only.` | `DISCORD_ALLOWED_USER_ID` doesn't match the Discord user running the slash command. Must be YOUR own User ID. |
| Bot won't start, `discord SDK not installed` | `pip3 install --user discord.py` |
| `SSLCertVerificationError` | Run macOS Python `Install Certificates.command` (Prerequisite P1 above). |
| `Failed to authenticate. API Error: 401` | OAuth token expired/revoked. Re-run `claude setup-token`. |
| `credit balance too low` (API key path only) | Add credits at `console.anthropic.com/settings/billing` ($5 = ~1,600 messages). |
| Token has whitespace/quotes in discord.env | Edit the file — no spaces around `=`, no quotes around values. |

---

© 2026 LindaAI — Built by Daniel Wise
