#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skrypt generujący 40 pytań testowych w formacie Moodle XML
na podstawie wykładów z cyklu "Internet Rzeczy (IoT)".

Autor: generowane automatycznie na podstawie materiałów wykładowych
       prof. UPP dr hab. inż. Marka Urbaniaka

Uruchomienie:
    python3 generuj_pytania_40.py

Wynik:
    moodle/pytania_iot_40.xml
"""

import os
import html

# ============================================================
# BAZA 40 PYTAŃ – oparta na treści pięciu wykładów .qmd
# ============================================================

questions = [

    # ── WYKŁAD INTRO 1 ─────────────────────────────────────────

    {
        "qtext": "Według Yuvala Noaha Harariego, kto przeprowadza rewolucje w biotechnologii i technologii informacyjnej?",
        "ans_correct": "Inżynierowie, przedsiębiorcy i naukowcy, którzy często nie zdają sobie sprawy z globalnych konsekwencji swoich decyzji.",
        "ans_wrong": [
            "Politycy i rządy państw na podstawie demokratycznych wyborów.",
            "Filozofowie i etycy tworzący kodeksy moralne dla technologii.",
            "Organizacje pozarządowe kontrolujące wdrażanie innowacji."
        ]
    },
    {
        "qtext": "Czym jest system Tree Talker omawiany na wykładzie jako przykład zastosowania IoT w leśnictwie?",
        "ans_correct": "Autonomiczna opaska montowana na pniu drzewa, mierząca przepływ soków, absorpcję światła oraz orientację przestrzenną za pomocą akcelerometrów 3D.",
        "ans_wrong": [
            "Stacja meteorologiczna montowana na wieży obserwacyjnej nad koronami drzew.",
            "Dron skanujący lasy za pomocą kamery termowizyjnej i lidaru.",
            "Aplikacja mobilna do ręcznego notowania pomiarów dendrometrycznych przez leśników."
        ]
    },
    {
        "qtext": "Co oznacza pojęcie 'Przemysł 4.0' (Generacja 4.0) w kontekście ewolucji przetwarzania danych?",
        "ans_correct": "Wykorzystanie narzędzi IoT na brzegu sieci do zbierania danych i napędzania nimi algorytmów uczenia maszynowego (ML/AI).",
        "ans_wrong": [
            "Całkowite zastąpienie pracowników fizycznych przez roboty humanoidalne.",
            "Przejście z napędu parowego na napęd elektryczny w liniach produkcyjnych.",
            "Ręczne planowanie wydajności produkcji w arkuszach kalkulacyjnych."
        ]
    },
    {
        "qtext": "Na czym polega koncepcja jazdy plutonowej (platooning) ciężarówek omawiana w kontekście komunikacji wektorowej IoT?",
        "ans_correct": "Pojazdy sprzężone radiowo jadą w odległości ok. 2 metrów od siebie, drastycznie redukując opór aerodynamiczny (Cx) i zużycie paliwa.",
        "ans_wrong": [
            "Ciężarówki poruszają się autonomicznie po wyznaczonym pasie bez kierowcy.",
            "Pojazdy komunikują się z infrastrukturą drogową w celu omijania korków.",
            "Kolumny ciężarówek są ładowane bezprzewodowo z nadajników umieszczonych w nawierzchni drogi."
        ]
    },
    {
        "qtext": "Jakie zastosowanie IoT w rolnictwie pozwala na minimalizację użycia oprysków chemicznych?",
        "ans_correct": "Algorytmy AI analizujące dane z czujników polowych i sugerujące stosowanie fungicydów dopiero po przekroczeniu fizycznego progu punktu rosy.",
        "ans_wrong": [
            "Drony rozpylające środki ochrony roślin na całej powierzchni pola według stałego harmonogramu.",
            "Systemy nawadniające rozcieńczające opryski w wodzie podlewanej na pole.",
            "Kamery satelitarne wykonujące zdjęcia pól raz w miesiącu."
        ]
    },

    # ── WYKŁAD INTRO 2 ─────────────────────────────────────────

    {
        "qtext": "Na czym polega zagrożenie związane z Chińskim Systemem Kredytu Społecznego omawiane na wykładzie?",
        "ans_correct": "Automatyczna klasyfikacja zachowań obywateli – np. osoba grająca 10 godzin dziennie w gry wideo zostaje uznana za bezproduktywną, co prowadzi do ograniczenia jej praw.",
        "ans_wrong": [
            "System blokuje dostęp do internetu osobom, które nie opłacają rachunków.",
            "Obywatele muszą obowiązkowo nosić opaski fitness monitorujące ich aktywność fizyczną.",
            "System przyznaje kredyty bankowe wyłącznie na podstawie historii zakupów online."
        ]
    },
    {
        "qtext": "Jaki paradoks dotyczący autonomicznych dronów opisano na wykładzie?",
        "ans_correct": "Do obsługi jednego drona potrzeba ok. 30 osób na ziemi i ok. 80 analityków danych – 'autonomia' sprzętu oznacza więcej pracy z danymi, a nie mniej ludzi.",
        "ans_wrong": [
            "Drony zużywają mniej energii niż samoloty, ale są droższe w produkcji.",
            "Drony mogą latać wyłącznie w przestrzeni kontrolowanej przez rząd.",
            "Każdy dron musi posiadać wbudowany system blockchain do weryfikacji lotów."
        ]
    },
    {
        "qtext": "Na jakie zagrożenie zwrócił uwagę Aldous Huxley, cytowany na wykładzie w kontekście 'cyfrowego znieczulenia'?",
        "ans_correct": "Ludzie spędzający czas w świecie rozrywki i fantazji nie potrafią oprzeć się manipulacji ze strony tych, którzy chcą przejąć kontrolę nad społeczeństwem.",
        "ans_wrong": [
            "Technologia doprowadzi do nuklearnej wojny między maszynami a ludźmi.",
            "Sztuczna inteligencja zastąpi ludzki mózg w ciągu najbliższych 10 lat.",
            "Komputery kwantowe złamią wszystkie szyfry i zniszczą prywatność."
        ]
    },
    {
        "qtext": "Co udowodnił eksperyment Rajesh Rao i Andrei Stocco na University of Washington w 2013 r.?",
        "ans_correct": "Możliwość przesyłania impulsu ruchowego między mózgami dwóch osób za pomocą EEG i cewki magnetycznej połączonych przez sieć TCP/IP – nieinwazyjny interfejs mózg-mózg.",
        "ans_wrong": [
            "Możliwość bezprzewodowego ładowania implantów mózgowych przez Wi-Fi.",
            "Zdolność AI do odczytywania ludzkich myśli z dokładnością 99%.",
            "Przesyłanie plików bezpośrednio do pamięci długotrwałej człowieka."
        ]
    },
    {
        "qtext": "Ile energii (w przybliżeniu) potrzebuje samochód na pokonanie 5 km, w porównaniu z dobowym zapotrzebowaniem energetycznym człowieka?",
        "ans_correct": "Pokonanie 5 km autem wymaga ładunku energetycznego większego niż całodobowe zapotrzebowanie organizmu człowieka (ok. 12,6 MJ dziennie).",
        "ans_wrong": [
            "Samochód potrzebuje tysiąckrotnie mniej energii niż człowiek na dobę.",
            "Zużycie energii jest porównywalne – ok. 500 kcal na 5 km jazdy.",
            "Człowiek zużywa więcej energii na 5 km biegu niż samochód na tę samą odległość."
        ]
    },

    # ── WYKŁAD 1 ────────────────────────────────────────────────

    {
        "qtext": "Kto i w którym roku po raz pierwszy użył terminu 'Internet of Things' (Internet Rzeczy)?",
        "ans_correct": "Kevin Ashton w 1999 roku, podczas pracy nad łańcuchami dostaw w firmie Procter & Gamble.",
        "ans_wrong": [
            "John Romkey w 1990 roku, prezentując zdalnie sterowany toster.",
            "Studenci Carnegie Mellon University w 1982 roku.",
            "Tim Berners-Lee w 1991 roku, tworząc World Wide Web."
        ]
    },
    {
        "qtext": "Jakie urządzenie z 1982 roku na Carnegie Mellon University jest uznawane za pierwszy 'inteligentny' przedmiot podłączony do sieci?",
        "ans_correct": "Automat (dystrybutor) z napojami Coca-Cola, z mikroprzełącznikami rejestrującymi dostępność i temperaturę butelek.",
        "ans_wrong": [
            "Zdalnie sterowany toster kuchenny.",
            "Inteligentna lodówka z czujnikiem temperatury.",
            "Terminal tekstowy monitorujący drukarkę w laboratorium."
        ]
    },
    {
        "qtext": "Kiedy, według analiz firmy Cisco, liczba urządzeń podłączonych do sieci po raz pierwszy przekroczyła populację ludzi na Ziemi?",
        "ans_correct": "W latach 2008–2009.",
        "ans_wrong": [
            "W 1999 roku, po sformułowaniu definicji IoT.",
            "W 2016 roku, podczas ataku botnetu Mirai.",
            "Dopiero w 2020 roku, wraz z rozwojem sieci 5G."
        ]
    },
    {
        "qtext": "Z jakich trzech warstw składa się standardowa architektura systemów IoT?",
        "ans_correct": "Z warstwy percepcji (czujniki i aktuatory), warstwy sieciowej (bramy i routing) oraz warstwy aplikacji (interfejsy i analityka).",
        "ans_wrong": [
            "Z warstwy bazy danych, warstwy logicznej i warstwy radiowej.",
            "Z warstwy użytkownika, warstwy serwera i warstwy zabezpieczeń.",
            "Z warstwy fizycznej, warstwy transportowej i warstwy prezentacji (model OSI)."
        ]
    },
    {
        "qtext": "Czym różnią się czujniki pasywne od aktywnych w warstwie percepcji IoT?",
        "ans_correct": "Czujniki pasywne (np. fotorezystor) nie emitują sygnału – jedynie reagują na otoczenie. Aktywne (np. ultradźwiękowe, Lidar) emitują sygnał i mierzą jego odbicie, co zużywa więcej energii.",
        "ans_wrong": [
            "Pasywne są zawsze cyfrowe, a aktywne analogowe.",
            "Pasywne wymagają stałego zasilania sieciowego, a aktywne działają na baterii.",
            "Pasywne przesyłają dane do chmury, a aktywne je jedynie zapisują lokalnie."
        ]
    },
    {
        "qtext": "Czym jest Edge Computing (przetwarzanie brzegowe) i jaką rolę pełni bramka brzegowa (Edge Gateway)?",
        "ans_correct": "Gateway filtruje i przetwarza dane lokalnie, przesyłając do chmury jedynie przesianie agregaty zamiast milionów surowych pakietów – zmniejsza to opóźnienia i obciążenie sieci.",
        "ans_wrong": [
            "Edge Gateway to router służący wyłącznie do szyfrowania danych przed wysyłką do chmury.",
            "To termin oznaczający fizyczną krawędź płytki drukowanej mikrokontrolera.",
            "Edge Computing zastępuje chmurę obliczeniową w całości – dane nigdy nie trafiają do internetu."
        ]
    },
    {
        "qtext": "Co oznacza tryb 'Deep Sleep' (głębokiego uśpienia) w mikrokontrolerach IoT, takich jak ESP32?",
        "ans_correct": "Procesor odcina sobie zasilanie, pozostawiając jedynie minimalny zegar czasu rzeczywistego (RTC) do wybudzenia, co redukuje pobór prądu do mikroamperów.",
        "ans_wrong": [
            "Urządzenie przechodzi w tryb awaryjny i przestaje reagować na jakiekolwiek sygnały.",
            "Procesor zmniejsza częstotliwość taktowania do 1 MHz, ale wszystkie moduły pozostają aktywne.",
            "Deep Sleep oznacza wyłączenie modułu radiowego przy jednoczesnej pracy wszystkich czujników."
        ]
    },
    {
        "qtext": "Dlaczego mikrokontroler ESP32 jest popularniejszy w zastosowaniach IoT niż klasyczne Arduino Uno?",
        "ans_correct": "ESP32 to układ SoC z wbudowanym modułem Wi-Fi i Bluetooth, podczas gdy Arduino Uno nie posiada łączności radiowej na płytce i wymaga dokupienia zewnętrznych modułów (shieldów).",
        "ans_wrong": [
            "ESP32 posiada pełny system operacyjny Linux jak Raspberry Pi.",
            "Arduino Uno jest droższe i trudniejsze w programowaniu.",
            "ESP32 działa wyłącznie z językiem Python, co jest łatwiejsze niż C++ w Arduino."
        ]
    },
    {
        "qtext": "Czym jest Cyfrowy Bliźniak (Digital Twin) w kontekście Internetu Rzeczy?",
        "ans_correct": "Wirtualna kopia fizycznego obiektu (np. silnika, hali produkcyjnej), zasilana danymi z czujników w czasie rzeczywistym, umożliwiająca symulacje 'what-if' bez zatrzymywania rzeczywistego systemu.",
        "ans_wrong": [
            "Kopia zapasowa (backup) danych z czujników przechowywana na drugim serwerze.",
            "Drugi, identyczny fizyczny egzemplarz urządzenia działający jako rezerwa awaryjna.",
            "Wirtualna sieć VPN łącząca dwa identyczne systemy IoT w różnych lokalizacjach."
        ]
    },
    {
        "qtext": "Jaka jest główna rola Raspberry Pi w architekturze systemów IoT?",
        "ans_correct": "Pełni rolę lokalnej bramy (Gateway) koordynującej czujniki – uruchamia Linuxa, serwer MQTT, Edge Computing. Jest jednak zbyt prądożerne, by służyć jako autonomiczny czujnik bateryjny.",
        "ans_wrong": [
            "Służy wyłącznie jako zastępczy czujnik temperatury w zastosowaniach polowych.",
            "Jest podstawowym mikrokontrolerem IoT o najniższym poborze prądu na rynku.",
            "Zastępuje chmurę obliczeniową AWS w dużych wdrożeniach przemysłowych."
        ]
    },

    # ── WYKŁAD 2 ────────────────────────────────────────────────

    {
        "qtext": "Na czym polega tzw. 'Trójkąt Niemożliwy' w komunikacji bezprzewodowej IoT?",
        "ans_correct": "Inżynier musi wybrać tylko dwa z trzech parametrów: zasięg (kilometry), przepustowość (megabajty/s) i czas życia na baterii (lata). Nie można mieć wszystkich trzech jednocześnie.",
        "ans_wrong": [
            "Odnosi się do trzech warstw architektury IoT, które muszą działać równolegle.",
            "To ograniczenie procesora, który może obsłużyć maksymalnie trzy czujniki naraz.",
            "Jest to reguła bezpieczeństwa wymagająca trzech poziomów szyfrowania."
        ]
    },
    {
        "qtext": "Dlaczego Wi-Fi (IEEE 802.11) nie nadaje się do zasilanych bateryjnie czujników IoT?",
        "ans_correct": "Architektura Wi-Fi jest prądożerna – przeszukiwanie nadajników i zestawianie połączenia pochłaniają setki mA, szybko wyczerpując baterię.",
        "ans_wrong": [
            "Wi-Fi nie obsługuje protokołu MQTT niezbędnego do komunikacji IoT.",
            "Wi-Fi działa wyłącznie w paśmie 5 GHz, które nie jest legalne w UE.",
            "Wi-Fi wymaga stałego połączenia kablowego z routerem."
        ]
    },
    {
        "qtext": "Na czym polega rewolucja wprowadzona przez Bluetooth Low Energy (BLE) w wersji 4.0?",
        "ans_correct": "Urządzenie BLE nie utrzymuje ciągłego połączenia – błyskawicznie emituje kilka pakietów danych i natychmiast wraca w tryb uśpienia, co redukuje pobór energii nawet stukrotnie.",
        "ans_wrong": [
            "BLE umożliwia przesyłanie ciągłego strumienia wideo w jakości HD.",
            "BLE zwiększa zasięg transmisji do kilkunastu kilometrów.",
            "BLE zastąpił Wi-Fi jako główny protokół domowych routerów."
        ]
    },
    {
        "qtext": "Jaką architekturę sieciową stosują protokoły Zigbee i Z-Wave i jaki problem rozwiązują?",
        "ans_correct": "Stosują topologię sieci kratowej (Mesh) – urządzenia zasilane z sieci (np. gniazdka) pełnią rolę routerów, przekazując sygnał dalej i rozwiązując problem słabego zasięgu przez grube ściany.",
        "ans_wrong": [
            "Stosują topologię gwiazdy wymagającej centralnego serwera w chmurze.",
            "Działają wyłącznie w paśmie 5 GHz zapewniającym dużą przepustowość.",
            "Wymagają stałego łącza kablowego Ethernet między wszystkimi urządzeniami."
        ]
    },
    {
        "qtext": "Czym jest LPWAN (Low Power Wide Area Network) i do jakich zastosowań służy?",
        "ans_correct": "To sieć o bardzo niskim poborze energii i dużym zasięgu (nawet 15–20 km), ale z drastycznie ograniczoną przepustowością – służy wyłącznie do przesyłania krótkich danych telemetrycznych.",
        "ans_wrong": [
            "To szybka sieć lokalna do strumieniowania wideo z kamer w budynkach.",
            "To sieć Mesh łącząca inteligentne żarówki w jednym pomieszczeniu.",
            "To protokół warstwy aplikacji alternatywny wobec MQTT i CoAP."
        ]
    },
    {
        "qtext": "Czym różni się LoRaWAN od NB-IoT jako technologie dalekiego zasięgu?",
        "ans_correct": "LoRaWAN pozwala budować własne bramki w darmowym paśmie 868 MHz (bez opłat abonamentowych), a NB-IoT korzysta ze stacji bazowych operatorów komórkowych i wymaga karty SIM z abonamentem.",
        "ans_wrong": [
            "LoRaWAN przesyła strumienie wideo, a NB-IoT jedynie tekst.",
            "NB-IoT działa w darmowym paśmie radiowym, a LoRaWAN wymaga licencji.",
            "LoRaWAN działa wyłącznie w budynkach, a NB-IoT tylko w terenie otwartym."
        ]
    },
    {
        "qtext": "Jakie specyficzne ograniczenia ma technologia Sigfox?",
        "ans_correct": "Maksymalnie 140 wiadomości dziennie na urządzenie, z ładunkiem zaledwie 12 bajtów na wiadomość – jest to architektura silnie asymetryczna.",
        "ans_wrong": [
            "Sigfox wymaga budowy własnych stacji bazowych i nie oferuje pokrycia globalnego.",
            "Sigfox przesyła do 1 GB danych dziennie, ale wymaga stałego zasilania sieciowego.",
            "Sigfox obsługuje wyłącznie komunikację między serwerami, a nie czujnikami."
        ]
    },
    {
        "qtext": "Dlaczego protokół HTTP nie jest odpowiedni dla urządzeń IoT o ograniczonych zasobach?",
        "ans_correct": "Nagłówki HTTP zajmują więcej bajtów niż przesyłane dane pomiarowe, a synchroniczny model Request-Response zmusza czujnik do utrzymywania włączonego, prądożernego radia w oczekiwaniu na odpowiedź.",
        "ans_wrong": [
            "HTTP nie obsługuje szyfrowania TLS wymaganego przez certyfikaty IoT.",
            "HTTP działa wyłącznie na komputerach stacjonarnych z systemem Windows.",
            "HTTP wymaga stałego łącza kablowego i nie obsługuje transmisji bezprzewodowej."
        ]
    },
    {
        "qtext": "Na jakim modelu architektonicznym opiera się protokół MQTT?",
        "ans_correct": "Na modelu Publikacja/Subskrypcja (Pub/Sub) – czujnik wysyła wiadomość do centralnego Brokera pod określonym tematem (Topic), a Broker dystrybuuje ją do zainteresowanych subskrybentów.",
        "ans_wrong": [
            "Na modelu Żądanie-Odpowiedź (Request-Response) jak w HTTP.",
            "Na bezpośrednim połączeniu peer-to-peer między czujnikiem a serwerem.",
            "Na modelu kolejki FIFO, gdzie wiadomości są odbierane w ściśle ustalonej kolejności."
        ]
    },
    {
        "qtext": "Ile bajtów zajmuje nagłówek wiadomości MQTT i dlaczego jest to istotne?",
        "ans_correct": "Zaledwie 2 bajty – dzięki temu czas pracy modułu radiowego jest minimalny, co redukuje zużycie energii w urządzeniach bateryjnych.",
        "ans_wrong": [
            "Około 500 bajtów – tyle samo co nagłówek HTTP.",
            "Dokładnie 128 bajtów – jest to stała wartość wynikająca ze specyfikacji TCP.",
            "MQTT nie posiada nagłówków – przesyłane są wyłącznie surowe dane binarne."
        ]
    },
    {
        "qtext": "Co oznaczają poziomy QoS (Quality of Service) 0, 1 i 2 w protokole MQTT?",
        "ans_correct": "QoS 0 – 'wyślij i zapomnij' (najszybszy). QoS 1 – wymaga potwierdzenia (możliwe duplikaty). QoS 2 – pełny handshake z gwarancją jednokrotnego dostarczenia.",
        "ans_wrong": [
            "QoS 0 – szyfrowanie wyłączone. QoS 1 – szyfrowanie TLS. QoS 2 – szyfrowanie AES-256.",
            "QoS odnosi się do priorytetów tematów (Topics) w brokerze MQTT.",
            "QoS 0, 1 i 2 określają liczbę subskrybentów mogących jednocześnie odbierać wiadomość."
        ]
    },
    {
        "qtext": "Co oznacza mechanizm LWT (Last Will and Testament) w protokole MQTT?",
        "ans_correct": "Automatyczne powiadomienie wysyłane przez Brokera do subskrybentów w momencie nagłej, nieoczekiwanej utraty połączenia z urządzeniem – informuje o awarii czujnika.",
        "ans_wrong": [
            "Ostatnia wiadomość wysyłana przez czujnik przed jego planowanym wyłączeniem.",
            "Mechanizm tworzenia kopii zapasowej wszystkich wiadomości w kolejce Brokera.",
            "Protokół autoryzacji urządzenia przy pierwszym połączeniu z siecią MQTT."
        ]
    },
    {
        "qtext": "Czym jest CoAP (Constrained Application Protocol) i czym różni się od MQTT?",
        "ans_correct": "CoAP to lekki protokół oparty na bezpołączeniowym UDP z modelem Żądanie-Odpowiedź (jak HTTP), idealny do prostych interakcji na mikrokontrolerach – w odróżnieniu od asynchronicznego modelu Pub/Sub w MQTT.",
        "ans_wrong": [
            "CoAP obsługuje wyłącznie szyfrowanie symetryczne, a MQTT asymetryczne.",
            "CoAP działa tylko w sieciach kablowych, a MQTT wyłącznie bezprzewodowo.",
            "CoAP jest cięższy od HTTP i stosowany tylko na serwerach korporacyjnych."
        ]
    },
    {
        "qtext": "Czym różni się NB-IoT od LTE-M pod kątem mobilności urządzeń?",
        "ans_correct": "NB-IoT jest przeznaczony dla urządzeń stacjonarnych (brak handoveru) z doskonałą penetracją piwnic, a LTE-M obsługuje mobilność (handover między stacjami bazowymi) – np. do śledzenia pojazdów.",
        "ans_wrong": [
            "NB-IoT przesyła strumienie wideo, a LTE-M jedynie dane tekstowe.",
            "LTE-M działa wyłącznie w terenie otwartym, a NB-IoT tylko w budynkach.",
            "Oba standardy wymagają budowy własnych stacji bazowych i nie korzystają z sieci operatorów."
        ]
    },

    # ── WYKŁAD 3 ────────────────────────────────────────────────

    {
        "qtext": "Dlaczego Chmura Obliczeniowa (Cloud Computing) jest niezbędna jako warstwa aplikacji w architekturze IoT?",
        "ans_correct": "Pozwala składować, filtrować i analizować dane z tysięcy czujników generujących Big Data – pojedynczy czujnik jest bezwartościowy, ale 10 000 czujników z logami co minutę tworzy użyteczne wzorce.",
        "ans_wrong": [
            "Chmura jest jedynym miejscem, w którym można uruchomić protokół MQTT.",
            "Dane IoT są zbyt małe, by zapisywać je lokalnie na dyskach.",
            "Bez chmury czujniki nie mogą się ze sobą komunikować."
        ]
    },
    {
        "qtext": "Co oznacza zjawisko 'Vendor Lock-in' (Złota Klatka) i jaki podano przykład na wykładzie?",
        "ans_correct": "Uzależnienie od jednego dostawcy chmury – np. w 2023 r. Google wyłączyło usługę Cloud IoT Core, zmuszając tysiące firm do kosztownej migracji do konkurencji.",
        "ans_wrong": [
            "Fizyczne zablokowanie urządzenia IoT przez producenta po upływie gwarancji.",
            "Konieczność stosowania wyłącznie jednego typu czujników danego producenta.",
            "Odcięcie urządzenia od internetu po nieopłaceniu abonamentu SIM."
        ]
    },
    {
        "qtext": "Czym jest Node-RED i jaką pełni rolę w ekosystemie IoT?",
        "ans_correct": "To narzędzie open-source do wizualnego, graficznego programowania logiki (Low-code), pozwalające budować przepływy danych IoT bez pisania dużej ilości kodu.",
        "ans_wrong": [
            "To system operacyjny instalowany na mikrokontrolerach ESP32.",
            "To komercyjna platforma chmurowa Amazona do zarządzania bramkami IoT.",
            "To język programowania stworzony specjalnie do obsługi protokołu MQTT."
        ]
    },
    {
        "qtext": "Co oznacza skrót OTA (Over The Air) w kontekście zarządzania urządzeniami IoT?",
        "ans_correct": "Zdalna aktualizacja oprogramowania wewnętrznego (firmware) urządzenia drogą bezprzewodową, bez fizycznego podłączania kablem – np. auto aktualizujące się po wjeździe do garażu z Wi-Fi.",
        "ans_wrong": [
            "Protokół radiowy do przesyłania danych telemetrycznych na duże odległości.",
            "Standard szyfrowania komunikacji między czujnikiem a brokerem MQTT.",
            "Metoda bezprzewodowego ładowania baterii urządzeń IoT."
        ]
    },
    {
        "qtext": "Jakie oszczędności przyniosło inteligentne oświetlenie miejskie w Barcelonie, opisanej jako studium przypadku Smart City?",
        "ans_correct": "Oszczędność 30% budżetu energetycznego rocznie dzięki 10 000 lamp analizujących ruch pieszych i inteligentnie gasnących na peryferiach.",
        "ans_wrong": [
            "Oszczędność 90% energii dzięki całkowitemu wyłączeniu oświetlenia nocą.",
            "Brak oszczędności – system generował równie wysokie koszty konserwacji.",
            "Oszczędność wynikała wyłącznie z wymiany lamp na LED, bez systemu IoT."
        ]
    },
    {
        "qtext": "Co to jest botnet Mirai (2016) i dlaczego stanowi przestrogę dla branży IoT?",
        "ans_correct": "Złośliwe oprogramowanie, które przejęło kontrolę nad niezabezpieczonymi kamerami IP (z domyślnym hasłem 'admin/admin'), przeprowadzając gigantyczny atak DDoS na infrastrukturę DNS (m.in. Twitter, Netflix).",
        "ans_wrong": [
            "Wirus komputerowy atakujący wyłącznie serwery banków poprzez protokół MQTT.",
            "Program szpiegujący stworzony przez rząd do monitorowania obywateli.",
            "Atak polegający na fizycznym niszczeniu mikrokontrolerów IoT poprzez przeciążenie zasilania."
        ]
    },
    {
        "qtext": "Na czym polega zasada segmentacji sieci (VLAN) jako praktyka bezpieczeństwa IoT?",
        "ans_correct": "Izolowanie czujników IoT w osobnej sieci wirtualnej (VLAN), oddzielonej zaporą (firewall) od głównej sieci biurowej i serwerów – aby włamanie do czujnika nie dało dostępu do wrażliwych danych.",
        "ans_wrong": [
            "Podział danych na mniejsze pakiety przesyłane różnymi trasami radiowymi.",
            "Tworzenie kopii danych z czujników na wielu serwerach jednocześnie.",
            "Stosowanie osobnych haseł dla każdego czujnika w sieci."
        ]
    },
    {
        "qtext": "Jakie zagrożenie prywatności wiąże się z inteligentnymi licznikami energii opisanym na wykładzie?",
        "ans_correct": "Pomiar zużycia co 10 sekund pozwala na analizę pików i określenie, kiedy mieszkaniec włącza czajnik, wychodzi z domu i wraca – te dane są dostępne dostawcy energii.",
        "ans_wrong": [
            "Liczniki mogą zostać zhakowane, by wyłączyć prąd w całym budynku.",
            "Liczniki emitują promieniowanie elektromagnetyczne szkodliwe dla zdrowia.",
            "Inteligentne liczniki są zbyt drogie, by wdrożyć je na dużą skalę."
        ]
    },
    {
        "qtext": "Co oznacza termin 'Predictive Maintenance' (konserwacja predykcyjna) w kontekście IIoT?",
        "ans_correct": "Przewidywanie awarii maszyn na podstawie analizy danych z czujników wibracji i temperatur, zanim do uszkodzenia fizycznie dojdzie – np. wykrycie zatartych łożysk przed pęknięciem.",
        "ans_wrong": [
            "Regularne przeglądy techniczne wykonywane co miesiąc według stałego harmonogramu.",
            "Automatyczna naprawa urządzenia przez robota bez udziału człowieka.",
            "System wyłączający maszynę po wystąpieniu awarii i powiadamiający serwisanta."
        ]
    },

]

# ============================================================
# GENERACJA XML W FORMACIE MOODLE
# ============================================================

def escape_xml(text: str) -> str:
    """Zabezpiecza znaki specjalne w tekście XML."""
    return html.escape(text, quote=True)

def build_moodle_xml(questions_list: list) -> str:
    """Generuje poprawny plik Moodle XML z listą pytań wielokrotnego wyboru."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<quiz>')
    lines.append('')

    # Kategoria
    lines.append('  <question type="category">')
    lines.append('    <category>')
    lines.append('      <text>$course$/IoT - Internet Rzeczy</text>')
    lines.append('    </category>')
    lines.append('  </question>')
    lines.append('')

    for i, q in enumerate(questions_list, start=1):
        lines.append(f'  <question type="multichoice">')
        lines.append(f'    <name>')
        lines.append(f'      <text>Pytanie {i:02d}</text>')
        lines.append(f'    </name>')
        lines.append(f'    <questiontext format="html">')
        lines.append(f'      <text><![CDATA[<p>{q["qtext"]}</p>]]></text>')
        lines.append(f'    </questiontext>')
        lines.append(f'    <defaultgrade>1</defaultgrade>')
        lines.append(f'    <penalty>0.3333333</penalty>')
        lines.append(f'    <single>true</single>')
        lines.append(f'    <shuffleanswers>true</shuffleanswers>')
        lines.append(f'    <answernumbering>abc</answernumbering>')

        # Odpowiedź poprawna
        lines.append(f'    <answer fraction="100" format="html">')
        lines.append(f'      <text><![CDATA[<p>{q["ans_correct"]}</p>]]></text>')
        lines.append(f'      <feedback format="html">')
        lines.append(f'        <text><![CDATA[<p>Odpowiedź poprawna.</p>]]></text>')
        lines.append(f'      </feedback>')
        lines.append(f'    </answer>')

        # Odpowiedzi błędne
        for wrong in q["ans_wrong"]:
            lines.append(f'    <answer fraction="0" format="html">')
            lines.append(f'      <text><![CDATA[<p>{wrong}</p>]]></text>')
            lines.append(f'      <feedback format="html">')
            lines.append(f'        <text><![CDATA[<p>Odpowiedź niepoprawna.</p>]]></text>')
            lines.append(f'      </feedback>')
            lines.append(f'    </answer>')

        lines.append(f'  </question>')
        lines.append('')

    lines.append('</quiz>')
    return '\n'.join(lines)

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "moodle")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "pytania_iot_40.xml")

    xml_content = build_moodle_xml(questions)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_content)

    print(f"✅ Wygenerowano {len(questions)} pytań w formacie Moodle XML.")
    print(f"📄 Plik zapisano: {output_path}")
