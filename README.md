# Internet Rzeczy — kurs w ośmiu wykładach

Materiały wykładowe w formacie Quarto / reveal.js.
Autor: **prof. UPP dr hab. inż. Marek Urbaniak**, Wydział Inżynierii Środowiska
i Inżynierii Mechanicznej, Uniwersytet Przyrodniczy w Poznaniu.

Osiem samodzielnych prezentacji tworzących jedną ścieżkę: od społecznych i technologicznych
konsekwencji Internetu przyszłości, przez granicę systemu i kryterium odbioru, urządzenie,
łącze, kontrakt danych, brzeg sieci i platformę, po odporność i eksploatację.

| | Wykład | Slajdów merytorycznych |
|:--|:--|--:|
| 00 | Internet przyszłości — obietnice, ryzyka i decyzje | 28 |
| 01 | Architektura systemu IoT i wymagania | 17 |
| 02 | Urządzenie, sensory i energia | 20 |
| 03 | Łączność sieciowa i aktualizacje OTA | 19 |
| 04 | MQTT i kontrakt danych | 18 |
| 05 | Brzeg sieci, Node-RED i Google Sheets | 14 |
| 06 | ThingsBoard CE — telemetria, pulpity i sterowanie | 16 |
| 07 | Odporność, bezpieczeństwo i eksploatacja | 18 |

Razem **150 slajdów merytorycznych**, 8 slajdów tytułowych i 27 przekładek sekcyjnych.

## Szybki start

```bash
# 1. Quarto w katalogu użytkownika (weryfikuje sumę kontrolną wydawcy)
scripts/install-quarto.sh
export PATH="/opt/data/tools/quarto/quarto-1.10.18/bin:$PATH"

# 2. Przeglądarka dla mermaid-format: svg — jedna z dwóch dróg
export QUARTO_CHROMIUM="/ścieżka/do/chrome-headless-shell"   # istniejąca binarka
quarto install chromium                                       # albo instalacja przez Quarto

# 3. Budowanie
quarto render

# 4. Podgląd
scripts/serve.sh 8090          # http://127.0.0.1:8090/
```

Wynik trafia do `docs/`. Wszystkie ścieżki są **względne**, więc witryna działa
zarówno pod adresem głównym, jak i w podkatalogu `/nazwa-repo/`.

### Zgłaszanie uwag

Do adresu prezentacji dopisz `?review=1`. Możesz wtedy zaznaczyć fragment tekstu,
kliknąć **💬 Dodaj uwagę** i na końcu skopiować lub pobrać komplet komentarzy.
Instrukcja: `review/FEEDBACK-WORKFLOW.md`. Kliknięcie dowolnej grafiki lub diagramu
Mermaid otwiera powiększenie pełnoekranowe.

## Wymagania

| Składnik | Wersja | Wymagany do |
|:---|:---|:---|
| Quarto CLI | **1.10.18** (przypięta) | budowania |
| Chromium / Chrome headless | dowolna aktualna | renderowania diagramów mermaid do SVG |
| Python | 3.9+ | testów i skryptów |
| `uv` | dowolna | uruchomienia testów przeglądarkowych i generowania wykresów |

R, TeX ani Jupyter nie są potrzebne.

### Dlaczego wymagana jest przeglądarka

Plik `_quarto.yml` ustawia `mermaid-format: svg`, czyli renderowanie diagramów
**na etapie budowania**. Renderowanie po stronie przeglądarki daje w reveal.js błędny
układ: nieaktywne slajdy mają `display: none`, więc mermaid mierzy etykiety jako zerowe
i tekst wychodzi poza obrys węzła (stwierdzone pomiarem, patrz `review/REPORT.md`).

## Budowanie i testy

```bash
quarto render                                                   # pełny build do docs/

python3 scripts/verify-calc.py                                  # przeliczenie wszystkich liczb ze slajdów
uv run --with matplotlib python scripts/make-figures.py         # wykresy własne do assets/img/
python3 scripts/build-provenance.py                             # manifest pochodzenia + kontrola zgodności z HTML

python3 scripts/test-structure.py                               # 96 testów strukturalnych
python3 scripts/test-links.py                                   # odnośniki lokalne (offline)
python3 scripts/test-links.py --external                        # + statusy odnośników zewnętrznych
uv run --with playwright python scripts/test-browser.py         # wszystkie slajdy i fragmenty w przeglądarce
uv run --with playwright python scripts/test-browser.py --base /nazwa-repo   # symulacja hostingu w podkatalogu
```

Test przeglądarkowy wymaga wskazania binarki przeglądarki zmienną
`AGENT_BROWSER_EXECUTABLE_PATH`. Wyniki zapisują się w `review/verification-*.json`,
zrzuty ekranu w `review/screenshots/`.

Kolejność przy pełnej weryfikacji: `verify-calc` → `make-figures` → `quarto render`
→ `build-provenance` → testy.

## Struktura repozytorium

```
_quarto.yml            konfiguracja projektu (lista renderowanych plików, motyw, mermaid)
index.qmd              strona indeksowa
slides/00..07-*.qmd    osiem wykładów — zwykłe, edytowalne pliki Quarto
assets/theme/          wspólny motyw SCSS + arkusz strony indeksowej
assets/img/            ilustracje (patrz THIRD_PARTY_NOTICES.md)
assets/vendor/         bootstrap-icons (MIT) i lokalne obejście błędu Quarto
notes/                 materiały prowadzącego — tylko lokalnie, poza repozytorium (.gitignore)
scripts/               instalacja, generowanie wykresów, manifest, testy, serwer podglądu
provenance/            mapa pochodzenia slajdów, inwentarz źródeł, wyniki obliczeń
review/                raport odbioru, wyniki testów w JSON (zrzuty ekranu i logi poza repozytorium)
docs/                  wynik budowania
.github/workflows/     publikacja na GitHub Pages po każdym wypchnięciu na main
```

## Notatki prowadzącego

Publiczne prezentacje **nie zawierają** notatek dydaktycznych ani odpowiedzi do pytań
sprawdzających. Notatki reveal.js (`::: {.notes}`) trafiają do publicznego kodu HTML,
więc scenariusze i odpowiedzi trzymamy w katalogu `notes/`, wyłączonym z renderowania.
Zasady i konsekwencje dla publikacji opisuje **`notes/POLITYKA.md`**.

Test strukturalny sprawdza po każdym budowaniu, że w `docs/` nie ma elementu
`<aside class="notes">`.

## Pochodzenie treści

Wykłady 01–07 powstały przez **wybór i redakcję** slajdów z pięciu wcześniejszych talii
z repozytorium [`moondec/iot_lectures`](https://github.com/moondec/iot_lectures)
(commit `c62ccf6174fea4db9d0c0bfefef174fca4b0f709`, gałąź `main`, odczyt 30.09.2026,
CC BY 4.0), uzupełnione o tematy nieobecne w materiałach źródłowych — przede wszystkim
OTA, kontrakt danych, przepływ na brzegu sieci i model danych platformy. Wykład 00 jest
pełną aktualizacją prezentacji Advanced Slides `Internet_przyszlosci`: zachowuje jej pytanie
o społeczny wymiar technologii, ale weryfikuje tezy na podstawie źródeł pierwotnych i prowadzi
bezpośrednio do wymagań rozwijanych w modułach 01–07.

Każdy slajd ma wpis w `provenance/slide-map.json` z oznaczeniem pochodzenia
(`retained` / `adapted` / `new`), wskazaniem slajdu źródłowego i uzasadnieniem zmian.
Plik zawiera również listę **15 slajdów źródłowych świadomie nieprzeniesionych**
wraz z powodami oraz listę wykluczonych ilustracji. Skrót w `provenance/PROWENIENCJA.md`.

Korekty merytoryczne są wprowadzone **bezpośrednio w treści**, bez etykiet „sprostowanie",
porównywania ze starszymi materiałami i erraty skierowanej do studentów. Historia decyzji pozostaje
wyłącznie w wewnętrznym rejestrze prowadzącego.

Pełny rejestr w układzie *źródło → teza błędna → wersja poprawna → dowód → slajd docelowy*:
**`review/REJESTR-KOREKT.md`** (50 pozycji) — wraz z listą przypadków, których
świadomie **nie** rozstrzygnięto.

## Liczby na slajdach

Wszystkie wartości podane jako wynik rachunku pochodzą ze skryptu
`scripts/verify-calc.py`; wyniki zapisano w `provenance/obliczenia.json`.
Liczby są **dydaktyczne**, nie pomiarowe — nie pochodzą z pomiarów na stanowisku
i tak są opisane na slajdach.

## Sprzęt stanowiska

Kurs pracuje na dwóch potwierdzonych płytkach:

* **Arduino Nano ESP32 (ABX00083)** — moduł u-blox NORA-W106-10B z układem ESP32-S3
  (rdzeń Xtensa LX7, dwurdzeniowy);
* **M5Stack Stamp-C3U (SKU C122-B)** — układ ESP32-C3 (rdzeń RISC-V, jednordzeniowy),
  z natywnym USB-Serial/JTAG, **bez** mostka CH9102.

Płytki nie są zamienne: różni je architektura rdzenia, numeracja wyprowadzeń i sposób
komunikacji z komputerem. Stamp-C3U to **nie** Stamp-C3 — różnice opisuje wykład 02.

## Publikacja

* przebieg `.github/workflows/publish.yml` uruchamia się po każdym wypchnięciu na `main`:
  instaluje Quarto 1.10.18 i Chromium, renderuje projekt i publikuje go na gałąź `gh-pages`;
* repozytorium jest publiczne — dlatego katalog `notes/` jest w `.gitignore`;
* nazwa repozytorium GitHub nie jest nigdzie zakładana; wszystkie odnośniki są względne;
* katalog `docs/` jest śledzony jako podgląd lokalnego budowania.

Przed publikacją warto przejrzeć `THIRD_PARTY_NOTICES.md` — sekcja o ilustracjach
świadomie niewłączonych do repozytorium.

## Licencja

Tekst slajdów i wykresy własne: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.pl)
(plik `LICENSE`).
Ilustracje Arduino: CC BY-SA 4.0. Bootstrap Icons: MIT.
Pełny wykaz: `THIRD_PARTY_NOTICES.md`.
