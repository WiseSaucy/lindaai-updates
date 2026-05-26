---
name: discord-setup
description: Set up the LindaAI Discord bridge so the user can chat with LindaAI via Discord slash commands. Walks them through creating a Discord bot app, getting their Anthropic API key, server ID, and starting the bridge. Use when user says "/discord-setup", "set up discord", "connect discord", "discord bridge", "discord bot", "chat from discord", "lindaai on discord".
---

# /discord-setup — Connect LindaAI to Discord (slash-command bot)

Walks the customer through creating their Discord bot + wiring it to the Anthropic API so they can chat with LindaAI from Discord using `/linda` slash commands.

## Why this setup is the way it is (so you don't deviate)

Three issues bit customer #1 (Isaac King, 2026-05-25). Boss47 mandated they never bite anyone else:

1. **NO Privileged Intents.** This bot uses slash commands ONLY — never `on_message` and never `Message Content Intent`. The customer never has to flip any toggle in the Discord developer portal.
2. **Anthropic API directly — not the local `claude` CLI.** Different customers store the Claude binary in different places, and the Cowork desktop app's bundled binary isn't callable. Bot connects straight to the Anthropic API using the customer's own API key.
3. **Instant slash-command sync.** First run also syncs to the customer's specific server via `DISCORD_GUILD_ID`, so slash commands appear immediately (not after a 1-hour global propagation wait).

Walk the customer through these steps IN ORDER. Do not skip the API key step. Do not tell them to enable Message Content Intent — that's the old broken way.

## Walk the user through these steps in order

### Step 1: Create a Discord bot application

> "Open `https://discord.com/developers/applications` in your browser. Log in with your Discord account. Click **New Application** top-right, name it 'My LindaAI' or similar, click **Create**. In the left sidebar click **Bot**. Click **Reset Token** and copy the bot token (you'll only see it once — save it somewhere). **Paste that token here.**"

Wait for the user to paste the token.

### Step 2: Invite the bot to your server

> "In the left sidebar click **OAuth2 → URL Generator**. Under 'Scopes' check `bot` AND `applications.commands`. Under 'Bot Permissions' check `Send Messages`, `Use Slash Commands`. Copy the generated URL at the bottom, paste it into a new browser tab, and invite the bot to a Discord server you own. **Tell me when the bot has joined your server.**"

### Step 3: Get your Anthropic API key

> "Open `https://console.anthropic.com/settings/keys` in a new tab. Sign in with the email you use for Claude. Click **Create Key**, name it 'LindaAI Discord', copy the key (starts with `sk-ant-...`). You won't see it again so save it. **Paste it here.**"

If they say they don't have one yet, walk them through signup at console.anthropic.com first. A small balance ($5-10) is enough to start.

### Step 4: Get your Discord User ID + Server ID

> "In Discord open **Settings → Advanced** and turn on **Developer Mode**.
> Then right-click YOUR OWN AVATAR anywhere and click **Copy User ID**. Paste that here.
> Then right-click the SERVER ICON (top-left list of your server) and click **Copy Server ID**. Paste that here too."

### Step 5: Save everything to discord.env

```bash
mkdir -p ~/.claude/lindaai
cat > ~/.claude/lindaai/discord.env <<EOF
DISCORD_BOT_TOKEN=<token-from-step-1>
ANTHROPIC_API_KEY=<key-from-step-3>
DISCORD_ALLOWED_USER_ID=<user-id-from-step-4>
DISCORD_GUILD_ID=<server-id-from-step-4>
ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
EOF
chmod 600 ~/.claude/lindaai/discord.env
```

### Step 6: Install dependencies + start the bot

```bash
pip3 install --user discord.py anthropic
mkdir -p ~/.claude/lindaai/discord-bridge
# Copy the bot files from the LindaAI install
cp <THIS_FOLDER>/bridges/discord/bot.py ~/.claude/lindaai/discord-bridge/
cp <THIS_FOLDER>/bridges/discord/run-bot.sh ~/.claude/lindaai/discord-bridge/
cp <THIS_FOLDER>/bridges/discord/stop-bot.sh ~/.claude/lindaai/discord-bridge/
chmod +x ~/.claude/lindaai/discord-bridge/*.sh
bash ~/.claude/lindaai/discord-bridge/run-bot.sh
```

The bot will print "✓ LindaAI Discord Bridge online" and "✓ Synced N commands to guild ... (instant)".

### Step 7: Test

> "Open Discord on your server. Type `/` in any channel — you should see `/linda` and `/howdy` slash commands available. Try `/linda what's on my plate today` to test. To stop the bot: `bash ~/.claude/lindaai/discord-bridge/stop-bot.sh`."

## Troubleshooting (paste these if customer reports issues)

| Symptom | Fix |
|---|---|
| Bot online but no slash commands visible | Check that DISCORD_GUILD_ID is set correctly in discord.env (Step 4). Restart the bot. |
| "Application did not respond" | Anthropic API key invalid or no balance. Check `console.anthropic.com/settings/billing`. |
| "🔒 This LindaAI is bound to its owner only." | DISCORD_ALLOWED_USER_ID doesn't match the user who's running the slash command. Double-check Step 4 — it must be YOUR Discord ID. |
| Bot won't start, "anthropic SDK not installed" | Re-run: `pip3 install --user anthropic discord.py` |
| Bot crashes on startup with token error | Token in discord.env has whitespace or quotes around it. Edit and clean. |

---

© 2026 LindaAI — Built by Daniel Wise
