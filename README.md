# Physical AI / Industrial AI Market Landscape

A static site + downloadable PDFs profiling nine vendors competing to sense, model,
and act on physical infrastructure (water, energy, telecom, industrial operations,
government). September 2026.

**Live structure:** one overview page (`index.html` / `market-overview.html`) links
out to nine vendor dashboards, each with a matching one-page PDF you can download
straight from the dashboard.

---

## What's in this repo

```
index.html                        ← copy of market-overview.html (GitHub Pages root)
market-overview.html              ← the hub: vendor cards + capability matrix
sand-technologies-dashboard.html  ← hand-maintained (see note below)
palantir-dashboard.html
c3ai-dashboard.html
cognite-dashboard.html
bentley-systems-dashboard.html
aveva-dashboard.html
ibm-watsonx-dashboard.html
honeywell-forge-dashboard.html
siemens-xcelerator-dashboard.html

Sand-Technologies-One-Sheet.pdf   ← hand-maintained (see note below)
palantir-one-sheet.pdf
c3ai-one-sheet.pdf
cognite-one-sheet.pdf
bentley-systems-one-sheet.pdf
aveva-one-sheet.pdf
ibm-watsonx-one-sheet.pdf
honeywell-forge-one-sheet.pdf
siemens-xcelerator-one-sheet.pdf

scripts/
  vendor_data.py            ← single source of truth for 8 of the 9 vendors
  shared.css                ← shared stylesheet for every dashboard + overview page
  build_dashboards.py       ← generates the 8 vendor *-dashboard.html files
  build_pdfs.py             ← generates the 8 vendor *-one-sheet.pdf files
  build_overview.py         ← generates market-overview.html + index.html
  build_sand_onesheet.py    ← generates Sand-Technologies-One-Sheet.pdf only
```

**Every file must stay in one flat folder.** All the links between pages
(dashboard ↔ overview, dashboard → PDF, vendor name → company website) are
relative paths that assume everything sits side by side — the same way GitHub
Pages serves a repo.

### The Sand Technologies exception

Sand's dashboard and PDF were built first, by hand, before the other eight vendors
existed as a data-driven pipeline — they carry more research depth (Glassdoor
detail, disaster-response case study, etc.) than a first pass on a new vendor
would. They are **not** generated from `vendor_data.py`; editing that file will
not change Sand's files. Update `sand-technologies-dashboard.html` directly (it's
plain HTML) and `scripts/build_sand_onesheet.py` (then re-run it) if Sand's facts
change. Sand *is* included as an entry at the top of `vendor_data.py` purely so
the other eight vendors' "Competitive Landscape" sections can list it correctly —
don't edit the fields below `"has_full_dashboard": True` expecting them to flow
into Sand's own page.

---

## How to regenerate everything with fresh data

### 1. Set up once

You need Python 3 with a couple of packages:

```bash
pip install reportlab pypdf --break-system-packages
```

(`reportlab` builds the PDFs; `pypdf` is only used to sanity-check page counts.)

### 2. Update the data

Open `scripts/vendor_data.py`. It's a Python list called `VENDORS`, one dict per
company, with fields like:

```python
{
    "slug": "palantir",                  # used in filenames — keep it URL-safe
    "name": "Palantir Technologies",
    "website": "https://www.palantir.com",
    "linkedin": "https://www.linkedin.com/company/palantir-technologies",
    "category": "...",
    "tagline": "...",
    "founded": "...", "hq": "...", "employees": "...",
    "ownership": "...", "revenue": "...", "revenue_short": "...",
    "offering": "...",
    "digital_twin": "...", "genai": "...", "buyer": "...",
    "customers": [...],
    "people": [{"name": "...", "title": "..."}, ...],
    "description": "...",
    "position_note": "...",
    "glassdoor": {"rating": "...", "reviews": "...", "recommend": "...",
                  "outlook": "...", "ceo_approval": "..."},
    "use_cases": [
        {"sector": "...", "deployment": "...", "impact": "...",
         "status": "Deployed", "source": "https://..."},
        ...
    ],
    "sentiment_bull": [...],
    "sentiment_bear": [...],
    "customer_sentiment": "...",
    "employee_sentiment": "...",
},
```

Edit the fields you have new numbers for. A few things that will bite you if you
skip them:

- **Escape ampersands.** Write `&amp;` not `&` anywhere in a text field — it feeds
  straight into both HTML and a ReportLab PDF, and a bare `&` breaks the PDF
  build. Same goes for arrow characters like `→` — ReportLab's base font can't
  render them and shows a black box instead; spell it out ("leading to",
  "increased from X to Y") rather than using the glyph.
- **Keep KPI-row values short.** The `founded`, `employees`, `revenue_short`,
  `ownership`, and `glassdoor` values get displayed as compact stat-box numbers
  and labels. Long strings there cause uneven box heights or wrapped text in the
  PDF — put the detail in `revenue`, `ownership`, etc. (the prose fields) instead,
  and keep the `_short` / KPI-facing fields to a few words.
- **Use case sources are real URLs**, not decorative — they're the actual link
  behind "Source ↗" on the dashboard and "Link" in the PDF table. If you don't
  have a clean source URL, link to the vendor's general newsroom/case-studies
  page rather than leaving it blank.

### 3. Add a new vendor (optional)

Copy an existing dict in `VENDORS`, give it a new `"slug"`, and fill in every
field. No other code changes are needed — the build scripts loop over whatever
is in `VENDORS`. You will also want to add it manually to any vendor's
`"position_note"` or the overview's intro text if you want it referenced by name
in prose elsewhere (the auto-generated "Other vendors in this market" list
updates itself; the hand-written prose paragraphs don't).

### 4. Run the build

From the repo root:

```bash
python3 scripts/build_overview.py     # → index.html, market-overview.html
python3 scripts/build_dashboards.py   # → 8 vendor *-dashboard.html files
python3 scripts/build_pdfs.py         # → 8 vendor *-one-sheet.pdf files
python3 scripts/build_sand_onesheet.py  # → Sand-Technologies-One-Sheet.pdf
```

Each script prints what it wrote. `build_pdfs.py` and `build_sand_onesheet.py`
also print a page count for each PDF — every one should say `pages: 1`. If a PDF
comes back at 2 pages after you've added content, the layout has overflowed; the
fix is almost always to shorten the new text, not to fight the page break (see
"Keeping PDFs to one page" below).

Sand's dashboard (`sand-technologies-dashboard.html`) is not touched by any
script — edit it directly if Sand's facts change.

### 5. Check your work

```bash
python3 - <<'EOF'
from html.parser import HTMLParser
import glob

class Checker(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack = []; self.ok = True; self.errs = []
    def handle_starttag(self, tag, attrs):
        if tag not in {'meta','link','br','img','input','hr'}:
            self.stack.append(tag)
    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            self.ok = False; self.errs.append((tag, self.stack[-3:]))
        else:
            self.stack.pop()

for path in sorted(glob.glob('*.html')):
    c = Checker(); c.feed(open(path).read())
    print(path, '->', 'OK' if c.ok and not c.stack else (c.errs, c.stack))
EOF
```

This catches unclosed tags — the most common thing that goes wrong when editing
HTML by hand (usually a missing `</div>`). It should print `OK` for every file.

Then eyeball at least one regenerated dashboard and one PDF before pushing —
open them in a browser / PDF viewer and skim for anything that looks off.

### 6. Push to GitHub

Commit everything — the HTML/PDF files at the root *and* the `scripts/` folder —
and push. If GitHub Pages is enabled on the repo, it will serve `index.html` at
the root automatically. Nothing else to configure.

---

## Design notes (useful context if you're editing by hand)

- **Palette:** light grey page background (`#EFF0F3`), white cards, dark ink text
  (`#14161C`), a sand/ochre accent (`#A5702B`) and steel-blue accent (`#2B6684`).
  Defined once as CSS variables in `scripts/shared.css` for the dashboards, and
  duplicated as Python color constants at the top of each PDF-building script
  (ReportLab can't read a CSS file). If you change the palette, update both
  places.
- **Section structure is deliberately identical across every vendor:** Company
  Snapshot → Use Cases & Reported Metrics → Competitive Landscape → Sentiment.
  There's no dedicated "Ratings" section (removed by request) — the Glassdoor
  score still shows as a single KPI tile in the header of each page.
- **Keeping PDFs to one page:** each PDF script uses fixed-height KPI stat boxes
  and fairly tight paragraph/table padding tuned to just barely fit one page.
  Adding a 4th or 5th use case, a long new sentence in `position_note`, etc. can
  push a PDF to 2 pages. If that happens, trim the new text first; only touch
  the padding/spacer values in the script as a last resort, and re-check every
  other vendor's page count afterward since padding changes are global to the
  script, not per-vendor.
- **Figures are estimates where noted.** Revenue, employee counts, and Glassdoor
  data for the 8 non-Sand vendors were gathered from public sources (company
  filings where available, otherwise PitchBook/Crunchbase/Datanyze/BuiltIn and
  similar) as of September 2026, not verified against primary financial
  statements in every case. Treat anything marked "est." or "not disclosed" as a
  starting point for diligence, not a confirmed number.
