#!/usr/bin/env python3
"""
Linda-LOI — Follow-Up Runner (LindaAI v1.4)
Runs daily via launchd. Reads brain/loi/queue.json and sends due follow-ups.
Idempotent — marks each entry 'sent' so it won't fire twice.
"""

import json
import sys
from datetime import date, datetime
from pathlib import Path

# Resolve project root by looking for brain/loi/queue.json upward
def find_brain():
    p = Path(__file__).resolve()
    for parent in [Path.cwd()] + list(p.parents):
        candidate = parent / "brain" / "loi"
        if candidate.exists():
            return candidate
    return Path.cwd() / "brain" / "loi"


BRAIN = find_brain()
sys.path.insert(0, str(Path(__file__).parent))
from send_loi import send  # type: ignore


TEMPLATES = {
    1: {
        "subject": "Following up on my offer for {property}",
        "body": """Hi {seller_name},

Just wanted to make sure my LOI for {property} hit your inbox. Happy to walk through any of the terms or adjust where it makes sense.

Looking forward to hearing back.

Best,
{buyer_name}
""",
    },
    2: {
        "subject": "Quick question on {property}",
        "body": """Hi {seller_name},

Hope you're well. I'm a serious buyer with funds in place and can close fast. Is there anything specific holding you back on the offer? I'm flexible on terms — happy to restructure to make it work for you.

Best,
{buyer_name}
""",
    },
    3: {
        "subject": "Final check-in on {property}",
        "body": """Hi {seller_name},

This is my last touch on the LOI for {property}. If now isn't the right time, no worries — just let me know and I'll close the file. If you'd like to move forward or revise terms, I'm all ears.

Best,
{buyer_name}
""",
    },
}


def template(touch):
    return TEMPLATES.get(touch, TEMPLATES[3])


def send_followup(entry):
    loi_dir = Path(entry["loi_dir"])
    meta_path = loi_dir / "loi.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    buyer_name = meta.get("buyer_name", "")
    pdf = loi_dir / "LOI.pdf"

    salutation = entry['seller_name'] if entry['seller_name'].lower() != 'to whom it may concern' else 'To Whom It May Concern'
    tpl = template(entry["touch"])
    subject = tpl["subject"].format(property=entry["property"])
    body = tpl["body"].format(
        seller_name=salutation,
        property=entry["property"],
        buyer_name=buyer_name,
    )

    try:
        send(entry["to"], subject, body, str(pdf) if pdf.exists() else None)
        return True, ""
    except Exception as e:
        return False, str(e)


def main():
    queue_path = BRAIN / "queue.json"
    if not queue_path.exists():
        print("No queue file. Nothing to do.")
        return

    queue = json.loads(queue_path.read_text())
    today_iso = date.today().isoformat()
    sent_count = 0
    failed_count = 0

    for entry in queue.get("pending", []):
        if entry.get("status") != "pending":
            continue
        if entry["send_on"] > today_iso:
            continue

        ok, err = send_followup(entry)
        entry["status"] = "sent" if ok else "failed"
        entry["sent_at"] = datetime.now().isoformat()
        entry["error"] = err if not ok else ""
        if ok:
            sent_count += 1
        else:
            failed_count += 1

        loi_dir = Path(entry["loi_dir"])
        sent_log = loi_dir / "sent.json"
        log_data = json.loads(sent_log.read_text()) if sent_log.exists() else {}
        log_data.setdefault("followups", []).append({
            "touch": entry["touch"],
            "sent_at": entry["sent_at"],
            "to": entry["to"],
            "ok": ok,
            "error": err if not ok else "",
        })
        sent_log.write_text(json.dumps(log_data, indent=2))

    queue_path.write_text(json.dumps(queue, indent=2))

    log_path = BRAIN / "runner.log"
    with log_path.open("a") as f:
        f.write(f"[{datetime.now().isoformat()}] sent={sent_count} failed={failed_count}\n")

    print(json.dumps({"sent": sent_count, "failed": failed_count}, indent=2))


if __name__ == '__main__':
    main()
