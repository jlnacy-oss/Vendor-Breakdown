# -*- coding: utf-8 -*-
"""
Sand Technologies — Vendor One-Sheet
Built with reportlab platypus.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import glob
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)

# ---------- palette (aligned with the companion dashboard: light grey page, white cards, dark ink text) ----------
NAVY      = colors.HexColor("#14161C")   # dark ink — used for headings/rules, NOT as a fill anymore
STEEL     = colors.HexColor("#2B6684")   # steel blue accent
SAND      = colors.HexColor("#A5702B")   # sand/ochre accent (brand tie-in)
INK       = colors.HexColor("#14161C")
MUTED     = colors.HexColor("#5B6270")
LIGHT_BG  = colors.HexColor("#EFF0F3")   # page background (light grey)
PANEL_BG  = colors.HexColor("#F5F6F8")   # secondary surface / zebra stripe
LINE      = colors.HexColor("#DCDFE4")   # hairline border
GREEN     = colors.HexColor("#1F7A4D")
GREEN_BG  = colors.HexColor("#E6F5EC")
AMBER     = colors.HexColor("#8A5B10")
RED       = colors.HexColor("#B23A2E")
RED_BG    = colors.HexColor("#FBEAE8")
WHITE     = colors.white

# ---------- fonts (fallback to Helvetica family; try to register a serif for headlines) ----------
BASE_FONT = "Helvetica"
BASE_BOLD = "Helvetica-Bold"

styles = {}
styles["kicker"] = ParagraphStyle("kicker", fontName=BASE_BOLD, fontSize=8.0, leading=9.5,
                                   textColor=SAND, spaceAfter=2, tracking=0)
styles["title"] = ParagraphStyle("title", fontName=BASE_BOLD, fontSize=21, leading=23,
                                  textColor=INK, spaceAfter=2)
styles["subtitle"] = ParagraphStyle("subtitle", fontName=BASE_FONT, fontSize=10.5, leading=13,
                                     textColor=MUTED)
styles["h2"] = ParagraphStyle("h2", fontName=BASE_BOLD, fontSize=11.5, leading=13,
                               textColor=NAVY, spaceBefore=0, spaceAfter=5)
styles["body"] = ParagraphStyle("body", fontName=BASE_FONT, fontSize=8.2, leading=10.3,
                                 textColor=INK)
styles["body_sm"] = ParagraphStyle("body_sm", fontName=BASE_FONT, fontSize=7.1, leading=8.6,
                                    textColor=INK)
styles["muted"] = ParagraphStyle("muted", fontName=BASE_FONT, fontSize=7.3, leading=9.4,
                                  textColor=MUTED)
styles["stat_num"] = ParagraphStyle("stat_num", fontName=BASE_BOLD, fontSize=12.5, leading=13.5,
                                     textColor=INK, alignment=TA_CENTER)
styles["stat_lbl"] = ParagraphStyle("stat_lbl", fontName=BASE_FONT, fontSize=6.3, leading=7.8,
                                     textColor=MUTED, alignment=TA_CENTER)
styles["tag"] = ParagraphStyle("tag", fontName=BASE_BOLD, fontSize=7, leading=9,
                                textColor=WHITE, alignment=TA_CENTER)
styles["src"] = ParagraphStyle("src", fontName=BASE_FONT, fontSize=6.0, leading=7.6,
                                textColor=MUTED)

def para(text, style="body"):
    return Paragraph(text, styles[style])

def section_head(title, num):
    t = Table(
        [[Paragraph(f'<font color="#C8934A">{num}</font>  {title}', styles["h2"])]],
        colWidths=[7.1*inch]
    )
    t.setStyle(TableStyle([
        ("LINEBELOW", (0,0), (-1,-1), 1.1, NAVY),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
    ]))
    return t

def stat_box(num, label, width=1.68):
    # Fixed row heights so every KPI box renders at the same height regardless
    # of how many lines its own number/label happen to wrap to.
    inner = Table([[Paragraph(num, styles["stat_num"])], [Paragraph(label, styles["stat_lbl"])]],
                   colWidths=[width*inch], rowHeights=[18, 20])
    inner.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), WHITE),
        ("BOX", (0,0), (-1,-1), 0.6, LINE),
        ("VALIGN", (0,0), (0,0), "BOTTOM"),
        ("VALIGN", (0,1), (0,1), "TOP"),
        ("TOPPADDING", (0,0), (0,0), 2),
        ("BOTTOMPADDING", (0,0), (0,0), 1),
        ("TOPPADDING", (0,1), (0,1), 2),
        ("BOTTOMPADDING", (0,1), (0,1), 2),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("LINEABOVE", (0,0), (-1,0), 2, SAND),
    ]))
    return inner

doc = SimpleDocTemplate(
    os.path.join(ROOT_DIR, "Sand-Technologies-One-Sheet.pdf"),
    pagesize=letter,
    leftMargin=0.45*inch, rightMargin=0.45*inch,
    topMargin=0, bottomMargin=0.02*inch,
)

story = []

# ===================== HEADER BAND =====================
header_inner = Table(
    [[Paragraph("VENDOR ONE-SHEET &nbsp;·&nbsp; SEPTEMBER 11, 2026", styles["kicker"])],
     [Paragraph("Sand Technologies", styles["title"])],
     [Paragraph('"Physical AI" operating system for critical infrastructure &nbsp;—&nbsp; water, energy, telecom, health &amp; government &nbsp;·&nbsp; sandtech.com', styles["subtitle"])]],
    colWidths=[7.5*inch]
)
header_inner.setStyle(TableStyle([
    ("TOPPADDING", (0,0), (-1,0), 5),
    ("BOTTOMPADDING", (0,0), (-1,0), 2),
    ("TOPPADDING", (0,1), (-1,1), 2),
    ("BOTTOMPADDING", (0,1), (-1,1), 2),
    ("TOPPADDING", (0,2), (-1,2), 3),
    ("BOTTOMPADDING", (0,2), (-1,2), 4),
    ("LEFTPADDING", (0,0), (-1,-1), 4),
    ("BACKGROUND", (0,0), (-1,-1), WHITE),
    ("BOX", (0,0), (-1,-1), 0.6, LINE),
]))
story.append(header_inner)

# thin sand accent rule under header
story.append(Table([[""]], colWidths=[8.5*inch], rowHeights=[3],
                    style=TableStyle([("BACKGROUND",(0,0),(-1,-1), SAND)])))
story.append(Spacer(1, 1))

# ===================== SNAPSHOT STAT ROW =====================
stats = [
    stat_box("2023", "Founded", width=1.02),
    stat_box("~500–680", "Employees", width=1.02),
    stat_box("18+", "Countries deployed", width=1.02),
    stat_box("12+", "Named clients (public)", width=1.02),
    stat_box("$15–67M", "Est. revenue (3rd-party)", width=1.02),
    stat_box("3.6 / 5", "Glassdoor (47)", width=1.02),
    stat_box("B–", "Simplify rating", width=1.02),
]
stat_row = Table([stats], colWidths=[1.02*inch]*7, hAlign="LEFT")
stat_row.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),3), ("RIGHTPADDING",(0,0),(-1,-1),3),
                               ("TOPPADDING",(0,0),(-1,-1),0), ("BOTTOMPADDING",(0,0),(-1,-1),0)]))
story.append(stat_row)
story.append(Spacer(1, 1))

# ===================== 01 COMPANY SNAPSHOT + LEADERSHIP =====================
snap_left = [
    para("<b>Product:</b> Symmetri — a real-time \u201cPhysical AI\u201d control layer that models physical assets/networks and acts on them (vs. dashboards/analytics alone). Applied across water, energy, telecom, health and government operations.", "body_sm"),
    Spacer(1,1),
    para("<b>Footprint:</b> Engineering &amp; delivery across Silicon Valley, Paris, Romania, Latin America and Africa; registered HQ entity in Mauritius; opened a formal U.S. commercial presence with a New York launch event, June 2025.", "body_sm"),
    Spacer(1,1),
    para("<b>Lineage:</b> Grew out of a decade-plus of AI/data consulting work; merged with ExploreAI (Feb 2024); heritage entity distinct from the unrelated 1980s-founded \u201cSAND Technology\u201d (Canada, columnar database).", "body_sm"),
    Spacer(1,1),
    para("<b>Leadership:</b> Founder/CEO Fred Swaniker — Stanford MBA, ex-McKinsey; also founder of African Leadership Group / ALX (talent pipeline of 300,000+ trained professionals feeding Sand's hiring). TIME 100 (2019, 2023 Impact Award), WEF Young Global Leader, TED Fellow.", "body_sm"),
]
snap_right = [
    para("<b>Selected clients &amp; partners</b>", "body_sm"),
    para("AWS (Advanced Tier partner) · GE · JP Morgan · Thames Water (UK) · Telkomsel (Indonesia) · Envision Racing / Formula E · Cassava Technologies (GPU-as-a-service MoU) · Compass UOL", "body_sm"),
    Spacer(1,1),
    para("<b>Ownership / funding</b>", "body_sm"),
    para("Backed in part by the Bestseller Foundation; total funding not publicly disclosed (PitchBook lists no reported round). Structured largely as a project/subscription services business, not VC-metric SaaS.", "body_sm"),
    Spacer(1,1),
    para('<b>Web:</b> <a href="https://www.sandtech.com" color="#2B6684">Link</a> &nbsp;\u00b7&nbsp; <a href="https://www.linkedin.com/company/sand-technologies" color="#2B6684">LinkedIn</a>', "body_sm"),
    Spacer(1,1),
    para("<b>Key people:</b> Fred Swaniker (Founder &amp; CEO) \u00b7 Danai Mavunga (COO) \u00b7 David Bratt (CFO)", "body_sm"),
]
snap_table = Table([[snap_left, snap_right]], colWidths=[4.35*inch, 2.85*inch])
snap_table.setStyle(TableStyle([
    ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("LEFTPADDING",(1,0),(1,0),14),
    ("LINEBEFORE",(1,0),(1,0),0.6,LINE),
]))
story.append(section_head("Company Snapshot", "01"))
story.append(snap_table)
story.append(Spacer(1, 1))

# ===================== 03 USE CASES =====================
uc_data = [
    [para("<b>Sector</b>","body_sm"), para("<b>Deployment</b>","body_sm"), para("<b>Reported impact</b>","body_sm"), para("<b>Source</b>","body_sm")],
    [para("Water utilities","body_sm"), para("Thames Water (UK) — predictive network management","body_sm"),
     para("Vendor describes moving the utility from reactive to predictive management; no standalone quantified result published","body_sm"),
     para('<a href="https://www.sandtech.com/water-utilities/" color="#2B6684">Link</a>',"body_sm")],
    [para("Telecom","body_sm"), para("Telkomsel (Indonesia) network optimization; AWS Marketplace “AI-Driven Network Planner” (Bedrock + SageMaker) for site investment","body_sm"),
     para("+8–15% data traffic, +5–8% coverage, $10–50M annual value at Telkomsel — without new infrastructure","body_sm"),
     para('<a href="https://www.sandtech.com/telecommunications/" color="#2B6684">Link</a>',"body_sm")],
    [para("Health","body_sm"), para("Rural clinic network, Africa","body_sm"),
     para("Connects thousands of rural clinics into one coordinated-care network serving millions of patients","body_sm"),
     para('<a href="https://www.sandtech.com/health/" color="#2B6684">Link</a>',"body_sm")],
    [para("Disaster response","body_sm"), para("Post-tornado city response — Symmetri damage-assessment layer","body_sm"),
     para("~5,400 damaged structures mapped, ~$0.8B in estimated losses prioritized for recovery resources","body_sm"),
     para('<a href="https://aws.amazon.com/marketplace/pp/prodview-ae2fh6326bbpi" color="#2B6684">Link</a>',"body_sm")],
]
uc_table = Table(uc_data, colWidths=[0.85*inch, 2.35*inch, 3.06*inch, 0.94*inch])
uc_table.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), WHITE),
    ("TEXTCOLOR",(0,0),(-1,0), MUTED),
    ("FONTNAME",(0,0),(-1,0), BASE_BOLD),
    ("FONTSIZE",(0,0),(-1,0), 7.2),
    ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("TOPPADDING",(0,0),(-1,-1),1.4),
    ("BOTTOMPADDING",(0,0),(-1,-1),1.4),
    ("LEFTPADDING",(0,0),(-1,-1),6),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, PANEL_BG]),
    ("LINEBELOW",(0,0),(0,0),1,INK),
    ("LINEBELOW",(0,1),(-1,-1),0.4,LINE),
    ("BOX",(0,0),(-1,-1),0.6,LINE),
    ("TEXTCOLOR",(3,1),(3,-1), GREEN),
    ("FONTNAME",(3,1),(3,-1), BASE_BOLD),
    ("FONTSIZE",(3,1),(3,-1), 7.4),
]))
story.append(section_head("Use Cases & Reported Metrics", "02"))
story.append(para("All impact figures below are vendor- or partner-reported and have not been independently audited.", "muted"))
story.append(Spacer(1,1))
story.append(uc_table)
story.append(Spacer(1, 1))

# ===================== 04 COMPETITIVE LANDSCAPE =====================
comp_left = [
    para("<b>Direct — industrial / physical-AI platforms</b>", "body_sm"),
    para("Palantir (Foundry / Gotham / AIP) · C3.ai · Cognite · IBM watsonx · Bentley Systems (iTwin / AssetWise) · AVEVA · Honeywell Forge · Siemens Xcelerator", "body_sm"),
]
comp_right = [
    para("<b>Adjacent</b>", "body_sm"),
    para("Global IT-services / AI consultancies (Globant, Endava) and Africa talent-to-tech delivery peers (Andela) compete for the same services budget, if not the same platform category.", "body_sm"),
]
comp_table = Table([[comp_left, comp_right]], colWidths=[4.35*inch, 2.85*inch])
comp_table.setStyle(TableStyle([
    ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("LEFTPADDING",(1,0),(1,0),14),
    ("LINEBEFORE",(1,0),(1,0),0.6,LINE),
]))
story.append(section_head("Competitive Landscape", "03"))
story.append(comp_table)
story.append(Spacer(1,1.3))
story.append(para("<b>Positioning:</b> Sand markets a new \u201cPhysical AI\u201d category — sensing, modeling and directly acting on infrastructure, vs. dashboards/analytics. Palantir and C3.ai are the closest comparables by ambition; Cognite, Bentley and AVEVA are closer on the digital-twin angle. Sand's edge is emerging-market delivery reach (ALX talent pipeline, Cassava GPU access); its risk is being a smaller, services-heavy player among better-capitalized platform vendors — echoed in its own C differentiation score above.", "body_sm"))
story.append(Spacer(1, 1))

# ===================== 04 GIP & BLACKROCK CONNECTIONS =====================
story.append(section_head("GIP &amp; BlackRock Connections", "04"))
story.append(para("GIP became a wholly-owned BlackRock subsidiary in October 2024 and now operates as BlackRock's dedicated infrastructure-investment arm. Stakes below are standard institutional/index-fund positions unless otherwise noted.", "muted"))
story.append(Spacer(1,1))
gb_data = [
    [para("<b>Entity</b>","body_sm"), para("<b>Possible connection</b>","body_sm")],
    [para("Global Infrastructure Partners","body_sm"),
     para("No direct connection found. Sand is privately held with no disclosed GIP investment, and none of Sand's named customers appear on GIP's own portfolio-company list (airports, ports, rail, data centers, water/waste and energy assets).","body_sm")],
    [para("BlackRock","body_sm"),
     para("No equity or ownership connection found. There is a real indirect link worth flagging: Sand's flagship water-utilities customer, Thames Water, has BlackRock as one of the senior creditor bondholders (with Aberdeen, Elliott Management, Apollo, M&amp;G and Silver Point Capital) in the ~\u00a317B debt restructuring on track to hand ownership of Thames Water to its creditors. If that completes as proposed, BlackRock becomes a part-owner of a Sand customer — a deal-contingent link, not a current relationship.","body_sm")],
]
gb_table = Table(gb_data, colWidths=[1.5*inch, 5.7*inch])
gb_table.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), WHITE), ("TEXTCOLOR",(0,0),(-1,0), MUTED),
    ("FONTNAME",(0,0),(-1,0), BASE_BOLD), ("FONTSIZE",(0,0),(-1,0), 7.2),
    ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("TOPPADDING",(0,0),(-1,-1),1.2), ("BOTTOMPADDING",(0,0),(-1,-1),1.2),
    ("LEFTPADDING",(0,0),(-1,-1),6),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, PANEL_BG]),
    ("LINEBELOW",(0,0),(0,0),1,INK),
    ("LINEBELOW",(0,1),(-1,-1),0.4,LINE),
    ("BOX",(0,0),(-1,-1),0.6,LINE),
]))
story.append(gb_table)
story.append(Spacer(1, 0.5))

# ===================== 05 SENTIMENT =====================
bull = [
    "High-profile founder (TIME 100, WEF Young Global Leader, TED Fellow) drives press and government access; Aug 2026 \u201cEvolve\u201d summit drew 300+ leaders",
    "AWS Advanced Tier partner status + Compass UOL partnership broaden enterprise channel reach",
    "Warm public reception at 2025 U.S. launch, incl. on-record praise from NYC's CTO",
    "Deployments claimed across 18+ countries with \u201czero mission-critical failures\u201d (vendor claim, unaudited)",
]
bear = [
    "Headcount down ~6% (6-mo) / ~9% (2-yr) per Simplify tracking, despite a growth narrative",
    "Revenue concentration in large infrastructure clients, which creates project-delay risk if deployments slip",
    "Cassava GPU-access agreement is a non-binding MoU; employee reviews cite frequent strategy pivots and an \u201cunclear product offering\u201d",
    "Analyst-rated C on Differentiation — crowded field vs. Palantir, C3.ai, Cognite, Bentley, AVEVA",
]
bull_paras = [para("&#8226; " + b, "body_sm") for b in bull]
bear_paras = [para("&#8226; " + b, "body_sm") for b in bear]

sent_header = Table([[para('<font color="#1F7A4D"><b>What supports the story</b></font>',"body_sm"),
                       para('<font color="#B23A2E"><b>What to pressure-test</b></font>',"body_sm")]],
                     colWidths=[3.6*inch, 3.6*inch])
sent_header.setStyle(TableStyle([("BOTTOMPADDING",(0,0),(-1,-1),4)]))

sent_body = Table([[bull_paras, bear_paras]], colWidths=[3.6*inch, 3.6*inch])
sent_body.setStyle(TableStyle([
    ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("BACKGROUND",(0,0),(0,0), GREEN_BG),
    ("BACKGROUND",(1,0),(1,0), RED_BG),
    ("BOX",(0,0),(0,0),0.6,LINE),
    ("BOX",(1,0),(1,0),0.6,LINE),
    ("TOPPADDING",(0,0),(-1,-1),2),
    ("BOTTOMPADDING",(0,0),(-1,-1),2),
    ("LEFTPADDING",(0,0),(-1,-1),9),
    ("RIGHTPADDING",(0,0),(-1,-1),9),
    ("LINEBEFORE",(1,0),(1,0),0.6,LIGHT_BG),
]))

story.append(section_head("Sentiment", "05"))
story.append(para("<b>Customer:</b> No independent review presence: Sand Symmetri's AWS Marketplace listing shows zero submitted reviews, and there is no active G2/Capterra/TrustRadius profile. What exists is vendor-published case studies with metrics but no verbatim customer quotes.", "body_sm"))
story.append(Spacer(1,1))
story.append(sent_header)
story.append(sent_body)
story.append(Spacer(1,1))
story.append(para("<b>Employee:</b> Praise for mission, talent and pace of delivery; recurring complaints about frequent strategic pivots, an unclear product offering, and meeting load.", "body_sm"))

# ===================== SOURCES =====================
story.append(HRFlowable(width="100%", thickness=0.5, color=LINE))
story.append(Spacer(1,1))
src_text = ("Sources: sandtech.com · Glassdoor · Simplify.jobs · PitchBook &amp; Crunchbase · AWS Marketplace listing "
            "· FF News/Hypertext/EA Business Times (Cassava MoU) · Wikipedia · IoT For All, ZoomInfo &amp; BuiltIn · "
            "ITV/AOL/Reuters (Thames Water restructuring) · BlackRock/GIP disclosures. Vendor/partner-reported as of Sept. 2026, not independently verified.")
story.append(para(src_text, "src"))

def paint_bg(canvas, doc_):
    canvas.saveState()
    canvas.setFillColor(LIGHT_BG)
    canvas.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
    canvas.restoreState()

doc.build(story, onFirstPage=paint_bg, onLaterPages=paint_bg)
print("done")
