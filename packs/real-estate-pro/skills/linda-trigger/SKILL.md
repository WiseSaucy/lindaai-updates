---
name: linda-trigger
description: Run a deal through the Sauce Underwriter — Boss's locked formula for wholesale MAO and fix-and-flip walk-away. Use when the user says "underwrite this deal", "what should I offer", "MAO", "max allowable offer", "Sauce Underwriter", "run the numbers", "wholesale MAO", "fix and flip walk-away", "is this a good wholesale", "is this a good flip", "what's the buy price", "what's the dispo price", "run a flip analysis", "/linda-trigger", "pull the trigger", "trigger on this deal", "trigger the MAO", "linda trigger", "/linda-trigger", "/linda-deals", "Sauce numbers", "Boss numbers", or any request involving evaluating a single-family or small-multi residential deal for a wholesale assignment or fix-and-flip exit.
tier: gold
tags: [real-estate, wholesale, fix-and-flip, MAO, underwriting, deal-analysis, sauce-formula]
---

# 🤠 Linda Trigger — Pull the Trigger on the MAO

> When Bandit's done huntin', it's Trigger time. This is the Sauce Underwriter — Boss's locked formula for wholesale MAO + fix-and-flip walk-away. **Pull the trigger when the numbers say green.**

> Boss's locked formula for wholesale + fix-and-flip deals.
> Source: `Sauce Underwriter.xlsx` (Boss's personal calculator).
> Locked 2026-06-09 — anyone underwriting a deal in LindaAI runs THIS math.

---

## 🎯 WHEN TO USE

- User pastes a deal address + asking price
- User asks "what should I offer?" / "what's the MAO?"
- User wants to wholesale a house (find Max Allowable Offer)
- User wants to flip a house (find walk-away profit at sale price)
- User says "underwrite this" / "run the Sauce numbers" / "Sauce UW"

---

## 📥 INPUTS YOU NEED (ask the user)

**REQUIRED:**
1. **Subject SQFT** — heated living space of the subject property
2. **Subject Address** (for context + comp pull)
3. **Repair Level** — one of: Move-In Ready · Cosmetic Refresh · Regular Rehab · Full Rehab · Major Rehab · Custom

**ARV — can come 2 ways (ask which):**
   - **A) Pull comps:** ask user for 4 SOLD comps (Address, SQFT, Sold Price, Sold Date) → calculate ARV from average $/sqft × subject SQFT
   - **B) User provides ARV directly** — they already know

**OPTIONAL (defaults apply):**
- Wholesale Fee (default: $15,000)
- Investor Profit Override (skip unless user wants to manually set)
- Custom repair $/sqft (only if Repair Level = "Custom")

---

## 🧮 THE LOCKED FORMULA (Sauce Underwriter — DO NOT DEVIATE)

### Step 1 — Determine ARV
If pulling comps:
```
ARV = AVG(comp $/sqft) × Subject SQFT
where comp $/sqft = Sold Price ÷ SQFT  (per comp, averaged)
```
If user-provided: use their number.

### Step 2 — Repair Cost (from table by Repair Level)

| Repair Level | $/sqft | Typical Range |
|---|---|---|
| Move-In Ready | $8 | $4.5 - $7 |
| Cosmetic Refresh | $15 | $14 - $25 |
| Regular Rehab | $39 | $30 - $40 |
| Full Rehab | $65 | $41 - $57 |
| Major Rehab | $100 | $60 - $90 |
| Custom | user-entered | — |

```
Repair Cost = Subject SQFT × $/sqft (from table)
```

### Step 3 — Selling Costs
```
Selling Costs = ARV × 7%
```

### Step 4 — Investor Profit (auto-calculated, but user can override)
```
Investor Profit = MAX($20,000, 57% × Repair Cost, 10% × ARV)
```
The MAX of three floors — so investor ALWAYS clears at least $20K, or 57% of their rehab spend, or 10% of ARV (whichever is highest).

**If user provides override:** use override instead.

### Step 5 — Holding Costs (by Repair Level)

| Repair Level | Holding % of ARV |
|---|---|
| Move-In Ready | 3% |
| Cosmetic Refresh | 3% |
| Regular Rehab | 4% |
| Full Rehab | 5% |
| Major Rehab | 6% |
| Custom | 6% |

```
Holding Costs = ARV × (% from table)
```

### Step 6 — DISPO PRICE (price you sell to end-buyer)
```
DISPO PRICE = ARV - Selling Costs - Repair Cost - Investor Profit - Holding Costs
```

### Step 7 — Wholesale Fee
Default $15,000 unless user changes.
```
Wholesale Fee = $15,000  (or user-entered)
```

### Step 8 — MAO / BUY PRICE (Max you can offer the seller)
```
MAO = DISPO PRICE - Wholesale Fee
```

---

## 📊 OUTPUT FORMAT (always show this table)

```
🤠 Sauce Underwriter — [Property Address]

INPUTS
  Subject SQFT:        [SQFT]
  Repair Level:        [Level]  ($/sqft × $SQFT = $RepairCost)
  ARV:                 $[ARV]     (source: comp avg / user-provided)
  Wholesale Fee:       $[Fee]

CALCULATION
  ARV                                          $[ARV]
  - Selling Costs (7% of ARV)                 -$[SellingCosts]
  - Repair Cost ([level] @ $/sqft × SQFT)     -$[RepairCost]
  - Investor Profit (MAX of 20K/57%/10%)      -$[Profit]
  - Holding Costs ([%] of ARV)                -$[Holding]
  ─────────────────────────────────────────────
  = DISPO PRICE (sell to end buyer)           $[DispoPrice]   ([X]% of ARV)
  - Wholesale Fee                             -$[Fee]
  ─────────────────────────────────────────────
  🎯 MAO (Max Allowable Offer)                $[MAO]          ([X]% of ARV)

DEAL QUALITY (red/yellow/green light)
  🟢 GREEN — MAO < 70% of ARV (strong margin)
  🟡 YELLOW — MAO 70-80% of ARV (workable, slim)
  🔴 RED — MAO > 80% of ARV (won't close, walk away)
```

---

## 🔁 BONUS — FIX-AND-FLIP WALK-AWAY MODE

If the user wants to check the FLIP exit instead (they own/control the property and want to know what they walk with):

INPUTS:
- MLS sales price (what house lists/sells for)
- Total updates / rehab spent
- Holding costs spent

CALCULATION:
```
Net after Commissions = MLS Sales Price × (1 - 10%)   # 10% covers RE commissions + closing
Walk-Away Profit      = Net - Updates - Holding
```

Show:
```
🤠 Flip Walk-Away

  MLS Sales Price:        $[SalesPrice]
  - 10% (commissions + closing):  -$[10Pct]
  - Updates / Rehab:               -$[Updates]
  - Holding (taxes/insurance/HOA): -$[Holding]
  ─────────────────────────────
  💰 Walk-Away Profit:    $[WalkAway]
```

---

## 🎤 BRAND VOICE

Lead with: *"🤠 Bandit (Deal Hunter) running the Sauce numbers on [address]..."*

Close with: red/yellow/green verdict + ONE recommended next action:
- 🟢 → *"Hand to 💼 Closer to draft the LOI at $[MAO]"*
- 🟡 → *"Marginal — push the seller down OR re-pick repair level"*
- 🔴 → *"Walk. Find the next one. 🤠"*

---

## 🚨 DO NOT DEVIATE

- These are Boss's LOCKED formulas. Do NOT make up new ones.
- If user wants a different formula, run THIS first, then offer alternates.
- If user wants a DIFFERENT deal type (multifamily, MHP, RV park, land, commercial) → use the specialized skill (linda-dealpack, linda-bandit, etc.). This skill is for SINGLE-FAMILY + SMALL-MULTI residential wholesale/flip ONLY.

---

## 📋 INTERNAL — FORMULA CHEAT SHEET (for the model)

```python
def sauce_uw(sqft, arv, repair_level, wholesale_fee=15000, profit_override=None, custom_repair_per_sqft=None):
    REPAIR_TABLE = {
        "Move-In Ready": 8, "Cosmetic Refresh": 15, "Regular Rehab": 39,
        "Full Rehab": 65, "Major Rehab": 100,
    }
    HOLDING_PCT = {
        "Move-In Ready": 0.03, "Cosmetic Refresh": 0.03, "Regular Rehab": 0.04,
        "Full Rehab": 0.05, "Major Rehab": 0.06, "Custom": 0.06,
    }
    repair_psf = custom_repair_per_sqft if repair_level == "Custom" else REPAIR_TABLE[repair_level]
    repair_cost = sqft * repair_psf
    selling_costs = arv * 0.07
    investor_profit = profit_override if profit_override else max(20000, 0.57 * repair_cost, 0.10 * arv)
    holding_costs = arv * HOLDING_PCT[repair_level]
    dispo_price = arv - selling_costs - repair_cost - investor_profit - holding_costs
    mao = dispo_price - wholesale_fee
    return {
        "arv": arv, "repair_cost": repair_cost, "selling_costs": selling_costs,
        "investor_profit": investor_profit, "holding_costs": holding_costs,
        "dispo_price": dispo_price, "wholesale_fee": wholesale_fee, "mao": mao,
        "mao_pct_arv": mao / arv if arv else 0,
        "verdict": "GREEN" if mao < arv * 0.70 else ("YELLOW" if mao < arv * 0.80 else "RED"),
    }
```

---

— LOCKED 2026-06-09 by 🤠 Bandit + 🔥 Forge. Source: Boss's Sauce Underwriter.xlsx.
— © 2022-2026 Daniel Wise · LindaAI · Built by Daniel Wise
