---
name: invoice-generator
description: This skill should be used when the user asks to "create an invoice", "generate an invoice", "make an invoice", "invoice a client", "bill a client", "send an invoice", "invoice for services", "billing", "create a bill", "generate a bill", "invoice template", "new invoice", "invoice number", "payment due", "invoice for {client name}", "charge for", "bill for", "create receipt", or anything related to generating, creating, or managing invoices and billing documents.
version: 1.0.0
---

# Invoice Generator

## Overview

LindaAI generates professional invoices as structured markdown files. Hand over your client details, services rendered, amounts, and payment terms, and LindaAI produces a clean, formatted invoice with automatic calculations (subtotals, tax, totals), unique invoice numbering, and payment instructions. Invoices are saved to an organized client folder structure for easy retrieval and record-keeping.

## When This Skill Applies

- User asks to create, generate, or make an invoice
- User wants to bill a client for services
- User mentions invoicing, billing, or creating a bill
- User says "invoice {client name} for {amount/service}"
- User wants a payment receipt or billing document
- User asks about outstanding invoices or payment tracking
- User needs to re-issue or update an existing invoice

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
5. **Server Verification (tamper check):** If the license file contains an `api_url` field, use WebFetch to check `{api_url}/v1/licenses/validate/{license_key}`. Parse the JSON response.
   - If the server responds with `"valid": false`, the local license has been tampered with. Stop and tell the user:
     > 🤠 "Hold up, partner — your license didn't check out with the server. Something's not matching up. Reach out to support to get this straightened out."
     Then use WebFetch to POST a tamper alert to `{api_url}/v1/licenses/tamper-alert` with JSON body: `{"license_key": "[key]", "local_expiration": "[local expiration_date]", "server_expiration": "[server expires from response]", "local_status": "[local status]", "details": "Local file passed but server validation failed"}`. Do not proceed.
   - If the server is unreachable or returns an error, proceed anyway (allow offline use — don't block paying customers because of a server hiccup).
   - If the server responds with `"valid": true`, proceed.
6. If all checks pass, proceed.

### Step 1: Gather Invoice Details

Extract from the user's message (ask for anything missing that is essential):

**Required:**
| Field | Description |
|-------|-------------|
| Client Name | Person or company being billed |
| Services/Items | What was delivered or provided |
| Amounts | Dollar amount for each line item |

**Optional (use defaults if not provided):**
| Field | Default |
|-------|---------|
| Invoice Date | Today's date |
| Due Date | Net 30 (30 days from invoice date) |
| Invoice Number | Auto-generated: `INV-{YYYYMMDD}-{sequence}` |
| Tax Rate | 0% (no tax unless specified) |
| Payment Terms | Net 30 |
| Payment Method | Check, Zelle, wire, or as configured |
| Notes | None |
| From (Business) | Read from brain config or ask |

### Step 2: Look Up Business Info

Check for existing business configuration:

1. Read `brain/invoices/config.md` if it exists — this has the user's business name, address, payment details
2. If no config exists, ask the user for their business info on the first invoice, then save it as `brain/invoices/config.md` for future use

Business config template (`brain/invoices/config.md`):
```markdown
# Invoice Configuration

## Business Info
- **Business Name:** {name}
- **DBA:** {dba if any}
- **Address:** {street, city, state, zip}
- **Phone:** {phone}
- **Email:** {email}
- **Website:** {url}

## Payment Methods
- **Zelle:** {email or phone}
- **Wire:** {bank, routing, account}
- **Check payable to:** {name}
- **Other:** {PayPal, Venmo, etc.}

## Default Terms
- **Payment Due:** Net 30
- **Late Fee:** 0%
- **Tax Rate:** 0%

## Invoice Numbering
- **Prefix:** INV
- **Last Number:** {auto-updated}
```

### Step 3: Look Up Client Info

Check if the client exists in `brain/people/` for address and contact details. If found, auto-populate the client's billing info.

### Step 4: Calculate Totals

| Calculation | Formula |
|------------|---------|
| Line Item Total | quantity x unit price |
| Subtotal | sum of all line item totals |
| Tax | subtotal x tax rate |
| Discount | subtotal x discount rate (if any) |
| **Total Due** | subtotal + tax - discount |

### Step 5: Generate Invoice Number

Format: `INV-{YYYYMMDD}-{NNN}`

1. Check `brain/invoices/config.md` for the last used number
2. Increment by 1
3. Update the config with the new last number

If no config exists, start at `INV-{YYYYMMDD}-001`.

### Step 6: Generate the Invoice

Create the invoice file at:
```
brain/invoices/{client-slug}/INV-{YYYYMMDD}-{NNN}.md
```

Create the `brain/invoices/` and client subdirectory if they do not exist.

### Step 7: Update Invoice Log

Maintain a master log at `brain/invoices/log.md`:

```markdown
# Invoice Log

| Invoice # | Date | Client | Amount | Status | Due Date |
|-----------|------|--------|--------|--------|----------|
| INV-20260302-001 | 2026-03-02 | ABC Motors | $5,000.00 | Sent | 2026-04-01 |
```

Append the new invoice to this log. Create the log file if it does not exist.

### Currency Support

Support multiple currencies. Default to USD unless the user specifies otherwise.

| Currency | Symbol | Code | Format Example |
|----------|--------|------|---------------|
| US Dollar | $ | USD | $1,234.56 |
| Euro | EUR | EUR | EUR 1.234,56 |
| British Pound | GBP | GBP | GBP 1,234.56 |
| Canadian Dollar | CAD | CAD | CAD $1,234.56 |
| Australian Dollar | AUD | AUD | AUD $1,234.56 |
| Mexican Peso | MXN | MXN | MXN $1,234.56 |

If the user says "invoice in euros" or "bill in GBP", use the appropriate currency symbol and code throughout the invoice. Store the currency in the invoice config for consistency.

## Output Format — Markdown Version

Save a markdown version to `brain/invoices/{client-slug}/INV-{YYYYMMDD}-{NNN}.md`:

```markdown
# INVOICE

---

**From:**
{Business Name}
{Address Line 1}
{City, State ZIP}
{Phone} | {Email}
{Website}

---

**Bill To:**
{Client Name}
{Client Company (if applicable)}
{Client Address}
{Client Email}

---

| | |
|---|---|
| **Invoice Number** | {INV-YYYYMMDD-NNN} |
| **Invoice Date** | {YYYY-MM-DD} |
| **Due Date** | {YYYY-MM-DD} |
| **Payment Terms** | {Net 30 / Due on receipt / etc.} |
| **Currency** | {USD / EUR / GBP / etc.} |

---

## Services

| # | Description | Qty | Unit Price | Amount |
|---|-------------|-----|-----------|--------|
| 1 | {Service description} | {qty} | ${price} | ${total} |
| 2 | {Service description} | {qty} | ${price} | ${total} |
| 3 | {Service description} | {qty} | ${price} | ${total} |

---

| | |
|---|---|
| **Subtotal** | ${subtotal} |
| **Tax ({rate}%)** | ${tax} |
| **Discount** | -${discount} |
| **TOTAL DUE** | **${total}** |

---

## Payment Instructions

{Payment method details — Zelle, wire, check, etc.}

Please include invoice number **{INV-YYYYMMDD-NNN}** with your payment.

---

## Notes

{Any additional notes, late fee policy, thank you message}

---

*Thank you for your business.*

🤠 *Generated by LindaAI* 🏇
```

## Output Format — HTML Version (Primary)

Also save an HTML version to `brain/invoices/{client-slug}/INV-{YYYYMMDD}-{NNN}.html` that can be opened in any browser and printed or saved as PDF:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Invoice {INV-YYYYMMDD-NNN}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Helvetica Neue', Arial, sans-serif; color: #333; max-width: 800px; margin: 0 auto; padding: 40px; }
        .header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 40px; border-bottom: 3px solid #333; padding-bottom: 20px; }
        .header h1 { font-size: 36px; font-weight: 700; letter-spacing: 2px; color: #333; }
        .company-info { text-align: right; font-size: 13px; line-height: 1.6; color: #555; }
        .addresses { display: flex; justify-content: space-between; margin-bottom: 30px; }
        .bill-to, .invoice-details { width: 48%; }
        .bill-to h3, .invoice-details h3 { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #999; margin-bottom: 8px; }
        .bill-to p, .invoice-details p { font-size: 14px; line-height: 1.6; }
        .invoice-details table { width: 100%; font-size: 14px; }
        .invoice-details td { padding: 4px 0; }
        .invoice-details td:first-child { font-weight: 600; color: #555; }
        .invoice-details td:last-child { text-align: right; }
        table.line-items { width: 100%; border-collapse: collapse; margin: 30px 0; }
        table.line-items th { background: #333; color: #fff; padding: 12px 15px; text-align: left; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }
        table.line-items th:last-child, table.line-items td:last-child { text-align: right; }
        table.line-items th:nth-child(3), table.line-items td:nth-child(3),
        table.line-items th:nth-child(4), table.line-items td:nth-child(4) { text-align: center; }
        table.line-items td { padding: 12px 15px; border-bottom: 1px solid #eee; font-size: 14px; }
        table.line-items tr:last-child td { border-bottom: 2px solid #333; }
        .totals { width: 300px; margin-left: auto; margin-bottom: 40px; }
        .totals table { width: 100%; }
        .totals td { padding: 8px 0; font-size: 14px; }
        .totals td:last-child { text-align: right; }
        .totals tr.total { border-top: 2px solid #333; }
        .totals tr.total td { font-size: 18px; font-weight: 700; padding-top: 12px; }
        .payment-info { background: #f8f8f8; padding: 20px; border-radius: 4px; margin-bottom: 30px; }
        .payment-info h3 { font-size: 14px; font-weight: 600; margin-bottom: 10px; }
        .payment-info p { font-size: 13px; line-height: 1.6; color: #555; }
        .notes { font-size: 13px; color: #777; line-height: 1.6; margin-bottom: 30px; }
        .notes h3 { font-size: 14px; color: #333; margin-bottom: 8px; }
        .footer { text-align: center; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #999; }
        .status-badge { display: inline-block; padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; text-transform: uppercase; }
        .status-unpaid { background: #fff3cd; color: #856404; }
        .status-paid { background: #d4edda; color: #155724; }
        @media print { body { padding: 20px; } .header { border-bottom-color: #333; } }
    </style>
</head>
<body>
    <div class="header">
        <h1>INVOICE</h1>
        <div class="company-info">
            <strong>{Business Name}</strong><br>
            {Address}<br>
            {City, State ZIP}<br>
            {Phone}<br>
            {Email}<br>
            {Website}
        </div>
    </div>

    <div class="addresses">
        <div class="bill-to">
            <h3>Bill To</h3>
            <p>
                <strong>{Client Name}</strong><br>
                {Client Company}<br>
                {Client Address}<br>
                {Client Email}
            </p>
        </div>
        <div class="invoice-details">
            <table>
                <tr><td>Invoice Number</td><td>{INV-YYYYMMDD-NNN}</td></tr>
                <tr><td>Invoice Date</td><td>{YYYY-MM-DD}</td></tr>
                <tr><td>Due Date</td><td>{YYYY-MM-DD}</td></tr>
                <tr><td>Payment Terms</td><td>{Net 30}</td></tr>
                <tr><td>Status</td><td><span class="status-badge status-unpaid">Unpaid</span></td></tr>
            </table>
        </div>
    </div>

    <table class="line-items">
        <thead>
            <tr>
                <th>#</th>
                <th>Description</th>
                <th>Qty</th>
                <th>Unit Price</th>
                <th>Amount</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>{Service description}</td>
                <td>1</td>
                <td>{currency}{price}</td>
                <td>{currency}{total}</td>
            </tr>
            <!-- Additional line items as needed -->
        </tbody>
    </table>

    <div class="totals">
        <table>
            <tr><td>Subtotal</td><td>{currency}{subtotal}</td></tr>
            <tr><td>Tax ({rate}%)</td><td>{currency}{tax}</td></tr>
            <tr><td>Discount</td><td>-{currency}{discount}</td></tr>
            <tr class="total"><td>TOTAL DUE</td><td>{currency}{total}</td></tr>
        </table>
    </div>

    <div class="payment-info">
        <h3>Payment Instructions</h3>
        <p>{Payment method details}</p>
        <p>Please include invoice number <strong>{INV-YYYYMMDD-NNN}</strong> with your payment.</p>
    </div>

    <div class="notes">
        <h3>Notes</h3>
        <p>{Any additional notes}</p>
    </div>

    <div class="footer">
        <p>Thank you for your business.</p>
    </div>
</body>
</html>
```

**To convert to PDF:** Open the HTML file in any web browser, press Ctrl/Cmd+P, and select "Save as PDF". The styles are print-optimized.

## Example Usage

**User:** "Invoice John Smith at ABC Motors for a connection fee — $4,500"

**AI:** Checks for existing business config and client info. Generates invoice INV-20260302-001 with one line item: "Connection Fee — Vehicle Transaction Coordination" for $4,500. Saves to `brain/invoices/abc-motors/INV-20260302-001.md`. Updates the invoice log.

**User:** "Create an invoice for Sarah Johnson. Services: TC fee $2,000 and document preparation $500. Net 15 terms."

**AI:** Generates invoice with 2 line items, subtotal of $2,500, Net 15 due date, saves to client folder.

**User:** "Bill XYZ Corp for consulting — 10 hours at $150/hour"

**AI:** Generates invoice with line item "Consulting Services — 10 hours @ $150/hr" totaling $1,500.

**User:** "Show me all outstanding invoices"

**AI:** Reads `brain/invoices/log.md`, filters for invoices with status "Sent" or "Outstanding" where due date has not passed, presents the list.

**User:** "Mark invoice INV-20260302-001 as paid"

**AI:** Updates the invoice log status to "Paid" and adds a payment date. Updates the invoice file with a "PAID" stamp. In the HTML version, changes the status badge from "Unpaid" (yellow) to "Paid" (green).

**User:** "Invoice Rivera Auto Group for 3 vehicle TCs at $2,000 each, plus document prep $500. Due in 15 days. Use EUR."

**AI:** Generates invoice with 2 line items: "Vehicle Transaction Coordination (3 units @ EUR 2,000)" = EUR 6,000 and "Document Preparation" = EUR 500. Total: EUR 6,500. Due date: 15 days from today. Both markdown and HTML versions saved with EUR formatting.

## Example Generated HTML Output

When the user opens `brain/invoices/abc-motors/INV-20260302-001.html` in a browser, they see a clean, professional invoice with:
- Company header with logo area and contact info (right-aligned)
- "INVOICE" title (bold, large)
- Bill-To section with client details
- Invoice details table (number, date, due date, terms, status badge)
- Line items table with dark header row, clean borders, right-aligned amounts
- Totals section (right-aligned: subtotal, tax, discount, bold total)
- Payment instructions in a light gray box
- Notes section
- "Thank you for your business" footer

The invoice is print-ready with optimized @media print styles. Opening the browser print dialog produces a clean single-page PDF.

## Error Handling

- **If `brain/invoices/` directory does not exist:** Create it automatically along with the client subdirectory. Do not error — initialize silently.
- **If `brain/invoices/config.md` does not exist (first invoice):** Ask the user for their business info (name, address, phone, email, payment methods). Create `brain/invoices/config.md` with their answers. Inform them: "I saved your business info so future invoices will auto-populate. You can update it anytime at `brain/invoices/config.md`."
- **If user does not provide a client name:** Ask specifically: "Who should this invoice be billed to? I need at least a client name."
- **If user does not provide amounts or services:** Ask specifically: "What services or items should I include on this invoice, and what are the amounts?"
- **If user provides ambiguous amounts (e.g., "a few thousand"):** Ask for exact numbers: "I need specific dollar amounts for each line item. Can you give me the exact figures?"
- **If the invoice number sequence has a gap or conflict:** Read all existing invoice files to determine the true next number. If `config.md` says the last number was 005 but an INV-007 file exists, use INV-008. Always trust the actual files over the config.
- **If an invoice file already exists with the same number:** Do not overwrite. Increment the sequence number and inform the user: "INV-{number} already exists. Created as INV-{next number} instead."
- **If the client has no entry in `brain/people/`:** Proceed without it, but suggest: "I don't have {client name} in your contacts. Want me to create a contact entry for them?"
- **If tax rate is unclear:** Default to 0% (no tax) and note on the invoice: "Tax not included. Consult your accountant for applicable tax obligations."
- **If currency is not recognized:** Default to USD and inform: "I didn't recognize the currency '{input}'. Using USD. Supported currencies: USD, EUR, GBP, CAD, AUD, MXN."
- **If the user asks to edit an existing invoice:** Read the existing file, make the requested changes, update the "Last Modified" date, and add a note in the invoice log: "Revised on {date}". Do not delete the original — create a revision suffix if needed (e.g., INV-20260302-001-R1).
- **If writing the HTML file fails:** Fall back to markdown-only output and inform the user: "HTML generation encountered an issue. Saved the markdown version instead. You can still view it in any text editor."


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
