# Sauce Hub Site

Static site: homepage, 6 ebook pages with segmented waitlist forms, blog, coaching page.
No build step — plain HTML/CSS, deploys anywhere (GitHub Pages ready).

## Deploy options
1. **Own repo (recommended):** copy `sauce-site/` contents into a new repo
   (e.g. `sauce-hub`), enable GitHub Pages → live at `<user>.github.io/sauce-hub`
   or a custom domain via CNAME.
2. **Subpath of this repo's Pages site** — works, but mixes brands with LindaAI.

## Wiring the waitlists (required before launch)
Forms currently point at `action="#"` (placeholders — they do NOT store emails yet).
1. Create a free MailerLite account (1,000 subs free).
2. Create one **group per segment**: health, husband, football, injury,
   realestate, kids, coaching.
3. For each page, replace the placeholder form with the MailerLite embedded
   form for that group (search the HTML for `TODO`). The hidden `segment`
   field documents which group each page maps to — this is what guarantees
   nobody gets emails about the wrong book.

## Checkout (when health book is ready)
Gumroad product link replaces the waitlist CTA on `books/health.html`;
coaching page gets Gumroad/Stripe checkout links for the $149 playbook and
$99/mo coaching.
