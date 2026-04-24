#!/usr/bin/env python3
"""
LindaAI Discord Bridge — generic customer-ready bot.

Reads DISCORD_BOT_TOKEN + DISCORD_ALLOWED_USER_ID from ~/.claude/lindaai/discord.env
Forwards owner messages (DMs or @mentions in servers) to the local `claude` CLI.

© 2026 LindaAI — Built by Daniel Wise
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import discord
except ImportError:
    print("ERROR: discord.py not installed.")
    print("  Run: pip3 install discord.py")
    sys.exit(1)


ENV_FILE = Path.home() / ".claude" / "lindaai" / "discord.env"
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")
ALLOWED_USER_ID = os.environ.get("DISCORD_ALLOWED_USER_ID", "")

if not TOKEN:
    print("ERROR: DISCORD_BOT_TOKEN not set in ~/.claude/lindaai/discord.env")
    print("       Run /discord-setup to configure.")
    sys.exit(1)

CLAUDE_BIN = shutil.which("claude")
if not CLAUDE_BIN:
    for candidate in [
        Path.home() / ".npm-global" / "bin" / "claude",
        Path.home() / ".local" / "bin" / "claude",
        Path.home() / ".claude" / "local" / "claude",
        Path("/opt/homebrew/bin/claude"),
        Path("/usr/local/bin/claude"),
    ]:
        if candidate.exists():
            CLAUDE_BIN = str(candidate)
            break


intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

client = discord.Client(intents=intents)


async def send_chunked(channel, text: str):
    """Discord caps messages at 2000 chars."""
    CHUNK = 1900
    for i in range(0, len(text), CHUNK):
        await channel.send(text[i:i + CHUNK])


@client.event
async def on_ready():
    print(f"✓ LindaAI Discord Bridge online as {client.user}")
    print(f"  Bound to user ID: {ALLOWED_USER_ID or '(open — unbound)'}")
    print(f"  Claude CLI: {CLAUDE_BIN or 'NOT FOUND'}")


@client.event
async def on_message(message: discord.Message):
    # Don't talk to ourselves
    if message.author.id == client.user.id:
        return

    # Respond to DMs always, or to @mentions in servers
    is_dm = isinstance(message.channel, discord.DMChannel)
    is_mention = client.user in message.mentions
    if not (is_dm or is_mention):
        return

    user_id = str(message.author.id)
    if ALLOWED_USER_ID and user_id != ALLOWED_USER_ID:
        await message.channel.send(
            "🔒 This LindaAI is bound to its owner only."
        )
        print(f"[SECURITY] Rejected message from Discord user {user_id}")
        return

    # Clean the message (strip @mention if present)
    user_msg = message.content.replace(f"<@{client.user.id}>", "").strip()
    if not user_msg:
        user_msg = "Howdy!"

    async with message.channel.typing():
        if not CLAUDE_BIN:
            await message.channel.send("❌ Claude CLI not found. Install Claude Code first.")
            return
        try:
            result = subprocess.run(
                [CLAUDE_BIN, "-p", user_msg],
                capture_output=True,
                text=True,
                timeout=180,
            )
            response = result.stdout.strip() or result.stderr.strip() or "LindaAI had trouble — try again, partner."
        except subprocess.TimeoutExpired:
            response = "⏳ Took too long. LindaAI timed out — try a shorter question."
        except Exception as e:
            response = f"❌ Error: {e}"

    await send_chunked(message.channel, response)


if __name__ == "__main__":
    client.run(TOKEN)
