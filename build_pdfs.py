# -*- coding: utf-8 -*-
import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)
from vendor_data import VENDORS

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER

# ---------- palette (matches the dashboard: light grey page, white cards, dark ink text) ----------
NAVY      = colors.HexColor("#14161C")
STEEL     = colors.HexColor("#2B6684")
SAND      = colors.HexColor("#A5702B")
INK       = colors.HexColor("#14161C")
MUTED     = colors.HexColor("#5B6270")
LIGHT_BG  = colors.HexColor("#EFF0F3")
PANEL_BG  = colors.HexColor("#F5F6F8")
LINE      = colors.HexColor("#DCDFE4")
GREEN     = colors.HexColor("#1F7A4D")
GREEN_BG  = colors.HexColor("#E6F5EC")
RED       = colors.HexColor("#B23A2E")
RED_BG    = colors.HexColor("#FBEAE8")
WHITE     = colors.white

BASE_FONT = "Helvetica"
BASE_BOLD = "Helvetica-Bold"

styles = {}
styles["kicker"] = ParagraphStyle("kicker", fontName=BASE_BOLD, fontSize=7.6, leading=9.0, textColor=SAND)
styles["title"] = ParagraphStyle("title", fontName=BASE_BOLD, fontSize=19, leading=21, textColor=INK)
styles["subtitle"] = ParagraphStyle("subtitle", fontName=BASE_FONT, fontSize=9.3, leading=11.5, textColor=MUTED)
styles["h2"] = ParagraphStyle("h2", fontName=BASE_BOLD, fontSize=10.5, leading=12, textColor=NAVY)
styles["body"] = ParagraphStyle("body", fontName=BASE_FONT, fontSize=8.0, leading=10.2, textColor=INK)
styles["body_sm"] = ParagraphStyle("body_sm", fontName=BASE_FONT, fontSize=7.3, leading=9.3, textColor=INK)
styles["muted"] = ParagraphStyle("muted", fontName=BASE_FONT, fontSize=7.0, leading=9.0, textColor=MUTED)
styles["stat_num"] = ParagraphStyle("stat_num", fontName=BASE_BOLD, fontSize=10.5, leading=11.5, textColor=INK, alignment=TA_CENTER)
styles["stat_lbl"] = ParagraphStyle("stat_lbl", fontName=BASE_FONT, fontSize=5.9, leading=7.2, textColor=MUTED, alignment=TA_CENTER)
styles["src"] = ParagraphStyle("src", fontName=BASE_FONT, fontSize=6.0, leading=7.6, textColor=MUTED)

def para(text, style="body"):
    return Paragraph(text, styles[style])

def section_head(title, num):
    t = Table([[Paragraph(f'<font color="#A5702B">{num}</font>  {title}', styles["h2"])]], colWidths=[7.6*inch])
    t.setStyle(TableStyle([
        ("LINEBELOW", (0,0), (-1,-1), 1.0, INK),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
    ]))
    return t

def stat_box(num, label, width=1.26):
    # Fixed row heights so every KPI box in the row renders at the same height,
    # regardless of how many lines its own number/label happen to wrap to.
    inner = Table([[Paragraph(num, styles["stat_num"])], [Paragraph(label, styles["stat_lbl"])]],
                   colWidths=[width*inch], rowHeights=[26, 18])
    inner.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), WHITE),
        ("BOX", (0,0), (-1,-1), 0.6, LINE),
        ("VALIGN", (0,0), (0,0), "BOTTOM"),
        ("VALIGN", (0,1), (0,1), "TOP"),
        ("TOPPADDING", (0,0), (0,0), 2),
        ("BOTTOMPADDING", (0,0), (0,0), 1),
        ("TOPPADDING", (0,1), (0,1), 2),
        ("BOTTOMPADDING", (0,1), (0,1), 2),
        ("LEFTPADDING", (0,0), (-1,-1), 3),
        ("RIGHTPADDING", (0,0), (-1,-1), 3),
        ("LINEABOVE", (0,0), (-1,0), 1.6, SAND),
    ]))
    return inner

def chip_line(items):
    return " \u00b7 ".join(items)

def bullets(items):
    return "<br/>".join("\u2022 " + i for i in items)

def build_pdf(v, out_path):
    doc = SimpleDocTemplate(out_path, pagesize=letter,
                             leftMargin=0.42*inch, rightMargin=0.42*inch,
                             topMargin=0, bottomMargin=0.06*inch)
    story = []
    gd = v["glassdoor"]

    # ---- Header ----
    header_inner = Table(
        [[Paragraph(f"VENDOR ONE-SHEET &nbsp;\u00b7&nbsp; {v['category'].upper()} &nbsp;\u00b7&nbsp; SEPTEMBER 11, 2026", styles["kicker"])],
         [Paragraph(v["name"], styles["title"])],
         [Paragraph(v["tagline"] + f' &nbsp;\u00b7&nbsp; <a href="{v["website"]}" color="#2B6684">{v["website"].replace("https://","")}</a>', styles["subtitle"])]],
        colWidths=[7.66*inch]
    )
    header_inner.setStyle(TableStyle([
        ("TOPPADDING", (0,0), (-1,0), 5), ("BOTTOMPADDING", (0,0), (-1,0), 1),
        ("TOPPADDING", (0,1), (-1,1), 1), ("BOTTOMPADDING", (0,1), (-1,1), 1),
        ("TOPPADDING", (0,2), (-1,2), 2), ("BOTTOMPADDING", (0,2), (-1,2), 4),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("BACKGROUND", (0,0), (-1,-1), WHITE),
        ("BOX", (0,0), (-1,-1), 0.6, LINE),
    ]))
    story.append(header_inner)
    story.append(Table([[""]], colWidths=[8.5*inch], rowHeights=[2.4], style=TableStyle([("BACKGROUND",(0,0),(-1,-1), SAND)])))
    story.append(Spacer(1, 5))

    ownership_short = ("Public" if "Public" in v["ownership"] else
                        ("Acquired" if "cquir" in v["ownership"] else
                         ("Subsidiary" if ("ubsidiary" in v["ownership"] or "Product line" in v["ownership"] or "Platform of" in v["ownership"]) else "Private")))
    stats = [
        stat_box(__import__("re").search(r"\d{4}", v["founded"]).group(), "Founded"),
        stat_box("Not disclosed" if v["employees"].startswith("Not disclosed") else v["employees"].split(" ")[0], "Employees"),
        stat_box(v["revenue_short"], "Revenue (latest/est.)"),
        stat_box(ownership_short, "Ownership"),
        stat_box(f"{gd['rating']}/5", f"Glassdoor ({gd['reviews']})"),
        stat_box(v["digital_twin"].split(" ")[0], "Digital twin"),
    ]
    stat_row = Table([stats], colWidths=[1.276*inch]*6, hAlign="LEFT")
    stat_row.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),2), ("RIGHTPADDING",(0,0),(-1,-1),2),
                                   ("TOPPADDING",(0,0),(-1,-1),0), ("BOTTOMPADDING",(0,0),(-1,-1),0)]))
    story.append(stat_row)
    story.append(Spacer(1, 6))

    # ---- 01 Overview ----
    left = [para(v["description"], "body_sm"), Spacer(1,3), para(f"<b>Offering:</b> {v['offering']}", "body_sm")]
    people_line = " \u00b7 ".join(f"{p['name']} ({p['title']})" for p in v["people"])
    right = [
        para("<b>Key facts</b>", "body_sm"), Spacer(1,1),
        para(f"<b>HQ:</b> {v['hq']}", "body_sm"), Spacer(1,1),
        para(f"<b>Ownership:</b> {v['ownership']}", "body_sm"), Spacer(1,1),
        para(f"<b>Revenue:</b> {v['revenue']}", "body_sm"), Spacer(1,1),
        para(f'<b>Web:</b> <a href="{v["website"]}" color="#2B6684">{v["website"].replace("https://","")}</a> &nbsp;\u00b7&nbsp; <a href="{v["linkedin"]}" color="#2B6684">LinkedIn</a>', "body_sm"), Spacer(1,1),
        para(f"<b>Key people:</b> {people_line}", "body_sm"), Spacer(1,1),
        para(f"<b>Digital twin:</b> {v['digital_twin']} &nbsp;\u00b7&nbsp; <b>GenAI:</b> {v['genai']}", "body_sm"),
    ]
    snap = Table([[left, right]], colWidths=[4.5*inch, 3.16*inch])
    snap.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"), ("LEFTPADDING",(1,0),(1,0),12),
                               ("LINEBEFORE",(1,0),(1,0),0.6,LINE)]))
    story.append(section_head("Overview", "01"))
    story.append(snap)
    story.append(Spacer(1, 5))

    # ---- 03 Use cases (top 3) ----
    uc_data = [[para("<b>Sector</b>","body_sm"), para("<b>Deployment</b>","body_sm"), para("<b>Reported impact</b>","body_sm"), para("<b>Source</b>","body_sm")]]
    for uc in v["use_cases"][:3]:
        uc_data.append([para(uc["sector"],"body_sm"), para(uc["deployment"],"body_sm"), para(uc["impact"],"body_sm"),
                         para(f'<a href="{uc["source"]}" color="#2B6684">Link</a>', "body_sm")])
    uc_table = Table(uc_data, colWidths=[0.9*inch, 2.05*inch, 3.51*inch, 1.2*inch])
    uc_table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0), WHITE), ("TEXTCOLOR",(0,0),(-1,0), MUTED),
        ("FONTNAME",(0,0),(-1,0), BASE_BOLD), ("FONTSIZE",(0,0),(-1,0), 6.8),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),2.2), ("BOTTOMPADDING",(0,0),(-1,-1),2.2),
        ("LEFTPADDING",(0,0),(-1,-1),5),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, PANEL_BG]),
        ("LINEBELOW",(0,0),(0,0),1,INK),
        ("LINEBELOW",(0,1),(-1,-1),0.4,LINE),
        ("BOX",(0,0),(-1,-1),0.6,LINE),
    ]))
    story.append(section_head("Use Cases &amp; Reported Metrics", "02"))
    story.append(uc_table)
    story.append(Spacer(1, 5))

    # ---- 04 Competitive landscape ----
    comp_rows = [v2["name"] for v2 in VENDORS if v2["slug"] != v["slug"]]
    story.append(section_head("Competitive Landscape", "03"))
    story.append(para(f"<b>Other vendors in this market:</b> {chip_line(comp_rows)}", "body_sm"))
    story.append(Spacer(1,3))
    story.append(para(f"<b>Where it sits:</b> {v['position_note']}", "body_sm"))
    story.append(Spacer(1, 5))

    # ---- 05 Sentiment ----
    story.append(section_head("Sentiment", "04"))
    story.append(para(f"<b>Customer:</b> {v['customer_sentiment']}", "body_sm"))
    story.append(Spacer(1,4))

    sent_header = Table([[para('<font color="#1F7A4D"><b>What supports the story</b></font>',"body_sm"),
                           para('<font color="#B23A2E"><b>What to pressure-test</b></font>',"body_sm")]],
                         colWidths=[3.83*inch, 3.83*inch])
    sent_header.setStyle(TableStyle([("BOTTOMPADDING",(0,0),(-1,-1),3)]))
    sent_body = Table([[para(bullets(v["sentiment_bull"]), "body_sm"), para(bullets(v["sentiment_bear"]), "body_sm")]],
                       colWidths=[3.83*inch, 3.83*inch])
    sent_body.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("BACKGROUND",(0,0),(0,0), GREEN_BG), ("BACKGROUND",(1,0),(1,0), RED_BG),
        ("BOX",(0,0),(0,0),0.6,LINE), ("BOX",(1,0),(1,0),0.6,LINE),
        ("TOPPADDING",(0,0),(-1,-1),4), ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),8), ("RIGHTPADDING",(0,0),(-1,-1),8),
        ("LINEBEFORE",(1,0),(1,0),0.6,LIGHT_BG),
    ]))
    story.append(sent_header)
    story.append(sent_body)
    story.append(Spacer(1,4))
    story.append(para(f"<b>Employee:</b> {v['employee_sentiment']}", "body_sm"))
    story.append(Spacer(1, 5))

    # ---- Sources ----
    story.append(HRFlowable(width="100%", thickness=0.5, color=LINE))
    story.append(Spacer(1,2))
    src_text = (f"Sources: {v['name']} public filings/website, company fact sheets, Wikipedia, PitchBook/Crunchbase/Datanyze/BuiltIn "
                f"profiles, Glassdoor employer reviews, vendor case studies and press releases as of Sept. 2026. Figures marked "
                f"\u201cest.\u201d or \u201cnot disclosed\u201d are third-party estimates or unavailable \u2014 not company-confirmed \u2014 validate in "
                f"diligence. Part of the Physical AI / Industrial AI for Critical Infrastructure market landscape.")
    story.append(para(src_text, "src"))

    def paint_bg(canvas, doc_):
        canvas.saveState()
        canvas.setFillColor(LIGHT_BG)
        canvas.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
        canvas.restoreState()

    doc.build(story, onFirstPage=paint_bg, onLaterPages=paint_bg)

if __name__ == "__main__":
    import subprocess
    for v in VENDORS:
        if v["slug"] == "sand-technologies":
            continue
        out = os.path.join(ROOT_DIR, f"{v['slug']}-one-sheet.pdf")
        build_pdf(v, out)
        pages = subprocess.run(["python3","-c",
            f"from pypdf import PdfReader; print(len(PdfReader('{out}').pages))"],
            capture_output=True, text=True).stdout.strip()
        print(out, "-> pages:", pages)
