#!/usr/bin/env python3
"""Builds the Hop To It Events site.

    python3 _src/build.py            # live site: clean URLs like /about/
    python3 _src/build.py --preview  # same pages, links point at index.html files
                                     # (for previewing without a web server)

Every page is written to <slug>/index.html so URLs are short and keyword-focused
(/corporate-event-planning/). Shared header, footer, CTA band and structured data
live here; service copy lives in services.py and city pages in locations.py.
GitHub Pages ignores folders that start with an underscore, so this folder is
never served.

Also writes sitemap.xml, robots.txt, llms.txt and 404.html.
"""
import json
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from services import SERVICES, BY_SLUG, GROUPS, COMMON_WHERE  # noqa: E402
from locations import CITIES as _LA_CITIES  # noqa: E402
from citygen import CITY_PAGES  # noqa: E402

PUBLISH_PHASE = 2   # all LA pages are live
CITIES = _LA_CITIES + CITY_PAGES
for _c in _LA_CITIES:
    _c.setdefault("nearby", ["orange-county", "beverly-hills", "san-diego", "santa-barbara", "palm-springs"])
    _c.setdefault("worked", True)
CITY_BY_SLUG = {c["slug"]: c for c in CITIES}
FOOTER_CITIES = ["los-angeles", "new-york-city", "chicago", "las-vegas", "dallas", "orange-county", "seattle", "atlanta"]
STATE_NAMES = {"AL": "Alabama", "AZ": "Arizona", "CA": "California", "CO": "Colorado", "DC": "District of Columbia",
               "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "IA": "Iowa", "IL": "Illinois", "IN": "Indiana",
               "LA": "Louisiana", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MO": "Missouri",
               "NV": "Nevada", "NY": "New York", "OH": "Ohio", "OR": "Oregon", "PA": "Pennsylvania", "SC": "South Carolina",
               "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "WA": "Washington", "WI": "Wisconsin",
               "NC": "North Carolina", "VA": "Virginia", "KY": "Kentucky", "OK": "Oklahoma", "NM": "New Mexico",
               "NE": "Nebraska", "KS": "Kansas", "MD": "Maryland", "NJ": "New Jersey", "ID": "Idaho", "AK": "Alaska",
               "UT": "Utah", "AR": "Arkansas", "MS": "Mississippi", "WV": "West Virginia", "CT": "Connecticut",
               "RI": "Rhode Island", "DE": "Delaware", "NH": "New Hampshire", "VT": "Vermont", "ME": "Maine",
               "MT": "Montana", "WY": "Wyoming", "ND": "North Dakota"}


def nearby_links(c, suffix=""):
    out = []
    for k in c.get("nearby", []):
        n = CITY_BY_SLUG.get(k)
        if n and n["slug"] != c["slug"]:
            path = f'locations/{k}/' + (suffix + "/" if suffix and any(p["slug"] == suffix for p in n["pages"]) else "")
            out.append((f'{n["city"]}' if not suffix else f'{n["city"]}', path))
    return out[:4]
from photos import SHOTS, LABEL_TO_SHOT, OVERRIDE_ALT, SHOT_CITY, OVERRIDE_CITY, NEARBY, PHOTO_POS  # noqa: E402

MISSING_SHOTS = set()

ROOT = Path(__file__).resolve().parent.parent
PREVIEW = "--preview" in sys.argv
EMAIL = "hello@hoptoit.events"
SITE = "https://hoptoit.events"
UPDATED = "2026-11-19"
ORG_ID = SITE + "/#organization"
TICKETS_DONUT_FEST_LV = "https://donutfestvegas2027.eventbrite.com/"
GCL = "https://globalchefleague.com"

# Google Apps Script web app URL (see _src/google-apps-script.gs and README "Leads").
# Leave empty and forms fall back to opening the visitor's email app.
GTM_ID = "GTM-KLKNGPX8"  # Google Tag Manager container
LEADS_URL = "https://script.google.com/macros/s/AKfycbwmjAIhKdDtkGFeoEN6RQR_A7u6uX6mOk1NcdM7VwKH8TmKuh1J5seDjRJ-FtLqRSQ/exec"
FORM_NOTE = ("Thanks! We got your request and will be in touch soon." if LEADS_URL
             else "Your email app should open with your details filled in. Just hit send.")

# Add a profile URL and it appears in the footer and in structured data (sameAs).
SOCIAL = {"Instagram": "https://www.instagram.com/hoptoitevents/", "Facebook": "https://www.facebook.com/hoptoitevents/", "TikTok": "", "LinkedIn": ""}
SOCIAL_ICONS = {
    "Instagram": '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M12 2.2c3.2 0 3.6 0 4.8.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1.1.4 2.2.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1.1.4-2.2.4-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1.1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1.1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 1.8c-3.1 0-3.5 0-4.7.1-1.1.1-1.7.2-2 .4-.5.2-.9.4-1.3.8-.4.4-.6.8-.8 1.3-.2.4-.3 1-.4 2C2.8 8.5 2.8 8.9 2.8 12s0 3.5.1 4.7c.1 1.1.2 1.7.4 2 .2.5.4.9.8 1.3.4.4.8.6 1.3.8.4.2 1 .3 2 .4 1.2.1 1.6.1 4.7.1s3.5 0 4.7-.1c1.1-.1 1.7-.2 2-.4.5-.2.9-.4 1.3-.8.4-.4.6-.8.8-1.3.2-.4.3-1 .4-2 .1-1.2.1-1.6.1-4.7s0-3.5-.1-4.7c-.1-1.1-.2-1.7-.4-2-.2-.5-.4-.9-.8-1.3-.4-.4-.8-.6-1.3-.8-.4-.2-1-.3-2-.4C15.5 4 15.1 4 12 4zm0 3.1a4.9 4.9 0 110 9.8 4.9 4.9 0 010-9.8zm0 8a3.1 3.1 0 100-6.2 3.1 3.1 0 000 6.2zm5.1-8.2a1.1 1.1 0 110-2.3 1.1 1.1 0 010 2.3z"/></svg>',
    "Facebook": '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M22 12a10 10 0 10-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.3v7A10 10 0 0022 12z"/></svg>',
}

# Real photography: see _src/photos.py for the shot list and file names.

PRESS = ["Los Angeles Times", "Chicago Tribune", "KPBS", "Las Vegas Review-Journal",
         "Cincinnati Refined", "Patch", "Food + Travel", "Salt Lake City Weekly",
         "KWQC", "San Diego Reader", "KTNV Las Vegas", "West Hawaii Today",
         "RedEye", "Dispatch-Argus"]
BRANDS = ["Dunkin'", "Walmart", "STK Steakhouse", "Fogo de Chão", "Diageo", "Coors Light", "Red Bull", "T-Mobile", "AT&T", "Miller Lite",
          "Ketel One", "Captain Morgan", "Johnnie Walker", "Tanqueray",
          "Performance Foodservice", "Breakthru Beverage", "Cabot", "SkinnyPop",
          "barkTHINS", "Boxed Water", "Smart & Final", "Kona Brewing"]
MARKETS = ["Atlanta", "Austin", "Bakersfield", "Bay Area", "Birmingham", "Boston",
           "Cedar Rapids", "Charleston", "Chicago", "Dallas", "Denver", "Des Moines",
           "Detroit", "Grand Rapids", "Hawaii", "Indianapolis", "Kansas City",
           "Las Vegas", "Los Angeles", "Madison", "Minneapolis", "Nashville",
           "New Orleans", "Orange County", "Phoenix", "Portland", "Quad Cities",
           "St. Louis", "San Diego", "Sioux Falls", "Spokane", "Washington, D.C."]
EVENT_BRANDS = ["Donut Fest", "Chef Battle", "Bartender Battle", "Wine Bash", "Wing Fest",
                "Say Cheese Fest", "Sweets + Snacks Fest", "Cheers + Drink Fest",
                "Donut & Dessert Fest", "Treat Me Fest", "Drink Local", "After Work Social",
                "Cocktail Shake Off", "Pizza Party", "Donut 5K"]

SERVICES_LIST = [
    ("Event strategy & concept", "Creative concepts, themes, programming, budgets and timelines"),
    ("Venue sourcing", "Venue research, selection and coordination"),
    ("Vendor management", "Food trucks, caterers, rentals and suppliers"),
    ("Event production", "Layouts, staging, AV, logistics and permitting"),
    ("Talent & entertainment", "Chefs, hosts, DJs, performers and programming"),
    ("Photography & video", "Event photographers, videographers, recap reels and social content"),
    ("Rentals & decor", "Tents, furniture, staging, lighting, decor and signage"),
    ("Marketing & promotion", "Branding, websites, ticketing and advertising"),
    ("Sponsorship development", "Packages, prospecting and on-site activation"),
    ("On-site management", "Staffing, registration and vendor coordination"),
]

ORG_DESC = ("Hop To It Events is a full-service event planning and production company "
            "that has been planning and producing events since 2010. It plans corporate events, brand activations, team building, festivals, "
            "fundraisers, food truck catering and private parties, and creates its own "
            "signature food and drink festivals in 30+ U.S. markets.")

INDEXED = []   # paths that go in the sitemap

# ------------------------------------------------------------------ linking
_depth = 0
_absolute = False
_city = None   # city slug while building a city page
_used = set()  # photo files already shown on the page being built


def link(target=""):
    """Relative link to a site path like 'about/', 'plan-your-event/?type=x', 'events/#faq'."""
    if target.startswith(("http", "mailto:", "#")):
        return target
    path, sep, rest = target.partition("?")
    if not sep:
        path, sep, rest = target.partition("#")
    tail = (sep + rest) if sep else ""
    if PREVIEW and (path == "" or path.endswith("/")):
        path += "index.html"
    if _absolute:
        return "/" + path + tail
    out = "../" * _depth + path
    return (out or "./") + tail


def plan(event_type=None):
    return link("plan-your-event/" + (("?type=" + quote(event_type)) if event_type else ""))


def mailto(subject):
    return f"mailto:{EMAIL}?subject={quote(subject)}"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def pinkify(h):
    """'Company Events People *Talk About.*' -> pink span on the starred words."""
    parts = esc(h).split("*")
    return "".join(f'<span class="pink">{p}</span>' if i % 2 else p for i, p in enumerate(parts))


def slug_of(label):
    out = "".join(c if c.isalnum() else "-" for c in label.lower()).strip("-")
    while "--" in out:
        out = out.replace("--", "-")
    return out


def target_info(key):
    """Service slug, page key or site path -> (label, path)."""
    if key in BY_SLUG:
        return BY_SLUG[key]["name"], key + "/"
    return {"events": ("Our Signature Events", "events/"),
            "services": ("All Services", "services/")}[key]


def set_depth(slug):
    global _depth
    _depth = slug.count("/")
    _used.clear()


# ------------------------------------------------------------------ chrome
NAV = [("food-truck-catering/", "Food Truck Catering", "food-truck-catering"),
       ("corporate-team-building/", "Corporate Experiences", "corporate-team-building"),
       ("events/", "Our Events", "events"),
       ("about/", "About Us", "about")]


def header(active):
    cols = ""
    css = ["c1", "c2", "c3", "c5", "c4"]
    for (title, slugs), cls in zip(GROUPS, css):
        lis = "".join(f'<li><a href="{link(s + "/")}">{esc(BY_SLUG[s]["name"])}</a></li>' for s in slugs)
        cols += f'<div><h5 class="{cls}">{title}</h5><ul>{lis}</ul></div>'
    planning_keys = (set(BY_SLUG) | {"services", "locations"}) - {"food-truck-catering", "corporate-team-building"}
    planning_active = ' class="active"' if active in planning_keys else ""
    links = ""
    for href, label, key in NAV:
        cur = ' aria-current="page"' if key == active else ""
        links += f'<li><a href="{link(href)}"{cur}>{label}</a></li>'
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <nav class="wrap nav" aria-label="Main">
    <a class="logo" href="{link()}" aria-label="Hop To It Events home"><b>hop to it</b><small>events</small></a>
    <button class="menu-toggle" aria-label="Menu" aria-expanded="false" aria-controls="nav-links"><span></span><span></span><span></span></button>
    <ul class="nav-links" id="nav-links">
      <li class="has-mega">
        <button aria-expanded="false" aria-controls="mega"{planning_active}>Event Planning &#9662;</button>
        <div class="mega" id="mega"><div class="mega-inner">{cols}
          <div class="mega-cta"><p>Not sure what kind of event you need?</p><a class="btn btn-gold btn-sm" href="{plan()}">Plan Your Event</a></div>
          <a class="mega-all" href="{link('services/')}">See all event planning services &rarr;</a>
        </div></div>
      </li>
      {links}
      <li><a class="btn btn-pink" href="{plan()}">Plan Your Event</a></li>
    </ul>
  </nav>
</header>"""


def cta_band():
    return f"""<section class="cta-band">
  <div class="wrap">
    <div><h2>Let&rsquo;s Create Something<br><span class="gold">Unforgettable.</span></h2>
    <p>Have an event in mind? Let&rsquo;s make it happen.</p></div>
    <a class="btn btn-gold" href="{plan()}">Plan Your Event</a>
  </div>
</section>"""


def footer():
    social = "".join(f'<a class="social" href="{u}" rel="noopener me" target="_blank" aria-label="Hop To It Events on {n}">{SOCIAL_ICONS.get(n, n)}</a>'
                     for n, u in SOCIAL.items() if u)
    right = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
    plan_links = [("corporate-event-planning", "Corporate Events"), ("brand-activations", "Brand Activations"),
                  ("corporate-team-building", "Team Building"), ("festival-event-planning", "Festivals & Community"),
                  ("fundraiser-event-planning", "Fundraisers"), ("food-truck-catering", "Food Truck Catering")]
    pl = "".join(f'<li><a href="{link(s + "/")}">{esc(n)}</a></li>' for s, n in plan_links)
    cities = "".join(f'<li><a href="{link("locations/" + k + "/")}">{esc(CITY_BY_SLUG[k]["city"])}</a></li>' for k in FOOTER_CITIES if k in CITY_BY_SLUG)
    cities += f'<li><a href="{link("locations/")}">All locations &rarr;</a></li>'
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div><a class="logo" href="{link()}"><b>hop to it</b><small>events</small></a>
        <p>A full-service event planning and production company creating memorable experiences since 2010, in 30+ U.S. markets.</p></div>
      <div><h5>Plan an Event</h5><ul>{pl}<li><a href="{link('services/')}">All Services</a></li>
        <li><a href="{link('tools/event-budget-calculator/')}">Event Budget Calculator</a></li></ul></div>
      <div><h5>Our Events</h5><ul>
        <li><a href="{link('events/')}">Signature Events</a></li>
        <li><a href="{link('events/#coming-up')}">Tickets</a></li>
        <li><a href="{esc(mailto('Sponsorship inquiry'))}">Become a Sponsor</a></li>
        <li><a href="{esc(mailto('Vendor application'))}">Become a Vendor</a></li></ul>
        <h5 style="margin-top:28px">Locations</h5><ul>{cities}</ul></div>
      <div><h5>Company</h5><ul>
        <li><a href="{link('about/')}">About Us</a></li>
        <li><a href="{link('about/#press')}">Press</a></li>
        <li><a href="{plan()}">Contact</a></li>
        <li><a href="{link('privacypolicy.html')}">Privacy Policy</a></li></ul></div>
    </div>
    <div class="foot-bottom"><span>&copy; 2026 Hop To It Events</span><span class="foot-right">{right}<span class="socials">{social}</span></span></div>
  </div>
</footer>"""


# ------------------------------------------------------------------ structured data
def org():
    o = {"@type": "Organization", "@id": ORG_ID, "name": "Hop To It Events",
         "alternateName": "Hop To It", "url": SITE + "/", "email": EMAIL,
         "foundingDate": "2010",
         "description": ORG_DESC,
         "logo": {"@type": "ImageObject", "url": SITE + "/assets/logo.png", "width": 512, "height": 512},
         "image": SITE + "/assets/og-image.png",
         "areaServed": {"@type": "Country", "name": "United States"},
         "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "email": EMAIL,
                          "areaServed": "US", "availableLanguage": "English"},
         "knowsAbout": ["Event planning", "Event production", "Corporate events", "Brand activations",
                        "Experiential marketing", "Team building", "Food festivals",
                        "Food truck catering", "Culinary competitions", "Sponsorship development",
                        "Event photography and videography"],
         "brand": [{"@type": "Brand", "name": b} for b in EVENT_BRANDS]}
    same = [u for u in SOCIAL.values() if u]
    if same:
        o["sameAs"] = same
    return o


def website():
    return {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/",
            "name": "Hop To It Events", "publisher": {"@id": ORG_ID}, "inLanguage": "en-US"}


def webpage(url, title, desc, crumbs, ptype="WebPage"):
    g = [{"@type": ptype, "@id": url + "#webpage", "url": url, "name": title, "description": desc,
          "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": ORG_ID},
          "inLanguage": "en-US", "dateModified": UPDATED}]
    if crumbs:
        g[0]["breadcrumb"] = {"@id": url + "#breadcrumb"}
        g.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + "/" + p}
            for i, (n, p) in enumerate(crumbs)]})
    return g


def faq_ld(url, faqs):
    return {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def service_ld(url, name, stype, desc, cards_title, cards, area):
    return {"@type": "Service", "@id": url + "#service", "name": name, "serviceType": stype,
            "description": desc, "url": url, "provider": {"@id": ORG_ID}, "areaServed": area,
            "hasOfferCatalog": {"@type": "OfferCatalog", "name": cards_title, "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": c[0], "description": c[1]}}
                for c in cards]}}


US = {"@type": "Country", "name": "United States"}


# ------------------------------------------------------------------ page shell
def page(slug, title, desc, active, body, graph, cta=True, out=None, index=True):
    url = SITE + "/" + slug
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    ld = ld.replace("</", "<\\/")
    robots = ("index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
              if index else "noindex, follow")
    canonical = f'<link rel="canonical" href="{url}">\n' if index else ""
    html = f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
{canonical}<meta property="og:type" content="website">
<meta property="og:site_name" content="Hop To It Events">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Hop To It Events: event planning and production">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1F2226">
<link rel="icon" href="{link('assets/favicon.svg')}" type="image/svg+xml">
<link rel="apple-touch-icon" href="{link('assets/apple-touch-icon.png')}">
<link rel="preload" href="{link('assets/fonts/fredoka-latin-600-normal.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{link('assets/fonts/nunito-sans-latin-400-normal.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{link('assets/styles.css')}">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
{header(active)}
<main id="main">
{body}
</main>
{cta_band() if cta else ""}
{footer()}
<script src="{link('assets/main.js')}" defer></script>
</body>
</html>
"""
    dest = ROOT / (out or (slug + "index.html"))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)
    if index and out != "404.html":
        INDEXED.append(slug)
    print("wrote", dest.relative_to(ROOT), "" if index else "(noindex)")


# ------------------------------------------------------------------ components
# City pages may show photos from any market (each photo's alt text names where it was taken).
# Set to True to limit city pages to photos from that city or nearby.
CITY_PHOTOS_ONLY = False


def city_ok(tag):
    """True if a photo tagged with this city may show on the page being built."""
    if not CITY_PHOTOS_ONLY:
        return True
    return not _city or tag is None or tag == _city or tag in NEARBY.get(_city, ())


def photo_for(label):
    """-> (src, alt) if a photo exists for this placeholder, else None."""
    own = slug_of(label)
    if own not in SHOTS and (ROOT / "assets/photos" / (own + ".jpg")).exists()  and city_ok(OVERRIDE_CITY.get(label)):
        alt = OVERRIDE_ALT.get(label) or SHOTS.get(LABEL_TO_SHOT.get(label, ""), (0, label))[1]
        return link("assets/photos/" + own + ".jpg"), alt
    key = LABEL_TO_SHOT.get(label)
    if key is None:
        MISSING_SHOTS.add(label)
        return None
    if not city_ok(SHOT_CITY.get(key)):
        return None
    if (ROOT / "assets/photos" / (key + ".jpg")).exists():
        return link("assets/photos/" + key + ".jpg"), SHOTS[key][1]
    return None


def ph(label, tone="", style="", inner="", eager=False):
    st = f' style="{style}"' if style else ""
    found = photo_for(label)
    if found and found[0] in _used:
        found = None   # never repeat a photo on the same page
    pos = f' style="object-position:{PHOTO_POS[label]}"' if label in PHOTO_POS else ""
    if found:
        _used.add(found[0])
        return (f'<div class="ph {tone}"{st}><img src="{found[0]}" alt="{esc(found[1])}"{pos} '
                + ('fetchpriority="high">' if eager else 'loading="lazy" decoding="async">') + f'{inner}</div>')
    return f'<div class="ph {tone}"{st} aria-hidden="true">{inner}<span class="ph-label">Photo &middot; {esc(label)}</span></div>'


def services_block(title, intro):
    items = "".join(f'<div class="svc"><h3>{t}</h3><p>{d}</p></div>' for t, d in SERVICES_LIST)
    return f"""<section class="dark" id="whats-included"><div class="wrap services">
  <div><h2>{title}</h2><p class="lede">{intro}</p></div>
  <div class="svc-list">{items}</div>
</div></section>"""


def marquee(label, items, style="cream", anchor=""):
    track = "".join(f"<span>{esc(i)}</span><span><i>&#10035;</i></span>" for i in items)
    aid = f' id="{anchor}"' if anchor else ""
    return f"""<div class="wrap marquee-row"{aid} style="margin-bottom:28px">
  <h2 class="eyebrow muted" style="margin:0;white-space:nowrap;font-weight:400">{label}</h2>
  <div class="marquee {style}"><p class="sr-only">{esc(', '.join(items))}</p><div class="marquee-track" aria-hidden="true">{track}{track}</div></div>
</div>"""


def faq_section(faqs, title="Frequently Asked Questions"):
    items = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs)
    return f"""<section id="faq"><div class="wrap">
  <span class="eyebrow">FAQ</span>
  <h2 class="h2" style="margin-bottom:32px">{title}</h2>
  <div class="faq">{items}</div>
</div></section>"""


def related_section(items, title="Related Services"):
    """items: list of (label, path)."""
    links = "".join(f'<a href="{link(p)}">{esc(n)}</a>' for n, p in items)
    return f"""<section style="padding-top:24px"><div class="wrap">
  <h2 class="eyebrow muted" style="font-weight:400">{title}</h2>
  <div class="related">{links}</div>
</div></section>"""


def crumbs_html(crumbs):
    lis = ""
    for i, (n, p) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            lis += f'<li><span aria-current="page">{esc(n)}</span></li>'
        else:
            lis += f'<li><a href="{link(p)}">{esc(n)}</a></li>'
    return f'<ol class="crumbs" aria-label="Breadcrumb">{lis}</ol>'


TONES = ["pink", "gold", "teal", "cream", "gold", "pink"]


def card_grid(cards, resolve):
    """cards: (title, desc[, key]); resolve(key) -> path."""
    out = ""
    for i, c in enumerate(cards):
        inner = f'{ph(c[0], TONES[i % len(TONES)])}<div class="card-body"><h3>{esc(c[0])}</h3><p>{esc(c[1])}</p></div>'
        if len(c) > 2:
            out += f'<a class="card card-link reveal" href="{link(resolve(c[2]))}">{inner}</a>'
        else:
            out += f'<article class="card reveal">{inner}</article>'
    cls = "grid-4" if len(cards) == 4 else "grid-3"
    return f'<div class="{cls}">{out}</div>'


def truck_cards(cards=None, resolve=lambda k: target_info(k)[1], meta=None):
    cards = cards or BY_SLUG["food-truck-catering"]["cards"]
    meta = meta or [("Events", "gold", "Food truck rally at dusk"),
                    ("Social", "teal", "Donut trailer at a brewery event")]
    out = ""
    for (badge, tone, label), c in zip(meta, cards):
        title, desc = c[0], c[1]
        head = f'<a href="{link(resolve(c[2]))}">{esc(title)}</a>' if len(c) > 2 else esc(title)
        out += (f'<article class="book-card reveal">{ph(label, tone, inner=f"<span class=\'badge {tone}\'>{badge}</span>")}'
                f'<h3>{head}</h3><p>{esc(desc)}</p></article>')
    cls = "grid-2" if len(meta) == 2 else "grid-3"
    return f'<div class="{cls}">{out}</div>'


def festival_formats():
    fmts = [("&#127849;", "Donut Fest", "Employee appreciation days", "employee-appreciation-events"),
            ("&#128298;", "Chef Battle", "Team-building cook-offs", "corporate-team-building"),
            ("&#127864;", "Bartender Battle", "Client and holiday parties", "bar-beverage-services"),
            ("&#127750;", "After Work Social", "Networking and mixers", "corporate-event-planning")]
    tiles = "".join(f'<a class="fmt reveal" href="{link(h + "/")}"><div class="emo" aria-hidden="true">{e}</div><h3>{n}</h3><p>{d}</p></a>'
                    for e, n, d, h in fmts)
    return f"""<section class="bg-pink" id="signature-experiences"><div class="wrap">
  <div class="sec-head">
    <div><span class="eyebrow">Signature experiences, customized for your team</span><h2>Bring the Festival Experience to Your Next Company Event</h2></div>
    <p class="lede">Why settle for another ordinary company event? Bring the excitement of our signature festivals to your holiday party, conference, client night or company celebration. From live Chef Battle competitions to Donut Fest experiences and Bartender Battle challenges, we create interactive events that go beyond traditional corporate gatherings.</p>
  </div>
  <div class="grid-4">{tiles}</div>
</div></section>"""


CHIPS = [("Tacos", "k"), ("BBQ", "p"), ("Pizza", ""), ("Burgers", "g"), ("Wings", "t"), ("Donuts", "k"),
         ("Ice Cream", "p"), ("Coffee", ""), ("Mediterranean", "g"), ("Asian Fusion", "t"), ("Vegan", "k"),
         ("Mini Pancakes", "p"), ("Grilled Cheese", ""), ("Lobster Rolls", "g")]


def chips_html():
    return '<ul class="chips" style="list-style:none">' + "".join(f'<li class="chip {c}">{n}</li>' for n, c in CHIPS) + "</ul>"


def truck_menu_steps():
    return f"""<section class="bg-pink" id="how-it-works"><div class="wrap">
  <h2 class="h2" style="margin-bottom:40px">How It Works</h2>
  <ol class="steps" style="list-style:none">
    <li class="step reveal"><span class="eyebrow">Step 1</span><h3>Tell Us About Your Event</h3><p>Date, location, guest count and food preferences.</p></li>
    <li class="step reveal"><span class="eyebrow">Step 2</span><h3>We Coordinate the Trucks</h3><p>Vendors, availability and logistics.</p></li>
    <li class="step reveal"><span class="eyebrow">Step 3</span><h3>Enjoy the Experience</h3><p>Guests enjoy great food while we help manage the details.</p></li>
  </ol>
</div></section>
<section><div class="wrap menu-split">
  <div><span class="eyebrow">On the menu</span><h2 class="h2">Something for Every Crowd</h2>
    <p class="lede" style="margin-top:16px">Tacos, BBQ, burgers, pizza, wings, ice cream, coffee, desserts and more. We help match the food experience to your audience, event style and budget.</p></div>
  {chips_html()}
</div></section>"""


def chef_battle_feature(team_path):
    return f"""<section class="dark"><div class="wrap tab-panel" style="grid-template-columns:1fr 1fr">
  <div><span class="eyebrow">Team-building feature</span>
    <h2 class="h2" style="margin-bottom:18px">Chef Battle, Built for Your Team</h2>
    <p class="lede" style="margin-bottom:24px">Chef Battle is the live culinary competition we produce in 20+ cities. For companies, we scale it into a team cook-off: groups collaborate, create dishes and compete for bragging rights while everyone else cheers them on.</p>
    <a class="btn btn-pink" href="{link(team_path)}">Explore Team Building</a></div>
  {ph("Chef Battle live round", "", "min-height:320px")}
</div></section>"""


def audiences():
    return """<section style="padding-top:24px"><div class="wrap aud">
  <h2 class="h2">Who We<br>Work With</h2>
  <div class="aud-grid">
    <div class="aud-item"><h3>Corporate HR, marketing &amp; event teams</h3><p>Employee events, customer appreciation, product launches and team building.</p></div>
    <div class="aud-item"><h3>Cities, chambers &amp; tourism organizations</h3><p>Downtown festivals, food events, community celebrations and destination experiences.</p></div>
    <div class="aud-item"><h3>Shopping centers, developers &amp; property managers</h3><p>Grand openings, tenant appreciation, seasonal events and foot-traffic-driving activations.</p></div>
    <div class="aud-item"><h3>Agencies &amp; brands</h3><p>White-label production, experiential campaigns, sampling programs and event execution.</p></div>
  </div>
</div></section>"""


def _opt(vals):
    return "".join(f"<option>{v}</option>" for v in vals)


def truck_form(location=""):
    loc_val = f' value="{esc(location)}"' if location else ""
    return f"""<form class="form-card" data-mailto="{EMAIL}" data-subject="Food truck quote request" data-leads="{LEADS_URL}" data-form="Food truck quote" novalidate>
  <input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" class="hp">
  <h2 class="eyebrow" style="font-weight:400">Get a food truck quote</h2>
  <div class="field"><label for="ft-occ">Event type <span class="req">*</span></label>
    <select id="ft-occ" name="occasion" data-label="Event type" required><option value="">Select</option>{_opt(["Office or employee lunch", "Food truck festival or rally", "Private party or celebration", "Company picnic", "Community or public event", "Something else"])}</select></div>
  <div class="field-row">
    <div class="field"><label for="ft-name">Name <span class="req">*</span></label><input id="ft-name" name="name" data-label="Name" required autocomplete="name" placeholder="First and last"></div>
    <div class="field"><label for="ft-email">Email <span class="req">*</span></label><input id="ft-email" type="email" name="email" data-label="Email" required autocomplete="email" placeholder="you@company.com"></div>
  </div>
  <div class="field-row">
    <div class="field"><label for="ft-date">Date</label><input id="ft-date" type="date" name="date" data-label="Date"></div>
    <div class="field"><label for="ft-loc">Location</label><input id="ft-loc" name="location" data-label="Location" placeholder="Address or city"{loc_val}></div>
  </div>
  <div class="field-row">
    <div class="field"><label for="ft-guests">Guest count</label><select id="ft-guests" name="guests" data-label="Guest count"><option value="">Select</option>{_opt(["Under 50", "50–150", "150–500", "500–1,500", "1,500+"])}</select></div>
    <div class="field"><label for="ft-trucks">Trucks</label><select id="ft-trucks" name="trucks" data-label="Trucks"><option value="">Select</option>{_opt(["1", "2–3", "4–6", "7+", "Not sure yet"])}</select></div>
  </div>
  <div class="field"><label for="ft-food">Food preferences</label><input id="ft-food" name="food" data-label="Food preferences" placeholder="Tacos, BBQ, dessert, vegan options…"></div>
  <button class="btn btn-pink" type="submit" style="width:100%">Get a Food Truck Quote</button>
  <p class="form-note" role="status">{FORM_NOTE}</p>
</form>"""


PLAN_TYPES = ["Corporate Event", "Brand Activation", "Team Building", "Food Truck Catering",
              "Festivals & Community", "Grand Opening", "Fundraiser", "Social Event"]


def plan_form(default_type="Corporate Event", location="", submit="Get Started", subject="Event inquiry"):
    pills = ""
    for i, t in enumerate(PLAN_TYPES):
        chk = " checked" if t == default_type else ""
        pills += f'<input type="radio" id="et{i}" name="event_type" value="{esc(t)}"{chk}><label for="et{i}">{esc(t)}</label>'
    loc_val = f' value="{esc(location)}"' if location else ""
    return f"""<form class="form-card" data-mailto="{EMAIL}" data-subject="{esc(subject)}" data-leads="{LEADS_URL}" data-form="{esc(subject)}" novalidate>
      <input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" class="hp">
      <fieldset class="field" name="event_type" data-label="Event type">
        <legend class="eyebrow">What are you planning?</legend>
        <div class="pill-set">{pills}</div>
      </fieldset>
      <div class="field-row">
        <div class="field"><label for="p-name">Name <span class="req">*</span></label><input id="p-name" name="name" data-label="Name" required autocomplete="name" placeholder="First and last"></div>
        <div class="field"><label for="p-co">Company or organization</label><input id="p-co" name="company" data-label="Company" autocomplete="organization" placeholder="Optional"></div>
      </div>
      <div class="field-row">
        <div class="field"><label for="p-email">Email <span class="req">*</span></label><input id="p-email" type="email" name="email" data-label="Email" required autocomplete="email" placeholder="you@company.com"></div>
        <div class="field"><label for="p-phone">Phone</label><input id="p-phone" type="tel" name="phone" data-label="Phone" autocomplete="tel" placeholder="Optional"></div>
      </div>
      <div class="field-row">
        <div class="field"><label for="p-date">Event date</label><input id="p-date" type="date" name="date" data-label="Event date">
          <label class="check"><input type="checkbox" data-flex-for="p-date"> Flexible / not sure yet</label></div>
        <div class="field"><label for="p-loc">Location</label><input id="p-loc" name="location" data-label="Location" placeholder="City, state"{loc_val}></div>
      </div>
      <div class="field-row">
        <div class="field"><label for="p-guests">Guest count</label><select id="p-guests" name="guests" data-label="Guest count"><option value="">Select</option>{_opt(["Under 50", "50–150", "150–500", "500–1,500", "1,500–5,000", "5,000+", "Not sure yet"])}</select></div>
        <div class="field"><label for="p-budget">Approximate budget</label><select id="p-budget" name="budget" data-label="Budget"><option value="">Select</option>{_opt(["Under $5,000", "$5,000–$15,000", "$15,000–$50,000", "$50,000–$100,000", "$100,000+", "Not sure yet"])}</select></div>
      </div>
      <div class="field"><label for="p-more">Tell us more</label><textarea id="p-more" name="details" data-label="Details" placeholder="Tell us about your event, goals or ideas."></textarea></div>
      <div class="form-foot">
        <p>Planning a festival for your city or venue? Pick &ldquo;Festivals &amp; Community&rdquo; above.</p>
        <button class="btn btn-pink" type="submit">{esc(submit)}</button>
      </div>
      <p class="form-note" role="status">{FORM_NOTE}</p>
    </form>"""


def service_hero(crumbs, h1, intro, cta_label, cta_href, photo, form_html=None):
    if form_html:
        side = f'<div class="hero-side" style="align-items:flex-start">{form_html}</div>'
        photo_in_copy = ph(photo, "", "min-height:220px;margin-top:32px") if photo else ""
        cta_btn = f'<a class="btn btn-pink" href="#ft-occ">{esc(cta_label)}</a>'
    else:
        side = f'<div class="hero-side" style="width:100%">{ph(photo, "", "width:100%;min-height:440px", eager=True)}</div>'
        photo_in_copy = ""
        cta_btn = f'<a class="btn btn-pink" href="{cta_href}">{esc(cta_label)}</a>'
    return f"""<section class="dark hero split"><div class="wrap hero-grid">
  <div class="hero-copy">
    {crumbs_html(crumbs)}
    <h1>{pinkify(h1)}</h1>
    <p class="lede">{esc(intro)}</p>
    <div class="hero-actions">{cta_btn}<a class="link-arrow" href="#faq">Common questions &rarr;</a></div>
    {photo_in_copy}
  </div>
  {side}
</div></section>"""


def why_band(why):
    if not why:
        return ""
    cols = "".join(f'<div class="reveal"><h2>{esc(h)}</h2><p>{esc(p)}</p></div>' for h, p in why)
    return f'<section style="background:var(--cream)"><div class="wrap split-copy">{cols}</div></section>'


def closing_block(heading, text, label, href):
    return f"""<section style="padding-top:0"><div class="wrap" style="max-width:820px;text-align:center">
  <h2 class="h2" style="margin-bottom:16px">{esc(heading)}</h2>
  <p class="lede" style="margin:0 auto 28px">{esc(text)}</p>
  <a class="btn btn-pink" href="{href}">{esc(label)}</a>
</div></section>"""


# ------------------------------------------------------------------ national service pages
def service_page(s):
    slug = s["slug"] + "/"
    set_depth(slug)
    url = SITE + "/" + slug
    crumbs = [("Home", ""), ("Services", "services/"), (s["name"], slug)]
    hero = service_hero(crumbs, s["h1"], s["intro"], s["cta"], plan(s["form_type"]), s["photo"],
                        truck_form() if s.get("hero_form") else None)
    resolve = lambda k: target_info(k)[1]
    grid = truck_cards(s["cards"]) if s.get("truck_cards") else card_grid(s["cards"], resolve)
    cards_sec = f"""<section id="services"><div class="wrap">
  <div class="sec-head"><h2>{esc(s["cards_title"])}</h2></div>
  {grid}
</div></section>"""
    extra = {"festival_formats": festival_formats, "truck_menu_steps": truck_menu_steps}.get(s.get("extra"), lambda: "")()
    why, closing = s["sections"][:-1], s["sections"][-1]
    caps = services_block("What&rsquo;s Included", "You bring the headcount and the date. We bring everything else.") if s.get("capabilities") else ""
    aud = audiences() if s.get("audiences") else ""
    brands = f'<section style="padding:56px 0 28px">{marquee("Brands we&rsquo;ve worked with", BRANDS)}</section>' if s.get("brands") else ""
    close_href = "#ft-occ" if s.get("hero_form") else plan(s["form_type"])
    rel = [target_info(k) for k in s["related"]]
    directory = city_directory(s["slug"])
    body = (hero + cards_sec + extra + why_band(why) + caps + aud + brands + faq_section(s["faqs"]) +
            closing_block(closing[0], closing[1], s["cta"], close_href) + directory + related_section(rel))
    graph = [org(), website()] + webpage(url, s["title"], s["meta"], crumbs) + [
        service_ld(url, s["name"], s["schema"], s["meta"], s["cards_title"], s["cards"], US),
        faq_ld(url, s["faqs"])]
    page(slug, s["title"], s["meta"], s["slug"], body, graph)


def services_hub():
    slug = "services/"
    set_depth(slug)
    url = SITE + "/" + slug
    title = "Event Planning & Production Services | Hop To It Events"
    desc = "Corporate events, brand activations, team building, festivals, fundraisers, food truck catering, private parties and event production services from Hop To It Events."
    crumbs = [("Home", ""), ("Services", slug)]
    groups = ""
    for gname, slugs in GROUPS:
        items = "".join(f'<a href="{link(x + "/")}"><h3>{esc(BY_SLUG[x]["name"])}</h3><p>{esc(BY_SLUG[x]["hub"])}</p></a>' for x in slugs)
        groups += f'<div class="hub-group"><h2>{gname}</h2><div class="hub-list">{items}</div></div>'
    faqs = [("What event planning services does Hop To It Events offer?",
             "Corporate event planning, team building, employee appreciation events, company picnics, brand activations, trade show activations, grand openings and product launches, festival and community event planning, fundraisers, private parties, food truck catering, bar and beverage services, event entertainment, event staffing and on-site management, and event rentals and decor coordination."),
            ("Can I hire Hop To It for just part of my event?",
             "Yes. You can hire us for full-service planning and production or for specific pieces, such as food truck catering, entertainment or on-site management."),
            ("Where does Hop To It Events work?", COMMON_WHERE)]
    body = f"""<section class="dark hero"><div class="wrap">
  {crumbs_html(crumbs)}
  <h1>Event Planning &amp; Production <span class="pink">Services</span></h1>
  <p class="lede">Hop To It Events is a full-service event planning and production company. Hire us for the whole event or the pieces you need, from concept and vendors to entertainment and on-site management.</p>
  <div class="hero-actions"><a class="btn btn-pink" href="{plan()}">Plan Your Event</a><a class="link-arrow" href="{link('tools/event-budget-calculator/')}">Estimate your budget &rarr;</a></div>
</div></section>
<section><div class="wrap">{groups}</div></section>
{faq_section(faqs)}"""
    item_list = {"@type": "ItemList", "name": "Event planning services", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": x["name"], "url": SITE + "/" + x["slug"] + "/"}
        for i, x in enumerate(SERVICES)]}
    graph = [org(), website()] + webpage(url, title, desc, crumbs, "CollectionPage") + [item_list, faq_ld(url, faqs)]
    page(slug, title, desc, "services", body, graph)


# ------------------------------------------------------------------ locations
def city_area(c):
    return [{"@type": "City", "name": c["city"],
             "containedInPlace": {"@type": "State", "name": STATE_NAMES.get(c["state"], c["state"])}},
            {"@type": "AdministrativeArea", "name": c["region"]}]


def city_directory(national):
    """Structured 'by city' directory for a national service page, grouped by state."""
    by_state = {}
    for c in CITIES:
        for p in c["pages"]:
            if p["national"] == national:
                by_state.setdefault(STATE_NAMES.get(c["state"], c["state"]), []).append(
                    (c["city"], f'locations/{c["slug"]}/{p["slug"]}/'))
    if not by_state:
        return ""
    name = BY_SLUG[national]["name"]
    groups = "".join(f'<div><h3>{esc(st)}</h3><p>' + " &middot; ".join(f'<a href="{link(u)}">{esc(n)}</a>' for n, u in sorted(items)) + '</p></div>'
                     for st, items in sorted(by_state.items()))
    return f"""<section id="by-city"><div class="wrap">
  <h2 class="h2" style="margin-bottom:24px">{esc(name)} by City</h2>
  <div class="city-dir">{groups}</div>
</div></section>"""


def locations_hub():
    slug = "locations/"
    set_depth(slug)
    url = SITE + "/" + slug
    title = "Event Planning Locations | Hop To It Events"
    desc = "Find Hop To It Events event planning, food truck catering, team building and brand activation services by city."
    crumbs = [("Home", ""), ("Locations", slug)]
    by_state = {}
    for c in CITIES:
        by_state.setdefault(STATE_NAMES.get(c["state"], c["state"]), []).append(c)
    groups = ""
    for st in sorted(by_state):
        tiles = "".join(f'<a href="{link("locations/" + c["slug"] + "/")}"><h3>{esc(c["city"])}</h3>'
                        f'<p>Corporate events, team building, food trucks and more across {esc(c["region"])}.</p></a>'
                        for c in sorted(by_state[st], key=lambda x: x["city"]))
        groups += f'<div class="hub-group"><h2>{esc(st)}</h2><div class="hub-list">{tiles}</div></div>'
    body = f"""<section class="dark hero"><div class="wrap">
  {crumbs_html(crumbs)}
  <h1>Event Planning <span class="pink">Locations</span></h1>
  <p class="lede">We&rsquo;ve produced events in 30+ U.S. markets. Find event planning, team building, food truck catering, brand activations and festival support by city. Don&rsquo;t see your city? Tell us where you&rsquo;re planning and we&rsquo;ll confirm what we can support.</p>
  <div class="hero-actions"><a class="btn btn-pink" href="{plan()}">Plan Your Event</a></div>
</div></section>
<section><div class="wrap">{groups}</div></section>"""
    items = [{"@type": "ListItem", "position": i + 1, "name": f'Event Planning in {c["city"]}',
              "url": f'{SITE}/locations/{c["slug"]}/'} for i, c in enumerate(CITIES)]
    graph = [org(), website()] + webpage(url, title, desc, crumbs, "CollectionPage") + [
        {"@type": "ItemList", "name": "Event planning locations", "itemListElement": items}]
    page(slug, title, desc, "locations", body, graph)


def city_hub(c):
    global _city
    _city = c["slug"]
    h = c["hub"]
    base = f'locations/{c["slug"]}/'
    set_depth(base)
    url = SITE + "/" + base
    crumbs = [("Home", ""), ("Locations", "locations/"), (c["city"], base)]
    pages_sorted = sorted(c["pages"], key=lambda p: p["phase"])
    cards = ""
    for i, p in enumerate(pages_sorted):
        cards += (f'<a class="card card-link reveal" href="{link(base + p["slug"] + "/")}">{ph(p["photo"], TONES[i % len(TONES)])}'
                  f'<div class="card-body"><h3>{esc(p["name"])}</h3><p>{esc(p["card"])}</p></div></a>')
    areas = "".join(f'<div class="hub-list-item"><h3 style="font-size:22px;margin-bottom:8px">{esc(n)}</h3><p style="color:var(--muted)">{esc(", ".join(towns))}.</p></div>'
                    for n, towns in h["areas"])
    form = plan_form(location=f'{c["city"]}, {c["state"]}', subject=f'{c["city"]} event inquiry')
    body = f"""
<section class="dark hero split"><div class="wrap hero-grid">
  <div class="hero-copy">
    {crumbs_html(crumbs)}
    <h1>{pinkify(h["h1"])}</h1>
    <p class="lede">{esc(h["intro"])}</p>
    <div class="hero-actions"><a class="btn btn-pink" href="#inquiry">{esc(h["cta"])}</a><a class="link-arrow" href="#services">Services in {esc(c["short"])} &rarr;</a></div>
  </div>
  <div class="hero-side" style="width:100%">{ph(h["photo"], "", "width:100%;min-height:440px", eager=True)}</div>
</div></section>

{calc_widget("corporate", f'{c["city"]}, {c["state"]}', f'What Will Your {c["city"]} Event Cost?')}

<section id="services"><div class="wrap">
  <div class="sec-head"><h2>{esc(h["services_title"])}</h2></div>
  <div class="grid-4b">{cards}</div>
</div></section>

<section style="background:var(--cream)"><div class="wrap split-copy">
  <div class="reveal"><h2>{esc(h["local"][0])}</h2><p>{esc(h["local"][1])}</p></div>
  <div class="reveal"><h2>{esc(h["proof"][0])}</h2><p>{esc(h["proof"][1])}</p></div>
</div></section>

{services_block(esc(h["caps"][0]), esc(h["caps"][1]))}

<section id="coverage"><div class="wrap">
  <h2 class="h2" style="margin-bottom:16px">{esc(h["coverage_title"])}</h2>
  <p class="lede" style="max-width:820px;margin-bottom:40px">{esc(h["coverage_intro"])}</p>
  <div class="split-copy" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:32px">{areas}</div>
</div></section>

{faq_section(h["faqs"])}

<section class="dark" id="inquiry"><div class="wrap" style="display:grid;grid-template-columns:minmax(0,.7fr) minmax(0,1.3fr);gap:48px">
  <div><span class="eyebrow gold">Get started</span><h2 class="h2" style="margin-bottom:16px">{esc(h["closing"])}</h2>
    <p class="lede">Tell us what you&rsquo;re planning and where in {esc(c["region"])}. Our team reviews every inquiry and follows up to talk through the details.</p></div>
  {form}
</div></section>
"""
    services = [{"@type": "ListItem", "position": i + 1, "name": f'{p["name"]} in {c["city"]}',
                 "url": SITE + "/" + base + p["slug"] + "/"} for i, p in enumerate(pages_sorted)]
    graph = [org(), website()] + webpage(url, h["title"], h["meta"], crumbs) + [
        {"@type": "Service", "@id": url + "#service", "name": f'Event Planning & Production in {c["city"]}',
         "serviceType": "Event planning and production", "description": h["meta"], "url": url,
         "provider": {"@id": ORG_ID}, "areaServed": city_area(c) + [
             {"@type": "Place", "name": t} for _, towns in h["areas"] for t in towns]},
        {"@type": "ItemList", "name": h["services_title"], "itemListElement": services},
        faq_ld(url, h["faqs"])]
    page(base, h["title"], h["meta"], "locations", body, graph)


def city_page(c, p):
    global _city
    _city = c["slug"]
    base = f'locations/{c["slug"]}/'
    slug = base + p["slug"] + "/"
    set_depth(slug)
    url = SITE + "/" + slug
    crumbs = [("Home", ""), ("Locations", "locations/"), (c["city"], base), (p["name"], slug)]
    loc = f'{c["city"]}, {c["state"]}'
    form = truck_form(loc) if p.get("hero_form") else None
    hero = service_hero(crumbs, p["h1"], p["intro"], p["cta"], "#inquiry", p["photo"], form)
    city_slugs = {x["slug"] for x in c["pages"]}
    resolve = lambda k: base + k + "/" if k in city_slugs else target_info(k)[1]
    cards_sec = f"""<section id="services"><div class="wrap">
  <div class="sec-head"><h2>{esc(p["cards_title"])}</h2></div>
  {card_grid(p["cards"], resolve)}
</div></section>"""
    feature = ""
    if p.get("feature") == "chef_battle":
        feature = chef_battle_feature(base + "team-building/" if p["slug"] != "team-building" else "corporate-team-building/")
    elif p.get("feature") == "menu":
        feature = f'<section class="bg-pink"><div class="wrap menu-split"><div><span class="eyebrow">On the menu</span><h2 class="h2">Pick Your Trucks</h2></div>{chips_html()}</div></section>'
    why, closing = p["sections"][:-1], p["sections"][-1]
    aud = audiences() if p.get("audiences") else ""
    brands = f'<section style="padding:56px 0 28px">{marquee("Brands we&rsquo;ve worked with", BRANDS)}</section>' if p.get("brands") else ""
    if form:
        inquiry = closing_block(closing[0], closing[1], p["cta"], "#ft-occ")
    else:
        inquiry = f"""<section class="dark" id="inquiry"><div class="wrap" style="display:grid;grid-template-columns:minmax(0,.7fr) minmax(0,1.3fr);gap:48px">
  <div><span class="eyebrow gold">Get started</span><h2 class="h2" style="margin-bottom:16px">{esc(closing[0])}</h2><p class="lede">{esc(closing[1])}</p></div>
  {plan_form(p["form_type"], loc, p["cta"], f'{c["city"]} {p["name"]} inquiry')}
</div></section>"""
    others = {x["slug"]: x for x in c["pages"]}
    rel = [(f'Event Planning in {c["city"]}', base), (f'{BY_SLUG[p["national"]]["name"]} Nationwide', p["national"] + "/")]
    rel += [(f'{others[k]["name"]} in {c["short"]}', base + k + "/") for k in p["related"][:3] if k in others]
    rel += [(f'{p["name"]} in {n}', u) for n, u in nearby_links(c, p["slug"])[:2]]
    calc = calc_widget(PLAN_TO_CALC.get(p["form_type"], "corporate"), loc,
                       f'Estimate Your {c["city"]} {p["name"]} Budget')
    body = (hero + cards_sec + feature + why_band(why) + aud + brands + calc + faq_section(p["faqs"]) + inquiry +
            related_section(rel, f'More in {c["city"]}'))
    index = p["phase"] <= PUBLISH_PHASE
    graph = [org(), website()] + webpage(url, p["title"], p["meta"], crumbs) + [
        service_ld(url, f'{p["name"]} in {c["city"]}', BY_SLUG[p["national"]]["schema"], p["meta"],
                   p["cards_title"], p["cards"], city_area(c)),
        faq_ld(url, p["faqs"])]
    page(slug, p["title"], p["meta"], "locations", body, graph, index=index)


# ------------------------------------------------------------------ budget calculator
# STARTING ESTIMATES FOR REVIEW. Replace with Hop To It's real pricing, then set
# CALC_CONFIRMED = True so the page is indexed and listed in the sitemap.
CALC_CONFIRMED = False
CALC_RATES = {
    "types": {
        "corporate": {"label": "Corporate event or party", "factor": 1.0, "planType": "Corporate Event"},
        "teambuilding": {"label": "Team building (Chef Battle or Bartender Battle)", "planType": "Team Building", "mode": "package"},
        "activation": {"label": "Brand activation or sampling", "planType": "Brand Activation", "mode": "activation"},
        "trucks": {"label": "Food truck catering", "planType": "Food Truck Catering", "mode": "trucks"},
        "festival": {"label": "Festival or public event", "planType": "Festivals & Community", "mode": "festival"},
        "opening": {"label": "Grand opening", "factor": 1.0, "planType": "Grand Opening"},
        "fundraiser": {"label": "Fundraiser or gala", "factor": 1.0, "planType": "Fundraiser"},
        "social": {"label": "Private party", "factor": 0.9, "planType": "Social Event"},
    },
    # Corporate events, openings, fundraisers, private parties
    "items": [
        {"id": "food", "label": "Food", "unit": "guest", "low": 25, "high": 60, "on": True},
        {"id": "bar", "label": "Bar & beverages", "unit": "hour", "low": 50, "high": 100, "on": True},
        {"id": "ent", "label": "Entertainment (DJ, hosts, performers)", "unit": "flat", "low": 800, "high": 3500, "on": True},
        {"id": "decor", "label": "Rentals & decor", "unit": "guest", "low": 10, "high": 35, "on": True},
        {"id": "photo", "label": "Photography & video", "unit": "flat", "low": 500, "high": 2500, "on": False},
        {"id": "staff", "label": "On-site staffing", "unit": "guest_hour", "low": 1.5, "high": 3.5, "min": 400, "on": True},
        {"id": "venue", "label": "Venue rental", "unit": "guest", "low": 15, "high": 60, "on": False},
    ],
    "planning": {"label": "Planning & production", "low": 0.15, "high": 0.20, "min": 1500},
    # Chef Battle / Bartender Battle packages (all-in). price None = "and up".
    "packages": {
        "onsite": {"label": "Team building on-site (at your office)", "tiers": [[20, 15000], [30, 20000], [50, 30000], [None, 50000]]},
        "offsite": {"label": "Team building off-site (venue, open bar, passed apps)", "tiers": [[20, 25000], [30, 35000], [50, 50000], [None, 75000]]},
        "private": {"label": "Private event (live pro chef competition, MC, AV)", "tiers": [[100, 75000], [200, 100000], [300, 150000], [None, 200000]]},
    },
    # Food truck catering: per-guest food cost, each truck has a minimum, about 1 truck per 100 guests.
    "trucks": {"guests_per_truck": 100, "low": 15, "high": 30, "truck_min_low": 1200, "truck_min_high": 1500,
               "fee_label": "Truck sourcing & coordination", "fee_low": 0.10, "fee_high": 0.15, "fee_min": 500},
    # Brand activations are priced by days and hours on site, not guest count.
    "activation_items": [
        {"id": "a-staff", "label": "On-site staffing team", "unit": "day_hour", "low": 200, "high": 1000, "on": True, "core": True},
        {"id": "a-setup", "label": "Booth setup, signage & breakdown", "unit": "day", "low": 400, "high": 1500, "on": False},
        {"id": "a-samples", "label": "Sampling supplies (cups, napkins, ice)", "unit": "sample", "low": 0.15, "high": 0.40, "on": False},
        {"id": "a-rentals", "label": "Tent, tables & display rentals", "unit": "day", "low": 250, "high": 900, "on": False},
        {"id": "a-recap", "label": "Photos & recap report", "unit": "flat", "low": 300, "high": 900, "on": False},
    ],
    "activation_planning": {"label": "Planning & coordination", "low": 0.15, "high": 0.20},
    # Festivals: production fee by attendance (1,000 = $35K,
    # 2,000 = $50K, 5,000 = $75K), plus event expenses per attendee and vendor allowances.
    "festival": {
        "fee_points": [[1000, 35000], [2000, 50000], [5000, 75000], [10000, 100000], [20000, 150000]],
        "fee_high": 1.2,
        "fee_label": "Planning, production, marketing & sponsorship sales",
        "expense_low": 25, "expense_high": 40,
        "expense_label": "Event expenses (production, security, permits, insurance, staffing, advertising)",
        "vendor_allowance": 1000,
        "ticket_low": 30, "ticket_high": 45,
    },
}


PLAN_TO_CALC = {"Corporate Event": "corporate", "Team Building": "teambuilding", "Brand Activation": "activation",
                "Festivals & Community": "festival", "Grand Opening": "opening", "Fundraiser": "fundraiser",
                "Social Event": "social", "Food Truck Catering": "trucks"}


def calc_widget(default="corporate", location="", heading=None):
    """Budget calculator + lead form. Used on the calculator page and every city page."""
    types = "".join(f'<option value="{k}"{" selected" if k == default else ""}>{esc(v["label"])}</option>'
                    for k, v in CALC_RATES["types"].items())
    checks = "".join(
        f'<label class="cb"><input type="checkbox" id="c-{i["id"]}"{" checked" if i["on"] else ""}> <span>{esc(i["label"])}</span></label>'
        for i in CALC_RATES["items"])
    loc_val = f' value="{esc(location)}"' if location else ""
    act_checks = "".join(
        f'<label class="cb"><input type="checkbox" id="c-{i["id"]}"{" checked" if i["on"] else ""}> <span>{esc(i["label"])}</span></label>'
        for i in CALC_RATES["activation_items"])
    pkgs = "".join(f'<option value="{k}">{esc(v["label"])}</option>' for k, v in CALC_RATES["packages"].items())
    sec_attr = ' id="budget" style="background:var(--cream)"' if heading else ""
    intro = (f'<div class="wrap" style="margin-bottom:32px"><span class="eyebrow">Event budget calculator</span>'
             f'<h2 class="h2">{esc(heading)}</h2><p class="lede" style="margin-top:12px">Pick your event, guest count and what you need for an instant budget range, then request a real proposal.</p></div>') if heading else ""
    return f"""<section{sec_attr}>{intro}<div class="wrap calc" id="calc" data-plan="{link('plan-your-event/')}">
  <form class="calc-in" onsubmit="return false">
    <div class="field"><label for="c-type">Event type</label><select id="c-type">{types}</select></div>
    <div class="field" data-show="event package trucks"><label for="c-guests">Guests: <b id="c-guests-out">100</b></label>
      <input type="range" id="c-guests-range" min="10" max="1000" step="10" value="100" aria-label="Guests slider">
      <input type="number" id="c-guests" min="10" max="5000" value="100" inputmode="numeric"></div>
    <div class="field" data-show="package"><label for="c-pkg">Format</label><select id="c-pkg">{pkgs}</select></div>
    <div class="field" data-show="festival"><label for="c-att">Expected attendance: <b id="c-att-out">2,000</b></label>
      <input type="range" id="c-att" min="500" max="20000" step="500" value="2000"></div>
    <div class="field" data-show="festival"><label for="c-vend">Food &amp; drink vendors: <b id="c-vend-out">15</b></label>
      <input type="range" id="c-vend" min="0" max="100" step="1" value="15"></div>
    <div class="field" data-show="event activation trucks"><label for="c-hours"><span data-show="event trucks">Event length</span><span data-show="activation">Hours per day</span>: <b id="c-hours-out">3 hours</b></label>
      <input type="range" id="c-hours" min="1" max="8" step="0.5" value="3"></div>
    <fieldset class="field" data-show="event"><legend class="lbl">What do you need?</legend><div class="cbs">{checks}</div></fieldset>
    <div data-show="activation">
      <div class="field"><label for="c-act-days">Activation days: <b id="c-act-days-out">1</b></label><input type="range" id="c-act-days" min="1" max="30" step="1" value="1"></div>
      <div class="field"><label for="c-act-samples">Expected samples handed out: <b id="c-act-samples-out">500</b></label><input type="range" id="c-act-samples" min="0" max="10000" step="100" value="500"></div>
      <fieldset class="field"><legend class="lbl">What do you need?</legend><div class="cbs">{act_checks}</div></fieldset>
    </div>
    <p class="note" data-show="package">Packages are all-in: competition format, equipment, ingredients, chef host and production.</p>
  </form>
  <div class="calc-out" aria-live="polite">
    <span class="eyebrow gold">Estimated budget</span>
    <p class="calc-total" id="c-total">$0</p>
    <p class="calc-per" id="c-per"></p>
    <p class="calc-offset" id="c-offset" hidden></p>
    <ul class="calc-rows" id="c-rows"></ul>
    <p class="note" style="margin:0 0 22px">Planning estimate, not a quote. Costs vary by city, date, venue and vendors.</p>
    <form class="calc-lead" data-mailto="{EMAIL}" data-subject="Budget calculator lead" data-leads="{LEADS_URL}" data-form="Budget calculator" novalidate>
      <input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" class="hp">
      <h2 class="calc-lead-h">Get a real proposal for this event</h2>
      <input type="hidden" name="event_type" id="h-type" data-label="Event type">
      <input type="hidden" name="guests" id="h-guests" data-label="Guests">
      <input type="hidden" name="hours" id="h-hours" data-label="Hours">
      <input type="hidden" name="services" id="h-services" data-label="Services">
      <input type="hidden" name="estimate" id="h-estimate" data-label="Calculator estimate">
      <div class="field-row">
        <div class="field"><label for="l-name">Name <span class="req">*</span></label><input id="l-name" name="name" data-label="Name" required autocomplete="name"></div>
        <div class="field"><label for="l-email">Email <span class="req">*</span></label><input id="l-email" type="email" name="email" data-label="Email" required autocomplete="email"></div>
      </div>
      <div class="field-row">
        <div class="field"><label for="l-phone">Phone</label><input id="l-phone" type="tel" name="phone" data-label="Phone" autocomplete="tel" placeholder="Optional"></div>
        <div class="field"><label for="l-date">Event date</label><input id="l-date" type="date" name="date" data-label="Event date"></div>
      </div>
      <div class="field"><label for="l-loc">City</label><input id="l-loc" name="location" data-label="Location" placeholder="City, state"{loc_val}></div>
      <button class="btn btn-pink" type="submit" style="width:100%">Get My Proposal</button>
      <p class="form-note" role="status">{FORM_NOTE}</p>
      <p class="note" style="margin-top:12px">Rather give more detail? <a id="c-cta" href="{plan()}" style="color:var(--gold);font-weight:700">Use the full form</a>.</p>
    </form>
  </div>
</div></section>
<script type="application/json" id="calc-rates">{json.dumps(CALC_RATES)}</script>
<script src="{link('assets/calculator.js')}" defer></script>"""


def calculator_page():
    slug = "tools/event-budget-calculator/"
    set_depth(slug)
    url = SITE + "/" + slug
    title = "Event Budget Calculator: Estimate Your Event Cost | Hop To It Events"
    desc = "Free event budget calculator. Estimate the cost of a corporate event, team building, brand activation, festival or party by guest count, hours and services."
    crumbs = [("Home", ""), ("Tools", "tools/event-budget-calculator/"), ("Event Budget Calculator", slug)]
    faqs = [("How much does a corporate event cost?",
             "It depends mostly on guest count, length and what's included. Food and beverage are usually the biggest line items, followed by entertainment, rentals and staffing. Use the calculator for a starting range, then share your details for a tailored proposal."),
            ("What's included in planning and production?",
             "Concept and strategy, vendor sourcing and management, timelines, logistics and on-site event management. Hop To It has been planning and producing events since 2010."),
            ("Is this estimate a quote?",
             "No. It's a planning range to help you set a budget. Prices vary by city, date, venue and vendors. Tell us about your event and we'll put together a real proposal."),
            ("How can I lower my event cost per guest?",
             "Shorter events, a focused menu, beer and wine instead of a full bar, weekday dates and fewer rentals all bring the per-guest cost down. We can suggest options that fit your budget.")]
    body = f"""
<section class="dark hero"><div class="wrap">
  {crumbs_html(crumbs)}
  <h1>Event Budget <span class="pink">Calculator</span></h1>
  <p class="lede">Get a quick estimate for your next corporate event, team building, brand activation or party. Pick your event, guest count and what you need, and see a budget range in seconds.</p>
</div></section>

{calc_widget()}
{faq_section(faqs)}
{related_section([target_info(k) for k in ["corporate-event-planning", "corporate-team-building", "brand-activations", "private-party-planning"]], "Plan It With Us")}
"""
    app = {"@type": "WebApplication", "@id": url + "#app", "name": "Event Budget Calculator",
           "url": url, "applicationCategory": "BusinessApplication", "operatingSystem": "Any",
           "description": desc, "isAccessibleForFree": True, "publisher": {"@id": ORG_ID},
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    graph = [org(), website()] + webpage(url, title, desc, crumbs) + [app, faq_ld(url, faqs)]
    page(slug, title, desc, "services", body, graph, index=CALC_CONFIRMED)


# ------------------------------------------------------------------ home
def home():
    set_depth("")
    url = SITE + "/"
    exp = [
        ("Corporate Events", "Bring your team, customers or partners together with memorable events designed to celebrate, connect and engage.", "Company celebration", "corporate-event-planning",
         [("Employee Appreciation", "employee-appreciation-events"), ("Company Picnics", "company-picnics"), ("Sales Meetings", "corporate-event-planning"), ("Conferences", "corporate-event-planning")]),
        ("Festivals &amp; Community Events", "From food festivals to large-scale community celebrations, we create experiences that bring people together.", "Downtown street festival", "festival-event-planning",
         [("Food Festivals", "festival-event-planning"), ("Downtown Celebrations", "festival-event-planning"), ("Food Truck Rallies", "food-truck-catering")]),
        ("Brand Activations", "Turn brand awareness into real-world engagement with interactive experiences that connect with your audience.", "Dunkin mascots at a festival", "brand-activations",
         [("Experiential Marketing", "brand-activations"), ("Trade Shows", "trade-show-activations"), ("Sampling Events", "brand-activations")]),
        ("Event Entertainment", "Give guests something to talk about with live competitions, DJs, performers and interactive experiences built around your event.", "Live chef competition, crowd", "event-entertainment",
         [("Live Competitions", "event-entertainment"), ("DJs &amp; Music", "event-entertainment"), ("Bartender Battle", "bar-beverage-services")]),
        ("Grand Openings &amp; Launches", "Make a memorable first impression with launch events that generate excitement, attract attention and bring people through the door.", "Ribbon cutting, crowd", "grand-openings-product-launches",
         [("Restaurant Openings", "grand-openings-product-launches"), ("Product Launches", "grand-openings-product-launches"), ("Business Anniversaries", "grand-openings-product-launches")]),
        ("Fundraisers &amp; Nonprofit Events", "Bring your mission to life with engaging events designed to inspire participation, build community and support fundraising goals.", "Benefit event, evening", "fundraiser-event-planning",
         [("Charity Festivals", "fundraiser-event-planning"), ("Benefit Events", "fundraiser-event-planning"), ("Private Parties", "private-party-planning")]),
    ]
    cards = ""
    for t, d, l, s, tg in exp:
        tags = '<div class="tags">' + "".join(f'<a href="{link(h + "/")}">{n}</a>' for n, h in tg) + "</div>"
        cards += f'<article class="card reveal">{ph(l, "pink")}<div class="card-body"><h3><a href="{link(s + "/")}">{t}</a></h3><p>{d}</p>{tags}</div></article>'
    signature = [("Chef Battle", "&#128298;", "Flagship", "pink", "Culinary competition &middot; 20+ cities"),
                 ("Donut Fest", "&#127849;", "Flagship", "pink", "Donut festival"),
                 ("BrunchFest", "&#129374;", "Licensable", "gold", "Brunch festival"),
                 ("Dessert Fest", "&#129473;", "Licensable", "gold", "Sweet treats festival"),
                 ("Bartender Battle", "&#127864;", "Team building", "teal", "Mixology competition"),
                 ("Wing Fest", "&#127831;", "Festival", "pink", "Wing festival")]
    tiles = "".join(f'<a class="brand-tile reveal" href="{link("events/")}"><span class="flag {c}">{f}</span><div class="emo" aria-hidden="true">{e}</div><h3>{n}</h3><p>{s}</p></a>'
                    for n, e, f, c, s in signature)
    faqs = [("What does Hop To It Events do?", ORG_DESC),
            ("What types of events does Hop To It Events plan?", "Corporate events, employee appreciation events, company picnics, team building, brand activations, trade show activations, grand openings and product launches, festivals and community events, fundraisers, private parties and food truck catering."),
            ("How is Hop To It different from other event planners?", "We've been planning and producing events since 2010, and we don't just plan events, we create our own. Our team builds, markets, tickets and produces signature event brands like Chef Battle and Donut Fest, and we bring that experience to every client event."),
            ("Where does Hop To It Events produce events?", "We've produced events in 30+ U.S. markets, including Los Angeles, San Diego, Las Vegas, Chicago, Austin, Denver, Atlanta and Boston. Tell us your city and we'll confirm what we can support."),
            ("How do I start planning an event with Hop To It?", f"Fill out the Plan Your Event form with your event type, date, location, guest count and budget, or email {EMAIL}. Our team reviews every inquiry and follows up to talk through the details.")]
    body = f"""
<section class="dark hero"><div class="wrap hero-grid">
  <div>
    <span class="eyebrow">Event planning &amp; production since 2010</span>
    <h1>We Plan It. We Produce It. You <span class="pink">Enjoy It.</span></h1>
    <p class="lede">From corporate celebrations and brand activations to food festivals and community events, Hop To It Events brings your vision to life with creative event planning, seamless production and unforgettable experiences.</p>
    <div class="hero-actions"><a class="btn btn-pink" href="{plan()}">Plan Your Event</a><a class="link-arrow" href="{link('events/')}">Explore Our Events &rarr;</a></div>
  </div>
  {ph("Produced client event", "", "min-height:460px", eager=True)}
</div></section>

<section><div class="wrap">
  <h2 class="h2">We Plan &amp; Produce Events</h2>
  <div class="tabs" role="tablist" aria-label="What we do">
    <button class="tab" role="tab" aria-selected="true" aria-controls="tp1" id="t1">Full-Service Event Planning &amp; Production</button>
    <button class="tab" role="tab" aria-selected="false" aria-controls="tp2" id="t2">Our Signature Events</button>
    <button class="tab" role="tab" aria-selected="false" aria-controls="tp3" id="t3">Corporate Experiences &amp; Team Building</button>
  </div>
  <div class="tab-panel" role="tabpanel" id="tp1" aria-labelledby="t1">
    <div><h3>From the first big idea to the last guest out.</h3>
      <p>From the first big idea to the final guest leaving, we handle the details that make events successful. Our team brings together creative concepts, venues, vendors, entertainment, marketing and on-site production to deliver experiences worth remembering.</p>
      <p style="font-size:14px">Corporate celebrations, company picnics, grand openings, customer appreciation events, brand activations, community festivals and private events.</p>
      <a class="btn btn-pink" href="{link('services/')}" style="margin-top:12px">See All Services</a></div>
    {ph("Full-service event", "black")}
  </div>
  <div class="tab-panel" role="tabpanel" id="tp2" aria-labelledby="t2" hidden>
    <div><h3>We run our own festivals, too.</h3>
      <p>Chef Battle, Donut Fest, Bartender Battle and a dozen more original event brands, produced in 30+ U.S. markets. Every one is built, marketed, ticketed and run by our team.</p>
      <p style="font-size:14px">Buy a ticket, sponsor a stage, sell as a vendor or bring one of our events to your city.</p>
      <a class="btn btn-pink" href="{link('events/')}" style="margin-top:12px">See Our Events</a></div>
    {ph("Donut Fest crowd", "black")}
  </div>
  <div class="tab-panel" role="tabpanel" id="tp3" aria-labelledby="t3" hidden>
    <div><h3>Team building people actually look forward to.</h3>
      <p>Live culinary competitions, cocktail challenges and tasting experiences, scaled down from our public festivals for your team, your clients or your conference floor.</p>
      <p style="font-size:14px">Cook-offs, kickoffs, appreciation days and holiday parties.</p>
      <a class="btn btn-pink" href="{link('corporate-team-building/')}" style="margin-top:12px">Corporate Team Building</a></div>
    {ph("Corporate rooftop reception", "black")}
  </div>
</div></section>

<section class="bg-pink"><div class="wrap">
  <div class="sec-head"><h2>Experiences We Create</h2><a class="link-arrow" href="{link('services/')}">All services &rarr;</a></div>
  <div class="grid-3">{cards}</div>
</div></section>

<section><div class="wrap">
  <div class="sec-head">
    <div><span class="eyebrow">Food truck catering</span><h2>Bring the <span class="pink">Trucks</span> to You</h2></div>
    <div><p class="lede" style="margin-bottom:18px">Tell us the headcount and the date, and we&rsquo;ll help line up the trucks, the permits and the schedule.</p>
    <a class="btn btn-pink btn-sm" href="{link('food-truck-catering/')}">Get a Food Truck Quote</a></div>
  </div>
  {truck_cards(cards=[("Food Truck Catering", "We help bring food trucks to company events, festivals and community gatherings, from one truck to a full lineup.", "food-truck-catering"),
                       ("Specialty & Dessert Trucks", "Donuts, coffee and other specialty trucks that give guests a treat and add something different to your event.", "food-truck-catering")],
               meta=[("Food trucks", "pink", "Donut trailer at a brewery event"), ("Specialty", "gold", "Food truck rally at dusk")])}
</div></section>

{services_block("From Big Ideas to Flawless Execution", "We manage the moving parts so you can focus on your guests. From creative strategy and vendor coordination to event-day execution, our team brings everything together.")}

{calc_widget("corporate", "", "What Will Your Event Cost?")}

<section><div class="wrap">
  <div class="sec-head">
    <div><h2>We Don&rsquo;t Just Plan Events.<br>We Create Our Own.</h2></div>
    <a class="link-arrow" style="color:var(--pink)" href="{link('events/')}">All signature events &rarr;</a>
  </div>
  <p class="lede" style="max-width:760px;margin:-20px 0 44px">Our experience goes beyond planning events for clients. We&rsquo;re the team behind Chef Battle, Donut Fest, BrunchFest and other live experiences produced across the country, and we bring that same creativity, production expertise and attention to detail to every event we create.</p>
  <div class="grid-6">{tiles}</div>
</div></section>

{audiences()}
{faq_section(faqs)}
"""
    title = "Hop To It Events | Event Planning & Production Company"
    desc = "Hop To It Events is a full-service event planning and production company for corporate events, brand activations, team building, food truck catering and festivals in 30+ U.S. markets."
    graph = [org(), website()] + webpage(url, title, desc, None) + [faq_ld(url, faqs)]
    page("", title, desc, "home", body, graph)


# ------------------------------------------------------------------ events
def events():
    slug = "events/"
    set_depth(slug)
    url = SITE + "/" + slug
    title = "Food & Drink Festivals and Signature Events | Hop To It Events"
    desc = "Chef Battle, Donut Fest, Bartender Battle and 12 more food and drink festivals in 30+ U.S. markets. Get tickets, sponsor, vend or bring an event to your city."
    brands = [("Donut Fest", "&#127849;", "Donut Festival", "sweets", "Flagship", TICKETS_DONUT_FEST_LV),
              ("Chef Battle", "&#128298;", "Culinary Competition", "savory competitions", "Flagship", GCL),
              ("Bartender Battle", "&#127864;", "Mixology Competition", "drinks competitions", "", "bar-beverage-services/"),
              ("Wine Bash", "&#127863;", "Wine Tasting", "drinks", "", ""),
              ("Wing Fest", "&#127831;", "Wing Festival", "savory", "", ""),
              ("Say Cheese Fest", "&#129472;", "Cheese Festival", "savory", "", ""),
              ("Sweets + Snacks Fest", "&#127852;", "Confections Festival", "sweets", "", ""),
              ("Cheers + Drink Fest", "&#129346;", "Beverage Festival", "drinks", "", ""),
              ("Donut &amp; Dessert Fest", "&#129473;", "Sweet Treats Festival", "sweets", "", ""),
              ("Treat Me Fest", "&#127856;", "Tasting + Pampering", "sweets", "", ""),
              ("Drink Local", "&#127866;", "Local Beverage Showcase", "drinks", "", ""),
              ("After Work Social", "&#127750;", "Networking + Drinks", "drinks", "", ""),
              ("Cocktail Shake Off", "&#127865;", "Cocktail Competition", "drinks competitions", "", ""),
              ("Pizza Party", "&#127829;", "Pizza Festival", "savory", "", ""),
              ("Donut 5K", "&#127939;", "Fun Run + Donut Fest", "sweets", "", "")]
    tiles = ""
    for n, e, d, cat, flag, href in brands:
        f = f'<span class="flag pink">{flag}</span>' if flag else ""
        inner = f'{f}<div class="emo" aria-hidden="true">{e}</div><h3>{n}</h3><p>{d}</p>'
        if href:
            tgt = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
            tiles += f'<a class="brand-tile" href="{link(href)}"{tgt} data-cat="{cat}">{inner}</a>'
        else:
            tiles += f'<div class="brand-tile" data-cat="{cat}">{inner}</div>'
    faqs = [("What are Hop To It Events' signature events?", "Fifteen original food and drink event brands, including Donut Fest, Chef Battle, Bartender Battle, Wine Bash, Wing Fest, Say Cheese Fest, Cocktail Shake Off and Donut 5K."),
            ("How do I buy tickets to Donut Fest or Chef Battle?", "Upcoming dates are listed under Coming Up on this page, each with a link to tickets or event details."),
            ("How can my brand sponsor a festival?", f"Email {EMAIL} with your brand, goals and the markets you're interested in, and we'll share sponsorship options."),
            ("Can I bring one of these events to my city?", "Yes. We work with cities, venues and local partners to bring established event concepts like Donut Fest and Chef Battle to new markets.")]
    body = f"""
<section class="dark hero"><div class="wrap hero-grid" style="align-items:end">
  <div>
    <span class="eyebrow">Signature events &amp; experiences</span>
    <h1>Our Events. Your <span class="pink">Opportunity.</span></h1>
    <p class="lede">From culinary competitions and food festivals to cocktail experiences and community celebrations, we create and produce original events across the country. Join us as a guest, connect with consumers as a sponsor, showcase your business as a vendor or bring one of our experiences to your market.</p>
  </div>
  <div class="stats" style="justify-self:end">
    <div class="stat"><b>2010</b><span>Since</span></div>
    <div class="stat"><b>15</b><span>Event brands</span></div>
    <div class="stat"><b>30+</b><span>Markets</span></div>
    <div class="stat"><b>100+</b><span>Events produced</span></div>
  </div>
</div></section>

<section><div class="wrap">
  <h2 class="skip">Our event brands</h2>
  <div class="filters">
    <div class="set" role="group" aria-label="Filter event brands">
      <button class="filter" data-filter="all" aria-pressed="true">All</button>
      <button class="filter" data-filter="sweets" aria-pressed="false">Sweets</button>
      <button class="filter" data-filter="savory" aria-pressed="false">Savory</button>
      <button class="filter" data-filter="drinks" aria-pressed="false">Drinks</button>
      <button class="filter" data-filter="competitions" aria-pressed="false">Competitions</button>
    </div>
    <span class="eyebrow muted" style="margin:0">15 event brands</span>
  </div>
  <div class="grid-4b">{tiles}</div>
</div></section>

<section style="padding-top:0"><div class="wrap event-photos">
  {ph("Donut Fest Las Vegas crowd", "", "min-height:420px")}
  {ph("Donut Fest donuts", "", "min-height:420px")}
</div></section>

<section class="dark" id="take-part"><div class="wrap">
  <div class="sec-head"><h2>Ways to Take Part</h2></div>
  <div class="grid-4b">
    <div class="take p"><h3>Attend an Event</h3><p>Discover unique food, drink and entertainment experiences happening in cities across the country.</p><a href="#coming-up">Find an event &rarr;</a></div>
    <div class="take w"><h3>Become a Sponsor</h3><p>Put your brand in front of engaged audiences through memorable, real-world experiences and activations.</p><a href="{esc(mailto('Sponsorship inquiry'))}">Sponsorship info &rarr;</a></div>
    <div class="take g"><h3>Become a Vendor</h3><p>Showcase your products, connect with new customers and grow your business at our signature events.</p><a href="{esc(mailto('Vendor application'))}">Apply to vend &rarr;</a></div>
    <div class="take t"><h3>Bring an Event to Your City</h3><p>Explore opportunities to bring one of our established event concepts to your community or venue.</p><a href="{link('festival-event-planning/')}">Let&rsquo;s talk &rarr;</a></div>
  </div>
</div></section>

<section id="coming-up"><div class="wrap">
  <div class="sec-head"><h2>Coming Up</h2><span class="eyebrow muted" style="margin:0">More dates announced soon</span></div>
  <div class="dates">
    <div class="date-row"><div class="d"><small>Jan &ndash; Mar 2027</small><b>23</b></div><div class="e" aria-hidden="true">&#128298;</div>
      <h3>Chef Battle California Tour<small>Live culinary competitions in 25 California markets</small></h3><span class="loc">California</span>
      <a class="btn btn-pink btn-sm" href="{GCL}" target="_blank" rel="noopener">Details</a></div>
    <div class="date-row"><div class="d"><small>Jan 2027</small><b>24</b></div><div class="e" aria-hidden="true">&#127849;</div>
      <h3>Donut Fest Las Vegas<small>Saturday, January 24, 2027 &middot; 12&ndash;5 PM</small></h3><span class="loc">Las Vegas</span>
      <a class="btn btn-pink btn-sm" href="{TICKETS_DONUT_FEST_LV}" target="_blank" rel="noopener">Get tickets</a></div>
  </div>
  <p class="note">Sponsoring Donut Fest Las Vegas? <a href="{link('donutfestvegas.html')}" style="color:var(--pink);font-weight:700">See sponsorship packages</a>.</p>
</div></section>
{faq_section(faqs)}
{related_section([target_info(k) for k in ["festival-event-planning", "brand-activations", "corporate-team-building", "event-entertainment"]], "Hire Us for Your Event")}
"""
    crumbs = [("Home", ""), ("Our Events", slug)]
    event_ld = {"@type": "Event", "@id": url + "#donut-fest-las-vegas-2027", "name": "Donut Fest Las Vegas",
                "startDate": "2027-01-24T12:00:00-08:00", "endDate": "2027-01-24T17:00:00-08:00",
                "eventStatus": "https://schema.org/EventScheduled",
                "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                "description": "A donut festival with local donut shops, vendors and sponsors in Las Vegas.",
                "image": SITE + "/assets/og-image.png",
                "location": {"@type": "Place", "name": "Las Vegas, NV",
                             "address": {"@type": "PostalAddress", "addressLocality": "Las Vegas",
                                         "addressRegion": "NV", "addressCountry": "US"}},
                "organizer": {"@id": ORG_ID},
                "offers": {"@type": "Offer", "url": TICKETS_DONUT_FEST_LV}}
    graph = [org(), website()] + webpage(url, title, desc, crumbs, "CollectionPage") + [event_ld, faq_ld(url, faqs)]
    page(slug, title, desc, "events", body, graph)


# ------------------------------------------------------------------ about
def about():
    slug = "about/"
    set_depth(slug)
    url = SITE + "/" + slug
    title = "About Us | Hop To It Events, Event Planning & Production"
    desc = "Hop To It Events is a full-service event planning and production company that also creates and runs its own food and drink festivals in 30+ U.S. markets."
    svc_links = ", ".join(f'<a href="{link(x["slug"] + "/")}" style="text-decoration:underline">{esc(x["name"].lower() if i else x["name"])}</a>'
                          for i, x in enumerate(SERVICES[:8]))
    city_links = ", ".join(f'<a href="{link("locations/" + k + "/")}" style="text-decoration:underline">{esc(CITY_BY_SLUG[k]["city"])}</a>' for k in FOOTER_CITIES if k in CITY_BY_SLUG) + f' and <a href="{link("locations/")}" style="text-decoration:underline">more cities</a>'
    body = f"""
<section class="about-hero"><div class="wrap">
  <span class="eyebrow">About Hop To It Events</span>
  <h1>Big Ideas. <span class="pink">Unforgettable</span> Experiences.</h1>
  <p class="lede">Hop To It Events is a full-service event planning and production company creating memorable experiences for brands, businesses, organizations and communities. We&rsquo;ve been planning and executing events since 2010.</p>
  <p class="lede" style="margin-top:14px">From corporate celebrations and brand activations to food festivals and large-scale public events, we bring creativity, expertise and hands-on execution to every experience we produce.</p>
  <div class="about-media">
    {ph("Downtown street festival", "black", "border-radius:24px;min-height:400px", eager=True)}
    <div class="about-stats">
      <div style="background:var(--ink);color:#fff"><b>2010</b><span>Planning events since</span></div>
      <div style="background:var(--pink);color:#fff"><b>100+</b><span>Events produced</span></div>
      <div style="background:var(--gold)"><b>30+</b><span>U.S. markets</span></div>
    </div>
  </div>
</div></section>

<section style="padding-top:0"><div class="wrap pillars">
  <div class="pillar reveal"><h2 class="pill-h">Our Passion</h2><p>We believe great events bring people together, create meaningful connections and leave lasting impressions.</p></div>
  <div class="pillar reveal"><h2 class="pill-h">Our Approach</h2><p>Every event starts with a great idea. We combine creative planning, strategic partnerships and hands-on production to bring that idea to life.</p></div>
  <div class="pillar reveal"><h2 class="pill-h">Our Experience</h2><p>We&rsquo;ve been planning and executing events since 2010. Having produced events across the country, we understand what it takes to create engaging experiences, attract audiences, coordinate partners and execute successfully.</p></div>
</div></section>

<section class="dark"><div class="wrap">
  <div class="sec-head"><h2>Why Choose <span class="pink">Hop To It</span></h2></div>
  <div class="why">
    <div><h3>We&rsquo;re Event Creators, Not Just Event Planners</h3><p>We&rsquo;ve developed and produced our own signature event brands, giving us firsthand experience in every stage of event planning, marketing and execution.</p></div>
    <div><h3>Creative Ideas. Real-World Execution.</h3><p>From sourcing venues and coordinating vendors to managing logistics and event-day production, we know how to turn ambitious concepts into successful experiences.</p></div>
    <div><h3>Built Around Your Goals</h3><p>No two events are the same. We tailor every experience to your audience, objectives and budget, whether you&rsquo;re planning a private gathering or a large-scale public event.</p></div>
  </div>
</div></section>

<section id="at-a-glance"><div class="wrap">
  <h2 class="h2" style="margin-bottom:28px">Hop To It at a Glance</h2>
  <ul class="glance">
    <li><b>What we are</b><span>A full-service event planning and production company</span></li>
    <li><b>Experience</b><span>Planning and executing events since 2010</span></li>
    <li><b>Reach</b><span>100+ events produced in 30+ U.S. markets</span></li>
    <li><b>What we plan</b><span>{svc_links} and <a href="{link('services/')}" style="text-decoration:underline">more</a></span></li>
    <li><b>Signature events</b><span>15 original event brands, including Chef Battle, Donut Fest, Bartender Battle and Wing Fest</span></li>
    <li><b>Who we work with</b><span>Corporate teams, brands and agencies, cities and tourism organizations, property managers and nonprofits</span></li>
    <li><b>City pages</b><span>{city_links}</span></li>
    <li><b>Contact</b><span><a href="mailto:{EMAIL}" style="text-decoration:underline">{EMAIL}</a></span></li>
  </ul>
  <h3 style="font-size:24px;margin:48px 0 14px">Markets where we&rsquo;ve produced events</h3>
  <p class="lede" style="max-width:none">{", ".join(MARKETS)}.</p>
</div></section>

<section style="padding:56px 0 28px">
  {marquee("As seen in", PRESS, "cream", "press")}
</section>
<section style="padding:28px 0 72px"><div class="wrap">
  <h2 class="eyebrow muted" style="font-weight:400;margin-bottom:18px">Brands we&rsquo;ve worked with</h2>
  <ul class="brand-wall">{"".join(f"<li>{esc(b)}</li>" for b in BRANDS)}</ul>
</div></section>
"""
    crumbs = [("Home", ""), ("About Us", slug)]
    graph = [org(), website()] + webpage(url, title, desc, crumbs, "AboutPage")
    page(slug, title, desc, "about", body, graph)


# ------------------------------------------------------------------ plan
def plan_page():
    slug = "plan-your-event/"
    set_depth(slug)
    url = SITE + "/" + slug
    title = "Plan Your Event | Hop To It Events"
    desc = "Tell us about your corporate event, brand activation, festival, fundraiser or party. Hop To It Events will follow up with ideas and a plan."
    body = f"""
<div class="plan">
  <div class="plan-left">
    <span class="eyebrow gold">Get started</span>
    <h1>Let&rsquo;s Plan <span class="pink">Something</span></h1>
    <p class="lede">Have an event in mind? Tell us what you&rsquo;re planning, and we&rsquo;ll help bring it to life. Whether you have a fully developed concept or are just getting started, our team is ready to explore the possibilities.</p>
    <ol class="plan-steps">
      <li><h2>We&rsquo;ll Be in Touch</h2><p>Our team reviews your inquiry and follows up to learn more about your event.</p></li>
      <li><h2>Let&rsquo;s Talk Through the Details</h2><p>We&rsquo;ll discuss your goals, audience, budget, timing and what you want your event to accomplish.</p></li>
      <li><h2>We&rsquo;ll Build a Plan</h2><p>Based on your needs, we&rsquo;ll develop a customized event concept, scope and proposal.</p></li>
    </ol>
    <span class="eyebrow muted" style="margin-top:40px;color:#9AA0A7">Prefer email?</span>
    <a href="mailto:{EMAIL}" style="font-family:var(--head);font-size:24px;color:var(--pink)">{EMAIL}</a>
  </div>
  <div class="plan-right">
    {plan_form()}
  </div>
</div>
"""
    crumbs = [("Home", ""), ("Plan Your Event", slug)]
    graph = [org(), website()] + webpage(url, title, desc, crumbs, "ContactPage")
    page(slug, title, desc, "plan", body, graph, cta=False)


# ------------------------------------------------------------------ 404 + crawl files
def not_found():
    global _absolute, _depth
    _absolute, _depth = True, 0
    body = f"""<section class="dark hero"><div class="wrap">
  <span class="eyebrow">404</span>
  <h1>This Page Hopped <span class="pink">Away.</span></h1>
  <p class="lede">The page you&rsquo;re looking for doesn&rsquo;t exist or has moved.</p>
  <div class="hero-actions"><a class="btn btn-pink" href="{link()}">Go Home</a><a class="link-arrow" href="{link('services/')}">See our services &rarr;</a></div>
</div></section>"""
    page("404.html", "Page Not Found | Hop To It Events", "Page not found.", "", body, [org()],
         out="404.html", index=False)
    _absolute = False


def sitemap():
    paths = INDEXED + ["donutfestvegas.html"]
    urls = "".join(f"  <url><loc>{SITE}/{p}</loc><lastmod>{UPDATED}</lastmod></url>\n" for p in paths)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    print("wrote sitemap.xml", len(paths), "urls")


def robots():
    ai = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
          "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot",
          "Applebot", "DuckAssistBot", "Meta-ExternalAgent", "Amazonbot", "MistralAI-User"]
    blocks = "".join(f"User-agent: {b}\nAllow: /\n\n" for b in ai)
    (ROOT / "robots.txt").write_text(
        "# Search engines and AI assistants are welcome to crawl and cite this site.\n\n"
        "User-agent: *\nAllow: /\n\n" + blocks + f"Sitemap: {SITE}/sitemap.xml\n")
    print("wrote robots.txt")


def llms():
    lines = ["# Hop To It Events", "",
             f"> {ORG_DESC}", "",
             "Hop To It Events plans and produces events for clients and also creates, markets, tickets and runs its own "
             "signature event brands, which is its main difference from other event planners. "
             f"Contact: {EMAIL}. Inquiries: {SITE}/plan-your-event/", "",
             "## Key facts", "",
             "- Type: full-service event planning and production company",
             "- Experience: planning and executing events since 2010",
             "- Reach: 100+ events produced in 30+ U.S. markets",
             "- Signature event brands (15): " + ", ".join(EVENT_BRANDS),
             "- Clients: corporate HR, marketing and event teams; brands and agencies; cities, chambers and tourism "
             "organizations; shopping centers and property managers; nonprofits",
             "- Markets where events have been produced: " + ", ".join(MARKETS), "",
             "## Services", ""]
    for s in SERVICES:
        lines.append(f"- [{s['name']}]({SITE}/{s['slug']}/): {s['meta']}")
    lines += ["", "## Locations", ""]
    for c in CITIES:
        lines.append(f"- [{c['city']}]({SITE}/locations/{c['slug']}/): {c['hub']['meta']}")
        for p in c["pages"]:
            if p["phase"] <= PUBLISH_PHASE:
                lines.append(f"  - [{p['name']} in {c['city']}]({SITE}/locations/{c['slug']}/{p['slug']}/)")
    lines += ["", "## Pages", "",
              f"- [Home]({SITE}/): what Hop To It Events does and who it works with",
              f"- [All services]({SITE}/services/)",
              f"- [Signature events]({SITE}/events/): event brands, tickets, sponsorship, vendors, bringing an event to a new city",
              f"- [About]({SITE}/about/): company overview, press coverage, brands worked with, markets",
              f"- [Plan your event]({SITE}/plan-your-event/): inquiry form",
              f"- [Donut Fest Las Vegas sponsorship]({SITE}/donutfestvegas.html)", "",
              "## Upcoming events", "",
              f"- Donut Fest Las Vegas: Saturday, January 24, 2027, 12-5 PM. Tickets: {TICKETS_DONUT_FEST_LV}",
              f"- Chef Battle California Tour: January-March 2027 across 25 California markets. Details: {GCL}", ""]
    (ROOT / "llms.txt").write_text("\n".join(lines))
    print("wrote llms.txt")


if __name__ == "__main__":
    home(); services_hub()
    for s in SERVICES:
        service_page(s)
    locations_hub()
    for c in CITIES:
        city_hub(c)
        for p in c["pages"]:
            city_page(c, p)
    _city = None
    events(); about(); plan_page(); calculator_page(); not_found()
    sitemap(); robots(); llms()
    if MISSING_SHOTS:
        print('placeholders with no shot in photos.py:', sorted(MISSING_SHOTS))
