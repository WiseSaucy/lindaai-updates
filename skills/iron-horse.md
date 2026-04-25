---
name: iron-horse
description: This skill should be used when the user asks to "send an LOI", "letter of intent", "draft an LOI", "LOI builder", "LOI blaster", "linda-loi", "make an LOI", "send a letter of intent", "LOI for this property", "submit an offer letter", "offer letter to seller", "LOI to seller", "LOI for {property}", "draft offer to {seller}", "send LOI and follow up", "auto follow-up LOI", "LOI with follow-ups", "creative finance LOI", "seller finance LOI", "subject-to LOI", "wholesale LOI", "MHP LOI", "RV park LOI", "stack deal LOI", or any request to generate, send, and follow up on a real estate LOI to a seller.
version: 1.4.0
---

# Linda-LOI 🚂

## Overview

Linda-LOI is LindaAI's locomotive contract engine. Hand it a property and the seller's contact info — Linda-LOI drafts a professional Letter of Intent, generates a clean **signable PDF** (with working AcroForm radio buttons + signature/date/print-name fields the seller fills directly in Preview or Adobe), fires it off to the seller automatically, and queues follow-up emails at any day-counts you choose. Once Linda-LOI is loaded up, the user can walk away — the follow-ups send themselves via a launchd daemon that runs daily at 9 AM.

Cash, conventional, FHA, hard money, seller finance, subject-to, wrap, or stack creative finance — all of it. Supports single-option or dual-option (A/B) LOIs with real radio buttons so the seller picks their preferred structure.

## When This Skill Applies

- User asks to draft, send, or blast an LOI
- User mentions "letter of intent" for any property
- User says "send an offer letter to {seller}"
- User wants to submit an offer with auto follow-ups
- User says "linda-loi", "loi blaster"
- User wants automated LOI follow-up sequences
- User has a property + seller email and wants to fire off an offer
- User mentions creative finance — seller carry, sub-to, wrap, stack
- User wants a signable PDF with both buyer and seller signature fields

## How It Works

### License Check

Before proceeding, verify the LindaAI license:

1. Read `~/.claude/linda-license.json`
2. If the file does not exist, stop and tell the user:
   > 🤠 "Whoa there, partner — no LindaAI license found on this machine. You'll need a valid license to use LindaAI skills. Reach out to get set up and we'll have you in the saddle in no time."
   Do not proceed with any other steps.
3. If today's date is past the `expiration_date`, stop and tell the user:
   > 🤠 "Whoa there, partner — your LindaAI license expired on [expiration_date]. Reach out to renew and we'll get you back in the saddle." 🏇
   Do not proceed with any other steps.
4. If `status` is not `"active"`, stop and tell the user:
   > 🤠 "Whoa there, partner — your LindaAI license is currently [status]. Reach out to get this sorted and we'll have you riding again in no time."
   Do not proceed with any other steps.
5. If all checks pass, proceed.

### One-Time Setup (First Run Only)

Linda-LOI needs three things on first use:

1. **ReportLab installed:** `pip3 install reportlab pypdf`
2. **Gmail app password in Keychain** (for auto-send):
   ```bash
   security add-generic-password -a "your-email@gmail.com" -s "lindaai-gmail" -w "your-app-password"
   ```
   Get app password at https://myaccount.google.com/apppasswords
3. **Buyer config** at `brain/loi/config.json` — Linda-LOI creates the file with placeholders on first run; user fills in buyer name, entity, address, phone, email.

### Step 1: Gather LOI Details

Required (ask only for what's missing):

| Field | Description |
|-------|-------------|
| Property address | Full address |
| Property type | SFH, MHP, RV park, multi-family, land, commercial |
| Purchase price | Dollar amount |
| Earnest money | Default $2,500 |
| Due diligence | Default 30 days |
| Closing | Default 30 days from DD |
| Financing | All cash / conventional / DSCR / seller finance / stack |
| Seller name | Or "To Whom It May Concern" |
| Seller email | Required for auto-send |
| Follow-up cadence | Default 3, 7, 14 days |

For dual-option LOIs (A/B), gather terms for each option.

### Step 2: Generate the LOI

```bash
python3 ~/.claude/skills/linda-loi/scripts/generate_loi.py \
  --property "{address}" \
  --type "{property_type}" \
  --price {price} \
  --earnest 2500 \
  --dd-days 30 \
  --close-days 30 \
  --financing "{financing}" \
  --seller-name "{seller_name}" \
  --seller-email "{seller_email}" \
  --special "{special_terms}"
```

Output: `brain/loi/{seller-slug}/{YYYY-MM-DD}/`
- `LOI.md` — markdown source
- `LOI.html` — print-ready HTML
- `LOI.pdf` — **signable PDF** with working AcroForm fields
- `loi.json` — metadata for downstream scripts

### Step 3: Verify PDF Before Sending

ALWAYS render a quick visual check before fire:

```bash
python3 -c "
from pypdf import PdfReader
r = PdfReader('brain/loi/{seller-slug}/{date}/LOI.pdf')
print(f'Pages: {len(r.pages)}, fields: {len(r.trailer[\"/Root\"][\"/AcroForm\"][\"/Fields\"])}')
"
```

Confirm 4 form fields (or 3 for single-option): `accepted_option`, `seller_print_name`, `seller_signature`, `seller_date`.

### Step 4: Auto-Send the LOI

```bash
python3 ~/.claude/skills/linda-loi/scripts/send_loi.py \
  --loi-dir "brain/loi/{seller-slug}/{date}/" \
  --to "{seller_email}" \
  --seller-name "{seller_name}" \
  --property "{address}" \
  --price {price}
```

Sends immediately via Gmail SMTP using Keychain creds. PDF attached. **Always echo the recipient email back to user for confirmation before fire.**

### Step 5: Queue Follow-Ups

```bash
python3 ~/.claude/skills/linda-loi/scripts/schedule_followup.py \
  --loi-dir "brain/loi/{seller-slug}/{date}/" \
  --to "{seller_email}" \
  --seller-name "{seller_name}" \
  --property "{address}" \
  --days "3,7,14"
```

Appends to `brain/loi/queue.json`. Daemon checks daily.

### Step 6: Install Daemon (First Run)

```bash
python3 ~/.claude/skills/linda-loi/scripts/install_daemon.py
```

Creates `~/Library/LaunchAgents/com.lindaai.linda-loi.plist`. Runs daily at 9 AM. **One-time setup — must be run manually in Terminal.**

### Step 7: Confirm to User

> 🚂 Yeeee Hawww! Linda-LOI blasted that LOI.
>
> **Sent to:** {seller_name} ({seller_email})
> **Property:** {address}
> **Offer:** ${price:,}
> **Follow-ups queued:** {days[0]}d, {days[1]}d, {days[2]}d
>
> PDF + HTML saved to `brain/loi/{seller-slug}/{date}/`. Linda-LOI handles the rest.

## File Structure

```
brain/loi/
  config.json                          # Buyer info (one-time setup)
  queue.json                           # Pending follow-ups
  log.md                               # Master log of every LOI fired
  {seller-slug}/
    {YYYY-MM-DD}/
      LOI.md
      LOI.html
      LOI.pdf
      loi.json
      sent.json                        # Send timestamps + status
```

## Follow-Up Email Templates

Linda-LOI rotates three follow-up tones automatically:

**Touch 1 (gentle nudge):**
> Subject: Following up on my offer for {property}
> Body: Hi {seller_name}, just wanted to make sure my LOI hit your inbox. Happy to walk through the terms or adjust where it makes sense. — {buyer_name}

**Touch 2 (value-add):**
> Subject: Quick question on {property}
> Body: Hi {seller_name}, I'm a serious buyer with funds in place and can close fast. Anything specific holding you back? Happy to restructure to make it work. — {buyer_name}

**Touch 3 (final close):**
> Subject: Final check-in on {property}
> Body: Hi {seller_name}, this is my last touch on the LOI. If now isn't right, no worries — let me know and I'll close the file. Otherwise, I'm all ears. — {buyer_name}

## Critical Rules — Apply Every Time

1. **Always echo the recipient email back to the user character-by-character before any send.** Get confirmation. Never assume on first mention.
2. **Always render and inspect the PDF visually before sending.** Use `pdftoppm` or `sips` to convert to PNG and verify layout.
3. **Use AcroForm fields with `canvas.absolutePosition()`** for radio buttons + signature fields placed via custom Flowable. Do NOT use `onFirstPage`/`onLaterPages` callbacks for page-specific content — those fire on every page.
4. **Wrap option blocks in `KeepTogether`** so they don't split across pages.
5. **For Texas deals:** Property tax is 2.3% of purchase price annually — bake it into the underwrite if running deal numbers alongside.
6. **For DSCR-financed deals:** Senior LTV target 60-75% (offer 3 scenarios), DSCR ratio must clear 1.20.

## Example Usage

**User:** "Iron horse — fire an LOI on 123 Main St, MHP, $1.2M, all cash, seller is Bob Smith bob@email.com, follow up in 3, 7, 14 days"

**LindaAI:** Confirms email back: "Confirming fire to bob@email.com — yes/no?" Generates LOI PDF, fires email after confirmation, queues 3 follow-ups.

**User:** "LOI for 320 acres of land in Beaumont, $450k seller finance, 20% down, 30yr at 6%, send to lisa@gmail.com, follow up at 5 and 14 days"

**LindaAI:** Fires LOI with seller-finance terms, queues 2 follow-ups.

## Error Handling

- **No license file:** Stop with the standard partner message.
- **Missing seller email:** Ask — won't proceed without it.
- **Missing buyer config:** Ask once, save it, never ask again.
- **Email send fails:** Log to `sent.json` with error and tell user. Don't queue follow-ups for a failed send.
- **Daemon not installed:** Tell user to run `install_daemon.py` manually in Terminal.
- **ReportLab missing:** Tell user to run `pip3 install reportlab pypdf`.
- **PDF layout broken:** Re-generate with `KeepTogether` + `absolutePosition()` — never use canvas overlays for page-specific content.

---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
