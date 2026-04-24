#!/usr/bin/env python3
"""
LindaAI Telegram Bridge — generic customer-ready bot.

Reads TELEGRAM_BOT_TOKEN + TELEGRAM_ALLOWED_USER_ID from ~/.claude/lindaai/telegram.env
Forwards owner messages to the local `claude` CLI and returns responses.

© 2026 LindaAI — Built by Daniel Wise
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from telegram import Update
    from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
except ImportError:
    print("ERROR: python-telegram-bot not installed.")
    print("  Run: pip3 install python-telegram-bot")
    sys.exit(1)


# Load env
ENV_FILE = Path.home() / ".claude" / "lindaai" / "telegram.env"
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
ALLOWED_USER_ID = os.environ.get("TELEGRAM_ALLOWED_USER_ID", "")

if not TOKEN:
    print("ERROR: TELEGRAM_BOT_TOKEN not set in ~/.claude/lindaai/telegram.env")
    print("       Run /telegram-setup to configure.")
    sys.exit(1)

# Find claude CLI — handle launchd/cron PATH weirdness
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


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    # Security: owner-only unless ALLOWED_USER_ID is empty (unbound)
    if ALLOWED_USER_ID and user_id != ALLOWED_USER_ID:
        await update.message.reply_text(
            "🔒 This LindaAI is bound to its owner only. Your ID has been logged."
        )
        print(f"[SECURITY] Rejected message from Telegram user {user_id}")
        return

    user_msg = update.message.text
    if not user_msg:
        return

    await update.message.chat.send_action(action="typing")

    if not CLAUDE_BIN:
        await update.message.reply_text(
            "❌ Claude CLI not found. Install Claude Code on your machine first."
        )
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
        response = "⏳ That took too long. LindaAI timed out — try a shorter question."
    except Exception as e:
        response = f"❌ Error: {e}"

    # Telegram caps at 4096 chars per message
    CHUNK = 4000
    for i in range(0, len(response), CHUNK):
        await update.message.reply_text(response[i:i + CHUNK])


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if ALLOWED_USER_ID and user_id != ALLOWED_USER_ID:
        await update.message.reply_text(
            "🔒 This LindaAI is bound to its owner. You are not authorized."
        )
        return
    await update.message.reply_text(
        "🤠 Howdy, partner! LindaAI is online via Telegram.\n\n"
        "Just send me any message and I'll forward it to your LindaAI.\n"
        "Ask me to run any skill, draft an email, analyze a deal — anything.\n\n"
        "LindaAI has your back."
    )


async def cmd_whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Your Telegram user ID: `{update.effective_user.id}`\n"
        f"Use this in TELEGRAM_ALLOWED_USER_ID to lock the bot to you.",
        parse_mode="Markdown",
    )


def main():
    print(f"✓ LindaAI Telegram Bridge starting...")
    print(f"  Bound to user ID: {ALLOWED_USER_ID or '(open — unbound)'}")
    print(f"  Claude CLI: {CLAUDE_BIN or 'NOT FOUND'}")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("whoami", cmd_whoami))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✓ Bot online. Waiting for messages on Telegram...")
    app.run_polling()


if __name__ == "__main__":
    main()
