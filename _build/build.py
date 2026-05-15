#!/usr/bin/env python3
"""Builder for Above & Beyond Janitorial static site.

Generates inner pages from a per-page config so shared chrome (nav, footer,
modal, head meta) stays in one place. Run from repo root:

    python3 _build/build.py

Outputs to site/. Idempotent — overwrites generated pages.
"""
import json
import os
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DOMAIN = "https://aboveandbeyondjanitorialservice.com"

# ---- Shared chrome ----------------------------------------------------------

def nav_html(active: str) -> str:
    items = [
        ("/services/",     "Services",    "services"),
        ("/service-area/", "Service area", "areas"),
        ("/about.html",    "About",       "about"),
        ("/faq.html",      "FAQ",         "faq"),
        ("/contact.html",  "Contact",     "contact"),
    ]
    links = "\n".join(
        f'          <a href="{href}"{" aria-current=\"page\"" if key==active else ""}>{label}</a>'
        for href, label, key in items
    )
    return f"""    <header class="nav">
      <div class="nav-inner">
        <a href="/" class="brand">
          <img src="/assets/logo.png" alt="Above &amp; Beyond logo" width="32" height="32" decoding="async" fetchpriority="high">
          <div class="brand-name">Above &amp; Beyond<span class="sub">Est. 1997</span></div>
        </a>
        <nav class="nav-links" aria-label="Main">
{links}
        </nav>
        <div class="nav-right">
          <a href="tel:+12088183175" class="nav-phone" aria-label="Call (208) 818-3175">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.37 1.9.72 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.35 1.85.59 2.81.72A2 2 0 0 1 22 16.92z"/></svg>
            (208) 818-3175
          </a>
          <button type="button" class="btn btn-primary" onclick="openQuote()">Get my facility quoted</button>
          <button type="button" class="nav-toggle" aria-label="Open menu" aria-expanded="false"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
        </div>
      </div>
    </header>"""


FOOTER_HTML = """<footer>
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="brand">
          <img src="/assets/logo.png" alt="Above &amp; Beyond logo" width="32" height="32" decoding="async" loading="lazy" style="width:32px;height:32px;">
          <div class="brand-name" style="color:white">Above &amp; Beyond<span class="sub">Est. 1997</span></div>
        </div>
        <p>Family-owned commercial janitorial services serving North Idaho since 1997. Licensed, bonded, insured, green-certified.</p>
      </div>
      <div>
        <h5>Services</h5>
        <ul>
          <li><a href="/services/commercial-janitorial.html">Commercial janitorial</a></li>
          <li><a href="/services/medical-dental.html">Medical &amp; dental</a></li>
          <li><a href="/services/carpet-extraction.html">Carpet extraction</a></li>
          <li><a href="/services/hard-floor-care.html">Hard-floor care</a></li>
          <li><a href="/services/window-cleaning.html">Window cleaning</a></li>
          <li><a href="/services/restroom-sanitation.html">Restroom sanitation</a></li>
        </ul>
      </div>
      <div>
        <h5>Service area</h5>
        <ul>
          <li><a href="/service-area/hayden.html">Hayden, ID</a></li>
          <li><a href="/service-area/coeur-dalene.html">Coeur d'Alene, ID</a></li>
          <li><a href="/service-area/post-falls.html">Post Falls, ID</a></li>
          <li><a href="/service-area/rathdrum.html">Rathdrum, ID</a></li>
          <li><a href="/service-area/sandpoint.html">Sandpoint, ID</a></li>
          <li><a href="/service-area/spirit-lake.html">Spirit Lake, ID</a></li>
          <li><a href="/service-area/athol.html">Athol, ID</a></li>
        </ul>
      </div>
      <div>
        <h5>Contact</h5>
        <ul>
          <li><a href="tel:+12088183175">(208) 818-3175</a></li>
          <li><a href="mailto:todd@aboveandbeyondjanitorialservice.com">todd@aboveandbeyondjanitorialservice.com</a></li>
          <li>Hayden, Idaho</li>
          <li>Evenings &amp; weekends</li>
          <li style="margin-top:8px;"><a href="/privacy.html">Privacy</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div>© 2026 ABOVE &amp; BEYOND JANITORIAL, INC.</div>
      <div>"EXPERIENCE THE IMAGE."</div>
      <div>LIC · BONDED · INSURED · GREEN-CERTIFIED</div>
    </div>
  </div>
</footer>"""

MODAL_HTML = """<!-- MODAL -->
<div class="modal-scrim" id="quote-modal" role="dialog" aria-modal="true" aria-labelledby="quote-modal-title" onclick="if(event.target===this)closeQuote()">
  <div class="modal" id="quote-modal-inner"></div>
</div>"""


# ---- Schema helpers ---------------------------------------------------------

def localbusiness_schema(area_served: list[str] | None = None) -> dict[str, Any]:
    area_served = area_served or [
        "Hayden", "Coeur d'Alene", "Post Falls", "Rathdrum",
        "Sandpoint", "Spirit Lake", "Athol",
    ]
    return {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "@id": f"{DOMAIN}/#business",
        "name": "Above & Beyond Janitorial, Inc.",
        "image": f"{DOMAIN}/assets/logo.png",
        "logo": f"{DOMAIN}/assets/logo.png",
        "url": f"{DOMAIN}/",
        "telephone": "+1-208-818-3175",
        "email": "todd@aboveandbeyondjanitorialservice.com",
        "priceRange": "$$",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Hayden",
            "addressRegion": "ID",
            "addressCountry": "US",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 47.766, "longitude": -116.786},
        "areaServed": [{"@type": "City", "name": c} for c in area_served],
        "founder": {"@type": "Person", "name": "Todd D. Johnson"},
        "foundingDate": "1997",
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "17:00", "closes": "23:00",
        }],
        "slogan": "Experience the image.",
    }


def breadcrumb_schema(trail: list[tuple[str, str | None]]) -> dict[str, Any]:
    """trail = [(label, url or None for final)]"""
    items = []
    for i, (label, url) in enumerate(trail, 1):
        entry = {"@type": "ListItem", "position": i, "name": label}
        if url:
            entry["item"] = f"{DOMAIN}{url}"
        items.append(entry)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def service_schema(name: str, description: str, page_path: str) -> dict[str, Any]:
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "serviceType": name,
        "description": description,
        "url": f"{DOMAIN}{page_path}",
        "provider": {"@id": f"{DOMAIN}/#business"},
        "areaServed": [
            {"@type": "City", "name": c} for c in
            ["Hayden", "Coeur d'Alene", "Post Falls", "Rathdrum", "Sandpoint", "Spirit Lake", "Athol"]
        ],
    }


# ---- Page assembly ---------------------------------------------------------

def breadcrumb_html(trail: list[tuple[str, str | None]]) -> str:
    parts = []
    last = len(trail) - 1
    for i, (label, url) in enumerate(trail):
        if i > 0:
            parts.append('<span class="sep">/</span>')
        if i == last or not url:
            parts.append(f'<span aria-current="page">{label}</span>')
        else:
            parts.append(f'<a href="{url}">{label}</a>')
    return '<nav class="breadcrumb" aria-label="Breadcrumb">' + " ".join(parts) + "</nav>"


def build_page(
    *,
    out_path: str,
    title: str,
    description: str,
    canonical_path: str,
    active_nav: str,
    breadcrumb_trail: list[tuple[str, str | None]],
    hero_h1: str,
    hero_lede: str,
    hero_ctas: bool = True,
    body_content: str,
    extra_schemas: list[dict] | None = None,
):
    extra_schemas = extra_schemas or []
    canonical = f"{DOMAIN}{canonical_path}"
    og_image = f"{DOMAIN}/og-image.png"

    schema_blocks = [localbusiness_schema(), breadcrumb_schema(breadcrumb_trail)]
    schema_blocks.extend(extra_schemas)
    schema_html = "\n".join(
        f'<script type="application/ld+json">{json.dumps(s, separators=(",", ":"), ensure_ascii=False)}</script>'
        for s in schema_blocks
    )

    crumbs = breadcrumb_html(breadcrumb_trail)
    cta_html = ""
    if hero_ctas:
        cta_html = """
          <div class="hero-ctas" style="margin-top:28px;">
            <button type="button" class="btn btn-primary btn-lg" onclick="openQuote()">Get my facility quoted</button>
            <a href="tel:+12088183175" class="btn btn-outline-light btn-lg">Call (208) 818-3175</a>
          </div>"""

    page_html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">

<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=Geist+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=Geist+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/assets/css/styles.css">

{schema_html}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<section class="page-hero">
  <div class="hero-content">
{nav_html(active_nav)}
    <div class="page-hero-inner">
      <div class="wrap">
        {crumbs}
        <h1>{hero_h1}</h1>
        <p class="lede">{hero_lede}</p>{cta_html}
      </div>
    </div>
  </div>
</section>

<main id="main">
{body_content}
</main>

{FOOTER_HTML}

{MODAL_HTML}
<script src="/assets/js/app.js" defer></script>
</body>
</html>
"""
    full_path = SITE / out_path.lstrip("/")
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(page_html, encoding="utf-8")
    print(f"  wrote {out_path}")


# ---- Page content blocks ---------------------------------------------------

CTA_SECTION = """<section class="final">
  <div class="final-inner">
    <h2>Free walkthrough. <span class="accent">Written quote in 48 hours.</span></h2>
    <p>Tell us your facility type and frequency. We'll come look, write the scope, put a fixed price on it. No high-pressure pitch.</p>
    <div class="final-ctas">
      <button type="button" class="btn btn-primary btn-lg" onclick="openQuote()">Get my facility quoted</button>
      <a href="tel:+12088183175" class="btn btn-outline-light btn-lg">Call (208) 818-3175</a>
    </div>
  </div>
</section>"""


def service_body(*, included: list[str], who_for: str, process: str, faqs: list[tuple[str, str]], related_links: list[tuple[str, str]]) -> str:
    incl_html = "\n            ".join(f"<li>{item}</li>" for item in included)
    faq_html = "\n        ".join(
        f'<details class="fq"{" open" if i == 0 else ""}>\n          <summary>{q}<span class="plus">+</span></summary>\n          <p>{a}</p>\n        </details>'
        for i, (q, a) in enumerate(faqs)
    )
    related_html = "\n        ".join(f'<li><a href="{href}">{label}</a></li>' for label, href in related_links)
    return f"""<section class="lightpage">
  <div class="wrap">
    <div style="display:grid;grid-template-columns:1.5fr 1fr;gap:64px;align-items:start;" class="svc-grid">
      <div class="prose">
        <div class="eyebrow brass">/ what's included</div>
        <h2>Every scope, written down.</h2>
        <p>{who_for}</p>
        <ul>
            {incl_html}
        </ul>
        <h2>How it works.</h2>
        <p>{process}</p>
      </div>
      <aside style="background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:28px;">
        <div class="eyebrow brass" style="margin-bottom:14px;">/ related</div>
        <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:8px;font-size:14.5px;">
        {related_html}
        </ul>
        <hr style="border:none;border-top:1px solid var(--line);margin:22px 0;">
        <p style="font-size:13.5px;color:var(--ink-2);margin:0 0 14px;">Ready for a quote on this service?</p>
        <button type="button" class="btn btn-primary" onclick="openQuote()" style="width:100%;justify-content:center;">Get quoted →</button>
      </aside>
    </div>
  </div>
</section>

<section class="faq-section">
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="eyebrow">/ faq</div>
        <h2 class="section-h">Questions <span class="muted">we hear.</span></h2>
      </div>
      <div></div>
    </div>
    <div class="faq-grid">
      <div></div>
      <div>
        {faq_html}
      </div>
    </div>
  </div>
</section>

{CTA_SECTION}"""


def city_body(*, city: str, distance: str, services_blurb: str, local_paragraph: str, status: str) -> str:
    return f"""<section class="lightpage">
  <div class="wrap">
    <div style="display:grid;grid-template-columns:1.5fr 1fr;gap:64px;align-items:start;" class="svc-grid">
      <div class="prose">
        <div class="eyebrow brass">/ service in {city}</div>
        <h2>Commercial cleaning, on the schedule {city} buildings actually need.</h2>
        <p>{local_paragraph}</p>
        <p>{services_blurb}</p>
        <h2>Services in {city}</h2>
        <ul>
          <li><a href="/services/commercial-janitorial.html">Recurring commercial janitorial</a> — nightly to weekly.</li>
          <li><a href="/services/medical-dental.html">Medical &amp; dental office cleaning</a> — OSHA-aligned, EPA disinfectants.</li>
          <li><a href="/services/carpet-extraction.html">Carpet hot-water extraction</a> — quarterly programs.</li>
          <li><a href="/services/hard-floor-care.html">Hard-floor care</a> — strip, wax, burnish, grout.</li>
          <li><a href="/services/window-cleaning.html">Window cleaning</a> — storefront to mid-rise glass.</li>
          <li><a href="/services/restroom-sanitation.html">Restroom sanitation</a> — touch-point disinfection, restock.</li>
        </ul>
        <h2>How {city} accounts work</h2>
        <p>Same crew every visit. Written scope, fixed monthly price for recurring contracts. Owner-direct phone on every invoice. Most accounts start within a week of a signed proposal.</p>
        <p><strong>Distance from HQ:</strong> {distance}. <strong>Current cadence:</strong> {status}.</p>
      </div>
      <aside style="background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:28px;position:sticky;top:24px;">
        <div class="eyebrow brass" style="margin-bottom:14px;">/ {city} quote</div>
        <p style="font-size:14.5px;color:var(--ink-2);margin:0 0 18px;line-height:1.55;">Free walkthrough. Written, fixed-price scope in 48 hours.</p>
        <button type="button" class="btn btn-primary" onclick="openQuote()" style="width:100%;justify-content:center;margin-bottom:8px;">Get my facility quoted</button>
        <a href="tel:+12088183175" class="btn btn-outline-dark" style="width:100%;justify-content:center;">Call (208) 818-3175</a>
        <hr style="border:none;border-top:1px solid var(--line);margin:22px 0;">
        <div class="eyebrow brass" style="margin-bottom:10px;">/ other cities</div>
        <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:6px;font-size:13.5px;">
          <li><a href="/service-area/hayden.html">Hayden</a></li>
          <li><a href="/service-area/coeur-dalene.html">Coeur d'Alene</a></li>
          <li><a href="/service-area/post-falls.html">Post Falls</a></li>
          <li><a href="/service-area/rathdrum.html">Rathdrum</a></li>
          <li><a href="/service-area/sandpoint.html">Sandpoint</a></li>
          <li><a href="/service-area/spirit-lake.html">Spirit Lake</a></li>
          <li><a href="/service-area/athol.html">Athol</a></li>
        </ul>
      </aside>
    </div>
  </div>
</section>

{CTA_SECTION}"""


# ---- Page configs ----------------------------------------------------------

SERVICES = [
    {
        "slug": "commercial-janitorial",
        "name": "Commercial janitorial",
        "title": "Commercial Janitorial Services North Idaho | Above & Beyond",
        "description": "Recurring commercial janitorial for North Idaho offices, banks, clinics, retail. Same crew every visit, written scope, fixed monthly price.",
        "h1_main": "Commercial janitorial,",
        "h1_accent": "nightly to weekly.",
        "lede": "Trash, dust, vacuum, surfaces, restrooms, kitchen — all on a written checklist, on the cadence your building actually needs.",
        "included": [
            "Trash &amp; recycling collection, liner replacement",
            "Hard-surface dusting (desks, ledges, fixtures)",
            "Vacuuming + spot carpet treatment",
            "Restroom sanitation, fixture detailing, consumable restock",
            "Kitchen / breakroom: counters, sinks, appliances, floors",
            "High-traffic disinfection (door handles, switches, shared surfaces)",
            "Floors mopped or auto-scrubbed where applicable",
            "Monthly written audit, owner-direct line for issues",
        ],
        "who_for": "Built for office buildings, multi-tenant commercial, professional services, banks, retail back-of-house. Cadence ranges from 5+ nights/week down to monthly. We meet you where the building is.",
        "process": "Walkthrough → written line-item scope → same-crew assignment → start in 5–7 days. Monthly invoicing. Re-clean inside 24 hours if anything misses.",
        "faqs": [
            ("How often do you clean?", "Most accounts run 5+ nights/week (after-hours). We also offer 2–4 nights/week, weekly, or monthly cadence — whatever fits the building's traffic."),
            ("Who supplies the chemicals and equipment?", "We do. Green-certified by default. We can match your facility's procurement standards (low-VOC, EPA Safer Choice, etc.) on request."),
            ("Is it the same crew every night?", "Yes. The same team for the life of the contract — they learn your building. Crew tenure averages 3.5 years."),
            ("How are missed items handled?", "Call. Inside 24 hours we re-clean it at no charge. No invoice tricks, no minimum clauses."),
        ],
    },
    {
        "slug": "medical-dental",
        "name": "Medical &amp; dental cleaning",
        "title": "Medical & Dental Office Cleaning Idaho | Above & Beyond",
        "description": "OSHA-aligned medical and dental office cleaning across North Idaho. Color-coded microfiber, hospital-grade disinfectants, terminal cleans.",
        "h1_main": "Medical &amp; dental,",
        "h1_accent": "audit-ready every visit.",
        "lede": "Color-coded microfiber. EPA N-list disinfectants. OSHA-aligned protocols. Terminal cleans on demand for procedural rooms.",
        "included": [
            "Color-coded microfiber system (no cross-contamination)",
            "EPA-registered hospital-grade disinfectants (N-list eligible)",
            "Patient room turnover protocols",
            "Operatory wipe-down between patients (when scoped)",
            "Terminal cleans for procedural rooms",
            "Restroom + waiting-area sanitation",
            "OSHA-aligned bloodborne pathogen protocols",
            "After-hours service so clinical schedules aren't disrupted",
        ],
        "who_for": "Built for medical offices, dental practices, urgent care, specialty clinics, and outpatient facilities. Background-checked crew, comfortable in clinical environments after close.",
        "process": "We walk the facility with your office manager or clinical lead, map clean zones to color codes, set the terminal-clean cadence, and start within 5–7 days. Documented protocols, audit log on request.",
        "faqs": [
            ("Are your crews OSHA-trained?", "Yes. Bloodborne pathogen training, color-coded zone discipline, and proper PPE practices are baseline."),
            ("What disinfectants do you use?", "EPA-registered hospital-grade, N-list eligible for emerging viral pathogens. We can match your practice's preferred chemistry on request."),
            ("Can you do terminal cleans between cases?", "Yes — typically scoped as periodic or on-demand. Most clinics use us for end-of-day terminal cleans on procedural rooms."),
            ("Is documentation provided?", "Yes. We keep a written audit log of services, accessible to your practice administrator."),
        ],
    },
    {
        "slug": "carpet-extraction",
        "name": "Carpet extraction",
        "title": "Commercial Carpet Cleaning North Idaho | Above & Beyond",
        "description": "Truck-mount hot-water carpet extraction for North Idaho offices. Quarterly programs, spot treatment included with recurring janitorial.",
        "h1_main": "Carpet extraction,",
        "h1_accent": "truck-mount, scheduled.",
        "lede": "Hot-water extraction with commercial truck-mount equipment. Quarterly programs for high-traffic offices. Spot treatment bundled with recurring contracts.",
        "included": [
            "Pre-treatment of high-traffic lanes and visible soiling",
            "Hot-water extraction (truck-mount) — deep clean, fast dry",
            "Edge and corner detail",
            "Furniture moved and replaced (within scope)",
            "Drying fans deployed where needed",
            "Quarterly or scheduled cadence on contract",
            "Spot treatment included in recurring janitorial contracts",
            "Post-construction carpet first cleans",
        ],
        "who_for": "Offices with carpet tile or broadloom, retail showrooms, banks, churches, conference centers. Quarterly extraction extends carpet life 2–3× over vacuum-only.",
        "process": "Walk the space, map the carpet zones, set a quarterly schedule that fits your operations. We typically work after-hours so the carpet dries before your team is back.",
        "faqs": [
            ("How long does drying take?", "Truck-mount hot-water extraction dries in 2–6 hours with airflow. We schedule overnight to be safe."),
            ("Do you move furniture?", "Yes — within scope. Heavy/fragile items stay in place and we extract around them."),
            ("How often is needed?", "Quarterly for high-traffic commercial. Semi-annual works for low-traffic offices. We'll recommend based on the walkthrough."),
            ("Is this bundled with recurring contracts?", "Spot treatment is. Full extraction is typically a separate quarterly line item or per-project quote."),
        ],
    },
    {
        "slug": "hard-floor-care",
        "name": "Hard-floor care",
        "title": "Strip & Wax / Floor Care North Idaho | Above & Beyond",
        "description": "Strip and wax, burnishing, buffing, grout deep-cleans across North Idaho. VCT, LVT, concrete, terrazzo, hardwood — commercial floor care.",
        "h1_main": "Hard-floor care,",
        "h1_accent": "strip, wax, burnish, buff.",
        "lede": "VCT, LVT, concrete, terrazzo, hardwood. Strip and wax cycles, burnishing programs, grout deep-cleans. Whatever your flooring spec requires.",
        "included": [
            "Strip and wax (VCT, LVT) — full cycle including base coat + finish",
            "Burnishing programs for gloss recovery",
            "Buffing on schedule",
            "Concrete sealing and polishing",
            "Terrazzo restoration",
            "Hardwood maintenance and recoating",
            "Grout deep-clean (tile floors)",
            "Quarterly or annual program scheduling",
        ],
        "who_for": "Retail, healthcare, education, government, banking — any facility with hard floors that need to look as good as the brand. We work on a scheduled cycle so floors never drift below standard.",
        "process": "Walkthrough → floor-by-floor scope and cycle plan → schedule that fits operations (often after-hours or weekend) → start. Documented in your service agreement.",
        "faqs": [
            ("How often should VCT be stripped?", "Annually for most commercial environments. Burnishing every 60–90 days between full strips keeps the gloss up."),
            ("Do you work on hardwood?", "Yes — including screen-and-recoat to refresh finish without full sanding."),
            ("Concrete floors?", "Yes — including polish, seal, and ongoing maintenance programs."),
            ("Can you scope after-hours or weekends?", "Yes. That's typical for floor work because of drying and curing times."),
        ],
    },
    {
        "slug": "window-cleaning",
        "name": "Window cleaning",
        "title": "Commercial Window Cleaning North Idaho | Above & Beyond",
        "description": "Interior and exterior commercial window cleaning across Hayden, Coeur d'Alene, Post Falls, and the surrounding North Idaho corridor.",
        "h1_main": "Window cleaning,",
        "h1_accent": "storefront to mid-rise.",
        "lede": "Interior and exterior commercial glass. Storefronts, lobbies, mid-rise. Squeegee or water-fed pole — whatever the building actually needs.",
        "included": [
            "Interior window panes (all reachable surfaces)",
            "Exterior storefront and lobby glass",
            "Mid-rise exterior (water-fed pole)",
            "Frames, sills, and tracks wiped",
            "Atrium and skylight (where reachable)",
            "Hard-water spot removal on request",
            "Quarterly, monthly, or one-time service",
            "Pre-event detail cleans for showrooms and lobbies",
        ],
        "who_for": "Storefronts, professional offices, banks, healthcare lobbies, churches, mid-rise commercial. Schedules range from monthly (high-touch retail) to quarterly (most offices).",
        "process": "Walk the property to map glass surfaces, set a cadence, schedule first service. We use water-fed pole for upper exterior to keep crews safe and the glass spot-free.",
        "faqs": [
            ("Interior + exterior, or just exterior?", "Whichever scope you want. Most offices do both interior and exterior on the same visit."),
            ("How high can you reach?", "Water-fed pole reaches mid-rise (~4–5 stories). Higher needs a specialty subcontractor — we'll be straight with you about that."),
            ("Hard-water spotting?", "We can mineral-treat on request — adds a step but resolves it."),
            ("Pre-event service for a launch or open house?", "Yes — we'll schedule a detail clean within 24 hours of your event."),
        ],
    },
    {
        "slug": "restroom-sanitation",
        "name": "Restroom sanitation",
        "title": "Commercial Restroom Cleaning North Idaho | Above & Beyond",
        "description": "Touch-point disinfection, fixture detailing, restocking, floor care. Audit-ready commercial restroom sanitation across North Idaho.",
        "h1_main": "Restroom sanitation,",
        "h1_accent": "audit-ready.",
        "lede": "Touch-point disinfection. Fixture detailing. Consumable restocking. Floor work. Audit log every visit so you can prove the work was done.",
        "included": [
            "Touch-point disinfection (handles, switches, dispensers, partitions)",
            "Fixture detailing (sinks, toilets, urinals)",
            "Mirror and chrome polishing",
            "Floor mop or auto-scrub with sanitizing solution",
            "Trash collection and liner replacement",
            "Consumable restocking (paper, soap, sanitizer) — supplied by us or you",
            "Audit log per visit, available to property managers",
            "Day-porter service available for high-traffic facilities",
        ],
        "who_for": "Any building where restroom condition affects the guest or tenant experience — retail, hospitality, healthcare lobbies, multi-tenant office, banks, churches, government. We can scope this standalone or as part of a recurring janitorial contract.",
        "process": "Walk the restrooms, count fixtures, set per-visit checklist, set consumable supply method, start. Audit log is delivered weekly or accessible on-demand.",
        "faqs": [
            ("Do you provide the paper, soap, etc.?", "Either way — we can supply at cost-plus or you can stock yourself and we just refill from your storage."),
            ("How often is needed?", "Daily for high-traffic public restrooms. Several times per week for office buildings. Driven by traffic, not square footage."),
            ("Audit log?", "Yes — we keep a written log per visit. Property managers can request it weekly or anytime."),
            ("Day-porter for events?", "Yes. Hourly day-porter rates available for events, high-traffic days, or post-construction cleanup."),
        ],
    },
]


CITIES = [
    {
        "slug": "hayden",
        "name": "Hayden",
        "title": "Commercial Cleaning Hayden, ID | Above & Beyond Janitorial",
        "description": "Hayden's locally-owned commercial janitorial service since 1997. Same crew every visit, licensed and insured. Free walkthrough + 48-hour quote.",
        "h1_main": "Commercial cleaning in Hayden,",
        "h1_accent": "where we're headquartered.",
        "lede": "Above & Beyond has been Hayden-based since the company started in 1997. Most Hayden routes run nightly.",
        "distance": "0 miles — HQ",
        "status": "Daily routes",
        "local": "Hayden is where Todd founded Above & Beyond in 1997, and it's still where the company is based. Most of our Hayden routes run nightly because we're right here — there's no drive time to absorb into your quote. From Government Way to the lake side of Highway 95, we already drive past most commercial buildings in town every working day.",
        "services_blurb": "Office buildings, dental and medical practices, retail along Highway 95, churches, and city buildings — we run scoped commercial cleaning across all of Hayden. If your building is between Hayden and Hayden Lake, or up toward Honeysuckle, we cover that corridor too.",
    },
    {
        "slug": "coeur-dalene",
        "name": "Coeur d'Alene",
        "title": "Commercial Cleaning Coeur d'Alene, ID | Above & Beyond",
        "description": "Coeur d'Alene commercial cleaning. Same crew every visit, licensed, bonded, insured. Free walkthrough + written 48-hour quote.",
        "h1_main": "Commercial cleaning in Coeur d'Alene,",
        "h1_accent": "daily routes.",
        "lede": "From downtown CDA to the Riverstone and Ramsey corridors, we run daily commercial routes through Coeur d'Alene.",
        "distance": "~8 miles south of HQ",
        "status": "Daily routes",
        "local": "Coeur d'Alene is the largest stop on our daily routes — downtown professional offices, the Riverstone and Ramsey-area commercial buildings, financial institutions along Sherman, and the medical corridor near Ironwood. After-hours commercial work fits naturally around CDA's day-traffic patterns.",
        "services_blurb": "We cover downtown CDA office buildings, the lakeside hospitality belt, banking and financial offices, medical practices in the Ironwood / Kootenai Health area, retail along Government Way, and the church/nonprofit cluster across the city. Recurring contracts get same-crew assignment.",
    },
    {
        "slug": "post-falls",
        "name": "Post Falls",
        "title": "Commercial Cleaning Post Falls, ID | Above & Beyond",
        "description": "Post Falls commercial janitorial services. Daily routes, same crew, licensed and insured. Free walkthrough, 48-hour written quote.",
        "h1_main": "Commercial cleaning in Post Falls,",
        "h1_accent": "daily routes.",
        "lede": "Post Falls is on our daily route — from the Riverbend industrial corridor to the Mullan / 5th Ave commercial belt, we already drive past most buildings every working day.",
        "distance": "~14 miles west of HQ",
        "status": "Daily routes",
        "local": "Post Falls sits between Hayden and Spokane on the I-90 corridor, which means it lines up naturally with our daily routes both directions. We work the Riverbend industrial buildings, the Mullan Ave commercial belt, the Beck Rd and Pleasant View corridor, and the cluster of medical and dental offices along 5th Avenue. The Post Falls Chamber of Commerce listed us as a member for the same reason we still operate here — most of our work comes from referrals inside this town.",
        "services_blurb": "Daily janitorial for Post Falls offices, manufacturing front-offices, medical buildings, churches, and retail. Quarterly carpet extraction and hard-floor programs available on the same contracts.",
    },
    {
        "slug": "rathdrum",
        "name": "Rathdrum",
        "title": "Commercial Cleaning Rathdrum, ID | Above & Beyond",
        "description": "Rathdrum commercial cleaning, weekly routes. Same crew, licensed and insured. Free walkthrough + 48-hour quote.",
        "h1_main": "Commercial cleaning in Rathdrum,",
        "h1_accent": "weekly routes.",
        "lede": "Rathdrum is on our weekly run — for a town growing this fast, that cadence handles most professional offices. Higher frequency available where needed.",
        "distance": "~10 miles north of HQ",
        "status": "Weekly routes",
        "local": "Rathdrum has grown rapidly along the Highway 53 / 41 corridor, with new professional offices, medical practices, and retail filling in north of Hayden. Most of our Rathdrum work sits along Highway 41 and the downtown commercial blocks. The drive from our Hayden HQ is short — when a building needs higher cadence than weekly we can flex up without route penalty.",
        "services_blurb": "Weekly recurring janitorial is the default for Rathdrum buildings. Quarterly carpet, floor care, and windows on the same schedule. Daily cadence on request for offices that need it.",
    },
    {
        "slug": "sandpoint",
        "name": "Sandpoint",
        "title": "Commercial Cleaning Sandpoint, ID | Above & Beyond",
        "description": "Sandpoint commercial janitorial. Weekly Bonner County routes, same crew, licensed and insured. Free walkthrough + written quote.",
        "h1_main": "Commercial cleaning in Sandpoint,",
        "h1_accent": "weekly Bonner County route.",
        "lede": "We've run a weekly Sandpoint route up Highway 95 for years — most professional offices and medical practices here run on a 1× or 2× weekly cadence.",
        "distance": "~50 miles north of HQ",
        "status": "Weekly routes",
        "local": "Sandpoint sits on the north end of our service area — Highway 95 up through Athol, Cocolalla, and Sagle into town. We do weekly commercial cleaning for offices around First and Cedar, professional practices along Schweitzer Cutoff, and medical buildings near Bonner General. For buildings that need higher cadence than weekly we can run a second visit, though most Sandpoint accounts find weekly sufficient.",
        "services_blurb": "Weekly janitorial is the standard Sandpoint cadence. Hard-floor programs, carpet extraction, and window cleaning bundle naturally on the same route days. We're happy to scope a one-time clean for events, opens, or building turnovers.",
    },
    {
        "slug": "spirit-lake",
        "name": "Spirit Lake",
        "title": "Commercial Cleaning Spirit Lake, ID | Above & Beyond",
        "description": "Spirit Lake commercial cleaning, weekly route. Same crew, licensed and insured. Free walkthrough + 48-hour written quote.",
        "h1_main": "Commercial cleaning in Spirit Lake,",
        "h1_accent": "weekly route.",
        "lede": "Spirit Lake sits on our weekly Highway 41 run between Rathdrum and Athol. Most professional offices and storefronts here are scoped weekly.",
        "distance": "~18 miles north of HQ",
        "status": "Weekly routes",
        "local": "Spirit Lake is a smaller commercial footprint than CDA or Post Falls, which fits our Highway 41 weekly route alongside Rathdrum and Athol. We handle professional offices, churches, small storefronts, and the occasional medical or dental practice in town. Drive time is built into the standing weekly schedule — your quote doesn't get penalized for the distance.",
        "services_blurb": "Weekly commercial janitorial. Floor care and carpet extraction available on quarterly programs, scheduled into the same weekly visit.",
    },
    {
        "slug": "athol",
        "name": "Athol",
        "title": "Commercial Cleaning Athol, ID | Above & Beyond",
        "description": "Athol commercial cleaning, weekly route through Highway 95 corridor. Same crew, licensed and insured. Free walkthrough + written quote.",
        "h1_main": "Commercial cleaning in Athol,",
        "h1_accent": "weekly route.",
        "lede": "Athol is on our weekly Highway 95 run heading toward Sandpoint — small but covered, with the same crew every visit.",
        "distance": "~22 miles north of HQ",
        "status": "Weekly routes",
        "local": "Athol sits on the Highway 95 corridor between Hayden Lake and Sandpoint, which puts it directly on our standing weekly run. We handle small commercial offices, faith-based facilities, and the few retail and professional buildings in town. Smaller footprint than the south corridor — but no different on standard and no different on follow-through.",
        "services_blurb": "Weekly recurring janitorial is the default cadence. Quarterly floor and carpet programs run on the same route days. Special-event cleans available — let us know what you need.",
    },
]


def build_services_overview():
    body = f"""<section class="lightpage">
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="eyebrow brass">/ all services</div>
        <h2 class="section-h">Six services. <span class="muted">One scope per facility.</span></h2>
      </div>
      <div class="section-sub right">Every service has its own scope template, supplies, and quality checklist. Mix and match into the schedule your building actually needs.</div>
    </div>
    <div class="services-grid">
      <article class="svc"><div class="svc-head"><div class="svc-num">01 / Recurring</div></div><h3><a href="/services/commercial-janitorial.html" style="color:inherit;text-decoration:none;">Commercial janitorial</a></h3><p>Trash, dust, vacuum, surfaces, restrooms, kitchen — on a written nightly-to-weekly checklist.</p><div class="svc-tags"><span class="svc-tag">5+ x/wk</span><span class="svc-tag">Checklist</span><span class="svc-tag">Monthly invoicing</span></div></article>
      <article class="svc"><div class="svc-head"><div class="svc-num">02 / Specialized</div></div><h3><a href="/services/medical-dental.html" style="color:inherit;text-decoration:none;">Medical &amp; dental</a></h3><p>Color-coded microfiber, hospital-grade disinfectants, terminal cleans. OSHA-aligned.</p><div class="svc-tags"><span class="svc-tag">OSHA</span><span class="svc-tag">EPA-N list</span><span class="svc-tag">Terminal cleans</span></div></article>
      <article class="svc"><div class="svc-head"><div class="svc-num">03 / Periodic</div></div><h3><a href="/services/carpet-extraction.html" style="color:inherit;text-decoration:none;">Carpet extraction</a></h3><p>Truck-mount hot-water extraction. Quarterly programs, spot treatment with recurring.</p><div class="svc-tags"><span class="svc-tag">Truck-mount</span><span class="svc-tag">Quarterly</span><span class="svc-tag">Spot included</span></div></article>
      <article class="svc"><div class="svc-head"><div class="svc-num">04 / Periodic</div></div><h3><a href="/services/hard-floor-care.html" style="color:inherit;text-decoration:none;">Hard-floor care</a></h3><p>Strip and wax, burnishing, buffing, grout deep-cleans. VCT, LVT, concrete, terrazzo, hardwood.</p><div class="svc-tags"><span class="svc-tag">Strip &amp; wax</span><span class="svc-tag">Burnish</span><span class="svc-tag">Grout</span></div></article>
      <article class="svc"><div class="svc-head"><div class="svc-num">05 / Periodic</div></div><h3><a href="/services/window-cleaning.html" style="color:inherit;text-decoration:none;">Window cleaning</a></h3><p>Interior + exterior commercial glass. Storefronts, lobbies, mid-rise. Squeegee or water-fed pole.</p><div class="svc-tags"><span class="svc-tag">Interior</span><span class="svc-tag">Exterior</span><span class="svc-tag">Water-fed pole</span></div></article>
      <article class="svc"><div class="svc-head"><div class="svc-num">06 / Recurring</div></div><h3><a href="/services/restroom-sanitation.html" style="color:inherit;text-decoration:none;">Restroom sanitation</a></h3><p>Touch-point disinfection, fixture detailing, restocking, floor work. After-hours, audit-ready.</p><div class="svc-tags"><span class="svc-tag">Touch-point</span><span class="svc-tag">Restock</span><span class="svc-tag">Audit log</span></div></article>
    </div>
  </div>
</section>

{CTA_SECTION}"""
    build_page(
        out_path="/services/index.html",
        title="Commercial Cleaning Services North Idaho | Above & Beyond",
        description="Commercial janitorial, medical/dental, carpet, hard-floor, window, restroom sanitation. Licensed and insured across North Idaho since 1997.",
        canonical_path="/services/",
        active_nav="services",
        breadcrumb_trail=[("Home", "/"), ("Services", None)],
        hero_h1='Six services. <span class="accent">One written scope per facility.</span>',
        hero_lede="Recurring or periodic — built around what your building actually needs, not a packaged plan.",
        body_content=body,
    )


def build_service_detail(s: dict):
    related = [
        (svc["name"].replace("&amp;", "&"), f"/services/{svc['slug']}.html")
        for svc in SERVICES if svc["slug"] != s["slug"]
    ]
    body = service_body(
        included=s["included"],
        who_for=s["who_for"],
        process=s["process"],
        faqs=s["faqs"],
        related_links=related[:5],
    )
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in s["faqs"]
        ],
    }
    svc_schema = service_schema(s["name"].replace("&amp;", "&"), s["lede"], f"/services/{s['slug']}.html")
    build_page(
        out_path=f"/services/{s['slug']}.html",
        title=s["title"],
        description=s["description"],
        canonical_path=f"/services/{s['slug']}.html",
        active_nav="services",
        breadcrumb_trail=[("Home", "/"), ("Services", "/services/"), (s["name"].replace("&amp;", "&"), None)],
        hero_h1=f'{s["h1_main"]} <span class="accent">{s["h1_accent"]}</span>',
        hero_lede=s["lede"],
        body_content=body,
        extra_schemas=[svc_schema, faq_schema],
    )


def build_service_area_overview():
    rows = "\n      ".join(
        f'<div class="area-row"><span class="area-num">{i:02d}</span><span class="area-city"><a href="/service-area/{c["slug"]}.html" style="color:inherit;">{c["name"]}, ID</a></span><span class="area-status {"hq" if c["slug"]=="hayden" else ""}">{c["status"] if c["slug"]!="hayden" else "Headquarters"}</span></div>'
        for i, c in enumerate(CITIES, 1)
    )
    body = f"""<section class="lightpage">
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="eyebrow brass">/ service area</div>
        <h2 class="section-h">North Idaho, <span class="muted">end to end.</span></h2>
      </div>
      <div class="section-sub right">Hayden-based, with regular routes throughout Kootenai and Bonner counties. If you're between two of these cities, we probably already drive past you.</div>
    </div>
    <div class="areas-grid">
      <div class="areas-table">
      {rows}
      </div>
      <div class="map-wrap">
        <iframe loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen title="Service area map centered on Hayden, Idaho"
          src="https://www.google.com/maps?q=Hayden,+Idaho&amp;t=&amp;z=9&amp;ie=UTF8&amp;iwloc=&amp;output=embed"></iframe>
        <div class="map-overlay">
          <div class="av"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg></div>
          <div>
            <div class="t">Above &amp; Beyond Janitorial</div>
            <div class="s">Hayden, ID · HQ</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

{CTA_SECTION}"""
    build_page(
        out_path="/service-area/index.html",
        title="Service Area — North Idaho Commercial Cleaning | Above & Beyond",
        description="Above & Beyond Janitorial serves Hayden, Coeur d'Alene, Post Falls, Rathdrum, Sandpoint, Spirit Lake, and Athol — the North Idaho corridor.",
        canonical_path="/service-area/",
        active_nav="areas",
        breadcrumb_trail=[("Home", "/"), ("Service area", None)],
        hero_h1='North Idaho, <span class="accent">end to end.</span>',
        hero_lede="Hayden HQ. Daily routes through Coeur d'Alene and Post Falls. Weekly runs up Highway 95 through Athol to Sandpoint.",
        body_content=body,
    )


def build_city(c: dict):
    body = city_body(
        city=c["name"],
        distance=c["distance"],
        services_blurb=c["services_blurb"],
        local_paragraph=c["local"],
        status=c["status"],
    )
    # Per-city LocalBusiness with areaServed scoped to this city
    city_business = localbusiness_schema(area_served=[c["name"]])
    build_page(
        out_path=f"/service-area/{c['slug']}.html",
        title=c["title"],
        description=c["description"],
        canonical_path=f"/service-area/{c['slug']}.html",
        active_nav="areas",
        breadcrumb_trail=[("Home", "/"), ("Service area", "/service-area/"), (c["name"], None)],
        hero_h1=f'{c["h1_main"]} <span class="accent">{c["h1_accent"]}</span>',
        hero_lede=c["lede"],
        body_content=body,
        extra_schemas=[city_business],
    )


def build_about():
    body = """<section class="lightpage">
  <div class="wrap">
    <div style="display:grid;grid-template-columns:1fr 1.4fr;gap:64px;align-items:start;" class="svc-grid">
      <div class="about-photo" aria-label="Photo of Todd D. Johnson — placeholder until real photo provided" style="aspect-ratio: 4/4.6; border-radius:12px; background: linear-gradient(180deg, rgba(10,37,64,0.15), rgba(10,37,64,0.45)), url('https://images.unsplash.com/photo-1521791136064-7986c2920216?w=900&q=80') center/cover; border: 1px solid var(--line); min-height: 420px;"></div>
      <div class="prose">
        <div class="eyebrow brass">/ about</div>
        <h2>Built in North Idaho, run by hand, since 1997.</h2>
        <p>Above &amp; Beyond Janitorial was founded by Todd D. Johnson in 1997 in Hayden, Idaho with a simple idea: treat every facility like a flagship. Nearly three decades later, that's still how the schedules are built, how the crews are trained, and how the work gets graded.</p>
        <p>We stay deliberately local. Hayden-based, North Idaho-focused, owner-involved on every account. That's why our clients tend to stay for years, not quarters.</p>
        <blockquote>"Experience the image." — it's been on the business card from day one.</blockquote>
        <h3>The crew</h3>
        <p>We hire for tenure, not turnover. The average crew member has been on the team 3.5 years, which means they learn your building — every door, every quirk, every preference. Every member is background-checked before they ever set foot on a client's property.</p>
        <h3>The promise</h3>
        <p>Same crew every visit. Written scope you can audit. Re-clean inside 24 hours if anything misses. Owner-direct phone on every invoice. The work has to earn the next month's contract.</p>
      </div>
    </div>
  </div>
</section>

{CTA_SECTION}""".format(CTA_SECTION=CTA_SECTION)
    person = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Todd D. Johnson",
        "jobTitle": "Founder & Owner",
        "worksFor": {"@id": f"{DOMAIN}/#business"},
    }
    build_page(
        out_path="/about.html",
        title="About — Todd D. Johnson, Founder | Above & Beyond Janitorial",
        description="Above & Beyond Janitorial was founded by Todd D. Johnson in Hayden, Idaho in 1997. Family-owned, locally-run commercial cleaning since.",
        canonical_path="/about.html",
        active_nav="about",
        breadcrumb_trail=[("Home", "/"), ("About", None)],
        hero_h1='Founded 1997. <span class="accent">Still owner-operated.</span>',
        hero_lede="Todd D. Johnson started Above & Beyond in Hayden, Idaho in 1997. Nearly three decades of accounts, almost all from referrals.",
        body_content=body,
        extra_schemas=[person],
    )


def build_contact():
    body = """<section class="lightpage">
  <div class="wrap">
    <div style="display:grid;grid-template-columns:1.2fr 1fr;gap:64px;align-items:start;" class="svc-grid">
      <div class="prose">
        <div class="eyebrow brass">/ direct line</div>
        <h2>Reach Todd directly.</h2>
        <p>Quotes are written by Todd, not by a service desk. Phone first if it's urgent — the same number is on every invoice for the life of the account.</p>
        <h3>Phone</h3>
        <p><a href="tel:+12088183175" style="font-family: var(--mono); font-size: 22px; color: var(--ink); text-decoration: none;">(208) 818-3175</a></p>
        <h3>Email</h3>
        <p><a href="mailto:todd@aboveandbeyondjanitorialservice.com">todd@aboveandbeyondjanitorialservice.com</a></p>
        <h3>Service area</h3>
        <p>Hayden · Coeur d'Alene · Post Falls · Rathdrum · Sandpoint · Spirit Lake · Athol</p>
        <h3>Hours</h3>
        <p>Evenings &amp; weekends (commercial after-hours). Walkthrough scheduling: weekdays.</p>
        <h3>Address</h3>
        <p>Hayden, Idaho<br><span style="font-family:var(--mono);font-size:12.5px;color:var(--ink-3);">Service-area business — no public storefront.</span></p>
      </div>
      <aside style="background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:28px;position:sticky;top:24px;">
        <div class="eyebrow brass" style="margin-bottom:14px;">/ written quote</div>
        <p style="font-size:14.5px;color:var(--ink-2);margin:0 0 18px;line-height:1.55;">Tell us your facility type, size, and frequency. We'll come walk it, write a fixed-price scope, and send it back inside 48 hours.</p>
        <button type="button" class="btn btn-primary btn-lg" onclick="openQuote()" style="width:100%;justify-content:center;margin-bottom:8px;">Get my facility quoted</button>
        <a href="tel:+12088183175" class="btn btn-outline-dark btn-lg" style="width:100%;justify-content:center;">Call (208) 818-3175</a>
      </aside>
    </div>

    <div style="margin-top:64px;">
      <div class="map-wrap" style="aspect-ratio:5/2;">
        <iframe loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen title="Map of Hayden, Idaho service area"
          src="https://www.google.com/maps?q=Hayden,+Idaho&amp;t=&amp;z=10&amp;ie=UTF8&amp;iwloc=&amp;output=embed"></iframe>
      </div>
    </div>
  </div>
</section>

{CTA}""".replace("{CTA}", CTA_SECTION)
    build_page(
        out_path="/contact.html",
        title="Contact — Above & Beyond Janitorial, North Idaho",
        description="Reach Todd at (208) 818-3175 or todd@aboveandbeyondjanitorialservice.com. Walkthrough + written 48-hour quote across North Idaho.",
        canonical_path="/contact.html",
        active_nav="contact",
        breadcrumb_trail=[("Home", "/"), ("Contact", None)],
        hero_h1='Talk to the owner. <span class="accent">Same number, every time.</span>',
        hero_lede="Todd D. Johnson takes the call. The same person who quoted you is the person who hears about problems.",
        body_content=body,
    )


def build_faq():
    faqs = [
        ("What does a quote actually include?", "A walkthrough, a written scope of work, and a fixed monthly price for recurring contracts (or per-project for one-time work). No hidden fees, no auto-renewal traps."),
        ("How fast can you start?", "Most accounts within a week of a signed proposal. Larger facilities or post-construction starts may need 10–14 days to staff properly."),
        ("Are you licensed, bonded, and insured?", "Yes. General liability and workers' compensation. COI sent directly to your office or property manager on request."),
        ("Do you supply chemicals and equipment?", "Yes — vacuums, microfiber, chemicals. Green-certified products by default. We can match any procurement standards your facility requires."),
        ("Is it the same crew every visit?", "Yes. Same team for the life of the contract. Average crew tenure is 3.5 years — they learn your building."),
        ("How are missed items handled?", "Call. Inside 24 hours we re-clean it free — no invoice tricks, no minimum clauses, no service-desk filter."),
        ("Do you serve buildings outside the listed cities?", "Often yes. We're Hayden-based but serve the broader North Idaho corridor — ask and we'll be straight about whether your address makes sense."),
        ("Are crews background-checked?", "Yes. Every member is vetted before they ever set foot on a client's property. Comfortable in secure environments after close — financial offices, clinics, government buildings."),
        ("Can you handle medical or dental offices?", "Yes — OSHA-aligned protocols, EPA-registered hospital-grade disinfectants, color-coded microfiber. Terminal cleans on request."),
        ("Do you do floor stripping and waxing?", "Yes — VCT, LVT, concrete, terrazzo, hardwood. Cycles are scheduled into your contract or scoped as one-time projects."),
        ("Carpet cleaning included with recurring?", "Spot treatment is bundled. Full hot-water extraction is typically a quarterly line item or per-project quote."),
        ("Do you offer day-porter service?", "Yes — hourly day-porter for high-traffic facilities, events, or post-construction cleanup."),
        ("Can we cancel?", "Most contracts are 30-day notice. We'd rather you stay because the work is good, not because the paperwork makes leaving hard."),
        ("How do you invoice?", "Monthly, billed the first of the following month for recurring contracts. Net-30 standard."),
        ("Do you serve government / municipal buildings?", "Yes — prevailing-wage capable, insured, security-log compliant. We've worked across public and private sectors."),
        ("Do you do post-construction cleans?", "Yes — final cleans for remodels, tenant improvements, and new builds. Turnover-ready handoff."),
    ]
    items = "\n        ".join(
        f'<details class="fq"{" open" if i == 0 else ""}>\n          <summary>{q}<span class="plus">+</span></summary>\n          <p>{a}</p>\n        </details>'
        for i, (q, a) in enumerate(faqs)
    )
    body = f"""<section class="lightpage">
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="eyebrow brass">/ faq</div>
        <h2 class="section-h">Questions <span class="muted">we hear.</span></h2>
      </div>
      <div class="section-sub right">If yours isn't here, ask in the quote form or by phone — we read everything.</div>
    </div>
    <div class="faq-grid">
      <div></div>
      <div>
        {items}
      </div>
    </div>
  </div>
</section>

{CTA_SECTION}"""
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }
    build_page(
        out_path="/faq.html",
        title="FAQ — Above & Beyond Janitorial, North Idaho",
        description="Frequently asked questions: quotes, scope, crew, supplies, licensing, scheduling, and how Above & Beyond works.",
        canonical_path="/faq.html",
        active_nav="faq",
        breadcrumb_trail=[("Home", "/"), ("FAQ", None)],
        hero_h1='Questions <span class="accent">we hear most.</span>',
        hero_lede="The honest answers to what most facility managers ask before they hire us.",
        body_content=body,
        extra_schemas=[faq_schema],
    )


def build_privacy():
    body = """<section class="lightpage">
  <div class="wrap">
    <div class="prose" style="max-width:780px;">
      <div class="eyebrow brass">/ privacy</div>
      <h2>Privacy policy</h2>
      <p><em>Effective: 2026-05-15. This is a placeholder pending review — replace with a generated policy via termly.io or iubenda.com before launch.</em></p>
      <h3>What we collect</h3>
      <p>The quote form on this site collects: your name, email, phone, facility type, size, frequency, and any optional notes you provide. This information is sent only to Todd D. Johnson, the owner of Above &amp; Beyond Janitorial, Inc. We do not sell, share, or rent your information.</p>
      <h3>Why we collect it</h3>
      <p>To respond to your quote request, schedule a walkthrough, and provide a written scope. That's it.</p>
      <h3>How we use it</h3>
      <p>The form submission is sent to <a href="mailto:todd@aboveandbeyondjanitorialservice.com">todd@aboveandbeyondjanitorialservice.com</a>. Submission delivery is handled by a third-party form service (Formspree) which retains the message per its own retention policy.</p>
      <h3>Cookies and tracking</h3>
      <p>This site does not run analytics or advertising trackers at this time. Future analytics (Google Analytics 4) will be added with a privacy notice update.</p>
      <h3>Your rights</h3>
      <p>To request deletion of any quote submission, email <a href="mailto:todd@aboveandbeyondjanitorialservice.com">todd@aboveandbeyondjanitorialservice.com</a> from the address you used.</p>
      <h3>Contact</h3>
      <p>Above &amp; Beyond Janitorial, Inc. · Hayden, Idaho · <a href="tel:+12088183175">(208) 818-3175</a></p>
    </div>
  </div>
</section>"""
    build_page(
        out_path="/privacy.html",
        title="Privacy Policy | Above & Beyond Janitorial",
        description="Privacy policy for Above & Beyond Janitorial. What we collect from the quote form, how we use it, your rights.",
        canonical_path="/privacy.html",
        active_nav="",
        breadcrumb_trail=[("Home", "/"), ("Privacy", None)],
        hero_h1='Privacy.',
        hero_lede="What we collect, how we use it, and what you can ask us to delete.",
        hero_ctas=False,
        body_content=body,
    )


def build_404():
    body = """<section class="lightpage" style="text-align:center;">
  <div class="wrap" style="max-width:640px;">
    <div class="prose" style="margin:0 auto;text-align:center;">
      <div class="eyebrow brass" style="text-align:center;">/ 404</div>
      <h2 style="text-align:center;">That page got cleaned right off the schedule.</h2>
      <p>The URL you tried doesn't exist on this site. Try one of the links below — or just call us, that always works.</p>
      <div style="margin-top:36px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap;">
        <a href="/" class="btn btn-primary">Back to home</a>
        <a href="/services/" class="btn btn-outline-dark">See services</a>
        <a href="tel:+12088183175" class="btn btn-outline-dark">Call (208) 818-3175</a>
      </div>
    </div>
  </div>
</section>"""
    build_page(
        out_path="/404.html",
        title="Page not found | Above & Beyond Janitorial",
        description="The page you're looking for doesn't exist. Go back to the home page or call (208) 818-3175.",
        canonical_path="/404.html",
        active_nav="",
        breadcrumb_trail=[("Home", "/"), ("404", None)],
        hero_h1='404.',
        hero_lede="Page not found. Try the home page, services, or call (208) 818-3175.",
        hero_ctas=False,
        body_content=body,
    )


def main():
    print("Building pages →", SITE)
    build_services_overview()
    for s in SERVICES:
        build_service_detail(s)
    build_service_area_overview()
    for c in CITIES:
        build_city(c)
    build_about()
    build_contact()
    build_faq()
    build_privacy()
    build_404()
    print("Done.")


if __name__ == "__main__":
    main()
