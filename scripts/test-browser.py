#!/usr/bin/env python3
"""Test przeglądarkowy wszystkich ośmiu talii.

Uruchomienie:
    uv run --with playwright python scripts/test-browser.py
    uv run --with playwright python scripts/test-browser.py --base /iot-course-slides

Dla każdej talii:
  * czeka na Reveal.isReady(),
  * przechodzi PRZEZ WSZYSTKIE slajdy i wszystkie fragmenty,
  * mierzy rzeczywiste przepełnienie treści w układzie slajdu (nie w oknie —
    transformacja skalująca reveal.js nie jest przepełnieniem),
  * sprawdza naturalWidth każdego obrazu po dociągnięciu (lazy load),
  * sprawdza, czy diagramy mermaid wyrenderowały się do SVG,
  * zbiera błędy JS i nieudane żądania sieciowe,
  * zapisuje zrzuty ekranu.

Testujemy w dwóch szerokościach: typowy pulpit i wąskie okno osadzone.
"""
import os, sys, json, time, http.server, socketserver, threading, functools, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
from playwright.sync_api import sync_playwright  # noqa: E402

PORT = int(os.environ.get("TEST_PORT", "8096"))
BASE = ""
if "--base" in sys.argv:
    BASE = sys.argv[sys.argv.index("--base") + 1].rstrip("/")
SERWUJ = "docs" if not BASE else os.path.join(
    os.environ.get("TMPDIR", "/opt/data/cache/scratch"), "iot-podkatalog")

TALIE = [
    "00-internet-przyszlosci",
    "01-architektura-i-wymagania", "02-urzadzenie-sensory-energia",
    "03-lacznosc-i-ota", "04-mqtt-i-kontrakt-danych",
    "05-brzeg-node-red-sheets", "06-thingsboard-ce",
    "07-odpornosc-bezpieczenstwo-eksploatacja",
]
if os.environ.get("TEST_DECKS"):
    wybrane = {x.strip() for x in os.environ["TEST_DECKS"].split(",") if x.strip()}
    TALIE = [t for t in TALIE if t in wybrane]
WIDOKI = [("pulpit", 1440, 810), ("osadzone", 800, 600)]
ZRZUTY = "review/screenshots"

# Skrypt pomiarowy wykonywany na bieżącym slajdzie.
POMIAR = r"""
() => {
  const sec = Reveal.getCurrentSlide();
  if (!sec) return null;
  const cfg = Reveal.getConfig();
  // Mierzymy w układzie współrzędnych slajdu (1600x900), a nie okna.
  // Skalowanie całego slajdu przez reveal.js nie jest przepełnieniem treści.
  const sr = sec.getBoundingClientRect();
  const sc = Reveal.getScale() || 1;
  let prawo = 0, dol = 0, winowajcy = [];
  // MJX_Assistive_MathML to element wyłącznie dla czytników ekranu: MathJax
  // umieszcza go poza obszarem widzenia (clip). Nie jest treścią widoczną,
  // więc nie liczy się jako przepełnienie.
  const pomijany = (el) =>
    el.closest('.MJX_Assistive_MathML') !== null ||
    el.classList.contains('MJX_Assistive_MathML');
  const widoczny = (el) => {
    if (pomijany(el)) return false;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    if (parseFloat(cs.opacity) === 0) return false;
    if (cs.position === 'absolute' && cs.clip && cs.clip !== 'auto') return false;
    return true;
  };
  for (const el of sec.querySelectorAll('*')) {
    if (!widoczny(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    const dx = (r.right - sr.right) / sc;
    const dy = (r.bottom - sr.bottom) / sc;
    if (dx > 2 || dy > 2) {
      if (dx > prawo) prawo = dx;
      if (dy > dol) dol = dy;
      winowajcy.push({tag: el.tagName.toLowerCase(),
                      cls: (el.className.baseVal ?? el.className ?? '').toString().slice(0, 48),
                      dx: Math.round(dx), dy: Math.round(dy)});
    }
  }
  // Wewnętrzne przewijanie: treść, której nie widać bez scrolla.
  let scroll = [];
  for (const el of sec.querySelectorAll('*')) {
    if (!widoczny(el)) continue;
    if (el.scrollHeight - el.clientHeight > 8 && el.clientHeight > 0) {
      const cs = getComputedStyle(el);
      if (cs.overflowY === 'auto' || cs.overflowY === 'scroll' || cs.overflowY === 'hidden') {
        scroll.push({tag: el.tagName.toLowerCase(),
                     nadmiar: el.scrollHeight - el.clientHeight,
                     cls: (el.className ?? '').toString().slice(0, 48)});
      }
    }
  }
  const obrazy = [...sec.querySelectorAll('img')].map(i => ({
    src: i.getAttribute('src'), naturalWidth: i.naturalWidth,
    naturalHeight: i.naturalHeight, complete: i.complete,
    widoczny: i.getBoundingClientRect().width > 0}));
  const mermaid_pre = sec.querySelectorAll('pre.mermaid, .mermaid').length;
  const mermaid_svgs = [...sec.querySelectorAll(
    'svg.flowchart, svg[id^="mermaid-"], svg[aria-roledescription]')];
  const mermaid_svg = mermaid_svgs.length;

  // Mermaid umieszcza etykiety w SVG oraz w HTML wewnątrz foreignObject.
  // Sam diagram może mieścić się na slajdzie, choć tekst wychodzi poza kafelek
  // albo zostaje przycięty wewnątrz foreignObject — dlatego mierzymy oba poziomy.
  const mermaid_tekst = [];
  const poza = (zew, wew, tolerancja = 2) =>
    wew.left < zew.left - tolerancja || wew.top < zew.top - tolerancja ||
    wew.right > zew.right + tolerancja || wew.bottom > zew.bottom + tolerancja;
  for (const svg of mermaid_svgs) {
    const svgBox = svg.getBoundingClientRect();
    for (const node of svg.querySelectorAll('g.node')) {
      const ksztalt = node.querySelector(
        '.label-container, rect.basic, polygon, ellipse, circle, path');
      const etykieta = node.querySelector('.label, .nodeLabel');
      if (ksztalt && etykieta) {
        const kb = ksztalt.getBoundingClientRect();
        const eb = etykieta.getBoundingClientRect();
        if (kb.width > 0 && eb.width > 0 && poza(kb, eb)) {
          mermaid_tekst.push({typ: 'etykieta-poza-wezlem',
            wezel: node.id || null,
            tekst: (etykieta.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 120),
            dx: Math.round(Math.max(0, eb.right - kb.right, kb.left - eb.left)),
            dy: Math.round(Math.max(0, eb.bottom - kb.bottom, kb.top - eb.top))});
        }
      }
    }
    for (const fo of svg.querySelectorAll('foreignObject')) {
      const zawartosc = fo.firstElementChild;
      if (!zawartosc) continue;
      const fb = fo.getBoundingClientRect();
      const zb = zawartosc.getBoundingClientRect();
      const przewija = zawartosc.scrollWidth > zawartosc.clientWidth + 2 ||
                       zawartosc.scrollHeight > zawartosc.clientHeight + 2;
      const ctm = fo.getScreenCTM();
      const skalaDiagramu = ctm ? Math.hypot(ctm.a, ctm.b) / sc : 1;
      const fontSlajdu = parseFloat(getComputedStyle(zawartosc).fontSize) * skalaDiagramu;
      if ((fb.width > 0 && zb.width > 0 && poza(fb, zb)) || przewija) {
        mermaid_tekst.push({typ: 'foreignobject-przyciety',
          tekst: (zawartosc.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 120),
          szerokosc: [Math.round(zb.width), Math.round(fb.width)],
          wysokosc: [Math.round(zb.height), Math.round(fb.height)]});
      }
      if (fb.width > 0 && fontSlajdu < 16) {
        mermaid_tekst.push({typ: 'tekst-za-maly',
          tekst: (zawartosc.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 120),
          fontSlajdu: Math.round(fontSlajdu * 10) / 10});
      }
    }
    for (const tekst of svg.querySelectorAll('text')) {
      const tb = tekst.getBoundingClientRect();
      if (svgBox.width > 0 && tb.width > 0 && poza(svgBox, tb)) {
        mermaid_tekst.push({typ: 'tekst-poza-svg',
          tekst: (tekst.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 120)});
      }
    }
  }
  return {
    id: sec.id, prawo: Math.round(prawo), dol: Math.round(dol),
    winowajcy: winowajcy.slice(0, 5), scroll,
    obrazy, mermaid_pre, mermaid_svg, mermaid_tekst,
    dlugosc_tekstu: (sec.innerText || '').trim().length,
    skala: sc,
  };
}
"""


def uruchom_serwer(katalog, port):
    H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=katalog)
    H.log_message = lambda *a, **k: None
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(("127.0.0.1", port), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def main():
    if BASE:
        # Symulacja hostingu w podkatalogu: /nazwa-repo/…
        import shutil
        cel = os.path.join(SERWUJ, BASE.lstrip("/"))
        shutil.rmtree(SERWUJ, ignore_errors=True)
        os.makedirs(os.path.dirname(cel) or SERWUJ, exist_ok=True)
        shutil.copytree("docs", cel)
        print(f"Symulacja podkatalogu: {cel}")

    os.makedirs(ZRZUTY, exist_ok=True)
    srv = uruchom_serwer(SERWUJ, PORT)
    raport = {"base": BASE or "/", "port": PORT, "talie": [],
              "podsumowanie": {}}
    blad_krytyczny = []

    with sync_playwright() as p:
        b = p.chromium.launch(
            executable_path=os.environ.get("AGENT_BROWSER_EXECUTABLE_PATH"))
        for talia in TALIE:
            wpis = {"talia": talia, "widoki": []}
            for nazwa_widoku, w, hgt in WIDOKI:
                pg = b.new_page(viewport={"width": w, "height": hgt})
                bledy_js, zle_zadania = [], []
                pg.on("console", lambda m: bledy_js.append(m.text)
                      if m.type == "error" else None)
                pg.on("pageerror", lambda e: bledy_js.append(f"PAGEERROR: {e}"))
                pg.on("requestfailed", lambda r: zle_zadania.append(
                    f"{r.url} :: {r.failure}"))
                pg.on("response", lambda r: zle_zadania.append(
                    f"HTTP {r.status} {r.url}") if r.status >= 400 else None)

                url = f"http://127.0.0.1:{PORT}{BASE}/slides/{talia}.html"
                pg.goto(url, wait_until="networkidle")
                pg.wait_for_function("window.Reveal && Reveal.isReady()",
                                     timeout=30000)
                # mermaid renderuje się po starcie reveal
                pg.wait_for_timeout(2500)

                total = pg.evaluate("Reveal.getTotalSlides()")
                slajdy, obrazy_zle, mermaid_zle, mermaid_tekst_zle = [], [], [], []
                przepelnienia, puste = [], []

                pg.evaluate("Reveal.slide(0,0,0)")
                pg.wait_for_timeout(250)
                odwiedzone, kroki, max_krokow = set(), 0, total * 12 + 60
                while kroki < max_krokow:
                    kroki += 1
                    m = pg.evaluate(POMIAR)
                    if m:
                        idx = pg.evaluate("JSON.stringify(Reveal.getIndices())")
                        klucz = (m["id"], idx)
                        if klucz not in odwiedzone:
                            odwiedzone.add(klucz)
                            if m["prawo"] > 4 or m["dol"] > 4:
                                przepelnienia.append(
                                    {"slajd": m["id"], "prawo": m["prawo"],
                                     "dol": m["dol"], "elementy": m["winowajcy"]})
                            if m["scroll"]:
                                przepelnienia.append(
                                    {"slajd": m["id"], "przewijanie": m["scroll"]})
                            for o in m["obrazy"]:
                                if o["widoczny"] and o["naturalWidth"] == 0:
                                    obrazy_zle.append({"slajd": m["id"], **o})
                            if m["mermaid_pre"] and not m["mermaid_svg"]:
                                mermaid_zle.append(m["id"])
                            if m["mermaid_tekst"]:
                                mermaid_tekst_zle.append(
                                    {"slajd": m["id"], "problemy": m["mermaid_tekst"]})
                            if m["dlugosc_tekstu"] < 3:
                                puste.append(m["id"])
                            slajdy.append({"id": m["id"], "indeks": idx,
                                           "prawo": m["prawo"], "dol": m["dol"],
                                           "obrazow": len(m["obrazy"]),
                                           "mermaid_svg": m["mermaid_svg"],
                                           "znakow": m["dlugosc_tekstu"]})
                    if pg.evaluate("Reveal.isLastSlide() && "
                                   "(Reveal.availableFragments().next === false)"):
                        break
                    pg.evaluate("Reveal.next()")
                    pg.wait_for_timeout(110)

                # Zrzuty: równomiernie rozłożone RÓŻNE slajdy całej talii.
                # Ważniejszy jest przegląd wszystkich slajdów niż ładny slajd tytułowy.
                if nazwa_widoku == "pulpit":
                    # Usuń zrzuty tej talii z wcześniejszego przebiegu. Bez tego zmiana
                    # liczby lub identyfikatorów slajdów zostawia nieaktualne pliki.
                    for stary in glob.glob(f"{ZRZUTY}/{talia}__*.png"):
                        os.remove(stary)
                    ids = []
                    for s in slajdy:               # kolejność zachowana, bez duplikatów
                        if s["id"] and s["id"] not in ids:
                            ids.append(s["id"])
                    ile = min(len(ids), int(os.environ.get("ZRZUTOW_NA_TALIE", "8")))
                    krok = max(1, len(ids) // ile)
                    wybrane = ids[::krok][:ile]
                    if ids[-1] not in wybrane:
                        wybrane[-1] = ids[-1]
                    for sid in wybrane:
                        pozycja = ids.index(sid)
                        pg.evaluate(
                            "(sid)=>{const e=document.getElementById(sid);"
                            "const i=Reveal.getIndices(e);Reveal.slide(i.h,i.v||0);}", sid)
                        pg.wait_for_timeout(600)
                        pg.evaluate("()=>{let n=0;while(Reveal.availableFragments().next"
                                    " && n<40){Reveal.nextFragment();n++;}}")
                        pg.wait_for_timeout(450)
                        pg.screenshot(path=f"{ZRZUTY}/{talia}__{pozycja:02d}_{sid[:28]}.png")

                wynik = {
                    "widok": nazwa_widoku, "szerokosc": w, "wysokosc": hgt,
                    "slajdow_reveal": total,
                    "stanow_odwiedzonych": len(odwiedzone),
                    "slajdow_unikalnych": len({s["id"] for s in slajdy}),
                    "przepelnienia": przepelnienia,
                    "obrazy_niezaladowane": obrazy_zle,
                    "mermaid_bez_svg": mermaid_zle,
                    "mermaid_tekst": mermaid_tekst_zle,
                    "slajdy_puste": puste,
                    "bledy_js": bledy_js,
                    "zle_zadania": zle_zadania,
                }
                wpis["widoki"].append(wynik)
                st = ("OK  " if not (przepelnienia or obrazy_zle or mermaid_zle
                                     or mermaid_tekst_zle or wynik["bledy_js"]
                                     or wynik["zle_zadania"] or puste) else "UWAGA")
                print(f"[{st}] {talia} / {nazwa_widoku}: "
                      f"{wynik['slajdow_unikalnych']} slajdów, "
                      f"{len(odwiedzone)} stanów (ze fragmentami), "
                      f"przepełnień={len(przepelnienia)}, "
                      f"obrazów bez dekodowania={len(obrazy_zle)}, "
                      f"mermaid bez svg={len(mermaid_zle)}, "
                      f"problemów tekstu mermaid={len(mermaid_tekst_zle)}, "
                      f"błędów JS={len(wynik['bledy_js'])}, "
                      f"żądań 4xx/5xx={len(wynik['zle_zadania'])}")
                for k in ("przepelnienia", "obrazy_niezaladowane",
                          "mermaid_bez_svg", "mermaid_tekst", "bledy_js",
                          "zle_zadania", "slajdy_puste"):
                    if wynik[k]:
                        blad_krytyczny.append(f"{talia}/{nazwa_widoku}: {k}")
                        for x in wynik[k][:4]:
                            print(f"        {k}: {x}")
                pg.close()
            raport["talie"].append(wpis)
        b.close()
    srv.shutdown()

    raport["podsumowanie"] = {
        "talii": len(TALIE),
        "slajdow_lacznie": sum(v["slajdow_unikalnych"] for t in raport["talie"]
                               for v in t["widoki"] if v["widok"] == "pulpit"),
        "stanow_lacznie": sum(v["stanow_odwiedzonych"] for t in raport["talie"]
                              for v in t["widoki"] if v["widok"] == "pulpit"),
        "problemow": len(blad_krytyczny),
        "problemy": blad_krytyczny,
    }
    nazwa = ("review/verification-browser.json" if not BASE
             else "review/verification-browser-podkatalog.json")
    json.dump(raport, open(nazwa, "w"), ensure_ascii=False, indent=1)
    print(f"\nRazem: {raport['podsumowanie']['slajdow_lacznie']} slajdów, "
          f"{raport['podsumowanie']['stanow_lacznie']} stanów z fragmentami")
    print(f"Zapisano: {nazwa}")
    sys.exit(1 if blad_krytyczny else 0)


if __name__ == "__main__":
    main()
