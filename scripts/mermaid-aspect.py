"""Match each Mermaid block's fig-height to its rendered drawing so the SVG box has no letterbox.

Usage: python aspect.py BUILT_SLIDES_DIR slides/*.qmd
The n-th mermaid block in a .qmd corresponds to the n-th mermaid SVG in the built HTML.
fig-height := fig-width * viewBox height / viewBox width (rounded to 0.1 in).
"""
import os, re, sys

built = sys.argv[1]
for qmd in sys.argv[2:]:
    html = os.path.join(built, os.path.basename(qmd).replace(".qmd", ".html"))
    h = open(html, encoding="utf-8").read()
    vbs = [tuple(map(float, m.group(1).split()[2:4]))
           for m in re.finditer(r'<svg[^>]*id="mermaid-figure[^"]*"[^>]*viewbox="([^"]+)"', h, flags=re.I)]
    s = open(qmd, encoding="utf-8").read()
    blocks = list(re.finditer(r"```\{mermaid\}\n(.*?)```", s, flags=re.S))
    if len(blocks) != len(vbs):
        sys.exit(f"{qmd}: {len(blocks)} blocks vs {len(vbs)} svgs")
    out, last, changes = [], 0, []
    for m, (w, hh) in zip(blocks, vbs):
        body = m.group(1)
        fw = float(re.search(r"%%\| fig-width: ([\d.]+)", body).group(1))
        new_h = max(1.5, round(fw * hh / w, 1))
        body2 = re.sub(r"%%\| fig-height: [\d.]+", f"%%| fig-height: {new_h}", body, count=1)
        if body2 != body:
            changes.append(new_h)
        out.append(s[last:m.start(1)]); out.append(body2); last = m.end(1)
    out.append(s[last:])
    open(qmd, "w", encoding="utf-8", newline="\n").write("".join(out))
    print(os.path.basename(qmd), changes)
