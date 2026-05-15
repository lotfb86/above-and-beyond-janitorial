#!/usr/bin/env python3
"""Generate sitemap.xml for the site."""
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DOMAIN = "https://aboveandbeyondjanitorialservice.com"

# (path, priority, changefreq)
URLS = [
    ("/", "1.0", "monthly"),
    ("/services/", "0.9", "monthly"),
    ("/services/commercial-janitorial.html", "0.8", "monthly"),
    ("/services/medical-dental.html", "0.8", "monthly"),
    ("/services/carpet-extraction.html", "0.8", "monthly"),
    ("/services/hard-floor-care.html", "0.8", "monthly"),
    ("/services/window-cleaning.html", "0.8", "monthly"),
    ("/services/restroom-sanitation.html", "0.8", "monthly"),
    ("/service-area/", "0.9", "monthly"),
    ("/service-area/hayden.html", "0.85", "monthly"),
    ("/service-area/coeur-dalene.html", "0.85", "monthly"),
    ("/service-area/post-falls.html", "0.85", "monthly"),
    ("/service-area/rathdrum.html", "0.8", "monthly"),
    ("/service-area/sandpoint.html", "0.8", "monthly"),
    ("/service-area/spirit-lake.html", "0.8", "monthly"),
    ("/service-area/athol.html", "0.8", "monthly"),
    ("/about.html", "0.7", "yearly"),
    ("/contact.html", "0.7", "yearly"),
    ("/faq.html", "0.7", "monthly"),
    ("/privacy.html", "0.3", "yearly"),
]

today = date.today().isoformat()

xml_urls = "\n".join(
    f"  <url>\n    <loc>{DOMAIN}{p}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n  </url>"
    for p, pr, cf in URLS
)
xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{xml_urls}\n</urlset>\n'
(SITE / "sitemap.xml").write_text(xml, encoding="utf-8")
print(f"wrote sitemap.xml — {len(URLS)} URLs, lastmod {today}")
