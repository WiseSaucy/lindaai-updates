#!/usr/bin/env python3
"""
LindaAI Discord backup — exports every forum post (active + archived threads,
with all comments) and text-channel history to markdown files, so Discord is
never your only copy of deal files, client pipelines, and decisions.

Run weekly (manually, or via a launchd/cron job):
  python3 export_server.py                 # writes to ~/lindaai-discord-backup/<date>/
  python3 export_server.py /path/to/dir    # custom destination

Files are named by channel and post title (titles carry your addresses and
IDs, so the archive stays greppable offline). Point the destination at a
private Drive-synced folder or a git repo for versioned, off-Discord copies.

© 2026 LindaAI — Built by Daniel Wise
"""
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
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
    print(f"❌ {ENV} not found."); sys.exit(1)
env = parse_env(ENV)
TOKEN, GUILD = env.get("DISCORD_BOT_TOKEN", ""), env.get("DISCORD_GUILD_ID", "")
if not TOKEN or not GUILD:
    print("❌ Missing DISCORD_BOT_TOKEN or DISCORD_GUILD_ID"); sys.exit(1)

DEST = Path(sys.argv[1]) if len(sys.argv) > 1 else \
    Path.home() / "lindaai-discord-backup" / datetime.now().strftime("%Y-%m-%d")
HEADERS = {"Authorization": f"Bot {TOKEN}", "User-Agent": "LindaAI-Backup/1.0"}


def api(path):
    req = urllib.request.Request(f"https://discord.com/api/v10{path}", headers=HEADERS)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = float(json.loads(e.read()).get("retry_after", 2))
                time.sleep(wait + 0.5)
                continue
            return None
    return None


def safe(name):
    return re.sub(r"[^\w\-. ]+", "_", name).strip()[:120] or "untitled"


def messages(channel_id, cap=4000):
    out, before = [], None
    while len(out) < cap:
        q = f"/channels/{channel_id}/messages?limit=100" + (f"&before={before}" if before else "")
        batch = api(q)
        if not batch:
            break
        out.extend(batch)
        if len(batch) < 100:
            break
        before = batch[-1]["id"]
        time.sleep(0.35)
    return list(reversed(out))


def write_md(path, title, msgs):
    lines = [f"# {title}", f"_Exported {datetime.now(timezone.utc).isoformat(timespec='minutes')}_", ""]
    for m in msgs:
        who = m.get("author", {}).get("username", "?")
        ts = (m.get("timestamp") or "")[:16].replace("T", " ")
        lines.append(f"**{who}** · {ts}")
        if m.get("content"):
            lines.append(m["content"])
        for a in m.get("attachments", []):
            lines.append(f"[attachment: {a.get('filename')}]({a.get('url')})")
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


channels = api(f"/guilds/{GUILD}/channels") or []
active = api(f"/guilds/{GUILD}/threads/active") or {}
active_by_parent = {}
for t in active.get("threads", []):
    active_by_parent.setdefault(t.get("parent_id"), []).append(t)

n_files = 0
for ch in channels:
    cname = safe(ch["name"])
    if ch["type"] == 15:  # forum: every post is a thread
        threads = list(active_by_parent.get(ch["id"], []))
        arch = api(f"/channels/{ch['id']}/threads/archived/public?limit=100") or {}
        threads += arch.get("threads", [])
        for t in threads:
            msgs = messages(t["id"])
            if msgs:
                write_md(DEST / cname / f"{safe(t['name'])}.md", t["name"], msgs)
                n_files += 1
        print(f"  📦 #{ch['name']}: {len(threads)} posts")
    elif ch["type"] == 0:  # text channel
        msgs = messages(ch["id"], cap=2000)
        if msgs:
            write_md(DEST / f"{cname}.md", f"#{ch['name']}", msgs)
            n_files += 1
        threads = list(active_by_parent.get(ch["id"], []))
        for t in threads:
            tmsgs = messages(t["id"])
            if tmsgs:
                write_md(DEST / cname / f"{safe(t['name'])}.md", t["name"], tmsgs)
                n_files += 1
        print(f"  📦 #{ch['name']}: channel + {len(threads)} threads")

print(f"\n✅ Backup complete → {DEST}  ({n_files} markdown files)")
print("   Tip: point this at a Drive-synced folder, or `git init` it for versioned history.")
