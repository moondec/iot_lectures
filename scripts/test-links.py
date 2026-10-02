#!/usr/bin/env python3
"""Sprawdza wszystkie odnośniki w zbudowanej witrynie.

Uruchomienie:
    python3 scripts/test-links.py            # tylko lokalne (szybko, offline)
    python3 scripts/test-links.py --external # dodatkowo statusy odnośników zewnętrznych

Lokalne src/href/url()/iframe muszą istnieć na dysku — to warunek twardy.
Odnośniki zewnętrzne raportujemy z jawnym rozróżnieniem: 404 to błąd treści,
403 i timeout to najczęściej blokada bota lub wolny serwer, nie martwy adres.
"""
import json, os, re, sys, glob, urllib.request, urllib.error, socket
import concurrent.futures as cf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
DOCS = "docs"
SPRAWDZAJ_ZEWNETRZNE = "--external" in sys.argv

HTML = sorted(glob.glob(f"{DOCS}/**/*.html", recursive=True))
HTML = [h for h in HTML if "/site_libs/" not in h]
# docs/archiwum/ is a frozen copy of the previous site: its unlicensed images were
# removed on purpose and konspekt_files/ never existed, so it is not checked here.
HTML = [h for h in HTML if not h.replace(os.sep, "/").startswith(f"{DOCS}/archiwum/")]

lokalne_ok, lokalne_brak, zewnetrzne = [], [], {}


def normalizuj(base_dir, ref):
    ref = ref.split("#")[0].split("?")[0]
    if not ref:
        return None
    return os.path.normpath(os.path.join(base_dir, urllib.parse.unquote(ref)))


import urllib.parse  # noqa: E402  (po definicji normalizuj dla czytelności)

for f in HTML:
    base = os.path.dirname(f)
    h = open(f, encoding="utf-8").read()
    refs = set()
    refs |= set(re.findall(r'(?:src|href)="([^"]+)"', h))
    refs |= set(re.findall(r"url\(['\"]?([^'\")]+)['\"]?\)", h))
    refs |= set(re.findall(r'<iframe[^>]*src="([^"]+)"', h))
    for r in refs:
        if r.startswith(("data:", "javascript:", "mailto:", "#")):
            continue
        if r.startswith(("http://", "https://")):
            zewnetrzne.setdefault(r, []).append(os.path.basename(f))
            continue
        p = normalizuj(base, r)
        if p is None:
            continue
        (lokalne_ok if os.path.exists(p) else lokalne_brak).append(
            {"plik": os.path.basename(f), "ref": r, "sciezka": p})

# arkusze CSS też odwołują się do zasobów (czcionki)
for css in glob.glob(f"{DOCS}/**/*.css", recursive=True):
    base = os.path.dirname(css)
    t = open(css, encoding="utf-8", errors="replace").read()
    for r in set(re.findall(r"url\(['\"]?([^'\")]+)['\"]?\)", t)):
        if r.startswith(("data:", "http://", "https://")):
            if r.startswith("http"):
                zewnetrzne.setdefault(r, []).append(os.path.relpath(css, DOCS))
            continue
        p = normalizuj(base, r)
        if p and not os.path.exists(p):
            lokalne_brak.append({"plik": os.path.relpath(css, DOCS),
                                 "ref": r, "sciezka": p})
        elif p:
            lokalne_ok.append({"plik": os.path.relpath(css, DOCS),
                               "ref": r, "sciezka": p})

print(f"Odnośniki lokalne: {len(lokalne_ok)} istnieje, {len(lokalne_brak)} brakuje")
for b in lokalne_brak:
    print(f"  BRAK  {b['plik']} → {b['ref']}")

wynik_zewn = []
if SPRAWDZAJ_ZEWNETRZNE:
    print(f"\nSprawdzanie {len(zewnetrzne)} unikalnych odnośników zewnętrznych…")

    def sprawdz(url):
        # Nagłówek musi być ASCII — urllib koduje nagłówki jako latin-1.
        naglowki = {"User-Agent": "Mozilla/5.0 (compatible; iot-course-slides link check)",
                    "Accept": "*/*"}
        for metoda in ("HEAD", "GET"):
            try:
                req = urllib.request.Request(url, method=metoda, headers=naglowki)
                with urllib.request.urlopen(req, timeout=20) as r:
                    koncowy = r.geturl()
                    pocz = urllib.parse.urlsplit(url)
                    kon = urllib.parse.urlsplit(koncowy)
                    przekierowany = (pocz.scheme, pocz.netloc, pocz.path) != (kon.scheme, kon.netloc, kon.path)
                    return {"url": url, "url_koncowy": koncowy, "status": r.status,
                            "kategoria": "przekierowanie" if przekierowany else "ok"}
            except urllib.error.HTTPError as e:
                if e.code in (403, 405) and metoda == "HEAD":
                    continue
                kat = ("nieistniejacy" if e.code in (404, 410)
                       else "blokada-bota" if e.code in (401, 403, 429)
                       else "inny-blad")
                return {"url": url, "status": e.code, "kategoria": kat}
            except (urllib.error.URLError, socket.timeout, TimeoutError) as e:
                return {"url": url, "status": None, "kategoria": "timeout-lub-sieć",
                        "szczegol": str(getattr(e, "reason", e))[:90]}
            except Exception as e:  # noqa: BLE001
                return {"url": url, "status": None, "kategoria": "inny-blad",
                        "szczegol": str(e)[:90]}
        return {"url": url, "status": None, "kategoria": "inny-blad"}

    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for r in ex.map(sprawdz, sorted(zewnetrzne)):
            r["wystepuje_w"] = sorted(set(zewnetrzne[r["url"]]))
            wynik_zewn.append(r)

    kat = {}
    for r in wynik_zewn:
        kat.setdefault(r["kategoria"], []).append(r)
    for k in ("ok", "przekierowanie", "blokada-bota", "timeout-lub-sieć", "inny-blad", "nieistniejacy"):
        if k in kat:
            print(f"\n  {k}: {len(kat[k])}")
            if k != "ok":
                for r in kat[k]:
                    cel = f" → {r['url_koncowy']}" if r.get("url_koncowy") else ""
                    print(f"     {r.get('status')}  {r['url']}{cel}")
else:
    print(f"\nOdnośników zewnętrznych: {len(zewnetrzne)} "
          f"(uruchom z --external, aby sprawdzić statusy)")

os.makedirs("review", exist_ok=True)
json.dump({
    "lokalne": {"ok": len(lokalne_ok), "brak": len(lokalne_brak),
                "brakujace": lokalne_brak},
    "zewnetrzne_liczba": len(zewnetrzne),
    "zewnetrzne_sprawdzone": bool(SPRAWDZAJ_ZEWNETRZNE),
    "zewnetrzne": wynik_zewn,
}, open("review/verification-links.json", "w"), ensure_ascii=False, indent=1)

blad = bool(lokalne_brak) or any(
    r["kategoria"] == "nieistniejacy" for r in wynik_zewn)
print(f"\nZapisano: review/verification-links.json")
sys.exit(1 if blad else 0)
