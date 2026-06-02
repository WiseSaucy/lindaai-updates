# LindaAI Agent Roster

The LindaAI Platinum tier ships with **18 specialized agents**. Rooster crows first — he's your daily motivator and opens every morning. After him, the team handles the work.

Each agent has a country-coded LindaAI name, a primary role, and an `avatar:` field in its frontmatter so you can drop a PNG into `agents/avatars/<name>.png` later and have it wire up automatically.

| # | Call Name | Role | Trigger Keywords |
|---|---|---|---|
| 1 | **Rooster** | Daily Motivator | "morning holler", "pep talk", "motivate me" |
| 2 | Bandit | Deal Hunter (real estate) | "find deals", "hunt properties", "scout markets" |
| 3 | Inkslinger | Content Machine | "write content", "batch posts", "content factory" |
| 4 | Sheriff | Inbox Sentinel | "watch inbox", "triage mail", "guard my time" |
| 5 | Doc | Customer Support | "customer support", "help ticket", "support reply" |
| 6 | Drawl | Copywriter | "copywriting", "write ad copy", "sales page" |
| 7 | Wrangler | Business Development | "partnerships", "biz dev", "new opportunities" |
| 8 | Tally | Data Analyst | "analyze data", "run numbers", "report metrics" |
| 9 | Mercantile | Ecommerce | "ecommerce", "product listings", "online store" |
| 10 | Closer | Sales Manager | "close deals", "sales coaching", "pipeline push" |
| 11 | Grit | Personal Development | "personal growth", "mindset", "coaching" |
| 12 | Scout | Recruiter | "hire someone", "recruiting", "find talent" |
| 13 | Compass | SEO Specialist | "SEO", "search optimization", "keyword research" |
| 14 | Holler | Social Media | "social media", "posting", "engagement" |
| 15 | Ranger | Virtual Assistant | "assistant tasks", "schedule", "organize" |
| 16 | Pony | Email Marketer | "email campaign", "drip sequence", "newsletter" |
| 17 | Bullhorn | Ad Manager | "run ads", "ad campaigns", "paid traffic" |
| 18 | Forge | Engineer / Automation | "automate this", "build me a tool", "fix the code", "connect my apps" |

## How to invoke
In any LindaAI chat, call an agent by name or role. Examples:
- "Bandit, find me 5 MHP deals in Texas under $2M"
- "Inkslinger, batch 10 LinkedIn posts about mobile home park investing"
- "Tally, pull the KPIs for last month"

## Adding avatars (future)
Drop a 512x512 PNG in `agents/avatars/` matching the agent filename:
- `agents/avatars/bandit.png`
- `agents/avatars/inkslinger.png`
- ...etc

The `avatar:` field in each agent file already points to the correct path.

---

© 2022-2026 Daniel Wise · LindaAI
All rights reserved · support@send.lindaai-brain.com · lindaai-brain.com
