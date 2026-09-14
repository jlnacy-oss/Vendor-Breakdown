# -*- coding: utf-8 -*-
import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)
from vendor_data import VENDORS

SHARED_CSS = open(os.path.join(SCRIPT_DIR, 'shared.css')).read()

def ownership_short(o):
    if "Public" in o: return "Public"
    if "cquir" in o: return "Acquired"
    if "ubsidiary" in o or "Product line" in o or "Platform of" in o: return "Subsidiary"
    return "Private"

def card(v):
    dash = "sand-technologies-dashboard.html" if v["slug"] == "sand-technologies" else f"{v['slug']}-dashboard.html"
    pdf = "Sand-Technologies-One-Sheet.pdf" if v["slug"] == "sand-technologies" else f"{v['slug']}-one-sheet.pdf"
    return f"""
      <div class="vcard">
        <div class="vcard-top">
          <a class="vcard-name" href="{v['website']}" target="_blank" rel="noopener">{v['name']} \u2197</a>
        </div>
        <div class="vcard-cat">{v['category']}</div>
        <div class="vcard-desc">{v['description']}</div>
        <div class="vcard-kpi">
          <div class="k-num">{v['revenue_short']}</div>
          <div class="k-lbl">Latest reported / estimated revenue</div>
        </div>
        <div class="vcard-actions">
          <a class="btn secondary" href="{dash}">Dashboard</a>
          <a class="btn secondary" href="{pdf}" download>PDF \u2193</a>
        </div>
      </div>"""

def matrix_row(v):
    dash = "sand-technologies-dashboard.html" if v["slug"] == "sand-technologies" else f"{v['slug']}-dashboard.html"
    return f"""
        <tr>
          <td class="mname"><a href="{dash}">{v['name']}</a></td>
          <td>{v['category']}</td>
          <td>{v['digital_twin']}</td>
          <td>{v['genai']}</td>
          <td>{ownership_short(v['ownership'])}</td>
          <td>{v['hq'].split(',')[0].split('(')[0].strip()}</td>
          <td>{v['revenue_short']}</td>
        </tr>"""

cards_html = "".join(card(v) for v in VENDORS)
rows_html = "".join(matrix_row(v) for v in VENDORS)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Physical AI / Industrial AI Market Landscape</title>
<style>
{SHARED_CSS}
</style>
</head>
<body>

<header class="hero">
  <div class="hero-inner">
    <div class="kicker"><span class="dot"></span>MARKET LANDSCAPE &nbsp;\u00b7&nbsp; SEPTEMBER 11, 2026</div>
    <h1>Physical AI &amp; Industrial AI for Critical Infrastructure</h1>
    <p class="tagline">Nine vendors competing to sense, model and act on the world's physical infrastructure \u2014 water, energy, telecom, industrial operations and government. Click any vendor to open its dashboard, or download its one-page PDF directly.</p>
    <div class="kpi-row">
      <div class="kpi"><div class="num">9</div><div class="lbl">Vendors tracked</div></div>
      <div class="kpi"><div class="num">1</div><div class="lbl">Public-market outlier (Palantir, $4.48B rev.)</div></div>
      <div class="kpi"><div class="num">1</div><div class="lbl">Recent $3.1B acquisition (Cognite \u2192 Schneider Electric)</div></div>
      <div class="kpi"><div class="num">3</div><div class="lbl">Vendors now inside larger conglomerates (AVEVA, Forge, Xcelerator)</div></div>
    </div>
  </div>
</header>

<div class="wrap">

  <section>
    <div class="sec-head"><span class="sec-num">01</span><h2>Vendors in this market</h2></div>
    <div class="sec-note">Vendor name links to the company's own website. Each card links to its full dashboard and its downloadable one-page PDF.</div>
    <div class="vendor-grid">{cards_html}
    </div>
  </section>

  <section>
    <div class="sec-head"><span class="sec-num">02</span><h2>What each vendor does &amp; offers</h2></div>
    <div class="sec-note">Vendor name links through to its dashboard. Figures are latest reported or best third-party estimate \u2014 many of the largest names here don't disclose this product line's revenue separately from their parent company.</div>
    <table class="matrix-table">
      <thead>
        <tr>
          <th style="width:15%;">Vendor</th>
          <th style="width:20%;">Category</th>
          <th style="width:15%;">Digital twin</th>
          <th style="width:13%;">Agentic / GenAI</th>
          <th style="width:10%;">Ownership</th>
          <th style="width:13%;">HQ</th>
          <th style="width:14%;">Revenue (latest/est.)</th>
        </tr>
      </thead>
      <tbody>{rows_html}
      </tbody>
    </table>
    <div class="callout" style="margin-top:18px;">
      <b>Reading this matrix:</b> the market splits into three tiers \u2014 independent platform companies still reporting their own numbers (Sand, Palantir, C3.ai, Bentley, Cognite pre-close), platforms newly folded into a much larger parent (AVEVA, about to absorb Cognite too), and platforms that are just one product line inside an industrial giant (IBM watsonx, Honeywell Forge, Siemens Xcelerator) where standalone economics aren't disclosed at all. Where a vendor sits in that structure matters as much as its technology for a PE evaluation \u2014 it determines whether you're assessing a standalone business or a feature of someone else's balance sheet.
    </div>
  </section>

  <footer>
    <b>Sources:</b> individual vendor dashboards and one-pagers (see each vendor page for full source lists) \u2014 company filings, fact sheets, Wikipedia, PitchBook/Crunchbase/Datanyze/BuiltIn profiles, and vendor press releases as of September 2026. Figures marked \u201cest.\u201d or \u201cnot disclosed\u201d are third-party estimates or unavailable, not company-confirmed \u2014 validate in diligence.
  </footer>

</div>
</body>
</html>
"""

out_path = os.path.join(ROOT_DIR, 'market-overview.html')
with open(out_path, 'w') as f:
    f.write(html)
# Also refresh index.html so GitHub Pages serves the overview at the repo root
with open(os.path.join(ROOT_DIR, 'index.html'), 'w') as f:
    f.write(html)
print("wrote market-overview.html and index.html")
