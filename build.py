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

from content import ABOUT, PAGES, PRIVACY

ROOT = Path(__file__).parent
OUT = ROOT / "docs"
BASE = os.getenv("BASE_URL", "https://dodid-kk.github.io/shopfloor-cost/").rstrip("/") + "/"
SECTIONS = json.loads((ROOT / "src" / "sections.json").read_text(encoding="utf-8"))
TODAY = date.today().isoformat()
ADSENSE_CLIENT = os.getenv("ADSENSE_CLIENT", "")  # ca-pub-XXXX once approved; empty = no ad script

CURRENCY = """<label class="cur" for="cur">Currency
      <select id="cur">
        <option value="USD">USD $</option><option value="EUR">EUR €</option><option value="GBP">GBP £</option>
        <option value="JPY">JPY ¥</option><option value="KRW">KRW ₩</option>
      </select>
    </label>"""


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
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' rx='3' fill='%23c2410c'/%3E%3Cpath d='M4 12V4h3a2 2 0 010 4H4m5 4l3-8' stroke='white' stroke-width='1.6' fill='none'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@500;600;700&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap">
<link rel="stylesheet" href="{up}assets/style.css">
{ads}{extra}
</head>
<body>
<div class="wrap">"""


def top(depth: int, current: str = "", show_currency: bool = True) -> str:
    up = "../" * depth
    nav = "".join(
        f'<a href="{up}{p["slug"]}/"' + (' aria-current="page"' if p["slug"] == current else "") + f'>{html.escape(p["nav"])}</a>'
        for p in PAGES)
    return f"""
  <header class="top">
    <div>
      <div class="brand"><a href="{up or './'}">Shopfloor<span>/</span>Cost</a></div>
      <div class="tag">Free cost calculators for manufacturers, importers and small makers</div>
    </div>
    {CURRENCY if show_currency else ''}
  </header>
  <nav class="site-nav" aria-label="Calculators">{nav}</nav>"""


def foot(depth: int, script: bool = True) -> str:
    up = "../" * depth
    js = f'<script src="{up}assets/calc.js"></script>' if script else ""
    return f"""
  <footer>
    <span>Estimates for planning only. Confirm duty rates and tax rules with your customs broker or accountant.</span>
    <span><a href="{up}about/">About</a> · <a href="{up}privacy/">Privacy</a> · Shopfloor/Cost</span>
  </footer>
</div>
{js}
</body>
</html>
"""


def ad_slot() -> str:
    return '<div class="ad" aria-hidden="true">Advertisement</div>' if not ADSENSE_CLIENT else (
        f'<ins class="adsbygoogle" style="display:block;margin:22px 0" data-ad-client="{ADSENSE_CLIENT}" data-ad-format="auto" '
        'data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({});</script>')


def calc_page(p: dict) -> str:
    sec = SECTIONS[p["section"]].replace('<div class="ad">AD SLOT · 728×90 / responsive</div>', ad_slot())
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}
    app_ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": p["title"].split(" – ")[0].split(" | ")[0],
              "url": f"{BASE}{p['slug']}/", "applicationCategory": "BusinessApplication", "operatingSystem": "Any",
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    ld = (f'<script type="application/ld+json">{json.dumps(app_ld)}</script>\n'
          f'<script type="application/ld+json">{json.dumps(faq_ld)}</script>')
    guide = "".join(f"<h2>{html.escape(h)}</h2>{body}" for h, body in p["guide"])
    faq = "".join(f"<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>" for q, a in p["faq"])
    related = "".join(f'<a href="../{o["slug"]}/"><b>{html.escape(o["nav"])}</b><span>{html.escape(o["blurb"])}</span></a>'
                      for o in PAGES if o["slug"] != p["slug"])
    return (head(p["title"], p["description"], f'{p["slug"]}/', 1, ld) + top(1, p["slug"])
            + f'\n  <section class="sheet" id="v-{p["section"]}">{sec}</section>'
            + f'\n  <article class="guide">{guide}<h2>Frequently asked questions</h2>{faq}'
            + f'<h2>More calculators</h2><div class="related">{related}</div></article>' + foot(1))


def index_page() -> str:
    cards = "".join(f'<a href="{p["slug"]}/"><b>{html.escape(p["nav"])}</b><span>{html.escape(p["blurb"])}</span></a>' for p in PAGES)
    body = f"""
  <section class="hero">
    <h1>Manufacturing cost calculators</h1>
    <p class="lede">Quick, transparent answers to the cost questions that come up on the shop floor and in purchasing: what an imported part really costs, what poor yield adds to every unit, how much scrap costs a year, when a product breaks even and whether a machine pays for itself. Every calculator shows its formula and runs in your browser.</p>
    <div class="cards">{cards}</div>
  </section>"""
    return head("Free Manufacturing Cost Calculators – Landed Cost, Yield, Scrap, Break-Even, Payback",
                "Free manufacturing cost calculators: landed cost with CIF/FOB duty, cost per good unit, scrap and rework cost, break-even and equipment payback.",
                "", 0) + top(0, show_currency=False) + body + foot(0, script=False)


def text_page(slug: str, title: str, desc: str, inner: str) -> str:
    return (head(title, desc, f"{slug}/", 1) + top(1, show_currency=False)
            + f'\n  <article class="guide" style="border-top:1px solid var(--line);margin-top:0">{inner}</article>' + foot(1, script=False))


def build() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    shutil.copy(ROOT / "src" / "style.css", OUT / "assets" / "style.css")
    shutil.copy(ROOT / "src" / "calc.js", OUT / "assets" / "calc.js")
    (OUT / "index.html").write_text(index_page(), encoding="utf-8")
    urls = [BASE]
    for p in PAGES:
        d = OUT / p["slug"]; d.mkdir()
        (d / "index.html").write_text(calc_page(p), encoding="utf-8")
        urls.append(f"{BASE}{p['slug']}/")
    for slug, title, desc, inner in [
        ("about", "About – Shopfloor/Cost", "Who makes Shopfloor/Cost and how the calculators work.", ABOUT),
        ("privacy", "Privacy Policy – Shopfloor/Cost", "Privacy policy for Shopfloor/Cost.", PRIVACY.replace("{date}", TODAY)),
    ]:
        d = OUT / slug; d.mkdir()
        (d / "index.html").write_text(text_page(slug, title, desc, inner), encoding="utf-8")
        urls.append(f"{BASE}{slug}/")
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
    (OUT / "404.html").write_text(text_page("404", "Page not found – Shopfloor/Cost", "Page not found.",
                                            f'<h1>Page not found</h1><p><a href="{BASE}">Go to the calculators</a></p>'), encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    if ADSENSE_CLIENT:
        (OUT / "ads.txt").write_text(f"google.com, {ADSENSE_CLIENT.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n", encoding="utf-8")
    print(f"built {len(urls)} pages → {OUT} (BASE {BASE})")


if __name__ == "__main__":
    build()
