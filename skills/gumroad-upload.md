---
name: gumroad-upload
description: Upload products to Gumroad automatically via browser automation. Reads a products JSON manifest, drives Chrome, creates every product with name/price/description/file/tags/publish. Use when user says "/gumroad-upload", "upload to gumroad", "publish my products", "list on gumroad", "gumroad automation", "batch upload gumroad", "create gumroad products".
---

# /gumroad-upload — Batch Upload Products to Gumroad

Drives a Chrome browser via Playwright to create products on Gumroad automatically. Customer logs in once, script handles the rest.

## What this skill does

1. Reads a `products.json` manifest (the list of products to upload)
2. Launches Chrome via Playwright
3. Opens gumroad.com — customer logs in manually ONE time
4. For each product: creates listing, sets name/price/description/tags, uploads zip file, publishes
5. Reports which succeeded and which need manual retry

## Steps when invoked

1. Ask the user for the path to their products manifest (default `~/Desktop/gumroad-products.json`)
2. If the manifest doesn't exist, offer to generate one from a `GUMROAD-UPLOAD-PACKET.md` file (parse it)
3. Confirm Playwright is installed:
   ```
   python3 -c "import playwright" 2>&1
   ```
   If missing, install: `pip3 install playwright && playwright install chromium`
4. Run the automation script:
   ```
   python3 ~/.claude/skills/gumroad-upload/upload.py --manifest <path>
   ```
5. A Chrome window opens — user logs in to Gumroad manually
6. Script waits for confirmation, then iterates through each product
7. Reports results: `✅ 5/5 products created` or which failed

## products.json manifest format

```json
{
  "products": [
    {
      "name": "LindaAI Bronze — AI Operating System for Business Owners",
      "price": 500,
      "description": "Full description text here...",
      "tagline": "Short one-liner summary",
      "tags": ["AI", "Business", "Productivity"],
      "file_path": "/Users/jowise/Desktop/LindaAI-OG/LindaAI-Gakusei/LindaAI-Bronze.zip",
      "custom_url": "lindaai-bronze",
      "call_to_action": "i_want_this_prompt"
    }
  ]
}
```

## Rules
- NEVER log in as the user. They log in manually in the Chrome window.
- NEVER auto-publish products until asked — default is draft mode
- Always wait 2-3 seconds between actions (Gumroad has rate limits + DOM settling)
- Save a log file of what was uploaded to `~/.claude/lindaai/gumroad-upload-log.md`
- If Gumroad's UI changes break selectors, fail gracefully with a clear error

## Example usage

User: "/gumroad-upload"
Assistant:
1. Reads manifest from Desktop
2. Confirms 5 products to upload: Bronze $500, Silver $1000, Gold $1500, Platinum $4000, Voice Pack $19.99
3. Launches Chrome
4. User logs in once
5. Script uploads all 5 products to draft state
6. User reviews drafts in Gumroad dashboard, clicks "Publish"

---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com
