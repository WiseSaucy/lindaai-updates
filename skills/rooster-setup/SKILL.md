---
name: rooster-setup
description: Set up Rooster — LindaAI's daily motivator — to fire automatically every morning on macOS, Windows, or Linux. Use when the user says "/rooster-setup", "set up Rooster", "schedule daily motivation", "turn on Rooster", "enable daily motivation", "daily holler on", "rooster schedule".
---

# /rooster-setup — Schedule Daily Rooster (Cross-Platform)

Auto-detects the user's OS and schedules Rooster via the right mechanism.

## Steps

1. Ask the user: "What time should Rooster crow each day? (e.g. 7:00, 6:30, 8:00)"
2. Parse hour + minute (default 7:00 if unclear)
3. Detect OS — check `sys.platform` / `uname` / `$OS` env var
4. Install + schedule per OS:

### macOS (launchd)

Write `~/Library/LaunchAgents/com.lindaai.rooster.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>com.lindaai.rooster</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>REPLACE_WITH_HOME/.claude/lindaai/rooster-daily.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict><key>Hour</key><integer>HOUR</integer><key>Minute</key><integer>MINUTE</integer></dict>
</dict>
</plist>
```

Then: `launchctl unload <plist> 2>/dev/null; launchctl load <plist>`

### Windows (Task Scheduler)

Run PowerShell:
```powershell
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
  -Argument "-NoProfile -ExecutionPolicy Bypass -File $env:USERPROFILE\.claude\lindaai\rooster-daily.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At "HH:MM"
Register-ScheduledTask -TaskName "LindaAI Rooster" -Action $action -Trigger $trigger -Force
```

### Linux (cron)

Add to crontab:
```
MINUTE HOUR * * * /bin/bash $HOME/.claude/lindaai/rooster-daily.sh
```

Use `crontab -l | grep -v rooster; echo "MINUTE HOUR * * * ..."` pattern piped back to `crontab -`.

5. Ensure the daily script is installed:
   - macOS/Linux: `~/.claude/lindaai/rooster-daily.sh` (copy from installer)
   - Windows: `%USERPROFILE%\.claude\lindaai\rooster-daily.ps1`
6. Confirm: "Rooster's scheduled — he'll crow every day at HH:MM. Want to hear his first holler right now? Type `/rooster`."

## To disable later
- **macOS:** `launchctl unload ~/Library/LaunchAgents/com.lindaai.rooster.plist`
- **Windows:** `Unregister-ScheduledTask -TaskName "LindaAI Rooster" -Confirm:$false`
- **Linux:** `crontab -l | grep -v rooster | crontab -`

---

© 2026 LindaAI — Built by Daniel Wise
