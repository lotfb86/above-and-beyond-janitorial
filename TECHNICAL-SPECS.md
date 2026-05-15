# TECHNICAL SPECIFICATIONS - Lighthouse 100/100
## Astro 5 + Tailwind CSS 4 + Vercel Static

---

## astro.config.mjs (Complete)

```js
import { defineConfig, fontProviders } from 'astro/config';
import vercelStatic from '@astrojs/vercel/static';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://aboveandbeyondjanitorial.com',
  output: 'static',
  adapter: vercelStatic({
    webAnalytics: { enabled: true },
    imageService: true,
  }),
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
  prefetch: {
    prefetchAll: false,
    defaultStrategy: 'hover',
  },
  image: {
    domains: [],
    remotePatterns: [{ protocol: 'https' }],
  },
  fonts: [
    {
      provider: fontProviders.local(),
      name: 'Inter',
      cssVariable: '--font-inter',
      options: {
        variants: [{
          weight: '100 900',
          style: 'normal',
          src: ['./src/assets/fonts/InterVariable.woff2'],
        }],
      },
    },
  ],
});
```

---

## vercel.json (Complete)

```json
{
  "headers": [
    {
      "source": "/_astro/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    },
    {
      "source": "/fonts/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    },
    {
      "source": "/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=0, must-revalidate" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-XSS-Protection", "value": "1; mode=block" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()" },
        { "key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload" }
      ]
    }
  ]
}
```

---

## Project Structure

```
project-root/
  astro.config.mjs
  vercel.json
  package.json
  public/
    robots.txt
    favicon.svg
    favicon.ico
    apple-touch-icon.png
    og-default.jpg              (1200x630)
  src/
    assets/
      fonts/
        InterVariable.woff2
      images/
        hero/
        services/
        gallery/
        team/
        logos/
    components/
      global/
        Header.astro
        Footer.astro
        SkipLink.astro
        EmergencyBanner.astro
        MobileBottomBar.astro
        Breadcrumbs.astro
      seo/
        SEOHead.astro
        StructuredData.astro
        SchemaLocalBusiness.astro
        SchemaService.astro
        SchemaFAQ.astro
        SchemaBreadcrumb.astro
      ui/
        Button.astro
        Card.astro
        ServiceCard.astro
        TestimonialCard.astro
        StatCounter.astro
        BeforeAfterSlider.astro  (client:visible)
        FAQ.astro
        ContactForm.astro        (client:visible)
        QuoteForm.astro          (client:visible)
        GoogleMap.astro           (client:visible)
        ImageGallery.astro        (client:visible)
      sections/
        Hero.astro
        ServiceGrid.astro
        WhyChooseUs.astro
        ProcessTimeline.astro
        Testimonials.astro
        ServiceAreaMap.astro
        BlogPreview.astro
        CTASection.astro
    layouts/
      BaseLayout.astro
      ServiceLayout.astro
      LocationLayout.astro
      BlogLayout.astro
    pages/
      index.astro
      about.astro
      contact.astro
      emergency.astro
      gallery.astro
      testimonials.astro
      privacy-policy.astro
      terms-of-service.astro
      services/
        index.astro
        commercial-cleaning.astro
        janitorial-services.astro
        floor-care.astro
        carpet-cleaning.astro
        window-cleaning.astro
        pressure-washing.astro
        move-in-out-cleaning.astro
        water-damage-restoration.astro
        fire-damage-restoration.astro
        mold-remediation.astro
        emergency-services.astro
        post-construction-cleanup.astro
      locations/
        hayden-idaho.astro
        coeur-dalene.astro
        post-falls.astro
        rathdrum.astro
        sandpoint.astro
        spirit-lake.astro
        moscow-idaho.astro
        spokane.astro
        spokane-valley.astro
        liberty-lake.astro
        cheney.astro
      blog/
        index.astro
        [...slug].astro
    content/
      blog/
        (markdown files for blog posts)
    styles/
      global.css
    data/
      services.json
      locations.json
      testimonials.json
      faq.json
```

---

## Performance Budget

| Resource | Budget |
|----------|--------|
| HTML | < 30KB |
| CSS (total, gzipped) | < 10KB |
| JavaScript (total) | < 50KB (0KB for static pages) |
| Fonts (total) | < 100KB |
| Hero Image | < 200KB (AVIF) |
| Total Page Weight | < 500KB |
| HTTP Requests | < 15 |

---

## Island Architecture Rules

```
No client directive  → Static HTML, zero JS (DEFAULT for everything)
client:load          → Above-fold interactive (ONLY emergency call button if needed)
client:visible       → Below-fold interactive (forms, sliders, gallery, map)
client:idle          → Non-critical (newsletter, chat widget)
```

---

## Accessibility Checklist

- [ ] Skip navigation link on every page
- [ ] Semantic landmarks: header, nav, main, aside, footer
- [ ] Exactly one <main> per page
- [ ] All images have alt text (decorative: alt="" aria-hidden="true")
- [ ] Color contrast 4.5:1 normal text, 3:1 large text
- [ ] Focus indicator: 3px solid, 3:1 contrast
- [ ] Touch targets: minimum 48x48px, 8px spacing
- [ ] All form inputs have associated labels
- [ ] Keyboard navigable (Tab, Enter, Escape for modals)
- [ ] No keyboard traps
- [ ] aria-live regions for dynamic content
- [ ] Icons with aria-label or visually hidden text
- [ ] Base font size >= 16px
- [ ] No horizontal scroll at any viewport width

---

## SEO Meta Tags Template (per page)

```html
<title>{pageTitle} | Above & Beyond Janitorial</title>
<meta name="description" content="{unique 150-160 char description}" />
<link rel="canonical" href="{full canonical URL}" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="robots" content="index, follow" />
<meta property="og:title" content="{pageTitle}" />
<meta property="og:description" content="{description}" />
<meta property="og:url" content="{canonical URL}" />
<meta property="og:image" content="{og image URL}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Above & Beyond Janitorial" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{pageTitle}" />
<meta name="twitter:description" content="{description}" />
<meta name="twitter:image" content="{og image URL}" />
<link rel="sitemap" href="/sitemap-index.xml" />
```
