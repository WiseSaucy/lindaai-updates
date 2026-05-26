#!/usr/bin/env python3
"""
LindaAI Telegram Bridge — customer-ready, zero-friction.

Reads from ~/.claude/lindaai/telegram.env:
  TELEGRAM_BOT_TOKEN          (required) — bot token from @BotFather
  ANTHROPIC_API_KEY           (required) — customer's API key from console.anthropic.com
  TELEGRAM_ALLOWED_USER_ID    (required) — only this Telegram user can talk to the bot
  ANTHROPIC_MODEL             (optional) — defaults to claude-sonnet-4-5

LESSONS BAKED IN (from the Isaac Discord incident 2026-05-25):
  - ANTHROPIC API DIRECT — no local `claude` CLI dependency. The Cowork desktop
    app stores claude binary in places the bot can't find; even when found, it's
    not callable as a CLI. We call the Anthropic API directly.
  - No hardcoded paths — content inbox lives in ~/.claude/lindaai/content-inbox.md
    (works on every customer's machine).

© 2026 LindaAI — Built by Daniel Wise
"""
import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# ─── DEPS ──────────────────────────────────────────────────────────────────
try:
    from telegram import Update
    from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
except ImportError:
    print("ERROR: python-telegram-bot not installed. Run:  pip3 install python-telegram-bot")
    sys.exit(1)

try:
    from anthropic import Anthropic
except ImportError:
    print("ERROR: anthropic SDK not installed. Run:  pip3 install anthropic")
    sys.exit(1)


# ─── ENV LOAD ──────────────────────────────────────────────────────────────
ENV_FILE = Path.home() / ".claude" / "lindaai" / "telegram.env"
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

TOKEN          = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
ANTHROPIC_KEY  = os.environ.get("ANTHROPIC_API_KEY", "").strip()
ALLOWED_USER   = os.environ.get("TELEGRAM_ALLOWED_USER_ID", "").strip()
MODEL          = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929").strip()


# ─── PRE-FLIGHT ────────────────────────────────────────────────────────────
def die(msg: str) -> None:
    print(f"ERROR: {msg}")
    sys.exit(1)

if not TOKEN:
    die("TELEGRAM_BOT_TOKEN not set. Run /telegram-setup to configure.")
if not ANTHROPIC_KEY:
    die("ANTHROPIC_API_KEY not set. Get one at console.anthropic.com, then add to ~/.claude/lindaai/telegram.env")
if not ALLOWED_USER:
    die("TELEGRAM_ALLOWED_USER_ID not set. Run /telegram-setup or DM the bot, then run /whoami.")


# ─── PATHS ─────────────────────────────────────────────────────────────────
LINDA_DIR     = Path.home() / ".claude" / "lindaai"
LINDA_DIR.mkdir(parents=True, exist_ok=True)
CONTENT_INBOX = LINDA_DIR / "content-inbox.md"


# ─── PERSONALITY ───────────────────────────────────────────────────────────
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
    "You are warm, direct, action-oriented, country in tone. "
    "Greet your partner with 'Howdy!' when the conversation starts. "
    "Keep replies tight — 2-5 sentences unless they ask for depth."
)
SYSTEM_PROMPT = CLAUDE_MD or DEFAULT_SYSTEM


# ─── CLIENTS ───────────────────────────────────────────────────────────────
anthropic = Anthropic(api_key=ANTHROPIC_KEY)


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


def append_to_content_inbox(text: str) -> int:
    """Append a content idea to ~/.claude/lindaai/content-inbox.md. Returns total count."""
    if not CONTENT_INBOX.exists():
        CONTENT_INBOX.write_text(
            "# Content Inbox\n\n"
            "Drop ideas here from anywhere. Captured via Telegram `/content` or `c:` prefix.\n\n"
            "---\n\n"
        )
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    with CONTENT_INBOX.open("a") as f:
        f.write(f"- **{ts}** — {text}\n")
    return sum(1 for line in CONTENT_INBOX.read_text().splitlines() if line.startswith("- **"))


# ─── HANDLERS ──────────────────────────────────────────────────────────────
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id != ALLOWED_USER:
        await update.message.reply_text("🔒 This LindaAI is bound to its owner only.")
        print(f"[SECURITY] Rejected message from Telegram user {user_id}")
        return

    user_msg = update.message.text
    if not user_msg:
        return

    # Content channel — "c: idea" → straight to inbox
    stripped = user_msg.strip()
    lower = stripped.lower()
    for prefix in ("c:", "content:", "📝"):
        if lower.startswith(prefix):
            idea = stripped[len(prefix):].strip()
            if not idea:
                await update.message.reply_text("📝 Add the idea after the prefix, partner.\nExample: `c: reel idea — Linda writes my taxes`")
                return
            total = append_to_content_inbox(idea)
            await update.message.reply_text(f"📝 Captured. Content inbox now has {total} idea{'s' if total != 1 else ''}. 🤠")
            return

    await update.message.chat.send_action(action="typing")
    try:
        response = await ask_claude(user_msg)
    except Exception as e:
        response = f"❌ Anthropic API error: {e}"

    # Telegram caps at 4096 chars
    CHUNK = 4000
    for i in range(0, len(response), CHUNK):
        await update.message.reply_text(response[i:i + CHUNK])


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id != ALLOWED_USER:
        await update.message.reply_text("🔒 This LindaAI is bound to its owner. You are not authorized.")
        return
    await update.message.reply_text(
        "🤠 Howdy, partner! LindaAI is online via Telegram.\n\n"
        "Just send me any message and I'll answer.\n"
        "Ask me to draft an email, analyze a deal, run any skill — anything.\n\n"
        "📝 *Content channel:*\n"
        "• `c: your idea` → captures to content inbox\n"
        "• `/content your idea` → same thing\n"
        "• `/ideas` → read back last 20\n\n"
        "LindaAI has your back.",
        parse_mode="Markdown",
    )


async def cmd_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id != ALLOWED_USER:
        await update.message.reply_text("🔒 Owner-only command.")
        return
    idea = " ".join(context.args).strip() if context.args else ""
    if not idea:
        await update.message.reply_text(
            "📝 *Content Inbox*\n\nUsage:\n• `/content your idea here`\n• Or just send `c: your idea here`",
            parse_mode="Markdown",
        )
        return
    total = append_to_content_inbox(idea)
    await update.message.reply_text(f"📝 Captured. Inbox now has {total} idea{'s' if total != 1 else ''}. 🤠")


async def cmd_ideas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id != ALLOWED_USER:
        await update.message.reply_text("🔒 Owner-only command.")
        return
    if not CONTENT_INBOX.exists():
        await update.message.reply_text("📝 Content inbox is empty. Send `c: your first idea` to start.")
        return
    entries = [line for line in CONTENT_INBOX.read_text().splitlines() if line.startswith("- **")]
    if not entries:
        await update.message.reply_text("📝 Content inbox is empty.")
        return
    last_20 = entries[-20:]
    msg = f"📝 *Last {len(last_20)} content ideas* (of {len(entries)} total)\n\n" + "\n".join(last_20)
    CHUNK = 4000
    for i in range(0, len(msg), CHUNK):
        await update.message.reply_text(msg[i:i + CHUNK], parse_mode="Markdown")


async def cmd_whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Your Telegram user ID: `{update.effective_user.id}`\n"
        f"Put this in TELEGRAM_ALLOWED_USER_ID inside ~/.claude/lindaai/telegram.env to lock the bot to you.",
        parse_mode="Markdown",
    )


def main():
    print(f"✓ LindaAI Telegram Bridge starting...")
    print(f"  Owner Telegram ID: {ALLOWED_USER}")
    print(f"  Anthropic model:   {MODEL}")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("whoami", cmd_whoami))
    app.add_handler(CommandHandler("content", cmd_content))
    app.add_handler(CommandHandler("ideas", cmd_ideas))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✓ Bot online. Waiting for messages on Telegram...")
    app.run_polling()


if __name__ == "__main__":
    main()
