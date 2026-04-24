#!/bin/bash
# Stop the LindaAI Telegram Bridge
PID_FILE="$HOME/.claude/lindaai/telegram-bridge.pid"
if [ -f "$PID_FILE" ]; then
  PID=$(cat "$PID_FILE")
  if kill -0 "$PID" 2>/dev/null; then
    kill "$PID"
    echo "✓ Stopped Telegram bridge (was PID $PID)"
  else
    echo "Bot was already stopped."
  fi
  rm -f "$PID_FILE"
else
  echo "No bot PID file found — bot not running."
fi
