"""Strict layout audit of built reveal.js decks.

For every slide (all fragments shown) reports:
  footer    - content reaching the footer band
  edge      - content beyond the slide's left/right edge
  column    - content wider than its column
  scroll    - pre/table/callout whose content is wider or taller than its box
  mm-label  - Mermaid node text larger than its node shape
  mm-overlap- Mermaid labels overlapping each other or foreign nodes
Writes a full-resolution screenshot for every flagged slide.

Usage: python layoutcheck.py DOCS_DIR OUT_DIR deck.html ...
"""
import http.server, functools, threading, os, sys, json
from playwright.sync_api import sync_playwright

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

docs, out, decks = sys.argv[1], sys.argv[2], sys.argv[3:]
# Skip redirect stubs left at old deck URLs by scripts/legacy-redirects.py (e.g. when called with 0*.html).
def is_redirect(name):
    p = os.path.join(docs, "slides", os.path.basename(name))
    try:
        t = open(p, encoding="utf-8").read()
    except OSError:
        return False
    return len(t) < 2000 and 'http-equiv="refresh"' in t
decks = [d for d in decks if not is_redirect(d)]
os.makedirs(out, exist_ok=True)
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8095), functools.partial(Q, directory=docs))
threading.Thread(target=srv.serve_forever, daemon=True).start()

JS = r"""
() => {
  const s = Reveal.getCurrentSlide();
  const issues = [];
  const R = e => e.getBoundingClientRect();
  const vis = e => { const cs = getComputedStyle(e); const r = R(e);
    return cs.visibility !== 'hidden' && cs.display !== 'none' && +cs.opacity > 0.05 && r.width > 1 && r.height > 1; };
  const txt = e => (e.textContent || e.getAttribute('alt') || e.tagName).trim().replace(/\s+/g,' ').slice(0, 50);
  const slide = R(s);
  const furniture = [];
  const footer = document.querySelector('.reveal .footer');
  if (footer && vis(footer)) { const rg = document.createRange(); rg.selectNodeContents(footer); furniture.push({r: rg.getBoundingClientRect(), what: 'stopka'}); }
  document.querySelectorAll('.reveal .slide-menu-button, .reveal .slide-chalkboard-buttons, .reveal .slide-number').forEach(e => { if (vis(e)) furniture.push({r: R(e), what: e.className.split(' ')[0]}); });
  const PAD = 8; const hit = r => furniture.filter(f => Math.min(r.right, f.r.right + PAD) - Math.max(r.left, f.r.left - PAD) > 0 && Math.min(r.bottom, f.r.bottom + PAD) - Math.max(r.top, f.r.top - PAD) > 0);
  const textRects = e => { const rg = document.createRange(); rg.selectNodeContents(e); return [...rg.getClientRects()]; };
  // 1-2: leaves of slide content
  const sel = 'p, li, td, th, h2, h3, pre, img, svg[id^="mermaid-figure"], .callout, table, .zrodlo, .liczby > div, figure, blockquote';
  s.querySelectorAll(sel).forEach(e => {
    if (!vis(e) || e.closest('svg') && e.tagName.toLowerCase() !== 'svg') return;
    const r = R(e);
    const tag = e.tagName.toLowerCase();
    const rects = ['li', 'p', 'td', 'th', 'h2', 'h3'].includes(tag) ? textRects(e) : [r];
    const hits = rects.flatMap(hit);
    if (hits.length) issues.push({type: 'footer', el: e.tagName, text: txt(e), what: [...new Set(hits.map(x => x.what))].join(',')});
    if (r.bottom > slide.bottom + 2) issues.push({type: 'bottom', el: e.tagName, text: txt(e), over: Math.round(r.bottom - slide.bottom)});
    if (r.right > slide.right + 2 || r.left < slide.left - 2)
      issues.push({type: 'edge', el: e.tagName, text: txt(e), over: Math.round(Math.max(r.right - slide.right, slide.left - r.left))});
    const col = e.closest('.column');
    if (col && e !== col) { const c = R(col);
      if (r.right > c.right + 3) issues.push({type: 'column', el: e.tagName, text: txt(e), over: Math.round(r.right - c.right)}); }
  });
  // 3: inner overflow of boxes
  s.querySelectorAll('pre, .callout, table, .cell-output-display, .sourceCode').forEach(e => {
    if (!vis(e)) return;
    if (e.scrollWidth > e.clientWidth + 2 || e.scrollHeight > e.clientHeight + 2)
      issues.push({type: 'scroll', el: e.className || e.tagName, text: txt(e), over: Math.max(e.scrollWidth - e.clientWidth, e.scrollHeight - e.clientHeight)});
  });
  // 4-5: Mermaid
  const inter = (a, b) => Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)) *
                          Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
  s.querySelectorAll('svg[id^="mermaid-figure"]').forEach((svg, k) => {
    if (!vis(svg)) return;
    // node text vs node shape
    const nodes = [...svg.querySelectorAll('g.node')].map(g => {
      const shape = g.querySelector('rect, polygon, circle, ellipse, path');
      const lab = g.querySelector('.nodeLabel, foreignObject div, text');
      return {g, shape: shape ? R(shape) : R(g), lab: lab ? R(lab) : null, text: txt(g)};
    });
    nodes.forEach(n => { if (!n.lab) return;
      const sh = n.shape, l = n.lab;
      if (l.width > sh.width + 2 || l.height > sh.height + 2)
        issues.push({type: 'mm-label', diagram: k, text: n.text, over: Math.round(Math.max(l.width - sh.width, l.height - sh.height))});
    });
    // edge labels: only the label background, not empty placeholders
    const elabs = [...svg.querySelectorAll('g.edgeLabel')].filter(g => (g.textContent || '').trim())
                   .map(g => ({r: R(g.querySelector('.labelBkg, foreignObject, rect, text') || g), text: txt(g)}));
    for (let i = 0; i < elabs.length; i++) {
      for (let j = i + 1; j < elabs.length; j++) if (inter(elabs[i].r, elabs[j].r) > 6)
        issues.push({type: 'mm-overlap', diagram: k, text: elabs[i].text + ' ⟷ ' + elabs[j].text, over: Math.round(inter(elabs[i].r, elabs[j].r))});
      nodes.forEach(n => { if (inter(elabs[i].r, n.shape) > 30)
        issues.push({type: 'mm-overlap', diagram: k, text: elabs[i].text + ' ⟷ węzeł ' + n.text, over: Math.round(inter(elabs[i].r, n.shape))}); });
    }
    // sequence diagrams: message texts vs notes / actors
    const msgs = [...svg.querySelectorAll('text.messageText')].map(t => ({r: R(t), text: txt(t)}));
    const boxes = [...svg.querySelectorAll('rect.note, rect.actor')].map(b => ({r: R(b), text: 'ramka'}));
    msgs.forEach((m, i) => {
      boxes.forEach(b => { if (inter(m.r, b.r) > 20) issues.push({type: 'mm-overlap', diagram: k, text: m.text + ' ⟷ ramka', over: Math.round(inter(m.r, b.r))}); });
      msgs.slice(i + 1).forEach(o => { if (inter(m.r, o.r) > 6) issues.push({type: 'mm-overlap', diagram: k, text: m.text + ' ⟷ ' + o.text, over: Math.round(inter(m.r, o.r))}); });
    });
    svg.querySelectorAll('text.noteText').forEach(t => {
      const g = t.parentElement; const rect = g && g.querySelector('rect.note');
      if (rect) { const a = R(t), b = R(rect);
        if (a.width > b.width + 2) issues.push({type: 'mm-label', diagram: k, text: txt(t), over: Math.round(a.width - b.width)}); }
    });
  });
  return {id: s.id, issues};
}
"""
total = 0
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["QUARTO_CHROMIUM"])
    pg = b.new_page(viewport={"width": 1600, "height": 900})
    for deck in decks:
        pg.goto(f"http://127.0.0.1:8095/slides/{deck}")
        pg.wait_for_function("window.Reveal && Reveal.isReady()")
        pg.evaluate("Reveal.configure({transition: 'none', backgroundTransition: 'none', transitionSpeed: 'fast'})")
        pg.add_style_tag(content=".reveal .slides section, .reveal .slides section .fragment { transition: none !important; }")
        n = pg.evaluate("Reveal.getSlides().length")
        for i in range(n):
            pg.evaluate(f"(() => {{const s=Reveal.getSlides()[{i}]; const x=Reveal.getIndices(s); Reveal.slide(x.h, x.v, 999);}})()")
            pg.wait_for_timeout(250)
            res = pg.evaluate(JS)
            if res["issues"]:
                total += len(res["issues"])
                pg.screenshot(path=f"{out}/{deck[:2]}-{i:02d}-{res['id']}.png")
                for it in res["issues"]:
                    print(json.dumps({"deck": deck[:2], "slide": i, "id": res["id"], **it}, ensure_ascii=False))
    b.close()
srv.shutdown()
print("TOTAL", total)
