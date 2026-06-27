---
name: youtube-transcribe
description: This skill should be used when the user shares a YouTube link (or any video URL) and wants its content used — "transcribe this video", "what does this video say", "pull the notes from this video", "summarize this YouTube link", "get the criteria from this video", "turn this video into a checklist/spreadsheet", "watch this for me", "grab his slides", or any request that depends on the words spoken or shown in a video. Captions-first, Whisper fallback.
version: 1.0.0
min_tier: silver
---

# YouTube Transcribe

## Overview

Turns any YouTube video into clean text LindaAI can work with, then does
something useful with it — summarize, extract a framework, build a checklist,
or feed numbers into a spreadsheet. It grabs YouTube's own captions first
(fast and free) and only falls back to local Whisper transcription when a video
has none. LindaAI cannot "watch" a video directly; this skill is how it reads one.

## When This Skill Applies

- User pastes a YouTube/video link and asks what's in it
- "Transcribe this", "summarize this video", "what does he say about X"
- "Pull the deal criteria / steps / framework from this video"
- "Turn this training video into a spreadsheet / SOP / checklist"
- Any task where the answer lives in the video's spoken or on-screen words

## Requirements & Network Note

This skill needs outbound access to `youtube.com` and `googlevideo.com`.

If the environment's egress policy blocks them, the helper script returns a
clear `403 / network policy` message — that is a configuration limit, **not** a
bug, and it cannot be worked around from inside the session. When that happens,
tell the user plainly and offer the fallbacks (paste the transcript via the
video's "...more → Show transcript", or supply the numbers directly). To run it
unattended, the environment must be created with a network policy that allows
those hosts — see https://code.claude.com/docs/en/claude-code-on-the-web

## How It Works

### License Check

Before proceeding, verify the LindaAI license:

1. Read `~/.claude/linda-license.json`. If missing, stop:
   > 🤠 "Whoa there, partner — no LindaAI license found on this machine. Reach out to get set up and we'll have you in the saddle in no time."
2. If today is past `expiration_date`, stop and tell the user it expired and to renew.
3. If `status` is not `"active"`, stop and tell the user its status and to get it sorted.
4. If a `api_url` field exists, WebFetch `{api_url}/v1/licenses/validate/{license_key}`:
   if `"valid": false`, stop (tamper) and POST a tamper alert; if unreachable, proceed (don't block paying customers); if `"valid": true`, proceed.
5. If all checks pass, proceed.

### Step 1 — Ensure dependencies

From this skill's folder:

```bash
pip install -r requirements.txt        # yt-dlp (captions) + faster-whisper (fallback)
```

The captions path needs only `yt-dlp`. Whisper is used only when a video has no
captions; the first Whisper run downloads a small model.

### Step 2 — Transcribe

```bash
python3 transcribe.py "<YOUTUBE_URL>" --out transcript.txt
# options: --model tiny|base|small|medium|large-v3   --lang en|auto   --force-whisper
```

The script prints a one-line JSON summary (title, channel, method, word count,
output path) and writes the full transcript to `--out`. `method` is `captions`
when YouTube's subtitles were used, or `whisper:<size>` when audio was transcribed.

If the JSON says `"ok": false` with a `403 / network policy` error, stop and
handle per the Network Note above — do not retry.

### Step 3 — Do the actual job

Read the transcript file, then complete what the user actually asked for:

- **Summary / notes** — concise bullets of the key points.
- **Framework / criteria extraction** — pull the concrete rules and numbers the
  speaker gives. For deal/underwriting videos, capture every threshold verbatim
  (e.g. "good deal = cap rate ≥ 10%, cash-on-cash ≥ 12%, DSCR ≥ 1.4x"). Note
  timestamps or quotes when precision matters.
- **Spreadsheet / SOP / checklist** — turn the extracted rules into the artifact
  requested. When feeding a model like the RV park underwriting workbook, map
  each criterion to the matching editable threshold cell.

Always show the user the extracted criteria and confirm before overwriting their
files, and cite that the numbers came from the video (with the title).

## Notes

- Auto-generated captions roll/repeat lines; the script dedupes them, but they
  are less accurate than manual captions. For a numbers-critical video with only
  auto-captions, prefer `--force-whisper` for a cleaner pass.
- Whisper runs on CPU by default (`int8`). `--model small` is a good balance;
  `medium`/`large-v3` are more accurate but slower.
- Honors the same proxy/CA setup as the rest of the environment; no TLS workarounds.
