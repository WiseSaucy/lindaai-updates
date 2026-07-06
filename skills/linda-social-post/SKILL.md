---
name: linda-social-post
description: This skill should be used when the user asks to post via "Ayrshare", "post with Ayrshare", "schedule via Ayrshare", "Ayrshare cross-post", or mentions their Ayrshare API key or Ayrshare account. RETIRED — this Ayrshare path is deprecated; requests route to /linda-post-walkthrough (guided manual posting) or /linda-postiz-post (Postiz automation).
version: 2.0.0
---

# Linda Social Post — RETIRED (Ayrshare path deprecated)

📣 **Holler** (Social Media) here. This Ayrshare-based publishing path is **retired**. LindaAI's publishing now runs through one front door:

- **`/linda-post-walkthrough`** — the front door for all "post my content / publish this" requests. Holler walks you through posting manually (no API, no extra bills), OR auto-routes to Postiz if you have it connected.
- **`/linda-postiz-post`** — the automation engine when Postiz Cloud is wired in (`~/.lindaai/postiz.json`). Zero-click scheduling across TikTok, Instagram, Facebook, YouTube, and Twitter/X.

## What to do when this skill is triggered

If a user mentions Ayrshare or lands here:

> 📣 Holler — the Ayrshare hookup has been retired, Boss. Good news: you don't need it (or the bill). Say "post my content" and I'll take it from `/linda-post-walkthrough` — I'll walk you through posting step by step, or if you've got Postiz connected I'll auto-schedule the whole pack for you.

Then invoke `/linda-post-walkthrough` with whatever project/pack and platforms the user asked for. Do not attempt any Ayrshare API calls.

---

📣 *Holler — Social Media* · LindaAI · Built by Daniel Wise

© 2022-2026 Daniel Wise · LindaAI · support@send.lindaai-brain.com · lindaai-brain.com
