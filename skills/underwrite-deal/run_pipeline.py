#!/usr/bin/env python3
"""
LindaAI — "Underwrite This Deal" pipeline runner.

Chains the whole flow in one command:
  deal JSON  ->  fill the underwriting workbook (normalized)  ->  branded PDF + PPTX

It calls the sibling skills' scripts:
  ../rv-park-autofill/fill_template.py   (fill + normalize)
  ../deal-report/make_report.py          (PDF + slide deck)

Usage:
  python3 run_pipeline.py deal.json
  python3 run_pipeline.py deal.json --template /path/RV_Park_Underwriting.xlsx \
      --out-dir ./out --logo /path/wise-certified-logo.png --no-report

The deal JSON schema is documented in ../rv-park-autofill/deal_input.example.json.
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILL = os.path.join(HERE, "..", "rv-park-autofill", "fill_template.py")
REPORT = os.path.join(HERE, "..", "deal-report", "make_report.py")
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
# prefer the template shipped with the autofill skill; fall back to repo root
_CANDIDATES = [os.path.join(HERE, "..", "rv-park-autofill", "RV_Park_Underwriting.xlsx"),
               os.path.join(REPO, "RV_Park_Underwriting.xlsx")]
DEFAULT_TEMPLATE = next((p for p in _CANDIDATES if os.path.exists(p)), _CANDIDATES[0])
DEFAULT_LOGO = os.path.join(HERE, "..", "deal-report", "assets", "wise-certified-logo.png")


def run(cmd):
    print("  $ " + " ".join(os.path.basename(c) if c.endswith(".py") else c for c in cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.stdout.strip():
        print(r.stdout.strip())
    if r.returncode != 0:
        sys.exit(f"  ! step failed:\n{r.stderr.strip() or r.stdout.strip()}")
    return r.stdout


def main():
    ap = argparse.ArgumentParser(description="Run the full underwrite-this-deal pipeline.")
    ap.add_argument("deal_json")
    ap.add_argument("--template", default=DEFAULT_TEMPLATE)
    ap.add_argument("--out-dir", default=".")
    ap.add_argument("--logo", default=DEFAULT_LOGO)
    ap.add_argument("--no-report", action="store_true", help="fill the workbook only")
    args = ap.parse_args()

    for p in (FILL, args.template, args.deal_json):
        if not os.path.exists(p):
            sys.exit(f"Not found: {p}")
    if not args.no_report and not os.path.exists(REPORT):
        sys.exit(f"Not found: {REPORT}")

    with open(args.deal_json, encoding="utf-8") as fh:
        name = (json.load(fh).get("property_name") or "RV Park").strip()
    os.makedirs(args.out_dir, exist_ok=True)
    base = os.path.join(args.out_dir, f"Wise Certified - {name}")
    xlsx = base + ".xlsx"

    print("[1/2] Filling & normalizing the workbook ...")
    run([sys.executable, FILL, args.deal_json, "--template", args.template, "--out", xlsx])

    made = [xlsx]
    if not args.no_report:
        print("[2/2] Generating branded PDF + PowerPoint ...")
        run([sys.executable, REPORT, xlsx, "--pdf", "--pptx", "--out", base, "--logo", args.logo])
        made += [base + ".pdf", base + ".pptx"]
    else:
        print("[2/2] Skipped report (--no-report).")

    print("\nDone. Deliverables:")
    for m in made:
        print("  • " + m)


if __name__ == "__main__":
    main()
