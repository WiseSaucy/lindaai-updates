#!/usr/bin/env python3
"""
post_to_socials.py — Ayrshare single-API multi-platform publisher.

Usage:
    post_to_socials.py \
        --caption "Hook + value + CTA" \
        --media /path/to/file.mp4 \
        --platforms tiktok,instagram,facebook,youtube,twitter \
        [--schedule "2026-05-27T20:23:00-06:00"]   # ISO 8601 with offset
        [--profile-key <ayrshare_profile_key>]      # if multi-brand
        [--dry-run]                                  # show payload, don't send
        [--per-platform-captions path/to/PUBLISH_PACK.md]  # use platform-specific captions

Reads API key from ~/.lindaai/ayrshare.json.

© 2022-2026 Daniel Wise · LindaAI
"""
from __future__ import annotations
import argparse
import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
except ImportError:
    print("⚠️  requests not installed. Run: pip3 install --user requests", file=sys.stderr)
    sys.exit(1)


AYRSHARE_BASE = "https://app.ayrshare.com/api"
CONFIG_PATH = Path.home() / ".lindaai" / "ayrshare.json"
CACHE_DIR = Path.home() / ".lindaai" / "ayrshare-cache"
HISTORY_PATH = Path.home() / ".lindaai" / "social-history.jsonl"

# MDT (UTC-6) optimal posting times per platform
# Off-minute picks intentionally avoid :00/:30 traffic spikes.
OPTIMAL_MDT = {
    "tiktok":     {"hour": 20, "minute": 23},
    "instagram":  {"hour": 20, "minute": 47},
    "facebook":   {"hour": 19, "minute": 33},
    "youtube":    {"hour": 18, "minute": 17},
    "twitter":    {"hour": 13, "minute": 43},
}

PLATFORM_ALIASES = {
    "ig": "instagram", "insta": "instagram", "reels": "instagram",
    "fb": "facebook",
    "yt": "youtube", "shorts": "youtube",
    "x": "twitter", "tweet": "twitter",
    "tt": "tiktok",
}


def load_config() -> dict:
    if not CONFIG_PATH.is_file():
        print(
            "📣 Holler — Ayrshare config not found.\n\n"
            f"  Missing file: {CONFIG_PATH}\n\n"
            "  Steps:\n"
            "    1. Sign up at https://www.ayrshare.com\n"
            "    2. Connect your social accounts\n"
            "    3. Copy your API key from Settings → API Keys\n"
            f"    4. Save it: mkdir -p ~/.lindaai && echo '{{\"api_key\":\"PASTE_HERE\"}}' > {CONFIG_PATH}\n",
            file=sys.stderr,
        )
        sys.exit(2)
    with open(CONFIG_PATH) as f:
        return json.load(f)


def normalize_platforms(raw: str) -> list[str]:
    """Comma-list (case/alias-tolerant) -> canonical Ayrshare platform names."""
    out = []
    for p in raw.split(","):
        p = p.strip().lower()
        if not p:
            continue
        p = PLATFORM_ALIASES.get(p, p)
        if p in OPTIMAL_MDT:
            out.append(p)
        else:
            print(f"⚠️  Unknown platform '{p}' — skipping", file=sys.stderr)
    return out


def default_schedule_for(platform: str) -> str:
    """ISO 8601 with -06:00 MDT offset, today's optimal slot (or tomorrow if past)."""
    now = datetime.now()
    pick = OPTIMAL_MDT[platform]
    target = now.replace(hour=pick["hour"], minute=pick["minute"], second=0, microsecond=0)
    if target <= now:
        target = target + timedelta(days=1)
    # Format with explicit MDT offset
    return target.strftime("%Y-%m-%dT%H:%M:%S-06:00")


def upload_media(media_path: Path, api_key: str) -> str:
    """Upload media file to Ayrshare → returns the media URL.

    Uses simple stat-based cache: same path + size + mtime → reuse URL.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    stat = media_path.stat()
    cache_key = f"{media_path.name}_{stat.st_size}_{int(stat.st_mtime)}"
    cache_file = CACHE_DIR / f"{cache_key}.url"
    if cache_file.is_file():
        return cache_file.read_text().strip()

    print(f"  Uploading {media_path.name} ({stat.st_size // 1024 // 1024} MB)...", file=sys.stderr)
    with open(media_path, "rb") as f:
        r = requests.post(
            f"{AYRSHARE_BASE}/media/upload",
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": (media_path.name, f, "video/mp4" if media_path.suffix.lower() == ".mp4" else None)},
            timeout=300,
        )
    if r.status_code != 200:
        print(f"❌ Media upload failed ({r.status_code}): {r.text[:300]}", file=sys.stderr)
        sys.exit(3)
    url = r.json().get("url") or r.json().get("mediaUrl")
    if not url:
        print(f"❌ Media upload response missing URL: {r.text[:300]}", file=sys.stderr)
        sys.exit(3)
    cache_file.write_text(url)
    return url


def parse_publish_pack(path: Path) -> dict[str, str]:
    """Extract per-platform captions from a sauce-cuts PUBLISH_PACK.md.
    Returns {"tiktok": "...", "instagram": "...", ...}. Best-effort: looks for
    section headings like '### TikTok' or '### Instagram Reels'.
    """
    if not path.is_file():
        return {}
    text = path.read_text()
    sections = {}
    current = None
    buffer = []
    SECTION_MAP = {
        "tiktok": "tiktok",
        "instagram reels": "instagram", "instagram": "instagram",
        "facebook reels": "facebook", "facebook": "facebook",
        "youtube shorts": "youtube", "youtube long-form": "youtube_long", "youtube": "youtube",
        "twitter": "twitter", "twitter/x": "twitter",
    }
    in_code_fence = False
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            if current is not None:
                buffer.append(line)
            continue
        if not in_code_fence and line.startswith("### "):
            if current and buffer:
                sections[current] = "\n".join(buffer).strip()
            heading_raw = line[4:].strip().lower()
            # Strip parenthetical
            heading = heading_raw.split("(")[0].strip()
            current = SECTION_MAP.get(heading)
            buffer = []
        elif current is not None and (in_code_fence or not line.startswith("### ")):
            # Keep #hashtag lines (they're not markdown headers in this context)
            buffer.append(line)
    if current and buffer:
        sections[current] = "\n".join(buffer).strip()
    # Strip surrounding code fences
    cleaned = {}
    for k, v in sections.items():
        if v.startswith("```"):
            v = v.split("```", 2)[1]
            if v.startswith("\n"):
                v = v[1:]
        cleaned[k] = v.strip()
    return cleaned


def post_one(platform: str, caption: str, media_url: str | None,
             schedule_iso: str | None, api_key: str, profile_key: str | None,
             dry_run: bool) -> dict:
    """Post or schedule to a single platform via Ayrshare."""
    payload = {
        "post": caption,
        "platforms": [platform],
    }
    if media_url:
        payload["mediaUrls"] = [media_url]
    if schedule_iso:
        payload["scheduleDate"] = schedule_iso

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    if profile_key:
        headers["Profile-Key"] = profile_key

    if dry_run:
        print(f"  [DRY-RUN] {platform}: {json.dumps(payload, indent=2)[:300]}...")
        return {"dry_run": True, "platform": platform, "payload": payload}

    r = requests.post(f"{AYRSHARE_BASE}/post", headers=headers,
                      data=json.dumps(payload), timeout=60)
    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text[:500]}
    return {"status_code": r.status_code, "platform": platform, "response": data}


def append_history(record: dict) -> None:
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    record["recorded_at"] = datetime.now().isoformat()
    with open(HISTORY_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--caption", help="Default caption (used if no per-platform PUBLISH_PACK)")
    p.add_argument("--media", help="Path to MP4 / MOV / JPG / PNG")
    p.add_argument("--platforms", required=True,
                   help="Comma list: tiktok,instagram,facebook,youtube,twitter")
    p.add_argument("--schedule", help="ISO 8601 timestamp with offset (overrides auto-time)")
    p.add_argument("--profile-key", help="Ayrshare profile key (multi-brand)")
    p.add_argument("--per-platform-captions", help="Path to sauce-cuts PUBLISH_PACK.md")
    p.add_argument("--dry-run", action="store_true", help="Print payload, do not send")
    args = p.parse_args()

    config = load_config()
    api_key = config["api_key"]
    profile_key = args.profile_key or config.get("default_profile_key")

    platforms = normalize_platforms(args.platforms)
    if not platforms:
        print("❌ No valid platforms specified", file=sys.stderr)
        sys.exit(1)

    # Resolve per-platform captions
    per_platform = {}
    if args.per_platform_captions:
        per_platform = parse_publish_pack(Path(args.per_platform_captions))

    # Upload media once if provided
    media_url = None
    if args.media:
        media_path = Path(args.media).expanduser().resolve()
        if not media_path.is_file():
            print(f"❌ Media not found: {media_path}", file=sys.stderr)
            sys.exit(1)
        media_url = upload_media(media_path, api_key)

    # Post per platform
    results = []
    for plat in platforms:
        caption = per_platform.get(plat) or args.caption
        if not caption:
            print(f"⚠️  No caption for {plat} — skipping", file=sys.stderr)
            continue
        schedule = args.schedule or default_schedule_for(plat)
        res = post_one(plat, caption, media_url, schedule, api_key, profile_key, args.dry_run)
        results.append(res)
        if args.dry_run:
            continue
        status = res.get("status_code")
        platform_id = (res.get("response", {}).get("postIds", [{}])[0] or {}).get("id", "?")
        if status == 200:
            print(f"  ✅ {plat} @ {schedule} (id: {platform_id})")
        else:
            print(f"  ❌ {plat} ({status}): {json.dumps(res.get('response'))[:200]}")
        append_history({
            "platform": plat,
            "caption": caption[:200],
            "media": str(media_path) if args.media else None,
            "scheduled_for": schedule,
            "status_code": status,
            "post_id": platform_id,
        })

    if args.dry_run:
        print("\n[DRY-RUN] No posts sent.")
        return

    print("\n📣 Holler — done. View in dashboard: https://app.ayrshare.com")


if __name__ == "__main__":
    main()
