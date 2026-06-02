#!/usr/bin/env python3
"""
LindaAI Telegram Bridge — Claude Max subscription edition.

Mirrors the Discord bridge pattern: calls the local `claude` CLI as a
subprocess (Claude Code headless), stripping ANTHROPIC_API_KEY from the
child env so authentication falls through to the user's Claude.ai Max
subscription. NO Anthropic API credits consumed.

Reads from ~/.claude/lindaai/telegram.env:
  TELEGRAM_BOT_TOKEN          (required) — bot token from @BotFather
  TELEGRAM_ALLOWED_USER_ID    (required) — your Telegram user ID
  CLAUDE_CODE_OAUTH_TOKEN     (recommended) — from `claude setup-token`,
                                              uses Max sub (NO API charges)
  ANTHROPIC_API_KEY           (fallback only) — pay-per-message if no Max sub
  CLAUDE_BIN                  (optional) — path to claude CLI (auto-detected)
  CLAUDE_PROJECT_DIR          (optional) — claude cwd (default: ~/Desktop/LindaAI-OG)
  CLAUDE_MODEL                (optional) — defaults to claude-opus-4-7

Design rules (locked 2026-05-29):
  1. CLAUDE CLI SUBPROCESS — uses Claude Max subscription (no API billing)
  2. STRIP ANTHROPIC_API_KEY from child env so CLI falls through to Max auth
  3. CONDITIONAL OVERRIDE env loader — file value wins over empty shell vars
  4. UNBUFFERED PRINTS — flush=True everywhere so launchd logs aren't empty
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
    from telegram import Update
    from telegram.ext import (
        ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
    )
except ImportError:
    print("ERROR: python-telegram-bot not installed. Run:  pip3 install --user python-telegram-bot", flush=True)
    sys.exit(1)


# ─── ENV LOAD ──────────────────────────────────────────────────────────────
ENV_FILE = Path.home() / ".claude" / "lindaai" / "telegram.env"
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        key = k.strip()
        val = v.strip().strip('"').strip("'")
        # FIX: setdefault would skip if shell has key set to "" (empty).
        # File value wins for these credentials.
        if not os.environ.get(key, "").strip():
            os.environ[key] = val
        else:
            os.environ.setdefault(key, val)

TOKEN          = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
ALLOWED_USER   = os.environ.get("TELEGRAM_ALLOWED_USER_ID", "").strip()
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


# ─── VALIDATE ──────────────────────────────────────────────────────────────
if not TOKEN:
    print("ERROR: TELEGRAM_BOT_TOKEN not set in ~/.claude/lindaai/telegram.env", flush=True)
    sys.exit(1)

if not ALLOWED_USER or not ALLOWED_USER.lstrip("-").isdigit():
    print("ERROR: TELEGRAM_ALLOWED_USER_ID not set or not a valid Telegram user ID.", flush=True)
    sys.exit(1)

if not CLAUDE_BIN or not Path(CLAUDE_BIN).exists():
    print(f"ERROR: claude CLI not found. Tried CLAUDE_BIN={CLAUDE_BIN!r}", flush=True)
    print("  Install Claude Code: npm install -g @anthropic-ai/claude-code", flush=True)
    sys.exit(1)

ALLOWED_USER_ID = int(ALLOWED_USER)


# ─── SESSION MEMORY ────────────────────────────────────────────────────────
session_id: str | None = None


# ─── CLAUDE CLI CALL ───────────────────────────────────────────────────────
async def run_claude(prompt: str) -> str:
    """Invoke claude CLI headless. Uses Max subscription (no API charges)."""
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
        sid = data.get("session_id")
        if sid:
            session_id = sid
        return data.get("result") or data.get("text") or raw[:4000] or "(empty)"
    except json.JSONDecodeError:
        return raw[:4000] or "(empty response)"


# ─── TELEGRAM HANDLERS ─────────────────────────────────────────────────────
def authorized(update: Update) -> bool:
    return update.effective_user is not None and update.effective_user.id == ALLOWED_USER_ID


async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not authorized(update):
        await update.message.reply_text("🔒 This LindaAI is bound to its owner only.")
        return
    await update.message.reply_text(
        "🤠 Howdy, Boss! LindaAI's online. Just message me — I'll handle the rest."
    )


async def cmd_whoami(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Your Telegram user ID: `{user.id}`\n"
        f"Name: {user.first_name}\n"
        f"Username: @{user.username or '(none)'}\n\n"
        f"Paste that ID into TELEGRAM_ALLOWED_USER_ID in telegram.env to lock the bot to you.",
        parse_mode="Markdown"
    )


# Chunk replies — Telegram caps messages at 4096 chars
TG_CHUNK = 3900


async def send_chunked(message, text: str):
    chunks = [text[i:i + TG_CHUNK] for i in range(0, len(text), TG_CHUNK)] or ["(empty reply)"]
    for c in chunks:
        await message.reply_text(c)


async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not authorized(update):
        await update.message.reply_text("🔒 This LindaAI is bound to its owner only.")
        return
    msg = update.message.text or ""
    if not msg.strip():
        return
    await ctx.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        reply = await run_claude(msg)
    except Exception as e:
        await update.message.reply_text(f"⚠️ LindaAI hit a snag: {e}")
        return
    await send_chunked(update.message, reply)


# ─── RUN ───────────────────────────────────────────────────────────────────
def main():
    print(f"✓ LindaAI Telegram Bridge starting", flush=True)
    print(f"  Owner Telegram ID: {ALLOWED_USER}", flush=True)
    print(f"  Claude bin:        {CLAUDE_BIN}", flush=True)
    print(f"  Project dir:       {PROJECT_DIR}", flush=True)
    print(f"  Model:             {MODEL}", flush=True)
    print(f"  Auth:              Claude Max subscription (ANTHROPIC_API_KEY stripped)", flush=True)

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("whoami", cmd_whoami))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print(f"  ✓ Bot online. Message your bot on Telegram!", flush=True)
    app.run_polling()


if __name__ == "__main__":
    main()
