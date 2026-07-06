---
name: linda-parts
description: This skill should be used when the user asks to "check parts inventory", "van stock", "warehouse stock", "parts pulse", "low on parts", "what's in the truck", "restock van", "common job kit", "parts I need", "order parts", "consume a part", "log parts used", "minimum stock alerts", or any request involving parts and inventory management for HVAC and plumbing.
version: 1.0.0
tags: [hvac, plumbing, inventory, parts, supply-chain]
---

# Parts / Inventory Pulse

## Overview

Tracks parts across the warehouse and every service van. Knows what's on each truck, what's running low, what to restock tonight, what's tied up in common-job kits (capacitor + contactor + UV bulb + drain pan tab, etc.). LindaAI consumes parts when `/linda-ticket` writes them up, alerts when stock dips below the minimum, and produces the daily restock list for the warehouse.

## When This Skill Applies

- User wants to check what's on a van or in the warehouse
- User wants today's restock list
- User says "we used 2 of 45+5 capacitor on the Henderson job"
- User asks "what's running low?"
- User wants to define or update a common-job kit
- User wants to order parts

## How It Works

### Step 0: License Check
Standard LindaAI license verification.

### Step 1: Inventory Schema

`brain/hvac-plumbing/inventory/parts.json`:
```json
{
  "parts": [
    {
      "sku": "CAP-45-5",
      "name": "Run capacitor 45+5 µF 440V",
      "trade": "HVAC",
      "cost": 18.50,
      "sell": 89,
      "supplier": "ABC Supply",
      "min_per_van": 2,
      "min_warehouse": 12,
      "kit_member": ["common-cooling"]
    }
  ]
}
```

Stock per location at `brain/hvac-plumbing/inventory/stock.json`:
```json
{
  "warehouse": { "CAP-45-5": 18, "CONT-2P-30": 9 },
  "vans": {
    "T1": { "CAP-45-5": 3, "CONT-2P-30": 2 },
    "T2": { "CAP-45-5": 0 }
  }
}
```

### Step 2: Consume on Ticket Close

When `/linda-ticket` finalizes, deduct each part from the assigned tech's van. If van goes below `min_per_van`, queue a restock from warehouse for the next morning. If warehouse goes below `min_warehouse`, queue a purchase order.

### Step 3: Common-Job Kits

`brain/hvac-plumbing/inventory/kits.json`:
```json
{
  "kits": [
    {
      "id": "common-cooling",
      "name": "Common AC repair kit",
      "items": [
        { "sku": "CAP-45-5", "qty": 2 },
        { "sku": "CAP-35-5", "qty": 2 },
        { "sku": "CONT-2P-30", "qty": 2 },
        { "sku": "R410A-2LB", "qty": 1 }
      ]
    }
  ]
}
```

Each van's required minimums = sum of kit memberships, plus any van-specific overrides.

### Step 4: Daily Pulse

Run on demand or via `/loop`:

```markdown
# Parts Pulse — {YYYY-MM-DD}

## Critical (Below Min, Today's Jobs At Risk)
| SKU | Name | Where | On hand | Min | Need |
|-----|------|-------|--------:|----:|-----:|
| CAP-45-5 | Run cap 45+5 | Van T2 | 0 | 2 | 2 |

## Low (Restock Tonight)
| SKU | Name | Where | On hand | Min |
|-----|------|-------|--------:|----:|
| CONT-2P-30 | Contactor 2P 30A | Warehouse | 9 | 12 |

## Purchase Order Suggestions
| Supplier | Items | Est. cost |
|----------|-------|----------:|
| ABC Supply | 24× CAP-45-5, 12× CONT-2P-30 | $612 |

🤠 *Tracked by LindaAI* 🏇
```

### Step 5: Order Parts

When Boss says "order it," generate a PO markdown + branded PDF:
```
brain/hvac-plumbing/inventory/pos/PO-{YYYYMMDD}-{NNN}.pdf
```

PDF brand: LindaAI top-right, {customer_handle} bottom-right, © 2024–2026.

## Example Usage

**User:** "Used 2 of CAP-45-5 and 1 R410A-2LB on Henderson, tech Mike."

**LindaAI:** Deducts from Van T1, sees Mike now has 1 cap (below min of 2), queues restock. "Yeeee Hawww 🤠 — logged. Mike's cap stock dropped to 1, restock queued from warehouse for tomorrow morning."

**User:** "What's the parts pulse?"

**LindaAI:** Returns the markdown report.

**User:** "Restock all vans for tomorrow."

**LindaAI:** Calculates van-by-van pulls from warehouse, prints pull sheets.

**User:** "Order the PO."

**LindaAI:** Generates PO PDF for ABC Supply with the suggested quantities.

## Voice & Tone

- Country, direct, **Boss**.
- Surface critical shortages first — they're tomorrow's lost jobs.

## Error Handling

- **Negative stock detected:** Don't go below zero — flag as data error, ask Boss to physical-count.
- **SKU not in catalog:** Offer to add it on the fly.
- **Multiple suppliers for same SKU:** Default to lowest cost, let Boss override.
- **No license:** Country howdy and stop.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
