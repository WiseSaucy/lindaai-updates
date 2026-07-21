#!/usr/bin/env python3
"""
LindaAI Discord org tool — applies an organization spec (categories, channels,
forums, tag MERGES, guidelines/topics, pinned posts, renames, moves, roles)
to your server. Pairs with setup_channels.py; use this for evolving a server
that already has channels and live posts.

SAFE BY DESIGN
  * Dry-run by DEFAULT: prints the full plan, changes nothing. Add --apply to execute.
  * Tags are MERGED by name into a forum's existing tags — never replaced —
    (Discord PATCH replaces the whole tag array, which would strip omitted tags
    from every live post; this tool always sends existing + new, and enforces
    Discord's 20-tag cap before any write).
  * Permission changes are ADDITIVE — existing overwrites are preserved.
  * Idempotent — anything that already exists is skipped; safe to re-run.

USAGE
  python3 org_apply.py my-spec.json            # dry run (plan only)
  python3 org_apply.py my-spec.json --apply    # execute

SPEC = JSON list of ops, executed in order:
  {"op":"category",        "name":"Deals"}
  {"op":"archive_category","name":"zz-archive"}                    # +deny Send for @everyone
  {"op":"text",  "name":"briefs", "category":"Linda AI", "topic":"..."}
  {"op":"forum", "name":"buyers", "category":"Deals", "tags":["💵 Cash"], "topic":"..."}
  {"op":"tags",  "channel":"sfh", "add":["🆕 New","💀 Dead"]}       # MERGE into existing
  {"op":"topic", "channel":"red-sauce", "text":"..."}               # forum topic = post guidelines
  {"op":"rename","from":"gc", "to":"tg-gc"}
  {"op":"move",  "channel":"content-alerts", "category":"Linda AI"}
  {"op":"forum_pin","forum":"tg-wip","title":"📌 START HERE","body":"..."}   # pinned forum post
  {"op":"text_pin", "channel":"mgl-general","body":"..."}                    # pinned message
  {"op":"role",     "name":"truegrit"}
  {"op":"role_view","category":"TrueGrit Flip","role":"truegrit"}   # role can View category

© 2026 LindaAI — Built by Daniel Wise
"""
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ENV = Path.home() / ".claude/lindaai/discord.env"
VIEW_CHANNEL = 1 << 10   # 1024
SEND_MESSAGES = 1 << 11  # 2048
PINNED_THREAD_FLAG = 1 << 1

APPLY = "--apply" in sys.argv
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
if not ARGS:
    print(__doc__)
    sys.exit(1)
SPEC_PATH = Path(ARGS[0])


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
    print(f"❌ {ENV} not found."); sys.exit(1)
env = parse_env(ENV)
TOKEN, GUILD = env.get("DISCORD_BOT_TOKEN", ""), env.get("DISCORD_GUILD_ID", "")
if not TOKEN or not GUILD:
    print("❌ Missing DISCORD_BOT_TOKEN or DISCORD_GUILD_ID in discord.env"); sys.exit(1)

HEADERS = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json",
           "User-Agent": "LindaAI-Org/1.0"}
FAILURES = []


def api(method, path, data=None, quiet=False):
    payload = json.dumps(data).encode() if data is not None else None
    detail = ""
    for _ in range(6):
        req = urllib.request.Request(f"https://discord.com/api/v10{path}",
                                     data=payload, headers=HEADERS, method=method)
        try:
            with urllib.request.urlopen(req) as r:
                body = r.read()
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as e:
            detail = e.read().decode()[:300]
            if e.code == 429:  # rate limited — wait exactly as long as Discord asks, retry
                try:
                    wait = float(json.loads(detail).get("retry_after", 2))
                except Exception:
                    wait = 2.0
                time.sleep(wait + 0.5)
                continue
            break
    if not quiet:
        print(f"  ⚠️  {method} {path} → {detail or 'failed after retries'}")
        FAILURES.append((f"{method} {path}", detail or "failed after retries"))
    return None


def norm(s):
    return (s or "").lower().replace(" ", "").replace("-", "").replace("_", "")


def refresh():
    global CHANNELS, ROLES
    CHANNELS = api("GET", f"/guilds/{GUILD}/channels") or []
    ROLES = api("GET", f"/guilds/{GUILD}/roles") or []


def find_channel(name, types=None, parent_id=None):
    for c in CHANNELS:
        if norm(c["name"]) == norm(name):
            if types and c["type"] not in types:
                continue
            if parent_id and c.get("parent_id") != parent_id:
                continue
            return c
    return None


def find_role(name):
    return next((r for r in ROLES if norm(r["name"]) == norm(name)), None)


def everyone_role_id():
    return GUILD  # @everyone role id == guild id


def act(msg):
    print(("PLAN: " if not APPLY else "  ✅ ") + msg)


def do(method, path, data):
    if APPLY:
        out = api(method, path, data)
        time.sleep(0.45)
        return out
    return {}


def ensure_category(name, archive=False):
    cat = find_channel(name, types=[4])
    if cat:
        print(f"  ✓ category exists: {cat['name']}")
        return cat
    act(f"create category '{name}'" + (" (send-muted archive)" if archive else ""))
    payload = {"name": name, "type": 4}
    if archive:
        payload["permission_overwrites"] = [
            {"id": everyone_role_id(), "type": 0, "allow": "0", "deny": str(SEND_MESSAGES)}]
    made = do("POST", f"/guilds/{GUILD}/channels", payload)
    if APPLY:
        refresh()
    return made or {"id": None, "name": name}


def ensure_channel(kind, name, category=None, tags=None, topic=None):
    parent = find_channel(category, types=[4]) if category else None
    if category and not parent and APPLY:
        print(f"  ⚠️  category '{category}' not found for #{name}"); return None
    ch = find_channel(name, types=[0, 15])
    if ch:
        print(f"  ✓ #{name} exists")
        if tags:
            merge_tags(name, tags)
        if topic is not None:
            ensure_topic(name, topic)
        return ch
    act(f"create {'forum' if kind == 15 else 'text'} #{name}"
        + (f" under '{category}'" if category else "")
        + (f" with {len(tags)} tags" if tags else ""))
    payload = {"name": name, "type": kind}
    if parent:
        payload["parent_id"] = parent["id"]
    if topic:
        payload["topic"] = topic[:1024]
    if kind == 15 and tags:
        payload["available_tags"] = [{"name": t[:20], "moderated": False} for t in tags[:20]]
    made = do("POST", f"/guilds/{GUILD}/channels", payload)
    if APPLY:
        refresh()
    return made


def _tagkey(s):
    # Discord moves a leading emoji into the tag's icon slot and stores the
    # name without it — so compare from the first LETTER onward ("🆕 New" ==
    # "New", and keycap emojis like 1️⃣ don't leak their digit into the key).
    s = s or ""
    m = re.search(r"[A-Za-z].*", s)
    s = m.group(0) if m else s
    return re.sub(r"[^0-9a-z]+", "", s.lower())


def merge_tags(channel_name, add):
    ch = find_channel(channel_name, types=[15])
    if not ch:
        print(f"  ⚠️  forum #{channel_name} not found — skipping tag merge")
        return
    live = api("GET", f"/channels/{ch['id']}") or ch
    existing = live.get("available_tags", []) or []
    have = {_tagkey(t["name"]) for t in existing}
    new = []
    for t in add:
        k = _tagkey(t)
        if k not in have:
            have.add(k)
            new.append(t)
    if not new:
        print(f"  ✓ #{channel_name}: all {len(add)} tags already present")
        return
    merged = existing + [{"name": t[:20], "moderated": False} for t in new]
    if len(merged) > 20:
        print(f"  ❌ #{channel_name}: merge would give {len(merged)} tags (cap 20) — NOT applied. "
              f"Remove some tags first."); return
    act(f"#{channel_name}: MERGE tags {new} (keeps existing {len(existing)}, total {len(merged)})")
    do("PATCH", f"/channels/{ch['id']}", {"available_tags": merged})


def ensure_topic(channel_name, text):
    ch = find_channel(channel_name, types=[0, 15])
    if not ch:
        print(f"  ⚠️  #{channel_name} not found — skipping topic"); return
    live = api("GET", f"/channels/{ch['id']}") or ch
    if (live.get("topic") or "").strip() == text.strip():
        print(f"  ✓ #{channel_name}: topic/guidelines already set")
        return
    act(f"#{channel_name}: set topic/guidelines ({len(text)} chars)")
    do("PATCH", f"/channels/{ch['id']}", {"topic": text[:1024]})


def rename(old, new):
    if find_channel(new):
        print(f"  ✓ #{new} already exists (rename done or unneeded)"); return
    ch = find_channel(old)
    if not ch:
        print(f"  ⚠️  #{old} not found — skipping rename"); return
    act(f"rename #{old} → #{new}")
    do("PATCH", f"/channels/{ch['id']}", {"name": new})
    if APPLY:
        refresh()


def move(channel_name, category):
    ch = find_channel(channel_name)
    cat = find_channel(category, types=[4])
    if not ch or not cat:
        print(f"  ⚠️  move: #{channel_name} or '{category}' not found"); return
    if ch.get("parent_id") == cat["id"]:
        print(f"  ✓ #{channel_name} already under '{category}'"); return
    act(f"move #{channel_name} under '{category}'")
    do("PATCH", f"/channels/{ch['id']}", {"parent_id": cat["id"]})


def _forum_thread_names(forum_id):
    names = set()
    active = api("GET", f"/guilds/{GUILD}/threads/active", quiet=True) or {}
    for t in active.get("threads", []):
        if t.get("parent_id") == forum_id:
            names.add(norm(t["name"]))
    arch = api("GET", f"/channels/{forum_id}/threads/archived/public?limit=100", quiet=True) or {}
    for t in arch.get("threads", []):
        names.add(norm(t["name"]))
    return names


def forum_pin(forum_name, title, body):
    ch = find_channel(forum_name, types=[15])
    if not ch:
        print(f"  ⚠️  forum #{forum_name} not found — skipping pin '{title}'"); return
    if norm(title) in _forum_thread_names(ch["id"]):
        print(f"  ✓ #{forum_name}: post '{title}' already exists"); return
    act(f"#{forum_name}: create + pin post '{title}'")
    thread = do("POST", f"/channels/{ch['id']}/threads",
                {"name": title[:100], "message": {"content": body[:2000]}})
    if APPLY and thread and thread.get("id"):
        do("PATCH", f"/channels/{thread['id']}", {"flags": PINNED_THREAD_FLAG})


def text_pin(channel_name, body):
    ch = find_channel(channel_name, types=[0])
    if not ch:
        print(f"  ⚠️  #{channel_name} not found — skipping pin"); return
    pins = api("GET", f"/channels/{ch['id']}/pins", quiet=True) or []
    marker = body.strip().splitlines()[0]
    if any(marker in (p.get("content") or "") for p in pins):
        print(f"  ✓ #{channel_name}: pin already present"); return
    act(f"#{channel_name}: post + pin message ({len(body)} chars)")
    msg = do("POST", f"/channels/{ch['id']}/messages", {"content": body[:2000]})
    if APPLY and msg and msg.get("id"):
        do("PUT", f"/channels/{ch['id']}/pins/{msg['id']}", None)


def ensure_role(name):
    if find_role(name):
        print(f"  ✓ role @{name} exists"); return
    act(f"create role @{name}")
    do("POST", f"/guilds/{GUILD}/roles", {"name": name, "permissions": "0"})
    if APPLY:
        refresh()


def role_view(category, role_name):
    cat = find_channel(category, types=[4])
    role = find_role(role_name)
    if not cat or not role:
        print(f"  ⚠️  role_view: '{category}' or @{role_name} not found"); return
    live = api("GET", f"/channels/{cat['id']}") or cat
    overwrites = live.get("permission_overwrites", []) or []
    if any(o["id"] == role["id"] for o in overwrites):
        print(f"  ✓ '{category}': @{role_name} overwrite already present"); return
    act(f"'{category}': ADD View-allow for @{role_name} (existing overwrites preserved)")
    overwrites.append({"id": role["id"], "type": 0, "allow": str(VIEW_CHANNEL), "deny": "0"})
    do("PATCH", f"/channels/{cat['id']}", {"permission_overwrites": overwrites})


OPS = {
    "category": lambda o: ensure_category(o["name"]),
    "archive_category": lambda o: ensure_category(o["name"], archive=True),
    "text": lambda o: ensure_channel(0, o["name"], o.get("category"), None, o.get("topic")),
    "forum": lambda o: ensure_channel(15, o["name"], o.get("category"), o.get("tags"), o.get("topic")),
    "tags": lambda o: merge_tags(o["channel"], o["add"]),
    "topic": lambda o: ensure_topic(o["channel"], o["text"]),
    "rename": lambda o: rename(o["from"], o["to"]),
    "move": lambda o: move(o["channel"], o["category"]),
    "forum_pin": lambda o: forum_pin(o["forum"], o["title"], o["body"]),
    "text_pin": lambda o: text_pin(o["channel"], o["body"]),
    "role": lambda o: ensure_role(o["name"]),
    "role_view": lambda o: role_view(o["category"], o["role"]),
}

spec = json.loads(SPEC_PATH.read_text())
print(f"{'🚀 APPLYING' if APPLY else '🔍 DRY RUN (nothing will change — add --apply to execute)'} "
      f"— {len(spec)} ops from {SPEC_PATH.name}\n")
refresh()
for o in spec:
    fn = OPS.get(o.get("op"))
    if not fn:
        print(f"  ⚠️  unknown op: {o.get('op')}"); continue
    fn(o)

if FAILURES:
    print(f"\n⚠️  {len(FAILURES)} API failure(s) — fix and re-run (idempotent):")
    for what, d in FAILURES:
        print(f"   - {what}: {d}")
elif APPLY:
    print("\n✅ All ops applied. Re-run any time — it skips what exists.")
else:
    print("\n📋 Plan complete. Run again with --apply to execute.")
