---
name: telegram-setup
description: Set up the LindaAI Telegram bridge so the user can chat with their LindaAI from their phone. Walks them through creating a Telegram bot, getting their Anthropic API key, and starting the bridge. Use when user says "/telegram-setup", "set up telegram", "connect my phone", "telegram bridge", "telegram bot", "chat from phone", "mobile access", "text LindaAI".
---

# /telegram-setup — Connect LindaAI to Telegram

Walks the customer through creating their Telegram bot + wiring it to the Anthropic API so they can text LindaAI from their phone.

## Why this setup is the way it is (so you don't deviate)

The Telegram bot connects DIRECTLY to the Anthropic API using the customer's own API key — it does NOT depend on the local `claude` CLI binary. This mirrors the Discord bot fix (Isaac incident, 2026-05-25):

- Cowork desktop app installs the `claude` binary in a hidden internal path the bot can't find
- Even when found, that binary isn't callable as a CLI (Exec format error)
- The fix: don't use the CLI. Use the Anthropic Python SDK directly.

So **do NOT skip the API key step**. Without it the bot won't start.

## Walk the user through these steps in order

### Step 1: Create a Telegram bot

> "Open Telegram. Search for **@BotFather** (the official blue-check account). Send `/newbot`. It'll ask for a name (e.g. 'My LindaAI') and a username (must end in `bot`, e.g. `my_lindaai_bot`). BotFather replies with your bot TOKEN — a long string like `123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`. **Copy that token and paste it here.**"

Wait for the user to paste the token.

### Step 2: Get an Anthropic API key

> "Open `https://console.anthropic.com/settings/keys` in a browser. Sign in with the email you use for Claude. Click **Create Key**, name it 'LindaAI Telegram', copy the key (starts with `sk-ant-...`). You won't see it again so save it. **Paste it here.**"

If they don't have an Anthropic account yet, walk them through signup at console.anthropic.com first. A small balance ($5-10) is plenty to start.

### Step 3: Get the user's Telegram ID

We need this BEFORE starting the bot so the env file is complete on first run.

> "In Telegram, search for **@userinfobot** and send it any message. It'll reply with your Telegram user ID (a number like `123456789`). **Paste that number here.**"

(Alternative: start the bot with a placeholder, send `/whoami` to your new bot, then update the env — but doing it up front is cleaner.)

### Step 4: Save everything to telegram.env

```bash
mkdir -p ~/.claude/lindaai
cat > ~/.claude/lindaai/telegram.env <<EOF
TELEGRAM_BOT_TOKEN=<token-from-step-1>
ANTHROPIC_API_KEY=<key-from-step-2>
TELEGRAM_ALLOWED_USER_ID=<id-from-step-3>
ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
EOF
chmod 600 ~/.claude/lindaai/telegram.env
```

### Step 5: Install dependencies + start the bot

```bash
pip3 install --user python-telegram-bot anthropic
mkdir -p ~/.claude/lindaai/telegram-bridge
# Copy from the LindaAI install folder:
cp <THIS_FOLDER>/bridges/telegram/bot.py ~/.claude/lindaai/telegram-bridge/
cp <THIS_FOLDER>/bridges/telegram/run-bot.sh ~/.claude/lindaai/telegram-bridge/
cp <THIS_FOLDER>/bridges/telegram/stop-bot.sh ~/.claude/lindaai/telegram-bridge/
chmod +x ~/.claude/lindaai/telegram-bridge/*.sh
bash ~/.claude/lindaai/telegram-bridge/run-bot.sh
```

The bot will print "✓ LindaAI Telegram Bridge starting..." and then "✓ Bot online."

### Step 6: Test

> "Open Telegram, find your new bot, send `/start`. You should get a Howdy back. Send any message — LindaAI will answer from the Anthropic API directly. To capture a content idea fast, send `c: my idea` and it lands in your inbox. Use `bash ~/.claude/lindaai/telegram-bridge/stop-bot.sh` to stop. LindaAI has your back."

## Troubleshooting (paste these if customer reports issues)

| Symptom | Fix |
|---|---|
| Bot won't start, "ANTHROPIC_API_KEY not set" | Step 2 missed. Add the key to `~/.claude/lindaai/telegram.env`. |
| "Application did not respond" / errors on every message | Anthropic API key invalid or no balance. Check `console.anthropic.com/settings/billing`. |
| "🔒 This LindaAI is bound to its owner only." | TELEGRAM_ALLOWED_USER_ID doesn't match the user texting. Send `/whoami` to verify. |
| Bot crashes on startup | Token has whitespace or quotes around it in telegram.env. Edit and clean. |
| Bot online but doesn't respond to messages | Make sure you DM'd the bot you created — bots don't respond in random Telegram chats. |
| "anthropic SDK not installed" on start | Re-run: `pip3 install --user anthropic python-telegram-bot` |

## Auto-start on boot (optional — offer if they ask)

Create `~/Library/LaunchAgents/com.lindaai.telegram.plist` with a `RunAtLoad=true` entry calling `run-bot.sh`. The run script handles double-start prevention.

---

© 2026 LindaAI — Built by Daniel Wise
