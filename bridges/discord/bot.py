"""
LindaAI Discord Bridge — Claude Max subscription edition.

Mirrors the Telegram bridge pattern: calls the local `claude` CLI as a
subprocess (Claude Code headless), stripping ANTHROPIC_API_KEY from the
child env so authentication falls through to the user's Claude.ai Max
subscription. NO Anthropic API credits consumed.

Reads from ~/.claude/lindaai/discord.env:
  DISCORD_BOT_TOKEN          (required) — bot token from Discord developer portal
  DISCORD_ALLOWED_USER_ID    (required) — only this Discord user can talk to the bot
  DISCORD_GUILD_ID           (optional) — server ID for INSTANT slash-command sync
  CLAUDE_BIN                 (optional) — path to claude CLI (auto-detected if not set)
  CLAUDE_PROJECT_DIR         (optional) — where claude runs (default: ~/Desktop/LindaAI-OG)
  CLAUDE_MODEL               (optional) — model id (default: claude-opus-4-7)

Design rules (locked in 2026-05-29):
  1. SLASH COMMANDS ONLY — no on_message, no privileged intents
  2. CLAUDE CLI SUBPROCESS — uses Claude Max subscription (no API billing)
  3. INSTANT GUILD SYNC — slash commands appear immediately on the target server
  4. STRIP ANTHROPIC_API_KEY from child env so CLI falls through to Max auth
  5. SESSION RESUME — conversation memory persists across messages

© 2026 LindaAI — Built by Daniel Wise
"""
import asyncio
import json
import os
import shutil
import sys
from pathlib import Path

# ─── DEPS ──────────────────────────────────────────────────────────────────
try:
    import discord
    from discord import app_commands
except ImportError:
    print("ERROR: discord.py not installed. Run:  pip3 install --user discord.py", flush=True)
    sys.exit(1)


# ─── ENV LOAD ──────────────────────────────────────────────────────────────
ENV_FILE = Path.home() / ".claude" / "lindaai" / "discord.env"
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        key = k.strip()
        val = v.strip().strip('"').strip("'")
        # File wins over empty/missing shell env. Customers often have
        # ANTHROPIC_API_KEY="" set from prior installs and setdefault would
        # silently skip the file value.
        if not os.environ.get(key, "").strip():
            os.environ[key] = val
        else:
            os.environ.setdefault(key, val)

TOKEN          = os.environ.get("DISCORD_BOT_TOKEN", "").strip()
ALLOWED_USER   = os.environ.get("DISCORD_ALLOWED_USER_ID", "").strip()
GUILD_ID_RAW   = os.environ.get("DISCORD_GUILD_ID", "").strip()
MODEL          = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5").strip()
PROJECT_DIR    = os.environ.get("CLAUDE_PROJECT_DIR", str(Path.home() / "Desktop" / "LindaAI-OG"))

# Auto-detect claude CLI
CLAUDE_BIN = os.environ.get("CLAUDE_BIN", "").strip()
if not CLAUDE_BIN:
    for candidate in [
        Path.home() / ".npm-global" / "bin" / "claude",
        Path("/usr/local/bin/claude"),
        Path("/opt/homebrew/bin/claude"),
    ]:
        if candidate.exists():
            CLAUDE_BIN = str(candidate)
            break
    if not CLAUDE_BIN:
        which = shutil.which("claude")
        if which:
            CLAUDE_BIN = which

GUILD_ID = None
if GUILD_ID_RAW.isdigit():
    GUILD_ID = int(GUILD_ID_RAW)

# ─── VALIDATE ──────────────────────────────────────────────────────────────
if not TOKEN:
    print("ERROR: DISCORD_BOT_TOKEN not set in ~/.claude/lindaai/discord.env", flush=True)
    sys.exit(1)

if not ALLOWED_USER or not ALLOWED_USER.isdigit():
    print("ERROR: DISCORD_ALLOWED_USER_ID not set or not a valid Discord user ID.", flush=True)
    sys.exit(1)

if not CLAUDE_BIN or not Path(CLAUDE_BIN).exists():
    print(f"ERROR: claude CLI not found. Tried CLAUDE_BIN={CLAUDE_BIN!r}", flush=True)
    print("  Install Claude Code: npm install -g @anthropic-ai/claude-code", flush=True)
    sys.exit(1)

ALLOWED_USER_ID = int(ALLOWED_USER)


# ─── SESSION MEMORY ────────────────────────────────────────────────────────
# Conversation continuity — keeps memory across /linda messages.
session_id: str | None = None


# ─── CLAUDE CLI CALL ───────────────────────────────────────────────────────
async def run_claude(prompt: str) -> str:
    """Invoke claude CLI in headless mode. Uses Max subscription (NOT API)."""
    global session_id

    cmd = [
        CLAUDE_BIN,
        "-p", prompt,
        "--output-format", "json",
        "--model", MODEL,
        "--setting-sources", "user,project,local",
        "--dangerously-skip-permissions",
    ]
    if session_id:
        cmd += ["--resume", session_id]

    # CRITICAL: strip ANTHROPIC_API_KEY so claude CLI uses Max subscription auth.
    child_env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        cwd=PROJECT_DIR,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=child_env,
    )
    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        err = stderr.decode("utf-8", errors="replace")[:1500]
        out = stdout.decode("utf-8", errors="replace")[:1500]
        print(f"[bot.py] claude exit {proc.returncode} | stderr={err!r} | stdout={out!r}", flush=True)
        raise RuntimeError(f"claude exit {proc.returncode}: {err or out or '(no output)'}")

    raw = stdout.decode("utf-8", errors="replace").strip()
    try:
        data = json.loads(raw)
        # Persist session_id for follow-up resume
        sid = data.get("session_id")
        if sid:
            session_id = sid
        # Extract the assistant text
        return data.get("result") or data.get("text") or raw[:4000] or "(empty)"
    except json.JSONDecodeError:
        return raw[:4000] or "(empty response)"


# ─── DISCORD CHUNKING ──────────────────────────────────────────────────────
async def send_chunked(interaction: discord.Interaction, text: str):
    """Discord caps messages at 2000 chars. Chunk and send via followup."""
    CHUNK = 1900
    chunks = [text[i:i + CHUNK] for i in range(0, len(text), CHUNK)] or ["(empty reply)"]
    first = True
    for c in chunks:
        if first:
            await interaction.followup.send(c)
            first = False
        else:
            await interaction.followup.send(c)


# ─── DISCORD CLIENT ────────────────────────────────────────────────────────
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)


def authorized(interaction: discord.Interaction) -> bool:
    return interaction.user.id == ALLOWED_USER_ID


# ─── SLASH COMMANDS ────────────────────────────────────────────────────────
@tree.command(name="linda", description="Ask LindaAI anything")
@app_commands.describe(message="What do you want to ask LindaAI?")
async def linda(interaction: discord.Interaction, message: str):
    if not authorized(interaction):
        await interaction.response.send_message(
            "🔒 This LindaAI is bound to its owner only.", ephemeral=True
        )
        return
    await interaction.response.defer(thinking=True)
    try:
        reply = await run_claude(message)
    except Exception as e:
        await interaction.followup.send(f"⚠️ LindaAI hit a snag: {e}")
        return
    await send_chunked(interaction, reply)


@tree.command(name="howdy", description="Quick LindaAI greeting test")
async def howdy(interaction: discord.Interaction):
    if not authorized(interaction):
        await interaction.response.send_message(
            "🔒 This LindaAI is bound to its owner only.", ephemeral=True
        )
        return
    await interaction.response.defer(thinking=True)
    try:
        reply = await run_claude("Howdy! Quick greeting check from Discord — say hi and confirm you're online.")
    except Exception as e:
        await interaction.followup.send(f"⚠️ LindaAI hit a snag: {e}")
        return
    await send_chunked(interaction, reply)


# ─── READY / SYNC ──────────────────────────────────────────────────────────
@bot.event
async def on_ready():
    print(f"✓ LindaAI Discord Bridge online as {bot.user}", flush=True)
    print(f"  Owner Discord ID: {ALLOWED_USER}", flush=True)
    print(f"  Claude bin:       {CLAUDE_BIN}", flush=True)
    print(f"  Project dir:      {PROJECT_DIR}", flush=True)
    print(f"  Model:            {MODEL}", flush=True)
    print(f"  Auth:             Claude Max subscription (ANTHROPIC_API_KEY stripped)", flush=True)

    if GUILD_ID:
        try:
            guild_obj = discord.Object(id=GUILD_ID)
            tree.copy_global_to(guild=guild_obj)
            synced = await tree.sync(guild=guild_obj)
            print(f"  ✓ Synced {len(synced)} commands to guild {GUILD_ID} (instant)", flush=True)
        except Exception as e:
            print(f"  ⚠ Guild sync failed for {GUILD_ID}: {e}", flush=True)

    try:
        synced = await tree.sync()
        print(f"  ✓ Synced {len(synced)} commands globally (may take up to 1hr for DMs)", flush=True)
    except Exception as e:
        print(f"  ⚠ Global sync failed: {e}", flush=True)

    if not GUILD_ID:
        print("  ℹ️  TIP: Set DISCORD_GUILD_ID in discord.env for INSTANT slash-command sync.", flush=True)


# ─── RUN ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    bot.run(TOKEN)
