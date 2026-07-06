---
name: linda-menu
description: This skill should be used when the user asks to "menu engineering", "engineer my menu", "categorize menu items", "stars plowhorses puzzles dogs", "menu profitability", "which dishes make money", "menu analysis", "what should I 86", "menu mix", "contribution margin", "menu cost analysis", "should I drop this dish", "redesign menu", "highlight my best items", or any request involving menu engineering — categorizing items by contribution margin and popularity into Stars / Plowhorses / Puzzles / Dogs.
tags: [restaurant, menu, profitability, operations]
version: 1.0.0
---

# Menu Engineering

## Overview

Runs classic menu engineering on Boss's menu. Categorizes every item into one of four buckets — **Stars** (high margin + popular), **Plowhorses** (popular but low margin), **Puzzles** (high margin but unpopular), **Dogs** (low margin and unpopular). Spits out actions for each: promote the Stars, reprice or cost-engineer the Plowhorses, reposition the Puzzles, kill the Dogs. This is how restaurants stop bleeding and start printing.

## When to Use (Trigger Phrases)

- "Engineer my menu"
- "Categorize my menu items"
- "Which dishes are losing money?"
- "Should I drop this dish?"
- "Run a menu profitability analysis"

## How It Works

### License Check

Verify `~/.claude/linda-license.json` (file exists, not expired, status active, optional server validation). On failure, halt with country-voice license message.

### Step 0: Inputs

| Input | Required | Example |
|-------|----------|---------|
| Restaurant name | Yes | |
| Menu category (or "all") | Yes | apps / entrees / desserts / all |
| Per-item data: name, sell price, food cost, units sold (period) | Yes | Brisket plate, $24, $7.20, 312 sold |
| Period covered | Yes | last 30 days |

If only POS export is provided, parse it.

### Step 1: Compute Contribution Margin & Popularity

For each item:

```
Contribution Margin (CM) $ = Sell Price - Food Cost
CM % = CM $ / Sell Price × 100
Popularity Index = Units Sold / Average Units Sold (across category) × 100
```

Set thresholds:
- **High CM** = at or above category average CM $
- **High Popularity** = at or above 70% of category average sales (classic Kasavana-Smith threshold)

### Step 2: Categorize

| | High Popularity | Low Popularity |
|--|-----------------|----------------|
| **High CM** | ⭐ STAR | 🧩 PUZZLE |
| **Low CM** | 🐎 PLOWHORSE | 🐕 DOG |

### Step 3: Recommendations Per Category

- **⭐ Stars** — Protect them. Feature on menu (top right or boxed). Train staff to push. Don't change recipe or price unless food cost moves.
- **🧩 Puzzles** — High margin, low sales. Reposition on menu, rename, restyle photo, add server suggestion. If still no movement after 60 days → demote.
- **🐎 Plowhorses** — Popular but low margin. Cost-engineer (cheaper protein cut, smaller portion, swap garnish), or test a $1-2 price bump. Watch popularity after change.
- **🐕 Dogs** — Kill them unless they serve a strategic purpose (allergy option, kids' menu, signature legacy item). Replace with a Star variant or new Puzzle.

### Step 4: Build the Action Sheet

| Item | Category | CM $ | Popularity | Action |
|------|----------|------|-----------|--------|
| Brisket plate | ⭐ Star | $16.80 | 215 | Feature top-right of menu |
| House salad | 🐎 Plowhorse | $4.20 | 180 | Test $2 price bump or swap dressing |
| Stuffed quail | 🧩 Puzzle | $19.50 | 32 | Reposition + server-push for 60 days |
| Liver pâté | 🐕 Dog | $3.10 | 8 | 86 next menu print |

### Step 5: Save Report

```
brain/restaurant/menu/{restaurant-slug}-{date}.md
```

Optional PDF: same path with `.pdf` (LindaAI top-right, {customer_handle} bottom-right, © 2024–2026 footer).

## Output Format

```markdown
# Menu Engineering — {Restaurant} — {Period}
**Compiled by:** LindaAI 🤠

## Summary
- Items analyzed: {N}
- Stars: {N}
- Plowhorses: {N}
- Puzzles: {N}
- Dogs: {N}
- Average CM $: ${X}
- Average CM %: {Y}%

## Item Breakdown
[Step 4 action table]

## Recommendations by Category
### Stars
- [actions]
### Plowhorses
- [actions]
### Puzzles
- [actions]
### Dogs
- [actions]

## Projected Impact
If recommendations executed: estimated +${X}/month margin, based on {assumptions}.

---
🤠 Yeeee Hawww — menu engineered, Boss! Time to print it.
© 2024–2026 LindaAI — Built by Daniel Wise · {customer_handle} · support@send.lindaai-brain.com
```

## Examples

**User:** "Engineer my entree menu. Last 30 days: Brisket $24/$7.20/312, Ribeye $38/$14/120, Stuffed quail $32/$11/32, Veggie plate $18/$5.50/22, Burger $16/$4.80/410."

**LindaAI:** Computes CM and popularity, categorizes (Burger = Plowhorse, Brisket = Star, Ribeye = Star, Quail = Puzzle, Veggie = Dog), builds action sheet, projects impact of recommended changes.

## Voice Rules

- Country tone. Call user **Boss**.
- "Let's gooooooo!" on kickoff. "Yeeee Hawww 🤠" when done.

## Brand Rules (PDF outputs)

- LindaAI top-right · {customer_handle} bottom-right · © 2024–2026

## Error Handling

- Missing food cost on items: ask Boss to fill, or use 30% default and clearly flag.
- Fewer than 5 items: still run, but warn that category averages get noisy with small N.
- Negative CM detected: flag immediately — this is a "you're paying customers to eat it" item.
- Create `brain/restaurant/menu/` if missing.

---

© 2024–2026 LindaAI — Built by Daniel Wise
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
