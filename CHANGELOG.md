# 🤠 LindaAI Release Notes

> What just landed in your barn, partner. Newest at the top.
> Built by Daniel Wise · LindaAI · `lindaai-brain.com`

---

## 2026-08-08 — 🪟 Autopilot for Windows — the whole barn rides now (Gold + Platinum)

**Autopilot v1.2.0** — Windows joins the ride:
- Morning Brief, Weekly Review (and Inbox Triage on Platinum) now schedule natively on **Windows Task Scheduler** — same draft-only rules, same approval queue, same Discord DMs
- Mac + Windows installs get the update automatically with `/linda-sync` — then say "turn on autopilot"

---

## 2026-08-08 — 📬 Approval Queue — approve Linda's drafts from your phone (Gold + Platinum)

**NEW `/linda-approvals`** + Autopilot v1.1.0 — the loop is closed:
- Autopilot now files every draft it writes in `brain/autopilot/queue/` awaiting YOUR go — nothing sends itself, ever
- Discord bridge connected? Linda **DMs you the moment drafts are waiting** — reply "show my approvals", then "approve 2", coffee in hand
- Approve → she sends it exactly as drafted · Reject → she tears it up (or redrafts it your way)
- Works in the terminal too — Discord is optional

Run `/linda-sync` to grab both, then say "turn on autopilot."

---

## 2026-08-08 — 🤖 LindaAI Autopilot — she works while you sleep (Gold + Platinum)

**NEW `/linda-autopilot`** — Linda now runs your routines on a schedule, no asking needed:
- ☀️ **Morning Brief** waiting before you wake (daily) · 📊 **Weekly Review** every Friday — Gold + Platinum
- 📬 **Automatic Inbox Triage** with reply drafts — Platinum
- **Draft-only by design:** Linda never sends, posts, or spends on her own — anything outbound waits for YOUR go
- Results land in `brain/autopilot/` with a Mac notification (macOS now, Windows next update)

Run `/linda-sync` to grab it, then say "turn on autopilot."

---

## 2026-07-13 — 🏠 Sauce Underwriter baked into Discord + Discord-only bridges

**Your Discord just got a deal desk:**

- 🤠 **The Sauce Underwriter now ships INSIDE the Discord bridge.** New installs get a
  **#deals** channel with `/underwrite` (wholesale MAO **+** fix-and-flip P&L, all-in % of
  ARV, and the 70%-rule check) working the moment the bot comes online — the locked
  formula is built into the bot itself, no skill download needed. `/flip` and `/comps`
  ride along, plus paste-a-bare-address auto-underwriting (opt-in).
- 🗂️ **Per-channel isolation.** The bridge is now channel-aware: #deals talks deals,
  #linda-ai is your assistant (`/brief /mail /followup /research`), and neither crosses
  into the other. Add channels for your own businesses by editing one file
  (`channels.json`) — no code.
- 🏗️ **`setup_channels.py`** — one command builds the Deals + Linda AI channels in your
  server, deal-structure tags included (Cash / Fix & Flip / Seller Finance / BRRRR /
  Subject-To / Wholesale).
- 🛡️ Sturdier bot: per-thread conversation memory with auto-expiry, `/reset`, hard
  timeouts, multi-owner support, per-channel access control, Google Drive link handling,
  and Discord file uploads passed through to Claude.
- 📵 **Telegram bridge retired.** Discord is the one mobile bridge going forward — it's
  better in every way (channels, forums, threads, tags). Existing Telegram setups keep
  working; they're just no longer shipped or synced.

Paste an address. Get the numbers. Yeeee Hawww 🤠

---

## 2026-07-06 — 🧹 Catalog cleanup

**Leaner and meaner:**

- 🎯 **`/linda-trigger`** now in the sync catalog — the Sauce Underwriter pulls down clean on every Gold+ sync
- 🧹 **8 redundant skills retired** (invest, actions, finance, swot, compete, network, outreach, kajabi) — their jobs are covered better by the tools that stayed. Your next `/linda-sync` tidies them out of your install automatically. Less clutter, clearer lineup.

**The underwriting lineup now:** `/linda-trigger` (flips + wholesale) · `/linda-deals` (multifamily + creative finance) · `/linda-airbnb` (short-term rentals) · `/linda-coliving` (rent-by-room) · `/linda-rents` (comps).

Yeeee Hawww 🤠

---

## 2026-07-06 — Pack Barn Fully Stocked 🤠

Howdy partners — big restock landed in your barn today:

**New in your barn:**
- 🏗️ **Construction PM Pack** now included in every new install (10 skills — change orders, RFIs, submittals, punch lists, daily reports)
- 🔧 **HVAC & Plumbing Pack** now included (9 skills — dispatch, tech routing, parts, estimates, maintenance plans)
- 🌱 **Landscaper Pack** now included (8 skills — crew dispatch, routes, seasonal planning, yard leads)
- 🧭 **Life Coach Pack** now included (8 skills — client files, sessions, accountability, discovery leads)
- 🍽️ **Restaurant Pack** now included (12 skills — menus, shifts, inventory, reviews)

Every pack now carries a version number. Pack updates now ride the secure license-gated channel — type /linda-sync and your packs refresh automatically. Ride easy — Yeeee Hawww 🤠

## 2026-07-06 — 🛡️ Full 157-skill content audit (multi-agent sweep)

**What happened:** the whole crew — 15 reader agents + adversarial verifiers — read every single skill file end to end. Result: cleaner copy across the board.

- 🧹 86+ skill files scrubbed of founder-specific branding — your PDFs and posts now carry YOUR handle, not ours
- 🕐 Content-calendar timezone now asks YOU instead of assuming Denver time
- ✅ Every fix verified + audit-22 green before this shipped

**All tiers.** Just type `/linda-sync` and you're current.

Yeeee Hawww 🤠

---

## 2026-06-09 — 🎯 Sauce Underwriter is live

**What's new:**

- 🎯 **`/linda-trigger`** — NEW skill. Bandit (Deal Hunter) runs YOUR locked Sauce Underwriter formula on any single-family wholesale or fix-and-flip deal. Outputs MAO, dispo price, and a green/yellow/red verdict. Try: *"Pull the trigger — 1900 sqft, ARV $310K, Regular Rehab"*
- 📦 **real-estate-pro pack refreshed** — `linda-deals` now points at `linda-trigger` for SFR wholesale/flip math; still handles multifamily, MHP/RV, and creative finance separately.

**For Platinum + Gold tiers.**

Yeeee Hawww 🤠

---

## 2026-06-09 — 🚀 One-click install + dual-path setup

**What's new in your install:**

- 🚀 **`Start-LindaAI.bat`** (Windows) and **`Start-LindaAI.command`** (Mac) — double-click installers. Auto-install Node, Git, Claude Code, then drop you straight into LindaAI. No PowerShell wrestling.
- 📚 **`customer-guides/`** — 8-PDF library you can read anytime (Getting Started, Discord, Email, Voice, SMS, Auto-Publish, Windows Quick Start, Library index).
- 📱 **`CLAUDE-AI/`** folder — bonus claude.ai Projects bundle for iPhone, iPad, Android, or any browser. Same brain, anywhere you ride.
- 🛡️ **`/audit22`** is now a hard gate before any update ships to you — Sentry leak-scans, audit-auditor reviews, Ranger visual-QAs. No more surprises in your inbox.

**For ALL tiers (Bronze · Silver · Gold · Platinum).**

---

## How to grab future updates

Type `/linda-sync` in Claude Code any time. The crew pulls down whatever's new for your tier — and you'll see exactly what landed in your install + what you can do with it.

---

— © 2022-2026 Daniel Wise · LindaAI
