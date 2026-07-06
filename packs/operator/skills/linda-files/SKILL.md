---
name: linda-files
description: This skill should be used when the user asks to "file this document", "filing cabinet", "store this lease", "save this contract", "save this insurance doc", "save this tax form", "file this license", "where's my [document]", "find my [doc type]", "search my files", "digital filing cabinet", "organize my documents", "retrieve a document", "where is the [X] contract", or any request involving document filing, retrieval, or digital records management.
tags: [operator, files, filing, documents, records, contracts, leases]
version: 1.0.0
---

# Linda Files — Digital Filing Cabinet

## Overview

Operators drown in PDFs. Leases, contracts, insurance certs, tax forms, EIN letters, business licenses, articles of organization, operating agreements, NDAs, K-1s, depreciation schedules, vendor agreements — every one of 'em lives in a different folder, and finding the right one in 90 seconds during a closing is an actual skill. Linda Files solves it. Drop any document, and Linda classifies it (type, entity, year), extracts metadata, tags it, files it under a clean taxonomy, and serves it back instantly when asked. Searchable by entity, year, type, or fuzzy keyword. One source of truth for the operator's whole paper life.

## When This Skill Applies

- "File this lease for the Burlington duplex"
- "Save my insurance cert for [Your Business]"
- "Where's the operating agreement for [Your Holding Co LLC]?"
- "Find my 2024 EIN letter"
- "Pull the most recent insurance cert for the duplex"
- "Search my files for anything related to Liz"

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Classify the Document

When Boss drops a doc (PDF, DOCX, image, or paste-text), Linda runs:
1. **Extract text** — PDF text layer or OCR
2. **Detect type** — match against doc-type patterns:
   - Lease (terms, parties, rent, dates)
   - Operating Agreement
   - Articles of Organization / Incorporation
   - EIN Letter (CP 575)
   - Insurance Certificate (ACORD 25)
   - Business License
   - Tax Form (W-2, W-9, 1099-NEC, K-1, 1040, 1065, 1120-S)
   - Bank Statement
   - Loan Document (Note, Mortgage, Deed)
   - Vendor Contract
   - NDA / MSA / SOW
   - Articles of Organization Amendments
   - Property Deed
   - Title Insurance
   - HOA Document
3. **Extract metadata** — parties, entity, effective date, expiration, dollar amounts
4. **Detect entity** — match against `brain/operator/entities.json`

### Step 2: File Path Convention

Linda saves to:
```
brain/operator/files/{entity-slug}/{type}/{YYYY}/{date}-{descriptor}.pdf
```

Example:
- `brain/operator/files/your-business/leases/2026/2026-04-01-burlington-duplex-unit-a.pdf`
- `brain/operator/files/your-holdco/formation/2026/2026-04-22-articles-of-organization.pdf`
- `brain/operator/files/your-business/insurance/2026/2026-03-15-acord-25-liability-renewal.pdf`

If entity unknown → `brain/operator/files/_unfiled/` and ask Boss next session.

### Step 3: Index

Maintain a master index at `brain/operator/files/index.csv`:
```
date_filed, entity, type, sub_type, filename, parties, effective_date, expiration_date, amount, key_terms, full_path, sha256
```

Plus a fast-search index at `brain/operator/files/search-index.json` — keyword → file path mapping for sub-second retrieval.

### Step 4: Set Renewal / Expiration Reminders

If a doc has an expiration (insurance cert, business license, registered agent, lease term), automatically register a reminder via `linda-compliance`:
- 60 days before expiration → first ping
- 30 days → second ping
- 7 days → urgent ping
- Day-of → red alert

### Step 5: Retrieve on Demand

Search modes:
- **Type search** — "show me all leases" → returns indexed list
- **Entity search** — "all docs for [Your Business]" → grouped by type
- **Date range** — "everything filed in March"
- **Keyword fuzzy** — "find anything mentioning Liz" → matches inside parties / counterparties / extracted terms
- **Expiration scan** — "what's expiring in the next 90 days?"

### Step 6: Serve

Return:
- Direct file path (Boss opens in Preview or sends to Liz)
- Summary card with top 5 metadata fields
- Quick-action menu: "open / copy path / send via linda-mail / view related docs"

## Inputs

- File (PDF, DOCX, JPG, PNG) OR pasted text
- Entity (auto-detected or asked once)
- Optional override: doc type + descriptor

## Outputs

- Filed document at canonical path
- Updated `index.csv`
- Updated search index
- (If applicable) reminder set in `linda-compliance`
- Summary card returned in chat

## Example Usage

**User:** (drops PDF) "File this — it's the new insurance cert for the duplex."

**LindaAI:** "Let's gooooooo Boss!" Detects ACORD 25, parties = Travelers Insurance, insured = [Your Business LLC], expiration = 2027-03-15. Files to `brain/operator/files/your-business/insurance/2026/2026-03-15-acord-25-burlington-duplex.pdf`. Sets renewal ping for Jan 15, 2027. "Yeeee Hawww 🤠 — filed. Renewal alert set 60 days out."

**User:** "Pull the most recent operating agreement for [Your Holding Co LLC]."

**LindaAI:** Returns latest filed OA, summary card with members + ownership %, full path.

**User:** "What's expiring in the next 90 days?"

**LindaAI:** Returns 3 items — registered agent (45 days), business license (62 days), liability insurance (88 days).

## Voice & Tone

- Country, helpful. **Boss.**
- "Let's gooooooo!" on file. "Yeeee Hawww 🤠" once filed.
- On retrieval: "Got it right here Boss — second drawer of the cabinet."

## Brand Rules

- Filed docs are stored as-is (don't re-brand customer files)
- Any PDF Linda generates ABOUT the cabinet (e.g. inventory report) gets standard brand: LindaAI top-right, {customer_handle} bottom-right, © 2024–2026

## Cross-Skill Hooks

- **Feeds → linda-compliance** — expirations + renewals registered automatically
- **Feeds → linda-taxprep** — pulls W-2s, 1099s, EIN letters into year-end package
- **Feeds → linda-vendor** — vendor contracts cross-linked to vendor records
- **Feeds → linda-tenants** — leases cross-linked to tenant records
- **Feeds → linda-bgcheck** — authorization forms filed here
- **Feeds → linda-bizops** — count of expiring-soon docs surfaces on dashboard

## Error Handling

- **Can't classify document:** Ask Boss for type + entity, file as-is to `_unfiled/` first.
- **Duplicate file detected (same SHA-256):** Skip re-filing, point to existing.
- **Doc has no expiration but is a renewable type:** Ask Boss to set one or skip reminder.
- **OCR returns garbage:** File anyway with raw filename, mark for manual review.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
