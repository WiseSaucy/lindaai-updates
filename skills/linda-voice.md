---
name: linda-voice
description: Toggle LindaAI's voice-speak-every-response hook on or off. Use when Boss47 says "turn voice on", "turn voice off", "mute LindaAI", "unmute LindaAI", "stop talking", "start talking", "/voice on", "/voice off", or just "/voice" to flip the current state.
---

# Voice Toggle

This skill turns the Stop hook in `~/.claude/settings.json` on or off. The hook runs `~/.claude/speak-last-response.sh` which speaks every response through `say -v Samantha` in country voice.

## How to run it

1. Read `~/.claude/settings.json`.
2. Check whether `hooks.Stop` exists with the `speak-last-response.sh` command.
3. Based on the user's request:
   - **"on" / "unmute" / "start talking"** → Add the Stop hook block if missing:
     ```json
     "Stop": [{ "hooks": [{ "type": "command", "command": "/Users/jowise/.claude/speak-last-response.sh", "async": true }] }]
     ```
   - **"off" / "mute" / "stop talking"** → Remove the entire `Stop` entry from `hooks`. If `hooks` becomes empty, remove the `hooks` key entirely.
   - **No argument (just `/voice`)** → Flip the current state.
4. Write the updated JSON back. Preserve all other settings (especially `extraKnownMarketplaces`).
5. Confirm to Boss47 in country voice whether voice is now ON or OFF.
6. Remind him: "Run `/hooks` or restart Claude Code once for the change to take effect mid-session."

## Important

- Never touch `extraKnownMarketplaces` or any other settings key.
- Always validate the resulting JSON (`python3 -c "import json; json.load(open('/Users/jowise/.claude/settings.json'))"`) before finishing.
- Speak the confirmation aloud via `say -v Samantha "..."` country-style.


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
