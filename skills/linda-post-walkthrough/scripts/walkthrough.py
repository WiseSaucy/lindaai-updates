#!/usr/bin/env python3
"""
walkthrough.py — LindaAI's agentic posting coach.

📣 Holler (Social Media) walks the user through posting finished content to
TikTok, Instagram, Facebook, YouTube Shorts, and Twitter/X — one platform at a
time, with no API and no paid integration.

For each platform:
  1. Copies the per-platform caption to the system clipboard
  2. Opens the platform's upload URL in the default browser
  3. Reveals the right MP4 file in Finder (macOS) so the user can drag it in
  4. Prints stepwise instructions
  5. Waits for the user to confirm "done" / "skip" / "stop" before moving on

After all platforms are processed, logs a record to
~/.lindaai/post-walkthrough-history.jsonl for use by /linda-pulse and friends.

Usage:
    walkthrough.py --project /path/to/sauce-cuts-folder \
                   [--platforms tiktok,instagram,facebook,youtube,twitter] \
                   [--schedule-mode auto|now] \
                   [--non-interactive]   # for testing — skips the input prompts

Reads per-platform captions from <project>/PUBLISH_PACK.md using the same
parser format as linda-social-post (### TikTok, ### Instagram Reels, etc).

macOS-first. Linux/Windows fall back gracefully:
  - pbcopy → xclip (Linux) → clip.exe (Windows) → inline print
  - open   → xdg-open (Linux) → start (Windows)
  - open -R (reveal in Finder) → no-op on Linux/Windows; prints the file path

© 2022-2026 Daniel Wise · LindaAI
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

HISTORY_PATH = Path.home() / ".lindaai" / "post-walkthrough-history.jsonl"

# MDT (UTC-6) optimal posting times — matches linda-social-post exactly so
# customers get the same coaching whether they auto-post or walk through.
OPTIMAL_MDT = {
    "tiktok":    {"hour": 20, "minute": 23, "label": "8:23 PM MDT"},
    "instagram": {"hour": 20, "minute": 47, "label": "8:47 PM MDT"},
    "facebook":  {"hour": 19, "minute": 33, "label": "7:33 PM MDT"},
    "youtube":   {"hour": 18, "minute": 17, "label": "6:17 PM MDT"},
    "twitter":   {"hour": 13, "minute": 43, "label": "1:43 PM MDT"},
}

PLATFORM_URLS = {
    "tiktok":    "https://www.tiktok.com/tiktokstudio/upload",
    # Single Meta composer handles both Instagram + Facebook
    "instagram": "https://business.facebook.com/latest/composer",
    "facebook":  "https://business.facebook.com/latest/composer",
    "youtube":   "https://studio.youtube.com",
    "twitter":   "https://x.com/compose/post",
}

# Per-platform MP4 preference order — first existing file wins.
MP4_PREFERENCE = {
    "tiktok":    ["TIKTOK.mp4", "TIKTOK.MP4", "tiktok.mp4"],
    "instagram": ["IG.mp4", "INSTAGRAM.mp4", "FB-IG.mp4", "FB_IG.mp4", "TIKTOK.mp4"],
    "facebook":  ["FB.mp4", "FACEBOOK.mp4", "FB-IG.mp4", "FB_IG.mp4", "TIKTOK.mp4"],
    "youtube":   ["YOUTUBE.mp4", "YT.mp4", "TIKTOK.mp4"],
    "twitter":   ["TWITTER.mp4", "X.mp4", "TIKTOK.mp4"],
}

PLATFORM_ALIASES = {
    "ig": "instagram", "insta": "instagram", "reels": "instagram",
    "fb": "facebook",
    "yt": "youtube", "shorts": "youtube",
    "x": "twitter", "tweet": "twitter",
    "tt": "tiktok",
}

# Pretty display labels
PLATFORM_LABELS = {
    "tiktok":    "TikTok",
    "instagram": "Instagram Reels",
    "facebook":  "Facebook Reels",
    "youtube":   "YouTube Shorts",
    "twitter":   "Twitter/X",
}

# Per-platform stepwise scripts (printed after each open/copy/reveal)
PLATFORM_STEPS = {
    "tiktok": [
        "Drag the highlighted MP4 from Finder into the TikTok Studio upload area",
        "Click the caption field, then paste with Cmd+V (your caption is on the clipboard)",
        "Toggle 'Schedule' on, set the time to {schedule_label}",
        "Click the 'Schedule' button",
        "Holler back with 'done' to move to the next platform (or 'skip' / 'stop')",
    ],
    "instagram": [
        "In the Meta composer that just opened, select Instagram + your primary IG account",
        "WARNING: do not post to an unrelated business page — confirm the page picker shows YOUR account",
        "Drag the highlighted MP4 from Finder into the upload area",
        "Click in the caption field, paste with Cmd+V",
        "Click 'Schedule', set time to {schedule_label}",
        "Click 'Schedule Post'",
        "Holler back with 'done' (or 'skip' / 'stop')",
    ],
    "facebook": [
        "In the Meta composer, select Facebook + your primary FB page",
        "WARNING: confirm the page picker shows YOUR page, not a shared/other page",
        "Drag the highlighted MP4 from Finder into the upload area",
        "Paste the caption with Cmd+V",
        "Click 'Schedule', set time to {schedule_label}",
        "Click 'Schedule Post'",
        "Holler back with 'done' (or 'skip' / 'stop')",
    ],
    "youtube": [
        "In YouTube Studio, click 'Create' (top right) then 'Upload videos'",
        "Drag the highlighted MP4 from Finder into the upload window",
        "Title: paste the first line of your caption (60 char max)",
        "Description: paste the full caption (Cmd+V — it's on your clipboard)",
        "Visibility: select 'Schedule', set time to {schedule_label}",
        "Click 'Schedule'",
        "Holler back with 'done' (or 'skip' / 'stop')",
    ],
    "twitter": [
        "Drag the MP4 from Finder into the Twitter compose window (vertical is fine on X)",
        "Click the caption field, paste with Cmd+V",
        "IMPORTANT: Twitter cap is 280 chars — trim if you see a red counter",
        "Click the calendar icon at the bottom, set the time to {schedule_label}",
        "Click 'Schedule'",
        "Holler back with 'done' (or 'skip' / 'stop')",
    ],
}


# ─────────────────────────────────────────────────────────────────────────────
# Caption parser — identical format to linda-social-post for consistency.
# Looks for ### Section headings, maps to platform keys.
# ─────────────────────────────────────────────────────────────────────────────

SECTION_MAP = {
    "tiktok": "tiktok",
    "instagram reels": "instagram", "instagram": "instagram",
    "facebook reels": "facebook", "facebook": "facebook",
    "youtube shorts": "youtube", "youtube long-form": "youtube_long", "youtube": "youtube",
    "twitter": "twitter", "twitter/x": "twitter", "x": "twitter",
}


def parse_publish_pack(path: Path) -> dict[str, str]:
    """Extract per-platform captions from a sauce-cuts PUBLISH_PACK.md.

    Returns {"tiktok": "...", "instagram": "...", ...}.
    """
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    sections: dict[str, str] = {}
    current: str | None = None
    buffer: list[str] = []
    in_code_fence = False
    for line in text.splitlines():
        # Track fenced code blocks so #hashtag lines inside captions aren't
        # mistaken for markdown headings (fixed 2026-05-27 — hashtags were
        # being stripped from IG/TikTok captions).
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
            heading = heading_raw.split("(")[0].strip()
            current = SECTION_MAP.get(heading)
            buffer = []
        elif current is not None and (in_code_fence or not line.startswith("### ")):
            # Inside a section: keep everything except the next ###-heading.
            # Hashtags (#fyp etc.) are kept because we only skip on `### `.
            buffer.append(line)
    if current and buffer:
        sections[current] = "\n".join(buffer).strip()
    # Strip surrounding code fences
    cleaned: dict[str, str] = {}
    for k, v in sections.items():
        if v.startswith("```"):
            parts = v.split("```")
            if len(parts) >= 2:
                v = parts[1]
                if v.startswith("\n"):
                    v = v[1:]
        cleaned[k] = v.strip()
    return cleaned


# ─────────────────────────────────────────────────────────────────────────────
# Cross-platform helpers (mac-first, gentle Linux/Windows fallback)
# ─────────────────────────────────────────────────────────────────────────────

IS_MAC = platform.system() == "Darwin"
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"


def copy_to_clipboard(text: str) -> bool:
    """Copy text to the system clipboard. Returns True on success.

    macOS:    pbcopy
    Linux:    xclip -selection clipboard  (or xsel -b -i)
    Windows:  clip.exe
    """
    try:
        if IS_MAC and shutil.which("pbcopy"):
            subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
            return True
        if IS_LINUX:
            if shutil.which("xclip"):
                subprocess.run(
                    ["xclip", "-selection", "clipboard"],
                    input=text.encode("utf-8"), check=True,
                )
                return True
            if shutil.which("xsel"):
                subprocess.run(
                    ["xsel", "-b", "-i"],
                    input=text.encode("utf-8"), check=True,
                )
                return True
        if IS_WINDOWS and shutil.which("clip"):
            subprocess.run(["clip"], input=text.encode("utf-16le"), check=True)
            return True
    except subprocess.CalledProcessError as e:
        print(f"  [warn] Clipboard command failed: {e}", file=sys.stderr)
    return False


def open_url(url: str) -> None:
    """Open a URL in the default browser."""
    try:
        if IS_MAC:
            subprocess.Popen(["open", url])
        elif IS_WINDOWS:
            os.startfile(url)  # type: ignore[attr-defined]
        elif IS_LINUX and shutil.which("xdg-open"):
            subprocess.Popen(["xdg-open", url])
        else:
            print(f"  [info] Open this URL manually: {url}")
    except Exception as e:
        print(f"  [warn] Couldn't auto-open URL ({e}). Copy/paste: {url}", file=sys.stderr)


def reveal_in_finder(file_path: Path) -> None:
    """Highlight a file in Finder (macOS only). Linux/Windows: print path."""
    if IS_MAC:
        try:
            subprocess.Popen(["open", "-R", str(file_path)])
            return
        except Exception as e:
            print(f"  [warn] open -R failed ({e}); path: {file_path}", file=sys.stderr)
    elif IS_WINDOWS:
        try:
            subprocess.Popen(["explorer", "/select,", str(file_path)])
            return
        except Exception:
            pass
    # Linux + fallback: just print the path so the user can navigate manually
    print(f"  📂 File location: {file_path}")


# ─────────────────────────────────────────────────────────────────────────────
# Schedule helper
# ─────────────────────────────────────────────────────────────────────────────

def next_optimal_slot(platform_key: str, mode: str = "auto") -> tuple[str, str]:
    """Return (iso_timestamp, friendly_label) for the next optimal slot.

    If mode is "now", return ("now", "right now").
    """
    if mode == "now":
        return ("now", "right now (no schedule — hit Publish, not Schedule)")
    pick = OPTIMAL_MDT[platform_key]
    now = datetime.now()
    target = now.replace(hour=pick["hour"], minute=pick["minute"], second=0, microsecond=0)
    if target <= now:
        target = target + timedelta(days=1)
        when = "tomorrow"
    else:
        when = "tonight" if pick["hour"] >= 17 else "today"
    iso = target.strftime("%Y-%m-%dT%H:%M:%S-06:00")
    return (iso, f"{pick['label']} ({when})")


# ─────────────────────────────────────────────────────────────────────────────
# Platform resolution
# ─────────────────────────────────────────────────────────────────────────────

def normalize_platforms(raw: str | None) -> list[str]:
    """Comma list → canonical platform names. Default: all 5."""
    if not raw:
        return ["tiktok", "instagram", "facebook", "youtube", "twitter"]
    out: list[str] = []
    for p in raw.split(","):
        p = p.strip().lower()
        if not p:
            continue
        p = PLATFORM_ALIASES.get(p, p)
        if p in OPTIMAL_MDT:
            out.append(p)
        else:
            print(f"  [warn] Unknown platform '{p}' — skipping", file=sys.stderr)
    return out


def find_mp4(project_dir: Path, platform_key: str) -> Path | None:
    """Walk the per-platform preference list, return first existing file."""
    for candidate in MP4_PREFERENCE[platform_key]:
        p = project_dir / candidate
        if p.is_file():
            return p
    # Also try lowercase variants and a recursive shallow search
    for candidate in MP4_PREFERENCE[platform_key]:
        for found in project_dir.glob(f"**/{candidate}"):
            if found.is_file():
                return found
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Interactive prompt
# ─────────────────────────────────────────────────────────────────────────────

def prompt_continue(platform_label: str, non_interactive: bool) -> str:
    """Wait for user to type 'done' / 'skip' / 'stop'. Returns the choice."""
    if non_interactive:
        return "done"  # test mode auto-confirms
    while True:
        try:
            answer = input(
                f"\n  📣 Holler waiting on {platform_label} → type 'done', 'skip', or 'stop': "
            ).strip().lower()
        except (EOFError, KeyboardInterrupt):
            return "stop"
        if answer in ("done", "d", "next", "n", "yes", "y", ""):
            return "done"
        if answer in ("skip", "s"):
            return "skip"
        if answer in ("stop", "quit", "q", "exit"):
            return "stop"
        print("    (didn't catch that — try 'done', 'skip', or 'stop')")


# ─────────────────────────────────────────────────────────────────────────────
# History logging
# ─────────────────────────────────────────────────────────────────────────────

def append_history(record: dict) -> None:
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# Per-platform walkthrough
# ─────────────────────────────────────────────────────────────────────────────

def walk_one_platform(
    platform_key: str,
    caption: str | None,
    mp4_path: Path | None,
    schedule_mode: str,
    non_interactive: bool,
) -> str:
    """Run the full walkthrough for a single platform. Returns 'done' / 'skip' / 'stop'."""
    label = PLATFORM_LABELS[platform_key]
    iso, schedule_label = next_optimal_slot(platform_key, schedule_mode)

    print(f"\n{'━' * 60}")
    print(f"  📣 Holler — {label}")
    print(f"{'━' * 60}")

    if not caption:
        print(f"  [warn] No caption found for {label} in PUBLISH_PACK.md")
        print(f"  [warn] Skipping {label}. Add a '### {label}' section to your pack to fix.")
        return "skip"

    # 1. Copy caption to clipboard
    copied = copy_to_clipboard(caption)
    if copied:
        print(f"  📋 Caption copied to clipboard ({len(caption)} chars)")
    else:
        print(f"  [warn] Couldn't auto-copy on this OS — caption printed below for manual copy:")
        print(f"  {'─' * 56}")
        for line in caption.splitlines():
            print(f"  | {line}")
        print(f"  {'─' * 56}")

    # 2. Reveal MP4 in Finder
    if mp4_path:
        reveal_in_finder(mp4_path)
        print(f"  📂 Revealed: {mp4_path.name}")
    else:
        print(f"  [warn] No MP4 found for {label} — you'll need to attach a file manually")

    # 3. Open browser to platform upload URL
    url = PLATFORM_URLS[platform_key]
    open_url(url)
    print(f"  🌐 Opened: {url}")

    # 4. Print stepwise instructions
    print(f"  ⏰ Schedule for: {schedule_label}")
    print(f"\n  STEPS:")
    for i, step in enumerate(PLATFORM_STEPS[platform_key], 1):
        print(f"    {i}. {step.format(schedule_label=schedule_label)}")

    # 5. Wait for user confirmation
    return prompt_continue(label, non_interactive)


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="LindaAI's agentic posting coach — walks the user through posting.",
    )
    parser.add_argument("--project", required=True,
                        help="Path to project folder containing PUBLISH_PACK.md + MP4s")
    parser.add_argument("--platforms", default=None,
                        help="Comma list. Default: tiktok,instagram,facebook,youtube,twitter")
    parser.add_argument("--schedule-mode", choices=["auto", "now"], default="auto",
                        help="auto = per-platform optimal MDT times. now = no schedule.")
    parser.add_argument("--non-interactive", action="store_true",
                        help="Skip input prompts (test/CI mode). Auto-marks every platform 'done'.")
    args = parser.parse_args()

    project_dir = Path(args.project).expanduser().resolve()
    if not project_dir.is_dir():
        print(f"❌ Project folder not found: {project_dir}", file=sys.stderr)
        return 1

    pack_path = project_dir / "PUBLISH_PACK.md"
    if not pack_path.is_file():
        print(
            f"❌ PUBLISH_PACK.md not found in {project_dir}\n"
            f"   📣 Holler — Run /sauce-cuts on this folder first, or point me at one\n"
            f"   that already has a publish pack.",
            file=sys.stderr,
        )
        return 1

    captions = parse_publish_pack(pack_path)
    if not captions:
        print(
            f"❌ Couldn't parse any captions from {pack_path}\n"
            f"   📣 Holler — make sure the file has '### TikTok', '### Instagram Reels',\n"
            f"   etc headings. See linda-social-post for the format.",
            file=sys.stderr,
        )
        return 1

    platforms = normalize_platforms(args.platforms)
    if not platforms:
        print("❌ No valid platforms specified", file=sys.stderr)
        return 1

    started_at = datetime.now().isoformat()
    project_name = project_dir.name

    # Show the plan
    print(f"\n📣 Holler — walkthrough plan for \"{project_name}\":\n")
    for i, plat in enumerate(platforms, 1):
        mp4 = find_mp4(project_dir, plat)
        mp4_name = mp4.name if mp4 else "(no MP4 — manual attach)"
        _, label = next_optimal_slot(plat, args.schedule_mode)
        print(f"  {i}. {PLATFORM_LABELS[plat]:18s} — {mp4_name:22s} → {label}")
    print(
        "\n  Going one at a time. For each platform I'll:\n"
        "    • Copy the caption to your clipboard\n"
        "    • Open the upload page in your browser\n"
        "    • Reveal the MP4 in Finder so you can drag it in\n"
        "    • Give you the step-by-step\n"
        "  You tell me 'done' / 'skip' / 'stop' to move on.\n"
    )

    if not args.non_interactive:
        try:
            go = input("  📣 Say 'go' to start (or 'stop' to bail): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            go = "stop"
        if go in ("stop", "quit", "no", "n", "exit", "q"):
            print("\n  📣 Holler — bailed before starting. Holler when you're ready.")
            return 0

    completed: list[str] = []
    skipped: list[str] = []
    stopped_early = False

    for plat in platforms:
        caption = captions.get(plat)
        mp4 = find_mp4(project_dir, plat)
        result = walk_one_platform(
            plat, caption, mp4, args.schedule_mode, args.non_interactive,
        )
        if result == "done":
            completed.append(plat)
            print(f"  ✅ {PLATFORM_LABELS[plat]} — done.")
        elif result == "skip":
            skipped.append(plat)
            print(f"  ⏭  {PLATFORM_LABELS[plat]} — skipped.")
        elif result == "stop":
            stopped_early = True
            print(f"\n  📣 Holler — stopping the walkthrough. Progress saved.")
            break

    finished_at = datetime.now().isoformat()

    # Log to history
    append_history({
        "project": project_name,
        "project_path": str(project_dir),
        "platforms_requested": platforms,
        "platforms_completed": completed,
        "platforms_skipped": skipped,
        "stopped_early": stopped_early,
        "schedule_mode": args.schedule_mode,
        "started_at": started_at,
        "finished_at": finished_at,
    })

    # Wrap-up message
    print(f"\n{'━' * 60}")
    print(f"  📣 Holler — walkthrough done!")
    print(f"{'━' * 60}")
    if completed:
        print(f"\n  Posted/scheduled:")
        for plat in completed:
            _, label = next_optimal_slot(plat, args.schedule_mode)
            print(f"    ✅ {PLATFORM_LABELS[plat]:18s} @ {label}")
    if skipped:
        print(f"\n  Skipped:")
        for plat in skipped:
            print(f"    ⏭  {PLATFORM_LABELS[plat]}")
    if stopped_early:
        print(f"\n  Stopped early — resume anytime with the same command.")
    print(f"\n  Logged to {HISTORY_PATH}")
    print(f"\n  Yeeee Hawww! 🤠 That pack is live.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
