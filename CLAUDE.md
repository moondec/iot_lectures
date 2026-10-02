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
| `slides/00…07-*.qmd` | **Aktualny kurs** — osiem wykładów (źródło) |
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
- Liczby z rachunków dopisuj do `scripts/verify-calc.py`, a wykresy do `scripts/make-figures.py`.

## Ilustracje

- W repo tylko grafiki z jasną licencją (Wikimedia Commons CC/PD, wykresy własne).
  Każdą dopisz do `THIRD_PARTY_NOTICES.md` i `ILUSTRACJE_WYKORZYSTANE` w `build-provenance.py`,
  a na slajdzie podaj autora i licencję w `.zrodlo`.
- Grafiki bez potwierdzonej licencji (stockowe, zrzuty, kadry) leżą w `private/` (w `.gitignore`).
- Klasy motywu do slajdów obrazowych: `.foto` (zdjęcie na całym tle), `.cytat`, `.wielkie`,
  `.kafelki` (siatka zdjęć), `img.portret`.

## Publikacja

- Repozytorium jest **publiczne**. GitHub Pages serwuje gałąź `main` od katalogu
  głównego, więc kurs jest pod https://moondec.github.io/iot_lectures/docs/,
  a stara wersja pod `/archiwum/`. Każdy push na `main` od razu zmienia stronę.
- `.github/workflows/publish.yml` publikuje dodatkowo na gałąź `gh-pages`,
  której Pages obecnie nie używa.

## Poufność — nie commitować

- `notes/` — materiały prowadzącego z **odpowiedziami do pytań sprawdzających**.
  Nigdy nie umieszczaj ich w slajdach (`::: {.notes}` trafia do publicznego HTML)
  ani w repo. Są w `.gitignore`; leżą tylko w `~/.hermes/iot-course-slides/notes` (WSL).
- `review/REJESTR-KOREKT.md` — wewnętrzny rejestr korekt.
- `Lista_obecnosci.xlsx`, `List.docx` — dane studentów.

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
