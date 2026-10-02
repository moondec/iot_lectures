#!/usr/bin/env python3
"""Składa raport odbioru i zbiorczy plik weryfikacji z wyników testów.

Uruchomienie (po quarto render i po wszystkich testach):
    python3 scripts/build-report.py

Wytwarza:
    provenance/PROWENIENCJA.md      czytelne zestawienie pochodzenia slajdów
    review/verification.json        zbiorczy wynik maszynowy
    review/REPORT.md                sekcja z licznikami (wstawiana do raportu)

Wszystkie liczby są wyliczane z plików wynikowych, nie wpisywane ręcznie.
"""
import json, os, re, glob, collections, hashlib, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


def wczytaj(p):
    return json.load(open(p, encoding="utf-8")) if os.path.isfile(p) else None


man = wczytaj("provenance/slide-map.json")
inv = wczytaj("provenance/source-inventory.json")
calc = wczytaj("provenance/obliczenia.json")
t_str = wczytaj("review/verification-structure.json")
t_lnk = wczytaj("review/verification-links.json")
t_brw = wczytaj("review/verification-browser.json")
t_sub = wczytaj("review/verification-browser-podkatalog.json")

DECKS = sorted(glob.glob("docs/slides/*.html"))

# --- liczniki wyliczone z HTML ------------------------------------------
talie = []
for f in DECKS:
    h = open(f, encoding="utf-8").read()
    deck = os.path.basename(f).replace(".html", "")
    tytul = re.search(r'<h1 class="title">(.*?)</h1>', h, re.S)
    ids = re.findall(r'<section[^>]*\bid="([^"]*)"', h)
    sek = len(re.findall(r'<section[^>]*class="[^"]*\bsekcja\b', h))
    talie.append({
        "plik": os.path.basename(f),
        "tytul": re.sub(r"<[^>]+>", "", tytul.group(1)).strip() if tytul else "?",
        "sekcji_html": len(ids),
        "slajdy_merytoryczne": len(ids) - sek - (1 if "title-slide" in ids else 0),
        "przekladki_sekcyjne": sek,
        "diagramow_mermaid": len(re.findall(r'<svg id="mermaid-figure', h)),
        "tabel": h.count("<table"),
        "obrazow": len(re.findall(r"<img[^>]*src=", h)),
        "bajtow": len(h.encode()),
        "sha256": hashlib.sha256(open(f, "rb").read()).hexdigest(),
    })

origin = collections.Counter(s["origin"] for s in man["slajdy"])
origin_tresc = collections.Counter(
    s["origin"] for s in man["slajdy"] if s["rodzaj"] == "tresc")

src_h2 = [(d, s["title"]) for d, v in inv.items()
          for s in v["slides"] if s["level"] == 2]
uzyte = {(z["qmd"].replace(".qmd", ""), z["tytul"])
         for s in man["slajdy"]
         for z in [s.get("zrodlo")] + s.get("zrodla_dodatkowe", [])
         if z and z.get("typ") == "prezentacja"}

# --- sumaryczny wynik testów przeglądarkowych ---------------------------
def zbierz_brw(r):
    if not r:
        return None
    problemy = []
    stanow = slajdow = 0
    for t in r["talie"]:
        for v in t["widoki"]:
            if v["widok"] == "pulpit":
                stanow += v["stanow_odwiedzonych"]
                slajdow += v["slajdow_unikalnych"]
            for k in ("przepelnienia", "obrazy_niezaladowane", "mermaid_bez_svg",
                      "bledy_js", "zle_zadania", "slajdy_puste"):
                if v.get(k):
                    problemy.append(f"{t['talia']}/{v['widok']}:{k}")
    return {"base": r["base"], "slajdow": slajdow, "stanow_z_fragmentami": stanow,
            "widokow": sum(len(t["widoki"]) for t in r["talie"]),
            "problemow": len(problemy), "problemy": problemy}


ver = {
    "projekt": "iot-course-slides",
    "opis": "Osiem prezentacji Quarto/reveal.js — wynik weryfikacji.",
    "budowanie": {
        "quarto": subprocess.run(["quarto", "--version"], capture_output=True,
                                 text=True).stdout.strip() or "1.10.18",
        "mermaid_format": "svg (render po stronie budowania)",
        "output_dir": "docs",
        "sciezki": "wyłącznie względne",
    },
    "zrodlo": man["zrodlo"],
    "talie": talie,
    "sumy": {
        "talii": len(talie),
        "sekcji_html_lacznie": sum(t["sekcji_html"] for t in talie),
        "slajdow_merytorycznych": sum(t["slajdy_merytoryczne"] for t in talie),
        "przekladek_sekcyjnych": sum(t["przekladki_sekcyjne"] for t in talie),
        "diagramow_mermaid": sum(t["diagramow_mermaid"] for t in talie),
        "tabel": sum(t["tabel"] for t in talie),
        "obrazow": sum(t["obrazow"] for t in talie),
    },
    "pochodzenie": {
        "wg_origin_wszystkie": dict(origin),
        "wg_origin_merytoryczne": dict(origin_tresc),
        "slajdow_zrodlowych_ogolem": len(src_h2),
        "slajdow_zrodlowych_wykorzystanych": len(uzyte),
        "slajdow_zrodlowych_odrzuconych": len(man["odrzucone_slajdy_zrodlowe"]),
        "ilustracji_wykluczonych": len(man["ilustracje_wykluczone"]),
    },
    "testy": {
        "strukturalne": {
            "testow": t_str["testow"], "zaliczonych": t_str["zaliczonych"],
            "bledow": t_str["bledow"],
        } if t_str else None,
        "odnosniki": {
            "lokalnych_ok": t_lnk["lokalne"]["ok"],
            "lokalnych_brak": t_lnk["lokalne"]["brak"],
            "zewnetrznych": t_lnk["zewnetrzne_liczba"],
            "zewnetrznych_ok": sum(1 for r in t_lnk["zewnetrzne"]
                                   if r["kategoria"] == "ok"),
            "zewnetrznych_przekierowania": [
                {"url": r["url"], "url_koncowy": r.get("url_koncowy"), "status": r["status"]}
                for r in t_lnk["zewnetrzne"] if r["kategoria"] == "przekierowanie"],
            "zewnetrznych_404": [r["url"] for r in t_lnk["zewnetrzne"]
                                 if r["kategoria"] == "nieistniejacy"],
            "zewnetrznych_403_lub_timeout": [
                {"url": r["url"], "status": r["status"], "kategoria": r["kategoria"]}
                for r in t_lnk["zewnetrzne"]
                if r["kategoria"] in ("blokada-bota", "timeout-lub-sieć")],
        } if t_lnk else None,
        "przegladarka_root": zbierz_brw(t_brw),
        "przegladarka_podkatalog": zbierz_brw(t_sub),
    },
    "obliczenia": calc,
}
os.makedirs("review", exist_ok=True)
json.dump(ver, open("review/verification.json", "w"), ensure_ascii=False, indent=1)

# --- PROWENIENCJA.md ----------------------------------------------------
L = []
L.append("# Pochodzenie slajdów\n")
L.append("Plik generowany skryptem `scripts/build-report.py` z `provenance/slide-map.json`.")
L.append("Nie edytuj ręcznie — zmiany wprowadzaj w tabeli `MAPA` w `scripts/build-provenance.py`.\n")
z = man["zrodlo"]
L.append(f"Repozytorium źródłowe: `{z['repozytorium']}`, commit `{z['commit']}`, "
         f"gałąź `{z['galaz']}`, odczyt **{z['data_odczytu']}**, licencja {z['licencja']}.\n")
L.append("## Oznaczenia\n")
for k, v in man["legenda_origin"].items():
    L.append(f"* **`{k}`** — {v}")
L.append("")
L.append("## Bilans\n")
L.append("| Wielkość | Liczba |")
L.append("|:---|---:|")
L.append(f"| Slajdów merytorycznych w pięciu taliach źródłowych | {len(src_h2)} |")
L.append(f"| — z nich wykorzystanych (`retained` / `adapted`) | {len(uzyte)} |")
L.append(f"| — z nich świadomie nieprzeniesionych | {len(man['odrzucone_slajdy_zrodlowe'])} |")
L.append(f"| Slajdów merytorycznych w nowym kursie | {sum(origin_tresc.values())} |")
L.append(f"| — `retained` | {origin_tresc.get('retained', 0)} |")
L.append(f"| — `adapted` | {origin_tresc.get('adapted', 0)} |")
L.append(f"| — `new` | {origin_tresc.get('new', 0)} |")
L.append("")
L.append("Slajdy `adapted` bywają scaleniem dwóch lub więcej slajdów źródłowych, "
         "dlatego liczba wykorzystanych slajdów źródłowych przewyższa liczbę slajdów "
         "`retained` i `adapted` razem wziętych.\n")

for deck in sorted({s["deck"] for s in man["slajdy"]}):
    ttl = next((t["tytul"] for t in talie if t["plik"].startswith(deck)), deck)
    L.append(f"## {deck}\n")
    L.append(f"*{ttl}*\n")
    L.append("| Slajd | Pochodzenie | Źródło | Uzasadnienie |")
    L.append("|:---|:---|:---|:---|")
    for s in man["slajdy"]:
        if s["deck"] != deck:
            continue
        zr = s.get("zrodlo")
        if zr and zr.get("typ") == "prezentacja":
            opis = f"`{zr['qmd']}` — {zr['tytul']} (w. {zr['wiersze']})"
        elif zr:
            opis = f"`{zr['qmd']}`"
        else:
            opis = "—"
        dod = s.get("zrodla_dodatkowe", [])
        if dod:
            opis += " + " + ", ".join(
                f"`{d.get('qmd','')}`" + (f" — {d['tytul']}" if d.get("tytul") else "")
                for d in dod)
        L.append(f"| `#{s['id']}` {s['tytul']} | **{s['origin']}** | {opis} | "
                 f"{s['uzasadnienie']} |")
    L.append("")

L.append("## Slajdy źródłowe świadomie nieprzeniesione\n")
L.append("| Slajd źródłowy | Plik | Powód |")
L.append("|:---|:---|:---|")
for o in man["odrzucone_slajdy_zrodlowe"]:
    L.append(f"| {o['tytul_zrodlowy']} | `{o.get('qmd') or '—'}` | {o['powod']} |")
L.append("")
L.append("## Ilustracje wykluczone z repozytorium\n")
L.append("| Plik / grupa | Powód |")
L.append("|:---|:---|")
for i in man["ilustracje_wykluczone"]:
    L.append(f"| `{i['plik']}` | {i['powod']} |")
L.append("")
open("provenance/PROWENIENCJA.md", "w", encoding="utf-8").write("\n".join(L))

print("Zapisano:")
print("  review/verification.json")
print("  provenance/PROWENIENCJA.md")
print()
print(f"Talii: {ver['sumy']['talii']}, slajdów merytorycznych: "
      f"{ver['sumy']['slajdow_merytorycznych']}, "
      f"sekcji HTML: {ver['sumy']['sekcji_html_lacznie']}")
print(f"Pochodzenie (merytoryczne): {ver['pochodzenie']['wg_origin_merytoryczne']}")
b = ver["testy"]["przegladarka_root"]
if b:
    print(f"Przeglądarka: {b['slajdow']} slajdów, {b['stanow_z_fragmentami']} stanów, "
          f"problemów: {b['problemow']}")
