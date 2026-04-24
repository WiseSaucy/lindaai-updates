#!/bin/bash
# LindaAI Discord Bridge runner
set -e

BRIDGE_DIR="$HOME/.claude/lindaai/discord-bridge"
LOG="$HOME/.claude/lindaai/discord-bridge.log"
PID_FILE="$HOME/.claude/lindaai/discord-bridge.pid"

mkdir -p "$(dirname "$LOG")"

if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "Discord bridge already running (PID $(cat "$PID_FILE")). Stopping first..."
  kill "$(cat "$PID_FILE")"
  sleep 2
fi

if ! python3 -c "import discord" 2>/dev/null; then
  echo "Installing discord.py..."
  pip3 install -q discord.py || pip3 install --user -q discord.py
fi

cd "$BRIDGE_DIR" || { echo "ERROR: $BRIDGE_DIR not found. Run /discord-setup first."; exit 1; }
nohup python3 bot.py > "$LOG" 2>&1 &
echo $! > "$PID_FILE"
sleep 2

if kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "✓ LindaAI Discord Bridge running (PID $(cat "$PID_FILE"))"
  echo "  Log: $LOG"
else
  echo "✗ Bot failed to start. Check $LOG"
  tail -20 "$LOG"
  exit 1
fi
