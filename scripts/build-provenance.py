#!/usr/bin/env python3
"""Buduje provenance/slide-map.json — mapę pochodzenia każdego slajdu.

Uruchomienie:  python3 scripts/build-provenance.py

Tabela MAPA jest utrzymywana ręcznie (to decyzja redakcyjna, nie wynik automatu),
ale skrypt weryfikuje ją wobec faktycznie wyrenderowanego HTML: każdy slajd
w wyniku musi mieć wpis, a każdy wpis musi wskazywać istniejący slajd.

origin:
  retained — slajd przeniesiony z zachowaniem tezy i większości treści
  adapted  — slajd przeniesiony, ale przeredagowany (skrót, korekta, scalenie)
  new      — slajd napisany od nowa na podstawie materiałów kursu i źródeł pierwotnych
"""
import json, os, re, glob, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SRC_COMMIT = "c62ccf6174fea4db9d0c0bfefef174fca4b0f709"
SRC_REPO = "https://github.com/moondec/iot_lectures.git"
DATA_ODCZYTU = "2026-09-30"

# skrót źródła → (plik qmd, tytuł slajdu, zakres wierszy w źródle)
Z = {
    "i1_01": ("wyklad_intro_1.qmd", "1. Technologia was wyzwoli?", "62-74"),
    "i1_02": ("wyklad_intro_1.qmd", "2. Kto tworzy \"przyszłość\"?", "78-91"),
    "i1_03": ("wyklad_intro_1.qmd", "3. Jasna strona mocy (Profity z IoT)", "97-111"),
    "i1_04": ("wyklad_intro_1.qmd", "4. IoT w Rolnictwie: Monitoring upraw i ekosystemów", "115-138"),
    "i1_05": ("wyklad_intro_1.qmd", "5. Medycyna – Poznać Siebie (Smart Wearables)", "142-165"),
    "i1_06": ("wyklad_intro_1.qmd", "6. Zrównoważone Zastosowanie Zasobów", "169-191"),
    "i1_07": ("wyklad_intro_1.qmd", "7. Przemysł 4.0: Monitoring Procesów", "195-215"),
    "i1_08": ("wyklad_intro_1.qmd", "8. Komunikacja wektorowa", "219-241"),
    "i1_09": ("wyklad_intro_1.qmd", "9. Cykl IoT & AI – To przyszłość, a obecnie?", "245-264"),
    "i1_10": ("wyklad_intro_1.qmd", "10. Przypadek Studyjny: 'Tree Talker'", "268-293"),
    "i1_11": ("wyklad_intro_1.qmd", "11. Podsumowanie Wstępu", "297-309"),
    "i2_01": ("wyklad_intro_2.qmd", "1. Ciemna strona mocy: Dobre narzędzia, Złe intencje", "62-87"),
    "i2_02": ("wyklad_intro_2.qmd", "2. Sztuczna Inteligencja: Asystent czy Konkurencja?", "91-116"),
    "i2_03": ("wyklad_intro_2.qmd", "3. Czy jesteśmy programami?", "120-137"),
    "i2_04": ("wyklad_intro_2.qmd", "4. Ucieczka z \"Tu i Teraz\"", "141-155"),
    "i2_05": ("wyklad_intro_2.qmd", "5. Kierunki rozwoju: Wychodząc z Jaskini", "161-183"),
    "i2_06": ("wyklad_intro_2.qmd", "6. Bezpośredni transfer wrażeń (BCI)", "187-210"),
    "i2_07": ("wyklad_intro_2.qmd", "7. Interfejs Człowiek-Człowiek (UW, 2013)", "214-237"),
    "i2_08": ("wyklad_intro_2.qmd", "8. Podstawowa Blokada: Prawdziwy Koszt Energii", "241-265"),
    "i2_09": ("wyklad_intro_2.qmd", "9. Literatura do Wstępu i Zakończenie", "269-289"),
    "w1_01": ("wyklad_1.qmd", "1. Ewolucja: Od punktu do punktu", "63-77"),
    "w1_02": ("wyklad_1.qmd", "2. Mit Założycielski: Pragnienie", "81-108"),
    "w1_03": ("wyklad_1.qmd", "3. Kevin Ashton i Toster (Lata 90.)", "112-140"),
    "w1_04": ("wyklad_1.qmd", "3. Moment Zwrotny: Skala zjawiska", "144-175"),
    "w1_05": ("wyklad_1.qmd", "4. Architektura Systemów IoT", "181-196"),
    "w1_06": ("wyklad_1.qmd", "5. Schemat przepływu", "200-254"),
    "w1_07": ("wyklad_1.qmd", "6. Warstwa Percepcji: Zmysły maszyny", "258-285"),
    "w1_08": ("wyklad_1.qmd", "7. Warstwa Percepcji: Aktuatory", "289-304"),
    "w1_09": ("wyklad_1.qmd", "8. Brama brzegu sieci (Edge Gateway)", "308-332"),
    "w1_10": ("wyklad_1.qmd", "9. Od pomysłu do wdrożenia", "338-350"),
    "w1_11": ("wyklad_1.qmd", "10. Platformy sprzętowe jako kamień węgielny", "354-383"),
    "w1_12": ("wyklad_1.qmd", "11. \"Deep Sleep\" - czyli kompromis Mocy", "387-399"),
    "w1_13": ("wyklad_1.qmd", "12. Digital Twins (Cyfrowy Bliźniak)", "403-427"),
    "w1_14": ("wyklad_1.qmd", "13. Zestawienie: Arduino vs ESP vs Raspberry Pi", "431-445"),
    "w1_15": ("wyklad_1.qmd", "14. Podsumowanie", "449-462"),
    "w2_01": ("wyklad_2.qmd", "1. Problem Komunikacji M2M", "63-95"),
    "w2_02": ("wyklad_2.qmd", "2. Wi-Fi (IEEE 802.11)", "101-127"),
    "w2_03": ("wyklad_2.qmd", "3. Bluetooth i rewolucja BLE (Low Energy)", "131-157"),
    "w2_04": ("wyklad_2.qmd", "4. Zigbee i Z-Wave: Inżynieria Roju (Mesh)", "161-198"),
    "w2_05": ("wyklad_2.qmd", "5. LPWAN: Telemetria na kilometry", "204-227"),
    "w2_06": ("wyklad_2.qmd", "6. Porównanie technologii radiowych", "231-251"),
    "w2_07": ("wyklad_2.qmd", "7. LoRaWAN vs NB-IoT", "255-296"),
    "w2_08": ("wyklad_2.qmd", "8. Sigfox: ultralekkie wiadomości jako usługa", "300-313"),
    "w2_09": ("wyklad_2.qmd", "9. Dlaczego protokół HTTP nie pasuje do IoT?", "319-358"),
    "w2_10": ("wyklad_2.qmd", "10. MQTT: Lekki, binarny standard IoT", "362-401"),
    "w2_11": ("wyklad_2.qmd", "11. MQTT: Tematy, QoS i „Ostatnia Wola\"", "405-453"),
    "w2_12": ("wyklad_2.qmd", "12. CoAP i AMQP", "457-480"),
    "w2_13": ("wyklad_2.qmd", "13. Podsumowanie: Dobór technologii", "484-499"),
    "w2_14": ("wyklad_2.qmd", "14. Dziękuję za uwagę", "503-510"),
    "w3_01": ("wyklad_3.qmd", "1. Od gigabajtów do wiedzy", "63-110"),
    "w3_02": ("wyklad_3.qmd", "2. Platformy korporacyjne (PaaS)", "116-141"),
    "w3_03": ("wyklad_3.qmd", "3. Narzędzia otwartoźródłowe", "145-167"),
    "w3_04": ("wyklad_3.qmd", "4. Barcelona: Pionierzy „miasta jako komputera\"", "173-198"),
    "w3_05": ("wyklad_3.qmd", "5. Smart City i Przemysł 4.0 (IIoT)", "202-227"),
    "w3_06": ("wyklad_3.qmd", "6. Cyfrowe Bliźniaki (Digital Twins)", "231-251"),
    "w3_07": ("wyklad_3.qmd", "7. Gdy „rzeczy\" stają się bronią DDoS", "257-285"),
    "w3_08": ("wyklad_3.qmd", "8. Dobre praktyki bezpieczeństwa (Defence in Depth)", "289-337"),
    "w3_09": ("wyklad_3.qmd", "9. Prywatność w epoce mikrofonów zawsze włączonych", "341-353"),
    "w3_10": ("wyklad_3.qmd", "10. Bilans korzyści i wyzwań na nową dekadę", "359-383"),
    "w3_11": ("wyklad_3.qmd", "11. Przyszłość: 6G i nowe paradygmaty", "387-399"),
    "w3_12": ("wyklad_3.qmd", "12. Zakończenie cyklu wykładów", "403-423"),
}

# materiały uzupełniające kursu (nie prezentacje) — podstawa slajdów "new"
U = {
    "u01": "lecture-materials/content/uzupelnienie-01.html",
    "u02": "lecture-materials/content/uzupelnienie-02.html",
    "u03": "lecture-materials/content/uzupelnienie-03.html",
    "u04": "lecture-materials/content/uzupelnienie-04.html",
    "u05": "lecture-materials/content/uzupelnienie-05.html",
    "u06": "lecture-materials/content/uzupelnienie-06.html",
    "u07": "lecture-materials/content/uzupelnienie-07.html",
    "s01": "lecture-materials/content/sprostowania-01.html",
    "s02": "lecture-materials/content/sprostowania-02.html",
    "s03": "lecture-materials/content/sprostowania-03.html",
    "s04": "lecture-materials/content/sprostowania-04.html",
    "s05": "lecture-materials/content/sprostowania-05.html",
    "s06": "lecture-materials/content/sprostowania-06.html",
    "s07": "lecture-materials/content/sprostowania-07.html",
    "hw": "unified-materials/content/cm178__lesson_page51__contents.html",
}

T = "title"   # slajd tytułowy
S = "sekcja"  # przekładka sekcji

# (id, rodzaj, origin, [skróty źródeł], tytuł, uzasadnienie)
MAPA = {
"00-internet-przyszlosci": [
 ("title-slide", T, "new", [], "Slajd tytułowy", "Podtytuł pierwowzoru: utopia, dystopia, rzeczywistość."),
 ("motto", "t", "adapted", ["i1_01"], "Technologia nas wyzwoli?", "Przywrócono otwarcie pierwowzoru: motto Harariego na zdjęciu Ziemi nocą."),
 ("cele", "t", "adapted", ["i1_02"], "Kto decyduje o przyszłości?", "Cytat Harariego o inżynierach; zwrot do studentów i trzy pytania wykładu zamiast listy celów."),
 ("skala", "t", "new", [], "Przyszłość jest już infrastrukturą", "Szacunek i prognozy IoT Analytics 2025 jako wykres z rozróżnieniem prognozy."),
 ("utopia", S, "new", [], "Sekcja: Utopia", "Pierwszy akt struktury pierwowzoru."),
 ("profity", "t", "adapted", ["i1_03", "i1_05", "i1_06"], "Jasna strona mocy", "Kolaż obszarów korzyści z pierwowzoru na licencjonowanych zdjęciach."),
 ("srodowisko", "t", "adapted", ["i1_10"], "Poszerzenie wiedzy o środowisku", "Nature 4.0 (Valentini 2019) pokazane na przykładach pomiarów ekosystemowych."),
 ("lancuch", "t", "new", [], "Nie rzecz, lecz pętla", "Pętla pomiar–model–decyzja–działanie na przykładzie nawadniania."),
 ("pytanie-sala", "t", "new", [], "Pytanie do sali", "Przejście od utopii do dystopii jako pytanie do dyskusji."),
 ("dystopia", S, "new", [], "Sekcja: Dystopia", "Drugi akt struktury pierwowzoru."),
 ("cambridge", "t", "adapted", ["i2_01"], "Ale czy tylko korzyści?", "Cambridge Analytica i system kredytu społecznego z pierwowzoru, w wersji zgodnej z ustaleniami FTC i MERICS."),
 ("petla-wladzy", "t", "new", [], "Pętla danych jest pętlą władzy", "Model obserwacja–inferencja–klasyfikacja–interwencja."),
 ("huxley", "t", "retained", ["i2_04"], "Cukiereczki dla mózgu", "Cytat Huxleya z pierwowzoru, odniesiony do ekonomii uwagi."),
 ("człowiek-i-maszyna", S, "new", [], "Sekcja: Człowiek i maszyna", "Przekładka sekcyjna."),
 ("czy-programy", "t", "retained", ["i2_03"], "Czy jesteśmy programami?", "Cytat Harariego z pierwowzoru i pytanie o prawo systemu do działania."),
 ("blue-gene", "t", "adapted", ["i2_02"], "Ile kosztuje mózg kota?", "Symulacja Blue Gene/P z pierwowzoru, poprawiona na publikację SC'09 (2009) zamiast Blue Brain (2007)."),
 ("ai-fizyczny", "t", "new", [], "AI wychodzi z ekranu", "Konsekwencje połączenia predykcji z działaniem fizycznym."),
 ("praca", "t", "adapted", ["i2_02"], "Bezużyteczna klasa?", "Ostrzeżenie Harariego z pierwowzoru zestawione z danymi ILO 2025."),
 ("bci", "t", "adapted", ["i2_06", "i2_07"], "Bezpośredni transfer wrażeń?", "Eksperymenty mózg–mózg z pierwowzoru z publikacjami źródłowymi i granicami interpretacji."),
 ("rzeczywistość", S, "new", [], "Sekcja: Rzeczywistość", "Trzeci akt struktury pierwowzoru."),
 ("energia", "t", "retained", ["i2_08"], "Energia jest najważniejsza", "Rachunek paliwo–człowiek z pierwowzoru, przeliczony w scripts/verify-calc.py."),
 ("centrum-danych", "t", "new", [], "Optymalizacja ma własny rachunek", "Dane IEA 2025 o zużyciu energii przez centra danych."),
 ("botnet", "t", "new", [], "Twoje urządzenie, cudza broń, czyjś odpad", "Botnet (Cloudflare 2026), koniec chmury Wemo i elektroodpady."),
 ("koordynacja", "t", "adapted", ["i2_05"], "Człowiek nie wygrał dzięki samotnej inteligencji", "Cytat Naama z pierwowzoru w przekładzie własnym."),
 ("od-wizji-do-projektu", S, "new", [], "Sekcja: Od wizji do projektu", "Przekładka sekcyjna."),
 ("pytania", "t", "new", [], "Sześć pytań przed wyborem czujnika", "Kryteria projektowe; pytania sprawdzające przeniesiono do materiałów prowadzącego."),
 ("most", "t", "new", [], "Mapa kursu", "Powiązanie pytań wykładu 00 z modułami 01–07."),
 ("podsumowanie", "t", "new", [], "Utopia, dystopia, rzeczywistość", "Synteza wykładu."),
 ("literatura", "t", "adapted", ["i2_09"], "Co warto przeczytać", "Bibliografia filozoficzna i literacka pierwowzoru."),
 ("zrodla", "t", "new", [], "Źródła", "Źródła pierwotne, publikacje naukowe i licencje ilustracji."),
],
"01-architektura-i-wymagania": [
 ("title-slide", T, "new", [], "Slajd tytułowy", "Nowy nagłówek modułu; usunięto hotlinki logotypów uczelni obecne we wszystkich taliach źródłowych."),
 ("cele", "t", "new", ["u01"], "Po co ten wykład", "Talie źródłowe nie miały slajdu celów. Dodano cele i plan drogi, wymagane przez strukturę kursu."),
 ("skąd-się-to-wzięło", S, "new", [], "Sekcja: Skąd się to wzięło", "Przekładka sekcyjna; zastępuje numerowane „Rozdział I/II” ze starej struktury."),
 ("geneza", "t", "adapted", ["w1_01", "s01"], "Od punktu do punktu", "Zachowano oś czasu. Poprawiono datowanie komputera Thorpa: koncepcja 1955, realizacja 1960–61."),
 ("coke", "t", "retained", ["w1_02"], "Mit założycielski: pragnienie", "Zachowano narrację o automacie CMU; notatkę prowadzącego przeniesiono do treści slajdu jako opis mechanizmu."),
 ("ashton", "t", "retained", ["w1_03"], "Kevin Ashton", "Zachowano dwa wątki (toster Romkeya, RFID Ashtona) bez zmian merytorycznych."),
 ("skala", "t", "adapted", ["w1_04", "s01"], "Skala zjawiska", "Zachowano tezę i wykres. Poprawiono atrybucję: Cisco IBSG (Evans 2011), nie Annual Internet Report; dodano zastrzeżenie o charakterze szacunku."),
 ("zastosowania", "t", "adapted", ["i1_03", "i1_04", "i1_06", "i1_07", "i1_08"], "Po co to robimy", "Pięć slajdów aplikacyjnych ze wstępu skondensowano w jeden przegląd, podporządkowany tezie modułu: wymagania wynikają z decyzji, nie z listy czujników."),
 ("model-odniesienia", S, "new", [], "Sekcja: Model odniesienia", "Przekładka sekcyjna."),
 ("warstwy", "t", "adapted", ["w1_05", "s01"], "Trzy warstwy", "Zachowano model trójwarstwowy. Usunięto błędne stwierdzenie o standaryzacji przez IEEE; dodano odniesienie do IEEE 2413-2019 i ISO/IEC/IEEE 42010."),
 ("przeplyw", "t", "adapted", ["w1_06"], "Przepływ w pionie", "Zachowano ideę diagramu. Usunięto trzystopniowe fragmenty i transform scale(3.5), który wypychał diagram poza slajd; dodano kierunek poleceń i reakcję lokalną."),
 ("mapa-kursu", "t", "new", ["u01"], "Warstwy a moduły kursu", "Nowa tabela wiążąca warstwy z siedmioma modułami — spoiwo nowej struktury, nieobecne w taliach źródłowych."),
 ("od-narracji-do-wymagań", S, "new", [], "Sekcja: Od narracji do wymagań", "Przekładka sekcyjna."),
 ("granica", "t", "new", ["u01"], "Granica systemu — cztery pytania", "Temat nieobecny w prezentacjach źródłowych; przeniesiony z materiałów uzupełniających kursu."),
 ("klasy", "t", "new", ["u01", "u04"], "Trzy klasy komunikatów", "Nowa tabela klas komunikatów; zapowiada regułę retained rozwiniętą w module 04."),
 ("kryterium", "t", "new", ["u01"], "Kryterium akceptacji jest liczbą", "Nowy slajd metodyczny z materiałów uzupełniających."),
 ("zalozenia", "t", "new", ["u01"], "Lista założeń", "Nowy slajd; lista założeń oddawana razem z architekturą."),
 ("stanowisko", "t", "new", ["u01"], "Przypadek: stanowisko pilotażowe", "Nowy slajd wprowadzający przypadek laboratoryjny wspólny dla siedmiu modułów."),
 ("pytania", "t", "new", [], "Pytania sprawdzające", "Nowe pytania sprawdzające; talie źródłowe ich nie zawierały."),
 ("podsumowanie", "t", "adapted", ["w1_15"], "Podsumowanie i przejście", "Zachowano funkcję podsumowania. Usunięto odwołanie do nieaktualnej struktury „wykład 1 z 3” i dodano przejście do modułu 02."),
 ("zrodla", "t", "new", [], "Źródła", "Nowy wykaz źródeł; talie źródłowe nie miały slajdu bibliograficznego."),
],
"02-urzadzenie-sensory-energia": [
 ("title-slide", T, "new", [], "Slajd tytułowy", "Nowy nagłówek modułu."),
 ("cele", "t", "new", ["u02"], "Po co ten wykład", "Nowy slajd celów."),
 ("percepcja-zmysły-i-mięśnie", S, "new", [], "Sekcja: Percepcja", "Przekładka sekcyjna."),
 ("czujniki", "t", "adapted", ["w1_07"], "Czym system czuje", "Zachowano klasyfikację czujników i ostrzeżenie o środowisku. Dodano podział ze względu na rodzaj wyjścia (analogowe / cyfrowe) jako przygotowanie do slajdu o ADC."),
 ("lancuch", "t", "new", ["u02"], "Łańcuch pomiarowy", "Nowy slajd z materiałów uzupełniających; pięć ogniw od przetwornika do walidacji lokalnej."),
 ("adc", "t", "new", ["u02", "s02"], "Rozdzielczość to nie dokładność", "Nowy slajd; sprostowanie do materiałów źródłowych, które nie rozdzielały tych pojęć. Liczby z scripts/verify-calc.py."),
 ("aktuatory", "t", "retained", ["w1_08"], "Aktuatory i pętla sterowania", "Zachowano typologię i ostrzeżenie o ryzyku twardym; pętlę sterowania uzupełniono o pomiar potwierdzający."),
 ("stan-bezpieczny", "t", "new", ["u02"], "Stan bezpieczny wyjścia", "Nowy slajd; temat nieobecny w prezentacjach źródłowych, kluczowy dla planu testów w module 07."),
 ("płytki-stanowiska", S, "new", [], "Sekcja: Płytki stanowiska", "Przekładka sekcyjna."),
 ("platformy", "t", "adapted", ["w1_11", "s02"], "Klasy platform", "Zachowano podział MCU / SBC. Sprostowano dwa stwierdzenia: brak radia nie jest cechą marki Arduino, a Raspberry Pi nie jest „przestarzałe”."),
 ("rodzina", "t", "new", ["s02", "hw"], "„ESP32” to rodzina, nie układ", "Nowy slajd; sprostowanie do slajdu porównawczego, który traktował ESP32 jako jeden model."),
 ("nano-esp32", "t", "new", ["hw"], "Arduino Nano ESP32 (ABX00083)", "Nowy slajd; potwierdzona płytka stanowiska, dane z instrukcji producenta. Ilustracje Arduino na CC BY-SA 4.0."),
 ("nano-listwa", "t", "new", ["hw"], "Nano ESP32 — co jest na listwie", "Nowa tabela wyprowadzeń z oficjalnego pinoutu ABX00083."),
 ("stamp-c3u", "t", "new", ["hw"], "M5Stack Stamp-C3U (C122-B)", "Nowy slajd; druga potwierdzona płytka. Ilustracji M5Stack nie redystrybuujemy (all rights reserved) — podano odnośnik do dokumentacji producenta."),
 ("c3-vs-c3u", "t", "new", ["hw"], "Stamp-C3 a Stamp-C3U", "Nowa tabela różnic oparta na faktach z dokumentacji; przeciwdziała myleniu wariantów."),
 ("strapping", "t", "new", ["hw"], "Piny strapping", "Nowy slajd; dane za dokumentacją Espressif, wraz z przykładem sprzecznego zapisu u producenta."),
 ("prad-pinu", "t", "new", ["u02", "hw"], "Prąd wyprowadzenia: limit, nie prąd pracy", "Nowy slajd; sprostowanie błędu „40 mA to bezpieczny prąd zalecany” obecnego w starszych materiałach."),
 ("energia", S, "new", [], "Sekcja: Energia", "Przekładka sekcyjna."),
 ("deep-sleep", "t", "adapted", ["w1_12", "s02"], "Deep sleep", "Zachowano wyjaśnienie paradygmatu. Dodano sprostowanie: wartości 7 µA i 240 µA dotyczą samego SoC, nie całej płytki."),
 ("budzet", "t", "new", ["u02"], "Budżet energii to rachunek", "Nowy slajd; wzór i wykres własny wygenerowany przez scripts/make-figures.py."),
 ("budzet-wniosek", "t", "new", ["u02"], "Ile wytrzyma ogniwo?", "Wydzielone ze slajdu budzet: wniosek dla płytki zoptymalizowanej i seryjnej (2 mA w uśpieniu)."),
 ("decyzja-okres", "t", "new", ["u02"], "Okres raportowania jest decyzją", "Nowa tabela; wszystkie wartości z scripts/verify-calc.py."),
 ("pytania", "t", "new", [], "Pytania sprawdzające", "Nowe pytania sprawdzające."),
 ("podsumowanie", "t", "new", [], "Podsumowanie i przejście", "Nowe podsumowanie modułu i zapowiedź modułu 03."),
 ("zrodla", "t", "new", [], "Źródła", "Nowy wykaz źródeł pierwotnych (Arduino, u-blox, M5Stack, Espressif)."),
],
"03-lacznosc-i-ota": [
 ("title-slide", T, "new", [], "Slajd tytułowy", "Nowy nagłówek modułu."),
 ("cele", "t", "new", ["u03"], "Po co ten wykład", "Nowy slajd celów."),
 ("fizyczne-granice", S, "new", [], "Sekcja: Fizyczne granice", "Przekładka sekcyjna."),
 ("trojkat", "t", "retained", ["w2_01"], "Trójkąt niemożliwy", "Zachowano tezę i wykres autorski scatter_triangle.png."),
 ("wifi", "t", "adapted", ["w2_02", "u03"], "Wi-Fi", "Zachowano bilans zalet i wad. Dodano powiązanie z doborem dla stanowiska i przypomnienie o braku pasma 5 GHz na obu płytkach."),
 ("ble-mesh", "t", "adapted", ["w2_03", "w2_04", "s03"], "Bluetooth LE i sieci kratowe", "Scalono dwa slajdy źródłowe. Dodano warunek „samoleczenia” sieci mesh i aktualną nazwę organizacji (Connectivity Standards Alliance, Matter)."),
 ("lpwan", "t", "retained", ["w2_05", "w2_06"], "LPWAN", "Zachowano opis i wykres bąbelkowy; scalono ze slajdem porównawczym, by uniknąć powtórzenia."),
 ("lora-nbiot", "t", "adapted", ["w2_07", "s03"], "LoRaWAN a NB-IoT", "Zachowano zestawienie. Sprostowano „darmowe pasmo 868 MHz” (regulowane, duty cycle) i status NB-IoT (3GPP Rel. 13, własna warstwa radiowa)."),
 ("brama-lorawan", "t", "adapted", ["w1_09", "w2_07"], "Brama LoRaWAN to infrastruktura", "Dodano fotografię rzeczywistej bramy i rozdzielono role węzła radiowego, bramy i serwera sieciowego."),
 ("sigfox", "t", "adapted", ["w2_08", "s03"], "Sigfox", "Zachowano parametry. Dodano zmianę właściciela (UnaBiz, Sigfox 0G) i ryzyko operatora jako parametr projektowy."),
 ("cztery-liczby", "t", "new", ["u03"], "Metodyka doboru — cztery liczby", "Nowy slajd metodyczny; zamienia porównanie technologii w powtarzalną procedurę."),
 ("łącze-które-się-podnosi", S, "new", [], "Sekcja: Łącze", "Przekładka sekcyjna."),
 ("reconnect", "t", "new", ["u03"], "Ponowne łączenie z wycofaniem", "Nowy slajd; temat nieobecny w prezentacjach źródłowych."),
 ("bufor", "t", "new", ["u03"], "Buforowanie w czasie awarii", "Nowy slajd; trzy warunki poprawnego buforowania plus pułapka znacznika czasu."),
 ("wydanie-firmware", S, "new", [], "Sekcja: Wydanie firmware", "Przekładka sekcyjna."),
 ("ota-co-to", "t", "new", ["u03", "s03"], "OTA to nie nadpisanie firmware", "Nowy slajd; wypełnia lukę odnotowaną w mapowaniu modułów (OTA nie występował w żadnej z pięciu talii źródłowych)."),
 ("ota-api", "t", "new", ["u03"], "Mechanizmy ESP-IDF", "Nowa tabela mechanizmów OTA z dokumentacji Espressif."),
 ("self-test", "t", "new", ["u03"], "Self-test i wycofanie", "Nowy slajd; kolejność dowód → zatwierdzenie jako sedno mechanizmu."),
 ("ota-granice", "t", "new", [], "Czego OTA nie gwarantuje", "Nowy slajd napisany, by nie formułować fałszywych obietnic o niezawodności aktualizacji."),
 ("ota-platforma", "t", "new", ["u03"], "Wydanie zarządzane przez platformę", "Nowy slajd; stany pakietu i tempo wdrożenia, liczby z scripts/verify-calc.py."),
 ("ota-tempo", "t", "new", ["u03"], "Tempo wdrożenia jest ograniczone", "Wydzielone ze slajdu ota-platforma: parametry wysyłki i czas wydania."),
 ("procedura", "t", "new", ["u03"], "Procedura wydania w pilocie", "Nowy slajd; sześciopunktowa procedura z kryterium zaliczenia."),
 ("pytania", "t", "new", [], "Pytania sprawdzające", "Nowe pytania sprawdzające."),
 ("podsumowanie", "t", "new", [], "Podsumowanie i przejście", "Nowe podsumowanie i zapowiedź modułu 04."),
 ("zrodla", "t", "new", [], "Źródła", "Nowy wykaz źródeł pierwotnych."),
],
"04-mqtt-i-kontrakt-danych": [
 ("title-slide", T, "new", [], "Slajd tytułowy", "Nowy nagłówek modułu."),
 ("cele", "t", "new", ["u04"], "Po co ten wykład", "Nowy slajd celów."),
 ("protokół", S, "new", [], "Sekcja: Protokół", "Przekładka sekcyjna."),
 ("http", "t", "adapted", ["w2_09"], "Dlaczego HTTP nie pasuje", "Zachowano trzy argumenty. Usunięto diagram porównawczy o zmyślonych rozmiarach pakietów na rzecz rachunku na slajdzie „Nagłówek MQTT”; dodano zastrzeżenie, że problemem jest rola, nie protokół."),
 ("mqtt", "t", "adapted", ["w2_10", "s04"], "MQTT: publikacja i subskrypcja", "Zachowano opis pub/sub i diagram. Sprostowano autorstwo (Stanford-Clark i Nipper) oraz status normalizacyjny (OASIS, ISO/IEC 20922:2016)."),
 ("naglowek", "t", "new", ["s04"], "Ile naprawdę waży nagłówek", "Nowy slajd; sprostowanie do „nagłówek MQTT to 2 bajty”. Rozmiary pakietów policzone w scripts/verify-calc.py."),
 ("tematy-i-niezawodność", S, "new", [], "Sekcja: Tematy i niezawodność", "Przekładka sekcyjna."),
 ("tematy", "t", "new", ["u04"], "Drzewo tematów pilota", "Nowa tabela; konkretne drzewo tematów z kierunkiem i regułą retained."),
 ("retained", "t", "new", ["u04"], "Dlaczego polecenie nigdy nie jest retained", "Nowy slajd z diagramem sekwencji; konsekwencja fizyczna błędu projektowego."),
 ("qos", "t", "adapted", ["w2_11", "s04", "s06"], "QoS i jego koszt", "Zachowano poziomy QoS i LWT. Sprostowano „QoS 2 gwarantuje dostarczenie”; dodano kolumnę kosztu oraz ograniczenie platformy do QoS 0/1."),
 ("mechanizmy", "t", "new", ["u04"], "Retained, Last Will, keep alive, sesja", "Wydzielone z przeładowanego slajdu QoS; doprecyzowane wg MQTT 5 (0x04, 1,5 × keep alive)."),
 ("qos-sekwencja", "t", "retained", ["w2_11"], "Sekwencja trzech poziomów", "Zachowano diagram sekwencji ze źródła; usunięto transform scale(1.7) powodujący wyjście poza slajd."),
 ("kontrakt-danych", S, "new", [], "Sekcja: Kontrakt danych", "Przekładka sekcyjna."),
 ("kontrakt", "t", "new", ["u04"], "Samoopisujący się ładunek", "Nowy slajd; schemat komunikatu JSON z materiałów uzupełniających."),
 ("wersjonowanie", "t", "new", ["u04"], "Wersjonowanie kontraktu", "Nowy slajd; zmiana zgodna i niezgodna wstecz."),
 ("idempotencja", "t", "new", ["u04"], "Idempotencja polecenia", "Nowy slajd z diagramem sekwencji."),
 ("dostep", "t", "new", ["u04", "s04"], "Zamknięcie dostępu do brokera", "Nowy slajd; ACL, TLS, unikalny ClientID. Sprostowano separację środowisk przez prefiks."),
 ("coap-amqp", "t", "adapted", ["w2_12", "s04"], "CoAP i AMQP", "Zachowano zestawienie. Sprostowano „bez gwarancji dostarczenia” dla CoAP (tryb confirmable)."),
 ("test-odbioru", "t", "new", ["u04"], "Test odbioru kontraktu", "Nowy slajd; pięć dowodów działania kontraktu."),
 ("zestawienie", "t", "retained", ["w2_13"], "Dobór technologii", "Zachowano tabelę podsumowującą; zaktualizowano nazwę Sigfox 0G."),
 ("pytania", "t", "new", [], "Pytania sprawdzające", "Nowe pytania sprawdzające."),
 ("podsumowanie", "t", "new", [], "Podsumowanie i przejście", "Nowe podsumowanie i zapowiedź modułu 05."),
 ("zrodla", "t", "new", [], "Źródła", "Nowy wykaz źródeł pierwotnych (OASIS, RFC, Mosquitto)."),
],
"05-brzeg-node-red-sheets": [
 ("title-slide", T, "new", [], "Slajd tytułowy", "Nowy nagłówek modułu."),
 ("cele", "t", "new", ["u05"], "Po co ten wykład", "Nowy slajd celów."),
 ("brzeg-sieci", S, "new", [], "Sekcja: Brzeg sieci", "Przekładka sekcyjna."),
 ("redukcja", "t", "retained", ["w3_01"], "Od gigabajtów do wiedzy", "Zachowano tezę i diagram redukcji danych; usunięto transform scale(2) i dodano gałąź zapisu raportowego."),
 ("brama", "t", "adapted", ["w1_09", "s05"], "Brama brzegowa — cztery zadania", "Zachowano definicję bramy i pojęcie latency. Rozszerzono z samej agregacji na cztery zadania, zgodnie ze sprostowaniem."),
 ("jakosc", "t", "new", ["s05"], "Piąte zadanie: jakość danych", "Nowy slajd; sprostowanie do opisu Node-RED jako „kleju” bez odpowiedzialności."),
 ("przepływ", S, "new", [], "Sekcja: Przepływ", "Przekładka sekcyjna."),
 ("przeplyw", "t", "new", ["u05"], "Node-RED węzeł po węźle", "Nowy slajd; konkretny przepływ z jawną ścieżką błędu."),
 ("walidacja", "t", "new", ["u05"], "Minimalny zestaw reguł walidacji", "Nowy slajd; pięć reguł i wymóg logowania powodu odrzucenia."),
 ("zapis-do-arkusza", S, "new", [], "Sekcja: Zapis do arkusza", "Przekładka sekcyjna."),
 ("warianty", "t", "new", ["u05", "s05"], "Dwa warianty zapisu", "Nowa tabela; Apps Script a Sheets API v4, wraz ze sprostowaniem o adresie wdrożenia jako sekrecie."),
 ("limity", "t", "new", ["u05"], "Limity Google Sheets API", "Nowy slajd; limity z dokumentacji Google, wykres własny z scripts/make-figures.py."),
 ("ponowienia", "t", "new", ["u05"], "Ponowienia i granice arkusza", "Nowy slajd; rozróżnienie błędów ponawialnych i nieponawialnych."),
 ("autoryzacja", "t", "new", ["u05"], "Autoryzacja i błędy eksportu", "Nowy slajd; procedura konta usługi i tabela kodów odpowiedzi."),
 ("test-odbioru", "t", "new", ["u05"], "Test odbioru przepływu", "Nowy slajd; pięć dowodów działania przepływu."),
 ("pytania", "t", "new", [], "Pytania sprawdzające", "Nowe pytania sprawdzające."),
 ("podsumowanie", "t", "new", [], "Podsumowanie i przejście", "Nowe podsumowanie i zapowiedź modułu 06."),
 ("zrodla", "t", "new", [], "Źródła", "Nowy wykaz źródeł pierwotnych (Google, Node-RED)."),
],
"06-thingsboard-ce": [
 ("title-slide", T, "new", [], "Slajd tytułowy", "Nowy nagłówek modułu."),
 ("cele", "t", "new", ["u06"], "Po co ten wykład", "Nowy slajd celów."),
 ("model-danych", S, "new", [], "Sekcja: Model danych", "Przekładka sekcyjna."),
 ("model-najpierw", "t", "new", ["u06", "s06"], "Wykres jest ostatni", "Nowy slajd; sprostowanie do traktowania platformy jako „dashboardu w chmurze”."),
 ("rodzaje", "t", "new", ["u06"], "Trzy rodzaje danych", "Nowa tabela; telemetria a cztery kategorie atrybutów."),
 ("wspoldzielone", "t", "new", ["u06"], "Atrybuty współdzielone", "Nowy slajd; konfiguracja bez ponownego wgrywania firmware."),
 ("styk-z-urządzeniem", S, "new", [], "Sekcja: Styk z urządzeniem", "Przekładka sekcyjna."),
 ("tematy", "t", "new", ["u06", "s06"], "Kontrakt tematów MQTT platformy", "Nowa tabela tematów standardowych i skróconych; sprostowanie o braku QoS 2."),
 ("poswiadczenia", "t", "new", ["u06"], "Poświadczenia urządzenia", "Nowy slajd; trzy typy poświadczeń i ostrzeżenie o tokenie jako sekrecie."),
 ("rpc", "t", "new", ["u06"], "Sterowanie zwrotne: RPC", "Nowy slajd z diagramem sekwencji; stan potwierdzony wobec żądanego."),
 ("pulpit", "t", "new", ["u06"], "Od telemetrii do pulpitu", "Nowy slajd; co pulpit powinien pokazywać i czego nie zastąpi."),
 ("pulpit-przyklad", "t", "new", ["u06"], "Pulpit ma pokazywać stan, nie tylko wykres", "Nowy slajd wizualny; przykład pulpitu środowiskowego służy do rozróżnienia stanu bieżącego, kontekstu i alarmu."),
 ("kontekst-i-ryzyko", S, "new", [], "Sekcja: Kontekst i ryzyko", "Przekładka sekcyjna."),
 ("bliźniak", "t", "adapted", ["w3_06", "w1_13", "s06"], "Cyfrowy bliźniak", "Scalono dwa slajdy źródłowe z dwóch różnych talii w jedno omówienie, zgodnie ze sprostowaniem o powtórzeniu. Dodano zastrzeżenie, że to nie wizualizacja 3D."),
 ("smart-city", "t", "adapted", ["w3_04", "w3_05", "s01"], "Zastosowania w skali miasta", "Scalono dwa slajdy o Smart City. Usunięto konkretne wartości procentowe jako danych pomiarowych; dodano zastrzeżenie o poglądowym charakterze liczb."),
 ("ryzyko", "t", "adapted", ["w3_02", "s06"], "Ryzyko dostawcy i licencji", "Zachowano przypadek Google IoT Core. Uściślono daty (ogłoszenie 2022-08, wyłączenie 2023-08-16) i dodano ryzyko zmiany licencji oprogramowania lokalnego."),
 ("ce-pe", "t", "new", ["u06", "s06"], "CE a PE", "Nowy slajd; sprostowanie o „fizycznej izolacji środowisk” i ostrzeżenie przed materiałami dotyczącymi PE."),
 ("test-odbioru", "t", "new", ["u06"], "Test odbioru modułu", "Nowy slajd; pięć dowodów."),
 ("pytania", "t", "new", [], "Pytania sprawdzające", "Nowe pytania sprawdzające."),
 ("podsumowanie", "t", "new", [], "Podsumowanie i przejście", "Nowe podsumowanie i zapowiedź modułu 07."),
 ("zrodla", "t", "new", [], "Źródła", "Nowy wykaz źródeł pierwotnych (ThingsBoard, Google Cloud)."),
],
"07-odpornosc-bezpieczenstwo-eksploatacja": [
 ("title-slide", T, "new", [], "Slajd tytułowy", "Nowy nagłówek modułu."),
 ("cele", "t", "new", ["u07"], "Po co ten wykład", "Nowy slajd celów."),
 ("sekcja-rama", S, "new", [], "Sekcja: Rama", "Przekładka sekcyjna."),
 ("rama", "t", "adapted", ["i1_01", "i1_02", "s07"], "Kto tworzy skutki", "Scalono dwa slajdy otwierające wstęp w jedną ramę odpowiedzialności. Zgodnie ze sprostowaniem umieszczono ją przy eksploatacji jako decyzję inżynierską, nie dygresję."),
 ("odporność", S, "new", [], "Sekcja: Odporność", "Przekładka sekcyjna."),
 ("nieaktywnosc", "t", "new", ["u07"], "Wykrycie nieaktywności", "Nowy slajd; atrybuty stanu urządzenia i parametry progu."),
 ("pulapka", "t", "new", ["u07"], "Pułapka fałszywego alarmu", "Nowy slajd; zależność progu od okresu raportowania aktywności, liczby z scripts/verify-calc.py."),
 ("alarm", "t", "new", ["u07"], "Alarm i dowód jego zamknięcia", "Nowy slajd; wymóg pojedynczego powiadomienia i samoczynnego zamknięcia."),
 ("bezpieczeństwo", S, "new", [], "Sekcja: Bezpieczeństwo", "Przekładka sekcyjna."),
 ("model-zagrozen", "t", "new", ["u07"], "Model zagrożeń", "Nowa tabela czterech powierzchni ataku; porządkuje mechanizmy wprowadzone w modułach 03–06."),
 ("mirai", "t", "adapted", ["w3_07", "s07"], "Mirai — dwa incydenty", "Zachowano przypadek. Rozdzielono dwa łączone wcześniej incydenty (Dyn 2016-10-21, TR-064 Deutsche Telekom 2016-11). Usunięto mapę o nieudokumentowanym pochodzeniu."),
 ("kryptografia", "t", "new", ["s07"], "Brak mocy na kryptografię to nieprawda", "Nowy slajd; dwa sprostowania — akceleratory sprzętowe w ESP32-S3/C3 oraz X.509 jako format, nie algorytm."),
 ("defence", "t", "adapted", ["w3_08", "s07"], "Obrona warstwowa", "Zachowano cztery warstwy i diagram segmentacji. Sprostowano, że VLAN bez polityki odmowy domyślnej nie izoluje; usunięto transform scale(1.7)."),
 ("eksploatacja", S, "new", [], "Sekcja: Eksploatacja", "Przekładka sekcyjna."),
 ("testy-awarii", "t", "new", ["u07"], "Plan testów awarii", "Nowy slajd; pięć scenariuszy wiążących mechanizmy ze wszystkich modułów."),
 ("higiena", "t", "new", ["u07"], "Higiena testu powiadomień", "Nowy slajd; domena .invalid i osobny łańcuch reguł."),
 ("prywatnosc", "t", "adapted", ["w3_09", "u07"], "Prywatność: dane pośrednie", "Zachowano trzy przykłady profilowania. Dodano pojęcie danych osobowych pośrednich i wymóg minimalizacji."),
 ("obowiazki", "t", "new", ["u07", "s07"], "Obowiązki poza kodem", "Nowy slajd; aktualne daty Cyber Resilience Act i dokumentacja wyjścia z systemu."),
 ("koszt-energii", "t", "adapted", ["i2_08"], "Koszt energii jako rama", "Zachowano porównanie człowiek / samochód. Przeliczenie zweryfikowane w scripts/verify-calc.py; powiązane z budżetem energii z modułu 02."),
 ("bilans", "t", "adapted", ["w3_10", "w3_11", "s07"], "Bilans korzyści i wyzwań", "Scalono bilans i slajd o przyszłości. Dodano sprostowanie: opóźnienia sub-milisekundowe 6G to cele badawcze, nie parametry wdrożonego standardu."),
 ("pytania", "t", "new", [], "Pytania sprawdzające", "Nowe pytania sprawdzające."),
 ("zamkniecie", "t", "adapted", ["w3_12", "i2_09"], "Zamknięcie cyklu", "Zachowano puentę o automacie z napojami i pytanie do audytorium. Rozszerzono pytanie o odpowiedzialność; dołączono listę lektur ze wstępu części 2."),
 ("zrodla", "t", "new", [], "Źródła i dalsza lektura", "Nowy wykaz źródeł pierwotnych oraz lektura uzupełniająca."),
],
}

# --- Slajdy źródłowe świadomie nieprzeniesione ---------------------------
ODRZUCONE = [
 ("i1_09", "Cykl IoT & AI — cztery generacje", "Narracja o generacjach 1.0–4.0 nie wnosi kryterium projektowego; jej funkcję („po co mierzymy”) przejął slajd 01#zastosowania."),
 ("i1_11", "Podsumowanie Wstępu", "Podsumowanie nieistniejącej już części „Wstęp 1”; zastąpione podsumowaniami modułów."),
 ("w1_10", "Od pomysłu do wdrożenia", "Teza o obniżeniu bariery wejścia wchłonięta przez 02#platformy; osobny slajd nie wnosił kryterium wyboru."),
 ("w1_14", "Zestawienie Arduino vs ESP vs Raspberry Pi", "Tabela zbudowana na nieaktualnych założeniach (Arduino bez radia, Raspberry Pi „przestarzałe”). Zastąpiona przez 02#platformy i 02#rodzina, opartymi na płytkach stanowiska."),
 ("w3_03", "Narzędzia otwartoźródłowe", "Lista narzędzi wchłonięta: Node-RED do modułu 05, ThingsBoard do 06 wraz ze sprostowaniem o statusie licencyjnym. Osobny slajd powielałby treść."),
 ("w2_14", "Dziękuję za uwagę (zapowiedź wykładu 3)", "Slajd czysto organizacyjny, zapowiadający nieaktualną strukturę trzech wykładów. Każdy moduł ma własne podsumowanie z przejściem do kolejnego."),
]

# --- Zewnętrzne ilustracje wykorzystane w slajdach ------------------------
ILUSTRACJE_WYKORZYSTANE = [
 ("kurs/kasa-kody.jpg", 'U.S. Navy photo by Photographer’s Mate 1st Class Michael W. Pendergrass.', 'https://commons.wikimedia.org/wiki/File:US_Navy_020813-N-3235P-532_A_Navy_family_unloads_their_shopping_cart_while_purchasing_groceries_at_the_Navy_Commissary_located_just_outside_Naval_Air_Station_Oceana.jpg', 'domena publiczna', ['01#skąd-się-to-wzięło']),
 ("kurs/operatorzy.jpg", 'PEO ACWA', 'https://commons.wikimedia.org/wiki/File:Blue_Grass_Chemical_Agent-Destruction_Pilot_Plant_Control_Room_Operators_(33545979468).jpg', 'CC BY 2.0', ['01#model-odniesienia']),
 ("kurs/stacja-meteo-antarktyda.jpg", 'William M. Connolley', 'https://commons.wikimedia.org/wiki/File:IMG_0430-aws-rothera_1200x900.jpg', 'CC BY-SA 3.0', ['01#od-narracji-do-wymagań']),
 ("kurs/rfid-etykieta.jpg", 'Boevaya mashina', 'https://commons.wikimedia.org/wiki/File:RFID_tag_in_textile_label_disassembled.jpg', 'CC BY-SA 4.0', ['01#ashton']),
 ("kurs/lutowanie.jpg", 'Aisart', 'https://commons.wikimedia.org/wiki/File:Soldering_a_0805.jpg', 'CC BY-SA 3.0', ['02#percepcja-zmysły-i-mięśnie']),
 ("kurs/pcb-smd.jpg", 'wdwd', 'https://commons.wikimedia.org/wiki/File:SMD_circuit_on_a_wave_soldered_PCB.JPG', 'CC BY-SA 4.0', ['02#płytki-stanowiska']),
 ("kurs/ogniwa.jpg", 'Mk2010', 'https://commons.wikimedia.org/wiki/File:18650_Li-ion_%26_Panasonic_CR123A_20121116.jpg', 'CC BY-SA 3.0', ['02#energia']),
 ("kurs/esp32-plytka.jpg", 'Edwiyanto', 'https://commons.wikimedia.org/wiki/File:ESP32_Dev_Board.jpg', 'CC BY-SA 4.0', ['02#platformy']),
 ("kurs/raspberry-pi.jpg", 'Laserlicht', 'https://commons.wikimedia.org/wiki/File:Raspberry_Pi_4_Model_B_-_Top.jpg', 'CC BY-SA 4.0', ['02#platformy', '05#brama']),
 ("kurs/multimetr-prad.jpg", 'Christiankral', 'https://commons.wikimedia.org/wiki/File:Fluke_multimeter_DC_current.jpg', 'CC BY 4.0', ['02#deep-sleep']),
 ("kurs/maszty.jpg", 'CEphoto, Uwe Aranas', 'https://commons.wikimedia.org/wiki/File:Lahad-Datu_Sabah_Mount-Silam-Telecommunication-towers-01.jpg', 'CC BY-SA 3.0', ['03#fizyczne-granice']),
 ("kurs/przelacznik.jpg", 'Raysonho @ Open Grid Scheduler / Grid Engine', 'https://commons.wikimedia.org/wiki/File:EthernetSwitch.jpg', 'CC0', ['03#łącze-które-się-podnosi']),
 ("kurs/szafa-sieciowa.jpg", 'Shixart1985', 'https://commons.wikimedia.org/wiki/File:Network_equipment_and_cables_organized_in_a_server_rack_at_a_modern_office_environment_during_the_afternoon.jpg', 'CC BY 2.0', ['03#wydanie-firmware']),
 ("kurs/router-wifi.jpg", 'Florian838', 'https://commons.wikimedia.org/wiki/File:TP-Link_WR841ND_WiFi_router_transparent.png', 'CC BY 4.0', ['03#wifi']),
 ("kurs/stacja-czujnikowa.jpg", 'NOAA', 'https://commons.wikimedia.org/wiki/File:PHOTO-IMETs-traiining-Incident-Remote-Automatic-Weather-Station-2023.jpg', 'domena publiczna', ['03#lpwan']),
 ("kurs/sortownia-poczty.jpg", 'Archives New Zealand from New Zealand', 'https://commons.wikimedia.org/wiki/File:General_Post_Office_mail_sorting_room,_Wellington_c.1900s.jpg', 'CC BY-SA 2.0', ['04#protokół']),
 ("kurs/panel-krosowy.jpg", 'Dsimic', 'https://commons.wikimedia.org/wiki/File:19-inch_rackmount_Ethernet_switches_and_patch_panels.jpg', 'CC BY-SA 4.0', ['04#tematy-i-niezawodność']),
 ("kurs/panel-sterowania.jpg", 'Shixart1985', 'https://commons.wikimedia.org/wiki/File:Control_panel_displays_settings_and_data_for_industrial_equipment.jpg', 'CC BY 2.0', ['04#kontrakt-danych']),
 ("kurs/raspberry-przelacznik.jpg", 'RAIL P\xa0(RAIL.PHOTOGRAPHY)', 'https://commons.wikimedia.org/wiki/File:Raspberry_Pi_4_on_a_network_switch.jpg', 'CC0', ['05#brzeg-sieci']),
 ("kurs/kable-splatane.jpg", 'Kim Scarborough from Chicago, IL', 'https://commons.wikimedia.org/wiki/File:Server_Rack_with_Spaghetti-Like_Mass_of_Network_Cables.jpg', 'CC BY-SA 2.0', ['05#przepływ']),
 ("kurs/sterownia-nasa.jpg", 'NASA Glenn Research Center', 'https://commons.wikimedia.org/wiki/File:Operators_in_the_Plum_Brook_Reactor_Facility_Control_Room_(GRC-1970-C-00860).jpg', 'domena publiczna', ['05#zapis-do-arkusza']),
 ("kurs/monitory-diagnostyczne.jpg", 'Siarhei Besarab', 'https://commons.wikimedia.org/wiki/File:Diagnostic_monitors_in_the_control_room_of_Wendelstein_7-X.jpg', 'CC BY-SA 4.0', ['06#model-danych']),
 ("kurs/panel-robota.jpg", 'Artem Svetlov from Moscow, Russia', 'https://commons.wikimedia.org/wiki/File:%D0%9F%D0%B0%D0%BD%D0%B5%D0%BB%D1%8C_%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F_%D1%80%D0%BE%D0%B1%D0%BE%D1%82%D0%BE%D0%BC_(14660763727).jpg', 'CC BY 2.0', ['06#styk-z-urządzeniem']),
 ("kurs/turbina-serwis.jpg", 'U.S. Department of Energy from United States', 'https://commons.wikimedia.org/wiki/File:Wind_turbine_maintenance_(51689968067).jpg', 'domena publiczna', ['06#kontekst-i-ryzyko']),
 ("kurs/oscyloskop.jpg", 'Jrmlhermitte', 'https://commons.wikimedia.org/wiki/File:Oscilloscope_with_a_Doppler_radar_signal.jpg', 'CC BY-SA 4.0', ['07#odporność']),
 ("kurs/klodka.jpg", 'Lacz02', 'https://commons.wikimedia.org/wiki/File:Padlock_with_chain.jpg', 'CC BY-SA 4.0', ['07#bezpieczeństwo']),
 ("kurs/panel-maszyny.jpg", 'Shixart1985', 'https://commons.wikimedia.org/wiki/File:Worker_interacts_with_machine_control_panel_in_a_manufacturing_facility.jpg', 'CC BY 2.0', ['07#eksploatacja']),
 ("zasieg-przepustowosc.png", "wykres własny", "scripts/make-figures.py", "CC BY 4.0", ["03#trojkat"]),
 ("iot-urzadzenia.png", "wykres własny (dane IoT Analytics 2025)", "scripts/make-figures.py", "CC BY 4.0", ["00#skala", "01#skala"]),
 ("energia-auto-czlowiek.png", "wykres własny", "scripts/make-figures.py", "CC BY 4.0", ["00#energia", "07#koszt-energii"]),
 ("lecture00/ziemia-noca.jpg", "NASA Goddard Space Flight Center", "https://commons.wikimedia.org/wiki/File:Black_Marble_-_City_Lights_2012_(8246892319).jpg", "domena publiczna", ["00#motto", "07#rama"]),
 ("lecture00/harari.jpg", "Martin Kraft", "https://commons.wikimedia.org/wiki/File:MKr364740_Yuval_Noah_Harari_(Frankfurter_Buchmesse_2024)_(cropped).jpg", "CC BY-SA 4.0", ["00#cele"]),
 ("lecture00/dron-ryz.jpg", "Christopher Hedreyd, PIA", "https://commons.wikimedia.org/wiki/File:IRRI_BBM_rice_drone_demo_2.jpg", "domena publiczna", ["00#profity"]),
 ("lecture00/opaski-fitness.jpg", "Abas Gemini", "https://commons.wikimedia.org/wiki/File:Fitness-trackers-companies-Fitbug-Orb-Jawbone-Up.jpg", "CC BY-SA 4.0", ["00#profity"]),
 ("lecture00/deszczownia.jpg", "Killarnee", "https://commons.wikimedia.org/wiki/File:Center-pivot_irrigation_system_-_1.jpg", "CC BY-SA 4.0", ["00#profity"]),
 ("lecture00/licznik-energii.jpg", "277volts", "https://commons.wikimedia.org/wiki/File:Aclara_I-210%2B_single_phase_smart_electricity_meter.jpg", "CC BY-SA 4.0", ["00#profity"]),
 ("lecture00/kowariancja-wirow.jpg", "Veedar", "https://commons.wikimedia.org/wiki/File:Eddy_Covariance_IRGA_Sonic.jpg", "domena publiczna", ["00#srodowisko"]),
 ("lecture00/czujnik-wilgotnosci.jpg", "P e z i", "https://commons.wikimedia.org/wiki/File:Cosmic_Ray_Sensor_for_soil_moisture_measurements-DSC_6642w.jpg", "CC BY-SA 3.0 AT", ["00#srodowisko"]),
 ("lecture00/instalacja-czujnikow.jpg", "UBC Micrometeorology", "https://commons.wikimedia.org/wiki/File:Installation_of_soil_sensors.jpg", "CC BY 2.0", ["00#srodowisko"]),
 ("lecture00/wylie.jpg", "Chatham House", "https://commons.wikimedia.org/wiki/File:Christopher_Wylie_at_Chatham_House_-_2018_(42624320935).jpg", "CC BY 2.0", ["00#cambridge"]),
 ("lecture00/kamery.jpg", "µKöff", "https://commons.wikimedia.org/wiki/File:2020-04-05_17.18.01_Pole_with_surveillance_cameras_in_Saarbr%C3%BCcken.jpg", "CC BY 4.0", ["00#cambridge"]),
 ("lecture00/huxley.jpg", "Dwight (Shadowland, 1923)", "https://commons.wikimedia.org/wiki/File:Aldous_Huxley_(Dwight,_July_1923).jpg", "domena publiczna", ["00#huxley"]),
 ("lecture00/blue-gene-p.jpg", "Argonne National Laboratory", "https://commons.wikimedia.org/wiki/File:IBM_Blue_Gene_P_supercomputer.jpg", "CC BY-SA 2.0", ["00#blue-gene"]),
 ("lecture00/robot-papryka.jpg", "Lozada, Bosland, Barchenger, Haghshenas-Jaryani, Sanogo, Walker", "https://commons.wikimedia.org/wiki/File:Robotic_arm_with_a_cutter_end-effector_harvesting_green_chile_peppers_in_an_indoor_setting.jpg", "CC BY 4.0", ["00#ai-fizyczny"]),
 ("lecture00/brain-to-brain.jpg", "C. Grau i in. (PLoS ONE 2014)", "https://commons.wikimedia.org/wiki/File:Brain-to-brain_(B2B)_communication_system_overview.jpg", "CC BY 4.0", ["00#bci"]),
 ("lecture00/centrum-danych.jpg", "BalticServers.com", "https://commons.wikimedia.org/wiki/File:BalticServers_data_center.jpg", "CC BY-SA 3.0", ["00#centrum-danych"]),
 ("lecture00/wemo.jpg", "Harborsparrow", "https://commons.wikimedia.org/wiki/File:Wemo_smart_plugs_and_switches.jpg", "CC BY-SA 4.0", ["00#botnet"]),
 ("lecture00/elektroodpady.jpg", "AvWijk", "https://commons.wikimedia.org/wiki/File:Ewaste-pile.jpg", "domena publiczna", ["00#botnet"]),
 ("lecture00/naam.jpg", "Sebastiaan ter Burg", "https://commons.wikimedia.org/wiki/File:Ramez_Naam_at_the_SingularityU_The_Netherlands_Summit_2016_(29025926993)_(cropped).jpg", "CC BY 2.0", ["00#koordynacja"]),
 ("lecture00/lem.jpg", "Wojciech Zemek (archiwum S. Lema)", "https://commons.wikimedia.org/wiki/File:St_Lem_resize.jpg", "CC BY-SA 3.0", ["00#literatura"]),
 ("arduino-nano-esp32-board.png", "Arduino", "https://docs.arduino.cc/hardware/nano-esp32/", "CC BY-SA 4.0", ["02#nano-esp32"]),
 ("arduino-nano-esp32-pinout.png", "Arduino", "https://docs.arduino.cc/resources/pinouts/ABX00083-full-pinout.pdf", "CC BY-SA 4.0", ["02#nano-listwa"]),
 ("irrigation-navfac.jpg", "NAVFAC", "https://commons.wikimedia.org/wiki/File:New_water-saving_irrigation_system_tested_at_NAVFAC_EXWC_(8099733341).jpg", "CC BY 2.0", ["00#lancuch"]),
 ("iiot-building-blocks.jpg", "Sujata Tilak, Ascent Intellimation Pvt. Ltd.", "https://commons.wikimedia.org/wiki/File:IIoT_System_Building_Blocks.jpg", "CC BY-SA 4.0", ["01#warstwy"]),
 ("kerlink-lorawan-gateway.jpg", "Fabian Horst", "https://commons.wikimedia.org/wiki/File:2020-10-05_-_Kerlink_LoRaWAN_Gateway_in_Kiel.jpg", "CC BY-SA 4.0", ["03#brama-lorawan"]),
 ("mqtt-broker-listeners.svg", "Ademant", "https://commons.wikimedia.org/wiki/File:MQTT_single_broker_multiple_listener.svg", "CC BY-SA 4.0", ["04#mqtt"]),
 ("node-red-example.png", "1-Byte", "https://commons.wikimedia.org/wiki/File:Node-RED_Example.png", "CC BY-SA 4.0", ["05#przeplyw"]),
 ("iot-dashboard-aquaculture.jpg", "Stephane Malhomme", "https://commons.wikimedia.org/wiki/File:Aquaculture_iot_water_monitoring_solution_pentair_eagle.io.jpg", "CC BY-SA 4.0", ["06#pulpit-przyklad"]),
 ("axis-ip-cameras.png", "Bungle", "https://commons.wikimedia.org/wiki/File:Axis_ip_dome_cameras.png", "CC BY-SA 4.0", ["07#mirai", "00#botnet"]),
]

# --- Ilustracje wykluczone z nowego repozytorium -------------------------
ILUSTRACJE_ODRZUCONE = [
 ("img/Oura-ring.jpg", "Brak udokumentowanego źródła i licencji."),
 ("img/IIoT-smart-manufacturing-smart-factory-3751296197.jpg", "Zdjęcie stockowe bez udokumentowanej licencji."),
 ("img/residential-sprinkler-systems-2663960231.jpg", "Zdjęcie stockowe bez udokumentowanej licencji."),
 ("img/smart_transportation_781x512-1163925340.jpg", "Zdjęcie stockowe bez udokumentowanej licencji."),
 ("img/th-1774962466.png", "Brak udokumentowanego źródła."),
 ("img/Pasted image 2022*.png", "Zrzuty ekranu i ilustracje o nieustalonym pochodzeniu (14 plików użytych w taliach źródłowych)."),
 ("img/mirai_map.png", "Mapa bez wskazania autora i źródła danych; treść przeniesiona do tekstu slajdu 07#mirai."),
 ("img/iot_dashboard.png", "Zrzut ekranu bez wskazania wersji i licencji oprogramowania."),
 ("img/digital_twin_nature.png", "Brak udokumentowanego źródła."),
 ("img/mcu_compare.png", "Brak udokumentowanego źródła; zastąpione tabelami opartymi na dokumentacji producentów."),
 ("img/lpwan_station.png", "Brak udokumentowanego źródła."),
 ("img/iot_tlo_gr.jpg, iot_tlo_or.jpg, iot_tlo_bl.jpg", "Tła fotograficzne bez udokumentowanej licencji; charakter wizualny odtworzony w assets/theme/iot.scss."),
 ("img/kbig.jpg", "Logotyp o nieustalonym statusie praw; slajd tytułowy nie zawiera logotypów."),
 ("logo up.poznan.pl, logo wisim.up.poznan.pl", "Hotlinki do serwerów uczelni — usunięte zgodnie z wymogiem eliminacji łamanych odnośników do logotypów."),
 ("m5stamp-c3-board.png, m5stamp-c3-pinmap.png, m5stamp-c3u-board.png, m5stamp-c3u-pinmap.png",
  "Materiały M5Stack Technology Co., Ltd. — all rights reserved. Nie redystrybuujemy ich w repozytorium przeznaczonym do publikacji; w slajdzie 02#stamp-c3u podano odnośnik do dokumentacji producenta, a tabela wyprowadzeń została zestawiona z faktów."),
]


def main():
    slajdy, bledy = [], []
    for deck, pozycje in MAPA.items():
        for sid, rodzaj, origin, zrodla, tytul, uzas in pozycje:
            wpis = {
                "deck": deck,
                "id": sid,
                "rodzaj": {"title": "tytulowy", "sekcja": "sekcja"}.get(rodzaj, "tresc"),
                "tytul": tytul,
                "origin": origin,
                "uzasadnienie": uzas,
            }
            src = []
            for k in zrodla:
                if k in Z:
                    qmd, tyt, zakres = Z[k]
                    src.append({"typ": "prezentacja", "qmd": qmd, "tytul": tyt,
                                "wiersze": zakres})
                elif k in U:
                    src.append({"typ": "material-kursu", "qmd": U[k]})
                else:
                    bledy.append(f"{deck}#{sid}: nieznany skrót źródła {k}")
            if src:
                wpis["zrodlo"] = src[0]
                if len(src) > 1:
                    wpis["zrodla_dodatkowe"] = src[1:]
            slajdy.append(wpis)

    # weryfikacja wobec wyrenderowanego HTML
    for f in sorted(glob.glob("docs/slides/*.html")):
        deck = os.path.basename(f).replace(".html", "")
        h = open(f, encoding="utf-8").read()
        ids = re.findall(r'<section[^>]*\bid="([^"]*)"', h)
        wpisane = [s["id"] for s in slajdy if s["deck"] == deck]
        for i in ids:
            if i not in wpisane:
                bledy.append(f"{deck}#{i}: brak wpisu w manifeście")
        for i in wpisane:
            if i not in ids:
                bledy.append(f"{deck}#{i}: wpis bez slajdu w HTML")

    stat = collections.Counter(s["origin"] for s in slajdy)
    stat_tresc = collections.Counter(
        s["origin"] for s in slajdy if s["rodzaj"] == "tresc")
    manifest = {
        "opis": "Mapa pochodzenia slajdów kursu IoT w ośmiu wykładach.",
        "zrodlo": {
            "repozytorium": SRC_REPO,
            "commit": SRC_COMMIT,
            "galaz": "main",
            "data_odczytu": DATA_ODCZYTU,
            "licencja": "CC BY 4.0",
            "materialy_kursu": "moodle-lab/course-source/frontend/{lecture-materials,unified-materials}",
        },
        "legenda_origin": {
            "retained": "slajd przeniesiony z zachowaniem tezy i większości treści",
            "adapted": "slajd przeniesiony, lecz przeredagowany: skrót, korekta faktograficzna lub scalenie",
            "new": "slajd napisany od nowa na podstawie materiałów kursu i źródeł pierwotnych",
        },
        "statystyka": {
            "slajdow_lacznie": len(slajdy),
            "wg_origin": dict(stat),
            "slajdy_merytoryczne_wg_origin": dict(stat_tresc),
            "wg_talii": {d: len(v) for d, v in MAPA.items()},
        },
        "slajdy": slajdy,
        "odrzucone_slajdy_zrodlowe": [
            {"skrot": k, "qmd": Z[k][0] if k in Z else None,
             "tytul_zrodlowy": Z[k][1] if k in Z else t, "tytul": t, "powod": p}
            for k, t, p in ODRZUCONE
        ],
        "ilustracje_wykorzystane": [
            {"plik": p, "autor": a, "zrodlo": z, "licencja": l, "slajdy": s}
            for p, a, z, l, s in ILUSTRACJE_WYKORZYSTANE
        ],
        "ilustracje_wykluczone": [
            {"plik": p, "powod": r} for p, r in ILUSTRACJE_ODRZUCONE
        ],
    }
    os.makedirs("provenance", exist_ok=True)
    json.dump(manifest, open("provenance/slide-map.json", "w"),
              ensure_ascii=False, indent=1)

    print(f"Slajdów w manifeście: {len(slajdy)}")
    print(f"  wg origin (wszystkie):      {dict(stat)}")
    print(f"  wg origin (merytoryczne):   {dict(stat_tresc)}")
    print(f"Odrzuconych slajdów źródłowych: {len(ODRZUCONE)}")
    print(f"Wykluczonych pozycji ilustracji: {len(ILUSTRACJE_ODRZUCONE)}")
    if bledy:
        print("\nNIEZGODNOŚCI:")
        for b in bledy:
            print("  -", b)
        sys.exit(1)
    print("\nZapisano: provenance/slide-map.json (zgodny z wyrenderowanym HTML)")


if __name__ == "__main__":
    main()
