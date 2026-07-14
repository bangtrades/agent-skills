#!/usr/bin/env python3
"""
wl-bvc-report — WaiveLabs Build & Value Creation Report engine.

Renders a branded, multi-page US-Letter PDF from a JSON config.
Layout, brand mechanics, fonts, header/footer, and the client-safe
language lint are handled here; the agent supplies only content.

Usage:
    python3 build_report.py <report.json>

Exit codes:
    0 = clean render
    2 = rendered, but with overflow warnings (fix copy and re-run)
    3 = language lint failure (forbidden terms found; nothing rendered)
"""
import json
import os
import sys
import urllib.request

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)

# ---------------- brand palette (brand-waive) ----------------
BLUE = HexColor('#3179F5'); DEEP = HexColor('#0D43AA'); ORANGE = HexColor('#E65100')
SUN = HexColor('#FF7A1A'); INK = HexColor('#0F172A'); BODY = HexColor('#1E2435')
CREAM = HexColor('#FFF8F1'); MORN = HexColor('#F4F7FD'); NAVY = HexColor('#0C1428')
MUTE = HexColor('#6B7280'); LINE = HexColor('#DDE3EE'); WHITE = HexColor('#FFFFFF')
AMBER_ON_NAVY = HexColor('#FFB454'); SLATE_ON_NAVY = HexColor('#9FB3D9')

W, H = letter
M = 1.0 * inch
BOTTOM = 0.85 * inch          # nothing below this except the footer
FONT_CACHE = '/tmp/wl-fonts'

# Default lint list. Words that make prospects ask the wrong questions.
DEFAULT_FORBIDDEN = ['simulat', 'prototype', 'mock', 'synthetic',
                     'proof-of-concept', 'proof of concept', ' poc ', 'dummy']

warnings = []


# ---------------- fonts ----------------
def ensure_fonts():
    """Download + instance Sora/Inter once, cache in /tmp/wl-fonts.
    Falls back to Helvetica if offline — the report still ships."""
    os.makedirs(FONT_CACHE, exist_ok=True)
    targets = {'Sora-Bold.ttf': ('sora', 700), 'Sora-SemiBold.ttf': ('sora', 600),
               'Inter-Regular.ttf': ('inter', 400), 'Inter-SemiBold.ttf': ('inter', 600),
               'Inter-Bold.ttf': ('inter', 700)}
    if not all(os.path.exists(os.path.join(FONT_CACHE, t)) for t in targets):
        try:
            srcs = {
                'sora': 'https://github.com/google/fonts/raw/main/ofl/sora/Sora%5Bwght%5D.ttf',
                'inter': 'https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf',
            }
            from fontTools.ttLib import TTFont as FTFont
            from fontTools.varLib.instancer import instantiateVariableFont
            vf = {}
            for key, url in srcs.items():
                p = os.path.join(FONT_CACHE, f'{key}-var.ttf')
                if not os.path.exists(p):
                    urllib.request.urlretrieve(url, p)
                vf[key] = p
            for out, (fam, wght) in targets.items():
                axes = {'wght': wght}
                if fam == 'inter':
                    axes['opsz'] = 14
                f = FTFont(vf[fam])
                instantiateVariableFont(f, axes)
                f.save(os.path.join(FONT_CACHE, out))
        except Exception as e:
            warnings.append(f'font setup failed ({e}); using Helvetica fallback')
            return {'Sora-B': 'Helvetica-Bold', 'Sora-SB': 'Helvetica-Bold',
                    'Inter': 'Helvetica', 'Inter-SB': 'Helvetica-Bold', 'Inter-B': 'Helvetica-Bold'}
    reg = {'Sora-B': 'Sora-Bold.ttf', 'Sora-SB': 'Sora-SemiBold.ttf',
           'Inter': 'Inter-Regular.ttf', 'Inter-SB': 'Inter-SemiBold.ttf', 'Inter-B': 'Inter-Bold.ttf'}
    for name, fn in reg.items():
        pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_CACHE, fn)))
    return {k: k for k in reg}


# ---------------- language lint ----------------
def collect_strings(node, acc):
    if isinstance(node, str):
        acc.append(node)
    elif isinstance(node, dict):
        for k, v in node.items():
            if k not in ('output', 'forbidden_terms', 'client_terms'):
                collect_strings(v, acc)
    elif isinstance(node, list):
        for v in node:
            collect_strings(v, acc)


def lint(cfg):
    terms = [t.lower() for t in cfg.get('forbidden_terms', DEFAULT_FORBIDDEN)]
    terms += [t.lower() for t in cfg.get('client_terms', [])]
    acc = []
    collect_strings(cfg, acc)
    hits = []
    for s in acc:
        low = ' ' + s.lower() + ' '
        for t in terms:
            if t in low:
                hits.append((t.strip(), s[:90]))
    return hits


# ---------------- layout engine ----------------
class Report:
    def __init__(self, cfg, fonts):
        self.cfg = cfg
        self.F = fonts
        self.c = canvas.Canvas(cfg['output'], pagesize=letter)
        self.c.setTitle(cfg.get('title', 'Build & Value Creation Report') + ' — WaiveLabs.ai')
        self.c.setAuthor('WaiveLabs.ai')
        logo = cfg.get('logo') or os.path.join(SKILL_DIR, 'assets', 'waivelabs-logo.png')
        self.logo = ImageReader(logo)
        self.page_no = 0
        self.y = H

    # -- chrome --
    def header(self):
        c = self.c
        lw = 1.5 * inch
        lh = lw * self.logo.getSize()[1] / self.logo.getSize()[0]
        c.drawImage(self.logo, M, H - 0.62 * inch - lh / 2, width=lw, height=lh, mask='auto')
        c.setFont(self.F['Sora-SB'], 8); c.setFillColor(MUTE)
        c.drawRightString(W - M, H - 0.55 * inch, self.cfg.get('doc_type', 'BUILD & VALUE CREATION REPORT'))
        c.drawRightString(W - M, H - 0.70 * inch, self.cfg.get('date_line', ''))
        c.setStrokeColor(BLUE); c.setLineWidth(1.4)
        c.line(M, H - 0.95 * inch, W - M, H - 0.95 * inch)
        self.y = H - 1.45 * inch

    def footer(self):
        self.page_no += 1
        c = self.c
        c.setFont(self.F['Inter'], 9); c.setFillColor(MUTE)
        c.drawString(M, 0.55 * inch, 'WaiveLabs.ai · confidential')
        c.drawRightString(W - M, 0.55 * inch, str(self.page_no))

    def check(self, need, what):
        if self.y - need < BOTTOM:
            warnings.append(f'page {self.page_no + 1}: "{what}" overflows by '
                            f'{(BOTTOM - (self.y - need)) / inch:.2f}in — trim copy or move the block')

    # -- text helpers --
    def wrap(self, text, font, size, width):
        words = text.split(); lines = []; cur = ''
        for w_ in words:
            t = (cur + ' ' + w_).strip()
            if pdfmetrics.stringWidth(t, font, size) <= width:
                cur = t
            else:
                lines.append(cur); cur = w_
        if cur:
            lines.append(cur)
        return lines

    # -- blocks --
    def b_title(self, blk):
        c = self.c
        c.setFont(self.F['Sora-B'], 27); c.setFillColor(INK)
        c.drawString(M, self.y, blk['text'])
        self.y -= 0.32 * inch
        if blk.get('dek'):
            self.b_para({'text': blk['dek'], 'size': 11.5, 'lead': 16, 'color': 'mute'})
        self.y -= 0.18 * inch

    def b_h2(self, blk):
        c = self.c
        self.check(0.6 * inch, blk['text'])
        c.setFont(self.F['Sora-SB'], 16); c.setFillColor(DEEP)
        c.drawString(M, self.y, blk['text'])
        c.setStrokeColor(SUN if blk.get('accent', 'orange') == 'orange' else BLUE)
        c.setLineWidth(2.5)
        c.line(M, self.y - 7, M + 0.55 * inch, self.y - 7)
        self.y -= 0.34 * inch

    def b_para(self, blk):
        c = self.c
        size = blk.get('size', 10.5); lead = blk.get('lead', 15.5)
        font = self.F['Inter-SB'] if blk.get('bold') else self.F['Inter']
        color = {'mute': MUTE, 'deep': DEEP}.get(blk.get('color'), BODY)
        width = W - 2 * M
        lines = self.wrap(blk['text'], font, size, width)
        self.check(len(lines) * lead, blk['text'][:40])
        c.setFont(font, size); c.setFillColor(color)
        for ln in lines:
            c.drawString(M, self.y, ln); self.y -= lead
        self.y -= blk.get('after', 6)

    def b_kpi_strip(self, blk):
        c = self.c
        items = blk['items']; hgt = 0.86 * inch
        self.check(hgt + 0.3 * inch, 'kpi strip')
        n = len(items); gap = 0.14 * inch
        bw = (W - 2 * M - gap * (n - 1)) / n
        for i, it in enumerate(items):
            x = M + i * (bw + gap)
            c.setFillColor(MORN); c.setStrokeColor(LINE); c.setLineWidth(0.75)
            c.roundRect(x, self.y - hgt, bw, hgt, 5, fill=1, stroke=1)
            c.setFillColor(ORANGE if it.get('hot') else DEEP)
            val = it['value']
            c.setFont(self.F['Sora-B'], 17 if len(val) <= 9 else 14)
            c.drawCentredString(x + bw / 2, self.y - 0.36 * inch, val)
            c.setFont(self.F['Inter-SB'], 7.6); c.setFillColor(MUTE)
            for j, ln in enumerate(self.wrap(it['label'].upper(), self.F['Inter-SB'], 7.6, bw - 10)):
                c.drawCentredString(x + bw / 2, self.y - 0.55 * inch - j * 10, ln)
        self.y -= hgt + 0.3 * inch

    def b_table(self, blk):
        c = self.c
        headers = blk['headers']; rows = blk['rows']
        widths = blk.get('widths')
        total = W - 2 * M
        if widths:
            colw = [w * inch if w else None for w in widths]
            fixed = sum(w for w in colw if w)
            flex = colw.count(None)
            colw = [w if w else (total - fixed) / flex for w in colw]
        else:
            colw = [total / len(headers)] * len(headers)
        pad = 7; size = 9.2; row_lead = 13.5
        hh = 0.28 * inch
        # estimate height for overflow check
        est = hh
        cells_all = []
        for row in rows:
            cells = [self.wrap(t, self.F['Inter'], size, cw - 2 * pad) for t, cw in zip(row, colw)]
            cells_all.append(cells)
            est += max(len(cl) for cl in cells) * row_lead + 9
        self.check(est + 0.26 * inch, f'table "{headers[0]}"')
        c.setFillColor(MORN); c.rect(M, self.y - hh, sum(colw), hh, fill=1, stroke=0)
        c.setFont(self.F['Inter-B'], 8.2); c.setFillColor(DEEP)
        cx = M
        for htxt, cw in zip(headers, colw):
            c.drawString(cx + pad, self.y - hh + 8, htxt.upper()); cx += cw
        self.y -= hh
        for cells in cells_all:
            rh = max(len(cl) for cl in cells) * row_lead + 9
            cx = M
            for k, (cl, cw) in enumerate(zip(cells, colw)):
                ty = self.y - 13
                c.setFont(self.F['Inter-SB'] if k == 0 else self.F['Inter'], size)
                c.setFillColor(INK if k == 0 else BODY)
                for ln in cl:
                    c.drawString(cx + pad, ty, ln); ty -= row_lead
                cx += cw
            self.y -= rh
            c.setStrokeColor(LINE); c.setLineWidth(0.5)
            c.line(M, self.y, M + sum(colw), self.y)
        self.y -= 0.26 * inch

    def b_callout(self, blk):
        c = self.c
        width = W - 2 * M; size = 10.5; lead = 15
        lines = self.wrap(blk['text'], self.F['Inter'], size, width - 0.55 * inch)
        hgt = 0.42 * inch + len(lines) * lead + 8
        self.check(hgt + 0.28 * inch, f'callout "{blk["title"]}"')
        c.setFillColor(CREAM); c.rect(M, self.y - hgt, width, hgt, fill=1, stroke=0)
        c.setFillColor(SUN); c.rect(M, self.y - hgt, 3.5, hgt, fill=1, stroke=0)
        ty = self.y - 0.28 * inch
        c.setFont(self.F['Sora-SB'], 10.5); c.setFillColor(DEEP)
        c.drawString(M + 0.28 * inch, ty, blk['title']); ty -= lead + 3
        c.setFont(self.F['Inter'], size); c.setFillColor(BODY)
        for ln in lines:
            c.drawString(M + 0.28 * inch, ty, ln); ty -= lead
        self.y -= hgt + 0.28 * inch

    def b_brand_band(self, blk):
        """Navy closing band. Use only on the final page (skips the page-number footer)."""
        c = self.c
        c.setFillColor(NAVY); c.rect(0, 0, W, 0.9 * inch, fill=1, stroke=0)
        c.setFont(self.F['Sora-SB'], 11); c.setFillColor(WHITE)
        c.drawString(M, 0.52 * inch, 'WaiveLabs.ai')
        c.setFont(self.F['Inter'], 9.5); c.setFillColor(SLATE_ON_NAVY)
        c.drawString(M, 0.32 * inch, blk.get('tagline', 'Ride the AI wave.'))
        c.setFillColor(AMBER_ON_NAVY)
        c.drawRightString(W - M, 0.42 * inch, blk.get('contact', 'hello@waivelabs.ai'))

    # -- driver --
    def render(self):
        blocks = {'title': self.b_title, 'h2': self.b_h2, 'para': self.b_para,
                  'kpi_strip': self.b_kpi_strip, 'table': self.b_table,
                  'callout': self.b_callout, 'brand_band': self.b_brand_band}
        for pi, page in enumerate(self.cfg['pages']):
            self.header()
            has_band = any(b['type'] == 'brand_band' for b in page['blocks'])
            for blk in page['blocks']:
                blocks[blk['type']](blk)
            if not has_band:
                self.footer()
            else:
                self.page_no += 1
            self.c.showPage()
        self.c.save()


def main():
    if len(sys.argv) != 2:
        print(__doc__); sys.exit(1)
    with open(sys.argv[1]) as f:
        cfg = json.load(f)
    hits = lint(cfg)
    if hits:
        print('LANGUAGE LINT FAILED — fix these before rendering:')
        for term, ctx in hits:
            print(f'  [{term}] …{ctx}…')
        sys.exit(3)
    fonts = ensure_fonts()
    Report(cfg, fonts).render()
    print('wrote', cfg['output'])
    if warnings:
        print('WARNINGS:')
        for w_ in warnings:
            print(' -', w_)
        sys.exit(2)


if __name__ == '__main__':
    main()
