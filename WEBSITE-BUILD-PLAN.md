# Above & Beyond Janitorial - Epic Website Build Plan
## "$100,000 Website" for a 29-Year Local Legend

---

## VISION
Build a website so impressive that it positions Above & Beyond Janitorial as THE premium commercial cleaning and restoration company in North Idaho. The name says it all - "Above & Beyond" - and the website needs to match that promise. This site should make SERVPRO and ServiceMaster franchises look generic by comparison.

---

## TECH STACK
- **Framework**: Astro (static site generation for blazing speed)
- **Styling**: Tailwind CSS (utility-first, responsive-first)
- **Hosting**: Vercel (edge deployment, instant deploys, SSL)
- **CMS**: Optional - Decap CMS or Keystatic for Todd to update content
- **Forms**: Vercel serverless functions or Formspree
- **Analytics**: Google Analytics 4 + Google Search Console
- **Speed Target**: 95+ Lighthouse score across all metrics

---

## PHASE 1: BRAND FOUNDATION (Week 1)

### 1.1 Brand Identity
- Design professional logo (if none exists)
  - Primary logo + icon mark
  - Color variations (dark bg, light bg, monochrome)
- Define brand colors:
  - Suggestion: Deep navy blue (trust, professionalism) + vibrant gold/amber (premium, "above and beyond")
  - Accent: Clean white + slate gray
- Typography selection:
  - Headlines: Bold, commanding (e.g., Montserrat Bold or Inter Black)
  - Body: Clean, readable (e.g., Inter or Source Sans Pro)
- Brand voice: Professional, trustworthy, local, 29 years of expertise

### 1.2 Content Strategy
- Write brand story: "Since 1997, Todd Johnson has built..."
- Define core messaging pillars:
  1. **29 Years of Trust** - Nearly three decades serving North Idaho
  2. **Above & Beyond Service** - Not just cleaning, total care
  3. **Emergency Ready** - 24/7 restoration when disaster strikes
  4. **Local Expert** - Born and raised in the community

---

## PHASE 2: SITE ARCHITECTURE & SEO BLUEPRINT (Week 1-2)

### 2.1 Page Structure (23+ pages)

```
/                           → Homepage (hero + trust signals + services overview)
/about                      → Todd's story, company history, team, values
/services                   → Services overview hub
/services/commercial-cleaning  → Office/building cleaning
/services/janitorial        → Recurring janitorial contracts
/services/floor-care        → Strip, wax, buff, polish
/services/carpet-cleaning   → Commercial carpet cleaning
/services/window-cleaning   → Interior/exterior window cleaning
/services/pressure-washing  → Exterior pressure washing
/services/move-in-out-cleaning → Move in/move out
/services/water-damage-restoration  → Water/flood damage
/services/fire-damage-restoration   → Fire/smoke damage
/services/mold-remediation  → Mold assessment and removal
/services/emergency-services → 24/7 emergency response
/locations/hayden-idaho     → Local landing page
/locations/coeur-dalene     → Local landing page
/locations/post-falls       → Local landing page
/locations/spokane          → Local landing page
/locations/rathdrum         → Local landing page
/gallery                    → Before/after photos, project showcase
/testimonials               → Customer reviews and case studies
/blog                       → SEO content hub
/contact                    → Contact form, map, phone, email
/free-quote                 → Quote request form (lead gen)
/emergency                  → Emergency contact page (24/7)
```

### 2.2 SEO Strategy

#### Technical SEO
- Server-side rendered static HTML (Astro)
- Schema.org structured data (LocalBusiness, Service, FAQPage, Review)
- XML sitemap auto-generated
- Robots.txt optimized
- Canonical URLs on every page
- Open Graph + Twitter Card meta tags
- Image optimization (WebP with fallbacks)
- Lazy loading for images below fold
- Core Web Vitals optimized (LCP < 2.5s, FID < 100ms, CLS < 0.1)

#### On-Page SEO (per page)
- Unique title tags (60 chars max, location + service + brand)
- Meta descriptions (155 chars, action-oriented)
- H1 containing primary keyword
- H2/H3 hierarchy with secondary keywords
- Internal linking between related services
- Alt text on every image (descriptive, keyword-rich)
- FAQ schema on service pages

#### Local SEO (Critical Priority)
- Google Business Profile setup (FIRST THING - this alone is huge)
- NAP consistency across all directories
- Local schema markup on every page
- City-specific landing pages with unique content
- Embed Google Maps on contact page
- Claim and optimize: Yelp, Angi, BBB, Manta, Yellow Pages, MapQuest

#### Content SEO (Blog Strategy)
Monthly blog posts targeting long-tail keywords:
- "How to Handle Water Damage in Your Hayden Idaho Home"
- "5 Signs Your Commercial Building Needs Professional Cleaning"
- "What to Do When You Find Mold in Your Coeur d'Alene Business"
- "Commercial Floor Care Guide: Strip, Wax, and Maintenance"
- "Emergency Flood Cleanup: Steps to Take Before the Pros Arrive"
- "Why North Idaho Businesses Choose Professional Janitorial Services"

---

## PHASE 3: DESIGN & UX (Week 2-3)

### 3.1 Homepage Design
- **Hero Section**: Full-width dramatic image/video background
  - Headline: "29 Years of Going Above & Beyond for North Idaho"
  - Subhead: "Commercial Cleaning | Restoration | Emergency Services"
  - Two CTAs: "Get a Free Quote" + "Emergency? Call Now"
  - Trust badges below hero: "Since 1997" | "24/7 Emergency" | "Licensed & Insured" | "Chamber Member"

- **Services Grid**: 3-column cards with icons for each major service category

- **Why Choose Us Section**: 
  - 29 years experience
  - Local, owner-operated
  - 24/7 emergency response
  - Both cleaning AND restoration
  - Insurance claims expertise

- **Testimonials Carousel**: Customer quotes with names and companies

- **Service Area Map**: Interactive map showing coverage area

- **Emergency Banner**: Sticky bottom bar with phone number (always visible)

- **Footer**: Full contact info, services list, location links, social links

### 3.2 Key UX Elements (Every Page)
- Sticky header with logo + phone number + "Get Quote" button
- Emergency ribbon/banner (red, always visible on restoration pages)
- Click-to-call phone number (mobile)
- Breadcrumbs for navigation
- Related services sidebar
- CTA at bottom of every page
- Live chat widget (optional but recommended)
- Mobile-first responsive design (60%+ traffic will be mobile)

### 3.3 Gallery/Portfolio Page
- Before/after slider component for restoration work
- Filterable gallery by service type
- Project case studies with details

---

## PHASE 4: DEVELOPMENT (Week 3-5)

### 4.1 Astro Project Setup
- Initialize Astro project with Tailwind CSS
- Configure Vercel deployment
- Set up component library:
  - Header/Nav (sticky, mobile hamburger)
  - Footer
  - Hero sections
  - Service cards
  - Testimonial carousel
  - Before/after slider
  - Contact form
  - Quote request form
  - Google Map embed
  - Emergency banner
  - FAQ accordion
  - Blog post layout
  - Image gallery with lightbox

### 4.2 Page Development (Priority Order)
1. Homepage
2. Contact / Free Quote
3. Emergency page
4. All service pages (12 pages)
5. About page
6. Location pages (5 pages)
7. Gallery
8. Testimonials
9. Blog layout + first 3 posts

### 4.3 Performance Optimization
- Image pipeline: WebP conversion, responsive srcset, lazy loading
- Font optimization: Subset, preload critical fonts
- CSS: Purge unused Tailwind classes
- JavaScript: Minimal, defer non-critical
- Caching headers configured on Vercel

---

## PHASE 5: CONTENT CREATION (Week 2-4, parallel with dev)

### 5.1 Copywriting
- Homepage copy (500 words)
- About page (800 words - Todd's story, company history)
- 12 service pages (400-600 words each, unique content)
- 5 location pages (300-500 words each, locally relevant)
- Emergency page (300 words, action-oriented)
- Contact page copy
- FAQ content (10-15 questions per service category)
- 3 initial blog posts (800-1200 words each)

### 5.2 Visual Content
- Stock photography selection (premium, not generic):
  - Commercial building interiors
  - Professional cleaning crews
  - Restoration equipment
  - Before/after examples
  - North Idaho landscapes (for local feel)
- Custom graphics:
  - Service icons
  - Process infographics
  - Trust badges
  - Call-to-action graphics

### 5.3 Placeholder Strategy
- Use high-quality stock photos initially
- Flag every stock image for replacement with real photos
- Design photo shot list for Todd (what photos to take and how)

---

## PHASE 6: LAUNCH PREPARATION (Week 5-6)

### 6.1 Pre-Launch Checklist
- [ ] All pages built and content loaded
- [ ] Forms tested (contact, quote, emergency)
- [ ] Mobile responsive on all devices
- [ ] Cross-browser testing (Chrome, Safari, Firefox, Edge)
- [ ] Lighthouse audit: 95+ on all metrics
- [ ] Schema markup validated
- [ ] XML sitemap submitted to Google Search Console
- [ ] Google Analytics 4 installed and tracking
- [ ] SSL certificate active
- [ ] 404 page designed
- [ ] Favicon and app icons
- [ ] Social sharing previews (OG tags)
- [ ] Alt text on every image
- [ ] All links tested (no broken links)
- [ ] Print stylesheet (for quote/estimate pages)
- [ ] Cookie consent (if needed)
- [ ] Privacy policy page
- [ ] Terms of service page

### 6.2 Domain Strategy
- Secure domain: `aboveandbeyondjanitorial.com` or similar
  - Note: `abovebeyondjanitorial.com` is taken (Georgia company)
  - Alternatives: `abovebeyondcda.com`, `abnbjanitorial.com`, `abovebeyondidaho.com`
- Configure DNS and SSL on Vercel
- Set up email forwarding (todd@domain.com)

---

## PHASE 7: POST-LAUNCH (Ongoing)

### 7.1 Google Business Profile (DAY ONE PRIORITY)
- Create and verify Google Business Profile
- Add all services, hours, photos
- Set up Google Posts (weekly updates)
- Begin requesting reviews from happy customers

### 7.2 Directory Cleanup
- Claim Manta listing
- Create Yelp listing
- Create Angi listing
- Apply for BBB accreditation
- Update Yellow Pages
- Update MapQuest
- Ensure NAP consistency everywhere

### 7.3 Review Acquisition Strategy
- Create a simple review request card/email for Todd to send after jobs
- Set up review links (Google, Yelp, Facebook)
- Target: 5 reviews in first month, 20 in first quarter

### 7.4 Content Calendar
- 2 blog posts per month
- Weekly Google Business Profile posts
- Monthly testimonial collection
- Quarterly case study

---

## BUDGET BREAKDOWN (What This Would Cost at Agency Rates)

| Item | Agency Cost | Our Cost |
|---|---|---|
| Brand Identity & Logo | $5,000-$15,000 | $0 (AI-assisted) |
| UX/UI Design | $15,000-$30,000 | $0 (AI-assisted) |
| Content Strategy & SEO | $10,000-$20,000 | $0 (AI-assisted) |
| Copywriting (23+ pages) | $8,000-$15,000 | $0 (AI-assisted) |
| Development | $20,000-$40,000 | $0 (AI-assisted) |
| Photography | $3,000-$5,000 | Todd's phone + guidance |
| Local SEO Setup | $5,000-$10,000 | $0 (AI-assisted) |
| Blog Content (initial) | $3,000-$5,000 | $0 (AI-assisted) |
| **Total** | **$69,000-$140,000** | **~$0 + Vercel hosting** |

---

## IMMEDIATE NEXT STEPS

1. **Share this plan with Todd** - Get his buy-in and feedback
2. **Collect from Todd**:
   - Logo (or approval to create one)
   - Photos (or schedule a photo day)
   - His story and "why"
   - Client testimonials (even verbal ones we can write up)
   - Certifications list
   - Confirmed service area
   - Preferred contact info for the site
3. **Secure domain name**
4. **Set up Google Business Profile** (can do immediately, huge SEO impact)
5. **Begin building** - Start with Astro + Tailwind scaffolding

---

## THE "ABOVE & BEYOND" DIFFERENCE

What makes this a $100K website and not a $5K template:

1. **29 years of story** - We lean HARD into the longevity. Most competitors are 5-10 years old.
2. **Dual expertise** - No competitor owns both janitorial AND restoration online. We own both.
3. **Local SEO domination** - 5 city-specific pages, each ranking independently.
4. **Content depth** - Every service gets its own optimized page, not a bullet point.
5. **Emergency-first UX** - When someone's basement is flooding at 2am, they find Todd in 3 seconds.
6. **Trust architecture** - 29 years, chamber member, insurance provider, real testimonials.
7. **Performance** - Sub-2-second load times crush every local competitor.
8. **Blog authority** - Ongoing content establishes Todd as THE expert in North Idaho.
