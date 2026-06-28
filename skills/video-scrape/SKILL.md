---
name: video-scrape
description: This skill should be used when the user wants the FULL contents of a video — not just the words, but what's ON SCREEN — "scrape this video", "screenshot the video", "read the slides/spreadsheet in this video", "pull the formulas off this video", "extract the on-screen text", "rip this video", "walk through this video frame by frame", "get everything out of this video/walkthrough/workshop". Downloads the video, grabs frames on an interval so the agent can read slides/spreadsheets/charts, and runs Whisper on the audio. Use over `youtube-transcribe` when on-screen visuals matter, not only narration.
version: 1.0.0
min_tier: gold
---

# Video Scrape

## Overview

Pulls a video apart so Linda can both **see** and **hear** it. Downloads the
video (yt-dlp), grabs a **screenshot every N seconds** so the agent can read
anything shown on screen — slides, spreadsheets, charts, formulas — and runs a
local **Whisper transcript** with timestamps. Pair the frames with the narration
and you can reconstruct a whole workshop, course lesson, or demo. Works on a URL
or a local video file.

This is the heavier cousin of `youtube-transcribe` (which only pulls captions).
Reach for `video-scrape` when the *visuals* carry the information.

## ⚠️ Network requirement (read this first)

Video and audio bytes come from a media CDN (`googlevideo.com`), **not** the page
domain. The page/captions can work while media is blocked. To download media, the
environment's **Network access** must allow these (Custom allowlist):

```
*.googlevideo.com
youtube.com
*.youtube.com
*.ytimg.com
```

(plus the host of any non-YouTube video you're scraping). If media is blocked the
script returns a clean `403 / network policy` error — that is a policy limit, it
**cannot be coded around**, and should not be retried. Set it in the environment
settings (claude.ai/code → environment → Network access → Custom), then re-run.
Local video files work with no network at all.

## When This Skill Applies

- "Scrape / screenshot / rip this video", "read the slides in this video"
- "Pull the spreadsheet/formulas/numbers shown in this walkthrough"
- Any time the answer is on the screen, not just in the narration
- Turning a course lesson, workshop, or demo into notes + extracted visuals

## How It Works

### License Check

Verify the LindaAI license (`~/.claude/linda-license.json`) exactly as the other
LindaAI skills do: missing / expired / not `active` → stop with the matching
message; if an `api_url` is present, server-validate and POST a tamper alert on
`"valid": false`; unreachable → proceed. Otherwise proceed.

### Step 1 — Install deps

```bash
pip install -r requirements.txt   # yt-dlp, av (PyAV), pillow, faster-whisper
```

(No system ffmpeg needed — PyAV handles decoding; single-format downloads need no merge.)

### Step 2 — Extract frames (+ transcript)

```bash
# Whole video, a frame every 15s, plus Whisper transcript:
python3 extract.py "<URL or local.mp4>" --out-dir out

# Just the part that matters, denser frames, no audio:
python3 extract.py "<URL>" --start 27:40 --end 31:40 --interval 8 --no-audio
```

Options: `--interval <sec>` (frame spacing), `--start/--end` (e.g. `27:40`),
`--no-audio`, `--model tiny|base|small|medium|large-v3`, `--lang en|auto`.

It prints a JSON manifest: `frames_dir`, the list of frame PNGs, frame count,
duration, and the transcript path.

### Step 3 — READ the frames (this is the point)

The script extracts images; **the agent does the reading.** Open the frame PNGs
and transcribe what's on screen — slide bullet points, spreadsheet cells and
layout, on-screen formulas, chart values. Cross-reference with `transcript.txt`
(timestamps line up with the frame filenames, e.g. `frame_28m10s.png` ≈ `[28:10]`).
Tighten `--interval` over the section that matters (a demo, a slide) to catch detail.

### Step 4 — Use it

Synthesize the frames + narration into whatever was asked: notes, a slide
breakdown, extracted criteria/formulas, or data to feed another tool (e.g. the
RV park underwriting workbook).

## Notes

- **Only scrape videos you have the right to use** — your own content, public
  videos, or material you're licensed for. This is a reading tool, not a way to
  bypass access controls.
- Frame filenames are timestamped (`frame_MMmSSs.png`) so they map to the transcript.
- CPU Whisper: `small` is a good balance; `medium`/`large-v3` are slower but sharper.
- Pairs with `youtube-transcribe` (captions-only, lighter) and the deal pipeline.
