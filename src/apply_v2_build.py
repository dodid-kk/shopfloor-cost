from pathlib import Path

p = Path(__file__).parent.parent / "build.py"
s = p.read_text(encoding="utf-8")


def rep(old, new):
    global s
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new)


rep('from content import ABOUT, PAGES, PRIVACY\n',
    'from content import ABOUT, PRIVACY\nfrom content import PAGES as _BASE_PAGES\nfrom content_v2 import CATEGORY, CATEGORY_ORDER, CONTACT, NEW_PAGES\n\n'
    '_ALL = _BASE_PAGES + NEW_PAGES\n'
    'PAGES = sorted(_ALL, key=lambda p: (CATEGORY_ORDER.index(CATEGORY[p["slug"]]), _ALL.index(p)))\n'
    'REVIEWED = date.today().strftime("%B %Y")\n')
# hide the ad placeholder until AdSense is approved
rep('''    return '<div class="ad" aria-hidden="true">Advertisement</div>' if not ADSENSE_CLIENT else (''',
    '''    return '' if not ADSENSE_CLIENT else (''')
# breadcrumbs, reviewed line, print url, breadcrumb JSON-LD
rep('''    ld = (f'<script type="application/ld+json">{json.dumps(app_ld)}</script>\\n'
          f'<script type="application/ld+json">{json.dumps(faq_ld)}</script>')''',
    '''    crumb_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Calculators", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": CATEGORY[p["slug"]], "item": f"{BASE}#{_cat_id(CATEGORY[p['slug']])}"},
        {"@type": "ListItem", "position": 3, "name": p["nav"], "item": f"{BASE}{p['slug']}/"}]}
    ld = (f'<script type="application/ld+json">{json.dumps(app_ld)}</script>\\n'
          f'<script type="application/ld+json">{json.dumps(faq_ld)}</script>\\n'
          f'<script type="application/ld+json">{json.dumps(crumb_ld)}</script>')''')
rep('''            + f'\\n  <section class="sheet" id="v-{p["section"]}">{sec}</section>'
            + f'\\n  <article class="guide">{guide}<h2>Frequently asked questions</h2>{faq}\'''',
    '''            + f'\\n  <p class="crumbs"><a href="../">Calculators</a> › <a href="../#{_cat_id(CATEGORY[p["slug"]])}">{html.escape(CATEGORY[p["slug"]])}</a> › {html.escape(p["nav"])}</p>'
            + f'\\n  <section class="sheet" id="v-{p["section"]}">{sec}<div class="print-url">{BASE}{p["slug"]}/</div></section>'
            + f'\\n  <article class="guide"><p class="reviewed">Reviewed {REVIEWED}. Formulas are shown above the guide. <a href="../contact/">Report an error or request a calculator</a>.</p>{guide}<h2>Frequently asked questions</h2>{faq}\'''')
# homepage grouped by category
rep('''    cards = "".join(f'<a href="{p["slug"]}/"><b>{html.escape(p["nav"])}</b><span>{html.escape(p["blurb"])}</span></a>' for p in PAGES)''',
    '''    cards = ""
    for cat in CATEGORY_ORDER:
        items = "".join(f'<a href="{p["slug"]}/"><b>{html.escape(p["nav"])}</b><span>{html.escape(p["blurb"])}</span></a>'
                        for p in PAGES if CATEGORY[p["slug"]] == cat)
        cards += f'<div class="cat" id="{_cat_id(cat)}"><h2>{html.escape(cat)}</h2><div class="cards" style="margin-top:6px">{items}</div></div>\'''')
rep('''    <div class="cards">{cards}</div>''', '''    {cards}
    <p class="reviewed">Missing a calculator you need? <a href="contact/">Tell us</a>; requests that come up often are built first.</p>''')
rep('''    <p class="lede">Quick, transparent answers to the cost questions that come up on the shop floor and in purchasing: what an imported part really costs, what poor yield adds to every unit, how much scrap costs a year, when a product breaks even and whether a machine pays for itself. Every calculator shows its formula and runs in your browser.</p>''',
    '''    <p class="lede">Quick, transparent answers to the cost questions that come up on the shop floor and in purchasing: what an imported part really costs, what a machine hour costs, how efficient a line is, how much scrap costs a year, what to charge and whether a machine pays for itself. Every calculator shows its formula, runs in your browser and gives you a link you can share with the numbers filled in.</p>''')
rep('''    return head("Free Manufacturing Cost Calculators – Landed Cost, Yield, Scrap, Break-Even, Payback",
                "Free manufacturing cost calculators: landed cost with CIF/FOB duty, cost per good unit, scrap and rework cost, break-even and equipment payback.",''',
    '''    return head("Free Manufacturing Cost Calculators – Landed Cost, Machine Rate, OEE, Pricing, Payback",
                "Free manufacturing cost calculators: landed cost, cost per good unit, machine hour rate, scrap cost, OEE, takt time, margin and markup, break-even and equipment payback.",''')
# contact page + footer link
rep('''        ("privacy", "Privacy Policy – Shopfloor/Cost", "Privacy policy for Shopfloor/Cost.", PRIVACY.replace("{date}", TODAY)),''',
    '''        ("privacy", "Privacy Policy – Shopfloor/Cost", "Privacy policy for Shopfloor/Cost.", PRIVACY.replace("{date}", TODAY)),
        ("contact", "Contact – Shopfloor/Cost", "Report an error or request a new manufacturing calculator.", CONTACT),''')
rep('''<a href="{up}about/">About</a> · <a href="{up}privacy/">Privacy</a> · Shopfloor/Cost''',
    '''<a href="{up}about/">About</a> · <a href="{up}contact/">Contact</a> · <a href="{up}privacy/">Privacy</a> · Shopfloor/Cost''')
rep('''def head(title''', '''def _cat_id(cat: str) -> str:
    return "c-" + "".join(ch for ch in cat.lower() if ch.isalnum())


def head(title''')
p.write_text(s, encoding="utf-8")
print("build.py patched")
