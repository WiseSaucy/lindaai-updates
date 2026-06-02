#!/bin/bash
# LindaAI Telegram Bridge runner
# Starts the bot in the background, tracks PID, redirects logs.

set -e

BRIDGE_DIR="$HOME/.claude/lindaai/telegram-bridge"
LOG="$HOME/.claude/lindaai/telegram-bridge.log"
PID_FILE="$HOME/.claude/lindaai/telegram-bridge.pid"

mkdir -p "$(dirname "$LOG")"

# Stop if already running
if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "Telegram bridge already running (PID $(cat "$PID_FILE")). Stopping first..."
  kill "$(cat "$PID_FILE")"
  sleep 2
fi

# Install dependencies if needed
if ! python3 -c "import telegram" 2>/dev/null; then
  echo "Installing python-telegram-bot..."
  pip3 install -q python-telegram-bot || pip3 install --user -q python-telegram-bot
fi

# anthropic SDK is no longer required — bot uses claude CLI subprocess via Max sub.
# (Kept fallback install for backwards compat with the API-key path.)
# if ! python3 -c "import anthropic" 2>/dev/null; then
#   pip3 install --user -q anthropic
# fi

# Start bot (unbuffered so startup logs flush immediately)
cd "$BRIDGE_DIR" || { echo "ERROR: $BRIDGE_DIR not found. Run /telegram-setup first."; exit 1; }
nohup python3 -u bot.py > "$LOG" 2>&1 &
echo $! > "$PID_FILE"
sleep 2

if kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "✓ LindaAI Telegram Bridge running (PID $(cat "$PID_FILE"))"
  echo "  Log: $LOG"
else
  echo "✗ Bot failed to start. Check $LOG"
  tail -20 "$LOG"
  exit 1
fi
