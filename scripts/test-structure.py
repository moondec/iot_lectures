#!/usr/bin/env python3
"""Testy strukturalne zbudowanej witryny.

Uruchomienie:  python3 scripts/test-structure.py
Wynik:         review/verification-structure.json  (+ kod wyjścia 1 przy błędzie)

Sprawdza: liczbę talii, obecność slajdów obowiązkowych, unikalność identyfikatorów,
brak notatek prowadzącego w HTML, brak sekretów i zaślepek, pokrycie manifestem
pochodzenia, brak zduplikowanych bloków treści między taliami.
"""
import json, os, re, sys, glob, hashlib, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
DOCS = "docs"
SLIDES = sorted(glob.glob(f"{DOCS}/slides/*.html"))

wyniki, bledy = [], []


def spr(nazwa, ok, szczegol=""):
    wyniki.append({"test": nazwa, "ok": bool(ok), "szczegol": szczegol})
    if not ok:
        bledy.append(f"{nazwa}: {szczegol}")
    print(f"[{'OK ' if ok else 'BŁĄD'}] {nazwa}" + (f" — {szczegol}" if szczegol else ""))


def tekst(html):
    """Surowy tekst slajdów bez skryptów, stylów i znaczników."""
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t)


# --- 1. Dokładnie osiem talii i strona indeksowa ------------------------
spr("Liczba talii = 8", len(SLIDES) == 8, f"znaleziono {len(SLIDES)}")
spr("Strona indeksowa istnieje", os.path.isfile(f"{DOCS}/index.html"))

obce = [p for p in glob.glob(f"{DOCS}/*.html") if os.path.basename(p) != "index.html"]
spr("Brak dodatkowych stron w katalogu głównym", not obce, str(obce))

# Stare talie nie mogą trafić do publikacji.
stare = [p for p in glob.glob(f"{DOCS}/**/*.html", recursive=True)
         if re.search(r"wyklad_(intro_)?\d", os.path.basename(p))]
spr("Brak oryginalnych talii w wyniku", not stare, str(stare))

# --- 2. Slajdy obowiązkowe w każdej talii -------------------------------
WYMAGANE = {
    "cele": "cele/agenda",
    "pytania": "pytania sprawdzające",
    "zrodla": "źródła",
}
for f in SLIDES:
    h = open(f, encoding="utf-8").read()
    ids = re.findall(r'<section[^>]*\bid="([^"]*)"', h)
    nazwa = os.path.basename(f)
    brak = [op for sid, op in WYMAGANE.items() if sid not in ids]
    spr(f"{nazwa}: slajdy obowiązkowe", not brak, f"brakuje: {brak}" if brak else "")
    ma_podsum = "podsumowanie" in ids or "zamkniecie" in ids
    spr(f"{nazwa}: podsumowanie / zamknięcie", ma_podsum)

# --- 3. Unikalność identyfikatorów sekcji -------------------------------
for f in SLIDES:
    h = open(f, encoding="utf-8").read()
    ids = re.findall(r'<section[^>]*\bid="([^"]*)"', h)
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    spr(f"{os.path.basename(f)}: identyfikatory unikalne", not dup, str(dup))

# --- 4. Brak notatek prowadzącego w publicznym HTML ---------------------
for f in SLIDES + [f"{DOCS}/index.html"]:
    h = open(f, encoding="utf-8").read()
    n = h.count('<aside class="notes"')
    spr(f"{os.path.basename(f)}: brak aside.notes", n == 0, f"znaleziono {n}")

# notes/ nie może trafić do wyniku renderowania
spr("Katalog notes/ poza wynikiem", not os.path.exists(f"{DOCS}/notes"))

# --- 5. Brak zaślepek i niedokończonych fragmentów ----------------------
WZORCE = [r"\bTODO\b", r"\bFIXME\b", r"\bTBD\b", r"\bLorem ipsum\b",
          r"\bXXX\b", r"\[placeholder\]", r"\bdo uzupełnienia\b"]
for f in SLIDES + [f"{DOCS}/index.html"]:
    t = tekst(open(f, encoding="utf-8").read())
    trafienia = [w for w in WZORCE if re.search(w, t, re.I)]
    spr(f"{os.path.basename(f)}: brak zaślepek", not trafienia, str(trafienia))

# --- 6. Brak metakomentarzy o budowie, korektach i pochodzeniu ------------
# Historia redakcji zostaje w review/ i provenance/, ale nie trafia do materiału dla studentów.
META_PUBLICZNE = [
    r"\bsprostowanie\b",
    r"(?:provenance|review|notes)/",
    r"scripts/verify-calc\.py",
    r"slide-map\.json",
    r"REJESTR-KOREKT",
    r"prezentacj[ae] źródłow",
    r"starsz(?:e|ych) materiał",
    r"materiał(?:ach|ów) źródłow",
]
for f in SLIDES + [f"{DOCS}/index.html"]:
    t = tekst(open(f, encoding="utf-8").read())
    trafienia = [w for w in META_PUBLICZNE if re.search(w, t, re.I)]
    spr(f"{os.path.basename(f)}: brak metakomentarzy redakcyjnych",
        not trafienia, str(trafienia))

# --- 7. Brak sekretów i adresów laboratoryjnych -------------------------
# Wzorce celowo wąskie: szukamy realnych poświadczeń, nie słowa "token" w tekście.
SEKRETY = [
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "klucz prywatny"),
    (r"\bAIza[0-9A-Za-z_\-]{30,}", "klucz API Google"),
    (r"\bya29\.[0-9A-Za-z_\-]{20,}", "token OAuth Google"),
    (r"\bghp_[0-9A-Za-z]{30,}", "token GitHub"),
    (r'"private_key_id"\s*:', "klucz konta usługi"),
    (r"\b\d{1,3}(?:\.\d{1,3}){3}:\d{2,5}\b", "adres IP z portem"),
    (r"localhost:8088", "endpoint Moodle"),
    (r"\bmqtt://[^\s\"<]+", "adres brokera w URL"),
    (r"password\s*[=:]\s*[\"'][^\"'\s]{3,}", "hasło w kodzie"),
]
for f in SLIDES + [f"{DOCS}/index.html"]:
    h = open(f, encoding="utf-8").read()
    znalezione = [op for wz, op in SEKRETY if re.search(wz, h)]
    spr(f"{os.path.basename(f)}: brak sekretów", not znalezione, str(znalezione))

# --- 7. Pokrycie manifestem pochodzenia ---------------------------------
MAN = "provenance/slide-map.json"
if os.path.isfile(MAN):
    man = json.load(open(MAN, encoding="utf-8"))
    mapowane = {(s["deck"], s["id"]) for s in man["slajdy"]}
    brakujace, nadmiarowe = [], []
    for f in SLIDES:
        deck = os.path.basename(f).replace(".html", "")
        h = open(f, encoding="utf-8").read()
        ids = [i for i in re.findall(r'<section[^>]*\bid="([^"]*)"', h)]
        for i in ids:
            if (deck, i) not in mapowane:
                brakujace.append(f"{deck}#{i}")
        for d, i in mapowane:
            if d == deck and i not in ids:
                nadmiarowe.append(f"{d}#{i}")
    spr("Manifest pokrywa wszystkie wyrenderowane slajdy", not brakujace,
        f"bez wpisu: {brakujace[:8]}")
    spr("Manifest nie zawiera slajdów nieistniejących", not nadmiarowe,
        f"nadmiarowe: {sorted(set(nadmiarowe))[:8]}")
    origins = collections.Counter(s["origin"] for s in man["slajdy"])
    spr("Manifest: dozwolone wartości origin",
        set(origins) <= {"retained", "adapted", "new"}, str(dict(origins)))
    bez_uzas = [s["id"] for s in man["slajdy"]
                if s["origin"] != "new" and not s.get("zrodlo", {}).get("qmd")]
    spr("Slajdy retained/adapted mają wskazane źródło", not bez_uzas, str(bez_uzas[:8]))
else:
    spr("Manifest pochodzenia istnieje", False, f"brak {MAN}")

# --- 8. Brak powielonych bloków treści między taliami -------------------
# Porównujemy akapity o długości >200 znaków; krótkie powtórzenia
# (przypomnienia, nagłówki) są dopuszczalne.
akapity = collections.defaultdict(list)
for f in SLIDES:
    h = open(f, encoding="utf-8").read()
    for m in re.findall(r"<p[^>]*>(.*?)</p>", h, flags=re.S):
        t = re.sub(r"<[^>]+>", " ", m)
        t = re.sub(r"\s+", " ", t).strip()
        if len(t) > 200:
            akapity[hashlib.sha1(t.encode()).hexdigest()].append(
                (os.path.basename(f), t[:70]))
powtorzone = {k: v for k, v in akapity.items() if len({x[0] for x in v}) > 1}
spr("Brak identycznych długich akapitów w dwóch taliach", not powtorzone,
    str([v[0][1] for v in powtorzone.values()][:3]))

# --- 9. Ścieżki względne (działanie pod /nazwa-repo/) -------------------
for f in SLIDES + [f"{DOCS}/index.html"]:
    h = open(f, encoding="utf-8").read()
    abs_ref = re.findall(r'(?:src|href)="(/(?!/)[^"]*)"', h)
    spr(f"{os.path.basename(f)}: brak ścieżek bezwzględnych",
        not abs_ref, str(abs_ref[:5]))

# --- 10. Zasoby lokalne, nie z CDN --------------------------------------
for f in SLIDES + [f"{DOCS}/index.html"]:
    h = open(f, encoding="utf-8").read()
    zdalne = re.findall(r'<(?:script|link)[^>]*(?:src|href)="(https?://[^"]+)"', h)
    spr(f"{os.path.basename(f)}: skrypty i style lokalne", not zdalne, str(zdalne[:3]))

# --- 11. Liczba slajdów merytorycznych w zakresie -----------------------
for f in SLIDES:
    h = open(f, encoding="utf-8").read()
    ids = re.findall(r'<section[^>]*\bid="([^"]*)"', h)
    tytul = sum(1 for i in ids if i == "title-slide")
    sekcje = len(re.findall(r'<section[^>]*class="[^"]*sekcja', h))
    tresc = len(ids) - tytul - sekcje
    spr(f"{os.path.basename(f)}: {tresc} slajdów merytorycznych w zakresie 12–28",
        12 <= tresc <= 28, f"{tresc}")

# --- Zapis wyniku -------------------------------------------------------
os.makedirs("review", exist_ok=True)
podsumowanie = {
    "testow": len(wyniki),
    "zaliczonych": sum(1 for w in wyniki if w["ok"]),
    "bledow": len(bledy),
    "talie": [os.path.basename(f) for f in SLIDES],
    "wyniki": wyniki,
}
json.dump(podsumowanie, open("review/verification-structure.json", "w"),
          ensure_ascii=False, indent=1)
print(f"\n{podsumowanie['zaliczonych']}/{podsumowanie['testow']} testów zaliczonych")
if bledy:
    print("\nBŁĘDY:")
    for b in bledy:
        print("  -", b)
sys.exit(1 if bledy else 0)
