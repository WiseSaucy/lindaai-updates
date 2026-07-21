"""
LindaAI Discord Bridge — Claude Max subscription edition (per-channel build).

Calls the local `claude` CLI as a subprocess (Claude Code headless), stripping
ANTHROPIC_API_KEY from the child env so authentication falls through to the
user's Claude.ai Max subscription. NO Anthropic API credits consumed.

Per-channel command isolation:
  * Every Discord channel gets its OWN slash commands, defined in channels.json.
  * Commands are LOCKED to their channel — a Deals command run in #linda-ai is
    politely refused and points you to the right channel.
  * Each channel's commands tell Claude to use ONLY that channel's skills, so
    there are NO crossings between the businesses.
  * Conversation memory is kept PER discord channel/forum-post (and expires
    after SESSION_TTL_HOURS), so deals and clients never bleed into each other.
  * Deals: /underwrite and /flip; with ENABLE_MESSAGE_TRIGGERS=1 +
    Message Content Intent, pasting a bare address auto-underwrites and any
    plain message is handled by that channel's assistant (auto_respond).

Reads from ~/.claude/lindaai/discord.env:
  DISCORD_BOT_TOKEN          (required) — bot token from Discord developer portal
  DISCORD_ALLOWED_USER_IDS   (required) — comma-separated Discord user IDs who may
                                          use the bot (singular DISCORD_ALLOWED_USER_ID
                                          also accepted)
  DISCORD_GUILD_ID           (optional) — server ID for INSTANT slash-command sync
  CHANNEL_ALLOWED_USERS_<KEY>(optional) — restrict ONE channel to specific user IDs,
                                          e.g. CHANNEL_ALLOWED_USERS_DEALS=111,222
                                          (<KEY> = channel key uppercased, - -> _).
                                          Keeps personal IDs out of channels.json.
  CLAUDE_BIN                 (optional) — path to claude CLI (auto-detected if not set)
  CLAUDE_PROJECT_DIR         (optional) — where claude runs (default: the LindaAI folder this bridge lives in)
  CLAUDE_MODEL               (optional) — model id (default: claude-sonnet-4-5)
  CLAUDE_TIMEOUT_SECONDS     (optional) — max seconds per claude call (default 300)
  SESSION_TTL_HOURS          (optional) — hours before a conversation auto-resets (default 12)
  CHANNELS_CONFIG            (optional) — path to channels.json (default: next to this file)
  ENABLE_MESSAGE_TRIGGERS    (optional) — "1" enables plain-message handling (address
                                          auto-underwrite + auto_respond). Requires the
                                          Message Content Intent in the dev portal.
                                          (Legacy alias: ENABLE_AUTO_UNDERWRITE.)

Design rules:
  1. SLASH COMMANDS by default — no privileged intents required.
  2. CLAUDE CLI SUBPROCESS — uses Claude Max subscription (no API billing).
  3. INSTANT GUILD SYNC + a global sync (DMs work; stale globals get cleared).
  4. STRIP ANTHROPIC_API_KEY from child env so CLI falls through to Max auth.
  5. PER-CHANNEL/THREAD SESSION RESUME with TTL — memory that can't bleed or
     grow forever; /reset clears the current conversation.
  6. MESSAGE TRIGGERS are OPT-IN only (privileged intent), off by default.

© 2026 LindaAI — Built by Daniel Wise
"""
import asyncio
import json
import os
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

import aiohttp  # ships with discord.py

# ─── DEPS ──────────────────────────────────────────────────────────────────
try:
    import discord
    from discord import app_commands
except ImportError:
    print("ERROR: discord.py not installed. Run:  pip3 install --user discord.py", flush=True)
    sys.exit(1)


# ─── ENV LOAD ──────────────────────────────────────────────────────────────
ENV_FILE = Path.home() / ".claude" / "lindaai" / "discord.env"
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        key = k.strip()
        val = v.strip().strip('"').strip("'")
        # File wins over empty/missing shell env. Customers often have
        # ANTHROPIC_API_KEY="" set from prior installs, which must not mask
        # the file value.
        if not os.environ.get(key, "").strip():
            os.environ[key] = val

TOKEN          = os.environ.get("DISCORD_BOT_TOKEN", "").strip()
# Owners: DISCORD_ALLOWED_USER_IDS (comma-separated). Older singular form accepted.
ALLOWED_USERS_RAW = (
    os.environ.get("DISCORD_ALLOWED_USER_IDS", "").strip()
    or os.environ.get("DISCORD_ALLOWED_USER_ID", "").strip()
)
GUILD_ID_RAW   = os.environ.get("DISCORD_GUILD_ID", "").strip()
MODEL          = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5").strip()
PROJECT_DIR    = os.environ.get("CLAUDE_PROJECT_DIR", str(Path(__file__).resolve().parents[2]))
# ENABLE_MESSAGE_TRIGGERS gates ALL plain-message handling (auto-underwrite +
# auto_respond). ENABLE_AUTO_UNDERWRITE kept as a legacy alias.
_TRUTHY = ("1", "true", "yes", "on")
MSG_TRIGGERS = (
    os.environ.get("ENABLE_MESSAGE_TRIGGERS", "").strip().lower() in _TRUTHY
    or os.environ.get("ENABLE_AUTO_UNDERWRITE", "").strip().lower() in _TRUTHY
)
CLAUDE_TIMEOUT = int(os.environ.get("CLAUDE_TIMEOUT_SECONDS", "300") or "300")
SESSION_TTL_S  = float(os.environ.get("SESSION_TTL_HOURS", "12") or "12") * 3600
CHANNELS_CONFIG = os.environ.get("CHANNELS_CONFIG", "").strip() or str(Path(__file__).resolve().parent / "channels.json")

# ─── PATH SELF-HEAL ────────────────────────────────────────────────────────
# Under launchd the daemon can start with a bare PATH (/usr/bin:/bin:...).
# The claude CLI is a node script ("#!/usr/bin/env node"), so even when we
# invoke claude by absolute path, its launcher dies with exit 127
# ("env: node: No such file or directory") if the dir holding `node` isn't
# on PATH. Prepend the standard tool dirs so claude/node always resolve,
# no matter how the plist was written. child_env inherits this.
_TOOL_DIRS = [
    str(Path.home() / ".npm-global" / "bin"),
    str(Path.home() / ".local" / "bin"),
    "/usr/local/bin",
    "/opt/homebrew/bin",
]
_path_parts = [p for p in os.environ.get("PATH", "").split(os.pathsep) if p]
_missing_dirs = [d for d in _TOOL_DIRS if d not in _path_parts and Path(d).is_dir()]
if _missing_dirs:
    os.environ["PATH"] = os.pathsep.join(_missing_dirs + _path_parts)
    print(f"PATH self-heal: prepended {_missing_dirs} (daemon env was missing them)", flush=True)

# Auto-detect claude CLI
CLAUDE_BIN = os.environ.get("CLAUDE_BIN", "").strip()
if not CLAUDE_BIN:
    for candidate in [
        Path.home() / ".npm-global" / "bin" / "claude",
        Path("/usr/local/bin/claude"),
        Path("/opt/homebrew/bin/claude"),
    ]:
        if candidate.exists():
            CLAUDE_BIN = str(candidate)
            break
    if not CLAUDE_BIN:
        which = shutil.which("claude")
        if which:
            CLAUDE_BIN = which

GUILD_ID = None
if GUILD_ID_RAW.isdigit():
    GUILD_ID = int(GUILD_ID_RAW)

# ─── VALIDATE ──────────────────────────────────────────────────────────────
if not TOKEN:
    print("ERROR: DISCORD_BOT_TOKEN not set in ~/.claude/lindaai/discord.env", flush=True)
    sys.exit(1)

_id_parts = [p.strip() for p in ALLOWED_USERS_RAW.split(",") if p.strip()]
_bad_ids = [p for p in _id_parts if not p.isdigit()]
ALLOWED_USER_IDS = {int(p) for p in _id_parts if p.isdigit()}
if _bad_ids:
    # Don't silently drop a mistyped family member — say so loudly at startup.
    print(f"⚠ WARNING: ignoring malformed owner ID(s) in DISCORD_ALLOWED_USER_IDS: {_bad_ids} "
          "(IDs are digits only — re-copy with Developer Mode → Copy User ID)", flush=True)
if not ALLOWED_USER_IDS:
    print("ERROR: no valid owner IDs. Set DISCORD_ALLOWED_USER_IDS (comma-separated) "
          "in ~/.claude/lindaai/discord.env.", flush=True)
    sys.exit(1)

if not CLAUDE_BIN or not Path(CLAUDE_BIN).exists():
    print(f"ERROR: claude CLI not found. Tried CLAUDE_BIN={CLAUDE_BIN!r}", flush=True)
    print("  Install Claude Code: npm install -g @anthropic-ai/claude-code", flush=True)
    sys.exit(1)


# ─── CHANNEL CONFIG ────────────────────────────────────────────────────────
def _norm(s: str) -> str:
    """Normalize a channel name for matching: lowercase, strip #, drop separators."""
    return re.sub(r"[\s\-_#]+", "", (s or "").lower())


def _resolve_skill_path(name: str) -> str | None:
    """Find a skill file in the LindaAI project: skills/<n>/SKILL.md,
    skills/<n>.md, or packs/*/skills/<n>/SKILL.md."""
    root = Path(PROJECT_DIR)
    for cand in (root / "skills" / name / "SKILL.md", root / "skills" / f"{name}.md"):
        if cand.exists():
            return str(cand.relative_to(root))
    packs = root / "packs"
    if packs.is_dir():
        for pack in packs.iterdir():
            cand = pack / "skills" / name / "SKILL.md"
            if cand.exists():
                return str(cand.relative_to(root))
    return None


def load_channels() -> list[dict]:
    p = Path(CHANNELS_CONFIG)
    if not p.exists():
        print(f"ERROR: channels config not found at {p}", flush=True)
        sys.exit(1)
    data = json.loads(p.read_text())
    chans = data.get("channels", [])
    if not chans:
        print(f"ERROR: no channels defined in {p}", flush=True)
        sys.exit(1)
    for c in chans:
        c["_norm_names"] = {_norm(n) for n in c.get("names", [])} | {_norm(c.get("key", ""))}
        c["_norm_cats"] = {_norm(n) for n in c.get("category_names", []) if n}
        c["_id"] = str(c.get("id", "")).strip()
        # Per-channel user restriction comes from the ENV (keeps personal IDs
        # out of the repo): CHANNEL_ALLOWED_USERS_<KEY>=id1,id2. A non-empty
        # allowed_users in channels.json still works but env wins.
        env_key = "CHANNEL_ALLOWED_USERS_" + c["key"].upper().replace("-", "_")
        env_val = os.environ.get(env_key, "").strip()
        if env_val:
            c["allowed_users"] = [x.strip() for x in env_val.split(",") if x.strip().isdigit()]
        # quiet_channels: Discord channels (names or IDs) inside this business
        # where the bot IGNORES plain messages — humans talk freely, slash
        # commands still work when explicitly invoked.
        quiet = c.get("quiet_channels", [])
        c["_quiet_names"] = {_norm(str(x)) for x in quiet if not str(x).strip().isdigit()}
        c["_quiet_ids"] = {str(x).strip() for x in quiet if str(x).strip().isdigit()}
        # Resolve skill names to real files so prompts can point Claude at them;
        # warn loudly about any skill that doesn't exist anywhere.
        resolved, missing = {}, []
        for s in c.get("skills", []):
            path = _resolve_skill_path(s)
            (resolved.__setitem__(s, path) if path else missing.append(s))
        c["_skill_paths"] = resolved
        if missing:
            print(f"⚠ WARNING: channel '{c['key']}' references skills with no file in "
                  f"{PROJECT_DIR}: {missing}", flush=True)
    return chans


CHANNELS = load_channels()


def channel_for(interaction_or_channel) -> dict | None:
    """Resolve which configured business this Discord channel belongs to.

    A forum POST or THREAD resolves to its parent forum/channel. Match order:
      1) explicit channel id pin,
      2) parent CATEGORY — the category a channel sits under decides its
         business, so a #comps forum under the Deals category is Deals
         (generic name aliases must not cross businesses),
      3) channel/parent name aliases (for uncategorized channels).
    """
    ch = getattr(interaction_or_channel, "channel", interaction_or_channel)
    if ch is None:
        return None

    base = ch
    if isinstance(ch, discord.Thread) and ch.parent is not None:
        base = ch.parent

    ids = {str(getattr(ch, "id", "") or ""), str(getattr(base, "id", "") or "")}
    ids.discard("")
    names = {_norm(getattr(x, "name", "") or "") for x in (ch, base)}
    names.discard("")
    cat = getattr(base, "category", None)
    cat_name = _norm(getattr(cat, "name", "") or "") if cat else ""

    for c in CHANNELS:
        if c["_id"] and c["_id"] in ids:
            return c
    if cat_name:
        for c in CHANNELS:
            if cat_name in c.get("_norm_cats", set()):
                return c
    for c in CHANNELS:
        if names & c["_norm_names"]:
            return c
    return None


def is_quiet_channel(chan: dict, discord_channel) -> bool:
    """True if this Discord channel (or its parent forum) is in the business's
    quiet_channels list — plain messages are ignored there so humans can talk;
    slash commands still work."""
    base = discord_channel
    parent = getattr(discord_channel, "parent", None)
    ids = {str(getattr(x, "id", "") or "") for x in (base, parent) if x is not None}
    names = {_norm(getattr(x, "name", "") or "") for x in (base, parent) if x is not None}
    ids.discard(""); names.discard("")
    return bool(ids & chan.get("_quiet_ids", set()) or names & chan.get("_quiet_names", set()))


# ─── SESSION MEMORY (per discord channel/thread, with TTL) ─────────────────
# Keyed by "<business>:<discord channel or thread id>" so each deal post /
# client thread keeps its OWN conversation — no bleed between deals, clients,
# or businesses. Sessions expire after SESSION_TTL_S and /reset clears one.
_sessions: dict[str, tuple[str, float]] = {}      # key -> (session_id, last_used_ts)
_session_locks: dict[str, asyncio.Lock] = {}      # serialize claude calls per key


def session_key_for(chan: dict, discord_channel) -> str:
    cid = getattr(discord_channel, "id", "") or "dm"
    return f"{chan['key']}:{cid}"


def _lock_for(key: str) -> asyncio.Lock:
    if key not in _session_locks:
        _session_locks[key] = asyncio.Lock()
    return _session_locks[key]


# ─── PROMPT BUILDING ───────────────────────────────────────────────────────
# One consistent rule for links in requests (Google Drive is the common case:
# public files work via the export/download URL form; private ones can't be
# fetched by anyone, so ask for link-sharing or a direct Discord upload).
LINKS_HINT = (
    "If the request contains links, FETCH them for context. Google Drive/Docs: "
    "use the direct form — docs.google.com/document/d/<ID>/export?format=txt for Docs, "
    "drive.google.com/spreadsheets/d/<ID>/export?format=csv for Sheets, "
    "drive.google.com/uc?export=download&id=<ID> for files. If the fetch fails the file "
    "is PRIVATE — say so and ask for 'Anyone with the link (Viewer)' sharing or a direct "
    "Discord upload, then continue with your best estimates from what you have. "
    "Discord photo/PDF attachments arrive as LOCAL FILE PATHS — use the Read tool on "
    "them to actually see the images."
)


ATTACH_ROOT = Path(tempfile.gettempdir()) / "lindaai-discord-attachments"

# ─── GOOGLE DRIVE PRE-FETCH ────────────────────────────────────────────────
# The bridge ATTEMPTS every Drive/Docs link itself before Claude runs, so a
# link is never declared "private" without a real try. Successes become local
# files Claude can Read; failures carry the exact HTTP result.
DRIVE_LINK_RE = re.compile(r"https://(?:drive|docs)\.google\.com/[^\s<>|)\]]+")
_DRIVE_ID_RES = (re.compile(r"/d/([A-Za-z0-9_-]{10,})"), re.compile(r"[?&]id=([A-Za-z0-9_-]{10,})"))
_CT_EXT = {"application/pdf": ".pdf", "image/jpeg": ".jpg", "image/png": ".png",
           "text/csv": ".csv", "text/plain": ".txt",
           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
           "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx"}
_DRIVE_MAX = 25 * 1024 * 1024


def _drive_candidates(url: str):
    """(file_id, [(download_url, forced_ext), ...]) for a Drive/Docs link."""
    fid = None
    for rx in _DRIVE_ID_RES:
        m = rx.search(url)
        if m:
            fid = m.group(1)
            break
    if not fid or "/folders/" in url:
        return fid, []
    if "docs.google.com/document" in url:
        return fid, [(f"https://docs.google.com/document/d/{fid}/export?format=txt", ".txt")]
    if "docs.google.com/spreadsheets" in url:
        return fid, [(f"https://docs.google.com/spreadsheets/d/{fid}/export?format=csv", ".csv")]
    if "docs.google.com/presentation" in url:
        return fid, [(f"https://docs.google.com/presentation/d/{fid}/export/pdf", ".pdf")]
    return fid, [(f"https://drive.google.com/uc?export=download&id={fid}", ""),
                 (f"https://drive.google.com/uc?export=download&confirm=t&id={fid}", "")]


async def drive_links_block(text: str, tag) -> str:
    """Attempt-download every Drive link in text; report exactly what happened."""
    urls = list(dict.fromkeys(DRIVE_LINK_RE.findall(text or "")))
    if not urls:
        return ""
    dest = ATTACH_ROOT / str(tag)
    dest.mkdir(parents=True, exist_ok=True)
    lines = []
    async with aiohttp.ClientSession() as sess:
        for url in urls[:5]:
            fid, cands = _drive_candidates(url)
            if "/folders/" in url:
                lines.append(f"  - {url} → FOLDER link: folders can't be fetched even when "
                             "public — ask for the individual file links or Discord uploads.")
                continue
            if not cands:
                lines.append(f"  - {url} → no file id found in the URL; try WebFetch on it yourself.")
                continue
            last = "no attempt"
            done = False
            for dl_url, ext in cands:
                try:
                    async with sess.get(dl_url, allow_redirects=True,
                                        timeout=aiohttp.ClientTimeout(total=30)) as r:
                        ct = (r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
                        if r.status == 200 and ct != "text/html":
                            data = await r.content.read(_DRIVE_MAX + 1)
                            if len(data) > _DRIVE_MAX:
                                lines.append(f"  - {url} → file is over 25MB; ask for a smaller export or the key pages.")
                                done = True
                                break
                            p = dest / f"drive-{fid}{ext or _CT_EXT.get(ct, '.bin')}"
                            p.write_bytes(data)
                            lines.append(f"  - {url} → DOWNLOADED to {p} (use the Read tool on it)")
                            done = True
                            break
                        last = f"HTTP {r.status}, {ct or 'unknown type'}"
                except Exception as e:
                    last = type(e).__name__
            if not done:
                lines.append(f"  - {url} → ATTEMPTED and failed ({last}). Most likely not link-shared: "
                             "tell the user you TRIED (quote the error), then ask for 'Anyone with the "
                             "link (Viewer)' sharing or a direct Discord upload.")
    return ("\n\nGOOGLE DRIVE LINKS — the bridge already ATTEMPTED each download "
            "(never claim a link is private beyond what these attempts show):\n" + "\n".join(lines))


async def attachments_block(message) -> str:
    """Download Discord uploads (photos/PDFs/etc.) to local files so Claude can
    actually SEE them via its Read tool (vision) — not just know their URLs."""
    atts = getattr(message, "attachments", None) or []
    if not atts:
        return ""
    dest = ATTACH_ROOT / str(message.id)
    dest.mkdir(parents=True, exist_ok=True)
    lines = []
    for a in atts[:10]:
        if getattr(a, "size", 0) > 25 * 1024 * 1024:
            lines.append(f"  - {a.filename}: SKIPPED (over 25MB — repost smaller)")
            continue
        p = dest / Path(a.filename).name
        try:
            await a.save(p)
            lines.append(f"  - {p}")
        except Exception as e:
            lines.append(f"  - {a.filename}: {a.url}  (local save failed: {type(e).__name__} — fetch the URL instead)")
    return ("\n\nATTACHED FILES — saved locally; use the Read tool on each path "
            "(Read renders photos and PDFs so you can SEE them):\n" + "\n".join(lines))


def scoped_prompt(chan: dict, user_text: str, skill_hint: str | None = None) -> str:
    """Wrap the user's request so Claude stays in this channel's lane (no crossings)."""
    paths = chan.get("_skill_paths", {})
    if paths:
        skills = "; ".join(f"{n} ({p})" for n, p in paths.items() if p) or "(your general skills)"
    else:
        skills = ", ".join(chan.get("skills", [])) or "(your general skills)"
    lines = [
        f"[CHANNEL: {chan['label']}]",
        f"You are answering inside the '{chan['label']}' Discord channel.",
        f"This channel's domain is: {chan['domain']}",
        "",
        "STAY IN YOUR LANE — strict rules:",
        f"  - You may ONLY use these LindaAI skills — each is a SKILL.md file in this "
        f"project; Read the file and follow it when it applies: {skills}.",
        "  - Do NOT use, invoke, or even mention skills or capabilities that belong to "
        "the OTHER channels (e.g. real-estate underwriting, credit repair/funding, or "
        "general assistant work that is not this channel's job).",
        "  - If the user's request clearly belongs to a different channel, do not answer it "
        "here. Briefly tell them which channel to use, then stop.",
        "  - Keep replies tight and Discord-friendly (this is a chat, not a document).",
        f"  - {LINKS_HINT}",
    ]
    if skill_hint:
        hint_path = paths.get(skill_hint)
        lines.append(f"  - Preferred skill for this request: {skill_hint}"
                     + (f" ({hint_path})." if hint_path else "."))
    lines += ["", "USER REQUEST:", user_text]
    return "\n".join(lines)


# Locked Sauce Underwriter formula embedded so /underwrite is deterministic and
# self-contained even if the skill file isn't loaded for some reason.
UNDERWRITE_PROMPT = """[CHANNEL: Deals — Real Estate]
Run the Sauce Underwriter on the property below. If a linda-trigger / deal-analyzer
skill file exists in this project you may Read it for extra detail, but the LOCKED
formula below is complete and authoritative on its own.
Give me BOTH exits: the wholesale MAO AND the fix-and-flip numbers (I may flip it myself).

PROPERTY (from the user): {addr}

Do this:
0. If the input contains links (Zillow, Google Drive, etc.), FETCH them for details. For
   Google Drive/Docs use the direct form (drive.google.com/uc?export=download&id=<ID>;
   Docs: /export?format=txt). If a Drive fetch fails the file is private — note it, ask for
   'Anyone with the link' sharing or a Discord upload, and continue with web estimates.
1. Identify the subject address. If asking price / sqft / repair level were given, use them.
2. If sqft or ARV is missing, pull what you can via web search (recent SOLD comps,
   subject sqft, neighborhood) to estimate ARV = avg(comp $/sqft) x subject sqft.
   State every assumption you make.
3. WHOLESALE — run the LOCKED Sauce formula (do NOT deviate):
   - Selling Costs   = ARV * 7%
   - Repair Cost     = sqft * repair_$psf  (Move-In Ready 8 / Cosmetic 15 / Regular 39 / Full 65 / Major 100)
   - Investor Profit = MAX(20000, 0.57*RepairCost, 0.10*ARV)
   - Holding Costs   = ARV * (MoveIn/Cosmetic 3% / Regular 4% / Full 5% / Major 6%)
   - DISPO PRICE     = ARV - SellingCosts - RepairCost - InvestorProfit - HoldingCosts
   - Wholesale Fee   = 15000 (unless user said otherwise)
   - MAO             = DISPO PRICE - Wholesale Fee
   Verdict: GREEN MAO<70% ARV, YELLOW 70-80%, RED >80%.
   - ARV CHECK (always show these two lines):
       All-In % of ARV = (MAO + RepairCost) / ARV * 100  — "we're at X% of ARV all-in"
       70% Rule benchmark = 0.70*ARV - RepairCost — show MAO vs it (over/under by $ and %)
4. FIX-AND-FLIP (if I buy + rehab + sell it myself) — run a full P&L:
   - Purchase Price (use asking, or the MAO if no price given — say which)
   - Buy-side closing (~2% of purchase)
   - Rehab Cost (sqft * repair_$psf from the table above)
   - Holding Costs (taxes/insurance/utilities for the hold; default ARV * holding% from table)
   - Financing cost if applicable (note assumptions — points + interest, or skip if all-cash)
   - Sell-side: Selling Costs = ARV * 7% (commissions + closing)
   - NET FLIP PROFIT = ARV - Purchase - BuyClosing - Rehab - Holding - Financing - SellingCosts
   - Flip ROI %      = NET FLIP PROFIT / (Purchase + Rehab + Holding + Financing) * 100
   - ARV CHECK (always show): All-In % of ARV = (Purchase + Rehab) / ARV * 100, and
     Purchase vs the 70% Rule benchmark (0.70*ARV - Rehab) — over/under by $ and %.
   Flip verdict: GREEN if NET PROFIT >= $25k AND ROI >= 15%; YELLOW if profit $10-25k or ROI 8-15%;
   RED if profit < $10k or ROI < 8% (the flip doesn't pay for the risk — walk or wholesale instead).
5. Output the wholesale table, then the flip P&L table, then say which exit is better and why.
6. End with ONE recommended next action.

RULES — find, don't ask:
- Do NOT ask me for numbers you can find or derive. The MAO never needs a purchase
  price. For the flip P&L, Purchase = asking price if known, otherwise the MAO (say which).
- Hunt the data yourself: WEB-SEARCH the address for list price, sqft, beds/baths, and
  recent SOLD comps — Zillow/Redfin/Realtor.com search results and snippets, county
  assessor/property records. Listing sites often block direct page fetches: search
  snippets usually carry the numbers anyway. Cross-check at least two sources.
- If PHOTOS are attached, Read every image and SET THE REPAIR LEVEL FROM WHAT YOU SEE:
  go room by room, list the visible work (kitchen, baths, flooring, paint, roof/HVAC if
  shown), pick the $psf tier it implies (Move-In 8 / Cosmetic 15 / Regular 39 / Full 65 /
  Major 100), and use it in the formula. Show the room-by-room scope in your reply.
- Only if search AND photos leave you truly blind may you ask ONE question — and even
  then, run the numbers with your best estimate FIRST and show them.
"""

# Flip-focused prompt for /flip — deeper on the self-flip P&L.
FLIP_PROMPT = """[CHANNEL: Deals — Real Estate]
Run a FIX-AND-FLIP analysis (I'm flipping this myself). Account for EVERY cost so I
know my real take-home. The formula below is complete on its own.

DEAL (from the user): {addr}

Do this:
0. If the input contains links (Zillow, Google Drive, etc.), FETCH them for details. For
   Google Drive/Docs use the direct form (drive.google.com/uc?export=download&id=<ID>;
   Docs: /export?format=txt). If a Drive fetch fails the file is private — note it, ask for
   'Anyone with the link' sharing or a Discord upload, and continue with web estimates.
1. Establish: Purchase Price, Rehab (sqft * repair_$psf — Move-In 8 / Cosmetic 15 / Regular 39 /
   Full 65 / Major 100), and ARV. If ARV is missing, estimate from SOLD comps via web search and
   state assumptions.
2. Full flip P&L:
   - Purchase Price
   - Buy-side closing (~2% of purchase)
   - Rehab Cost
   - Holding Costs (months_held * monthly carry; default 4 months, taxes+insurance+utilities; if
     unknown use ARV * holding% from the table)
   - Financing (if not all-cash: points + monthly interest over the hold; state the rate/points
     you assume, e.g. hard money 2 pts + 11%)
   - Sell-side Selling Costs = ARV * 7%
   - NET FLIP PROFIT = ARV - Purchase - BuyClosing - Rehab - Holding - Financing - SellingCosts
   - Cash invested = Purchase + Rehab + Holding + Financing (less loan proceeds if financed)
   - ROI % = NET PROFIT / Cash invested * 100   and   Annualized ROI = ROI% * (12 / months_held)
   - ARV CHECK (always show): All-In % of ARV = (Purchase + Rehab) / ARV * 100, and
     Purchase vs the 70% Rule benchmark (0.70*ARV - Rehab) — over/under by $ and %.
3. Show the P&L table + a 3-scenario sensitivity (ARV -5% / base / rehab +15%).
4. Verdict: GREEN profit >= $25k AND ROI >= 15%; YELLOW profit $10-25k or ROI 8-15%;
   RED profit < $10k or ROI < 8%.
5. End with ONE recommended next action (proceed / renegotiate to $X / wholesale instead / walk).

RULES — find, don't ask: web-search the address for price/sqft/SOLD comps (Zillow/
Redfin/Realtor snippets, county records) instead of asking me. If photos are attached,
Read every image and set the repair level from what you SEE (room-by-room scope + the
$psf tier it implies). Purchase defaults to asking price, else the wholesale MAO. Ask at
most ONE question, and only after showing best-estimate numbers.
"""

# Named prompt templates a quick_command can opt into via "template" in
# channels.json (renaming the command no longer silently loses the template).
PROMPT_TEMPLATES = {"underwrite": UNDERWRITE_PROMPT, "flip": FLIP_PROMPT}


# ─── CLAUDE CLI CALL ───────────────────────────────────────────────────────
async def run_claude(prompt: str, session_key: str) -> str:
    """Invoke claude CLI in headless mode. Uses Max subscription (NOT API).

    Serialized per session_key (no concurrent --resume of one session), with a
    hard timeout so a hung CLI can't wedge the bot, and TTL-based session
    expiry so conversations don't grow forever.
    """
    async with _lock_for(session_key):
        cmd = [
            CLAUDE_BIN,
            "-p", prompt,
            "--output-format", "json",
            "--model", MODEL,
            "--setting-sources", "user,project,local",
            "--dangerously-skip-permissions",
        ]
        entry = _sessions.get(session_key)
        if entry and (time.time() - entry[1]) < SESSION_TTL_S:
            cmd += ["--resume", entry[0]]
        elif entry:
            del _sessions[session_key]  # expired — start fresh

        # CRITICAL: strip ANTHROPIC_API_KEY so claude CLI uses Max subscription auth.
        child_env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=PROJECT_DIR,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=child_env,
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=CLAUDE_TIMEOUT)
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            raise RuntimeError(
                f"claude timed out after {CLAUDE_TIMEOUT}s — if this repeats, check the "
                "OAuth token (`claude setup-token`) and the office machine's network."
            )

        if proc.returncode != 0:
            err = stderr.decode("utf-8", errors="replace")[:1500]
            out = stdout.decode("utf-8", errors="replace")[:1500]
            print(f"[bot.py] claude exit {proc.returncode} | stderr={err!r} | stdout={out!r}", flush=True)
            raise RuntimeError(f"claude exit {proc.returncode}: {err or out or '(no output)'}")

        raw = stdout.decode("utf-8", errors="replace").strip()
        try:
            data = json.loads(raw)
            new_sid = data.get("session_id")
            if new_sid:
                _sessions[session_key] = (new_sid, time.time())
            return data.get("result") or data.get("text") or raw[:4000] or "(empty)"
        except json.JSONDecodeError:
            return raw[:4000] or "(empty response)"


# ─── DISCORD CHUNKING ──────────────────────────────────────────────────────
def chunk_text(text: str, limit: int = 1900) -> list[str]:
    """Discord caps messages at 2000 chars; one splitter for every send path."""
    return [text[i:i + limit] for i in range(0, len(text), limit)] or ["(empty reply)"]


async def send_chunked(interaction: discord.Interaction, text: str):
    for c in chunk_text(text):
        await interaction.followup.send(c)


# ─── DISCORD CLIENT ────────────────────────────────────────────────────────
intents = discord.Intents.default()
if MSG_TRIGGERS:
    # Plain-message handling needs to read message text. This is a PRIVILEGED
    # intent — the user must also enable "Message Content Intent" in the portal.
    intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)


def authorized(interaction: discord.Interaction) -> bool:
    return interaction.user.id in ALLOWED_USER_IDS


def channel_allows_user(chan: dict, user_id: int) -> bool:
    """A channel can be restricted to specific users (via the
    CHANNEL_ALLOWED_USERS_<KEY> env var, or allowed_users in channels.json).
    Empty/absent = every authorized owner may use it."""
    ids = chan.get("allowed_users") or []
    if not ids:
        return True
    return str(user_id) in {str(x) for x in ids}


async def deny_channel_user(interaction: discord.Interaction, chan: dict) -> bool:
    """True (and warns) if this owner isn't allowed in this specific channel."""
    if channel_allows_user(chan, interaction.user.id):
        return False
    await interaction.response.send_message(
        f"🔒 You don't have access to **{chan['label']}**.", ephemeral=True
    )
    return True


async def deny_unauthorized(interaction: discord.Interaction) -> bool:
    if authorized(interaction):
        return False
    await interaction.response.send_message(
        "🔒 This LindaAI is bound to its owner only.", ephemeral=True
    )
    return True


async def wrong_channel(interaction: discord.Interaction, expected: dict) -> bool:
    """True (and warns) if this command was run outside its home channel."""
    here = channel_for(interaction)
    if here is not None and here["key"] == expected["key"]:
        return False
    chan_name = expected["names"][0] if expected.get("names") else expected["key"]
    await interaction.response.send_message(
        f"↪️ That command lives in the **{expected['label']}** channel "
        f"(e.g. **#{chan_name}**). Run it there to keep things from crossing over.",
        ephemeral=True,
    )
    return True


# ─── DYNAMIC COMMAND REGISTRATION ──────────────────────────────────────────
def make_ask_handler(chan: dict):
    async def handler(interaction: discord.Interaction, message: str):
        if await deny_unauthorized(interaction):
            return
        if await wrong_channel(interaction, chan):
            return
        if await deny_channel_user(interaction, chan):
            return
        await interaction.response.defer(thinking=True)
        prompt = scoped_prompt(chan, message) + await drive_links_block(message, interaction.id)
        try:
            reply = await run_claude(prompt, session_key_for(chan, interaction.channel))
        except Exception as e:
            await interaction.followup.send(f"⚠️ LindaAI hit a snag: {e}")
            return
        await send_chunked(interaction, reply)
    return handler


def make_quick_handler(chan: dict, spec: dict):
    # A quick command can opt into a named prompt template via "template" in
    # channels.json; the command NAME is only a fallback so renames keep working.
    template = PROMPT_TEMPLATES.get(spec.get("template") or spec["name"])

    async def handler(interaction: discord.Interaction, value: str):
        if await deny_unauthorized(interaction):
            return
        if await wrong_channel(interaction, chan):
            return
        if await deny_channel_user(interaction, chan):
            return
        await interaction.response.defer(thinking=True)
        if template:
            prompt = template.format(addr=value)
        else:
            prompt = scoped_prompt(chan, value, skill_hint=spec.get("skill"))
        prompt += await drive_links_block(value, interaction.id)
        try:
            reply = await run_claude(prompt, session_key_for(chan, interaction.channel))
        except Exception as e:
            await interaction.followup.send(f"⚠️ LindaAI hit a snag: {e}")
            return
        await send_chunked(interaction, reply)
    return handler


def register_commands():
    for chan in CHANNELS:
        # Catch-all ask command for the channel, e.g. /saucedeals <message>
        ask_name = chan["ask_command"]
        ask_cb = make_ask_handler(chan)
        # describe() must be applied to the callback BEFORE Command() copies params.
        app_commands.describe(message=f"Your {chan['label']} request")(ask_cb)
        ask_cmd = app_commands.Command(
            name=ask_name,
            description=f"Ask LindaAI in {chan['label']}"[:100],
            callback=ask_cb,
        )
        tree.add_command(ask_cmd)

        # Quick one-shot commands unique to this channel.
        for spec in chan.get("quick_commands", []):
            arg_name = spec.get("arg", "input")
            quick_cb = make_quick_handler(chan, spec)
            app_commands.describe(value=spec.get("arg_desc", arg_name)[:100])(quick_cb)
            cmd = app_commands.Command(
                name=spec["name"],
                description=spec["description"][:100],
                callback=quick_cb,
            )
            tree.add_command(cmd)

    # Global health check (works anywhere). Verifies the claude BINARY too, so
    # a green /howdy means the pipeline can actually run (not just Discord).
    @tree.command(name="howdy", description="Quick LindaAI online + pipeline check")
    async def howdy(interaction: discord.Interaction):
        if await deny_unauthorized(interaction):
            return
        await interaction.response.defer(thinking=True, ephemeral=True)
        here = channel_for(interaction)
        where = here["label"] if here else "an unmapped channel"
        try:
            proc = await asyncio.create_subprocess_exec(
                CLAUDE_BIN, "--version",
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
            )
            out, _ = await asyncio.wait_for(proc.communicate(), timeout=15)
            cli = f"claude CLI ✅ ({out.decode().strip()[:40]})" if proc.returncode == 0 \
                else f"claude CLI ⚠️ exit {proc.returncode}"
        except Exception as e:
            cli = f"claude CLI ❌ ({type(e).__name__})"
        await interaction.followup.send(
            f"✅ LindaAI online. You're in **{where}**. {cli}\n"
            f"Type `/` to see this channel's commands.",
            ephemeral=True,
        )

    # Clear this channel/thread's conversation memory.
    @tree.command(name="reset", description="Forget this channel's conversation and start fresh")
    async def reset(interaction: discord.Interaction):
        if await deny_unauthorized(interaction):
            return
        here = channel_for(interaction)
        if not here:
            await interaction.response.send_message(
                "This channel isn't mapped to a LindaAI business — nothing to reset.",
                ephemeral=True)
            return
        key = session_key_for(here, interaction.channel)
        had = _sessions.pop(key, None)
        await interaction.response.send_message(
            f"🧹 {'Conversation cleared' if had else 'No saved conversation'} for "
            f"**{here['label']}** in this {'thread' if isinstance(interaction.channel, discord.Thread) else 'channel'}.",
            ephemeral=True,
        )


register_commands()


# ─── MESSAGE TRIGGERS (opt-in) ─────────────────────────────────────────────
ADDRESS_RE = re.compile(
    r"\d{1,6}\s+[\w\.\- ]+\b(st|street|ave|avenue|rd|road|dr|drive|ln|lane|blvd|"
    r"boulevard|ct|court|cir|circle|way|pl|place|hwy|highway|pkwy|terrace|ter|"
    r"trail|trl)\b",
    re.IGNORECASE,
)
# Words that signal the user wants something DONE with the address, not an
# underwrite of it ("draft an LOI for 123 Main St" must not fire the underwriter).
_INTENT_WORDS = re.compile(
    r"\b(draft|write|loi|comp|comps|outreach|letter|email|mail|list|listing|zillow|"
    r"pipeline|add|remove|update|schedule|call|text|post|market|research|what|why|"
    r"how|when|who|explain|show|find|negotiate|offer letter)\b|\?",
    re.IGNORECASE,
)


def looks_like_bare_address(content: str) -> bool:
    """True only when the message is essentially just an address (plus deal
    stats like price/sqft) — a stated request wins over the regex."""
    if not ADDRESS_RE.search(content):
        return False
    if _INTENT_WORDS.search(content):
        return False
    return len(content) <= 200


@bot.event
async def on_message(message: "discord.Message"):
    if not MSG_TRIGGERS:
        return
    if message.author.bot:
        return
    if message.author.id not in ALLOWED_USER_IDS:
        return
    chan = channel_for(message)
    if not chan:
        return
    if not channel_allows_user(chan, message.author.id):
        return
    if is_quiet_channel(chan, message.channel):
        return  # humans-only channel: the bot stays out of plain conversation
    content = (message.content or "").strip()
    if not content or content.startswith("/"):
        return  # let slash commands go through the normal command path

    # A bare address in an auto_underwrite channel -> the underwriter.
    # Anything else (including "do X with <address>") -> the channel assistant,
    # which can still choose to underwrite if that's what the request means.
    # Uploaded files (photos/PDFs) ride along as fetchable URLs either way.
    extra = await attachments_block(message) + await drive_links_block(content, message.id)
    if chan.get("auto_underwrite") and looks_like_bare_address(content):
        prompt = UNDERWRITE_PROMPT.format(addr=content) + extra
    elif chan.get("auto_respond"):
        prompt = scoped_prompt(chan, content) + extra
    else:
        return

    try:
        async with message.channel.typing():
            reply = await run_claude(prompt, session_key_for(chan, message.channel))
    except Exception as e:
        await message.channel.send(f"⚠️ LindaAI hit a snag: {e}")
        return
    for c in chunk_text(reply):
        await message.channel.send(c)


# ─── READY / SYNC ──────────────────────────────────────────────────────────
@bot.event
async def on_ready():
    print(f"✓ LindaAI Discord Bridge online as {bot.user}", flush=True)
    print(f"  Owners (IDs):     {', '.join(str(i) for i in sorted(ALLOWED_USER_IDS))}", flush=True)
    print(f"  Claude bin:       {CLAUDE_BIN}", flush=True)
    print(f"  Project dir:      {PROJECT_DIR}", flush=True)
    print(f"  Model:            {MODEL}", flush=True)
    print(f"  Channels:         {', '.join(c['label'] for c in CHANNELS)}", flush=True)
    print(f"  Message triggers: {'ON' if MSG_TRIGGERS else 'off'}", flush=True)
    print(f"  Session TTL:      {SESSION_TTL_S/3600:.0f}h | claude timeout: {CLAUDE_TIMEOUT}s", flush=True)
    print(f"  Auth:             Claude Max subscription (ANTHROPIC_API_KEY stripped)", flush=True)

    if GUILD_ID:
        try:
            guild_obj = discord.Object(id=GUILD_ID)
            # Commands are added to the global tree (no guild kwarg), so we must
            # copy_global_to before syncing to a specific guild — sync(guild=...)
            # alone only sends guild-specific commands, which would be 0.
            tree.copy_global_to(guild=guild_obj)
            synced = await tree.sync(guild=guild_obj)
            print(f"  ✓ Synced {len(synced)} commands to guild {GUILD_ID} (instant)", flush=True)
        except Exception as e:
            print(f"  ⚠ Guild sync failed for {GUILD_ID}: {e}", flush=True)

    # ALWAYS also sync globally: keeps DMs working and clears stale global
    # commands left by older deployments (global-only propagation can take ~1h).
    try:
        synced = await tree.sync()
        print(f"  ✓ Synced {len(synced)} commands globally (DMs; may take up to 1hr)", flush=True)
    except Exception as e:
        print(f"  ⚠ Global sync failed: {e}", flush=True)

    if not GUILD_ID:
        print("  ℹ️  TIP: Set DISCORD_GUILD_ID in discord.env for INSTANT slash-command sync.", flush=True)


# ─── RUN ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except discord.errors.PrivilegedIntentsRequired:
        print(
            "ERROR: ENABLE_MESSAGE_TRIGGERS (or legacy ENABLE_AUTO_UNDERWRITE) is on, "
            "which needs the MESSAGE CONTENT INTENT.\n"
            "  Fix: Discord dev portal -> your app -> Bot -> enable 'MESSAGE CONTENT INTENT'\n"
            "       -> Save, then restart the bot.\n"
            "  Or: set ENABLE_MESSAGE_TRIGGERS=0 in discord.env to use slash commands only.",
            flush=True,
        )
        sys.exit(1)
