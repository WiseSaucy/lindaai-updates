---
name: linda-discord-setup
description: Set up the LindaAI Discord bridge so the user can chat with LindaAI via Discord DMs or @mentions. Walks them through creating a Discord bot app, getting the token, and starting the bridge. Use when user says "/discord-setup", "set up discord", "connect discord", "discord bridge", "discord bot", "chat from discord", "lindaai on discord".
---

# /discord-setup — Connect LindaAI to Discord

Walks the customer through creating their own Discord bot and starting the LindaAI Discord bridge.

## Walk the user through these steps in order

### Step 1: Create a Discord bot application

Tell them exactly:
> "Open `https://discord.com/developers/applications` in your browser. Log in with your Discord account. Click **New Application** top-right, name it 'My LindaAI' or similar, click **Create**. In the left sidebar click **Bot**. Click **Reset Token** and copy the bot token (you'll only see it once — save it). **Paste that token here.**"

Wait for the user to paste the token.

### Step 2: Enable the Message Content intent

Tell them:
> "Still on the Bot page, scroll down to 'Privileged Gateway Intents' and toggle ON **Message Content Intent**. Save changes."

### Step 3: Invite the bot to your server (or DM)

Tell them:
> "In the left sidebar click **OAuth2 → URL Generator**. Under 'Scopes' check `bot`. Under 'Bot Permissions' check `Send Messages`, `Read Message History`, `Attach Files`. Copy the generated URL at the bottom, paste into a new browser tab, and invite the bot to a Discord server you own — OR just open a DM with the bot directly after it's online."

### Step 4: Save the token

Write to `~/.claude/lindaai/discord.env`:
```
mkdir -p ~/.claude/lindaai
cat > ~/.claude/lindaai/discord.env <<EOF
DISCORD_BOT_TOKEN=<user-pasted-token>
DISCORD_ALLOWED_USER_ID=
EOF
```

### Step 5: Get the user's Discord ID and save it

Tell them:
> "In Discord, go to **Settings → Advanced** and turn on **Developer Mode**. Then right-click your own avatar anywhere and click **Copy User ID**. **Paste the ID here.**"

Wait for ID, then:
```
sed -i '' "s/DISCORD_ALLOWED_USER_ID=/DISCORD_ALLOWED_USER_ID=<id>/" ~/.claude/lindaai/discord.env
```

### Step 6: Install bridge + start

```
mkdir -p ~/.claude/lindaai/discord-bridge
# Copy bot.py + run-bot.sh + stop-bot.sh from the install (or GitHub raw)
chmod +x ~/.claude/lindaai/discord-bridge/*.sh
bash ~/.claude/lindaai/discord-bridge/run-bot.sh
```

Installs `discord.py` and starts the bot.

### Step 7: Test

Tell them:
> "Open Discord, DM your new bot, send 'Howdy'. LindaAI should respond from your laptop. In a server, you can also @mention the bot to chat. Use `bash ~/.claude/lindaai/discord-bridge/stop-bot.sh` to stop. LindaAI has your back."

---

© 2026 LindaAI — Built by Daniel Wise
