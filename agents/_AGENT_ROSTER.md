# LindaAI Agent Roster

The LindaAI Platinum tier ships with 18 specialized agents. Each agent has a country-coded LindaAI name, a primary role, and an `avatar:` field in its frontmatter so you can drop a PNG into `agents/avatars/<name>.png` later and have it wire up automatically.

| Call Name | Role | Trigger Keywords |
|---|---|---|
| Bandit | Deal Hunter (real estate) | "find deals", "hunt properties", "scout markets" |
| Inkslinger | Content Machine | "write content", "batch posts", "content factory" |
| Sheriff | Inbox Sentinel | "watch inbox", "triage mail", "guard my time" |
| Doc | Customer Support | "customer support", "help ticket", "support reply" |
| Drawl | Copywriter | "copywriting", "write ad copy", "sales page" |
| Wrangler | Business Development | "partnerships", "biz dev", "new opportunities" |
| Tally | Data Analyst | "analyze data", "run numbers", "report metrics" |
| Mercantile | Ecommerce | "ecommerce", "product listings", "online store" |
| Closer | Sales Manager | "close deals", "sales coaching", "pipeline push" |
| Grit | Personal Development | "personal growth", "mindset", "coaching" |
| Scout | Recruiter | "hire someone", "recruiting", "find talent" |
| Compass | SEO Specialist | "SEO", "search optimization", "keyword research" |
| Holler | Social Media | "social media", "posting", "engagement" |
| Ranger | Virtual Assistant | "assistant tasks", "schedule", "organize" |
| Pony | Email Marketer | "email campaign", "drip sequence", "newsletter" |
| Mender | Credit Repair | "credit repair", "dispute letters", "credit score" |
| Ledger | Tax Filing | "tax filing", "tax prep", "deductions" |
| Bullhorn | Ad Manager | "run ads", "ad campaigns", "paid traffic" |

## How to invoke
In any LindaAI chat, call an agent by name or role. Examples:
- "Bandit, find me 5 MHP deals in Texas under $2M"
- "Inkslinger, batch 10 LinkedIn posts about mobile home park investing"
- "Ledger, what deductions can I take for my real estate business?"

## Adding avatars (future)
Drop a 512x512 PNG in `agents/avatars/` matching the agent filename:
- `agents/avatars/bandit.png`
- `agents/avatars/inkslinger.png`
- ...etc

The `avatar:` field in each agent file already points to the correct path.

---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
