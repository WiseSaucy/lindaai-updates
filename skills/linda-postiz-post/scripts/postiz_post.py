#!/usr/bin/env python3
"""
postiz_post.py — LindaAI · linda-postiz-post

Auto-schedules a finished content pack across all connected Postiz channels
at per-platform optimal LOCAL times (customer timezone). Reads creds from
~/.lindaai/postiz.json
and captions from PUBLISH_PACK.md.

Usage:
  python3 postiz_post.py --project /path/to/pack
  python3 postiz_post.py --pack-name "my-first-reel"
  python3 postiz_post.py --project /path/to/pack --platforms tiktok,instagram --schedule-mode now
  python3 postiz_post.py --project /path/to/pack --dry-run    # build plan, no API writes

Built by Daniel Wise · LindaAI · support@send.lindaai-brain.com
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

HOME = Path.home()
POSTIZ_CREDS = HOME / ".lindaai" / "postiz.json"
HISTORY = HOME / ".lindaai" / "postiz-history.jsonl"

# Customer's local timezone — from client.json "timezone" (IANA name) if set,
# otherwise the machine's system timezone. Never a hardcoded zone.
def _local_tz():
    cfg = HOME / ".lindaai" / "client.json"
    try:
        tzname = json.loads(cfg.read_text()).get("timezone")
        if tzname:
            from zoneinfo import ZoneInfo
            return ZoneInfo(tzname)
    except Exception:
        pass
    return datetime.now().astimezone().tzinfo

LOCAL_TZ = _local_tz()

PLATFORM_TIMES_LOCAL = {
    "tiktok":       (20, 23),
    "instagram":    (20, 47),
    "facebook":     (19, 33),
    "youtube":      (18, 17),
    "youtube-long": "weekend-morning",  # Special: next Saturday 10:00 AM local
    "x":            (13, 43),
}

POSTIZ_IDENTIFIER = {
    "tiktok":       "tiktok",
    "instagram":    "instagram-standalone",
    "facebook":     "facebook",
    "youtube":      "youtube",
    "youtube-long": "youtube",  # Same YT integration
    "x":            "x",
}

# Order matters — more specific keys first so "youtube long-form" matches before plain "youtube"
HEADING_KEYWORDS = {
    "youtube-long": ["youtube long-form", "youtube long form", "long-form"],
    "youtube":      ["youtube shorts", "youtube"],
    "tiktok":       ["tiktok"],
    "instagram":    ["instagram"],
    "facebook":     ["facebook"],
    "x":            ["twitter/x", "twitter", " x ", "/x"],
}

MEDIA_PRIMARY = {
    "tiktok":    ["TIKTOK.mp4"],
    "instagram": ["IG.mp4", "INSTAGRAM.mp4", "FB-IG.mp4"],
    "facebook":  ["FB.mp4", "FACEBOOK.mp4", "FB-IG.mp4"],
    "youtube":   ["YOUTUBE.mp4"],
    "x":         ["TWITTER.mp4", "X.mp4"],
}
MEDIA_FALLBACK = ["TIKTOK.mp4", "master.mp4"]


def resolve_archive_media(pack_dir):
    """For youtube-long: find the longest video in archive/ folder."""
    archive = pack_dir / "archive"
    if not archive.is_dir():
        return None
    candidates = list(archive.glob("*.mp4"))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_size)


def next_weekend_morning_utc():
    """Next Saturday 10:00 AM local time, in UTC."""
    now_local = datetime.now(LOCAL_TZ)
    days_until_saturday = (5 - now_local.weekday()) % 7  # Saturday is weekday 5
    if days_until_saturday == 0 and now_local.hour >= 10:
        days_until_saturday = 7
    target = now_local.replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=days_until_saturday)
    return target.astimezone(timezone.utc)

def _search_dirs():
    """Content folder comes from the customer's config (client.json
    'content_dir'), never a hardcoded personal path. Falls back to cwd."""
    dirs = []
    cfg = HOME / ".lindaai" / "client.json"
    try:
        content_dir = json.loads(cfg.read_text()).get("content_dir")
        if content_dir:
            dirs.append(Path(content_dir).expanduser())
    except Exception:
        pass
    dirs.append(Path.cwd())
    return dirs

SEARCH_DIRS = _search_dirs()


def die(msg, code=1):
    print(f"📣 Holler — {msg}", file=sys.stderr)
    sys.exit(code)


def load_creds():
    if not POSTIZ_CREDS.exists():
        die("No Postiz creds at ~/.lindaai/postiz.json. Hook up Postiz first.")
    creds = json.loads(POSTIZ_CREDS.read_text())
    if not creds.get("api_url") or not creds.get("api_key"):
        die("postiz.json is missing api_url or api_key.")
    return creds


def resolve_pack(project, pack_name):
    if project:
        p = Path(project).expanduser().resolve()
        if not p.is_dir():
            die(f"Project folder not found: {p}")
        return p
    if not pack_name:
        die("Provide --project or --pack-name.")
    matches = []
    needle = pack_name.lower()
    for root in SEARCH_DIRS:
        if not root.exists():
            continue
        for pack_md in root.rglob("PUBLISH_PACK.md"):
            folder = pack_md.parent
            if needle in folder.name.lower():
                matches.append(folder)
    if not matches:
        die(f"No content pack matching '{pack_name}'. Searched: {[str(d) for d in SEARCH_DIRS]}. Set content_dir in ~/.lindaai/client.json to point me at your content folder.")
    matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    if len(matches) > 1:
        print(f"📣 Holler — Multiple packs matched '{pack_name}':")
        for i, m in enumerate(matches, 1):
            print(f"  {i}. {m}")
        print(f"Using newest: {matches[0]}")
    return matches[0]


def parse_captions(pack_md_path):
    text = pack_md_path.read_text()
    sections = {}
    lines = text.split("\n")
    current_platform = None
    current_lines = []

    def commit():
        if current_platform and current_lines:
            body = "\n".join(current_lines).strip()
            body = re.sub(r"^```\s*$", "", body, flags=re.M)
            body = re.sub(r"\n\*\*Pin comment:\*\*.*$", "", body, flags=re.S)
            sections[current_platform] = body.strip()

    for line in lines:
        if line.startswith("### "):
            commit()
            heading = line[4:].lower()
            current_platform = None
            current_lines = []
            for plat, kws in HEADING_KEYWORDS.items():
                if plat in sections:
                    continue
                if any(kw in heading for kw in kws):
                    current_platform = plat
                    break
        elif current_platform:
            current_lines.append(line)
    commit()

    # Trim Twitter to 280
    if "x" in sections and len(sections["x"]) > 280:
        sections["x"] = sections["x"][:277].rstrip() + "..."
    return sections


def resolve_media(platform, pack_dir):
    if platform == "youtube-long":
        return resolve_archive_media(pack_dir)
    candidates = MEDIA_PRIMARY[platform] + MEDIA_FALLBACK
    for name in candidates:
        p = pack_dir / name
        if p.is_file():
            return p
    return None


def next_slot_utc(platform):
    slot_def = PLATFORM_TIMES_LOCAL[platform]
    if slot_def == "weekend-morning":
        return next_weekend_morning_utc()
    h, m = slot_def
    now_local = datetime.now(LOCAL_TZ)
    slot = now_local.replace(hour=h, minute=m, second=0, microsecond=0)
    if slot <= now_local:
        slot += timedelta(days=1)
    return slot.astimezone(timezone.utc)


def fmt_iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def curl_run(args):
    full = ["curl", "-sS", "-w", "\n__HTTP_CODE__:%{http_code}"] + args
    r = subprocess.run(full, capture_output=True, text=True)
    out = r.stdout
    code = 0
    if "__HTTP_CODE__:" in out:
        body, _, tail = out.rpartition("__HTTP_CODE__:")
        try:
            code = int(tail.strip())
        except ValueError:
            code = 0
    else:
        body = out
    return code, body.rstrip()


def fetch_integrations(api_url, api_key):
    code, body = curl_run(["-H", f"Authorization: {api_key}", f"{api_url}/integrations"])
    if code != 200:
        die(f"GET /integrations returned {code}: {body}")
    return json.loads(body)


def upload_file(api_url, api_key, file_path):
    code, body = curl_run([
        "-X", "POST",
        "-H", f"Authorization: {api_key}",
        "-F", f"file=@{file_path}",
        f"{api_url}/upload",
    ])
    if code not in (200, 201):
        die(f"Upload of {file_path.name} returned {code}: {body}")
    return json.loads(body)


def build_settings(identifier, caption):
    """Return platform-specific settings block (Postiz requires `__type` + per-platform fields)."""
    base = {"__type": identifier}
    if identifier == "tiktok":
        base.update({
            "privacy_level": "PUBLIC_TO_EVERYONE",
            "duet": True,        # allow duets (engagement)
            "stitch": True,      # allow stitches (engagement)
            "comment": True,     # allow comments (engagement)
            "autoAddMusic": "no",
            "content_posting_method": "DIRECT_POST",
            "brand_content_toggle": False,
            "brand_organic_toggle": False,
            "title": (caption.strip().split("\n", 1)[0])[:90] or "Post",
        })
    elif identifier == "instagram-standalone":
        base.update({"post_type": "post", "collaborators": []})
    elif identifier == "youtube":
        first_line = caption.strip().split("\n", 1)[0][:95] or "Untitled"
        base.update({
            "title": first_line,
            "type": "public",
            "tags": [],
            "category": "22",  # People & Blogs (YouTube category id)
        })
    elif identifier == "x":
        base.update({"who_can_reply_post": "everyone"})
    return base


def schedule_post(api_url, api_key, integration_id, identifier, caption, media_obj, when_utc, mode):
    payload = {
        "type": mode,
        "date": fmt_iso(when_utc),
        "shortLink": False,
        "tags": [],
        "posts": [
            {
                "integration": {"id": integration_id},
                "value": [
                    {
                        "content": caption,
                        "image": [media_obj] if media_obj else [],
                    }
                ],
                "settings": build_settings(identifier, caption),
            }
        ],
    }
    code, body = curl_run([
        "-X", "POST",
        "-H", f"Authorization: {api_key}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload),
        f"{api_url}/posts",
    ])
    return code, body


def reset_pack_history(api_url, api_key, pack_name):
    """Delete previously-queued posts for this pack (using IDs from ~/.lindaai/postiz-history.jsonl)."""
    if not HISTORY.exists():
        return 0
    to_delete = []
    keep_lines = []
    for line in HISTORY.read_text().splitlines():
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            keep_lines.append(line)
            continue
        if rec.get("project") == pack_name:
            for plat, info in (rec.get("results") or {}).items():
                pid = info.get("id")
                if pid and pid != "?":
                    to_delete.append((plat, pid))
        else:
            keep_lines.append(line)
    deleted = 0
    for plat, pid in to_delete:
        # Try REST-style first, then action-style
        for url in [f"{api_url}/posts/{pid}", f"{api_url}/posts/delete?id={pid}"]:
            code, _ = curl_run(["-X", "DELETE", "-H", f"Authorization: {api_key}", url])
            if code in (200, 204, 404):  # 404 = already deleted, treat as success
                deleted += 1
                break
        else:
            print(f"  ⚠ Could not delete {plat} post {pid}")
    # Rewrite history minus the deleted entries
    HISTORY.write_text("\n".join(keep_lines) + ("\n" if keep_lines else ""))
    return deleted


def parse_post_id(resp):
    """Postiz returns success as either a dict or list. Be liberal."""
    try:
        parsed = json.loads(resp)
    except json.JSONDecodeError:
        return "?"
    if isinstance(parsed, list):
        if parsed and isinstance(parsed[0], dict):
            return parsed[0].get("id") or parsed[0].get("postId") or "?"
        return "?"
    if isinstance(parsed, dict):
        if "id" in parsed:
            return parsed["id"]
        posts = parsed.get("posts") or []
        if posts and isinstance(posts[0], dict):
            return posts[0].get("id", "?")
    return "?"


def main():
    ap = argparse.ArgumentParser(description="LindaAI · Schedule a content pack via Postiz Cloud API.")
    ap.add_argument("--project", help="Absolute path to a content pack folder")
    ap.add_argument("--pack-name", help="Fuzzy pack name to search for")
    ap.add_argument("--platforms", default="all", help="Comma list: tiktok,instagram,facebook,youtube,x (or 'all')")
    ap.add_argument("--schedule-mode", default="auto", help="'auto' (per-platform local optimal), 'now', or ISO 8601 timestamp")
    ap.add_argument("--dry-run", action="store_true", help="Build the plan, don't call the API")
    ap.add_argument("--yes", action="store_true", help="Skip the interactive go-gate (still NOT recommended; the gate exists for safety)")
    ap.add_argument("--no-youtube-long", action="store_true", help="Skip auto-detection of YouTube long-form (archive/*.mp4 + long-form caption)")
    ap.add_argument("--reset", action="store_true", help="Delete previously scheduled posts for this pack (from history) before rescheduling")
    args = ap.parse_args()

    creds = load_creds()
    api_url = creds["api_url"].rstrip("/")
    api_key = creds["api_key"]

    pack = resolve_pack(args.project, args.pack_name)
    pack_md = pack / "PUBLISH_PACK.md"
    if not pack_md.exists():
        die(f"No PUBLISH_PACK.md in {pack}. Run your content pipeline first.")

    captions = parse_captions(pack_md)
    if args.platforms == "all":
        plat_list = [p for p in PLATFORM_TIMES_LOCAL.keys() if p != "youtube-long"]
        # Auto-add youtube-long if pack supports it
        if not args.no_youtube_long and "youtube-long" in captions and resolve_archive_media(pack) is not None:
            plat_list.append("youtube-long")
    else:
        plat_list = [p.strip().lower() for p in args.platforms.split(",") if p.strip()]

    if args.reset:
        deleted = reset_pack_history(api_url, api_key, pack.name)
        if deleted:
            print(f"🧹 Reset: deleted {deleted} previously-queued posts for this pack.\n")

    print(f"📣 Holler — Postiz schedule plan for \"{pack.name}\":\n")

    integrations = fetch_integrations(api_url, api_key)
    ident_to_int = {i["identifier"]: i for i in integrations}

    plan = []
    warnings = []
    for plat in plat_list:
        identifier = POSTIZ_IDENTIFIER.get(plat)
        if not identifier:
            warnings.append(f"Unknown platform '{plat}' — skipping")
            continue
        integ = ident_to_int.get(identifier)
        if not integ:
            warnings.append(f"{plat}: no Postiz integration ({identifier}) — skipping")
            continue
        if plat not in captions:
            if plat == "x" and "tiktok" in captions:
                captions[plat] = captions["tiktok"][:277].rstrip() + "..."
                warnings.append(f"{plat}: no caption in PUBLISH_PACK.md — fell back to trimmed TikTok caption")
            else:
                warnings.append(f"{plat}: no caption in PUBLISH_PACK.md — skipping")
                continue
        media = resolve_media(plat, pack)
        if not media:
            warnings.append(f"{plat}: no usable MP4 — skipping")
            continue
        if args.schedule_mode == "auto":
            when = next_slot_utc(plat)
            mode = "schedule"
        elif args.schedule_mode == "now":
            when = datetime.now(timezone.utc)
            mode = "now"
        else:
            try:
                when = datetime.fromisoformat(args.schedule_mode.replace("Z", "+00:00")).astimezone(timezone.utc)
                mode = "schedule"
            except ValueError:
                die(f"Bad --schedule-mode value: {args.schedule_mode}")
        plan.append({
            "platform": plat,
            "integration": integ,
            "identifier": identifier,
            "caption": captions[plat],
            "media": media,
            "when_utc": when,
            "mode": mode,
        })
        when_local = when.astimezone(LOCAL_TZ)
        when_str = when_local.strftime("%-I:%M %p (%a %m/%d)")
        print(f"  ✓ {plat:<10} → {integ.get('name','?'):<40} → {when_str} → {media.name}")

    if warnings:
        print("\n⚠ Warnings:")
        for w in warnings:
            print(f"  - {w}")

    if not plan:
        die("No platforms to post to. Halting.")

    if args.dry_run:
        print(f"\n📣 Holler — Dry run complete. {len(plan)} posts planned, no API writes.")
        return

    if not args.yes:
        print(f"\n📣 Holler — {len(plan)} posts above will be queued in Postiz against your LIVE social accounts.")
        print("Type 'go' to confirm and fire. Anything else aborts.")
        try:
            answer = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            answer = ""
        if answer != "go":
            print("📣 Holler — Aborted. Nothing was published.")
            return

    print(f"\n📤 Uploading media to Postiz...")
    upload_cache = {}
    for item in plan:
        m = item["media"]
        if m not in upload_cache:
            print(f"  ↗ {m.name}")
            upload_cache[m] = upload_file(api_url, api_key, m)
        item["media_obj"] = upload_cache[m]

    print(f"\n📅 Scheduling posts...")
    results = {}
    for item in plan:
        status, resp = schedule_post(
            api_url, api_key,
            item["integration"]["id"], item["identifier"],
            item["caption"], item["media_obj"],
            item["when_utc"], item["mode"],
        )
        if status in (200, 201):
            rid = parse_post_id(resp)
            when_local = item["when_utc"].astimezone(LOCAL_TZ).strftime("%-I:%M %p")
            print(f"  ✅ {item['platform']:<10} @ {when_local} (id: {rid})")
            results[item["platform"]] = {"id": rid, "status": "ok"}
        else:
            print(f"  ❌ {item['platform']:<10} FAILED ({status}): {resp[:300]}")
            results[item["platform"]] = {"status": "fail", "error": resp[:300]}

    record = {
        "project": pack.name,
        "scheduled_at": datetime.now(LOCAL_TZ).isoformat(),
        "platforms": [p["platform"] for p in plan],
        "results": results,
        "mode": args.schedule_mode,
    }
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    with HISTORY.open("a") as f:
        f.write(json.dumps(record) + "\n")

    print(f"\n📣 Holler — Yeeee Hawww! 🤠 Logged to {HISTORY}")
    print(f"View queue: https://platform.postiz.com/launches")


if __name__ == "__main__":
    main()
