#!/usr/bin/env python3
"""
LindaAI — YouTube transcription pipeline.

Strategy (fast + cheap first, heavy only when needed):
  1. METADATA  — pull title / uploader / duration.
  2. CAPTIONS  — try YouTube's own subtitles (manual, then auto-generated).
                 If present, parse them to clean text. Fast, free, no model.
  3. WHISPER   — only if there are no captions: download bestaudio and
                 transcribe locally with faster-whisper (CPU int8 by default).

Output: writes a plain-text transcript and prints a JSON summary
(title, source method, word count, output path) on the last line of stdout.

Usage:
  python3 transcribe.py "https://www.youtube.com/watch?v=ID"
  python3 transcribe.py URL --out transcript.txt --model small --lang en

Requires:  pip install -r requirements.txt   (yt-dlp, faster-whisper)

NOTE: this needs outbound access to YouTube. In a locked-down environment the
egress proxy returns 403 and the script will say so plainly — that is a network
policy limit, not a bug. See:
https://code.claude.com/docs/en/claude-code-on-the-web
"""
import argparse
import glob
import json
import os
import re
import sys
import tempfile


def _err(msg, hint=None):
    out = {"ok": False, "error": msg}
    if hint:
        out["hint"] = hint
    print(json.dumps(out))
    sys.exit(1)


def _require(mod, pip_name):
    try:
        return __import__(mod)
    except ImportError:
        _err(f"Missing dependency: {pip_name}",
             f"Install it with: pip install {pip_name}")


def is_blocked(exc: Exception) -> bool:
    s = str(exc).lower()
    return "403" in s or "forbidden" in s or "tunnel connection failed" in s


# --------------------------------------------------------------------------- #
# VTT / caption cleaning
# --------------------------------------------------------------------------- #
_TAG = re.compile(r"<[^>]+>")            # <00:00:01.500> and <c> styling tags
_TS  = re.compile(r"^\d{2}:\d{2}:\d{2}[.,]\d{3}\s*-->")


def vtt_to_text(path: str) -> str:
    lines = []
    last = None
    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if not line.strip():
                continue
            if line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
                continue
            if _TS.match(line) or "-->" in line:
                continue
            if line.strip().isdigit():        # cue index
                continue
            text = _TAG.sub("", line).strip()
            if not text:
                continue
            # auto-captions roll the same line repeatedly — drop consecutive dupes
            if text == last:
                continue
            lines.append(text)
            last = text
    # collapse a final pass of adjacent duplicate phrases
    cleaned = []
    for t in lines:
        if cleaned and (t == cleaned[-1] or t in cleaned[-1]):
            continue
        cleaned.append(t)
    return " ".join(cleaned)


# --------------------------------------------------------------------------- #
# steps
# --------------------------------------------------------------------------- #
def get_meta(ydl, url):
    info = ydl.extract_info(url, download=False)
    return {
        "title": info.get("title"),
        "uploader": info.get("uploader") or info.get("channel"),
        "duration": info.get("duration"),
        "id": info.get("id"),
    }


def try_captions(url, workdir, langs):
    """Return cleaned caption text or None."""
    yt_dlp = _require("yt_dlp", "yt-dlp")
    base = os.path.join(workdir, "cap")
    opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitlesformat": "vtt",
        "subtitleslangs": langs,
        "outtmpl": base + ".%(ext)s",
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    vtts = sorted(glob.glob(base + "*.vtt"))
    if not vtts:
        return None
    # prefer a manual/non-auto track if both exist (auto files contain a lang tag too;
    # just take the first, they are usually equivalent for our purpose)
    text = vtt_to_text(vtts[0])
    return text or None


def whisper_transcribe(url, workdir, model_size, lang):
    yt_dlp = _require("yt_dlp", "yt-dlp")
    fw = _require("faster_whisper", "faster-whisper")
    base = os.path.join(workdir, "audio")
    opts = {
        "format": "bestaudio/best",
        "outtmpl": base + ".%(ext)s",
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    files = [f for f in glob.glob(base + ".*")]
    if not files:
        _err("Could not download audio for transcription.")
    audio = files[0]
    from faster_whisper import WhisperModel
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _info = model.transcribe(
        audio, vad_filter=True, language=(None if lang == "auto" else lang)
    )
    return " ".join(s.text.strip() for s in segments).strip()


def main():
    ap = argparse.ArgumentParser(description="Transcribe a YouTube video.")
    ap.add_argument("url")
    ap.add_argument("--out", default="transcript.txt")
    ap.add_argument("--model", default="small",
                    help="faster-whisper size: tiny|base|small|medium|large-v3")
    ap.add_argument("--lang", default="en",
                    help="caption/whisper language, or 'auto'")
    ap.add_argument("--force-whisper", action="store_true",
                    help="skip captions, always transcribe audio")
    args = ap.parse_args()

    yt_dlp = _require("yt_dlp", "yt-dlp")
    langs = [args.lang, f"{args.lang}-orig", f"{args.lang}-US"] if args.lang != "auto" else ["en", "en-orig"]

    with tempfile.TemporaryDirectory() as workdir:
        # metadata (also the first thing that will 403 if YouTube is blocked)
        try:
            with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True, "skip_download": True}) as ydl:
                meta = get_meta(ydl, args.url)
        except Exception as e:
            if is_blocked(e):
                _err("YouTube is blocked by this environment's network policy (403).",
                     "Reconfigure the environment to allow youtube.com + googlevideo.com, "
                     "then re-run. Docs: https://code.claude.com/docs/en/claude-code-on-the-web")
            _err(f"Could not read video metadata: {e}")

        text, method = None, None
        if not args.force_whisper:
            try:
                text = try_captions(args.url, workdir, langs)
                if text:
                    method = "captions"
            except Exception as e:
                if is_blocked(e):
                    _err("YouTube is blocked by this environment's network policy (403).",
                         "Allow youtube.com + googlevideo.com in the environment's network policy.")
                # non-fatal: fall through to whisper

        if not text:
            try:
                text = whisper_transcribe(args.url, workdir, args.model, args.lang)
                method = f"whisper:{args.model}"
            except Exception as e:
                if is_blocked(e):
                    _err("YouTube is blocked by this environment's network policy (403).",
                         "Allow youtube.com + googlevideo.com in the environment's network policy.")
                _err(f"Transcription failed: {e}")

        if not text:
            _err("No transcript could be produced (no captions and audio transcription empty).")

        header = (f"Title: {meta.get('title')}\n"
                  f"Channel: {meta.get('uploader')}\n"
                  f"Video ID: {meta.get('id')}\n"
                  f"Source: {method}\n"
                  + "-" * 60 + "\n")
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(header + text + "\n")

        print(json.dumps({
            "ok": True,
            "title": meta.get("title"),
            "channel": meta.get("uploader"),
            "duration_sec": meta.get("duration"),
            "method": method,
            "words": len(text.split()),
            "out": os.path.abspath(args.out),
        }))


if __name__ == "__main__":
    main()
