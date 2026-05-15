# Above & Beyond Janitorial — site setup notes

Everything required to take this site from the current state to live on production. The build itself is complete; what's below is the manual steps that require accounts, credentials, or content from Todd.

## What ships on push

The `site/` directory is the deployable build. Vercel watches the GitHub repo and pushes deploy automatically.

- `site/index.html` — home
- `site/services/` — 1 overview + 6 detail pages
- `site/service-area/` — 1 overview + 7 city pages
- `site/about.html`, `/contact.html`, `/faq.html`, `/privacy.html`, `/404.html`
- `site/sitemap.xml`, `/robots.txt`
- `site/assets/css/styles.css`, `/assets/js/app.js` — shared chrome
- `site/assets/logo.png`, favicons, `og-image.png`
- `site/vercel.json` — security headers + cache rules

## What still needs a human

### 1. Wire the quote form to Formspree (required before launch)

The form currently logs the payload to the console with a placeholder Formspree ID. To make it actually email Todd:

1. Sign up at [formspree.io](https://formspree.io) with `todd@aboveandbeyondjanitorialservice.com` as the destination email.
2. Create a new form. Copy the form ID (looks like `xqalbpoz`).
3. In `site/assets/js/app.js`, find this line near the top:
   ```js
   const FORMSPREE_ID = 'REPLACE_WITH_FORMSPREE_ID';
   ```
   Replace with the real ID, commit, push.
4. Verify the destination email when Formspree sends the confirmation.
5. In Formspree settings, set the email subject to `[Quote] {{facility}} — {{name}}` (already built into the payload).
6. (Optional) Enable Formspree's reCAPTCHA. The honeypot field (`_gotcha`) is already in place.
7. (Optional) Set an auto-reply for the lead: *"Thanks — Todd will be in touch within one business day from (208) 818-3175."*

### 2. Things to confirm with Todd before going live

Already flagged in the design chat — these are still open:

- **Founding year 1997** — research (Post Falls Chamber) confirms this; verbal verify with Todd.
- **Idaho contractor / business license number** — add to footer fine-print once provided.
- **Insurance carrier name + COI document** — backs the "COI on request" promise on the trust bar.
- **2–3 sentences per city** about what's distinctive about Todd's experience there. The current city-page copy is good defaults; Todd's first-person details make it stronger.
- **10+ real photos** — Todd, crew, vans, equipment, before/after. Currently the only photos rendered come from Unsplash via CSS background-image. Replace those URLs in `site/assets/css/styles.css` (or in the inline industry-card markup in `site/index.html`) and the about photo on `/about.html`.
- **Verified Google reviews** — the home testimonials block has a "// Placeholder" comment under it. Replace those three reviews with real ones once they exist.

### 3. Local SEO — start the GBP clock now

Google Business Profile postcard verification takes 1–2 weeks. Start before launch:

1. Claim/create the listing at [business.google.com](https://business.google.com) under Todd's preferred Google account.
2. Primary category: **Janitorial service**. Secondary: **Commercial cleaning service**.
3. Set it as a **service-area business** (no public storefront). Add all 7 cities: Hayden, Coeur d'Alene, Post Falls, Rathdrum, Sandpoint, Spirit Lake, Athol.
4. Set the website URL to `https://aboveandbeyondjanitorialservice.com/`.
5. Upload 10+ real photos (logo + crew + vans + before/after).
6. Seed 5–10 Q&A items.
7. Generate the Google reviews link in GBP, share with Todd's existing happy clients. Target 10+ reviews within 30 days of launch.

### 4. Citations — same NAP everywhere

Use this exact format on every directory listing:

- Name: `Above & Beyond Janitorial, Inc.`
- Phone: `(208) 818-3175`
- Address city/state: `Hayden, Idaho`
- Email: `todd@aboveandbeyondjanitorialservice.com`
- Website: `https://aboveandbeyondjanitorialservice.com/`

Required listings: Bing Places, Apple Business Connect, Yelp, BBB, Manta (claim the existing listing). Optional: local chamber listings (Coeur d'Alene, Post Falls, Hayden chambers — strong local backlinks).

### 5. Search Console + Bing Webmaster (skip GA4 per Jesse — handle post-launch)

After deploy:

1. Verify domain in [Search Console](https://search.google.com/search-console) (DNS TXT record is cleanest).
2. Submit `https://aboveandbeyondjanitorialservice.com/sitemap.xml`.
3. In [Bing Webmaster Tools](https://www.bing.com/webmasters), import from Search Console (one click). Submit the same sitemap.

### 6. Things deliberately deferred

These were skipped per Jesse's direction or scoped out:

- **Analytics (GA4, Search Console, Bing)** — Jesse said skip for now. Add later.
- **Self-hosting fonts** — currently loading Geist from Google Fonts CDN with `display=swap` + preload. Self-hosting would shave 100–300ms TTFB; do as a perf optimization round once live.
- **WebP image conversion** — most current images are Unsplash CDN backgrounds. When real photos come in, optimize them with [Squoosh](https://squoosh.app) and add `<picture>` sources with WebP + JPEG fallback.
- **Privacy policy generation** — `site/privacy.html` has a placeholder. Replace with a generated policy from [termly.io](https://www.termly.io) before launch.
- **Cookie banner** — not needed unless EU traffic is expected.
- **CSP header** — not in `vercel.json` yet because it can break the Maps embed if mis-set. Add after testing in staging.

## Regenerating inner pages

Inner pages (services, service-area, about, contact, FAQ, 404, privacy) are templated. The home `site/index.html` is hand-maintained.

```bash
python3 _build/build.py     # regenerates inner pages
python3 _build/sitemap.py   # regenerates sitemap.xml
```

Edit page content in `_build/build.py` (the `SERVICES`, `CITIES`, and individual page functions). Rerun the build.

## Acceptance check before flipping the DNS

- [ ] Formspree ID set in `assets/js/app.js`, test submission delivered to Todd's inbox within 60 seconds
- [ ] All `tel:` and `mailto:` links work on real iPhone + Android
- [ ] Lighthouse mobile Performance ≥ 90, A11y ≥ 95, SEO 100, Best Practices ≥ 95
- [ ] [Schema.org validator](https://validator.schema.org) green on home, one service, one city, FAQ
- [ ] [Rich Results Test](https://search.google.com/test/rich-results) shows LocalBusiness + FAQPage + BreadcrumbList eligible
- [ ] [Mobile-Friendly test](https://search.google.com/test/mobile-friendly) passes on home + one inner page
- [ ] [securityheaders.com](https://securityheaders.com) grade A on the deployed domain
- [ ] HTTPS forced, www and non-www both 301 to canonical
- [ ] GBP verified and populated
- [ ] First 10 Google reviews collected (target within 30 days)

## Domain canonical

Confirm with Jesse whether canonical is `www.aboveandbeyondjanitorialservice.com` or `aboveandbeyondjanitorialservice.com`. Update the `<link rel="canonical">` and schema URLs in `_build/build.py` (`DOMAIN` constant) if it should be www-prefixed, then regenerate.

Right now everything uses the non-www form.
