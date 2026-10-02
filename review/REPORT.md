# Raport odbioru — osiem prezentacji Quarto

Data wykonania: **1 października 2026**.
Repozytorium: `/opt/data/iot-course-slides`, gałąź `main`, **bez commitów, bez remote, bez publikacji**.

Wszystkie liczby w tym raporcie są **wyliczone kodem** (`scripts/build-report.py`)
z wyników testów i z wyrenderowanego HTML. Maszynowy odpowiednik: `review/verification.json`.

---

## 1. Co powstało

Osiem samodzielnych, edytowalnych plików `.qmd` i wynik ich budowania w `docs/`. Wykład 00 jest zaktualizowaną, zweryfikowaną merytorycznie wersją prezentacji Advanced Slides `Internet_przyszlosci` i prowadzi do modułów 01–07.

| | Tytuł | Slajdy merytoryczne | Przekładki | Diagramy | Tabele | Obrazy |
|:--|:--|--:|--:|--:|--:|--:|
| **00** | Internet przyszłości — obietnice, ryzyka i decyzje | 28 | 5 | 3 | 2 | 0 |
| **01** | Architektura systemu IoT i wymagania | 17 | 3 | 2 | 2 | 1 |
| **02** | Urządzenie, sensory i energia | 20 | 3 | 1 | 7 | 3 |
| **03** | Łączność sieciowa i aktualizacje OTA | 19 | 3 | 3 | 2 | 2 |
| **04** | MQTT i kontrakt danych | 18 | 3 | 4 | 4 | 0 |
| **05** | Brzeg sieci, Node-RED i Google Sheets | 14 | 3 | 3 | 3 | 1 |
| **06** | ThingsBoard CE — telemetria, pulpity i sterowanie | 16 | 3 | 2 | 3 | 0 |
| **07** | Odporność, bezpieczeństwo i eksploatacja | 18 | 4 | 2 | 3 | 0 |
| | **Razem** | **150** | **27** | **20** | **26** | **7** |

Plus 8 slajdów tytułowych — **185 sekcji** w HTML łącznie.
Wszystkie wykłady mieszczą się w założonym przedziale 12–28 slajdów merytorycznych.

Każdy wykład ma: slajd celów z planem drogi, spójną sekwencję od pojęcia do zastosowania,
odniesienie do stanowiska laboratoryjnego, **trzy pytania sprawdzające**, podsumowanie
z przejściem do kolejnego modułu i wykaz źródeł pierwotnych.

---

## 2. Co przeniesiono, co dopisano, co odrzucono

| Wielkość | Liczba |
|:---|---:|
| Slajdów merytorycznych w pięciu taliach źródłowych | **61** |
| — wykorzystanych (jako `retained` lub `adapted`) | **46** |
| — świadomie nieprzeniesionych | **15** |
| Slajdów merytorycznych w nowym kursie | **150** |
| — `retained` (zachowana teza i większość treści) | 8 |
| — `adapted` (przeredagowane, skrócone, scalone, skorygowane) | 28 |
| — `new` (napisane od nowa) | 114 |

**Bilans źródła domknięty: 61 = 46 + 15.** Żaden slajd źródłowy nie został pominięty
bez decyzji — każdy jest albo wykorzystany, albo wymieniony na liście odrzuconych
z uzasadnieniem.

Liczba wykorzystanych slajdów źródłowych (46) przewyższa sumę `retained` + `adapted` (36),
ponieważ część slajdów `adapted` scala dwa lub więcej slajdów źródłowych — na przykład
`01#zastosowania` łączy pięć slajdów aplikacyjnych ze wstępu, a `06#bliźniak` scala
omówienie cyfrowego bliźniaka, które w materiałach źródłowych występowało w dwóch
różnych taliach.

### Skąd pochodzi 114 slajdów `new`

* **66** z materiałów uzupełniających kursu (`uzupelnienie-0X.html`, `sprostowania-0X.html`,
  strona o sprzęcie `cm178__lesson_page51`) oraz z dokumentacji pierwotnej producentów.
* **20** to elementy struktury, których talie źródłowe w ogóle nie miały: slajdy celów,
  pytania sprawdzające i wykazy źródeł (po trzy na wykład, poza wykładem 07).
* **28** tworzy wykład 00: gruntownie przebudowana treść prezentacji Advanced Slides,
  zweryfikowana na podstawie publikacji naukowych i źródeł oficjalnych z lat 2023–2026.

Wysoki udział slajdów `new` wynika z zakresu zadania: **cztery z siedmiu modułów 01–07
docelowych nie istniały w materiałach źródłowych**. Dotyczy to wydania firmware przez OTA
(moduł 03), kontraktu danych (04), przepływu Node-RED i zapisu do arkusza (05) oraz
modelu danych platformy (06). Dopasowanie slajdów wykonane wcześniej
(`frontend/quarto-embed/mapping.json`) odnotowało te braki wprost jako `gaps`.

Pełna mapa slajd po slajdzie, z numerami wierszy w plikach źródłowych i uzasadnieniem
każdej zmiany: **`provenance/PROWENIENCJA.md`** oraz **`provenance/slide-map.json`**.

### Przykłady slajdów świadomie nieprzeniesionych (15 pozycji)

* *Zestawienie Arduino vs ESP vs Raspberry Pi* — tabela oparta na nieaktualnych
  założeniach („Arduino bez radia”, „Raspberry Pi przestarzałe”). Zastąpiona przez
  `02#platformy` i `02#rodzina`, opartymi na płytkach stanowiska.
* *Bezpośredni transfer wrażeń (BCI)*, *Interfejs człowiek-człowiek*, *Czy jesteśmy
  programami?* — ciekawostki bez konsekwencji projektowej.
* *Narzędzia otwartoźródłowe* — treść wchłonięta do modułów 05 i 06 wraz z
  aktualnym opisem statusu licencyjnego; osobny slajd powielałby zawartość.
* *Dziękuję za uwagę (zapowiedź wykładu 3)* — slajd organizacyjny odwołujący się
  do nieaktualnej struktury trzech wykładów.

---

## 3. Korekty merytoryczne materiałów źródłowych

Wcześniejsze bloki „Sprostowanie” zostały usunięte z prezentacji. Zweryfikowane informacje
są teraz podane bezpośrednio jako obowiązująca treść — bez cytowania starego błędu,
porównywania z poprzednią wersją i bez erraty dla studentów. Wewnętrzny rejestr zachowuje
historię decyzji dla prowadzącego. Poniżej 29 najważniejszych korekt:

| Moduł | Co poprawiono |
|:--|:--|
| 01 | Model trójwarstwowy **nie jest** standardem IEEE — to model odniesienia z literatury; norma IEEE 2413-2019 operuje domenami i punktami widzenia |
| 01 | Atrybucja tezy o przełomie 2008–2009: Cisco IBSG (Evans 2011), nie „Cisco Annual Internet Report” |
| 01 | Komputer ubieralny Thorpa: koncepcja 1955, realizacja 1960–61 |
| 02 | **40 mA jest granicą**, nie prądem projektowym; nota ~29 mA dotyczy oryginalnego ESP32 (LX6), a nie ESP32-S3 w Nano ESP32 |
| 02 | „ESP32” to rodzina, nie układ: ESP32-S3 (Xtensa LX7) i ESP32-C3 (RISC-V) nie są zamienne |
| 02 | 7 µA / 240 µA dotyczą samego układu SoC, nie całej płytki |
| 02 | Rozdzielczość ADC to nie dokładność pomiaru |
| 03 | Pasmo 868 MHz nie jest „darmowe” — jest regulowane współczynnikiem wypełnienia |
| 03 | NB-IoT to standard 3GPP Rel. 13 z własną warstwą radiową, nie „nakładka na LTE” |
| 03 | „Samoleczenie” sieci mesh wymaga węzła-routera zasilanego z sieci |
| 03 | Sigfox po przejęciu: sieć rozwijana jako Sigfox 0G przez UnaBiz |
| 03 | **OTA nie jest nadpisaniem firmware** — obraz trafia do drugiej partycji, przełączenie po weryfikacji |
| 04 | Nagłówek MQTT: 2 bajty to minimum nagłówka stałego; realny narzut zależy od długości tematu |
| 04 | Autorstwo MQTT: Stanford-Clark (IBM) i Nipper; dziś standard OASIS / ISO-IEC 20922:2016 |
| 04 | **QoS 2 to „dokładnie raz”, nie „gwarancja dostarczenia”** |
| 04 | Prefiks tematu (`dev/`, `prod/`) porządkuje nazwy, ale **nie izoluje** |
| 04 | CoAP ma tryb potwierdzany — „bez gwarancji dostarczenia” dotyczy tylko `non-confirmable` |
| 05 | Adres wdrożenia Apps Script **jest sekretem**, nie publicznym punktem końcowym |
| 06 | ThingsBoard: platforma daje rozdział **logiczny**, nie fizyczną izolację środowisk |
| 06 | Status licencyjny: wydanie 4.4 opisane jako *source-available*, nie klasyczny open source |
| 06 | QoS 2 **nie jest wspierany** na styku z platformą — idempotencja obowiązkowa |
| 06 | Google Cloud IoT Core: ogłoszenie wycofania sierpień 2022, wyłączenie 16 sierpnia 2023 |
| 06 | Cyfrowy bliźniak to nie wizualizacja 3D |
| 07 | Mirai: atak na Dyn (21.10.2016) i incydent TR-064 w Deutsche Telekom (listopad 2016) to **dwa różne zdarzenia** |
| 07 | „Brak mocy na kryptografię” jest dziś nieprawdą — ESP32-S3/C3 mają akceleratory AES i SHA |
| 07 | X.509 to format certyfikatu, nie algorytm |
| 07 | VLAN bez polityki odmowy domyślnej nie izoluje |
| 07 | Cyber Resilience Act jest **przyjęty**: wejście w życie 10.12.2024, raportowanie od 11.09.2026, pozostałe wymagania od 11.12.2027 |
| 07 | 6G: opóźnienia sub-milisekundowe to cele badawcze, nie parametry wdrożonego standardu |

### Rejestr korekt

Kryterium odbioru z `review/CONTENT-ACCEPTANCE.md` wymaga, żeby poprawki były
**wprowadzone w docelowych slajdach**, a nie dopisane jako errata obok niepoprawnego
stwierdzenia, oraz żeby powstał rejestr w układzie
*źródło → teza błędna → wersja poprawna → dowód → slajd docelowy*.

Rejestr: **`review/REJESTR-KOREKT.md`** — **50 pozycji** (22 błędy faktograficzne,
23 uzupełnione niedomówienia, 5 korekt atrybucji), z cytowanym źródłem dowodu
i identyfikatorem slajdu docelowego przy każdej. Wszystkie **55 cytowanych kotwic
slajdów zweryfikowano** wobec zbudowanego HTML — każda istnieje.

Rejestr zawiera też sekcję **„Przypadki nierozstrzygnięte”** (6 pozycji: licencja
ilustracji M5Stack, prawa do logotypów, pochodzenie zdjęć stockowych, niezmierzony
pobór płytek, nieznana wersja instalacji platformy, wartości oszczędności we wdrożeniach
miejskich). W żadnym z tych przypadków nie podano wymyślonego rozstrzygnięcia.

Kontrola kodu źródłowego i wyrenderowanego HTML potwierdza, że publiczne materiały nie
zawierają klas ani etykiet `sprostowanie`, odwołań do katalogów `provenance/`, `review/`,
`notes/`, skryptów weryfikacyjnych ani komentarzy porównujących treść ze starszą wersją.

### Sprostowanie liczbowe znalezione podczas weryfikacji

Materiały kursu podawały dla przykładowego budżetu energii wartość
**0,19 mA i „około 1,7 Ah na rok”**. Przeliczenie podanych danych wejściowych
(120 mA przez 3 s, 0,05 mA w uśpieniu, cykl 900 s) daje:

```
I_śr  = (120·3 + 0,05·897) / 900 = 0,4498 mA
Q_rok = 0,4498 · 24 · 365        = 3940 mAh = 3,94 Ah
```

Poprawne wartości znajdują się bezpośrednio na slajdzie `02#budzet`; błędnych liczb nie powtarzamy studentom.
Skrypt `scripts/verify-calc.py` reprodukuje także czasy pracy dla wszystkich okresów z tabeli,
a wyniki zapisuje w `provenance/obliczenia.json`.

---

## 4. Budowanie

| Element | Wartość |
|:---|:---|
| Quarto | **1.10.18** (wydanie z 24.07.2026) |
| Archiwum | `quarto-1.10.18-linux-amd64.tar.gz`, 147 010 003 B |
| SHA-256 | `afad071b5bd22c02f2d300695743189d3650e0537a53073e654b630cff2b0c73` |
| Weryfikacja | zgodna z `quarto-1.10.18-checksums.txt` wydawcy |
| Lokalizacja | `/opt/data/tools/quarto/quarto-1.10.18` (katalog użytkownika, bez zmian w systemie) |
| Pandoc / Dart Sass / Deno | 3.10.0 / 1.101.0 / 2.7.14 (składniki Quarto) |
| Katalog wyjściowy | `docs/` — pozwala opublikować Pages bez zmiany konfiguracji |
| Diagramy | `mermaid-format: svg` — render na etapie budowania |
| Ścieżki | wyłącznie względne; **brak odwołań do `/assets`** |
| Zasoby zewnętrzne | brak — skrypty, style, czcionki i ikony serwowane lokalnie |

Polecenie odtwarzające build:

```bash
export PATH="/opt/data/tools/quarto/quarto-1.10.18/bin:$PATH"
export QUARTO_CHROMIUM="$AGENT_BROWSER_EXECUTABLE_PATH"
quarto render
```

---

## 5. Testy — co faktycznie wykonano

### 5.1 Testy strukturalne — **96 / 96 zaliczonych**

`python3 scripts/test-structure.py` → `review/verification-structure.json`

Sprawdzono: dokładnie 8 talii i strona indeksowa · brak dodatkowych stron i oryginalnych
talii w wyniku · obecność slajdów `cele`, `pytania`, `zrodla` i podsumowania w każdej
talii · unikalność identyfikatorów sekcji · **brak elementu `<aside class="notes">`**
w publicznym HTML · brak katalogu `notes/` w `docs/` · brak zaślepek (`TODO`, `FIXME`,
`lorem ipsum`) · **brak sekretów** (klucze prywatne, tokeny Google/GitHub, klucze kont
usługi, adresy IP z portem, endpoint Moodle, hasła w kodzie) · pełne pokrycie manifestem
pochodzenia w obie strony · brak identycznych akapitów dłuższych niż 200 znaków
w dwóch różnych taliach · brak ścieżek bezwzględnych · brak zasobów z CDN · liczba
slajdów merytorycznych w zakresie 12–28.

### 5.2 Odnośniki

`python3 scripts/test-links.py --external` → `review/verification-links.json`

* **297 odnośników lokalnych** (`src`, `href`, `url()` w CSS, `iframe`) — **wszystkie istnieją**, 0 brakujących.
* **70 unikalnych odnośników zewnętrznych**, sprawdzonych metodą HEAD z awaryjnym GET:
  * **67 × HTTP 2xx/3xx** — działają, w tym 17 poprawnych przekierowań;
  * **3 × HTTP 403** — DOI ACM, DOI Sage oraz strona ISO blokują automatyczne żądania;
    klasyfikacja `blokada-bota`, a nie martwy adres;
  * **0 × HTTP 404** — żaden odnośnik nie prowadzi do nieistniejącego zasobu.

Rozróżnienie 403 / timeout od 404 jest zapisane w `review/verification-links.json`
w polu `kategoria`.

### 5.3 Testy przeglądarkowe — **0 problemów**

`uv run --with playwright python scripts/test-browser.py` → `review/verification-browser.json`

Dla każdej z ośmiu talii, w **dwóch szerokościach okna** (pulpit 1440×810 i wąskie
okno osadzone 800×600), czyli **16 przebiegów**:

* oczekiwanie na `Reveal.isReady()`;
* przejście przez **wszystkie slajdy i wszystkie fragmenty** — łącznie
  **185 slajdów i 546 stanów** z rozwiniętymi fragmentami (nie tylko pierwszy i ostatni);
* pomiar przepełnienia treści **w układzie współrzędnych slajdu** (1600×900), z podziałem
  przez współczynnik skalowania — transformacja skalująca reveal.js nie jest liczona
  jako przepełnienie;
* pomiar `naturalWidth` każdego obrazu po dociągnięciu — **0 obrazów bez dekodowania**;
* kontrola, czy każdy diagram mermaid wyrenderował się do SVG — **0 braków**;
* zbieranie błędów JavaScript i żądań ze statusem ≥ 400 — **0 błędów, 0 nieudanych żądań**;
* wykrywanie slajdów pustych — **0**;
* zrzuty ekranu: `review/screenshots/` — **64 pliki, po 8 różnych slajdów z każdej
  talii**, równomiernie rozłożonych, z rozwiniętymi fragmentami. Kontaktówka do
  przeglądu jednym rzutem oka: `review/kontaktowka.html`.

### 5.4 Hosting w podkatalogu — **0 problemów**

`uv run --with playwright python scripts/test-browser.py --base /iot-course-slides`
→ `review/verification-browser-podkatalog.json`

Witryna skopiowana do `/iot-course-slides/` i przetestowana pod tym prefiksem:
te same **185 slajdów, 546 stanów, 16 przebiegów, 0 problemów**. Potwierdza, że
prezentacje zadziałają pod adresem typu `https://<użytkownik>.github.io/<nazwa-repo>/`.

### 5.5 Tła, powiększanie i tryb recenzji — **0 problemów**

`uv run --with playwright python scripts/test-review-mode.py`
→ `review/verification-review-mode.json`

* wszystkie osiem talii ma właściwą klasę i ładuje oryginalne tło: niebieskie dla 00 i 06–07,
  pomarańczowe dla 01–02 oraz zielone dla 03–05;
* tapeta jest mieszana z białą warstwą o kryciu 78%; pomiar tego samego slajdu 1440×810
  wykazał wzrost średniej luminancji z 136,3 do 241,7 w skali 0–255;
* automatyczny przegląd wszystkich talii nie wykrył jasnego tekstu na jasnym tle;
  przekładki sekcyjne zachowują ciemne tło `#0b3b45` i białą typografię;
* kliknięcie grafiki otwiera nakładkę pełnoekranową, a `Esc` ją zamyka;
* `?review=1` zapisuje identyfikator bieżącego slajdu, zaznaczony cytat i komentarz;
* uwaga pozostaje dostępna po odświeżeniu strony, można ją wyczyścić po potwierdzeniu,
  a eksport wykonać do Markdown i JSON.

Po zwiększeniu bazowego fontu Mermaid do 24 px skorygowano też dziedziczone białe znaki
i interlinię etykiet HTML. Pełny test 185 slajdów i 546 stanów potwierdził brak
przepełnień zarówno dla hostowania w katalogu głównym, jak i pod prefiksem.

### 5.6 Podgląd HTTP — potwierdzony odpowiedziami serwera

`scripts/serve.sh 8090` (nasłuch na 127.0.0.1; port 8088 nietknięty)

```
index.html                                  HTTP 200   27 096 B
slides/01-architektura-i-wymagania.html     HTTP 200   79 546 B
slides/02-urzadzenie-sensory-energia.html   HTTP 200   78 098 B
slides/03-lacznosc-i-ota.html               HTTP 200   97 703 B
slides/04-mqtt-i-kontrakt-danych.html       HTTP 200  143 769 B
slides/05-brzeg-node-red-sheets.html        HTTP 200  129 521 B
slides/06-thingsboard-ce.html               HTTP 200   83 848 B
slides/07-odpornosc-bezpieczenstwo-...html  HTTP 200   86 199 B
assets/img/energia-okres.png                HTTP 200  191 650 B
```

**Proces serwera nie przetrwa zakończenia pracy agenta.** Aby uruchomić podgląd:

```bash
cd /opt/data/iot-course-slides && scripts/serve.sh 8090
# potem: http://127.0.0.1:8090/
```

---

## 6. Usterki znalezione i naprawione w trakcie testów

Wszystkie poniższe zostały wykryte **pomiarem w przeglądarce**, nie przez oględziny.

| # | Objaw | Przyczyna | Naprawa |
|:--|:--|:--|:--|
| 1 | Po jednym **pustym slajdzie** na każdą przekładkę sekcyjną (22 puste slajdy w nawigacji) | separator `---` umieszczony bezpośrednio przed nagłówkiem `#` tworzy dodatkowy, pusty slajd poziomu 2 | usunięcie separatorów przed nagłówkami sekcji |
| 2 | Etykiety w diagramach **wychodziły poza obrys węzłów** (do 104 px) | mermaid renderowany w przeglądarce mierzy etykiety na slajdach ukrytych przez `display: none`, więc `foreignObject` dostaje szerokość 0 | `mermaid-format: svg` — render na etapie budowania, bez `foreignObject` |
| 3 | **Błąd JavaScript na każdym slajdzie**: `Cannot read properties of null (reading 'id')` | błąd w `mermaid-postprocess-shim.js` Quarto: `el.querySelector("desc").id` bez sprawdzenia, czy `<desc>` istnieje — a SVG renderowane na etapie budowania go nie mają | lokalne obejście `assets/vendor/mermaid-desc-shim.js` (dodaje pusty `<desc>` na `DOMContentLoaded`) |
| 4 | Dwa slajdy z diagramem sekwencji rozciągnięte do **ponad 4000 px wysokości**, treść SVG wysypana do dokumentu | reguły `@keyframes` w arkuszu stylów osadzonym w SVG były parsowane przez Pandoc jako **cytowania** (`@identyfikator`), co rozrywało element `<svg>` | `from: markdown-citations` — wyłączenie składni cytowań, nieużywanej w kursie |
| 5 | Tabele wystawały **8 px poza prawą krawędź** slajdu | Quarto nadaje dzieciom kolumny margines poziomy 0,25–0,5 rem; przy `width: 100%` sumuje się on z szerokością | wyzerowanie marginesu dla tabel, bloków kodu i rysunków wewnątrz kolumn |
| 6 | Pusty węzeł w diagramie self-testu — tekst zniknął | etykieta `esp_ota_mark_app_invalid_rollback_and_reboot()` przekraczała obrys węzła | skrócenie etykiet; pełne nazwy funkcji podane w tekście pod diagramem |
| 7 | Treść wychodziła poza dolną krawędź na 3 slajdach (21–102 px) | zbyt dużo treści w kolumnie | przeredagowanie i skrócenie `03#ota-granice`, `04#wersjonowanie`, `06#smart-city` |
| 8 | Fałszywe trafienia testu na elementach `MJX_Assistive_MathML` | element MathJax dla czytników ekranu, celowo poza obszarem widzenia | wykluczenie z pomiaru w `scripts/test-browser.py` wraz z uzasadnieniem w kodzie |

Usterki 3 i 4 to **błędy w narzędziach**, nie w treści. Obie mają w kodzie komentarz
z opisem objawu, przyczyny i warunków usunięcia obejścia.

---

## 7. Ilustracje, licencje, prywatność

### Włączone do repozytorium (7 plików)

* **Arduino Nano ESP32** — zdjęcie płytki i oficjalny pinout ABX00083, **CC BY-SA 4.0**,
  z atrybucją na slajdzie i w `THIRD_PARTY_NOTICES.md`; pliki niemodyfikowane.
* **Wykresy autorskie** z repozytorium źródłowego (`iot_growth`, `protocol_bubble`,
  `scatter_triangle`) — wygenerowane skryptami Marka, CC BY 4.0.
* **Dwa wykresy własne** wygenerowane w tym projekcie (`energia-okres`, `sheets-limit`)
  ze skryptu `scripts/make-figures.py`, na danych z `scripts/verify-calc.py`.

### Świadomie niewłączone (15 pozycji, pełna lista w `provenance/slide-map.json`)

* **Materiały M5Stack** (4 pliki: zdjęcia i mapy wyprowadzeń Stamp-C3 i C3U) —
  *all rights reserved*, brak potwierdzonej licencji na redystrybucję.
  **Nie przedstawiamy ich jako CC.** Slajd `02#stamp-c3u` odsyła do dokumentacji
  producenta, a tabela wyprowadzeń została zestawiona z **faktów** z tej dokumentacji.
* **Zdjęcia stockowe i zrzuty ekranu** z prezentacji źródłowych (m.in. `Oura-ring.jpg`,
  `mirai_map.png`, `iot_dashboard.png`, 14 plików `Pasted image 2022*.png`) — brak
  udokumentowanego źródła i licencji.
* **Hotlinki do logotypów uczelni** (`up.poznan.pl`, `wisim.up.poznan.pl`) — usunięte
  zgodnie z wymogiem eliminacji łamanych odnośników; slajdy tytułowe nie zawierają
  logotypów.

Jeżeli prowadzący dysponuje prawami do któregokolwiek z tych materiałów, można je
dodać — decyzja należy do autora kursu.

### Prywatność i sekrety

* Publiczny HTML **nie zawiera notatek prowadzącego** — sprawdzane testem.
* Materiały prowadzącego (scenariusze, odpowiedzi do pytań) są w `notes/`, wyłączonym
  z renderowania. Polityka i konsekwencje dla publikacji: `notes/POLITYKA.md`.
* W repozytorium nie ma tokenów, kluczy, haseł ani adresów instalacji laboratoryjnych.
  Kod przykładowy używa wyłącznie **placeholderów** (`lab/{zespol}/{urzadzenie}/...`,
  `iot-lab-01`); nie przeniesiono kanału `tip2/marek/telemetry` ani żadnych danych
  logowania z materiałów źródłowych.
* Slajdy i notatki wielokrotnie przypominają, że access token urządzenia i adres wdrożenia
  Apps Script nie mogą trafić do sprawozdania ani na zrzut ekranu.

---

## 8. Znane luki i świadome ograniczenia

1. **Trzy źródła zwracają 403** przy automatycznym sprawdzeniu: DOI ACM,
   DOI Sage i `https://www.iso.org/standard/74393.html`. To blokady bota, nie martwe
   odnośniki — potwierdzone kategorią `blokada-bota` w wyniku testu.
2. **Liczby są dydaktyczne, nie pomiarowe.** Budżet energii, tempo wydania OTA i limity
   zapisu do arkusza są rachunkami na założonych wartościach. Rzeczywisty budżet energii
   trzeba zmierzyć na stanowisku — co slajdy wprost mówią.
3. **Prezentacje nie były testowane na rzeczywistym rzutniku** ani na ekranach o innych
   proporcjach niż 16:9. Testy objęły dwie szerokości okna przeglądarki.
4. **Brak wersji anglojęzycznej.** Repozytorium źródłowe zawiera `lectures_en/` z dwiema
   prezentacjami; nie były przedmiotem tego zadania.
5. **Interaktywne dodatki z oryginału zostały usunięte**: wtyczki `appearance` i `pointer`
   oraz `chalkboard`. Nie były niezbędne dydaktycznie, a stanowiły dodatkowe źródło
   ryzyka. Zachowano menu reveal.js (`≡`), nawigację klawiaturą i widok siatki (`Esc`).
6. **Budowanie wymaga przeglądarki** z powodu `mermaid-format: svg`. Bez niej `quarto render`
   zgłosi brak Chromium. Obie drogi obejścia są opisane w `README.md`.
7. **Czas trwania zajęć nie został określony** — nie twierdzimy, że materiał mieści się
   w konkretnej liczbie godzin. Liczba slajdów wynika z zakresu tematu, nie z przyjętego
   czasu.
8. **Prezentacje nie zostały opublikowane.** Brak commitów, brak remote, przebieg
   GitHub Actions wyłączony rozszerzeniem `.disabled` i pozbawiony wyzwalacza `push`.
9. **Moodle nie został zmieniony.** Powiązanie wykładu 00 z kursem jest odłożone do czasu
   zakończenia przeglądu przez prowadzącego.

---

## 9. Co Marek ma ocenić

Uporządkowane od najważniejszego. Do przeglądu wystarczy podgląd lokalny
(`scripts/serve.sh 8090`) albo zrzuty w `review/screenshots/`.

### a) Kolejność modułów i podział treści — **najważniejsze**

Czy ścieżka **01 wymagania → 02 urządzenie → 03 łącze i OTA → 04 kontrakt → 05 brzeg →
06 platforma → 07 eksploatacja** odpowiada Twojemu sposobowi prowadzenia zajęć?
Miejsca warte szczególnej uwagi:

* Czy **OTA** należy do modułu o łączności (03), czy raczej do eksploatacji (07)?
  Obecny układ wiąże je z łączem; argumentem za przeniesieniem byłoby traktowanie
  OTA jako obowiązku eksploatacyjnego.
* Czy **kontrakt danych** (04) nie powinien wyprzedzać łączności (03)? Obecnie MQTT
  poznajemy po tym, jak urządzenie potrafi już utrzymać łącze.
* Czy rama etyczna w module 07 jest we właściwym miejscu, czy powinna otwierać cykl
  tak jak w oryginalnym wstępie?

### b) Głębokość poszczególnych modułów

Moduł **02** ma 20 slajdów merytorycznych i jest najgęstszy — dużo miejsca zajmują dwie
płytki i budżet energii. Moduł **05** ma 14 i jest najlżejszy.
Czy proporcje odpowiadają wadze tematów w Twoim kursie?

### c) Przykłady i przypadek przewodni

Przez wszystkie moduły 01–07 przewija się **jedno stanowisko pilotażowe**
(urządzenie → Wi-Fi → broker → Node-RED → arkusz + platforma).
Czy to właściwy przykład wiodący? Rozważ zwłaszcza:

* Czy zachować **Tree Talker** jako osobny przypadek studyjny? Obecnie jest tylko
  w notatkach prowadzącego (`notes/`), bo dublował rolę stanowiska pilotażowego,
  a jego ilustracja nie ma udokumentowanej licencji.
* Czy przykłady rolnicze i środowiskowe (`01#zastosowania`) są wystarczająco mocne
  dla Twojego kierunku — czy warto dołożyć konkretne dane z Twoich badań.

### d) Korekty wobec starszych materiałów

Decyzja prowadzącego: student widzi wyłącznie zweryfikowaną, aktualną treść. Usunięto
33 wizualnie oznaczone bloki „Sprostowanie”, komentarze o błędach starszych materiałów
i odwołania do wewnętrznej mapy pochodzenia. Historia korekt pozostaje tylko w
`review/REJESTR-KOREKT.md`.

Wcześniejszy osobny slajd z błędnymi wartościami również pozostaje usunięty; studenci
widzą wyłącznie poprawny rachunek na `02#budzet`.

### e) Pytania sprawdzające

Po trzy na wykład, razem **21**. Odpowiedzi wzorcowe są w `notes/`.
Czy poziom trudności odpowiada grupie? Czy pytania nadają się do użycia jako podstawa
zadań domowych albo pytań egzaminacyjnych?

### f) Styl wizualny

Motyw wykorzystuje oryginalne pomarańczowe, zielone i niebieskie tapety wcześniejszych
prezentacji, rozjaśnione białą warstwą dla zachowania kontrastu. Przekładki sekcyjne
pozostają ciemne, a zwykłe slajdy używają ciemnej typografii.

---

## 10. Pliki do przeglądu

| Ścieżka | Zawartość |
|:---|:---|
| `docs/index.html` | strona indeksowa z linkami do ośmiu wykładów |
| `docs/slides/*.html` | osiem zbudowanych prezentacji |
| `slides/*.qmd` | **edytowalne źródła** — zwykłe pliki Quarto, nie wrappery |
| `review/REJESTR-KOREKT.md` | **50 korekt**: źródło → teza błędna → wersja poprawna → dowód → slajd |
| `review/kontaktowka.html` | kontaktówka wszystkich zrzutów, do otwarcia z dysku |
| `review/screenshots/` | 56 zrzutów ekranu (8 różnych slajdów z każdego wykładu, fragmenty rozwinięte) |
| `review/verification.json` | zbiorczy wynik maszynowy wszystkich testów |
| `review/verification-{structure,links,browser,browser-podkatalog}.json` | wyniki poszczególnych testów |
| `provenance/PROWENIENCJA.md` | mapa pochodzenia slajd po slajdzie, czytelna |
| `provenance/slide-map.json` | to samo maszynowo + odrzucone slajdy + wykluczone ilustracje |
| `provenance/obliczenia.json` | wyniki wszystkich rachunków pokazanych na slajdach |
| `notes/` | materiały prowadzącego: scenariusze i odpowiedzi do pytań |
| `THIRD_PARTY_NOTICES.md` | licencje ilustracji i oprogramowania |
| `README.md` | instrukcja budowania, testowania i publikacji |

---

## 11. Stan repozytorium

```
gałąź      : main
commity    : brak
remote     : brak
publikacja : brak; workflow wyłączony (.disabled), bez wyzwalacza push
```

Moodle, repozytorium źródłowe `moondec/iot_lectures` oraz port 8088 pozostały nietknięte.
Poza nowym repozytorium zmieniono wyłącznie `/opt/data/tools/quarto` (instalacja narzędzia
w katalogu użytkownika) i cache Quarto w katalogu domowym.
