#!/bin/bash
# LindaAI Bootstrap Installer — macOS / Linux
# Downloads + installs LindaAI tier-appropriate files based on license.
#
# Usage (customer-facing):
#   curl -s https://raw.githubusercontent.com/WiseSaucy/lindaai-updates/main/bootstrap/install.sh | bash -s -- <LICENSE_KEY>
#
# © 2026 LindaAI — Built by Daniel Wise

set -e

LICENSE_KEY="${1:-}"
API="https://lindaai-api-production.up.railway.app"
CDN="https://raw.githubusercontent.com/WiseSaucy/lindaai-updates/main"
CLAUDE_DIR="$HOME/.claude"
SKILLS_DIR="$CLAUDE_DIR/skills"
AGENTS_DIR="$CLAUDE_DIR/agents"
BRAIN_DIR="$CLAUDE_DIR/lindaai-brain"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     LindaAI — License-Gated Bootstrap Installer           ║"
echo "║     © 2026 LindaAI — Built by Daniel Wise                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# --- Require license key ---
if [ -z "$LICENSE_KEY" ]; then
  echo "❌ No license key provided."
  echo ""
  echo "   Usage: bash install.sh <your-license-key>"
  echo "   Lost your key? Check your Gumroad email or contact support@lindaai.com"
  echo ""
  exit 1
fi

echo "🔑 License: ${LICENSE_KEY:0:6}...${LICENSE_KEY: -4}"
echo ""

# --- Machine ID (first MAC address) ---
if [ "$(uname -s)" = "Darwin" ]; then
  MACHINE_ID=$(ifconfig en0 | awk '/ether/{print $2}' | head -1)
else
  MACHINE_ID=$(ip link show | awk '/link\/ether/{print $2; exit}')
fi
MACHINE_ID="${MACHINE_ID:-unknown-machine}"

# --- Validate license against LindaAI API ---
echo "🌐 Validating license against $API ..."
VALIDATE_URL="$API/v1/licenses/validate/$LICENSE_KEY?machine_id=$MACHINE_ID"
VALIDATE_RESP=$(curl -sL "$VALIDATE_URL")

if [ -z "$VALIDATE_RESP" ]; then
  echo "❌ Can't reach LindaAI servers. Check your internet connection."
  exit 1
fi

# Parse valid/tier via python — be defensive against non-JSON responses
VALID=$(echo "$VALIDATE_RESP" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('valid', False))
except Exception:
    print('false')
" 2>/dev/null)
VALID="${VALID:-false}"
if [ "$VALID" != "True" ] && [ "$VALID" != "true" ]; then
  REASON=$(echo "$VALIDATE_RESP" | python3 -c "
import sys, json
try:
    print(json.load(sys.stdin).get('reason', 'unknown reason'))
except Exception:
    print('Server returned an unparseable response. Try again or email support@lindaai.com.')
" 2>/dev/null)
  echo "❌ License rejected: $REASON"
  echo ""
  echo "   Need help? Email support@lindaai.com with your license key and we'll fix it."
  exit 1
fi

# --- Extract tier directly from the validate response (it's right there) ---
echo "📜 Reading your license details..."
TIER=$(echo "$VALIDATE_RESP" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    t = (d.get('tier') or d.get('plan') or 'bronze').lower()
    if t in ('bronze','silver','gold','platinum','trial'):
        print(t)
    else:
        print('bronze')
except Exception:
    print('bronze')
" 2>/dev/null)
TIER="${TIER:-bronze}"

echo "✅ Tier: $TIER"
echo ""

# --- Fetch tier manifest to know which skills/agents for this tier ---
TIER_MANIFEST=$(curl -sL "$CDN/tier-manifest.json")
if [ -z "$TIER_MANIFEST" ]; then
  echo "❌ Couldn't fetch tier manifest from $CDN"
  exit 1
fi

# Build the skill list for this tier (customer names — linda-*)
SKILLS=$(echo "$TIER_MANIFEST" | python3 <<PY
import sys, json
m = json.load(sys.stdin)
rename_url = "$CDN/bootstrap/rename-map.json"
# Fallback: use raw skills list (tier-manifest skills are internal names, but updates server uses customer linda-* names)
tiers = m.get("tiers", {})
tier = "$TIER"

# Collect skills walking up the tier chain
skills = list(tiers.get("bronze", {}).get("skills", []))
if tier in ("silver","gold","platinum"):
    skills += tiers.get("silver", {}).get("additional_skills", [])
if tier in ("gold","platinum"):
    skills += tiers.get("gold", {}).get("additional_skills", [])
if tier == "platinum":
    skills += tiers.get("platinum", {}).get("additional_skills", [])

# Dedupe
seen, out = set(), []
for s in skills:
    if s not in seen:
        seen.add(s)
        out.append(s)
print(" ".join(out))
PY
)

# Agents (Platinum only)
AGENTS=""
if [ "$TIER" = "platinum" ]; then
  AGENTS=$(echo "$TIER_MANIFEST" | python3 -c "
import sys, json
m = json.load(sys.stdin)
print(' '.join(m.get('tiers',{}).get('platinum',{}).get('agents',[])))
" 2>/dev/null)
fi

SKILL_COUNT=$(echo "$SKILLS" | wc -w | tr -d ' ')
AGENT_COUNT=$(echo "$AGENTS" | wc -w | tr -d ' ')
echo "📦 Installing $SKILL_COUNT skills + $AGENT_COUNT agents..."

# --- Create directories ---
mkdir -p "$SKILLS_DIR" "$AGENTS_DIR" "$BRAIN_DIR"

# --- Download each skill ---
INSTALLED_SKILLS=0
for skill in $SKILLS; do
  # Try the "linda-<customer-name>" path first (customer naming in updates server)
  SKILL_URL="$CDN/skills/${skill}.md"
  TMP=$(mktemp)
  if curl -sL -f "$SKILL_URL" -o "$TMP" 2>/dev/null; then
    mkdir -p "$SKILLS_DIR/$skill"
    mv "$TMP" "$SKILLS_DIR/$skill/SKILL.md"
    INSTALLED_SKILLS=$((INSTALLED_SKILLS + 1))
  fi
  rm -f "$TMP" 2>/dev/null
done

# --- Download each agent ---
INSTALLED_AGENTS=0
for agent in $AGENTS; do
  AGENT_URL="$CDN/agents/${agent}.md"
  if curl -sL -f "$AGENT_URL" -o "$AGENTS_DIR/${agent}.md" 2>/dev/null; then
    INSTALLED_AGENTS=$((INSTALLED_AGENTS + 1))
  fi
done

# --- Voice Pack (Platinum only) ---
if [ "$TIER" = "platinum" ]; then
  echo "🎤 Installing bundled Voice Pack..."
  mkdir -p "$SKILLS_DIR/voice" "$SKILLS_DIR/voicesetup"
  curl -sL "$CDN/skills/voice.md" -o "$SKILLS_DIR/voice/SKILL.md" 2>/dev/null || true
  curl -sL "$CDN/skills/voicesetup.md" -o "$SKILLS_DIR/voicesetup/SKILL.md" 2>/dev/null || true
  mkdir -p "$HOME/.claude/lindaai"
  curl -sL "$CDN/scripts/speak-last-response.sh" -o "$HOME/.claude/speak-last-response.sh" 2>/dev/null || true
  [ -f "$HOME/.claude/speak-last-response.sh" ] && chmod +x "$HOME/.claude/speak-last-response.sh"
fi

# --- Brain folder scaffold ---
if [ ! -f "$BRAIN_DIR/README.md" ]; then
  cat > "$BRAIN_DIR/README.md" <<EOF
# Your LindaAI Brain

Drop reference files in this folder — LindaAI reads them as context.

Suggested files:
- goals.md — your current goals
- active-deals.md — deals in progress
- contacts.md — key people
- sop/ — standard operating procedures

© 2026 LindaAI — Built by Daniel Wise
EOF
fi

# --- Save license locally for /linda-sync ---
mkdir -p "$HOME/.claude/lindaai"
cat > "$HOME/.claude/lindaai/license.json" <<EOF
{
  "key": "$LICENSE_KEY",
  "tier": "$TIER",
  "machine_id": "$MACHINE_ID",
  "installed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║               ✅  LINDAAI INSTALLED                        ║"
echo "╠════════════════════════════════════════════════════════════╣"
printf "║  Tier:    %-48s║\n" "$TIER"
printf "║  Skills:  %-48s║\n" "$INSTALLED_SKILLS installed"
printf "║  Agents:  %-48s║\n" "$INSTALLED_AGENTS installed"
echo "║                                                            ║"
echo "║  Next: Restart Claude Code and type any LindaAI command    ║"
echo "║  Update anytime with: /linda-sync                          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Speak if on macOS
if command -v say >/dev/null 2>&1; then
  say -v Samantha "LindaAI $TIER installed. Welcome, partner. LindaAI has your back." &
fi

exit 0
