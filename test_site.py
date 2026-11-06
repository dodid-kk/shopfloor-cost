"""Browser test of the built site: every calculator's example output, URL state round-trip, reset, no JS errors, no overflow.

  python test_site.py            # tests ./docs via a local http server
"""
import functools
import http.server
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

DOCS = Path(__file__).parent / "docs"
EXPECT = {
    "landed-cost-calculator": ("lc-out", "$5.035"),
    "cost-per-good-unit-calculator": ("cg-out", "$4.849"),
    "machine-hour-rate-calculator": ("mh-out", "$14.67 / h"),
    "scrap-cost-calculator": ("sc-out", "$133,200"),
    "oee-calculator": ("oe-out", "74.8%"),
    "takt-time-calculator": ("tk-out", "43 s"),
    "margin-markup-calculator": ("pr-out", "$28.31"),
    "break-even-calculator": ("be-out", "2,667 units"),
    "equipment-payback-calculator": ("pb-out", "3.3 years"),
    "aql-sampling-calculator": ("aq-out", "80 units"),
    "compressed-air-leak-cost-calculator": ("al-out", "$11,520"),
    "freight-class-calculator": ("fc-out", "Class 100"),
    "cbm-container-calculator": ("cb-out", "24 m³"),
    "air-freight-chargeable-weight-calculator": ("ac-out", "90 kg"),
    "cpk-calculator": ("cp-out", "1.07"),
}
# (query string, element, expected) — AQL points checked against the ISO 2859-1 tables
EXTRA = [
    ("aql-sampling-calculator/?aq-lot=60", "aq-tbl", "Major · AQL 2.5\taccept 1 / reject 2\nMinor"),
    ("aql-sampling-calculator/?aq-lot=60", "aq-tbl", "Sample to pull (check all classes)	20 units"),
    ("aql-sampling-calculator/?aq-lot=40", "aq-tbl", "Major · AQL 2.5 · sample 5	accept 0 / reject 1"),
    ("aql-sampling-calculator/?aq-lot=5000&aq-major=1.5", "aq-tbl", "Major · AQL 1.5	accept 7 / reject 8"),
    ("aql-sampling-calculator/?aq-lot=70&aq-major=1.5", "aq-tbl", "Major · AQL 1.5 · sample 8	accept 0 / reject 1"),
    ("aql-sampling-calculator/?aq-lot=1000000", "aq-tbl", "Major · AQL 2.5 · sample 500	accept 21 / reject 22"),
    ("aql-sampling-calculator/?aq-fM=6", "aq-pill", "Fail: major 6 ≥ 6"),
    ("freight-class-calculator/?fc-wt=1700", "fc-out", "Class 60"),
    ("freight-class-calculator/?fc-wt=1000", "fc-out", "Class 70"),
    ("freight-class-calculator/?fc-wt=2000", "fc-out", "Class 55"),
    ("air-freight-chargeable-weight-calculator/?ac-div=5000", "ac-out", "108 kg"),
    ("air-freight-chargeable-weight-calculator/?ac-wt=30", "ac-out", "120 kg"),
    ("cpk-calculator/", "cp-sub", "about 688 ppm"),
    ("cbm-container-calculator/", "cb-pill", "Fits one 20ft container (86% full)"),
    ("cbm-container-calculator/?cb-n=100", "cb-pill", "Under 15 m³"),
    ("cbm-container-calculator/?cb-n=600", "cb-pill", "Fits one 40ft container"),
    ("freight-class-calculator/?fc-unit=cm&fc-l=120&fc-w=100&fc-h=120&fc-wt=227", "fc-out", "Class 100"),
]

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DOCS))
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8765), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
B = "http://127.0.0.1:8765/"
fails = []
with sync_playwright() as p:
    br = p.chromium.launch()
    for vw in (390, 1280):
        pg = br.new_page(viewport={"width": vw, "height": 900})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        for slug, (el, want) in EXPECT.items():
            pg.goto(B + slug + "/"); pg.wait_for_timeout(250)
            got = pg.locator("#" + el).inner_text()
            if got != want:
                fails.append(f"{vw} {slug}: {got!r} != {want!r}")
            if pg.evaluate("document.documentElement.scrollWidth") > vw:
                fails.append(f"{vw} {slug}: horizontal overflow")
            if pg.locator(".tools button").count() != 4:
                fails.append(f"{slug}: toolbar missing")
        if errs:
            fails.append(f"{vw} js errors: {errs}")
        pg.close()
    pg = br.new_page()
    for qs, el, want in EXTRA:
        pg.goto(B + qs); pg.wait_for_timeout(200)
        got = pg.locator("#" + el).inner_text()
        if want not in got:
            fails.append(f"{qs}: {want!r} not in {got!r}")
    # select state goes into the URL; menu and sticky bar exist
    pg.goto(B + "aql-sampling-calculator/"); pg.select_option("#aq-level", "3"); pg.wait_for_timeout(100)
    if "aq-level=3" not in pg.url:
        fails.append("select state not in URL: " + pg.url)
    if pg.locator("details.menu a").count() != len(EXPECT):
        fails.append(f"menu links {pg.locator('details.menu a').count()}")
    pg.set_viewport_size({"width": 390, "height": 800}); pg.goto(B + "machine-hour-rate-calculator/"); pg.wait_for_timeout(300)
    if not pg.locator(".stick.on").count():
        fails.append("sticky result bar not shown on phone")
    pg.click("[data-v='16']") if pg.locator("[data-v='16']").count() else None
    pg.goto(B + "compressed-air-leak-cost-calculator/"); pg.click(".presets button[data-v='16']"); pg.wait_for_timeout(100)
    if pg.input_value("#al-cfm") != "16":
        fails.append("preset chip did not fill")
    pg.goto(B); pg.fill(".finder", "aql"); pg.wait_for_timeout(100)
    if pg.locator(".cards a:not([hidden])").count() != 1:
        fails.append(f"finder shows {pg.locator('.cards a:not([hidden])').count()}")
    pg.set_viewport_size({"width": 1280, "height": 900})
    # URL state round-trip + reset
    pg.goto(B + "landed-cost-calculator/?lc-qty=10000&basis=fob&cur=EUR"); pg.wait_for_timeout(250)
    out = pg.locator("#lc-out").inner_text()
    if not out.startswith("€"):
        fails.append(f"state load currency: {out}")
    pg.fill("#lc-price", "5"); pg.wait_for_timeout(100)
    if "lc-price=5" not in pg.url:
        fails.append(f"state save: {pg.url}")
    pg.click(".tools button[data-a=reset]"); pg.wait_for_timeout(100)
    if pg.input_value("#lc-price") != "4.20":
        fails.append("reset failed")
    pg.goto(B + "equipment-payback-calculator/"); pg.wait_for_timeout(200)
    tbl = pg.locator("#pb-tbl").inner_text()
    if "IRR	23.6%" not in tbl:
        fails.append(f"IRR row: {tbl!r}")
    print("IRR row:", [l for l in tbl.splitlines() if "IRR" in l])
    for path in ["", "contact/", "about/", "privacy/"]:
        r = pg.goto(B + path)
        if r.status != 200:
            fails.append(f"{path} {r.status}")
    pg.goto(B); print("home categories:", pg.locator(".cat h2").all_inner_texts(), "cards", pg.locator(".cards a").count())
    pg.set_viewport_size({"width": 1280, "height": 900}); pg.screenshot(path=str(Path(__file__).parent / "shot_home2.png"), full_page=True)
    pg.goto(B + "oee-calculator/"); pg.screenshot(path=str(Path(__file__).parent / "shot_oee.png"))
    br.close()
srv.shutdown()
print("FAIL\n" + "\n".join(fails) if fails else "ALL PASS")
sys.exit(1 if fails else 0)
