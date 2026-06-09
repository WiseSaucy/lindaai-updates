#!/usr/bin/env python3
"""
Linda-LOI — Daemon Installer (LindaAI v1.4)
Installs a launchd agent that runs run_followups.py daily at 9:00 AM.
Idempotent — safe to run multiple times.

Run once in Terminal:
    python3 ~/.claude/skills/linda-loi/scripts/install_daemon.py
"""

import subprocess
import sys
from pathlib import Path


LABEL = "com.lindaai.linda-loi"
PLIST_PATH = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
RUNNER = Path.home() / ".claude" / "skills" / "linda-loi" / "scripts" / "run_followups.py"
LOG_OUT = Path.cwd() / "brain" / "loi" / "daemon.out.log"
LOG_ERR = Path.cwd() / "brain" / "loi" / "daemon.err.log"


def main():
    PLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_OUT.parent.mkdir(parents=True, exist_ok=True)

    plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{RUNNER}</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{Path.cwd()}</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>{LOG_OUT}</string>
    <key>StandardErrorPath</key>
    <string>{LOG_ERR}</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
"""
    PLIST_PATH.write_text(plist)
    subprocess.run(["launchctl", "unload", str(PLIST_PATH)], capture_output=True)
    result = subprocess.run(["launchctl", "load", str(PLIST_PATH)], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[WARN] launchctl load returned {result.returncode}: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"[OK] Linda-LOI daemon installed at {PLIST_PATH}")
    print(f"     Runs daily at 9:00 AM. Logs: {LOG_OUT}")


if __name__ == '__main__':
    main()
