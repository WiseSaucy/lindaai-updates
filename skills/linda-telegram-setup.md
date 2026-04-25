---
name: linda-telegram-setup
description: Set up the LindaAI Telegram bridge so the user can chat with their LindaAI from their phone. Walks them through creating a Telegram bot, getting the token, and starting the bridge. Use when user says "/telegram-setup", "set up telegram", "connect my phone", "telegram bridge", "telegram bot", "chat from phone", "mobile access", "text LindaAI".
---

# /telegram-setup — Connect LindaAI to Telegram

Walks the customer through creating their own Telegram bot and starting the LindaAI Telegram bridge.

## Walk the user through these steps in order

### Step 1: Create a Telegram bot

Tell them exactly:
> "Open Telegram on your phone or desktop. Search for `@BotFather` (the official blue-check Telegram account). Start a chat with BotFather and type `/newbot`. It'll ask for a name (something like 'My LindaAI') and a username (must end in `bot`, e.g. `my_lindaai_bot`). BotFather will reply with your bot TOKEN — a long string like `123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`. **Copy that token and paste it here.**"

Wait for the user to paste the token.

### Step 2: Save the token

Write it to `~/.claude/lindaai/telegram.env`:
```
mkdir -p ~/.claude/lindaai
cat > ~/.claude/lindaai/telegram.env <<EOF
TELEGRAM_BOT_TOKEN=<user-pasted-token>
TELEGRAM_ALLOWED_USER_ID=
EOF
```

### Step 3: Install the bridge files

Copy the bridge files into `~/.claude/lindaai/telegram-bridge/`:
- On Platinum/Gold installs these come in the tier zip at `bridges/telegram/`
- If missing: download from `https://raw.githubusercontent.com/WiseSaucy/lindaai-updates/main/bridges/telegram/bot.py` + `run-bot.sh` + `stop-bot.sh`

```
mkdir -p ~/.claude/lindaai/telegram-bridge
# Copy bot.py, run-bot.sh, stop-bot.sh in here
chmod +x ~/.claude/lindaai/telegram-bridge/*.sh
```

### Step 4: Start the bot
```
bash ~/.claude/lindaai/telegram-bridge/run-bot.sh
```

This installs `python-telegram-bot` if needed and starts the bot.

### Step 5: Lock the bot to the user (security)

Tell them:
> "Open Telegram, find the bot you just created, and send it `/whoami`. It'll reply with your Telegram user ID (a number). **Paste that number here.**"

Wait for the user to paste their ID, then update the env:
```
sed -i '' "s/TELEGRAM_ALLOWED_USER_ID=/TELEGRAM_ALLOWED_USER_ID=<user-id>/" ~/.claude/lindaai/telegram.env
bash ~/.claude/lindaai/telegram-bridge/stop-bot.sh
bash ~/.claude/lindaai/telegram-bridge/run-bot.sh
```

### Step 6: Confirm

Tell them:
> "Done, partner! Send your bot any message on Telegram — LindaAI will respond from your laptop. The bot only listens to YOU. Use `bash ~/.claude/lindaai/telegram-bridge/stop-bot.sh` to stop. LindaAI has your back."

## Auto-start on boot (optional — offer if they ask)

Create `~/Library/LaunchAgents/com.lindaai.telegram.plist` with a RunAtLoad=true entry calling `run-bot.sh`.

---

© 2026 LindaAI — Built by Daniel Wise
