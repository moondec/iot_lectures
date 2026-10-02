# Materiały i oprogramowanie osób trzecich

Tekst slajdów oraz wykresy własne są objęte licencją **CC BY 4.0** (plik `LICENSE`).
Poniżej wymieniono wszystko, co pochodzi od osób trzecich, wraz z licencją i sposobem użycia.

## Ilustracje w repozytorium (`assets/img/`)

| Plik | Autor / źródło | Licencja | Uwagi |
|:---|:---|:---|:---|
| `arduino-nano-esp32-board.png` | Arduino — [docs.arduino.cc](https://docs.arduino.cc/hardware/nano-esp32/) | **CC BY-SA 4.0** | zdjęcie płytki z dokumentacji produktu; plik niemodyfikowany |
| `arduino-nano-esp32-pinout.png` | Arduino — [Nano ESP32 Full Pinout, SKU ABX00083](https://docs.arduino.cc/resources/pinouts/ABX00083-full-pinout.pdf), aktualizacja 5.12.2023 | **CC BY-SA 4.0** (nadruk licencji na rysunku) | plik niemodyfikowany |
| `iot_growth.png` | Marek Urbaniak — wykres wygenerowany skryptem `generate_charts.py` w repozytorium `moondec/iot_lectures` | **CC BY 4.0** | dane poglądowe; atrybucja tezy: Cisco IBSG (D. Evans, 2011) |
| `protocol_bubble.png` | jak wyżej | **CC BY 4.0** | wartości poglądowe |
| `scatter_triangle.png` | Marek Urbaniak — `generate_scatter.py` / `generate_scatter.R` | **CC BY 4.0** | wartości poglądowe |
| `energia-okres.png` | ten projekt — `scripts/make-figures.py` | **CC BY 4.0** | dane z `scripts/verify-calc.py` |
| `sheets-limit.png` | ten projekt — `scripts/make-figures.py` | **CC BY 4.0** | limity wg dokumentacji Google Sheets API v4 |
| `irrigation-navfac.jpg` | NAVFAC — [test systemu oszczędnego nawadniania](https://commons.wikimedia.org/wiki/File:New_water-saving_irrigation_system_tested_at_NAVFAC_EXWC_(8099733341).jpg) | **CC BY 2.0** | pomniejszona fotografia; użyta w `00#rolnictwo` |
| `iiot-building-blocks.jpg` | Sujata Tilak, Ascent Intellimation — [IIoT System Building Blocks](https://commons.wikimedia.org/wiki/File:IIoT_System_Building_Blocks.jpg) | **CC BY-SA 4.0** | pomniejszona ilustracja; użyta w `01#warstwy` |
| `kerlink-lorawan-gateway.jpg` | Fabian Horst — [Kerlink LoRaWAN Gateway in Kiel](https://commons.wikimedia.org/wiki/File:2020-10-05_-_Kerlink_LoRaWAN_Gateway_in_Kiel.jpg) | **CC BY-SA 4.0** | pomniejszona fotografia urządzenia producenta; użyta w `03#brama-lorawan` |
| `mqtt-broker-listeners.svg` | Ademant — [MQTT single broker multiple listener](https://commons.wikimedia.org/wiki/File:MQTT_single_broker_multiple_listener.svg) | **CC BY-SA 4.0** | niezmodyfikowany diagram SVG; użyty w `04#mqtt` |
| `node-red-example.png` | 1-Byte — [Node-RED Example](https://commons.wikimedia.org/wiki/File:Node-RED_Example.png) | **CC BY-SA 4.0** | niezmodyfikowany zrzut przepływu; użyty w `05#przeplyw` |
| `iot-dashboard-aquaculture.jpg` | Stephane Malhomme — [Aquaculture IoT water monitoring](https://commons.wikimedia.org/wiki/File:Aquaculture_iot_water_monitoring_solution_pentair_eagle.io.jpg) | **CC BY-SA 4.0** | pomniejszony zrzut przykładowego pulpitu; na slajdzie jawnie oznaczony jako interfejs inny niż ThingsBoard; użyty w `06#pulpit-przyklad` |
| `axis-ip-cameras.png` | Bungle — [Axis IP Dome Network Cameras](https://commons.wikimedia.org/wiki/File:Axis_ip_dome_cameras.png) | **CC BY-SA 4.0** | pomniejszona fotografia urządzeń producenta; użyta w `07#mirai` |
| `background-orange.jpg`, `background-green.jpg`, `background-blue.jpg` | Marek Urbaniak — oryginalne tła prezentacji w repozytorium [`moondec/iot_lectures`](https://github.com/moondec/iot_lectures) | **CC BY 4.0** | skopiowane bez modyfikacji; przypisane kolorystycznie do modułów 01–02, 03–05 i 06–07 |

Licencja **CC BY-SA** jest wzajemna (*share-alike*) i dotyczy wskazanych w tabeli ilustracji Arduino oraz materiałów z Wikimedia Commons. Tekst slajdów pozostaje na CC BY 4.0; przy dalszym rozpowszechnianiu ilustracji obowiązuje ich własna wersja licencji wraz z atrybucją.

## Ilustracje świadomie **niewłączone** do repozytorium

**Materiały M5Stack** (zdjęcia i mapy wyprowadzeń Stamp-C3 oraz Stamp-C3U) są objęte
prawem autorskim producenta — *© M5Stack Technology Co., Ltd., all rights reserved*.
Nie mamy potwierdzenia licencji zezwalającej na ich redystrybucję, dlatego **nie ma ich
w tym repozytorium**. Slajd `02#stamp-c3u` odsyła do dokumentacji producenta
([Stamp-C3U](https://docs.m5stack.com/en/core/stamp_c3u),
[Stamp-C3](https://docs.m5stack.com/en/core/stamp_c3)), a tabela wyprowadzeń została
zestawiona z **faktów** podanych w tej dokumentacji — fakty nie podlegają prawu autorskiemu.

Pełna lista wykluczonych ilustracji wraz z powodami znajduje się w
`provenance/slide-map.json`, klucz `ilustracje_wykluczone` (15 pozycji). Obejmuje ona
m.in. zdjęcia stockowe i zrzuty ekranu o nieustalonym pochodzeniu z prezentacji
źródłowych oraz hotlinki do logotypów uczelni.

**Jeżeli prowadzący dysponuje prawami do któregoś z tych materiałów**, można je dodać
do `assets/img/` i uzupełnić ten plik — decyzja należy do autora kursu.

## Oprogramowanie w repozytorium (`assets/vendor/`)

| Składnik | Wersja | Licencja | Zastosowanie |
|:---|:---|:---|:---|
| [Bootstrap Icons](https://icons.getbootstrap.com/) | 1.13.1 | **MIT** (`assets/vendor/bootstrap-icons/LICENSE`) | ikony w nagłówkach slajdów; czcionka i arkusz stylów lokalnie, bez CDN |

Plik `assets/vendor/mermaid-desc-shim.js` jest kodem tego projektu (CC BY 4.0);
obchodzi błąd w skrypcie Quarto — opis w nagłówku pliku.

## Oprogramowanie używane do budowania (niedołączone)

| Narzędzie | Wersja | Licencja |
|:---|:---|:---|
| [Quarto CLI](https://quarto.org/) | 1.10.18 | MIT |
| [reveal.js](https://revealjs.com/) (dostarczany przez Quarto) | wg Quarto 1.10.18 | MIT |
| [Mermaid](https://mermaid.js.org/) (dostarczany przez Quarto) | wg Quarto 1.10.18 | MIT |
| [Source Sans Pro](https://github.com/adobe-fonts/source-sans) (dostarczany przez Quarto) | wg Quarto 1.10.18 | SIL Open Font License 1.1 |
| [Pandoc](https://pandoc.org/) (składnik Quarto) | 3.10.0 | GPL-2.0-or-later |
| [matplotlib](https://matplotlib.org/) — tylko do wygenerowania wykresów | dowolna 3.x | licencja matplotlib (styl PSF) |
| [Playwright](https://playwright.dev/) — tylko do testów | dowolna | Apache-2.0 |

Składniki dostarczane przez Quarto trafiają do `docs/site_libs/` podczas budowania.
Ich licencje znajdują się w plikach dystrybucji Quarto.

## Materiały źródłowe kursu

Prezentacje wyjściowe pochodzą z repozytorium
[`moondec/iot_lectures`](https://github.com/moondec/iot_lectures),
commit `c62ccf6174fea4db9d0c0bfefef174fca4b0f709`, gałąź `main`, odczyt 30.09.2026,
licencja **CC BY 4.0**, autor: Marek Urbaniak. Mapa wykorzystania każdego slajdu:
`provenance/slide-map.json`.

## Cytaty i dane liczbowe

Liczby na slajdach pochodzą z dokumentacji producentów i treści norm wskazanych na
slajdach `zrodla` każdego wykładu. Obliczenia własne są wykonywane przez
`scripts/verify-calc.py`, a wynik zapisany w `provenance/obliczenia.json` — żadna
liczba pokazana jako wynik rachunku nie została przepisana bez przeliczenia.

Krótkie cytaty z literatury (Harari, Huxley) w wykładzie 7 mieszczą się w prawie cytatu
i są opatrzone wskazaniem autora oraz dzieła.
