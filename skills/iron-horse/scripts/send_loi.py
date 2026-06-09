#!/usr/bin/env python3
"""
Linda-LOI — LOI Auto-Sender (LindaAI v1.4)
Fires the LOI email immediately via Gmail SMTP using Keychain credentials.

Usage:
    python3 send_loi.py --loi-dir <path> --to <email> --seller-name <name> --property <addr> --price <num>

Setup (one-time):
    security add-generic-password -a "you@gmail.com" -s "lindaai-gmail" -w "your-app-password"
"""

import argparse
import json
import mimetypes
import smtplib
import subprocess
import sys
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path


KEYCHAIN_SERVICE = "lindaai-gmail"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def get_credentials():
    try:
        result = subprocess.run(
            ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-g"],
            capture_output=True, text=True, check=True,
        )
        combined = result.stdout + result.stderr
        email = None
        password = None
        for line in combined.splitlines():
            line = line.strip()
            if line.startswith('"acct"'):
                email = line.split('"')[-2]
            elif line.startswith("password:"):
                password = line.split('"')[1] if '"' in line else line.split("password:", 1)[1].strip()
        if not email or not password:
            raise RuntimeError("Keychain entry found but could not parse email/password.")
        return email, password
    except subprocess.CalledProcessError:
        sys.stderr.write(
            f"\n[ERROR] No keychain entry for '{KEYCHAIN_SERVICE}'.\n"
            f"Run once to set up:\n"
            f'  security add-generic-password -a "you@gmail.com" -s "{KEYCHAIN_SERVICE}" -w "your-app-password"\n'
            f"Get app password at https://myaccount.google.com/apppasswords\n"
        )
        sys.exit(1)


def build_message(sender, to, subject, body, attachments):
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    for path_str in attachments or []:
        path = Path(path_str).expanduser().resolve()
        if not path.exists():
            sys.stderr.write(f"[WARN] Attachment not found: {path}\n")
            continue
        ctype, _ = mimetypes.guess_type(path.name)
        if ctype is None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        with open(path, "rb") as f:
            msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=path.name)
    return msg


def send(to, subject, body, attachment=None):
    sender, password = get_credentials()
    msg = build_message(sender, to, subject, body, [attachment] if attachment else [])
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(sender, password)
        smtp.send_message(msg)
    return sender


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--loi-dir', required=True)
    p.add_argument('--to', required=True)
    p.add_argument('--seller-name', required=True)
    p.add_argument('--property', required=True)
    p.add_argument('--price', type=float, required=True)
    args = p.parse_args()

    loi_dir = Path(args.loi_dir).expanduser().resolve()
    pdf = loi_dir / "LOI.pdf"
    meta_path = loi_dir / "loi.json"
    if not pdf.exists():
        sys.exit(f"[ERROR] LOI PDF not found at {pdf}")

    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    buyer_name = meta.get('buyer_name', '')
    buyer_email = meta.get('buyer_email', '')

    salutation = args.seller_name if args.seller_name.lower() != 'to whom it may concern' else 'To Whom It May Concern'

    subject = f"Letter of Intent — {args.property}"
    body = f"""{salutation},

Please find attached my Letter of Intent to purchase {args.property} for ${args.price:,.0f}.

The LOI outlines the principal terms — purchase price, earnest money, due diligence period, and proposed closing timeline. The PDF is set up so you can sign directly in Preview or Adobe and return it.

I'm a serious buyer and can move quickly. Happy to discuss any of the terms or adjust where it makes sense.

Looking forward to hearing back.

Best,
{buyer_name}
{buyer_email}
"""

    try:
        sender = send(args.to, subject, body, str(pdf))
        status_entry = {"timestamp": datetime.now().isoformat(), "to": args.to, "subject": subject, "from": sender, "status": "sent"}
    except Exception as e:
        status_entry = {"timestamp": datetime.now().isoformat(), "to": args.to, "subject": subject, "status": "failed", "error": str(e)}
        sent_log = loi_dir / "sent.json"
        log_data = json.loads(sent_log.read_text()) if sent_log.exists() else {}
        log_data["initial_send"] = status_entry
        sent_log.write_text(json.dumps(log_data, indent=2))
        sys.exit(f"[ERROR] Send failed: {e}")

    sent_log = loi_dir / "sent.json"
    log_data = json.loads(sent_log.read_text()) if sent_log.exists() else {}
    log_data["initial_send"] = status_entry
    sent_log.write_text(json.dumps(log_data, indent=2))
    print(json.dumps({"status": "sent", "to": args.to, "pdf": str(pdf)}, indent=2))


if __name__ == '__main__':
    main()
