"""WaiveLabs design system — Brand Guide v1 (Sora/Inter, Ocean Blue, Sunset Orange).
Tokens sourced from agency/_templates/engagement-docs/gen_proposal.js and the live site CSS."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether, CondPageBreak)
from reportlab.lib.enums import TA_LEFT

BLUE   = HexColor("#317FF5")  # Ocean Blue (primary)
ORANGE = HexColor("#E65100")  # Sunset Orange (accent)
INK    = HexColor("#0F172A")  # Near Black
MIST   = HexColor("#EAF1FB")  # Mist Gray
MIST2  = HexColor("#F4F7FD")  # lighter mist (site token) — alternating rows
GRAY   = HexColor("#64748B")
BORDER = HexColor("#DCE6F5")
NAVY   = HexColor("#0A1530")  # site deep navy
WHITE  = HexColor("#FFFFFF")

F = "/tmp/fonts"
LOGO = f"{F}/wl-logo-clean.png"
pdfmetrics.registerFont(TTFont("Sora",          f"{F}/Sora-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sora-Medium",   f"{F}/Sora-Medium.ttf"))
pdfmetrics.registerFont(TTFont("Sora-SemiBold", f"{F}/Sora-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("Sora-Bold",     f"{F}/Sora-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sora-ExtraBold",f"{F}/Sora-ExtraBold.ttf"))
pdfmetrics.registerFont(TTFont("Inter",         f"{F}/Inter-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Medium",  f"{F}/Inter-Medium.ttf"))
pdfmetrics.registerFont(TTFont("Inter-SemiBold",f"{F}/Inter-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Bold",    f"{F}/Inter-Bold.ttf"))

PAGE_W, PAGE_H = letter
MARGIN = 0.95 * inch

# ---- Per-engagement config. The build script overrides these before make_doc(). ----
CLIENT = "<CLIENT>"                 # e.g. "Summer Fridays" — used in running header
COVER = {
    "draft":        "DRAFT V0.1   ·   MONTH YEAR   ·   CONFIDENTIAL — PREPARED FOR <CLIENT>",
    "title":        "<Engagement Title>",      # large near-black cover line
    "subtitle":     "Vendor Proposal",          # blue line beneath it
    "slogan":       "Ride the Waive.",           # WaiveLabs slogan — keep
    "prepared_for": "<Client> — Executive Team",  # navy band
    "doc_title":    "Vendor Proposal",           # right-side running header + PDF title
    "footer_conf":  "Confidential — for <Client>",  # bottom-left running footer
}

def st(name, **kw):
    base = dict(fontName="Inter", fontSize=9.5, leading=14.5, textColor=INK,
                alignment=TA_LEFT, spaceAfter=0, spaceBefore=0)
    base.update(kw)
    return ParagraphStyle(name, **base)

S = {
    "body":      st("body"),
    "lede":      st("lede", fontName="Inter-Medium", fontSize=11, leading=17.5),
    "section":   st("section", fontName="Sora-Bold", fontSize=18.5, leading=23,
                    textColor=BLUE, spaceBefore=4),
    "kicker":    st("kicker", fontName="Inter-SemiBold", fontSize=7.5, leading=10,
                    textColor=ORANGE, spaceAfter=3),
    "sub":       st("sub", fontName="Sora-SemiBold", fontSize=11.5, leading=15.5,
                    spaceBefore=6),
    "callout_t": st("callout_t", fontName="Inter-SemiBold", fontSize=9, leading=13),
    "callout_b": st("callout_b", fontName="Inter", fontSize=8.8, leading=13.2),
    "tcell":     st("tcell", fontSize=8.2, leading=11.6),
    "tcell_b":   st("tcell_b", fontName="Inter-SemiBold", fontSize=8.2, leading=11.6),
    "tcell_w":   st("tcell_w", fontName="Inter-SemiBold", fontSize=8.2, leading=11.6, textColor=WHITE),
    "tnote":     st("tnote", fontSize=7.6, leading=10.6, textColor=GRAY),
    "bullet":    st("bullet", fontSize=9.3, leading=14.2, leftIndent=14, bulletIndent=2,
                    bulletFontName="Inter-Bold", bulletColor=ORANGE),
}

DOC_TITLE = COVER["doc_title"]  # legacy alias; live value read from COVER below

def _wordmark(canv, x, y, size):
    canv.setFont("Sora-SemiBold", size); canv.setFillColor(INK)
    canv.drawString(x, y, "WaiveLabs")
    canv.setFillColor(BLUE)
    canv.drawString(x + canv.stringWidth("WaiveLabs", "Sora-SemiBold", size), y, ".ai")

def _header_footer(canv, doc):
    canv.saveState()
    canv.setFont("Inter-SemiBold", 6.8); canv.setFillColor(GRAY)
    canv.drawString(MARGIN, PAGE_H - 0.55*inch, f"WAIVELABS  ×  {CLIENT.upper()}")
    canv.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.55*inch, COVER["doc_title"])
    canv.setStrokeColor(BORDER); canv.setLineWidth(0.8)
    canv.line(MARGIN, PAGE_H - 0.63*inch, PAGE_W - MARGIN, PAGE_H - 0.63*inch)
    canv.setFont("Inter", 6.8); canv.setFillColor(GRAY)
    canv.drawString(MARGIN, 0.5*inch, COVER["footer_conf"])
    _wordmark(canv, MARGIN + 3.05*inch, 0.5*inch, 7.4)
    canv.setFont("Inter", 7.4); canv.setFillColor(GRAY)
    canv.drawRightString(PAGE_W - MARGIN, 0.5*inch, str(canv.getPageNumber()))
    canv.restoreState()

def _cover(canv, doc):
    canv.saveState()
    x = 1.0*inch
    # logo (trim png is ~3.9:1)
    logo_w = 2.5*inch; logo_h = logo_w * 327/1155.0
    canv.drawImage(LOGO, x, PAGE_H - 1.15*inch - logo_h, width=logo_w, height=logo_h,
                   mask="auto")
    canv.setStrokeColor(BLUE); canv.setLineWidth(2.2)
    canv.line(x, PAGE_H - 1.45*inch - logo_h, PAGE_W - 1.0*inch, PAGE_H - 1.45*inch - logo_h)
    canv.setFont("Inter-SemiBold", 8); canv.setFillColor(GRAY)
    canv.drawString(x, PAGE_H - 3.1*inch, COVER["draft"])
    canv.setFont("Sora-ExtraBold", 29); canv.setFillColor(INK)
    canv.drawString(x, PAGE_H - 3.65*inch, COVER["title"])
    canv.setFont("Sora-Bold", 29); canv.setFillColor(BLUE)
    canv.drawString(x, PAGE_H - 4.12*inch, COVER["subtitle"])
    canv.setFont("Sora-Medium", 12); canv.setFillColor(ORANGE)
    canv.drawString(x, PAGE_H - 4.7*inch, COVER["slogan"])
    # bottom navy band
    band_h = 1.5*inch
    canv.setFillColor(NAVY); canv.rect(0, 0, PAGE_W, band_h, fill=1, stroke=0)
    canv.setFillColor(ORANGE); canv.rect(0, band_h, PAGE_W, 0.06*inch, fill=1, stroke=0)
    canv.setFont("Inter-SemiBold", 8); canv.setFillColor(HexColor("#BCD2FF"))
    canv.drawString(x, band_h - 0.42*inch, "PREPARED FOR")
    canv.setFont("Inter", 10); canv.setFillColor(WHITE)
    canv.drawString(x, band_h - 0.62*inch, COVER["prepared_for"])
    canv.restoreState()

def make_doc(path):
    doc = BaseDocTemplate(path, pagesize=letter,
                          leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=0.92*inch, bottomMargin=0.78*inch,
                          title=COVER["doc_title"], author="WaiveLabs")
    frame = Frame(MARGIN, 0.78*inch, PAGE_W - 2*MARGIN, PAGE_H - 0.92*inch - 0.78*inch, id="f")
    cover_frame = Frame(MARGIN, 0.78*inch, PAGE_W - 2*MARGIN, PAGE_H - 1.7*inch, id="c")
    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=[cover_frame], onPage=_cover),
        PageTemplate(id="Body", frames=[frame], onPage=_header_footer),
    ])
    return doc

CW = PAGE_W - 2*MARGIN  # content width

def section(num, title, kicker_suffix=""):
    k = f"SECTION {num:02d}" + (f" — {kicker_suffix}" if kicker_suffix else "")
    bar = Table([[""]], colWidths=[CW], rowHeights=[2.4])
    bar.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), ORANGE),
                             ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
    return [CondPageBreak(2.4*inch), Spacer(1, 14),
            KeepTogether([Paragraph(k, S["kicker"]), Paragraph(title, S["section"]),
                          Spacer(1, 5), bar]), Spacer(1, 10)]

def callout(title, body, accent=BLUE):
    inner = Table([[Paragraph(title, S["callout_t"])], [Paragraph(body, S["callout_b"])]],
                  colWidths=[CW - 14])
    inner.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),8),
                               ("TOPPADDING",(0,0),(0,0),7),("BOTTOMPADDING",(0,-1),(-1,-1),7),
                               ("TOPPADDING",(0,1),(0,1),1),
                               ("BACKGROUND",(0,0),(-1,-1), MIST)]))
    box = Table([["", inner]], colWidths=[3.5, CW - 14 + 10.5])
    box.setStyle(TableStyle([("BACKGROUND",(0,0),(0,0), accent),
                             ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
                             ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
    return KeepTogether([Spacer(1,4), box, Spacer(1,8)])

def data_table(header, rows, widths, header_bg=BLUE, note=None, bold_col0=True, sub=None):
    hdr = [Paragraph(h, S["tcell_w"]) for h in header]
    body = []
    for r in rows:
        cells = []
        for i, c in enumerate(r):
            sty = S["tcell_b"] if (i == 0 and bold_col0) else S["tcell"]
            cells.append(c if not isinstance(c, str) else Paragraph(c, sty))
        body.append(cells)
    t = Table([hdr] + body, colWidths=widths, repeatRows=1)
    style = [("BACKGROUND",(0,0),(-1,0), header_bg),
             ("VALIGN",(0,0),(-1,-1),"TOP"),
             ("TOPPADDING",(0,0),(-1,-1),5.5),("BOTTOMPADDING",(0,0),(-1,-1),5.5),
             ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
             ("LINEBELOW",(0,0),(-1,-1),0.4,BORDER)]
    for i in range(1, len(body)+1, 2):
        style.append(("BACKGROUND",(0,i),(-1,i), MIST2))
    t.setStyle(TableStyle(style))
    if sub:
        out = [KeepTogether([Paragraph(sub, S["sub"]), Spacer(1, 6), t])]
    else:
        out = [t]
    if note:
        out += [Spacer(1,4), Paragraph(note, S["tnote"])]
    out.append(Spacer(1,10))
    return out

def field_table(title, pairs, label_w=1.55*inch):
    rows = [[Paragraph("Field", S["tcell_w"]), Paragraph("Detail", S["tcell_w"])]]
    for k, v in pairs:
        rows.append([Paragraph(k, S["tcell_b"]), Paragraph(v, S["tcell"])])
    t = Table(rows, colWidths=[label_w, CW - label_w], repeatRows=1)
    style = [("BACKGROUND",(0,0),(-1,0), INK),
             ("VALIGN",(0,0),(-1,-1),"TOP"),
             ("TOPPADDING",(0,0),(-1,-1),5.5),("BOTTOMPADDING",(0,0),(-1,-1),5.5),
             ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
             ("LINEBELOW",(0,0),(-1,-1),0.4,BORDER)]
    for i in range(1, len(pairs)+1, 2):
        style.append(("BACKGROUND",(0,i),(-1,i), MIST))
    t.setStyle(TableStyle(style))
    return [KeepTogether([Paragraph(title, S["sub"]), Spacer(1,6), t]), Spacer(1,12)]

def bullets(items):
    return [Paragraph(f"<bullet>▸</bullet>{i}", S["bullet"]) for i in items]
