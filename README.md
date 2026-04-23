# LindaAI Updates Server

Static host for `/lindaai-update`. Customers' LindaAI installs pull from here.

## URLs customers will hit
- `GET https://updates.lindaai.com/manifest.json` — the version ledger
- `GET https://updates.lindaai.com/skills/<name>.md` — raw skill file
- `GET https://updates.lindaai.com/agents/<name>.md` — raw agent file

## How to publish this to GitHub Pages (free hosting)

```bash
# One-time setup
cd /Users/jowise/Desktop/LindaAI-OG/LindaAI-Updates-Server
git init
git add .
git commit -m "Initial LindaAI updates server"

# Create repo on GitHub (replace USERNAME with your GitHub handle)
gh repo create lindaai-updates --public --source=. --remote=origin --push

# Enable Pages: Settings -> Pages -> Deploy from branch: main / root
# Your updates URL becomes: https://USERNAME.github.io/lindaai-updates/
```

## Custom domain (`updates.lindaai.com`)

1. Buy `lindaai.com` if you don't have it yet
2. In your DNS: `CNAME updates -> USERNAME.github.io`
3. On GitHub repo: Settings -> Pages -> Custom domain -> `updates.lindaai.com`

## Shipping an update

1. Edit skill in `LindaAI-Master/skills/<name>/SKILL.md`
2. Bump version in `LindaAI-Master/updates/manifest.json`
3. Re-sync this folder:
   ```bash
   cp LindaAI-Master/updates/manifest.json LindaAI-Updates-Server/manifest.json
   cp LindaAI-Master/skills/<name>/SKILL.md LindaAI-Updates-Server/skills/<name>.md
   ```
4. `git add -A && git commit -m "skill: <name> v1.1.0" && git push`
5. Customers pull it on next `/lindaai-update`

---

© 2026 LindaAI — Built by Daniel Wise
