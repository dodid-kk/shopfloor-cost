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
}

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
