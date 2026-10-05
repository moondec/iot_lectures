# Budowa systemów Internetu Rzeczy — materiały kursu

Wykłady (Quarto / reveal.js) do kursu prowadzonego w Moodle UPP
(https://elearning2.up.poznan.pl/). Autor: Marek Urbaniak. Licencja CC BY 4.0.

## Komunikacja i konwencje

- Z użytkownikiem rozmawiaj po polsku. Treść slajdów jest po polsku (`lang: pl`).
- Komentarze w kodzie, nazwy zmiennych i komunikaty commitów — po angielsku.
- Pracuj na gałęzi, nie na `main` (patrz „Publikacja”). Commity z adresem
  `15210450+moondec@users.noreply.github.com` (ustawiony w `git config --local`);
  GitHub odrzuca pushe z prywatnym adresem e-mail.

## Struktura repozytorium

| Ścieżka | Zawartość |
|:--|:--|
| `slides/00…06-*.qmd` | **Aktualny kurs** — siedem wykładów (źródło): 00 wstęp i moduły 01–06 |
| `index.qmd`, `_quarto.yml` | Strona startowa i konfiguracja projektu |
| `assets/` | Motyw SCSS (`assets/theme/iot.scss`), ilustracje, skrypty JS |
| `docs/` | Wynik `quarto render` — **śledzony w git**, to on jest publikowany |
| `scripts/` | Testy (`test-structure.py`, `test-links.py`, `test-browser.py`), wykresy, obliczenia |
| `provenance/`, `review/` | Pochodzenie slajdów, raporty odbioru, wyniki testów JSON |
| `wyklad_1..3.qmd`, `wyklad_intro_1..2.qmd` | **Poprzednie 5 wykładów** — zachowane, nie są renderowane |
| `archiwum/` | Wyrenderowana poprzednia wersja strony (5 wykładów, `lectures_en`) |
| `konspekt.qmd`, `lectures_en/` | Program kursu i wersja angielska — nie są renderowane |
| `quiz/`, `moodle/`, `generuj_pytania*.py`, `quiz_iot.xml` | Banki pytań Moodle XML i ich generatory |

`_quarto.yml` ma jawną listę `project.render` (tylko `index.qmd` i `slides/`).
Nowy plik do strony trzeba do niej dopisać. Stare `wyklad_*.qmd` nie zbudują się
z obecną konfiguracją (motyw `../assets/...` jest względny wobec `slides/`).

## Budowanie i testy

- Quarto **1.10.18** (przypięte) + Chromium dla `mermaid-format: svg`
  (`QUARTO_CHROMIUM` albo `quarto install chromium`). Na Windows Quarto nie ma —
  buduj w WSL. Szczegóły: `README.md`.
- Najprościej budować w kontenerze `hermes` (ma Quarto i Chromium):
  `bash ~/.hermes/build/rebuild.sh 00-internet-przyszlosci` w WSL kopiuje repo do
  `~/.hermes/build/iot_lectures`, renderuje i robi zrzuty slajdów. Wynik `docs/` trzeba
  skopiować z powrotem do repo.
- Po każdym budowaniu: `python3 scripts/build-provenance.py`, `python3 scripts/test-structure.py`
  i `python3 scripts/test-links.py`. Każdy slajd (`#id`) musi mieć wpis w tabeli `MAPA`
  w `scripts/build-provenance.py`.
- Po zmianie diagramu Mermaid uruchom `python3 scripts/mermaid-aspect.py docs/slides slides/*.qmd` i zbuduj ponownie: ustawia `fig-height` tak, by ramka SVG miała proporcje rysunku (bez pustych pasów). Wysokość ograniczają klasy `.kompakt` (380 px), `.sredni` (360 px), `.mermaid-wysoka` (640 px). Polskie litery w etykietach Mermaid czasem psują się (Windows-1250) — sprawdź wynik `grep -l 'Ä…' docs/slides/*.html`; encje `#261;` nie działają w eksporcie SVG.
- Układ slajdów: `uv run --with playwright python scripts/test-layout.py docs OUT 0*.html` (sam uruchamia lokalny serwer; potrzebuje Chromium w QUARTO_CHROMIUM) zgłasza tekst wchodzący na stopkę/przyciski (z zapasem 8 px), wyjście poza krawędź lub kolumnę, przepełnione ramki oraz nakładające się etykiety Mermaid; zrzuty zgłoszonych slajdów trafiają do OUT. Wynik ma być TOTAL 0.
- Liczby z rachunków dopisuj do `scripts/verify-calc.py`, a wykresy do `scripts/make-figures.py`.

## Ilustracje

- W repo tylko grafiki z jasną licencją (Wikimedia Commons CC/PD, wykresy własne).
  Każdą dopisz do `THIRD_PARTY_NOTICES.md` i `ILUSTRACJE_WYKORZYSTANE` w `build-provenance.py`,
  a na slajdzie podaj autora i licencję w `.zrodlo`.
- Grafiki bez potwierdzonej licencji (stockowe, zrzuty, kadry) leżą w `private/` (w `.gitignore`), w tym dawne `img/` i `archiwum/img/` w `private/img/legacy/`. Stare `wyklad_*.qmd`, `lectures_en/` i `archiwum/` odwołują się do nich, więc publicznie wyświetlają się bez tych obrazów.
- Diagramy Mermaid mają czcionkę `Arial, Liberation Sans` w `themeVariables.fontFamily` (dla sekwencji też `sequence.*FontFamily`): kontener mierzy tekst czcionką Liberation Sans, metrycznie zgodną z Arial w Windows/macOS. Domyślna `trebuchet ms` powodowała wychodzenie tekstu z kafelków w przeglądarce.
- Element pokazywany razem z punktem listy przyrostowej: `* []{#id}tekst` i `::: {.fragment data-razem-z="id"}` (`assets/vendor/fragment-razem.js`).
- Tabele zajmujące mało miejsca: `::: {.tabela-duza}` (0,86 em), przy dłuższych komórkach
  `::: {.tabela-srednia}` (0,72 em). `.tabela-gesta` nie działa (przegrywa z regułą motywu
  dla tabel) — zostawiona, by nie zmieniać mieszczących się slajdów. Po zmianie sprawdź `test-layout.py`.
- Klasy motywu do slajdów obrazowych: `.foto` (zdjęcie na całym tle), `.cytat`, `.wielkie`,
  `.kafelki` (siatka zdjęć), `img.portret`.

## Publikacja

- Repozytorium jest **publiczne**. GitHub Pages serwuje katalog `docs/` gałęzi `main`
  (sprawdzone 2.10.2026), więc kurs jest pod https://moondec.github.io/iot_lectures/
  (wykłady: `/slides/0X-….html`), a stara wersja pod `/archiwum/`. Każdy push na `main`
  od razu zmienia stronę.
- `archiwum/` i `img/kbig.jpg` są w `project.resources`, więc trafiają do `docs/archiwum/`
  i `docs/img/`. Dawne adresy (`wyklad_*.html`, `konspekt.html`, `lectures_en/*`, także z
  przedrostkiem `docs/` z czasów, gdy Pages serwował katalog główny) to strony
  przekierowujące do `archiwum/` z zachowaniem `#/slajdu`. Tworzy je
  `scripts/legacy-redirects.py` (post-render); testy je dopuszczają, a `test-links.py`
  pomija zamrożone `docs/archiwum/`.
- Nie ma workflow GitHub Actions ani gałęzi `gh-pages` (usunięte 2.10.2026 — nigdy
  nie działały). `docs/` budujemy lokalnie i commitujemy.

## Poufność — nie commitować

- `notes/` — materiały prowadzącego z **odpowiedziami do pytań sprawdzających**.
  Nigdy nie umieszczaj ich w slajdach (`::: {.notes}` trafia do publicznego HTML)
  ani w repo. Są w `.gitignore`; leżą tylko w `~/.hermes/iot-course-slides/notes` (WSL).
- `review/REJESTR-KOREKT.md` — wewnętrzny rejestr korekt.
- `Lista_obecnosci.xlsx`, `List.docx` — dane studentów.

## Platforma na zajęciach

- Architektura (od 5.10.2026): płytka łączy się przez MQTT bezpośrednio z ThingsBoard CE (API urządzenia `v1/devices/me/…`, token, TLS 8883). Node-RED, kursowy broker Mosquitto (drzewo `lab/…`) i Google Sheets zostały usunięte z kursu — nie wprowadzaj ich z powrotem. Dawne `05-brzeg-node-red-sheets` usunięte, `06`→`05`, `07`→`06` (przekierowania w `scripts/legacy-redirects.py`).

- ThingsBoard **CE 4.3 LTS** (Apache 2.0, wsparcie do 20.07.2027), nie 4.4 (BSL).

## Środowisko lokalne (Windows + WSL Ubuntu 20.04 + Docker)

- **Moodle 4.5.4+** pod http://localhost:8088 (kontener `moodle-lab-web-1`, kod w
  `/home/marek/.hermes/moodle-lab/src/moodle`). Kurs roboczy: **PILOT — Budowa systemów
  Internetu Rzeczy, id=10**. Po skończeniu kurs trafia na serwer uczelni jako kopia `.mbz`.
  Serwer docelowy musi mieć tę samą lub nowszą wersję Moodle.
- Web services w Moodle są **wyłączone**. Zmiany przez CLI: `docker exec moodle-lab-web-1 php
  admin/cli/{backup,restore_backup,import}.php`. Kopie `.mbz` w `/home/marek/.hermes/inbox`
  (w kontenerze: `/backups`). Zmiany konfiguracji Moodle uzgadniaj z użytkownikiem.
- Agent **Hermes** (kontenery `hermes*`) przygotował slajdy w `/home/marek/.hermes/iot-course-slides`
  i serwuje podgląd na http://localhost:8090. To repo jest teraz źródłem prawdy;
  dalsza praca nad slajdami powinna się odbywać tutaj.
