#!/usr/bin/env python3
"""
Linda-LOI — LOI Generator (LindaAI v1.4)
Builds a professional Letter of Intent as Markdown, HTML, and a signable PDF
with working AcroForm signature fields.

Usage:
    python3 generate_loi.py \\
        --property "123 Main St, City TX" \\
        --type "SFH" \\
        --price 200000 \\
        --earnest 2500 \\
        --dd-days 30 \\
        --close-days 30 \\
        --financing "DSCR + seller carry stack" \\
        --seller-name "Bob Smith" \\
        --seller-email "bob@email.com" \\
        --special "Seller to deliver T12 P&L"

Output: brain/loi/{seller-slug}/{YYYY-MM-DD}/{LOI.md, LOI.html, LOI.pdf, loi.json}
"""

import argparse
import json
import re
from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, Flowable
)


BRAIN = Path.cwd() / "brain" / "loi"
DEFAULT_CONFIG = {
    "buyer_name": "",
    "buyer_entity": "",
    "buyer_address": "",
    "buyer_phone": "",
    "buyer_email": "",
    "default_earnest": 2500,
    "default_dd_days": 30,
    "default_close_days": 30,
    "default_followup_days": [3, 7, 14],
    "signature_image": "",
}


def load_config():
    cfg_path = BRAIN / "config.json"
    if not cfg_path.exists():
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
        cfg_path.write_text(json.dumps(DEFAULT_CONFIG, indent=2))
        return DEFAULT_CONFIG.copy()
    return json.loads(cfg_path.read_text())


def slugify(text):
    s = re.sub(r"[^\w\s-]", "", text.lower())
    s = re.sub(r"[\s_-]+", "-", s).strip("-")
    return s or "seller"


def fmt_money(n):
    return "${:,.0f}".format(float(n))


# ---------- Styles ----------
styles = getSampleStyleSheet()
H1 = ParagraphStyle('h1', parent=styles['Heading1'], fontSize=18,
                   textColor=colors.HexColor('#222'), spaceAfter=14, leading=22)
H2 = ParagraphStyle('h2', parent=styles['Heading2'], fontSize=13,
                   textColor=colors.HexColor('#222'), spaceBefore=14, spaceAfter=8, leading=16)
BODY = ParagraphStyle('body', parent=styles['BodyText'], fontSize=10.5,
                     leading=14.5, spaceAfter=6)
SMALL = ParagraphStyle('small', parent=BODY, fontSize=9.5, textColor=colors.HexColor('#444'))
NET = ParagraphStyle('net', parent=BODY, fontSize=9.5, leading=13,
                    backColor=colors.HexColor('#f0f7f0'),
                    borderPadding=8, leftIndent=4, rightIndent=4, spaceAfter=10)


def opt_table(rows):
    t = Table(rows, colWidths=[1.9 * inch, 4.5 * inch])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f3f3')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#333')),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ]))
    return t


class AcceptanceForm(Flowable):
    """AcroForm signature fields placed inline via absolutePosition()."""
    def __init__(self, width=6.5 * inch, height=1.5 * inch):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def wrap(self, *args):
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        H = self.height
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.HexColor('#222'))
        c.drawString(0, H - 14, "Print Name:")
        x, y = c.absolutePosition(70, H - 20)
        c.acroForm.textfield(name='seller_print_name', tooltip='Print full legal name',
                             x=x, y=y, width=300, height=18,
                             borderColor=colors.HexColor('#888'),
                             fillColor=colors.white, textColor=colors.black,
                             forceBorder=True, fontSize=10)

        c.drawString(0, H - 44, "Signature:")
        x, y = c.absolutePosition(70, H - 50)
        c.acroForm.textfield(name='seller_signature', tooltip='Type your full name to sign',
                             x=x, y=y, width=300, height=22,
                             borderColor=colors.HexColor('#888'),
                             fillColor=colors.white, textColor=colors.black,
                             forceBorder=True, fontSize=11)

        c.drawString(380, H - 44, "Date:")
        x, y = c.absolutePosition(420, H - 50)
        c.acroForm.textfield(name='seller_date', tooltip='MM/DD/YYYY',
                             x=x, y=y, width=110, height=22,
                             borderColor=colors.HexColor('#888'),
                             fillColor=colors.white, textColor=colors.black,
                             forceBorder=True, fontSize=11)


def build_markdown(d, cfg):
    salutation = d['seller_name'] if d['seller_name'].lower() != 'to whom it may concern' else 'To Whom It May Concern'
    return f"""# LETTER OF INTENT TO PURCHASE

**Date:** {d['today']}
**Property:** {d['property']}
**Buyer:** {cfg.get('buyer_entity') or cfg.get('buyer_name','')}

---

{salutation},

This Letter of Intent ("LOI") sets forth the principal terms under which {cfg.get('buyer_entity') or cfg.get('buyer_name','')} ("Buyer") proposes to purchase the property located at {d['property']} ("Property") from the current Owner of Record ("Seller").

## Offer Terms

| Term | Value |
|---|---|
| Purchase Price | {fmt_money(d['price'])} |
| Earnest Money | {fmt_money(d['earnest'])} |
| Financing | {d['financing']} |
| Due Diligence | {d['dd_days']} days |
| Closing | Within {d['close_days']} days of DD expiration |

{("## Special Terms\n\n" + d['special']) if d['special'] else ""}

## General Terms

1. Earnest Money deposited within 3 business days of executed PSA.
2. Buyer may terminate during DD for any reason; full refund of EMD.
3. Marketable title, free and clear, conveyed via warranty deed.
4. Closing costs split per local custom unless modified above.
5. This LOI is non-binding. Binding upon executed PSA only.
6. Confidentiality maintained except as required by law.
7. Expires 7 days from date above unless extended in writing.

## Acceptance

Please sign below and return to {cfg.get('buyer_email','')}.

---

**Buyer:** {cfg.get('buyer_name','')} — {cfg.get('buyer_entity','')} — Date: {d['today']}

**Seller:** ____________________________ Date: ____________

*Generated by LindaAI · Linda-LOI 🚂*
"""


def build_html(d, cfg):
    salutation = d['seller_name'] if d['seller_name'].lower() != 'to whom it may concern' else 'To Whom It May Concern'
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>LOI — {d['property']}</title>
<style>body{{font-family:'Helvetica Neue',Arial,sans-serif;color:#222;max-width:780px;margin:0 auto;padding:50px 40px;line-height:1.55}}h1{{font-size:24px;border-bottom:3px solid #222;padding-bottom:12px}}h2{{font-size:14px;text-transform:uppercase;letter-spacing:1px;color:#444;margin-top:22px}}table{{width:100%;border-collapse:collapse;margin:8px 0 16px}}th,td{{padding:8px 10px;border-bottom:1px solid #eee;text-align:left;font-size:13px}}th{{background:#f3f3f3;font-weight:600;width:35%}}.price{{font-size:20px;font-weight:700}}@media print{{body{{padding:30px}}}}</style>
</head><body>
<h1>LETTER OF INTENT TO PURCHASE</h1>
<p><b>Date:</b> {d['today']}<br><b>Property:</b> {d['property']}<br><b>Buyer:</b> {cfg.get('buyer_entity') or cfg.get('buyer_name','')} — {cfg.get('buyer_email','')}</p>
<p>{salutation},</p>
<p>This Letter of Intent ("LOI") sets forth the principal terms under which <b>{cfg.get('buyer_entity') or cfg.get('buyer_name','')}</b> ("Buyer") proposes to purchase the property located at <b>{d['property']}</b> ("Property") from the current Owner of Record ("Seller").</p>
<h2>Offer Terms</h2>
<table>
<tr><th>Purchase Price</th><td class="price">{fmt_money(d['price'])}</td></tr>
<tr><th>Earnest Money</th><td>{fmt_money(d['earnest'])}</td></tr>
<tr><th>Financing</th><td>{d['financing']}</td></tr>
<tr><th>Due Diligence</th><td>{d['dd_days']} days</td></tr>
<tr><th>Closing</th><td>Within {d['close_days']} days of DD expiration</td></tr>
</table>
{f"<h2>Special Terms</h2><p>{d['special']}</p>" if d['special'] else ""}
<h2>General Terms</h2>
<ol style="font-size:13px;line-height:1.7">
<li>Earnest Money deposited within 3 business days of executed PSA.</li>
<li>Buyer may terminate during DD for any reason; full refund of EMD.</li>
<li>Marketable title, free and clear, conveyed via warranty deed.</li>
<li>Closing costs split per local custom.</li>
<li>This LOI is non-binding. Binding upon executed PSA only.</li>
<li>Confidentiality maintained except as required by law.</li>
<li>Expires 7 days from date above unless extended in writing.</li>
</ol>
<h2>Acceptance</h2>
<p>Please sign and return to <b>{cfg.get('buyer_email','')}</b>.</p>
<p style="margin-top:60px;border-top:1px solid #222;padding-top:8px"><b>Buyer:</b> {cfg.get('buyer_name','')} — {cfg.get('buyer_entity','')} — Date: {d['today']}</p>
<p style="margin-top:40px"><b>Seller Signature:</b> ___________________________ <b>Date:</b> __________</p>
<p style="text-align:center;margin-top:60px;font-size:11px;color:#888">Generated by LindaAI · Linda-LOI 🚂</p>
</body></html>"""


def build_pdf(out_path, d, cfg):
    salutation = d['seller_name'] if d['seller_name'].lower() != 'to whom it may concern' else 'To Whom It May Concern'

    flow = []
    flow.append(Paragraph("LETTER OF INTENT TO PURCHASE", H1))

    header_tbl = Table([
        [Paragraph(f"<b>Date:</b> {d['today']}", BODY),
         Paragraph(f"<b>Property:</b> {d['property']}", BODY)],
        [Paragraph(f"<b>Buyer:</b> {cfg.get('buyer_entity','')}", BODY),
         Paragraph(f"{cfg.get('buyer_name','')} &nbsp;·&nbsp; {cfg.get('buyer_email','')}", BODY)],
    ], colWidths=[3.0 * inch, 3.5 * inch])
    header_tbl.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    flow.append(header_tbl)
    flow.append(Spacer(1, 12))

    flow.append(Paragraph(f"{salutation},", BODY))
    flow.append(Paragraph(
        f'This Letter of Intent ("LOI") sets forth the principal terms under which '
        f'<b>{cfg.get("buyer_entity") or cfg.get("buyer_name","")}</b> ("Buyer") proposes to purchase '
        f'the property located at <b>{d["property"]}</b> ("Property") from the current '
        f'Owner of Record ("Seller").', BODY))

    rows = [
        ['Purchase Price', Paragraph(f'<b><font size=14 color="#222">{fmt_money(d["price"])}</font></b>', BODY)],
        ['Earnest Money Deposit', fmt_money(d['earnest'])],
        ['Financing', d['financing']],
        ['Due Diligence Period', f'{d["dd_days"]} days from execution'],
        ['Closing', f'Within {d["close_days"]} days of DD expiration'],
        ['Title', 'Marketable title, free and clear, conveyed via warranty deed'],
        ['Possession', 'At closing'],
    ]
    flow.append(KeepTogether([
        Paragraph("OFFER TERMS", H2),
        opt_table(rows),
    ]))

    if d['special']:
        flow.append(Paragraph("SPECIAL TERMS", H2))
        flow.append(Paragraph(d['special'], BODY))

    flow.append(Paragraph("GENERAL TERMS", H2))
    terms = [
        "<b>Earnest Money:</b> Deposited with mutually agreed escrow agent within three (3) business days of executed PSA.",
        "<b>Due Diligence:</b> Buyer may conduct inspections, review title, and verify property condition. Buyer may terminate during DD period for any reason and receive full refund of earnest money.",
        "<b>Closing Costs:</b> Customary costs split per local practice unless modified by special terms above.",
        "<b>Buyer's Authority:</b> Buyer represents authority to consummate this transaction.",
        "<b>Non-Binding:</b> This LOI is non-binding. A binding agreement is created only upon execution of a definitive Purchase and Sale Agreement.",
        "<b>Confidentiality:</b> Parties agree to keep terms confidential except as required by law.",
        "<b>Expiration:</b> This LOI expires seven (7) days from date above unless extended in writing.",
    ]
    for i, t in enumerate(terms, 1):
        flow.append(Paragraph(f"{i}.&nbsp;&nbsp;{t}", BODY))

    flow.append(Spacer(1, 14))
    flow.append(Paragraph("ACCEPTANCE", H2))
    flow.append(Paragraph(
        f"Please complete the signature fields below and return the signed PDF to "
        f"<b>{cfg.get('buyer_email','')}</b>.", BODY))
    flow.append(Spacer(1, 10))
    flow.append(KeepTogether([AcceptanceForm()]))

    flow.append(Spacer(1, 18))
    buyer_sig = Table([
        [Paragraph("<b>BUYER</b>", SMALL)],
        [''],
        [Paragraph(f"{cfg.get('buyer_name','')}, Member &nbsp;·&nbsp; {cfg.get('buyer_entity','')} &nbsp;·&nbsp; Date: {d['today']}", SMALL)],
    ], colWidths=[6.5 * inch], rowHeights=[0.22 * inch, 0.45 * inch, 0.25 * inch])
    buyer_sig.setStyle(TableStyle([
        ('LINEBELOW', (0, 1), (0, 1), 0.75, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    flow.append(buyer_sig)

    def footer(canvas, doc_):
        canvas.saveState()
        canvas.setFont("Helvetica-Oblique", 8)
        canvas.setFillColor(colors.HexColor('#999'))
        canvas.drawCentredString(LETTER[0] / 2, 0.4 * inch,
                                 f"Generated by LindaAI · Linda-LOI · Page {doc_.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(
        str(out_path), pagesize=LETTER,
        leftMargin=0.85 * inch, rightMargin=0.85 * inch,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch,
        title=f"LOI - {d['property']}",
    )
    doc.build(flow, onFirstPage=footer, onLaterPages=footer)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--property', required=True)
    p.add_argument('--type', dest='property_type', required=True)
    p.add_argument('--price', type=float, required=True)
    p.add_argument('--earnest', type=float, default=2500)
    p.add_argument('--dd-days', type=int, default=30)
    p.add_argument('--close-days', type=int, default=30)
    p.add_argument('--financing', default="All cash")
    p.add_argument('--seller-name', required=True)
    p.add_argument('--seller-email', required=True)
    p.add_argument('--special', default="")
    args = p.parse_args()

    cfg = load_config()
    today = date.today().isoformat()
    seller_slug = slugify(args.seller_name)
    out_dir = BRAIN / seller_slug / today
    out_dir.mkdir(parents=True, exist_ok=True)

    d = {
        'property': args.property,
        'property_type': args.property_type,
        'price': args.price,
        'earnest': args.earnest,
        'dd_days': args.dd_days,
        'close_days': args.close_days,
        'financing': args.financing,
        'seller_name': args.seller_name,
        'seller_email': args.seller_email,
        'special': args.special,
        'today': today,
    }

    md_path = out_dir / "LOI.md"
    html_path = out_dir / "LOI.html"
    pdf_path = out_dir / "LOI.pdf"

    md_path.write_text(build_markdown(d, cfg))
    html_path.write_text(build_html(d, cfg))
    build_pdf(pdf_path, d, cfg)

    meta = {**d,
        'buyer_name': cfg.get('buyer_name', ''),
        'buyer_entity': cfg.get('buyer_entity', ''),
        'buyer_email': cfg.get('buyer_email', ''),
        'pdf_path': str(pdf_path),
        'html_path': str(html_path),
        'md_path': str(md_path),
    }
    (out_dir / "loi.json").write_text(json.dumps(meta, indent=2))

    print(json.dumps({
        'status': 'ok',
        'out_dir': str(out_dir),
        'pdf': str(pdf_path),
        'html': str(html_path),
        'md': str(md_path),
    }, indent=2))


if __name__ == '__main__':
    main()
