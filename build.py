"""Build the static site into ./site.

  python build.py                      # BASE_URL defaults to the GitHub Pages address
  BASE_URL=https://shopfloorcost.com/ python build.py   # after the domain is connected

All internal links are relative, so the same output works on a sub-path (GitHub Pages) and on a domain root.
"""
from __future__ import annotations

import html
import json
import os
import shutil
from datetime import date
from pathlib import Path

from content import PRIVACY
from content_pages import ABOUT, TERMS
from content import PAGES as _BASE_PAGES
from content_v2 import CATEGORY as _CAT2, CONTACT, NEW_PAGES
from content_v3 import CATEGORY_V3, ORDER_V3 as CATEGORY_ORDER, PAGES_V3, RENAME
from content_v4 import CATEGORY_V4, PAGES_V4
CATEGORY = {k: RENAME.get(v, v) for k, v in {**_CAT2, **CATEGORY_V3, **CATEGORY_V4}.items()}

_ALL = _BASE_PAGES + NEW_PAGES + PAGES_V3 + PAGES_V4
PAGES = sorted(_ALL, key=lambda p: (CATEGORY_ORDER.index(CATEGORY[p["slug"]]), _ALL.index(p)))
REVIEWED = date.today().strftime("%B %Y")

ROOT = Path(__file__).parent
OUT = ROOT / "docs"
BASE = os.getenv("BASE_URL", "https://everysolver.com/").rstrip("/") + "/"
SECTIONS = json.loads((ROOT / "src" / "sections.json").read_text(encoding="utf-8"))
TODAY = date.today().isoformat()
ADSENSE_CLIENT = os.getenv("ADSENSE_CLIENT", "")
CF_BEACON = os.getenv("CF_BEACON", "6ed43d34957a49fcb90ec8e43f7db523")  # Cloudflare Web Analytics (cookieless, public token)  # ca-pub-XXXX once approved; empty = no ad script

CURRENCY = """<label class="cur" for="cur">Currency
      <select id="cur">
        <option value="USD">USD $</option><option value="EUR">EUR €</option><option value="GBP">GBP £</option>
        <option value="JPY">JPY ¥</option><option value="KRW">KRW ₩</option>
      </select>
    </label>"""


def _cat_id(cat: str) -> str:
    return "c-" + "".join(ch for ch in cat.lower() if ch.isalnum())


def head(title: str, desc: str, path: str, depth: int, extra: str = "") -> str:
    up = "../" * depth
    ads = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" '
           'crossorigin="anonymous"></script>') if ADSENSE_CLIENT else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{BASE}{path}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}{path}">
<link rel="icon" href="{up}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="{up}icon-192.png">
<link rel="apple-touch-icon" href="{up}apple-touch-icon.png">
<meta property="og:image" content="{BASE}icon-512.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@500;600;700&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap">
<link rel="stylesheet" href="{up}assets/style.css">
{ads}{extra}
{('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=' + chr(39) + '{"token": "' + CF_BEACON + '"}' + chr(39) + '></script>') if CF_BEACON else ''}
</head>
<body>
<div class="wrap">"""


def top(depth: int, current: str = "", show_currency: bool = True) -> str:
    up = "../" * depth
    groups = ""
    for cat in CATEGORY_ORDER:
        links = "".join(f'<a href="{up}{p["slug"]}/"' + (' aria-current="page"' if p["slug"] == current else "") + f'>{html.escape(p["nav"])}</a>'
                        for p in PAGES if CATEGORY[p["slug"]] == cat)
        if links:
            groups += f'<div><h3>{html.escape(cat)}</h3>{links}</div>'
    nav = f'<details class="menu"><summary>All calculators ({len(PAGES)})</summary><nav class="menu-panel" aria-label="Calculators">{groups}</nav></details>'
    return f"""
  <header class="top">
    <div>
      <div class="brand"><a href="{up or './'}">Every<span>Solver</span></a></div>
      <div class="tag">Free calculators that solve real work problems · manufacturing &amp; cost</div>
    </div>
    {CURRENCY if show_currency else ''}
  </header>
  {nav}"""


def foot(depth: int, script: bool = True) -> str:
    up = "../" * depth
    js = f'<script src="{up}assets/calc.js"></script>' if script else ""
    return f"""
  <footer>
    <span>Estimates for planning only. Confirm duty rates and tax rules with your customs broker or accountant.</span>
    <span><a href="{up}about/">About</a> · <a href="{up}contact/">Contact</a> · <a href="{up}privacy/">Privacy</a> · <a href="{up}terms/">Terms</a> · EverySolver</span>
  </footer>
</div>
{js}
</body>
</html>
"""


def ad_slot() -> str:
    return '' if not ADSENSE_CLIENT else (
        f'<ins class="adsbygoogle" style="display:block;margin:22px 0" data-ad-client="{ADSENSE_CLIENT}" data-ad-format="auto" '
        'data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({});</script>')


def calc_page(p: dict) -> str:
    sec = SECTIONS[p["section"]].replace('<div class="ad">AD SLOT · 728×90 / responsive</div>', ad_slot())
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}
    app_ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": p["title"].split(" – ")[0].split(" | ")[0],
              "url": f"{BASE}{p['slug']}/", "applicationCategory": "BusinessApplication", "operatingSystem": "Any",
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    crumb_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Calculators", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": CATEGORY[p["slug"]], "item": f"{BASE}#{_cat_id(CATEGORY[p['slug']])}"},
        {"@type": "ListItem", "position": 3, "name": p["nav"], "item": f"{BASE}{p['slug']}/"}]}
    ld = (f'<script type="application/ld+json">{json.dumps(app_ld)}</script>\n'
          f'<script type="application/ld+json">{json.dumps(faq_ld)}</script>\n'
          f'<script type="application/ld+json">{json.dumps(crumb_ld)}</script>')
    guide = "".join(f"<h2>{html.escape(h)}</h2>{body}" for h, body in p["guide"])
    faq = "".join(f"<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>" for q, a in p["faq"])
    related = "".join(f'<a href="../{o["slug"]}/"><b>{html.escape(o["nav"])}</b><span>{html.escape(o["blurb"])}</span></a>'
                      for o in PAGES if o["slug"] != p["slug"])
    return (head(p["title"], p["description"], f'{p["slug"]}/', 1, ld) + top(1, p["slug"])
            + f'\n  <p class="crumbs"><a href="../">Calculators</a> › <a href="../#{_cat_id(CATEGORY[p["slug"]])}">{html.escape(CATEGORY[p["slug"]])}</a> › {html.escape(p["nav"])}</p>'
            + f'\n  <section class="sheet" id="v-{p["section"]}">{sec}<div class="print-url">{BASE}{p["slug"]}/</div></section>'
            + f'\n  <article class="guide"><p class="reviewed">Reviewed {REVIEWED}. Formulas are shown above the guide. <a href="../contact/">Report an error or request a calculator</a>.</p>{guide}<h2>Frequently asked questions</h2>{faq}'
            + f'<h2>More calculators</h2><div class="related">{related}</div></article>' + foot(1))


FINDER_JS = """<script>(function(){var f=document.querySelector(".finder");if(!f)return;
f.addEventListener("input",function(){var q=f.value.trim().toLowerCase();
document.querySelectorAll(".cards a").forEach(function(a){a.hidden=q&&a.textContent.toLowerCase().indexOf(q)<0;});
document.querySelectorAll(".cat").forEach(function(c){c.hidden=!c.querySelector(".cards a:not([hidden])");});});})();</script>"""


def index_page() -> str:
    cards = ""
    for cat in CATEGORY_ORDER:
        items = "".join(f'<a href="{p["slug"]}/"><b>{html.escape(p["nav"])}</b><span>{html.escape(p["blurb"])}</span></a>'
                        for p in PAGES if CATEGORY[p["slug"]] == cat)
        cards += f'<div class="cat" id="{_cat_id(cat)}"><h2>{html.escape(cat)}</h2><div class="cards" style="margin-top:6px">{items}</div></div>'
    body = f"""
  <section class="hero">
    <h1>Manufacturing cost calculators</h1>
    <p class="lede">Quick, transparent answers to the cost questions that come up on the shop floor and in purchasing: what an imported part really costs, what a machine hour costs, how efficient a line is, how much scrap costs a year, what to charge, how many units to inspect, how full a container will be, what air freight will bill and whether a machine pays for itself. Every calculator shows its formula, runs in your browser and gives you a link you can share with the numbers filled in.</p>
    <input class="finder" type="search" placeholder="Find a calculator… (e.g. OEE, freight, margin)" aria-label="Find a calculator">
    {cards}
    <p class="reviewed">Missing a calculator you need? <a href="contact/">Tell us</a>; requests that come up often are built first.</p>
  </section>"""
    return head("Free Manufacturing Cost Calculators | EverySolver",
                "Free calculators for landed cost, machine hour rate, OEE, takt time, scrap cost, margin, break-even and equipment payback. Formulas shown.",
                "", 0) + top(0, show_currency=False) + body + FINDER_JS + foot(0, script=False)


def text_page(slug: str, title: str, desc: str, inner: str) -> str:
    return (head(title, desc, f"{slug}/", 1) + top(1, show_currency=False)
            + f'\n  <article class="guide" style="border-top:1px solid var(--line);margin-top:0">{inner}</article>' + foot(1, script=False))


def build() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    shutil.copy(ROOT / "src" / "style.css", OUT / "assets" / "style.css")
    shutil.copy(ROOT / "src" / "calc.js", OUT / "assets" / "calc.js")
    for f in (ROOT / "src" / "static").iterdir():
        shutil.copy(f, OUT / f.name)
    (OUT / "index.html").write_text(index_page(), encoding="utf-8")
    urls = [BASE]
    for p in PAGES:
        d = OUT / p["slug"]; d.mkdir()
        (d / "index.html").write_text(calc_page(p), encoding="utf-8")
        urls.append(f"{BASE}{p['slug']}/")
    for slug, title, desc, inner in [
        ("about", "About – EverySolver", "Who makes EverySolver and how the calculators work.", ABOUT),
        ("privacy", "Privacy Policy – EverySolver", "Privacy policy for EverySolver.", PRIVACY.replace("{date}", TODAY)),
        ("contact", "Contact – EverySolver", "Report an error or request a new manufacturing calculator.", CONTACT),
        ("terms", "Terms of Use – EverySolver", "Terms of use for EverySolver calculators.", TERMS.replace("{date}", TODAY)),
    ]:
        d = OUT / slug; d.mkdir()
        (d / "index.html").write_text(text_page(slug, title, desc, inner), encoding="utf-8")
        urls.append(f"{BASE}{slug}/")
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
    (OUT / "404.html").write_text(text_page("404", "Page not found – EverySolver", "Page not found.",
                                            f'<h1>Page not found</h1><p><a href="{BASE}">Go to the calculators</a></p>'), encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    host = BASE.split("//", 1)[1].strip("/")
    if "github.io" not in host:  # custom domain for GitHub Pages
        (OUT / "CNAME").write_text(host + "\n", encoding="utf-8")
    if ADSENSE_CLIENT:
        (OUT / "ads.txt").write_text(f"google.com, {ADSENSE_CLIENT.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n", encoding="utf-8")
    print(f"built {len(urls)} pages → {OUT} (BASE {BASE})")


if __name__ == "__main__":
    build()
