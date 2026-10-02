# Pochodzenie slajdów

Plik generowany skryptem `scripts/build-report.py` z `provenance/slide-map.json`.
Nie edytuj ręcznie — zmiany wprowadzaj w tabeli `MAPA` w `scripts/build-provenance.py`.

Repozytorium źródłowe: `https://github.com/moondec/iot_lectures.git`, commit `c62ccf6174fea4db9d0c0bfefef174fca4b0f709`, gałąź `main`, odczyt **2026-09-30**, licencja CC BY 4.0.

## Oznaczenia

* **`retained`** — slajd przeniesiony z zachowaniem tezy i większości treści
* **`adapted`** — slajd przeniesiony, lecz przeredagowany: skrót, korekta faktograficzna lub scalenie
* **`new`** — slajd napisany od nowa na podstawie materiałów kursu i źródeł pierwotnych

## Bilans

| Wielkość | Liczba |
|:---|---:|
| Slajdów merytorycznych w pięciu taliach źródłowych | 61 |
| — z nich wykorzystanych (`retained` / `adapted`) | 46 |
| — z nich świadomie nieprzeniesionych | 15 |
| Slajdów merytorycznych w nowym kursie | 150 |
| — `retained` | 8 |
| — `adapted` | 28 |
| — `new` | 114 |

Slajdy `adapted` bywają scaleniem dwóch lub więcej slajdów źródłowych, dlatego liczba wykorzystanych slajdów źródłowych przewyższa liczbę slajdów `retained` i `adapted` razem wziętych.

## 00-internet-przyszlosci

*Internet przyszłości: obietnice, ryzyka, decyzje*

| Slajd | Pochodzenie | Źródło | Uzasadnienie |
|:---|:---|:---|:---|
| `#title-slide` Slajd tytułowy | **new** | — | Nowy nagłówek wykładu zerowego. |
| `#cele` Po co ten wykład | **new** | — | Cele i plan wykładu zerowego. |
| `#przyszłość-jest-już-architekturą` Sekcja: Przyszłość jest już architekturą | **new** | — | Przekładka sekcyjna. |
| `#skala` Przyszłość już jest infrastrukturą | **new** | — | Szacunek IoT Analytics 2025 z jawnym rozróżnieniem estymacji i prognozy. |
| `#lancuch` Nie rzecz, lecz pętla | **new** | — | Nowa rama wiążąca pomiar, model, decyzję i działanie. |
| `#obietnica` Obietnica technologii | **new** | — | Synteza korzyści IoT podporządkowana decyzji użytkownika. |
| `#rolnictwo` Agriculture 4.0 | **new** | — | Proces decyzyjny od obserwacji do oceny efektu. |
| `#destine` Destination Earth | **new** | — | Aktualny przykład cyfrowego bliźniaka uruchomionego w 2024 r. |
| `#matter` Matter 1.4 | **new** | — | Aktualny przykład interoperacyjności i zarządzania energią. |
| `#ntn` Sieci nie-naziemne | **new** | — | Aktualny przykład łączności IoT poza zasięgiem sieci naziemnej. |
| `#dane-zmieniają-władzę` Sekcja: Dane zmieniają władzę | **new** | — | Przekładka sekcyjna. |
| `#cambridge` Cambridge Analytica | **new** | — | Zweryfikowane ustalenia FTC oddzielone od tezy o wpływie na wynik wyborów. |
| `#social-credit` Chiński social credit | **new** | — | Korekta mitu jednego ogólnokrajowego wyniku obywatela. |
| `#petla-wladzy` Pętla danych i władzy | **new** | — | Model obserwacja–inferencja–klasyfikacja–interwencja. |
| `#data-act` Data Act | **new** | — | Aktualne obowiązki dotyczące danych z połączonych produktów. |
| `#ai-wchodzi-do-świata-fizycznego` Sekcja: AI w świecie fizycznym | **new** | — | Przekładka sekcyjna. |
| `#ai-fizyczny` AI i IoT | **new** | — | Konsekwencje połączenia predykcji z działaniem fizycznym. |
| `#praca` AI i rynek pracy | **new** | — | Wyniki ILO 2025 z rozróżnieniem ekspozycji zadań i likwidacji zawodów. |
| `#bci` BCI | **new** | — | Aktualne wyniki neuroprotez mowy i granice interpretacji. |
| `#blue` Blue Brain a Blue Gene | **new** | — | Rozdzielenie projektu naukowego EPFL od rodziny superkomputerów IBM. |
| `#granice-nie-znikają` Sekcja: Granice nie znikają | **new** | — | Przekładka sekcyjna. |
| `#energia` Energia | **new** | — | Bilans korzyści i kosztów w pełnym cyklu życia systemu, uzupełniony o dane IEA 2025. |
| `#botnet` IoT jako element botnetu | **new** | — | Aktualny przypadek Aisuru i ataku 31,4 Tb/s z raportu Cloudflare 2026. |
| `#odpornosc` Urządzenie jako zobowiązanie | **new** | — | Bezpieczeństwo i utrzymanie w całym okresie wsparcia. |
| `#koniec-wsparcia` Sprzęt działa, usługa znika | **new** | — | Przypadek wyłączenia usług chmurowych Wemo w 2026 r. i znaczenie trybu lokalnego. |
| `#prawo` Prawo zmienia backlog | **new** | — | Daty Data Act, RED, AI Act po zmianie 2026/1744 i Cyber Resilience Act. |
| `#od-wizji-do-projektu` Sekcja: Od wizji do projektu | **new** | — | Przekładka sekcyjna. |
| `#pytania-projektowe` Sześć pytań projektowych | **new** | — | Kryteria przed wyborem czujnika. |
| `#most` Most do modułów 01–07 | **new** | — | Powiązanie problemów wykładu 00 z dalszą strukturą kursu. |
| `#przypadek` Przypadek nawadniania | **new** | — | Przypadek przewodni łączący decyzję, architekturę i stan bezpieczny. |
| `#pytania` Pytania sprawdzające | **new** | — | Pytania sprawdzające wykładu zerowego. |
| `#podsumowanie` Podsumowanie | **new** | — | Synteza wykładu i przejście do modułu 01. |
| `#zrodla` Źródła: przypadki i badania | **new** | — | Źródła pierwotne i publikacje naukowe. |
| `#zrodla-2` Źródła: standardy, programy i prawo | **new** | — | Źródła oficjalne i dokumenty instytucjonalne. |

## 01-architektura-i-wymagania

*Architektura systemu IoT i wymagania*

| Slajd | Pochodzenie | Źródło | Uzasadnienie |
|:---|:---|:---|:---|
| `#title-slide` Slajd tytułowy | **new** | — | Nowy nagłówek modułu; usunięto hotlinki logotypów uczelni obecne we wszystkich taliach źródłowych. |
| `#cele` Po co ten wykład | **new** | `lecture-materials/content/uzupelnienie-01.html` | Talie źródłowe nie miały slajdu celów. Dodano cele i plan drogi, wymagane przez strukturę kursu. |
| `#skąd-się-to-wzięło` Sekcja: Skąd się to wzięło | **new** | — | Przekładka sekcyjna; zastępuje numerowane „Rozdział I/II” ze starej struktury. |
| `#geneza` Od punktu do punktu | **adapted** | `wyklad_1.qmd` — 1. Ewolucja: Od punktu do punktu (w. 63-77) + `lecture-materials/content/sprostowania-01.html` | Zachowano oś czasu. Poprawiono datowanie komputera Thorpa: koncepcja 1955, realizacja 1960–61. |
| `#coke` Mit założycielski: pragnienie | **retained** | `wyklad_1.qmd` — 2. Mit Założycielski: Pragnienie (w. 81-108) | Zachowano narrację o automacie CMU; notatkę prowadzącego przeniesiono do treści slajdu jako opis mechanizmu. |
| `#ashton` Kevin Ashton | **retained** | `wyklad_1.qmd` — 3. Kevin Ashton i Toster (Lata 90.) (w. 112-140) | Zachowano dwa wątki (toster Romkeya, RFID Ashtona) bez zmian merytorycznych. |
| `#skala` Skala zjawiska | **adapted** | `wyklad_1.qmd` — 3. Moment Zwrotny: Skala zjawiska (w. 144-175) + `lecture-materials/content/sprostowania-01.html` | Zachowano tezę i wykres. Poprawiono atrybucję: Cisco IBSG (Evans 2011), nie Annual Internet Report; dodano zastrzeżenie o charakterze szacunku. |
| `#zastosowania` Po co to robimy | **adapted** | `wyklad_intro_1.qmd` — 3. Jasna strona mocy (Profity z IoT) (w. 97-111) + `wyklad_intro_1.qmd` — 4. IoT w Rolnictwie: Monitoring upraw i ekosystemów, `wyklad_intro_1.qmd` — 6. Zrównoważone Zastosowanie Zasobów, `wyklad_intro_1.qmd` — 7. Przemysł 4.0: Monitoring Procesów, `wyklad_intro_1.qmd` — 8. Komunikacja wektorowa | Pięć slajdów aplikacyjnych ze wstępu skondensowano w jeden przegląd, podporządkowany tezie modułu: wymagania wynikają z decyzji, nie z listy czujników. |
| `#model-odniesienia` Sekcja: Model odniesienia | **new** | — | Przekładka sekcyjna. |
| `#warstwy` Trzy warstwy | **adapted** | `wyklad_1.qmd` — 4. Architektura Systemów IoT (w. 181-196) + `lecture-materials/content/sprostowania-01.html` | Zachowano model trójwarstwowy. Usunięto błędne stwierdzenie o standaryzacji przez IEEE; dodano odniesienie do IEEE 2413-2019 i ISO/IEC/IEEE 42010. |
| `#przeplyw` Przepływ w pionie | **adapted** | `wyklad_1.qmd` — 5. Schemat przepływu (w. 200-254) | Zachowano ideę diagramu. Usunięto trzystopniowe fragmenty i transform scale(3.5), który wypychał diagram poza slajd; dodano kierunek poleceń i reakcję lokalną. |
| `#mapa-kursu` Warstwy a moduły kursu | **new** | `lecture-materials/content/uzupelnienie-01.html` | Nowa tabela wiążąca warstwy z siedmioma modułami — spoiwo nowej struktury, nieobecne w taliach źródłowych. |
| `#od-narracji-do-wymagań` Sekcja: Od narracji do wymagań | **new** | — | Przekładka sekcyjna. |
| `#granica` Granica systemu — cztery pytania | **new** | `lecture-materials/content/uzupelnienie-01.html` | Temat nieobecny w prezentacjach źródłowych; przeniesiony z materiałów uzupełniających kursu. |
| `#klasy` Trzy klasy komunikatów | **new** | `lecture-materials/content/uzupelnienie-01.html` + `lecture-materials/content/uzupelnienie-04.html` | Nowa tabela klas komunikatów; zapowiada regułę retained rozwiniętą w module 04. |
| `#kryterium` Kryterium akceptacji jest liczbą | **new** | `lecture-materials/content/uzupelnienie-01.html` | Nowy slajd metodyczny z materiałów uzupełniających. |
| `#zalozenia` Lista założeń | **new** | `lecture-materials/content/uzupelnienie-01.html` | Nowy slajd; lista założeń oddawana razem z architekturą. |
| `#stanowisko` Przypadek: stanowisko pilotażowe | **new** | `lecture-materials/content/uzupelnienie-01.html` | Nowy slajd wprowadzający przypadek laboratoryjny wspólny dla siedmiu modułów. |
| `#pytania` Pytania sprawdzające | **new** | — | Nowe pytania sprawdzające; talie źródłowe ich nie zawierały. |
| `#podsumowanie` Podsumowanie i przejście | **adapted** | `wyklad_1.qmd` — 14. Podsumowanie (w. 449-462) | Zachowano funkcję podsumowania. Usunięto odwołanie do nieaktualnej struktury „wykład 1 z 3” i dodano przejście do modułu 02. |
| `#zrodla` Źródła | **new** | — | Nowy wykaz źródeł; talie źródłowe nie miały slajdu bibliograficznego. |

## 02-urzadzenie-sensory-energia

*Urządzenie, sensory i energia*

| Slajd | Pochodzenie | Źródło | Uzasadnienie |
|:---|:---|:---|:---|
| `#title-slide` Slajd tytułowy | **new** | — | Nowy nagłówek modułu. |
| `#cele` Po co ten wykład | **new** | `lecture-materials/content/uzupelnienie-02.html` | Nowy slajd celów. |
| `#percepcja-zmysły-i-mięśnie` Sekcja: Percepcja | **new** | — | Przekładka sekcyjna. |
| `#czujniki` Czym system czuje | **adapted** | `wyklad_1.qmd` — 6. Warstwa Percepcji: Zmysły maszyny (w. 258-285) | Zachowano klasyfikację czujników i ostrzeżenie o środowisku. Dodano podział ze względu na rodzaj wyjścia (analogowe / cyfrowe) jako przygotowanie do slajdu o ADC. |
| `#lancuch` Łańcuch pomiarowy | **new** | `lecture-materials/content/uzupelnienie-02.html` | Nowy slajd z materiałów uzupełniających; pięć ogniw od przetwornika do walidacji lokalnej. |
| `#adc` Rozdzielczość to nie dokładność | **new** | `lecture-materials/content/uzupelnienie-02.html` + `lecture-materials/content/sprostowania-02.html` | Nowy slajd; sprostowanie do materiałów źródłowych, które nie rozdzielały tych pojęć. Liczby z scripts/verify-calc.py. |
| `#aktuatory` Aktuatory i pętla sterowania | **retained** | `wyklad_1.qmd` — 7. Warstwa Percepcji: Aktuatory (w. 289-304) | Zachowano typologię i ostrzeżenie o ryzyku twardym; pętlę sterowania uzupełniono o pomiar potwierdzający. |
| `#stan-bezpieczny` Stan bezpieczny wyjścia | **new** | `lecture-materials/content/uzupelnienie-02.html` | Nowy slajd; temat nieobecny w prezentacjach źródłowych, kluczowy dla planu testów w module 07. |
| `#płytki-stanowiska` Sekcja: Płytki stanowiska | **new** | — | Przekładka sekcyjna. |
| `#platformy` Klasy platform | **adapted** | `wyklad_1.qmd` — 10. Platformy sprzętowe jako kamień węgielny (w. 354-383) + `lecture-materials/content/sprostowania-02.html` | Zachowano podział MCU / SBC. Sprostowano dwa stwierdzenia: brak radia nie jest cechą marki Arduino, a Raspberry Pi nie jest „przestarzałe”. |
| `#rodzina` „ESP32” to rodzina, nie układ | **new** | `lecture-materials/content/sprostowania-02.html` + `unified-materials/content/cm178__lesson_page51__contents.html` | Nowy slajd; sprostowanie do slajdu porównawczego, który traktował ESP32 jako jeden model. |
| `#nano-esp32` Arduino Nano ESP32 (ABX00083) | **new** | `unified-materials/content/cm178__lesson_page51__contents.html` | Nowy slajd; potwierdzona płytka stanowiska, dane z instrukcji producenta. Ilustracje Arduino na CC BY-SA 4.0. |
| `#nano-listwa` Nano ESP32 — co jest na listwie | **new** | `unified-materials/content/cm178__lesson_page51__contents.html` | Nowa tabela wyprowadzeń z oficjalnego pinoutu ABX00083. |
| `#stamp-c3u` M5Stack Stamp-C3U (C122-B) | **new** | `unified-materials/content/cm178__lesson_page51__contents.html` | Nowy slajd; druga potwierdzona płytka. Ilustracji M5Stack nie redystrybuujemy (all rights reserved) — podano odnośnik do dokumentacji producenta. |
| `#c3-vs-c3u` Stamp-C3 a Stamp-C3U | **new** | `unified-materials/content/cm178__lesson_page51__contents.html` | Nowa tabela różnic oparta na faktach z dokumentacji; przeciwdziała myleniu wariantów. |
| `#strapping` Piny strapping | **new** | `unified-materials/content/cm178__lesson_page51__contents.html` | Nowy slajd; dane za dokumentacją Espressif, wraz z przykładem sprzecznego zapisu u producenta. |
| `#prad-pinu` Prąd wyprowadzenia: limit, nie prąd pracy | **new** | `lecture-materials/content/uzupelnienie-02.html` + `unified-materials/content/cm178__lesson_page51__contents.html` | Nowy slajd; sprostowanie błędu „40 mA to bezpieczny prąd zalecany” obecnego w starszych materiałach. |
| `#energia` Sekcja: Energia | **new** | — | Przekładka sekcyjna. |
| `#deep-sleep` Deep sleep | **adapted** | `wyklad_1.qmd` — 11. "Deep Sleep" - czyli kompromis Mocy (w. 387-399) + `lecture-materials/content/sprostowania-02.html` | Zachowano wyjaśnienie paradygmatu. Dodano sprostowanie: wartości 7 µA i 240 µA dotyczą samego SoC, nie całej płytki. |
| `#budzet` Budżet energii to rachunek | **new** | `lecture-materials/content/uzupelnienie-02.html` | Nowy slajd; wzór i wykres własny wygenerowany przez scripts/make-figures.py. |
| `#decyzja-okres` Okres raportowania jest decyzją | **new** | `lecture-materials/content/uzupelnienie-02.html` | Nowa tabela; wszystkie wartości z scripts/verify-calc.py. |
| `#pytania` Pytania sprawdzające | **new** | — | Nowe pytania sprawdzające. |
| `#podsumowanie` Podsumowanie i przejście | **new** | — | Nowe podsumowanie modułu i zapowiedź modułu 03. |
| `#zrodla` Źródła | **new** | — | Nowy wykaz źródeł pierwotnych (Arduino, u-blox, M5Stack, Espressif). |

## 03-lacznosc-i-ota

*Łączność sieciowa i aktualizacje OTA*

| Slajd | Pochodzenie | Źródło | Uzasadnienie |
|:---|:---|:---|:---|
| `#title-slide` Slajd tytułowy | **new** | — | Nowy nagłówek modułu. |
| `#cele` Po co ten wykład | **new** | `lecture-materials/content/uzupelnienie-03.html` | Nowy slajd celów. |
| `#fizyczne-granice` Sekcja: Fizyczne granice | **new** | — | Przekładka sekcyjna. |
| `#trojkat` Trójkąt niemożliwy | **retained** | `wyklad_2.qmd` — 1. Problem Komunikacji M2M (w. 63-95) | Zachowano tezę i wykres autorski scatter_triangle.png. |
| `#wifi` Wi-Fi | **adapted** | `wyklad_2.qmd` — 2. Wi-Fi (IEEE 802.11) (w. 101-127) + `lecture-materials/content/uzupelnienie-03.html` | Zachowano bilans zalet i wad. Dodano powiązanie z doborem dla stanowiska i przypomnienie o braku pasma 5 GHz na obu płytkach. |
| `#ble-mesh` Bluetooth LE i sieci kratowe | **adapted** | `wyklad_2.qmd` — 3. Bluetooth i rewolucja BLE (Low Energy) (w. 131-157) + `wyklad_2.qmd` — 4. Zigbee i Z-Wave: Inżynieria Roju (Mesh), `lecture-materials/content/sprostowania-03.html` | Scalono dwa slajdy źródłowe. Dodano warunek „samoleczenia” sieci mesh i aktualną nazwę organizacji (Connectivity Standards Alliance, Matter). |
| `#lpwan` LPWAN | **retained** | `wyklad_2.qmd` — 5. LPWAN: Telemetria na kilometry (w. 204-227) + `wyklad_2.qmd` — 6. Porównanie technologii radiowych | Zachowano opis i wykres bąbelkowy; scalono ze slajdem porównawczym, by uniknąć powtórzenia. |
| `#lora-nbiot` LoRaWAN a NB-IoT | **adapted** | `wyklad_2.qmd` — 7. LoRaWAN vs NB-IoT (w. 255-296) + `lecture-materials/content/sprostowania-03.html` | Zachowano zestawienie. Sprostowano „darmowe pasmo 868 MHz” (regulowane, duty cycle) i status NB-IoT (3GPP Rel. 13, własna warstwa radiowa). |
| `#sigfox` Sigfox | **adapted** | `wyklad_2.qmd` — 8. Sigfox: ultralekkie wiadomości jako usługa (w. 300-313) + `lecture-materials/content/sprostowania-03.html` | Zachowano parametry. Dodano zmianę właściciela (UnaBiz, Sigfox 0G) i ryzyko operatora jako parametr projektowy. |
| `#cztery-liczby` Metodyka doboru — cztery liczby | **new** | `lecture-materials/content/uzupelnienie-03.html` | Nowy slajd metodyczny; zamienia porównanie technologii w powtarzalną procedurę. |
| `#łącze-które-się-podnosi` Sekcja: Łącze | **new** | — | Przekładka sekcyjna. |
| `#reconnect` Ponowne łączenie z wycofaniem | **new** | `lecture-materials/content/uzupelnienie-03.html` | Nowy slajd; temat nieobecny w prezentacjach źródłowych. |
| `#bufor` Buforowanie w czasie awarii | **new** | `lecture-materials/content/uzupelnienie-03.html` | Nowy slajd; trzy warunki poprawnego buforowania plus pułapka znacznika czasu. |
| `#wydanie-firmware` Sekcja: Wydanie firmware | **new** | — | Przekładka sekcyjna. |
| `#ota-co-to` OTA to nie nadpisanie firmware | **new** | `lecture-materials/content/uzupelnienie-03.html` + `lecture-materials/content/sprostowania-03.html` | Nowy slajd; wypełnia lukę odnotowaną w mapowaniu modułów (OTA nie występował w żadnej z pięciu talii źródłowych). |
| `#ota-api` Mechanizmy ESP-IDF | **new** | `lecture-materials/content/uzupelnienie-03.html` | Nowa tabela mechanizmów OTA z dokumentacji Espressif. |
| `#self-test` Self-test i wycofanie | **new** | `lecture-materials/content/uzupelnienie-03.html` | Nowy slajd; kolejność dowód → zatwierdzenie jako sedno mechanizmu. |
| `#ota-granice` Czego OTA nie gwarantuje | **new** | — | Nowy slajd napisany, by nie formułować fałszywych obietnic o niezawodności aktualizacji. |
| `#ota-platforma` Wydanie zarządzane przez platformę | **new** | `lecture-materials/content/uzupelnienie-03.html` | Nowy slajd; stany pakietu i tempo wdrożenia, liczby z scripts/verify-calc.py. |
| `#procedura` Procedura wydania w pilocie | **new** | `lecture-materials/content/uzupelnienie-03.html` | Nowy slajd; sześciopunktowa procedura z kryterium zaliczenia. |
| `#pytania` Pytania sprawdzające | **new** | — | Nowe pytania sprawdzające. |
| `#podsumowanie` Podsumowanie i przejście | **new** | — | Nowe podsumowanie i zapowiedź modułu 04. |
| `#zrodla` Źródła | **new** | — | Nowy wykaz źródeł pierwotnych. |

## 04-mqtt-i-kontrakt-danych

*MQTT i kontrakt danych*

| Slajd | Pochodzenie | Źródło | Uzasadnienie |
|:---|:---|:---|:---|
| `#title-slide` Slajd tytułowy | **new** | — | Nowy nagłówek modułu. |
| `#cele` Po co ten wykład | **new** | `lecture-materials/content/uzupelnienie-04.html` | Nowy slajd celów. |
| `#protokół` Sekcja: Protokół | **new** | — | Przekładka sekcyjna. |
| `#http` Dlaczego HTTP nie pasuje | **adapted** | `wyklad_2.qmd` — 9. Dlaczego protokół HTTP nie pasuje do IoT? (w. 319-358) | Zachowano trzy argumenty. Usunięto diagram porównawczy o zmyślonych rozmiarach pakietów na rzecz rachunku na slajdzie „Nagłówek MQTT”; dodano zastrzeżenie, że problemem jest rola, nie protokół. |
| `#mqtt` MQTT: publikacja i subskrypcja | **adapted** | `wyklad_2.qmd` — 10. MQTT: Lekki, binarny standard IoT (w. 362-401) + `lecture-materials/content/sprostowania-04.html` | Zachowano opis pub/sub i diagram. Sprostowano autorstwo (Stanford-Clark i Nipper) oraz status normalizacyjny (OASIS, ISO/IEC 20922:2016). |
| `#naglowek` Ile naprawdę waży nagłówek | **new** | `lecture-materials/content/sprostowania-04.html` | Nowy slajd; sprostowanie do „nagłówek MQTT to 2 bajty”. Rozmiary pakietów policzone w scripts/verify-calc.py. |
| `#tematy-i-niezawodność` Sekcja: Tematy i niezawodność | **new** | — | Przekładka sekcyjna. |
| `#tematy` Drzewo tematów pilota | **new** | `lecture-materials/content/uzupelnienie-04.html` | Nowa tabela; konkretne drzewo tematów z kierunkiem i regułą retained. |
| `#retained` Dlaczego polecenie nigdy nie jest retained | **new** | `lecture-materials/content/uzupelnienie-04.html` | Nowy slajd z diagramem sekwencji; konsekwencja fizyczna błędu projektowego. |
| `#qos` QoS i jego koszt | **adapted** | `wyklad_2.qmd` — 11. MQTT: Tematy, QoS i „Ostatnia Wola" (w. 405-453) + `lecture-materials/content/sprostowania-04.html`, `lecture-materials/content/sprostowania-06.html` | Zachowano poziomy QoS i LWT. Sprostowano „QoS 2 gwarantuje dostarczenie”; dodano kolumnę kosztu oraz ograniczenie platformy do QoS 0/1. |
| `#qos-sekwencja` Sekwencja trzech poziomów | **retained** | `wyklad_2.qmd` — 11. MQTT: Tematy, QoS i „Ostatnia Wola" (w. 405-453) | Zachowano diagram sekwencji ze źródła; usunięto transform scale(1.7) powodujący wyjście poza slajd. |
| `#kontrakt-danych` Sekcja: Kontrakt danych | **new** | — | Przekładka sekcyjna. |
| `#kontrakt` Samoopisujący się ładunek | **new** | `lecture-materials/content/uzupelnienie-04.html` | Nowy slajd; schemat komunikatu JSON z materiałów uzupełniających. |
| `#wersjonowanie` Wersjonowanie kontraktu | **new** | `lecture-materials/content/uzupelnienie-04.html` | Nowy slajd; zmiana zgodna i niezgodna wstecz. |
| `#idempotencja` Idempotencja polecenia | **new** | `lecture-materials/content/uzupelnienie-04.html` | Nowy slajd z diagramem sekwencji. |
| `#dostep` Zamknięcie dostępu do brokera | **new** | `lecture-materials/content/uzupelnienie-04.html` + `lecture-materials/content/sprostowania-04.html` | Nowy slajd; ACL, TLS, unikalny ClientID. Sprostowano separację środowisk przez prefiks. |
| `#coap-amqp` CoAP i AMQP | **adapted** | `wyklad_2.qmd` — 12. CoAP i AMQP (w. 457-480) + `lecture-materials/content/sprostowania-04.html` | Zachowano zestawienie. Sprostowano „bez gwarancji dostarczenia” dla CoAP (tryb confirmable). |
| `#test-odbioru` Test odbioru kontraktu | **new** | `lecture-materials/content/uzupelnienie-04.html` | Nowy slajd; pięć dowodów działania kontraktu. |
| `#zestawienie` Dobór technologii | **retained** | `wyklad_2.qmd` — 13. Podsumowanie: Dobór technologii (w. 484-499) | Zachowano tabelę podsumowującą; zaktualizowano nazwę Sigfox 0G. |
| `#pytania` Pytania sprawdzające | **new** | — | Nowe pytania sprawdzające. |
| `#podsumowanie` Podsumowanie i przejście | **new** | — | Nowe podsumowanie i zapowiedź modułu 05. |
| `#zrodla` Źródła | **new** | — | Nowy wykaz źródeł pierwotnych (OASIS, RFC, Mosquitto). |

## 05-brzeg-node-red-sheets

*Brzeg sieci, Node-RED i zapis do Google Sheets*

| Slajd | Pochodzenie | Źródło | Uzasadnienie |
|:---|:---|:---|:---|
| `#title-slide` Slajd tytułowy | **new** | — | Nowy nagłówek modułu. |
| `#cele` Po co ten wykład | **new** | `lecture-materials/content/uzupelnienie-05.html` | Nowy slajd celów. |
| `#brzeg-sieci` Sekcja: Brzeg sieci | **new** | — | Przekładka sekcyjna. |
| `#redukcja` Od gigabajtów do wiedzy | **retained** | `wyklad_3.qmd` — 1. Od gigabajtów do wiedzy (w. 63-110) | Zachowano tezę i diagram redukcji danych; usunięto transform scale(2) i dodano gałąź zapisu raportowego. |
| `#brama` Brama brzegowa — cztery zadania | **adapted** | `wyklad_1.qmd` — 8. Brama brzegu sieci (Edge Gateway) (w. 308-332) + `lecture-materials/content/sprostowania-05.html` | Zachowano definicję bramy i pojęcie latency. Rozszerzono z samej agregacji na cztery zadania, zgodnie ze sprostowaniem. |
| `#jakosc` Piąte zadanie: jakość danych | **new** | `lecture-materials/content/sprostowania-05.html` | Nowy slajd; sprostowanie do opisu Node-RED jako „kleju” bez odpowiedzialności. |
| `#przepływ` Sekcja: Przepływ | **new** | — | Przekładka sekcyjna. |
| `#przeplyw` Node-RED węzeł po węźle | **new** | `lecture-materials/content/uzupelnienie-05.html` | Nowy slajd; konkretny przepływ z jawną ścieżką błędu. |
| `#walidacja` Minimalny zestaw reguł walidacji | **new** | `lecture-materials/content/uzupelnienie-05.html` | Nowy slajd; pięć reguł i wymóg logowania powodu odrzucenia. |
| `#zapis-do-arkusza` Sekcja: Zapis do arkusza | **new** | — | Przekładka sekcyjna. |
| `#warianty` Dwa warianty zapisu | **new** | `lecture-materials/content/uzupelnienie-05.html` + `lecture-materials/content/sprostowania-05.html` | Nowa tabela; Apps Script a Sheets API v4, wraz ze sprostowaniem o adresie wdrożenia jako sekrecie. |
| `#limity` Limity Google Sheets API | **new** | `lecture-materials/content/uzupelnienie-05.html` | Nowy slajd; limity z dokumentacji Google, wykres własny z scripts/make-figures.py. |
| `#ponowienia` Ponowienia i granice arkusza | **new** | `lecture-materials/content/uzupelnienie-05.html` | Nowy slajd; rozróżnienie błędów ponawialnych i nieponawialnych. |
| `#autoryzacja` Autoryzacja i błędy eksportu | **new** | `lecture-materials/content/uzupelnienie-05.html` | Nowy slajd; procedura konta usługi i tabela kodów odpowiedzi. |
| `#test-odbioru` Test odbioru przepływu | **new** | `lecture-materials/content/uzupelnienie-05.html` | Nowy slajd; pięć dowodów działania przepływu. |
| `#pytania` Pytania sprawdzające | **new** | — | Nowe pytania sprawdzające. |
| `#podsumowanie` Podsumowanie i przejście | **new** | — | Nowe podsumowanie i zapowiedź modułu 06. |
| `#zrodla` Źródła | **new** | — | Nowy wykaz źródeł pierwotnych (Google, Node-RED). |

## 06-thingsboard-ce

*ThingsBoard CE — telemetria, pulpity i sterowanie*

| Slajd | Pochodzenie | Źródło | Uzasadnienie |
|:---|:---|:---|:---|
| `#title-slide` Slajd tytułowy | **new** | — | Nowy nagłówek modułu. |
| `#cele` Po co ten wykład | **new** | `lecture-materials/content/uzupelnienie-06.html` | Nowy slajd celów. |
| `#model-danych` Sekcja: Model danych | **new** | — | Przekładka sekcyjna. |
| `#model-najpierw` Wykres jest ostatni | **new** | `lecture-materials/content/uzupelnienie-06.html` + `lecture-materials/content/sprostowania-06.html` | Nowy slajd; sprostowanie do traktowania platformy jako „dashboardu w chmurze”. |
| `#rodzaje` Trzy rodzaje danych | **new** | `lecture-materials/content/uzupelnienie-06.html` | Nowa tabela; telemetria a cztery kategorie atrybutów. |
| `#wspoldzielone` Atrybuty współdzielone | **new** | `lecture-materials/content/uzupelnienie-06.html` | Nowy slajd; konfiguracja bez ponownego wgrywania firmware. |
| `#styk-z-urządzeniem` Sekcja: Styk z urządzeniem | **new** | — | Przekładka sekcyjna. |
| `#tematy` Kontrakt tematów MQTT platformy | **new** | `lecture-materials/content/uzupelnienie-06.html` + `lecture-materials/content/sprostowania-06.html` | Nowa tabela tematów standardowych i skróconych; sprostowanie o braku QoS 2. |
| `#poswiadczenia` Poświadczenia urządzenia | **new** | `lecture-materials/content/uzupelnienie-06.html` | Nowy slajd; trzy typy poświadczeń i ostrzeżenie o tokenie jako sekrecie. |
| `#rpc` Sterowanie zwrotne: RPC | **new** | `lecture-materials/content/uzupelnienie-06.html` | Nowy slajd z diagramem sekwencji; stan potwierdzony wobec żądanego. |
| `#pulpit` Od telemetrii do pulpitu | **new** | `lecture-materials/content/uzupelnienie-06.html` | Nowy slajd; co pulpit powinien pokazywać i czego nie zastąpi. |
| `#kontekst-i-ryzyko` Sekcja: Kontekst i ryzyko | **new** | — | Przekładka sekcyjna. |
| `#bliźniak` Cyfrowy bliźniak | **adapted** | `wyklad_3.qmd` — 6. Cyfrowe Bliźniaki (Digital Twins) (w. 231-251) + `wyklad_1.qmd` — 12. Digital Twins (Cyfrowy Bliźniak), `lecture-materials/content/sprostowania-06.html` | Scalono dwa slajdy źródłowe z dwóch różnych talii w jedno omówienie, zgodnie ze sprostowaniem o powtórzeniu. Dodano zastrzeżenie, że to nie wizualizacja 3D. |
| `#smart-city` Zastosowania w skali miasta | **adapted** | `wyklad_3.qmd` — 4. Barcelona: Pionierzy „miasta jako komputera" (w. 173-198) + `wyklad_3.qmd` — 5. Smart City i Przemysł 4.0 (IIoT), `lecture-materials/content/sprostowania-01.html` | Scalono dwa slajdy o Smart City. Usunięto konkretne wartości procentowe jako danych pomiarowych; dodano zastrzeżenie o poglądowym charakterze liczb. |
| `#ryzyko` Ryzyko dostawcy i licencji | **adapted** | `wyklad_3.qmd` — 2. Platformy korporacyjne (PaaS) (w. 116-141) + `lecture-materials/content/sprostowania-06.html` | Zachowano przypadek Google IoT Core. Uściślono daty (ogłoszenie 2022-08, wyłączenie 2023-08-16) i dodano ryzyko zmiany licencji oprogramowania lokalnego. |
| `#ce-pe` CE a PE | **new** | `lecture-materials/content/uzupelnienie-06.html` + `lecture-materials/content/sprostowania-06.html` | Nowy slajd; sprostowanie o „fizycznej izolacji środowisk” i ostrzeżenie przed materiałami dotyczącymi PE. |
| `#test-odbioru` Test odbioru modułu | **new** | `lecture-materials/content/uzupelnienie-06.html` | Nowy slajd; pięć dowodów. |
| `#pytania` Pytania sprawdzające | **new** | — | Nowe pytania sprawdzające. |
| `#podsumowanie` Podsumowanie i przejście | **new** | — | Nowe podsumowanie i zapowiedź modułu 07. |
| `#zrodla` Źródła | **new** | — | Nowy wykaz źródeł pierwotnych (ThingsBoard, Google Cloud). |

## 07-odpornosc-bezpieczenstwo-eksploatacja

*Odporność, bezpieczeństwo i eksploatacja*

| Slajd | Pochodzenie | Źródło | Uzasadnienie |
|:---|:---|:---|:---|
| `#title-slide` Slajd tytułowy | **new** | — | Nowy nagłówek modułu. |
| `#cele` Po co ten wykład | **new** | `lecture-materials/content/uzupelnienie-07.html` | Nowy slajd celów. |
| `#sekcja-rama` Sekcja: Rama | **new** | — | Przekładka sekcyjna. |
| `#rama` Kto tworzy skutki | **adapted** | `wyklad_intro_1.qmd` — 1. Technologia was wyzwoli? (w. 62-74) + `wyklad_intro_1.qmd` — 2. Kto tworzy "przyszłość"?, `lecture-materials/content/sprostowania-07.html` | Scalono dwa slajdy otwierające wstęp w jedną ramę odpowiedzialności. Zgodnie ze sprostowaniem umieszczono ją przy eksploatacji jako decyzję inżynierską, nie dygresję. |
| `#odporność` Sekcja: Odporność | **new** | — | Przekładka sekcyjna. |
| `#nieaktywnosc` Wykrycie nieaktywności | **new** | `lecture-materials/content/uzupelnienie-07.html` | Nowy slajd; atrybuty stanu urządzenia i parametry progu. |
| `#pulapka` Pułapka fałszywego alarmu | **new** | `lecture-materials/content/uzupelnienie-07.html` | Nowy slajd; zależność progu od okresu raportowania aktywności, liczby z scripts/verify-calc.py. |
| `#alarm` Alarm i dowód jego zamknięcia | **new** | `lecture-materials/content/uzupelnienie-07.html` | Nowy slajd; wymóg pojedynczego powiadomienia i samoczynnego zamknięcia. |
| `#bezpieczeństwo` Sekcja: Bezpieczeństwo | **new** | — | Przekładka sekcyjna. |
| `#model-zagrozen` Model zagrożeń | **new** | `lecture-materials/content/uzupelnienie-07.html` | Nowa tabela czterech powierzchni ataku; porządkuje mechanizmy wprowadzone w modułach 03–06. |
| `#mirai` Mirai — dwa incydenty | **adapted** | `wyklad_3.qmd` — 7. Gdy „rzeczy" stają się bronią DDoS (w. 257-285) + `lecture-materials/content/sprostowania-07.html` | Zachowano przypadek. Rozdzielono dwa łączone wcześniej incydenty (Dyn 2016-10-21, TR-064 Deutsche Telekom 2016-11). Usunięto mapę o nieudokumentowanym pochodzeniu. |
| `#kryptografia` Brak mocy na kryptografię to nieprawda | **new** | `lecture-materials/content/sprostowania-07.html` | Nowy slajd; dwa sprostowania — akceleratory sprzętowe w ESP32-S3/C3 oraz X.509 jako format, nie algorytm. |
| `#defence` Obrona warstwowa | **adapted** | `wyklad_3.qmd` — 8. Dobre praktyki bezpieczeństwa (Defence in Depth) (w. 289-337) + `lecture-materials/content/sprostowania-07.html` | Zachowano cztery warstwy i diagram segmentacji. Sprostowano, że VLAN bez polityki odmowy domyślnej nie izoluje; usunięto transform scale(1.7). |
| `#eksploatacja` Sekcja: Eksploatacja | **new** | — | Przekładka sekcyjna. |
| `#testy-awarii` Plan testów awarii | **new** | `lecture-materials/content/uzupelnienie-07.html` | Nowy slajd; pięć scenariuszy wiążących mechanizmy ze wszystkich modułów. |
| `#higiena` Higiena testu powiadomień | **new** | `lecture-materials/content/uzupelnienie-07.html` | Nowy slajd; domena .invalid i osobny łańcuch reguł. |
| `#prywatnosc` Prywatność: dane pośrednie | **adapted** | `wyklad_3.qmd` — 9. Prywatność w epoce mikrofonów zawsze włączonych (w. 341-353) + `lecture-materials/content/uzupelnienie-07.html` | Zachowano trzy przykłady profilowania. Dodano pojęcie danych osobowych pośrednich i wymóg minimalizacji. |
| `#obowiazki` Obowiązki poza kodem | **new** | `lecture-materials/content/uzupelnienie-07.html` + `lecture-materials/content/sprostowania-07.html` | Nowy slajd; aktualne daty Cyber Resilience Act i dokumentacja wyjścia z systemu. |
| `#koszt-energii` Koszt energii jako rama | **adapted** | `wyklad_intro_2.qmd` — 8. Podstawowa Blokada: Prawdziwy Koszt Energii (w. 241-265) | Zachowano porównanie człowiek / samochód. Przeliczenie zweryfikowane w scripts/verify-calc.py; powiązane z budżetem energii z modułu 02. |
| `#bilans` Bilans korzyści i wyzwań | **adapted** | `wyklad_3.qmd` — 10. Bilans korzyści i wyzwań na nową dekadę (w. 359-383) + `wyklad_3.qmd` — 11. Przyszłość: 6G i nowe paradygmaty, `lecture-materials/content/sprostowania-07.html` | Scalono bilans i slajd o przyszłości. Dodano sprostowanie: opóźnienia sub-milisekundowe 6G to cele badawcze, nie parametry wdrożonego standardu. |
| `#pytania` Pytania sprawdzające | **new** | — | Nowe pytania sprawdzające. |
| `#zamkniecie` Zamknięcie cyklu | **adapted** | `wyklad_3.qmd` — 12. Zakończenie cyklu wykładów (w. 403-423) + `wyklad_intro_2.qmd` — 9. Literatura do Wstępu i Zakończenie | Zachowano puentę o automacie z napojami i pytanie do audytorium. Rozszerzono pytanie o odpowiedzialność; dołączono listę lektur ze wstępu części 2. |
| `#zrodla` Źródła i dalsza lektura | **new** | — | Nowy wykaz źródeł pierwotnych oraz lektura uzupełniająca. |

## Slajdy źródłowe świadomie nieprzeniesione

| Slajd źródłowy | Plik | Powód |
|:---|:---|:---|
| 5. Medycyna – Poznać Siebie (Smart Wearables) | `wyklad_intro_1.qmd` | Przykład aplikacyjny bez związku z zakresem siedmiu modułów; budżet energetyczny urządzenia noszonego omawia moduł 02 na konkretnej płytce. Ilustracja (Oura Ring) bez udokumentowanej licencji. |
| 9. Cykl IoT & AI – To przyszłość, a obecnie? | `wyklad_intro_1.qmd` | Narracja o generacjach 1.0–4.0 nie wnosi kryterium projektowego; jej funkcję („po co mierzymy”) przejął slajd 01#zastosowania. |
| 10. Przypadek Studyjny: 'Tree Talker' | `wyklad_intro_1.qmd` | Wartościowy przykład autorski, ale dubluje rolę stanowiska pilotażowego jako przypadku przewodniego. Zachowany w notes/ jako materiał do rozwinięcia ustnego; ilustracja bez udokumentowanej licencji. |
| 11. Podsumowanie Wstępu | `wyklad_intro_1.qmd` | Podsumowanie nieistniejącej już części „Wstęp 1”; zastąpione podsumowaniami modułów. |
| 2. Sztuczna Inteligencja: Asystent czy Konkurencja? | `wyklad_intro_2.qmd` | Wątek rynku pracy i „bezużytecznej klasy” wykracza poza zakres kursu inżynierskiego i nie prowadzi do decyzji projektowej. |
| 3. Czy jesteśmy programami? | `wyklad_intro_2.qmd` | Dygresja filozoficzna bez konsekwencji technicznej. |
| 4. Ucieczka z "Tu i Teraz" | `wyklad_intro_2.qmd` | Cytat z Huxleya; rama etyczna zachowana w 07#rama w formie zwięzłej. |
| 5. Kierunki rozwoju: Wychodząc z Jaskini | `wyklad_intro_2.qmd` | Wątek antropologiczny bez związku z zakresem modułów. |
| 6. Bezpośredni transfer wrażeń (BCI) | `wyklad_intro_2.qmd` | Eksperyment Nicolelisa — ciekawostka bez konsekwencji dla projektowania systemu IoT. |
| 7. Interfejs Człowiek-Człowiek (UW, 2013) | `wyklad_intro_2.qmd` | Jak wyżej; dodatkowo ilustracja bez udokumentowanej licencji. |
| 9. Od pomysłu do wdrożenia | `wyklad_1.qmd` | Teza o obniżeniu bariery wejścia wchłonięta przez 02#platformy; osobny slajd nie wnosił kryterium wyboru. |
| 13. Zestawienie: Arduino vs ESP vs Raspberry Pi | `wyklad_1.qmd` | Tabela zbudowana na nieaktualnych założeniach (Arduino bez radia, Raspberry Pi „przestarzałe”). Zastąpiona przez 02#platformy i 02#rodzina, opartymi na płytkach stanowiska. |
| 3. Narzędzia otwartoźródłowe | `wyklad_3.qmd` | Lista narzędzi wchłonięta: Node-RED do modułu 05, ThingsBoard do 06 wraz ze sprostowaniem o statusie licencyjnym. Osobny slajd powielałby treść. |
| 1. Ciemna strona mocy: Dobre narzędzia, Złe intencje | `wyklad_intro_2.qmd` | Przykłady (Cambridge Analytica, system kredytu społecznego) dotyczą analityki danych społecznych, nie projektowania systemu IoT. Rolę ramy odpowiedzialności przejął slajd 07#rama, a konkretne konsekwencje projektowe — 07#prywatnosc i 07#obowiazki. |
| 14. Dziękuję za uwagę | `wyklad_2.qmd` | Slajd czysto organizacyjny, zapowiadający nieaktualną strukturę trzech wykładów. Każdy moduł ma własne podsumowanie z przejściem do kolejnego. |

## Ilustracje wykluczone z repozytorium

| Plik / grupa | Powód |
|:---|:---|
| `img/Oura-ring.jpg` | Brak udokumentowanego źródła i licencji. |
| `img/IIoT-smart-manufacturing-smart-factory-3751296197.jpg` | Zdjęcie stockowe bez udokumentowanej licencji. |
| `img/residential-sprinkler-systems-2663960231.jpg` | Zdjęcie stockowe bez udokumentowanej licencji. |
| `img/smart_transportation_781x512-1163925340.jpg` | Zdjęcie stockowe bez udokumentowanej licencji. |
| `img/th-1774962466.png` | Brak udokumentowanego źródła. |
| `img/Pasted image 2022*.png` | Zrzuty ekranu i ilustracje o nieustalonym pochodzeniu (14 plików użytych w taliach źródłowych). |
| `img/mirai_map.png` | Mapa bez wskazania autora i źródła danych; treść przeniesiona do tekstu slajdu 07#mirai. |
| `img/iot_dashboard.png` | Zrzut ekranu bez wskazania wersji i licencji oprogramowania. |
| `img/digital_twin_nature.png` | Brak udokumentowanego źródła. |
| `img/mcu_compare.png` | Brak udokumentowanego źródła; zastąpione tabelami opartymi na dokumentacji producentów. |
| `img/lpwan_station.png` | Brak udokumentowanego źródła. |
| `img/iot_tlo_gr.jpg, iot_tlo_or.jpg, iot_tlo_bl.jpg` | Tła fotograficzne bez udokumentowanej licencji; charakter wizualny odtworzony w assets/theme/iot.scss. |
| `img/kbig.jpg` | Logotyp o nieustalonym statusie praw; slajd tytułowy nie zawiera logotypów. |
| `logo up.poznan.pl, logo wisim.up.poznan.pl` | Hotlinki do serwerów uczelni — usunięte zgodnie z wymogiem eliminacji łamanych odnośników do logotypów. |
| `m5stamp-c3-board.png, m5stamp-c3-pinmap.png, m5stamp-c3u-board.png, m5stamp-c3u-pinmap.png` | Materiały M5Stack Technology Co., Ltd. — all rights reserved. Nie redystrybuujemy ich w repozytorium przeznaczonym do publikacji; w slajdzie 02#stamp-c3u podano odnośnik do dokumentacji producenta, a tabela wyprowadzeń została zestawiona z faktów. |
