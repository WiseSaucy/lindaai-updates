#!/usr/bin/env python3
"""
LindaAI — video-scrape.

Pulls a video apart so Linda can SEE and HEAR everything in it:
  • FRAMES  — grabs a screenshot every N seconds (or across a time range) so the
    agent can read on-screen content: slides, spreadsheets, charts, formulas.
  • AUDIO   — local Whisper transcript with timestamps.

Works on a YouTube/URL (via yt-dlp) or a local video file.

Usage:
  python3 extract.py "https://www.youtube.com/watch?v=ID" --out-dir out --interval 12
  python3 extract.py local.mp4 --start 27:40 --end 31:40 --interval 8 --no-audio

Then the agent READS the frame PNGs (vision) to transcribe slides/sheets, and
reads transcript.txt for the narration.

Requires:  pip install -r requirements.txt   (yt-dlp, av, pillow, faster-whisper)

NETWORK: downloading from YouTube needs the media CDN allowed, not just the page.
Allowlist BOTH  *.googlevideo.com  AND  youtube.com  (plus *.ytimg.com) in the
environment's network settings. If media is blocked you'll get a clean 403 here —
that's a policy limit, not a bug, and cannot be coded around.
"""
import argparse
import glob
import json
import os
import sys
import tempfile


def out(obj):
    print(json.dumps(obj, indent=2))


def err(msg, hint=None):
    o = {"ok": False, "error": msg}
    if hint:
        o["hint"] = hint
    out(o)
    sys.exit(1)


def is_blocked(e):
    s = str(e).lower()
    return "403" in s or "forbidden" in s or "tunnel connection failed" in s


def require(mod, pip_name):
    try:
        return __import__(mod)
    except ImportError:
        err(f"Missing dependency: {pip_name}", f"pip install {pip_name}")


def parse_ts(v):
    """'90', '1:30', '27:40' -> seconds (float)."""
    if v is None:
        return None
    v = str(v)
    if ":" in v:
        parts = [float(p) for p in v.split(":")]
        s = 0.0
        for p in parts:
            s = s * 60 + p
        return s
    return float(v)


def download(url, workdir):
    yt = require("yt_dlp", "yt-dlp")
    tmpl = os.path.join(workdir, "video.%(ext)s")
    opts = {
        "format": "bestvideo[height<=1080][ext=mp4]/best[ext=mp4]/best",
        "outtmpl": tmpl, "quiet": True, "no_warnings": True, "noprogress": True,
    }
    try:
        with yt.YoutubeDL(opts) as y:
            info = y.extract_info(url, download=True)
    except Exception as e:
        if is_blocked(e):
            err("Video media is blocked by this environment's network policy (403).",
                "Allow *.googlevideo.com (and *.ytimg.com, youtube.com) in the environment's "
                "network settings, then re-run. Captions work without it; media does not.")
        err(f"Download failed: {e}")
    files = glob.glob(os.path.join(workdir, "video.*"))
    if not files:
        err("Download produced no file.")
    return files[0], (info.get("title") if isinstance(info, dict) else None)


def grab_frames(path, outdir, interval, start, end):
    av = require("av", "av")
    require("PIL", "pillow")
    os.makedirs(outdir, exist_ok=True)
    container = av.open(path)
    stream = container.streams.video[0]
    tb = stream.time_base
    dur = float(stream.duration * tb) if stream.duration else None
    if dur is None and container.duration:
        dur = container.duration / 1_000_000
    start = start or 0.0
    end = end if end else (dur or 0.0)
    if not end or end <= start:
        end = (dur or (start + interval))
    saved = []
    t = start
    while t <= end + 0.001:
        try:
            container.seek(int(t / tb), stream=stream, any_frame=False, backward=True)
            frame = next(container.decode(stream))
            mm, ss = int(t // 60), int(t % 60)
            fn = os.path.join(outdir, f"frame_{mm:02d}m{ss:02d}s.png")
            frame.to_image().save(fn)
            saved.append(fn)
        except StopIteration:
            break
        except Exception:
            pass
        t += interval
    return saved, dur


def transcribe(path, model_size, lang):
    require("faster_whisper", "faster-whisper")
    from faster_whisper import WhisperModel
    m = WhisperModel(model_size, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(path, vad_filter=True, language=(None if lang == "auto" else lang))
    lines = []
    for s in segs:
        mm, ss = int(s.start // 60), int(s.start % 60)
        lines.append(f"[{mm:02d}:{ss:02d}] {s.text.strip()}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Extract frames + transcript from a video.")
    ap.add_argument("source", help="video URL or local file path")
    ap.add_argument("--out-dir", default="video_scrape")
    ap.add_argument("--interval", type=float, default=15.0, help="seconds between frames")
    ap.add_argument("--start", default=None, help="start time (e.g. 27:40)")
    ap.add_argument("--end", default=None, help="end time (e.g. 31:40)")
    ap.add_argument("--no-audio", action="store_true", help="skip Whisper transcript")
    ap.add_argument("--model", default="small", help="whisper size: tiny|base|small|medium|large-v3")
    ap.add_argument("--lang", default="en")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    frames_dir = os.path.join(args.out_dir, "frames")
    start, end = parse_ts(args.start), parse_ts(args.end)

    with tempfile.TemporaryDirectory() as workdir:
        title = None
        if os.path.exists(args.source):
            video = args.source
        else:
            video, title = download(args.source, workdir)

        frames, dur = grab_frames(video, frames_dir, args.interval, start, end)

        transcript_path = None
        if not args.no_audio:
            try:
                text = transcribe(video, args.model, args.lang)
                transcript_path = os.path.join(args.out_dir, "transcript.txt")
                with open(transcript_path, "w", encoding="utf-8") as fh:
                    fh.write((f"Title: {title}\n\n" if title else "") + text + "\n")
            except SystemExit:
                raise
            except Exception as e:
                if is_blocked(e):
                    err("Audio media blocked by network policy (403).",
                        "Allow *.googlevideo.com in the environment's network settings.")
                transcript_path = f"(audio transcription skipped: {e})"

    out({
        "ok": True,
        "title": title,
        "duration_sec": round(dur) if dur else None,
        "frames_dir": os.path.abspath(frames_dir),
        "frame_count": len(frames),
        "frames": [os.path.abspath(f) for f in frames],
        "transcript": transcript_path,
        "next": "The agent should READ the frame PNGs (vision) to capture on-screen "
                "text — slides, spreadsheets, formulas — and read transcript.txt for narration.",
    })


if __name__ == "__main__":
    main()
