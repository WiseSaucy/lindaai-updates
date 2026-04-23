---
name: linda-license-manager
description: This skill should be used when the user asks to "generate a license key", "create a license", "new license", "license a user", "issue a license", "LindaAI license", "check license", "validate license", "renew license", "revoke license", "expire a license", "update license", "license manager", "who has a license", "list licenses", "deactivate a license", "suspend a license", "license key generator", or any request involving creating, managing, validating, renewing, revoking, or checking LindaAI license keys for users or clients.
version: 1.0.0
---

# LindaAI License Manager

## Overview

The command center for LindaAI licensing. LindaAI uses a license key system to control access to all skills — every skill checks for a valid, active license before running. This skill lets the owner (you) generate new license keys for clients, set expiration dates, choose which plan/tier they get, renew existing licenses, revoke access, and audit who has what. Think of it as the front gate to the ranch — nobody rides without a ticket. 🤠

## License File Location

All license files live at `~/.claude/linda-license.json` on each user's machine. This is the file every LindaAI skill reads before executing.

The master license directory (for tracking all issued licenses) lives at: `brain/licenses/`

## License File Structure

```json
{
  "license_key": "LINDA-XXXX-XXXX-XXXX",
  "licensee_name": "Client Name",
  "licensee_email": "client@email.com",
  "plan": "pro",
  "issued_date": "2026-04-09",
  "expiration_date": "2027-04-09",
  "status": "active",
  "skills_allowed": "all",
  "brand": "LindaAI",
  "notes": ""
}
```

### Field Definitions

| Field | Required | Description |
|-------|----------|-------------|
| `license_key` | Yes | Unique key in format `LINDA-XXXX-XXXX-XXXX`. Generated automatically. |
| `licensee_name` | Yes | Full name of the person or company licensed |
| `licensee_email` | Yes | Contact email for the licensee |
| `plan` | Yes | License tier: `bronze`, `silver`, `gold`, `platinum` |
| `issued_date` | Yes | Date the license was issued (YYYY-MM-DD) |
| `expiration_date` | Yes | Date the license expires (YYYY-MM-DD). After this date, all skills stop working. |
| `status` | Yes | Current status: `active`, `expired`, `suspended`, `revoked` |
| `skills_allowed` | Yes | Which skills this license grants access to: `all` or a JSON array of skill names |
| `brand` | Yes | Always `"LindaAI"` |
| `notes` | No | Internal notes about this license |

### Plan Tiers

| Plan | Skills Included | Description |
|------|----------------|-------------|
| `bronze` | Basic skills (brain-dump, email-drafter, follow-up, content-batch, meeting-to-actions) | $500/yr — Entry-level, good for individual users getting started |
| `silver` | All skills except grant suite and advanced underwriting | $1,000/yr — Professional tier, covers most business needs |
| `gold` | All skills | $1,500/yr — Full access for businesses and power users |
| `platinum` | All skills + license management | $4,000 one-time — Owner-level, can generate and manage other licenses |

## How It Works

### Action: Generate a New License

When the user says "generate a license" or "create a license key":

1. Ask for the required details:
   - **Licensee name** — Who is this license for?
   - **Licensee email** — Their contact email
   - **Plan tier** — bronze, silver, gold, or platinum
   - **Duration** — How long? (e.g., 1 month, 3 months, 6 months, 1 year)
   - **Skills restriction** — All skills or specific ones only?

2. Generate a unique license key:
   - Format: `LINDA-[YEAR]-[4 RANDOM ALPHANUMERIC]-[4 RANDOM ALPHANUMERIC]`
   - Example: `LINDA-2026-K7XM-P3RW`
   - Use uppercase letters and numbers only, no ambiguous characters (no 0/O, 1/I/L)

3. Calculate the expiration date based on the duration.

4. Create the license JSON:

```json
{
  "license_key": "LINDA-2026-K7XM-P3RW",
  "licensee_name": "Jane Smith",
  "licensee_email": "jane@company.com",
  "plan": "pro",
  "issued_date": "2026-04-09",
  "expiration_date": "2027-04-09",
  "status": "active",
  "skills_allowed": "all",
  "brand": "LindaAI",
  "notes": ""
}
```

5. Save a copy to the master license directory:
   `brain/licenses/[licensee-name-slug]-[license-key].json`

6. Present the license to the owner:

> 🤠 "New license saddled up and ready to ride:"
>
> **License Key:** `LINDA-2026-K7XM-P3RW`
> **For:** Jane Smith (jane@company.com)
> **Plan:** Pro
> **Valid:** 2026-04-09 through 2027-04-09
> **Skills:** All Pro-tier skills
>
> "To activate, the client needs this license file saved to `~/.claude/linda-license.json` on their machine. Want me to draft an email with setup instructions?"

### Action: Validate / Check a License

When the user says "check license" or "validate license":

1. Read `~/.claude/linda-license.json`
2. Check all validation criteria:
   - File exists?
   - `status` is `active`?
   - `expiration_date` is in the future?
   - `license_key` format is valid?
   - `plan` matches a known tier?

3. Report status:

> 🤠 "License check complete:"
>
> **Status:** Active / Expired / Suspended / Revoked
> **Licensee:** [name]
> **Plan:** [tier]
> **Expires:** [date] ([X days remaining])
> **Skills:** [all or list]

### Action: Renew a License

When the user says "renew license" or "extend license":

1. Ask which license to renew (by name or key)
2. Ask for the new duration
3. Update the `expiration_date` in the master record
4. Generate the updated license JSON for the client
5. Offer to draft a renewal confirmation email

> 🤠 "License renewed — [name] is good to ride through [new expiration date]."

### Action: Revoke / Suspend a License

When the user says "revoke license" or "suspend license":

- **Suspend** — Sets `status` to `suspended`. Can be reactivated later.
- **Revoke** — Sets `status` to `revoked`. Permanent. The license key is dead.

Update the master record in `brain/licenses/`.

> 🤠 "License for [name] has been [suspended/revoked]. Their skills will stop working the next time they try to run one."

**Important:** Revoking/suspending only updates YOUR master record. The client's local `linda-license.json` still exists on their machine. The actual enforcement happens because:
- If you update their file remotely (via email with new file), it takes effect immediately
- If you can't update their file, you'd need to build a remote validation check (future enhancement)

For now, the practical approach is: when you revoke someone, send them an updated `linda-license.json` with `status: "revoked"` and ask them to replace their file. Or, set the expiration date to today's date so it expires immediately.

### Action: List All Licenses

When the user says "list licenses" or "who has a license":

1. Read all files in `brain/licenses/`
2. Present a summary table:

| Licensee | Email | Plan | Key | Status | Expires | Days Left |
|----------|-------|------|-----|--------|---------|-----------|
| Jane Smith | jane@co.com | Pro | LINDA-2026-K7XM-P3RW | Active | 2027-04-09 | 365 |
| Bob Jones | bob@co.com | Starter | LINDA-2026-M4FN-R8JT | Expired | 2026-03-01 | -39 |

3. Flag any licenses that are:
   - Expiring within 30 days (🟡)
   - Already expired (🔴)
   - Suspended or revoked (⛔)

### Action: Generate Client Setup Instructions

When the user says "send setup instructions" or after generating a new license:

Draft an email (or message) with:

```
Subject: Your LindaAI License — Setup Instructions

Hey [Name],

Welcome to LindaAI! 🤠 Here's your license key and setup instructions:

Your License Key: [KEY]
Plan: [TIER]
Valid Through: [DATE]

SETUP (takes 30 seconds):
1. Open your terminal
2. Run this command to create your license file:

   echo '[LICENSE JSON]' > ~/.claude/linda-license.json

3. That's it — LindaAI skills are now active. Try running any slash command to test.

If you run into any trouble, just holler.

[Your name]
```

Use the Gmail draft tool to create this as a draft.

## License Validation Block (Reference)

This is the exact validation block that exists in every LindaAI skill. It runs before anything else:

```markdown
### License Check

Before proceeding, verify the LindaAI license:

1. Read `~/.claude/linda-license.json`
2. If the file does not exist → stop and show the no-license message
3. If `expiration_date` is in the past → stop and show the expired message
4. If `status` is not `active` → stop and show the inactive message
5. If the skill name is not in `skills_allowed` (and skills_allowed is not "all") → stop and show the not-included message
6. If all checks pass → proceed to Step 0
```

### Denial Messages

**No license found:**
> 🤠 "Whoa there, partner — no LindaAI license found on this machine. You'll need a valid license to use LindaAI skills. Reach out to get set up and we'll have you in the saddle in no time."

**License expired:**
> 🤠 "Whoa there, partner — your LindaAI license expired on [date]. Reach out to renew and we'll get you back in the saddle." 🏇

**License suspended/revoked:**
> 🤠 "Whoa there, partner — your LindaAI license is currently [status]. Reach out to get this sorted and we'll have you riding again in no time."

**Skill not included in plan:**
> 🤠 "This skill isn't included in your [plan] plan. Upgrade your LindaAI license to unlock it — reach out and we'll get you set up."

🤠 *Generated by LindaAI* 🏇


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
