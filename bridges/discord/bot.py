#!/usr/bin/env python3
"""
LindaAI Discord Bridge — customer-ready, zero-friction.

Reads from ~/.claude/lindaai/discord.env:
  DISCORD_BOT_TOKEN          (required) — bot token from Discord developer portal
  ANTHROPIC_API_KEY          (required) — customer's API key from console.anthropic.com
  DISCORD_ALLOWED_USER_ID    (required) — only this Discord user can talk to the bot
  DISCORD_GUILD_ID           (optional) — server ID for INSTANT slash-command sync
                                          (falls back to global sync if not set)

THREE LESSONS BAKED IN (Isaac 2026-05-25 incident):
  1. SLASH COMMANDS ONLY — no on_message, no privileged intents. Customer doesn't
     have to flip "Message Content Intent" in the Discord portal.
  2. ANTHROPIC API DIRECT — no local `claude` CLI dependency. The Cowork desktop
     app stores claude binary in places the bot can't find; even when found, it's
     not callable as a CLI. We call the Anthropic API directly.
  3. INSTANT GUILD SYNC — first run also syncs to the customer's specific server
     so slash commands appear immediately (no 1-hour global-sync wait).

© 2026 LindaAI — Built by Daniel Wise
"""
import asyncio
import os
import sys
from pathlib import Path

# ─── DEPS ──────────────────────────────────────────────────────────────────
try:
    import discord
    from discord import app_commands
except ImportError:
    print("ERROR: discord.py not installed. Run:  pip3 install discord.py")
    sys.exit(1)

try:
    from anthropic import Anthropic
except ImportError:
    print("ERROR: anthropic SDK not installed. Run:  pip3 install anthropic")
    sys.exit(1)


# ─── ENV LOAD ──────────────────────────────────────────────────────────────
ENV_FILE = Path.home() / ".claude" / "lindaai" / "discord.env"
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

TOKEN          = os.environ.get("DISCORD_BOT_TOKEN", "").strip()
ANTHROPIC_KEY  = os.environ.get("ANTHROPIC_API_KEY", "").strip()
ALLOWED_USER   = os.environ.get("DISCORD_ALLOWED_USER_ID", "").strip()
GUILD_ID_RAW   = os.environ.get("DISCORD_GUILD_ID", "").strip()
MODEL          = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929").strip()

GUILD_ID = None
if GUILD_ID_RAW.isdigit():
    GUILD_ID = int(GUILD_ID_RAW)

# CLAUDE.md from current working folder (the LindaAI personality)
CLAUDE_MD = ""
for candidate in (Path.cwd() / "CLAUDE.md",
                  Path(__file__).resolve().parent.parent.parent / "CLAUDE.md"):
    if candidate.is_file():
        try:
            CLAUDE_MD = candidate.read_text()
            break
        except Exception:
            pass

DEFAULT_SYSTEM = (
    "You are LindaAI, the personal AI Operating System for business owners. "
    "You are warm, direct, action-oriented, and country in tone. "
    "Greet your partner with 'Howdy!' when the conversation starts. "
    "Keep replies tight — 2-5 sentences unless they ask for depth."
)
SYSTEM_PROMPT = CLAUDE_MD or DEFAULT_SYSTEM


# ─── PRE-FLIGHT ────────────────────────────────────────────────────────────
def die(msg: str) -> None:
    print(f"ERROR: {msg}")
    sys.exit(1)

if not TOKEN:
    die("DISCORD_BOT_TOKEN not set. Run /discord-setup to configure.")
if not ANTHROPIC_KEY:
    die("ANTHROPIC_API_KEY not set. Get one at console.anthropic.com, then add to ~/.claude/lindaai/discord.env")
if not ALLOWED_USER:
    die("DISCORD_ALLOWED_USER_ID not set. Run /discord-setup to set it.")
if not ALLOWED_USER.isdigit():
    die(f"DISCORD_ALLOWED_USER_ID must be numeric (got: {ALLOWED_USER!r})")


# ─── CLIENTS ───────────────────────────────────────────────────────────────
anthropic = Anthropic(api_key=ANTHROPIC_KEY)

# NO PRIVILEGED INTENTS — pure slash-command bot
intents = discord.Intents.default()  # default has NO message_content / members
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)


# ─── HELPERS ───────────────────────────────────────────────────────────────
async def ask_claude(prompt: str) -> str:
    """Call Anthropic API directly — no local CLI dependency."""
    def _call():
        msg = anthropic.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(b.text for b in msg.content if b.type == "text")
    return await asyncio.to_thread(_call)


async def send_chunked(interaction_or_resp, text: str, first_call=None):
    """Discord caps messages at 2000 chars. Chunk and send."""
    CHUNK = 1900
    chunks = [text[i:i + CHUNK] for i in range(0, len(text), CHUNK)] or ["(empty reply)"]
    first = True
    for c in chunks:
        if first:
            if first_call is not None:
                await first_call(c)
            else:
                await interaction_or_resp.send(c)
            first = False
        else:
            await interaction_or_resp.followup.send(c)


def authorized(interaction: discord.Interaction) -> bool:
    return str(interaction.user.id) == ALLOWED_USER


# ─── SLASH COMMANDS ────────────────────────────────────────────────────────
@tree.command(name="linda", description="Ask LindaAI anything — your AI Operating System")
@app_commands.describe(message="What do you want to ask LindaAI?")
async def linda(interaction: discord.Interaction, message: str):
    if not authorized(interaction):
        await interaction.response.send_message(
            "🔒 This LindaAI is bound to its owner only.", ephemeral=True
        )
        return
    await interaction.response.defer(thinking=True)
    try:
        reply = await ask_claude(message)
    except Exception as e:
        reply = f"❌ Anthropic API error: {e}"
    await send_chunked(
        interaction,
        reply,
        first_call=interaction.followup.send,
    )


@tree.command(name="howdy", description="Get a Howdy from LindaAI")
async def howdy(interaction: discord.Interaction):
    if not authorized(interaction):
        await interaction.response.send_message(
            "🔒 This LindaAI is bound to its owner only.", ephemeral=True
        )
        return
    await interaction.response.send_message("🤠 Howdy! Use `/linda` to ask me anything.")


# ─── READY / SYNC ──────────────────────────────────────────────────────────
@bot.event
async def on_ready():
    print(f"✓ LindaAI Discord Bridge online as {bot.user}")
    print(f"  Owner Discord ID: {ALLOWED_USER}")
    print(f"  Anthropic model:  {MODEL}")

    # INSTANT sync to the customer's specific guild (no 1-hour wait)
    if GUILD_ID:
        try:
            guild_obj = discord.Object(id=GUILD_ID)
            tree.copy_global_to(guild=guild_obj)
            synced = await tree.sync(guild=guild_obj)
            print(f"  ✓ Synced {len(synced)} commands to guild {GUILD_ID} (instant)")
        except Exception as e:
            print(f"  ⚠ Guild sync failed for {GUILD_ID}: {e}")

    # Also global sync (for DMs and other servers — up to 1hr propagation)
    try:
        synced = await tree.sync()
        print(f"  ✓ Synced {len(synced)} commands globally (may take up to 1hr for DMs)")
    except Exception as e:
        print(f"  ⚠ Global sync failed: {e}")

    if not GUILD_ID:
        print("  ℹ️  TIP: Set DISCORD_GUILD_ID in discord.env for INSTANT slash-command sync on your server.")


# ─── RUN ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    bot.run(TOKEN)
