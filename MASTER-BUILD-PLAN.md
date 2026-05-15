# ABOVE & BEYOND JANITORIAL - MASTER BUILD PLAN
## The $100,000 Website Blueprint | Astro + Tailwind CSS + Vercel
## Lighthouse Target: 100/100 in ALL Categories

---

## EXECUTIVE SUMMARY

We are building the most SEO-optimized, highest-performing, best-designed janitorial and water damage restoration website in the Pacific Northwest. This site will:

- Score **100/100 on Lighthouse** in Performance, Accessibility, Best Practices, and SEO
- Target **1,451+ keywords** across 11 cities in North Idaho and Eastern Washington
- Include **35+ fully optimized pages** with unique content
- Feature design patterns stolen from the **25 best cleaning/restoration websites** nationwide
- Implement **complete Schema.org structured data** (LocalBusiness, Service, FAQPage, BreadcrumbList, AggregateRating)
- Be built for **AI visibility** (Google AI Overviews, ChatGPT, Perplexity) from day one

---

## TECH STACK (Final)

| Component | Technology | Why |
|-----------|-----------|-----|
| Framework | Astro 5 (static output) | Zero JS by default, fastest possible TTFB |
| Styling | Tailwind CSS 4 via @tailwindcss/vite | Automatic purging, < 10KB CSS |
| Hosting | Vercel (static adapter) | Edge CDN, < 200ms TTFB globally |
| Images | Astro built-in (AVIF > WebP > JPEG) | Automatic optimization, responsive srcset |
| Fonts | Astro Fonts API, self-hosted Inter Variable | No FOUT, preloaded critical font |
| Forms | Vercel serverless functions | No external dependency |
| Analytics | GA4 + Google Search Console + Vercel Speed Insights | Real user metrics |
| Sitemap | @astrojs/sitemap (auto-generated) | Always current |
| Schema | astro-seo-schema (TypeScript-safe) | Validated structured data |

---

## BRAND IDENTITY

### Colors (Inspired by best-in-class analysis)
- **Primary:** Deep Navy `#1B2B4B` (trust, authority, professionalism)
- **Secondary:** Vibrant Teal/Green `#0D9488` (clean, fresh, eco-conscious)
- **Accent Emergency:** Warm Red `#DC2626` (urgency - restoration CTAs only)
- **Accent Gold:** `#D4A843` ("Above & Beyond" premium feel)
- **Neutral Light:** `#F8FAFC` (backgrounds)
- **Neutral Dark:** `#1E293B` (body text)
- **White:** `#FFFFFF` (cleanliness)

### Typography
- **Headlines:** Inter Variable (700-900 weight) - Bold, commanding
- **Body:** Inter Variable (400-500 weight) - Clean, readable
- **Base Size:** 16px minimum (WCAG AA requirement)
- **Self-hosted woff2 only** - no Google Fonts CDN dependency

### Brand Voice
- Professional but warm
- Local and community-focused ("your neighbors since 1997")
- Expert without being condescending
- Urgent when needed (restoration), calm when appropriate (janitorial)
- 29 years of earned authority in every sentence

---

## SITE ARCHITECTURE (35+ Pages)

### Tier 1 - Core Pages (8)
```
/                                    → Homepage
/about                               → Todd's Story + Company History
/services                            → Services Hub
/contact                             → Contact + Free Quote Form
/emergency                           → 24/7 Emergency Response
/gallery                             → Before/After + Project Showcase
/testimonials                        → Customer Reviews + Case Studies
/blog                                → SEO Content Hub
```

### Tier 2 - Service Pages (12)
```
/services/commercial-cleaning        → Office/Building Cleaning
/services/janitorial-services        → Recurring Janitorial Contracts
/services/floor-care                 → Strip, Wax, Buff, Polish
/services/carpet-cleaning            → Commercial Carpet Cleaning
/services/window-cleaning            → Interior/Exterior Windows
/services/pressure-washing           → Exterior Pressure Washing
/services/move-in-out-cleaning       → Move In/Move Out
/services/water-damage-restoration   → Water/Flood Damage
/services/fire-damage-restoration    → Fire/Smoke Damage
/services/mold-remediation           → Mold Assessment & Removal
/services/emergency-services         → 24/7 Emergency Hub
/services/post-construction-cleanup  → New Construction Cleaning
```

### Tier 3 - Location Pages (11)
```
/locations/hayden-idaho              → Headquarters city
/locations/coeur-dalene              → Largest nearby market
/locations/post-falls                → Adjacent market
/locations/rathdrum                  → Adjacent market
/locations/sandpoint                 → Northern market
/locations/spirit-lake               → Niche market (zero competition)
/locations/moscow-idaho              → University market
/locations/spokane                   → Major cross-state market
/locations/spokane-valley            → Adjacent to Spokane
/locations/liberty-lake              → Adjacent to Spokane
/locations/cheney                    → University market (zero competition)
```

### Tier 4 - Blog Posts (Initial 6, then 2/month ongoing)
```
/blog/what-to-do-water-damage-first-24-hours
/blog/commercial-cleaning-cost-north-idaho
/blog/prevent-mold-pacific-northwest
/blog/how-often-office-carpets-cleaned
/blog/water-damage-insurance-claims-idaho
/blog/spring-cleaning-checklist-commercial-buildings
```

### Tier 5 - Legal/Utility (3)
```
/privacy-policy
/terms-of-service
/sitemap (HTML sitemap for users)
```

---

## HOMEPAGE DESIGN SPECIFICATION

### Stolen Design Patterns (Best of the Best)

**From SERVPRO:** Icon-based service navigation cards
**From PuroClean:** "Paramedics of Property Damage" style positioning + AI chat
**From Coverall:** Industry/workplace-type navigation
**From Synergy Maids:** Live social proof counter
**From Paul Davis:** Animated process timeline
**From BELFOR:** Animated statistics counters
**From Stover's (floodandfire.com):** Family-owned authentic storytelling
**From Water Out Fort Wayne:** Before/after comparison sliders
**From Annie Cleaning:** Award/trust badge carousel
**From Better Life Home:** Instant pricing tool + sticky Book Now

### Homepage Section Flow

```
1. EMERGENCY ALERT BAR (conditional/always-on)
   - Red bar: "Water Damage Emergency? Call Now: (208) 818-3175"
   - Click-to-call on mobile

2. STICKY HEADER
   - Logo (left)
   - Main nav: Services | Locations | About | Gallery | Blog | Contact
   - Phone number + "Free Quote" button (right)
   - Stays visible on scroll

3. HERO SECTION (full-width)
   - Background: Professional team photo or subtle video
   - H1: "Going Above & Beyond for North Idaho Since 1997"
   - Subhead: "Commercial Cleaning | Water Damage Restoration | 24/7 Emergency"
   - Dual CTAs:
     - Primary (teal): "Get a Free Quote"
     - Emergency (red): "Emergency? Call (208) 818-3175"
   - Trust row below: "29 Years" | "24/7 Emergency" | "Licensed & Insured" | "Chamber Member"

4. SPLIT SERVICE PATH (from SERVPRO + PuroClean)
   - Two visual cards side-by-side:
   - LEFT: "Commercial Cleaning" (calm blue/teal, building icon)
     - "Office Cleaning | Floor Care | Windows | Carpet | Pressure Washing"
     - CTA: "Schedule Service"
   - RIGHT: "Emergency Restoration" (urgent red/orange, alert icon)
     - "Water Damage | Fire Damage | Mold | 24/7 Response"
     - CTA: "Get Help Now"

5. ANIMATED STATISTICS (from BELFOR)
   - Counter-style numbers animating on scroll:
   - "29+ Years" | "10,000+ Jobs" | "11 Cities Served" | "24/7 Response"

6. SERVICE ICON GRID (from SERVPRO)
   - 3x4 grid of service cards with custom icons
   - Each card: Icon + Service Name + 1-line description + "Learn More" link
   - 12 services total

7. WHY ABOVE & BEYOND (from Coverall + Annie Cleaning)
   - "The Above & Beyond Difference"
   - 4-column grid:
     - 29 Years Experience (icon + paragraph)
     - Local, Owner-Operated (icon + paragraph)
     - 24/7 Emergency Response (icon + paragraph)
     - Insurance Claims Experts (icon + paragraph)

8. BEFORE/AFTER SLIDER (from Water Out Fort Wayne)
   - Interactive drag slider showing restoration work
   - "See Our Work" heading
   - 3-4 examples cycling

9. PROCESS TIMELINE (from Paul Davis)
   - "How It Works" - 4-step visual timeline
   - For cleaning: Contact > Custom Plan > Professional Clean > Ongoing Care
   - For restoration: Call Us > Rapid Response > Restore > Return to Normal

10. TESTIMONIALS (from PuroClean + South Beach)
    - Carousel of customer quotes with names and cities
    - Star ratings displayed
    - "Read All Reviews" link

11. SERVICE AREA MAP
    - Interactive map of North Idaho + Eastern Washington
    - Clickable city markers linking to location pages
    - "Proudly Serving the Inland Northwest Since 1997"

12. BLOG PREVIEW (from Coverall's "Fresh Thoughts")
    - Latest 3 blog post cards with thumbnails
    - "Expert Tips & Guides" heading

13. CTA SECTION
    - Full-width teal background
    - "Ready to Experience the Above & Beyond Difference?"
    - Phone number + "Get Your Free Quote" button

14. FOOTER
    - 4-column layout:
      - Company info + NAP + phone
      - Services links
      - Locations links
      - Quick links (About, Contact, Blog, Privacy, Terms)
    - Social media icons
    - "Licensed & Insured | Chamber Member" badges
    - Copyright line

15. STICKY MOBILE BOTTOM BAR
    - Only on mobile (<768px)
    - Phone icon + "Call Now" | Message icon + "Free Quote"
    - Always visible, above fold
```

---

## SERVICE PAGE TEMPLATE

Every service page follows this structure (stolen from top performers):

```
1. BREADCRUMBS (with BreadcrumbList schema)
   Home > Services > [Service Name]

2. HERO SECTION
   - H1: "[Service Name] in North Idaho & Spokane"
   - 2-3 sentence description
   - CTA: "Get a Free Quote" + Phone number
   - Hero image (professional photo or stock)

3. DIRECT ANSWER BLOCK (for AI/GEO optimization)
   - First 40-60 words: concise answer to "what is [service]?"
   - This is what Google AI Overviews and ChatGPT will pull

4. SERVICE DETAILS (400-600 words unique content)
   - What the service includes
   - Who it's for (industries/building types)
   - Our approach/process
   - Why choose us for this service

5. OUR PROCESS (3-4 steps with icons)
   - Step 1: Assessment
   - Step 2: Custom Plan
   - Step 3: Professional Service
   - Step 4: Quality Check

6. INDUSTRIES SERVED (from Coverall pattern)
   - Icon grid: Offices, Medical, Dental, Schools, Churches, Restaurants, etc.

7. BEFORE/AFTER GALLERY (restoration pages only)
   - 2-3 slider examples

8. FAQ SECTION (with FAQPage schema)
   - 5-8 questions specific to this service
   - Natural keyword inclusion
   - Structured for rich snippets

9. TESTIMONIALS
   - 2-3 reviews specific to this service

10. RELATED SERVICES
    - "You May Also Need" section linking to related services

11. CTA SECTION
    - "Schedule [Service Name] Today"
    - Form + Phone number

12. LOCATION LINKS
    - "Available in: Hayden | CDA | Post Falls | Spokane | ..."
```

---

## LOCATION PAGE TEMPLATE

Every location page must have **800-1,500 words of genuinely unique content**:

```
1. H1: "[Service Type] in [City], [State]"

2. DIRECT ANSWER (40-60 words)

3. LOCAL INTRO (200-300 words)
   - Reference specific neighborhoods, landmarks, building types
   - Local climate/weather challenges relevant to services
   - "We've been serving [City] since [year]"

4. SERVICES AVAILABLE HERE
   - Full service list with links to service pages

5. LOCAL CASE STUDY (200-300 words)
   - Specific project in this city (real or realistic template)
   - Before/after photos from this area

6. LOCAL CHALLENGES SECTION (150-200 words)
   - Climate-specific issues (freeze-thaw for water damage, etc.)
   - Local building types (commercial, industrial, etc.)
   - Seasonal considerations

7. LOCAL FAQ (5-8 questions with city name)

8. LOCAL TESTIMONIALS
   - Reviews from customers in this specific city

9. EMBEDDED GOOGLE MAP
   - Centered on this city, showing service area

10. NEARBY CITIES
    - "Also serving nearby [City], [City], and [City]"
    - Internal links to other location pages

11. CTA: "Get a Free Quote in [City]"
```

---

## STRUCTURED DATA (JSON-LD) - EVERY PAGE

### Homepage
- WebSite schema
- Organization/LocalBusiness schema (HomeAndConstructionBusiness)
- AggregateRating (when reviews exist)

### Service Pages
- Service schema with areaServed
- FAQPage schema
- BreadcrumbList schema

### Location Pages
- LocalBusiness schema with specific city areaServed
- FAQPage schema
- BreadcrumbList schema

### Blog Posts
- Article schema
- BreadcrumbList schema

### All Pages
- BreadcrumbList schema
- Organization reference via @id

---

## TECHNICAL SPECS FOR 100/100 LIGHTHOUSE

### Performance Targets
| Metric | Target |
|--------|--------|
| LCP | < 1.5s |
| INP | < 100ms |
| CLS | < 0.05 |
| FCP | < 1.0s |
| TTFB | < 200ms |
| TBT | < 50ms |
| Total JS | < 50KB (ideally 0KB for static pages) |
| Total CSS | < 10KB gzipped |
| Total Page Size | < 500KB |

### Image Pipeline
- AVIF > WebP > JPEG fallback chain
- Responsive srcset: [400, 800, 1200, 1600, 2000]
- Above-fold: `loading="eager"` + `<link rel="preload">`
- Below-fold: `loading="lazy"` (default)
- Explicit width/height on every image (prevents CLS)

### Font Strategy
- Self-hosted Inter Variable (woff2 only)
- Preload critical font in <head>
- font-display: swap (automatic via Astro Fonts API)
- Subset to latin characters

### Caching (vercel.json)
- Static assets (/_astro/*): `public, max-age=31536000, immutable`
- Fonts: `public, max-age=31536000, immutable`
- HTML: `public, max-age=0, must-revalidate`
- Security headers: HSTS, CSP, X-Frame-Options, X-Content-Type-Options

### Accessibility (WCAG 2.1 AA)
- Skip navigation link
- Semantic landmarks: header, nav, main, footer
- All images have alt text
- Color contrast: 4.5:1 normal text, 3:1 large text
- Focus indicators: 3px solid outline, 3:1 contrast
- Touch targets: minimum 48x48px
- Keyboard navigation for all interactive elements
- ARIA labels on all non-text interactive elements

---

## WHAT WE NEED FROM TODD (Prioritized)

### Must Have (Cannot Launch Without)
1. **Logo** - Existing or we design one
2. **Phone number confirmation** - Which number goes on the site?
3. **Email address** - For the contact form
4. **Service area confirmation** - Exactly which cities?
5. **Hours of operation** - Sources conflict (some say 7 days, some say Mon-Fri)
6. **Todd's headshot** - For the About page
7. **Quick bio/story** - Why he started, 2-3 sentences minimum

### Should Have (Makes it 10x better)
8. **5-10 job site photos** - Phone photos are fine
9. **3-5 customer testimonials** - Names and companies
10. **Before/after restoration photos** - Even phone quality works
11. **Equipment/vehicle photos** - Shows professionalism
12. **Certifications list** - IICRC? Others?
13. **Insurance partners** - Which companies do you work with?
14. **Client list** - Permission to name businesses you serve

### Nice to Have (We can work without)
15. **Team photos** - If employees exist
16. **Video of a job** - Even 30 seconds on a phone
17. **Specialty/niche info** - What are you best known for?
18. **Pricing ranges** - Willing to share?
19. **Response time** - How fast for emergencies?
20. **Community involvement** - Sponsorships, charity?

### What We Can Create Without Todd
- All website copy (based on our research)
- Blog posts
- FAQ content
- SEO metadata
- Design and development
- Stock photography (as placeholders)
- Brand identity (if no logo exists)
- All technical implementation

---

## SEO LAUNCH CHECKLIST (Day 1 Priority Order)

### Before Website Launch
1. [ ] Secure domain name
2. [ ] Set up Google Search Console
3. [ ] Set up Google Analytics 4
4. [ ] Set up Vercel project
5. [ ] Configure DNS and SSL

### Day of Launch
6. [ ] Submit sitemap to Google Search Console
7. [ ] Verify all pages render correctly
8. [ ] Run Lighthouse audit on every page (target 100/100)
9. [ ] Validate all Schema.org markup
10. [ ] Test all forms (contact, quote, emergency)
11. [ ] Test click-to-call on mobile
12. [ ] Cross-browser test (Chrome, Safari, Firefox, Edge)

### Week 1 After Launch
13. [ ] Create and verify Google Business Profile
14. [ ] Submit to Bing Places
15. [ ] Submit to Apple Business Connect
16. [ ] Claim Manta listing
17. [ ] Create Yelp listing
18. [ ] Create Angi listing
19. [ ] Apply for BBB accreditation
20. [ ] Update Yellow Pages, MapQuest, DexKnows
21. [ ] Submit to data aggregators (Factual, Data Axle, Neustar)
22. [ ] Create Facebook Business Page (or fix existing)
23. [ ] Create Instagram Business Profile
24. [ ] Set up LinkedIn Company Page
25. [ ] Join Hayden, CDA, Post Falls, Spokane Chambers of Commerce

### Month 1 After Launch
26. [ ] Begin review acquisition (target 5-10 Google reviews)
27. [ ] Start GBP posting schedule (2-3x/week)
28. [ ] Publish first 2 blog posts
29. [ ] Begin local link building outreach
30. [ ] Monitor rankings for primary keywords in all target cities
31. [ ] Submit to 20+ additional citation sites

### Ongoing Monthly
32. [ ] 2-4 blog posts published
33. [ ] GBP posts 2-3x/week
34. [ ] Review acquisition after every job
35. [ ] Respond to all reviews within 24 hours
36. [ ] Add new photos to GBP weekly
37. [ ] Citation audit quarterly
38. [ ] Lighthouse audit monthly
39. [ ] Keyword ranking monitoring

---

## BUILD TIMELINE

| Week | Phase | Deliverables |
|------|-------|-------------|
| 1 | Brand + Architecture | Logo, colors, typography, site structure, domain secured |
| 1-2 | Content Creation | All page copy, meta tags, FAQs, schema markup |
| 2-3 | Design + Component Build | Astro project, Tailwind setup, component library, page templates |
| 3-4 | Page Development | All 35+ pages built with content loaded |
| 4-5 | Polish + Optimization | Lighthouse 100/100, cross-browser, mobile testing, accessibility audit |
| 5 | Launch | Deploy to Vercel, GBP setup, citation submissions |
| 5-6 | Post-Launch SEO | Blog cadence begins, review acquisition, link building |

---

## COMPETITIVE ADVANTAGE SUMMARY

Why this website will dominate the North Idaho market:

1. **No competitor does both janitorial AND restoration online well** - We own both verticals
2. **29 years in business** - More than any competitor except Environment Control (founded 1963, but they're national/generic)
3. **11 city-specific landing pages** - Competitors have 0-3 location pages
4. **1,451+ targeted keywords** - Competitors target maybe 20-50
5. **Perfect technical scores** - Competitors average 40-70 on Lighthouse
6. **AI-optimized content** - Ready for Google AI Overviews, ChatGPT, Perplexity citations
7. **Schema markup on every page** - Most competitors have zero structured data
8. **Blog content strategy** - Most local competitors don't blog at all
9. **Mobile-first design** - 75%+ of local searches are mobile
10. **Professional design** - Borrowed patterns from $100K+ enterprise sites (SERVPRO, BELFOR, PuroClean)

---

## SUPPORTING DOCUMENTS

All research files are in `/Users/jesseanglen/Documents/AboveBeyondJanitorial/`:

1. **RESEARCH.md** - Complete business intel and online presence audit
2. **GAP-ANALYSIS.md** - What we have vs. what we need from Todd
3. **KEYWORD-RESEARCH.md** - 1,451 keywords mapped to every page
4. **WEBSITE-BUILD-PLAN.md** - Original build plan (superseded by this document)
5. **MASTER-BUILD-PLAN.md** - This document (the definitive plan)

Research conducted by AI agents (not saved to files but referenced):
- Best Janitorial/Restoration Website Analysis (25 sites analyzed)
- Local SEO Playbook for Service-Area Businesses (2026)
- Technical SEO Specification for Lighthouse 100/100
- Competitive Keyword Gap Analysis
