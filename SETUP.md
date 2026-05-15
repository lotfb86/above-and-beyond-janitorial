# Above & Beyond Janitorial — site setup notes

Everything required to take this site from current state to launch. The build itself is in good shape; what's below is the manual steps that need accounts, credentials, content, or external action.

## Repo layout

The repo root IS the deploy root. Vercel `outputDirectory` is `.`, so every public file sits at the top level.

- `index.html` — home
- `services/` — 1 overview + 5 detail pages (medical-dental was folded into commercial-janitorial; 301 redirect lives in `vercel.json`)
- `service-area/` — 1 overview + 7 city pages
- `about.html`, `contact.html`, `faq.html`, `privacy.html`, `404.html`
- `sitemap.xml`, `robots.txt`
- `assets/css/styles.css`, `assets/js/app.js` — shared
- `assets/logo.png`, favicons, `og-image.png`
- `assets/photos/` — real photos (window-cleaning, hard-floor-care, van, government-municipal); rest are Unsplash backgrounds set inline
- `vercel.json` — security headers, cache rules, 301 redirects

The `_build/` directory holds Python scripts (`build.py`, `sitemap.py`) that originally generated the inner pages. Inner pages have since been hand-edited; rerunning the build would clobber any drift. Treat `_build/` as historical until/unless someone reconciles it with the live HTML.

## Deploy

GitHub repo: [lotfb86/above-and-beyond-janitorial](https://github.com/lotfb86/above-and-beyond-janitorial), branch `main`.

**The GitHub → Vercel webhook is not connected.** Pushes to `main` do NOT auto-deploy. Until someone reconnects the integration via the Vercel dashboard (Settings → Git), deploys must run via CLI:

```bash
vercel --prod --yes
```

Vercel project: `above-and-beyond-janitorial` under scope `jesse-anglens-projects-45c738e2`. Domain `aboveandbeyondjanitorialservice.com` is aliased to it.

To reconnect Git integration: open the Vercel dashboard → above-and-beyond-janitorial project → Settings → Git → connect to the GitHub repo. After that, pushes to `main` will deploy automatically.

## What still needs a human

### 1. Wire the quote form to Formspree (required before launch)

The form posts to a Formspree endpoint but the ID is a placeholder. Submissions currently fail silently in production (the JS catches the error and shows an alert with Todd's phone).

1. Sign up at [formspree.io](https://formspree.io) with `abovejanitorial@hotmail.com` as the destination email.
2. Create a new form. Copy the form ID (looks like `xqalbpoz`).
3. In `assets/js/app.js`, replace:
   ```js
   const FORMSPREE_ID = 'REPLACE_WITH_FORMSPREE_ID';
   ```
   with the real ID, commit, redeploy.
4. Click the verification link Formspree sends to `abovejanitorial@hotmail.com`.
5. (Optional) In Formspree settings, set email subject to `[Quote] {{facility}} — {{name}}` (already in the JSON payload).
6. (Optional) Enable Formspree's reCAPTCHA. The honeypot field (`_gotcha`) is already in place.
7. (Optional) Set an auto-reply: *"Thanks — Todd will be in touch within one business day from (208) 818-3175."*

### 2. Things to confirm with Todd

- **Founding year 1997** — research (Post Falls Chamber) confirms; verbal verify with Todd.
- **Idaho contractor / business license number** — for the footer fine-print.
- **Insurance carrier name + COI document** — backs the "COI on request" promise on the trust bar.
- **Real photos still needed** for: commercial janitorial card, carpet extraction card (currently a flagged compromise — floor scrubber on tile, not actual carpet equipment), restroom sanitation card, Todd's headshot in About. Real van + window-cleaning + floor-care + Idaho-Capitol-van photos are already in place under `assets/photos/`.
- **Verified Google reviews** — the testimonials section has been removed entirely (HTML comment placeholder marks the spot in `index.html`). Re-add once 5+ real reviews exist.
- **Branded email** — currently using `abovejanitorial@hotmail.com`. If Todd wants `todd@aboveandbeyondjanitorialservice.com`, set up Cloudflare Email Routing (free, forwards to hotmail) or Google Workspace ($6/mo).

### 3. Local SEO — start the GBP clock now

Google Business Profile postcard verification takes 1–2 weeks. Start before launch:

1. Claim/create the listing at [business.google.com](https://business.google.com).
2. Primary category: **Janitorial service**. Secondary: **Commercial cleaning service**.
3. Set as a **service-area business** (no public storefront). Add all 7 Idaho cities + Spokane / Spokane Valley / Liberty Lake (Eastern WA coverage).
4. Set the website URL to `https://aboveandbeyondjanitorialservice.com/`.
5. Upload 10+ real photos.
6. Seed 5–10 Q&A items.
7. Generate the Google reviews link, share with Todd's existing happy clients. Target 10+ within 30 days of launch.

### 4. Citations — same NAP everywhere

Use this exact format on every directory listing:

- Name: `Above & Beyond Janitorial, Inc.`
- Phone: `(208) 818-3175`
- Address city/state: `Hayden, Idaho`
- Email: `abovejanitorial@hotmail.com`
- Website: `https://aboveandbeyondjanitorialservice.com/`

Required listings: Bing Places, Apple Business Connect, Yelp, BBB, Manta (claim the existing listing). Optional: chamber listings (Coeur d'Alene, Post Falls, Hayden — strong local backlinks).

### 5. Search Console + Bing Webmaster + GA4

After deploy:

1. Verify domain in [Search Console](https://search.google.com/search-console) (DNS TXT record is cleanest).
2. Submit `https://aboveandbeyondjanitorialservice.com/sitemap.xml`.
3. In [Bing Webmaster Tools](https://www.bing.com/webmasters), import from Search Console (one click). Submit the same sitemap.
4. Create a GA4 property at [analytics.google.com](https://analytics.google.com). Install the global tag in every page's `<head>`. Mark `generate_lead`, `phone_call_click`, `email_click` as Key Events.

### 6. Things deliberately deferred

- **Self-hosted fonts** — currently loading Geist from Google Fonts CDN with `display=swap` + preload. Self-hosting would shave 100–300ms TTFB.
- **WebP image conversion** — real photos under `assets/photos/` are JPEG. Add `<picture>` sources with WebP + JPEG fallback.
- **Privacy policy content** — `privacy.html` has a placeholder. Replace with a generated policy from [termly.io](https://www.termly.io) before launch.
- **Cookie banner** — not needed unless EU traffic is expected.
- **CSP header** — not in `vercel.json` yet because it can break the Maps embed if mis-set. Add after testing in staging.

## Acceptance check before flipping the DNS

- [ ] Formspree ID set in `assets/js/app.js`, test submission delivered to Todd's inbox within 60 seconds
- [ ] GitHub → Vercel auto-deploy webhook reconnected (so pushes to main deploy automatically)
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

Currently using non-www: `aboveandbeyondjanitorialservice.com`. All canonical tags and schema URLs use this. If switching to www, update sitewide.
