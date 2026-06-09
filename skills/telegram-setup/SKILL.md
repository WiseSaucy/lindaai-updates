---
name: telegram-setup
description: Set up the LindaAI Telegram bridge so the user can chat with their LindaAI from their phone. Walks them through creating a Telegram bot, generating a Claude Code OAuth token (Max sub - no API charges) or API key fallback, locking the bot to their Telegram user ID, and starting the bridge. Use when user says "/telegram-setup", "set up telegram", "connect my phone", "telegram bridge", "telegram bot", "chat from phone", "mobile access", "text LindaAI".
---

# /telegram-setup — Connect LindaAI to Telegram

Walks the customer through creating their Telegram bot + wiring it to their Claude Max subscription (or API key fallback) so they can text LindaAI from their phone.

**Target time: 10-15 minutes.** Every step below was field-tested during Boss47's own bridge setup — same gotchas as Discord are pre-patched.

---

## Why this setup looks the way it does (do not deviate)

Lessons baked in (matches the Discord bridge pattern):

1. **CLAUDE CODE OAUTH (default) — NO API CHARGES.** Bot subprocess'es the local `claude` CLI with `CLAUDE_CODE_OAUTH_TOKEN`. Authenticates against the customer's Claude Max subscription. Texts don't cost extra — they're covered by Max.
2. **API key is a fallback only.** Customers without Max sub can paste an `ANTHROPIC_API_KEY` instead. ~$0.003/message.
3. **Empty shell env var bug.** Bot's env loader uses conditional override — if shell has `ANTHROPIC_API_KEY=""` set (common from prior installs), the file value wins. Old `setdefault` quietly broke this.
4. **Unbuffered logs.** `python3 -u` so startup output flushes immediately — customers see `online` instead of an empty log.
5. **Owner-only by default.** `TELEGRAM_ALLOWED_USER_ID` locks the bot to you — randos who find your bot get a 🔒 reply.

Walk the user through the steps IN ORDER. Confirm at each gate before moving on.

---

## Prerequisites (do these FIRST — skipping = customer pain)

### P1. macOS users — Install Python SSL certificates (one-time)

> "Open Finder -> Applications -> 'Python 3.12' folder -> double-click **Install Certificates.command**. A terminal window flashes, says 'update complete', and closes. Done."

(Without this, the bot fails with `SSLCertVerificationError` when it talks to Telegram or Anthropic. Bites every fresh-Mac customer.)

### P2. Claude Code installed + logged in

> "Open Terminal:  `claude --version`. You should see `2.x.x (Claude Code)`. If not: `npm install -g @anthropic-ai/claude-code`, then run `claude` once and complete login."

---

## Step 1 — Create the Telegram bot

> "Open Telegram on phone or desktop. Search for **@BotFather** (official blue-check). Send `/newbot`. It asks for a name (e.g. 'My LindaAI') and a username (must end in `bot`, e.g. `my_lindaai_bot`). BotFather replies with your bot TOKEN — a long string like `123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`. **Save it.**"

## Step 2 — Get the Claude Code OAuth token (RECOMMENDED — NO CHARGES)

> "In Terminal:  `claude setup-token`.
>
> Browser opens to a Claude OAuth flow. Sign in if needed. Click **Authorize**. Terminal prints a token starting with `sk-ant-oat01-...`. **Save it.**
>
> (This token authenticates the bot against YOUR Claude Max subscription. Messages don't cost extra — they're covered by Max. NO API charges.)"

**If they don't have Claude Max:** they can use an Anthropic API key instead. Go to `console.anthropic.com/settings/keys` -> Create Key -> save it. Also add at least $5 at `console.anthropic.com/settings/billing`. ~$0.003 per message.

## Step 3 — Get your Telegram user ID

> "In Telegram, search for **@userinfobot**. Send it any message. It replies with your Telegram user ID (a number like `123456789`). **Save it.**
>
> Alternative: skip this for now and use `/whoami` after the bot's running — it'll print your ID."

## Step 4 — Write telegram.env

```bash
mkdir -p ~/.claude/lindaai
nano ~/.claude/lindaai/telegram.env
```

Paste this, fill in the blanks (no quotes, no spaces around `=`):

```env
TELEGRAM_BOT_TOKEN=<token-from-step-1>
TELEGRAM_ALLOWED_USER_ID=<id-from-step-3>
CLAUDE_CODE_OAUTH_TOKEN=<oauth-from-step-2>
# Leave ANTHROPIC_API_KEY blank if using OAuth above.
ANTHROPIC_API_KEY=
```

Save (Ctrl+O, Enter, Ctrl+X for nano) and lock it:

```bash
chmod 600 ~/.claude/lindaai/telegram.env
```

## Step 5 — Install dependencies + launch the bot

```bash
pip3 install --user python-telegram-bot
mkdir -p ~/.claude/lindaai/telegram-bridge
# Copy the bridge files from the LindaAI install:
cp <LINDAAI_INSTALL>/bridges/telegram/bot.py ~/.claude/lindaai/telegram-bridge/
cp <LINDAAI_INSTALL>/bridges/telegram/run-bot.sh ~/.claude/lindaai/telegram-bridge/
cp <LINDAAI_INSTALL>/bridges/telegram/stop-bot.sh ~/.claude/lindaai/telegram-bridge/ 2>/dev/null
chmod +x ~/.claude/lindaai/telegram-bridge/*.sh
bash ~/.claude/lindaai/telegram-bridge/run-bot.sh
```

The bot prints:
```
LindaAI Telegram Bridge starting
  Auth: Claude Max subscription (ANTHROPIC_API_KEY stripped)
  Bot online. Message your bot on Telegram!
```

## Step 6 — Test it

> "Open Telegram, find your new bot, send `/start`. You should get a Howdy back. Then send any message — LindaAI replies with full personality + agent voice from your CLAUDE.md."

To stop: `bash ~/.claude/lindaai/telegram-bridge/stop-bot.sh`

---

## Step 7 (recommended) — Make the bot auto-start at login (launchd daemon)

For an always-on bot that survives reboot + auto-restarts on crash, use a launchd daemon. **One-time setup, ~60 seconds:**

```bash
# 1. Build a venv so launchd's python has python-telegram-bot available
python3 -m venv ~/.claude/lindaai/telegram-bridge/venv
~/.claude/lindaai/telegram-bridge/venv/bin/pip install python-telegram-bot

# 2. Copy the plist template:
cp <LINDAAI_INSTALL>/bridges/telegram/com.lindaai.telegram-bridge.plist.template \
   ~/Library/LaunchAgents/com.lindaai.telegram-bridge.plist

# 3. Edit the plist with TextEdit:
open -a TextEdit ~/Library/LaunchAgents/com.lindaai.telegram-bridge.plist
```

**In the plist, replace:**
- `PASTE_YOUR_OAUTH_TOKEN_HERE` -> your token from Step 2
- Every occurrence of `/Users/Saucy` -> your actual home dir (e.g. `/Users/yourname`)
  - Tip: Cmd+F in TextEdit -> find `/Users/Saucy` -> "Replace All"

**Save (Cmd+S) and load it:**

```bash
launchctl load ~/Library/LaunchAgents/com.lindaai.telegram-bridge.plist
```

**Verify:**
```bash
launchctl list | grep com.lindaai.telegram
# Should show PID + 0 exit code
tail ~/.claude/lindaai/telegram-bridge.out.log
# Should show "LindaAI Telegram Bridge starting" and "Bot online"
```

**To stop/disable:**
```bash
launchctl unload ~/Library/LaunchAgents/com.lindaai.telegram-bridge.plist
```

## Troubleshooting (paste these if a customer reports issues)

| Symptom | Fix |
|---|---|
| Bot won't start, `TELEGRAM_BOT_TOKEN not set` | Step 1 missed. Add the token to `~/.claude/lindaai/telegram.env`. |
| `python-telegram-bot not installed` | `pip3 install --user python-telegram-bot` |
| `Failed to authenticate. API Error: 401` | OAuth token expired/revoked. Re-run `claude setup-token`. |
| `credit balance too low` (API key path only) | Add credits at `console.anthropic.com/settings/billing` ($5 = ~1,600 messages). |
| `This LindaAI is bound to its owner only.` | `TELEGRAM_ALLOWED_USER_ID` doesn't match the Telegram user texting. Send `/whoami` to verify your ID. |
| Bot online but doesn't respond | Make sure you DM'd the bot you created. Bots don't respond in random Telegram chats. |
| Bot crashes on startup with token error | Whitespace or quotes around the token in telegram.env. Edit and clean. |
| `claude CLI not found` | `npm install -g @anthropic-ai/claude-code` |

---

© 2026 LindaAI — Built by Daniel Wise
