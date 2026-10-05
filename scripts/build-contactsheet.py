#!/usr/bin/env python3
"""Składa kontaktówkę zrzutów ekranu do szybkiego przeglądu.

Uruchomienie (po scripts/test-browser.py):
    python3 scripts/build-contactsheet.py

Wynik: review/kontaktowka.html — jedna strona ze wszystkimi zrzutami,
pogrupowanymi wykładami, z odnośnikami do odpowiednich slajdów.
Otwiera się z dysku (file://), nie wymaga serwera.
"""
import os, re, glob, html, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

TYTULY = {}
for f in sorted(glob.glob("docs/slides/*.html")):
    if 'http-equiv="refresh"' in open(f, encoding="utf-8").read(2000):
        continue  # redirect stub at an old deck URL
    h = open(f, encoding="utf-8").read()
    m = re.search(r'<h1 class="title">(.*?)</h1>', h, re.S)
    TYTULY[os.path.basename(f).replace(".html", "")] = (
        re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else "?")

zrzuty = sorted(glob.glob("review/screenshots/*.png"))
wg_talii = {}
for z in zrzuty:
    n = os.path.basename(z)
    talia, reszta = n.split("__", 1)
    idx, sid = reszta.replace(".png", "").split("_", 1)
    wg_talii.setdefault(talia, []).append((int(idx), sid, os.path.basename(z)))

CSS = """
:root { --akcent:#0b6b78; --ciemny:#0b3b45; }
* { box-sizing:border-box }
body { font-family:-apple-system,"Segoe UI",Roboto,Arial,sans-serif;
       margin:0; padding:24px 28px; color:#1f2933; background:#f4f7f8; }
h1 { color:var(--ciemny); margin:0 0 4px; font-size:1.55rem }
.pod { color:#5a646e; margin:0 0 22px; font-size:.92rem }
h2 { color:var(--ciemny); font-size:1.12rem; margin:30px 0 4px;
     border-bottom:2px solid var(--akcent); padding-bottom:5px }
h2 .mod { color:var(--akcent); font-weight:700; margin-right:.5em }
.siatka { display:grid; grid-template-columns:repeat(auto-fill,minmax(400px,1fr));
          gap:16px; margin-top:12px }
figure { margin:0; background:#fff; border:1px solid #dde4e6; border-radius:6px;
         overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,.06) }
figure img { width:100%; display:block; border-bottom:1px solid #eef2f3 }
figcaption { padding:7px 10px; font-size:.8rem; color:#51626c }
figcaption code { color:#8a2846; background:#f1f5f6; padding:.05em .3em;
                  border-radius:3px; font-size:.95em }
a.slajd { color:var(--akcent); text-decoration:none; font-weight:600 }
a.slajd:hover { text-decoration:underline }
.info { background:#e8f2f4; border-left:4px solid var(--akcent);
        padding:11px 14px; border-radius:0 4px 4px 0; font-size:.88rem;
        margin-bottom:18px }
"""

L = ['<!DOCTYPE html><html lang="pl"><head><meta charset="utf-8">',
     '<meta name="viewport" content="width=device-width, initial-scale=1">',
     "<title>Kontaktówka — osiem wykładów IoT</title>",
     f"<style>{CSS}</style></head><body>",
     "<h1>Kontaktówka zrzutów ekranu</h1>",
     f'<p class="pod">{len(zrzuty)} zrzutów z {len(wg_talii)} wykładów, '
     "okno 1440×810, wszystkie fragmenty rozwinięte.</p>",
     '<div class="info">Zrzuty pochodzą z automatycznego przejścia przez '
     "wszystkie slajdy (<code>scripts/test-browser.py</code>). Odnośnik przy każdym "
     "zrzucie otwiera dany slajd w prezentacji — działa po uruchomieniu podglądu "
     "poleceniem <code>scripts/serve.sh 8090</code>.</div>"]

for talia in sorted(wg_talii):
    nr = talia.split("-")[0]
    L.append(f'<h2><span class="mod">{nr}</span>'
             f"{html.escape(TYTULY.get(talia, talia))}</h2>")
    L.append('<div class="siatka">')
    for idx, sid, plik in sorted(wg_talii[talia]):
        url = f"http://127.0.0.1:8090/slides/{talia}.html#/{sid}"
        L.append(
            f'<figure><img src="screenshots/{html.escape(plik)}" loading="lazy" '
            f'alt="Slajd {html.escape(sid)} wykładu {nr}">'
            f'<figcaption><a class="slajd" href="{html.escape(url)}">'
            f"<code>#{html.escape(sid)}</code></a> · pozycja {idx}"
            "</figcaption></figure>")
    L.append("</div>")

L.append("</body></html>")
open("review/kontaktowka.html", "w", encoding="utf-8").write("\n".join(L))
print(f"Zapisano: review/kontaktowka.html ({len(zrzuty)} zrzutów, "
      f"{len(wg_talii)} wykładów)")
