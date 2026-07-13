#!/usr/bin/env python3
"""
One-time Discord channel setup script (safe to re-run — skips what exists).
Creates the default LindaAI layout: a Deals category with a #deals forum
(deal-structure tags included) and a Linda AI category with #linda-ai.

Run: python3 bridges/discord/setup_channels.py
"""
import urllib.request, urllib.error, json, time
from pathlib import Path

ENV = Path.home() / ".claude/lindaai/discord.env"

def parse_env(path):
    out = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out

if not ENV.exists():
    print(f"❌ {ENV} not found. Copy bridges/discord/discord.env.example there and fill it in first.")
    exit(1)

env = parse_env(ENV)
TOKEN = env.get("DISCORD_BOT_TOKEN", "")
GUILD = env.get("DISCORD_GUILD_ID", "")

if not TOKEN or not GUILD:
    print("❌ Missing DISCORD_BOT_TOKEN or DISCORD_GUILD_ID in discord.env")
    exit(1)

FAILURES = []  # (what, detail) — reported honestly at the end

HEADERS = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "LindaAI-Setup/1.0"
}

def api(method, path, data=None):
    url = f"https://discord.com/api/v10{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"  ⚠️  {method} {path} → {e.code}: {err[:200]}")
        FAILURES.append((f"{method} {path}", f"{e.code}: {err[:200]}"))
        return None

def get_guild_channels():
    return api("GET", f"/guilds/{GUILD}/channels") or []

def find_category(channels, name):
    name_clean = name.lower().replace(" ", "").replace("-", "")
    for c in channels:
        if c["type"] == 4:
            c_clean = c["name"].lower().replace(" ", "").replace("-", "")
            if c_clean == name_clean:
                return c
    return None

def find_channel(channels, name, parent_id=None):
    name_clean = name.lower().replace(" ", "").replace("-", "")
    for c in channels:
        c_clean = c["name"].lower().replace(" ", "").replace("-", "")
        if c_clean == name_clean:
            if parent_id is None or c.get("parent_id") == parent_id:
                return c
    return None

def create_category(name):
    print(f"  📁 Creating category: {name}")
    return api("POST", f"/guilds/{GUILD}/channels", {"name": name, "type": 4})

def create_forum(name, parent_id, tags):
    print(f"  📋 Creating forum: #{name}")
    tag_objs = [{"name": t, "moderated": False} for t in tags]
    result = api("POST", f"/guilds/{GUILD}/channels", {
        "name": name,
        "type": 15,  # GUILD_FORUM
        "parent_id": parent_id,
        "available_tags": tag_objs
    })
    if result is None:
        # Forum channels require a Community-enabled server. Fall back to a
        # plain text channel so the layout (and bot matching) still works.
        print(f"  ↪️  Forum failed (server may not have Community enabled) — "
              f"creating #{name} as a TEXT channel instead. To get forums+tags: "
              f"Server Settings → Enable Community, then re-run this script.")
        return create_text(name, parent_id)
    return result

def create_text(name, parent_id):
    print(f"  💬 Creating text channel: #{name}")
    return api("POST", f"/guilds/{GUILD}/channels", {
        "name": name,
        "type": 0,
        "parent_id": parent_id
    })

DEAL_TAGS = ["💵 Cash", "🔨 Fix & Flip", "📄 Seller Finance", "🔁 BRRRR", "🤝 Subject-To", "📦 Wholesale"]

print("🏗️  LindaAI Discord Channel Setup")
print(f"   Guild: {GUILD}\n")

channels = get_guild_channels()

# ── DEALS (the Sauce Underwriter lives here) ──
print("🏠  Deals")
cat = find_category(channels, "deals") or find_category(channels, "real estate")
if cat:
    print(f"  ✅ Category exists: {cat['name']} ({cat['id']})")
else:
    cat = create_category("Deals")
    time.sleep(0.5)
    channels = get_guild_channels()

if cat:
    if find_channel(channels, "deals", cat["id"]):
        print("  ✅ #deals already exists")
    else:
        create_forum("deals", cat["id"], DEAL_TAGS)
        time.sleep(0.5)

# ── LINDA AI ──
print("\n💼  Linda AI")
channels = get_guild_channels()
la_cat = find_category(channels, "linda ai")
if la_cat:
    print(f"  ✅ Category exists: {la_cat['name']} ({la_cat['id']})")
else:
    la_cat = create_category("Linda AI")
    time.sleep(0.5)
    channels = get_guild_channels()

if la_cat:
    channels = get_guild_channels()
    if not find_channel(channels, "linda-ai", la_cat["id"]):
        create_text("linda-ai", la_cat["id"])
    else:
        print("  ✅ #linda-ai already exists")

if FAILURES:
    print(f"\n⚠️  Finished with {len(FAILURES)} API failure(s):")
    for what, detail in FAILURES:
        print(f"   - {what}: {detail}")
    print("   Fix the cause (permissions? Community not enabled?) and re-run — "
          "the script skips anything that already exists.")
else:
    print("\n✅ Done! Open Discord: paste an address in a #deals post or run /underwrite.")
