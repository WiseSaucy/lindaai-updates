#!/bin/bash
# ============================================================
#  LindaAI - One-Click Mac Setup & Launcher
#  Built by Daniel Wise
#
#  The customer just DOUBLE-CLICKS this file. It:
#    1. Installs Homebrew if missing
#    2. Installs Node.js + Git via Homebrew (if missing)
#    3. Installs Claude Code via the official installer (if missing)
#    4. Launches LindaAI right in this folder
# ============================================================

set -e

# Color output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Move to this script's folder (the LindaAI folder)
cd "$(dirname "$0")"

echo
echo -e "${CYAN}  ============================================${NC}"
echo -e "${CYAN}     Howdy! Saddling up LindaAI for you...${NC}"
echo -e "${CYAN}  ============================================${NC}"
echo

# ---------- 1. Check / install Homebrew ----------
if ! command -v brew &> /dev/null; then
  echo -e "${YELLOW}  [*] Installing Homebrew (one-time)...${NC}"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  # Add brew to PATH for this session
  if [[ -f /opt/homebrew/bin/brew ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
  elif [[ -f /usr/local/bin/brew ]]; then
    eval "$(/usr/local/bin/brew shellenv)"
  fi
else
  echo -e "${GREEN}  [ok] Homebrew already installed.${NC}"
fi

# ---------- 2. Node.js ----------
if ! command -v node &> /dev/null; then
  echo -e "${YELLOW}  [*] Installing Node.js (one-time)...${NC}"
  brew install node
else
  echo -e "${GREEN}  [ok] Node.js already installed.${NC}"
fi

# ---------- 3. Git ----------
if ! command -v git &> /dev/null; then
  echo -e "${YELLOW}  [*] Installing Git (one-time)...${NC}"
  brew install git
else
  echo -e "${GREEN}  [ok] Git already installed.${NC}"
fi

# ---------- 4. Claude Code ----------
if ! command -v claude &> /dev/null; then
  echo -e "${YELLOW}  [*] Installing Claude Code (one-time)...${NC}"
  curl -fsSL https://claude.ai/install.sh | bash
  # Add claude to PATH for this session
  export PATH="$HOME/.local/bin:$PATH"
else
  echo -e "${GREEN}  [ok] Claude Code already installed.${NC}"
fi

echo
echo -e "${GREEN}  ============================================${NC}"
echo -e "${GREEN}     All set! Launching LindaAI now...${NC}"
echo -e "${GREEN}  ============================================${NC}"
echo
echo "  When Claude Code opens, type:  Howdy Linda"
echo "  (First time only: type /login and sign in to Claude.ai)"
echo

# ---------- 5. Launch Claude Code in this folder ----------
claude
