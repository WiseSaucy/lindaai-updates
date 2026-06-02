#!/usr/bin/env bash
# ============================================================================
# LindaAI Agent-Name SOP Enforcer (Stop hook)
# ----------------------------------------------------------------------------
# LindaAI Standing Rule: every response leads with one of your named agents +
# emoji. Your AI is a TEAM of specialists, not a faceless chatbot — this hook
# enforces it. If a response doesn't lead with an agent, it's blocked and the
# AI re-does it with the right agent named.
#
# Emergency disable: set env LINDA_AGENT_NAME_HOOK=off
# ============================================================================

set -euo pipefail

if [ "${LINDA_AGENT_NAME_HOOK:-on}" = "off" ]; then
  exit 0
fi

input=$(cat)
transcript_path=$(echo "$input" | /usr/bin/python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("transcript_path",""))' 2>/dev/null || echo "")

if [ -z "$transcript_path" ] || [ ! -f "$transcript_path" ]; then
  exit 0
fi

result=$(/usr/bin/python3 - "$transcript_path" <<'PY'
import json, sys, re

# LindaAI customer agent roster (lead with one of these + its emoji).
AGENTS = [
    ("🐓", "Rooster"), ("🤠", "Bandit"), ("✍️", "Inkslinger"), ("🛡️", "Sheriff"),
    ("🩺", "Doc"), ("🖋️", "Drawl"), ("🤝", "Wrangler"), ("📊", "Tally"),
    ("🛒", "Mercantile"), ("💼", "Closer"), ("💪", "Grit"), ("🔍", "Scout"),
    ("🧭", "Compass"), ("📣", "Holler"), ("🪖", "Ranger"), ("🐎", "Pony"),
    ("📢", "Bullhorn"), ("🔥", "Forge"),
]

path = sys.argv[1]
try:
    with open(path) as f:
        lines = f.readlines()
except Exception:
    sys.exit(0)

text = ""
for line in reversed(lines):
    try:
        rec = json.loads(line)
    except Exception:
        continue
    if rec.get("type") != "assistant":
        continue
    content = rec.get("message", {}).get("content", [])
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                t = block.get("text", "").strip()
                if t:
                    text = t
                    break
    elif isinstance(content, str):
        text = content.strip()
    if text:
        break

if not text or len(text) < 30:
    sys.exit(0)

head = text[:400]
preview = text[:60].replace("\n", " ").replace("|", "/")
found = any(
    emoji in head and re.search(rf"{re.escape(emoji)}.{{0,6}}{name}", head)
    for emoji, name in AGENTS
)
print(("FOUND|" if found else "NOTFOUND|") + preview)
PY
)

if [ -z "$result" ]; then
  exit 0
fi

status="${result%%|*}"
preview="${result#*|}"

LOG=~/.claude/hooks/agent-name.log
ts=$(date +"%Y-%m-%d %H:%M:%S")

if [ "$status" = "FOUND" ]; then
  echo "$ts  ✓ PASS  $preview" >> "$LOG" 2>/dev/null || true
  exit 0
fi

echo "$ts  ✗ VIOLATION  $preview" >> "$LOG" 2>/dev/null || true

cat <<'EOF'
{
  "decision": "block",
  "reason": "🛡️ AGENT-NAME RULE: Every LindaAI response must lead with one of your named agents + emoji — you're a TEAM of specialists, not a faceless chatbot. Lead with the right one: 🐓 Rooster (Daily Motivator), 🤠 Bandit (Deal Hunter), ✍️ Inkslinger (Content), 🛡️ Sheriff (Inbox), 🩺 Doc (Support), 🖋️ Drawl (Copywriter), 🤝 Wrangler (Biz Dev), 📊 Tally (Data), 🛒 Mercantile (Ecommerce), 💼 Closer (Sales), 💪 Grit (Mindset), 🔍 Scout (Recruiter), 🧭 Compass (SEO), 📣 Holler (Social), 🪖 Ranger (Virtual Assistant), 🐎 Pony (Email), 📢 Bullhorn (Ads), or 🔥 Forge (Engineer/Automation). If no specific agent fits, default to 🪖 Ranger. Redo the response with the agent named."
}
EOF
exit 0
