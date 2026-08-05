# 🤠 LindaAI Setup — Pick Your Path

Howdy, partner. There are **TWO ways** to run LindaAI. Pick the one that fits you. **95% of users want Path A.**

---

## ⚡ PATH A — claude.ai — RECOMMENDED for everyone

**Works on:** iPhone, iPad, Android, Mac, Windows, any browser, the Claude desktop app.

**Setup time:** 60 seconds.

**What you can do:** Talk to LindaAI in plain English. Use slash command-style prompts. Get briefings, draft emails, analyze deals, write content, plan trips, do hiring — everything LindaAI does, on any device.

**👉 Go to `CLAUDE-AI/START-HERE.md` for step-by-step.**

This is the path Daniel Wise designed LindaAI around. It's the easy way. If you're not sure which path to pick — PICK THIS ONE.

---

## 🔥 PATH B — Claude CODE (CLI) — POWER USERS only

**Works on:** Mac, Windows, Linux desktop ONLY. No mobile.

**Setup time:** 10-15 minutes (first time).

**What you can do:** Everything in Path A, PLUS actual script execution, real file editing, multi-agent automation, MCP servers, custom hooks, full developer workflow.

**Who should pick this?** Developers, engineers, people comfortable with terminals/PowerShell.

If that's you, keep reading. Otherwise — **close this file and go back to Path A** (`CLAUDE-AI/START-HERE.md`).

---

## 🔥 PATH B — Full Claude Code Setup

### ⚠️ Before you start — there are THREE different "Claudes"

This is the #1 confusion when installing Claude Code. ONLY the third one runs the Code path.

| Tool | What it is | Where to find it | This path uses it? |
|---|---|---|---|
| **claude.ai** | Web chat | Browser | ❌ — that's Path A |
| **Claude desktop app** | Web wrapper | Taskbar/dock | ❌ — that's Path A |
| **Claude CODE** | Command-line tool | Terminal / PowerShell | ✅ YES — this path |

**Claude Code is a terminal-based CLI.** It is NOT the desktop app you may have downloaded. Slash commands in this path execute as REAL code.

---

### 🍎 Mac install (3 minutes)

**Step 1 — Install Claude Code**
Open **Terminal** (`Cmd + Space` → type "Terminal" → Enter). Paste this:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

When it finishes, **close Terminal completely** and **open a fresh window**. (PATH only refreshes in a new shell.)

**Step 2 — Log into Claude**
```bash
claude
```
Browser pops open → log into your **Claude.ai Pro or Max** account → paste the token back into Terminal.

> ⚠️ Free Claude.ai accounts won't work — you need Pro or Max.
> ⚠️ DO NOT log in with GitHub — Claude Code uses your **Anthropic** account.

**Step 3 — Open LindaAI**
Type `cd ` (with a space), drag this LindaAI folder onto Terminal, hit Enter. Then:
```bash
claude
```
Once Claude Code opens:
```
Howdy Linda
```
🤠 **You're riding.**

---

### 🪟 Windows install (5-10 minutes)

**Step 1 — Know your CPU**
Press `Windows key + I` → **System** → **About** → "System type"
- "x64-based" → use **x64** (99% of laptops)
- "ARM-based" → use **arm64** (Surface Pro X / Snapdragon)

**Step 2 — Install Claude Code**
Open **Windows PowerShell** (NOT Command Prompt). Paste:

```powershell
irm https://claude.ai/install.ps1 | iex
```

Wait for it to finish. Then **CLOSE PowerShell completely** and **open a brand-new PowerShell window**. (Critical — PATH only refreshes in a new session.)

**Step 3 — Verify the install**
In the fresh PowerShell, paste:

```powershell
Get-ChildItem -Path $env:USERPROFILE -Filter "claude.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object FullName
```

You should see a path like `C:\Users\YOU\.local\bin\claude.exe`. If yes → keep going. If NOT → see **Fallback** below.

**Step 3.5 — Add to PATH (if `claude` says "not recognized")**
The installer sometimes forgets to update PATH. Fix:

```powershell
[Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";$env:USERPROFILE\.local\bin", "User")
```

Close PowerShell, open a fresh one.

**Step 4 — Log into Claude**
```powershell
claude
```
Browser pops open → log into your **Claude.ai Pro or Max** account → paste token back.

> ⚠️ DO NOT log in with GitHub — Claude Code uses your **Anthropic** account.
> ⚠️ If GitHub asks you to "select a repository" → ignore. Close that tab. You don't need a repo.

**Step 5 — Open LindaAI**
Type `cd ` (with a space), drag the LindaAI folder onto PowerShell, hit Enter. Then:
```powershell
claude
```
Once Claude Code starts:
```
Howdy Linda
```
🤠 **You're riding.**

---

### 🚨 Windows fallback (if the install above fails)

Sometimes Defender/IT policy blocks the native installer. Use npm instead:

1. Download Node.js LTS: https://nodejs.org (Windows Installer · 64-bit, or arm64 if applicable)
2. Run the installer (defaults are fine)
3. Open a fresh PowerShell:
```powershell
npm install -g @anthropic-ai/claude-code
```
4. Then:
```powershell
claude
```

---

## 🆘 Common errors

| Error | Fix |
|---|---|
| `'claude' is not recognized` (Windows) | Open a fresh PowerShell window. Still broken? Run the PATH-add line in Step 3.5. |
| `command not found: claude` (Mac) | Close Terminal, open a fresh window. Still broken? Re-run install line. |
| Asked to select GitHub repo | Close that browser tab — you don't need a repo. Sign back in with Google or email instead of GitHub. |
| Asked for license key | Use the one in your welcome email (`LINDA-2026-…`). Paste it in. |
| Browser doesn't open | `claude /logout` then `claude /login`. |
| Commands `/linda-brief` etc don't show up | You're in the wrong "Claude." Make sure you're in PowerShell/Terminal — NOT claude.ai web/desktop. (For claude.ai, use **Path A** — slash commands are just prompts you type as your message.) |
| Anything else | Email **support@send.lindaai-brain.com** with: tier, error screenshot, OS + CPU. |

---

## Once you're in — what to try

In Claude Code, after `Howdy Linda`:
- `/linda-brief` — daily CEO briefing
- `/linda-mail` — draft an email
- `/linda-invoice` — create an invoice
- `/linda-capture` — capture an idea or note
- `/linda-posts` — batch social posts

Or just talk: *"Bandit, find me distressed properties under $200K"*

---

**Let's gooooooo! 🤠**

© 2022-2026 Daniel Wise · LindaAI · Built by Daniel Wise
