---
name: linda-kajabi
description: This skill should be used when the user asks to "scrape kajabi", "kajabi audit", "crawl kajabi", "kajabi scraper", "audit this kajabi site", "extract kajabi content", "kajabi site audit", "pull content from kajabi", "reverse engineer this kajabi site", "what's on this kajabi site", "scrape this course site", "audit this online course site", "extract funnel from kajabi", "kajabi competitor research", "what courses does this kajabi site sell", "break down this kajabi page", "kajabi teardown", or any request involving crawling, scraping, auditing, or extracting content and structure from a Kajabi-powered website.
version: 1.0.0
---

# Kajabi Site Scraper & Auditor

## Overview

Crawls an entire Kajabi-powered website and produces a comprehensive audit report. Given a URL, LindaAI systematically visits every publicly accessible page on the site — homepage, sales pages, landing pages, course listings, about pages, checkout pages, blog posts — and extracts everything: page structure, copy, pricing, course/product offerings, CTAs, opt-in forms, funnel architecture, navigation, meta tags, media assets, testimonials, and social proof. The output is a structured markdown report saved to `brain/research/` that gives you a complete picture of how the site is built, what it sells, and how it sells it. Think of it as a competitive intelligence teardown for any Kajabi site — LindaAI does the legwork so you don't have to.

## When This Skill Applies

- User provides a Kajabi site URL and wants it audited
- User wants to reverse-engineer a competitor's Kajabi site
- User asks "what courses/products does this site sell?"
- User wants to understand a Kajabi site's funnel structure
- User asks to extract pricing, offers, or content structure from a Kajabi site
- User wants a teardown of an online course site
- User says "scrape this site" and the site is on Kajabi
- User wants to audit their own Kajabi site for gaps or improvements

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

### Step 0: Get the Target URL

The user provides a Kajabi site URL. If they just say "scrape this Kajabi site" with no URL, ask:

> "Drop the URL for the Kajabi site you want me to round up. I'll ride through every public page and pull out the full picture — pages, courses, pricing, funnels, copy, CTAs, the whole spread."

Validate the URL is accessible. Kajabi sites typically live on custom domains or `*.mykajabi.com` subdomains.

### Step 1: Homepage & Navigation Crawl

> 🤠 "Hold tight — heading over yonder to gather up the details."

Start at the homepage. Use WebFetch to pull the page content.

**Extract from the homepage:**
- Site name / brand name
- Headline and subheadline copy
- Hero section CTA (what does the main button say and where does it go?)
- Navigation menu items and their URLs — this is your crawl map
- Footer links (often contain pages not in the main nav)
- Social media links
- Any pop-ups, banners, or announcement bars mentioned in the content

**Build the crawl queue** from navigation links + footer links. Only follow links on the same domain — ignore external links. Deduplicate URLs.

### Step 2: Systematic Page Crawl

Visit every page in the crawl queue using WebFetch. For each page, extract:

| Data Point | What to Look For |
|-----------|-----------------|
| Page URL | Full URL |
| Page Title | `<title>` tag content |
| Meta Description | Meta description tag |
| H1 Headline | Primary headline on the page |
| Page Type | Sales page, landing page, about, blog, course listing, checkout, opt-in, contact, legal, etc. |
| Key Copy | First 2-3 paragraphs or the main value proposition |
| CTAs | Button text + destination URL for every call-to-action |
| Forms | Opt-in forms — what fields they collect (name, email, phone, etc.) |
| Pricing | Any pricing displayed — amounts, tiers, payment plans, trial offers |
| Testimonials | Names, titles, and a brief note of what the testimonial says |
| Social Proof | Student counts, revenue claims, media logos, badges |
| Images/Video | Key media assets referenced (hero images, video embeds) |
| Lead Magnets | Free offers, downloads, webinar registrations |

**While crawling, discover additional pages:**
- Links within page content that weren't in the nav
- Course/product detail pages linked from listing pages
- Blog post pages
- Thank-you or confirmation pages (if publicly accessible)

Add discovered pages to the crawl queue and continue until all pages are visited.

**Rate limiting:** Wait 2-3 seconds between page fetches to be respectful. Don't hammer the server.

### Step 3: Course & Product Extraction

From the crawl data, compile all courses and products:

| Field | Details |
|-------|---------|
| Product Name | Course or product title |
| Type | Online course, membership, community, coaching, digital product, bundle |
| Description | What the product promises / who it's for |
| Price | One-time, subscription, payment plan options |
| Modules/Sections | If visible — list out the curriculum structure |
| Bonuses | Any bonus items included |
| Guarantee | Money-back guarantee details if stated |
| Sales Page URL | Link to the sales page |
| Checkout URL | Link to checkout if visible |

### Step 4: Funnel Architecture Mapping

Analyze the crawl data to map the site's funnel structure:

**Traffic Entry Points:**
- What pages are designed to attract cold traffic? (blog, SEO pages, free resources)
- What lead magnets or opt-ins capture email addresses?

**Nurture Layer:**
- Is there a blog? How many posts? What topics?
- Are there free resources, webinars, or challenges?
- What email capture points exist?

**Conversion Layer:**
- What are the primary sales pages?
- What CTAs drive to checkout?
- Are there upsells, downsells, or order bumps visible?
- What pricing strategies are used? (anchoring, urgency, scarcity)

**Map the funnel flow:**
```
[Entry Point] → [Lead Capture] → [Nurture Content] → [Sales Page] → [Checkout]
```

Document each funnel path you can identify.

### Step 5: Competitive Intelligence Flags

Analyze the data and flag interesting patterns:

- **Pricing Strategy**: How are products priced? Payment plans? Anchoring? Free trials?
- **Content Volume**: How much free vs. paid content? Blog frequency?
- **Social Proof Density**: How heavily do they use testimonials? Where are they placed?
- **Funnel Complexity**: Simple (one product, one page) vs. complex (multiple funnels, tripwires, upsells)?
- **Gaps/Opportunities**: Missing pages? No blog? No lead magnet? Weak CTAs? No testimonials on key pages?
- **Tech Stack Clues**: Any third-party integrations visible? (chat widgets, analytics, payment processors)
- **Brand Positioning**: Who is this for? What transformation do they promise? How do they differentiate?

### Step 6: Generate the Audit Report

Compile everything into a structured markdown report:

```markdown
# Kajabi Site Audit: [Site Name]
**URL:** [site URL]
**Audit Date:** [today's date]
**Total Pages Crawled:** [count]

---

## Executive Summary
[2-3 paragraph overview: what the site sells, who it targets, how it's structured, and key observations]

## Site Architecture
### Navigation Structure
[Nav items with URLs]

### All Pages Discovered
[Table: URL | Page Title | Page Type]

## Products & Courses
[For each product: name, type, price, description, curriculum if visible, sales page URL]

## Funnel Architecture
[Flow diagrams and descriptions of each funnel path identified]

## Pricing Strategy
[How products are priced, payment options, anchoring, bundling]

## Content & Lead Magnets
[Blog overview, free resources, opt-in offers]

## Social Proof & Testimonials
[Summary of testimonials, social proof elements, and where they appear]

## CTAs & Conversion Points
[All CTAs found, what they say, where they link]

## Meta & SEO Data
[Table: Page | Title Tag | Meta Description]

## Competitive Intelligence Flags
[Patterns, strengths, weaknesses, gaps, opportunities]

## Raw Data Appendix
[Full crawl data for reference]
```

### Step 7: Save the Report

Save the report to `brain/research/kajabi-audit-[site-name]-[date].md`.

Tell the user: "Your Kajabi audit is saddled up and saved to brain/research/. Here's the executive summary and key findings — the full report has every page, product, funnel path, and data point LindaAI rounded up for you."

Present the Executive Summary and Competitive Intelligence Flags sections in the chat, with a note that the full report is in the file.

🤠 *Generated by LindaAI* 🏇


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com
