# Shopfloor/Cost

Free English manufacturing cost calculators (landed cost, cost per good unit, scrap & rework, break-even, equipment payback).

- Edit text in `content.py`, calculator markup in `src/sections.json`, logic in `src/calc.js`, styles in `src/style.css`.
- Build: `python build.py` → `docs/` (served by GitHub Pages).
- After buying the domain: `BASE_URL=https://<domain>/ python build.py`, add `docs/CNAME`, point DNS to GitHub Pages.
- After AdSense approval: `ADSENSE_CLIENT=ca-pub-... python build.py` (adds ad script, ad units and ads.txt).
