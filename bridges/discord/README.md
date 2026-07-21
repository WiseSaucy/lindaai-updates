# 🤖 LindaAI Discord — Channel Command System

One bot, isolated channels, and the **Sauce Underwriter baked in from day one**.
Each channel has its **own** slash commands, its **own** skills, and its **own**
memory — nothing crosses over. You run everything from Discord (desktop or phone),
and the work happens on your always-on computer.

## What you get out of the box

| Channel | Catch-all | Quick commands | What it does |
|---|---|---|---|
| 🏠 **Deals** | `/deals` | `/underwrite` `/flip` `/comps` | Real estate — the Sauce Underwriter (wholesale MAO **+** fix-and-flip P&L with ARV check), comps |
| 💼 **Linda AI** | `/linda` | `/brief` `/mail` `/followup` `/research` | General assistant — email, research, briefings, follow-ups |

Plus, anywhere: `/howdy` — online + pipeline check (verifies the claude CLI too), and
`/reset` — forget the current channel/thread's conversation and start fresh.

**The Sauce Underwriter needs zero extra setup** — the locked formula ships inside
`bot.py`, so `/underwrite` works the moment the bot is online: paste an address, get
the wholesale MAO, the full flip P&L, the all-in % of ARV, and where you stand
against the 70% rule.

## How isolation works (no crossings)

1. **Behavior** — each command tells Claude to use **only** that channel's skills, and to
   refuse + redirect if you ask for another channel's job.
2. **Placement** — run a command in the wrong channel and the bot replies privately
   ("that command lives in #deals") instead of answering. A channel's **category**
   decides its business, so every forum under your Deals category is Deals.
3. **Memory** — conversations are kept **per channel and per forum post/thread**, expire
   after 12h of quiet (`SESSION_TTL_HOURS`), and `/reset` clears one on demand.
4. **People** — the bot only answers Discord IDs in `DISCORD_ALLOWED_USER_IDS`; restrict
   a single channel further with `CHANNEL_ALLOWED_USERS_<KEY>=id1,id2` in `discord.env`.
5. **Human-only channels** — channels not mapped to any business are always bot-silent
   (make a "Team" category and chat freely). To mute plain-message replies in a mapped
   channel, list it in that business's `quiet_channels` in `channels.json` — the bot
   stays out of conversation there but still answers explicit slash commands.

It's all driven by **`channels.json`** (next to `bot.py`). That one file controls which
commands belong to which channel and which skills each may use. Add channels for your
own businesses, rename things, move commands — edit it and restart. No code changes.

## Files
- `bot.py` — the bridge. Registers per-channel commands, enforces isolation, runs the
  local `claude` CLI on your Max subscription (no API charges).
- `channels.json` — the channel → commands → skills map (**edit this to change anything**).
- `setup_channels.py` — one-shot script that creates the Deals + Linda AI channels
  (with deal-structure tags) in your server. Safe to re-run.
- `discord.env.example` — copy to `~/.claude/lindaai/discord.env` and fill in.
- `run-bot.sh` / `stop-bot.sh` — start/stop.
- `com.lindaai.discord-bridge.plist.template` — launchd daemon for 24/7 auto-start (macOS).

## Setup
Run the **`discord-setup`** skill (`/discord-setup`) in Claude and follow it: create the
bot app, invite it, fill `discord.env`, run `setup_channels.py`, start the bot. Then type
`/underwrite` in your #deals channel — you're underwriting.

© 2026 LindaAI — Built by Daniel Wise
