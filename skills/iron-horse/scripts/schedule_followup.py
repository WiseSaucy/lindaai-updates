#!/usr/bin/env python3
"""
Linda-LOI — Follow-Up Scheduler (LindaAI v1.4)
Adds follow-up entries to brain/loi/queue.json. Runner processes daily.

Usage:
    python3 schedule_followup.py --loi-dir <path> --to <email> --seller-name <name> --property <addr> --days "3,7,14"
"""

import argparse
import json
from datetime import date, timedelta
from pathlib import Path


BRAIN = Path.cwd() / "brain" / "loi"


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--loi-dir', required=True)
    p.add_argument('--to', required=True)
    p.add_argument('--seller-name', required=True)
    p.add_argument('--property', required=True)
    p.add_argument('--days', default="3,7,14")
    args = p.parse_args()

    days = [int(x.strip()) for x in args.days.split(",") if x.strip()]
    today = date.today()
    queue_path = BRAIN / "queue.json"
    queue = json.loads(queue_path.read_text()) if queue_path.exists() else {"pending": []}

    loi_dir = str(Path(args.loi_dir).expanduser().resolve())
    for i, d in enumerate(days, start=1):
        send_date = (today + timedelta(days=d)).isoformat()
        queue["pending"].append({
            "send_on": send_date,
            "touch": i,
            "loi_dir": loi_dir,
            "to": args.to,
            "seller_name": args.seller_name,
            "property": args.property,
            "status": "pending",
        })

    queue_path.parent.mkdir(parents=True, exist_ok=True)
    queue_path.write_text(json.dumps(queue, indent=2))
    print(json.dumps({"status": "queued", "count": len(days), "days": days}, indent=2))


if __name__ == '__main__':
    main()
