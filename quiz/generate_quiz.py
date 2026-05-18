#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IoT Quiz Generator - Generates 40 Moodle XML quiz questions
Based on lecture materials from wyklad_1.qmd, wyklad_2.qmd, wyklad_3.qmd,
wyklad_intro_1.qmd, wyklad_intro_2.qmd
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom

def create_question(category, qtype, name, question_text, answers, correct_indices=None, feedback=None):
    """
    Create a single question element for Moodle XML format.
    
    Args:
        category: Question category
        qtype: 'multiplechoice', 'truefalse', 'matching', 'numerical'
        name: Question name/identifier
        question_text: The actual question text (can include HTML)
        answers: List of tuples (answer_text, is_correct, feedback)
        correct_indices: For multiple choice, indices of correct answers
        feedback: General feedback for the question
    """
    question = ET.Element('question', type=qtype)
    
    # Category
    cat_elem = ET.SubElement(question, 'category')
    cat_text = ET.SubElement(cat_elem, 'text')
    cat_text.text = category
    
    # Name
    name_elem = ET.SubElement(question, 'name')
    name_text = ET.SubElement(name_elem, 'text')
    name_text.text = name
    
    # Question text
    questiontext = ET.SubElement(question, 'questiontext', format='html')
    qtext_elem = ET.SubElement(questiontext, 'text')
    qtext_elem.text = question_text
    
    # General feedback
    if feedback:
        generalfeedback = ET.SubElement(question, 'generalfeedback', format='html')
        gfb_elem = ET.SubElement(generalfeedback, 'text')
        gfb_elem.text = feedback
    
    # Default grade
    defaultgrade = ET.SubElement(question, 'defaultgrade')
    defaultgrade.text = '1'
    
    # Penalty
    penalty = ET.SubElement(question, 'penalty')
    penalty.text = '0.3333333'
    
    # Hidden
    hidden = ET.SubElement(question, 'hidden')
    # Single (for multiple choice - whether only one answer is correct)
    if qtype == 'multiplechoice':
        single = ET.SubElement(question, 'single')
        if correct_indices is not None:
            single.text = 'true' if len(correct_indices) == 1 else 'false'
        else:
            single.text = 'true'  # Default to single correct answer
    for i, (ans_text, is_correct, ans_feedback) in enumerate(answers):
        answer = ET.SubElement(question, 'answer', fraction=str(100 if is_correct else 0))
        answertext = ET.SubElement(answer, 'text')
        answertext.text = ans_text
        
        if ans_feedback:
            answerfeedback = ET.SubElement(answer, 'feedback', format='html')
            afb_elem = ET.SubElement(answerfeedback, 'text')
            afb_elem.text = ans_feedback
    
    return question


def generate_all_questions():
    """Generate all 40 quiz questions."""
    questions = []
    
    # ==================== WYKŁAD 1: Od koncepcji do Przemysłu 4.0 ====================
    
    # Q1 - Historia IoT - automat z Coca-Colą
    questions.append(create_question(
        category='Wykład 1 - Podstawy IoT',
        qtype='multiplechoice',
        name='Q1_Historia_IoT_CocaCola',
        question_text='<p>W którym roku i na jakiej uczelni powstał pierwszy prototyp urządzenia IoT - automat z napojami połączony z siecią?</p>',
        answers=[
            ('1982, Carnegie Mellon University (CMU)', True, 'Poprawnie! Studenci CMU w 1982 roku podłączyli automat z Coca-Colą do sieci wydziałowej.'),
            ('1999, MIT', False, 'Niepoprawnie. 1999 to rok coined terminu "Internet of Things" przez Kevina Ashtona.'),
            ('1969, Stanford', False, 'Niepoprawnie. 1969 to rok uruchomienia ARPANET.'),
            ('1990, Berkeley', False, 'Niepoprawnie.')
        ],
        feedback='<p>Pierwszy prototyp IoT powstał w 1982 roku na Carnegie Mellon University. Studenci zmęczeni schodzeniem po schodach do automatu podłączyli go do sieci, aby zdalnie sprawdzać dostępność napojów.</p>'
    ))
    
    # Q2 - Kevin Ashton
    questions.append(create_question(
        category='Wykład 1 - Podstawy IoT',
        qtype='multiplechoice',
        name='Q2_Kevin_Ashton_Termin',
        question_text='<p>Kto i w którym roku ukuł termin "Internet of Things" (IoT)?</p>',
        answers=[
            ('Kevin Ashton, 1999', True, 'Poprawnie! Kevin Ashton z Procter & Gamble użył tego terminu w prezentacji w 1999 roku.'),
            ('Tim Berners-Lee, 1989', False, 'Niepoprawnie. Tim Berners-Lee wynalazł World Wide Web.'),
            ('Vint Cerf, 2000', False, 'Niepoprawnie.'),
            ('Elon Musk, 2010', False, 'Niepoprawnie.')
        ],
        feedback='<p>Kevin Ashton, pracując w Procter & Gamble, analizował problem pustych półek ze szminkami Olay i zidentyfikował technologię RFID jako klucz do autonomicznego śledzenia towarów.</p>'
    ))
    
    # Q3 - Moment zwrotny IoT
    questions.append(create_question(
        category='Wykład 1 - Podstawy IoT',
        qtype='multiplechoice',
        name='Q3_Moment_Zwrotny_Skala',
        question_text='<p>W którym roku liczba aktywnych, połączonych urządzeń po raz pierwszy przewyższyła całkowitą populację ludzi na Ziemi?</p>',
        answers=[
            ('2008/2009', True, 'Poprawnie! Według analiz Cisco był to historyczny Rubikon.'),
            ('2000', False, 'Niepoprawnie. To za wcześnie.'),
            ('2015', False, 'Niepoprawnie. To już po przekroczeniu.'),
            ('1999', False, 'Niepoprawnie.')
        ],
        feedback='<p>Rok 2008/2009 to moment, gdy urządzenia IoT zaczęły generować więcej danych niż ludzie. To początek ery pasywnego generowania danych telemetrycznych.</p>'
    ))
    
    # Q4 - Architektura 3-warstwowa
    questions.append(create_question(
        category='Wykład 1 - Architektura IoT',
        qtype='multiplechoice',
        name='Q4_Architektura_Warstwy',
        question_text='<p>Jakie są trzy główne warstwy architektury systemów IoT według modelu IEEE?</p>',
        answers=[
            ('Percepcja, Sieć, Aplikacja', True, 'Poprawnie! To podstawowy model 3-warstwowy.'),
            ('Hardware, Software, Cloud', False, 'Niepoprawnie.'),
            ('Czujniki, Procesory, Ekrany', False, 'Niepoprawnie.'),
            ('Input, Processing, Output', False, 'Niepoprawnie. To model komputera, nie IoT.')
        ],
        feedback='<p>Model 3-warstwowy: Percepcja (czujniki/aktuatory), Sieć (bramy, routing), Aplikacja (dashboardy, analityka).</p>'
    ))
    
    # Q5 - Warstwa percepcji
    questions.append(create_question(
        category='Wykład 1 - Architektura IoT',
        qtype='multiplechoice',
        name='Q5_Warstwa_Percepcji',
        question_text='<p>Co należy do warstwy percepcji w systemie IoT?</p>',
        answers=[
            ('Czujniki i aktuatory', True, 'Poprawnie! To "zmysły" i "ręce" systemu IoT.'),
            ('Serwery chmurowe', False, 'Niepoprawnie. To warstwa aplikacji.'),
            ('Protokoły MQTT, HTTP', False, 'Niepoprawnie. To warstwa sieci/aplikacji.'),
            ('Bazy danych', False, 'Niepoprawnie.')
        ],
        feedback='<p>Warstwa percepcji odpowiada za zbieranie danych z otoczenia (czujniki) i wpływ na fizyczny świat (aktuatory).</p>'
    ))
    
    # Q6 - Edge Computing
    questions.append(create_question(
        category='Wykład 1 - Architektura IoT',
        qtype='multiplechoice',
        name='Q6_Edge_Computing_Definicja',
        question_text='<p>Czym jest Edge Computing w kontekście IoT?</p>',
        answers=[
            ('Przetwarzanie danych blisko źródła ich powstawania, na brzegu sieci', True, 'Poprawnie! Redukuje to opóźnienia i obciążenie chmury.'),
            ('Przesyłanie wszystkich danych bezpośrednio do chmury', False, 'Niepoprawnie. To przeciwieństwo Edge Computing.'),
            ('Zapisywanie danych na dyskach lokalnych', False, 'Niepoprawnie.'),
            ('Używanie tylko sieci kablowych', False, 'Niepoprawnie.')
        ],
        feedback='<p>Edge Computing pozwala na filtrowanie i agregację danych na bramie (Gateway), zanim trafią do chmury. Krytyczne dla systemów czasu rzeczywistego.</p>'
    ))
    
    # Q7 - ESP32 vs Arduino
    questions.append(create_question(
        category='Wykład 1 - Platformy Sprzętowe',
        qtype='multiplechoice',
        name='Q7_ESP32_Arduino_Porownanie',
        question_text='<p>Która platforma sprzętowa ma wbudowane Wi-Fi i Bluetooth oraz bardzo niski pobór prądu w trybie uśpienia?</p>',
        answers=[
            ('ESP32', True, 'Poprawnie! ESP32 to król taniego, profesjonalnego IoT.'),
            ('Arduino Uno', False, 'Niepoprawnie. Arduino wymaga dodatkowych shieldów do łączności radiowej.'),
            ('Raspberry Pi 5', False, 'Niepoprawnie. Raspberry Pi to komputer, zbyt prądożerny dla czujników bateryjnych.'),
            ('Intel NUC', False, 'Niepoprawnie.')
        ],
        feedback='<p>ESP32 to System on Chip (SoC) z wbudowanym Wi-Fi/Bluetooth, pobierający mikroampery w trybie deep sleep. Idealny dla autonomicznych czujników terenowych.</p>'
    ))
    
    # Q8 - Deep Sleep
    questions.append(create_question(
        category='Wykład 1 - Platformy Sprzętowe',
        qtype='multiplechoice',
        name='Q8_Deep_Sleep_Zasada',
        question_text='<p>Na czym polega mechanizm "Deep Sleep" w mikrokontrolerach IoT?</p>',
        answers=[
            ('Procesor wyłącza większość systemów, budzi się tylko na chwilę by wykonać zadanie i zasypia ponownie', True, 'Poprawnie! To klucz do wieloletniej pracy na baterii.'),
            ('Procesor działa z pełną wydajnością 24/7', False, 'Niepoprawnie. To szybko wyczerpie baterię.'),
            ('Bateria jest ładowana energią słoneczną', False, 'Niepoprawnie. To osobna technologia.'),
            ('Urządzenie jest podłączone do sieci elektrycznej', False, 'Niepoprawnie.')
        ],
        feedback='<p>Deep Sleep pozwala mikrokontrolerom pracować lata na jednej baterii. Procesor budzi się na ułamek sekundy, wysyła dane i wraca do snu.</p>'
    ))
    
    # Q9 - Digital Twins
    questions.append(create_question(
        category='Wykład 1 - Digital Twins',
        qtype='multiplechoice',
        name='Q9_Digital_Twins_Definicja',
        question_text='<p>Czym jest Cyfrowy Bliźniak (Digital Twin) w IoT?</p>',
        answers=[
            ('Wirtualna kopia fizycznego obiektu/systemu zasilana danymi z czujników w czasie rzeczywistym', True, 'Poprawnie!'),
            ('Kopia zapasowa danych w chmurze', False, 'Niepoprawnie.'),
            ('Drugi identyczny czujnik dla redundancji', False, 'Niepoprawnie.'),
            ('Symulator bez połączenia z rzeczywistymi danymi', False, 'Niepoprawnie.')
        ],
        feedback='<p>Cyfrowy Bliźniak to nie tylko wizualizacja 3D - to żywy model zasilany strumieniem danych z czujników, pozwalający na symulacje "What If".</p>'
    ))
    
    # Q10 - Raspberry Pi zastosowanie
    questions.append(create_question(
        category='Wykład 1 - Platformy Sprzętowe',
        qtype='multiplechoice',
        name='Q10_Raspberry_Pi_Zastosowanie',
        question_text='<p>Do czego najlepiej nadaje się Raspberry Pi w architekturze IoT?</p>',
        answers=[
            ('Lokalna brama (Gateway) koordynująca, serwer MQTT, Edge Computing', True, 'Poprawnie! Raspberry Pi to pełny komputer z Linuxem.'),
            ('Autonomiczny czujnik terenowy na baterii', False, 'Niepoprawnie. Zbyt prądożerny.'),
            ('Prosty prototyp edukacyjny bez łączności', False, 'Niepoprawnie. Do tego lepsze Arduino.'),
            ('Zasilanie innych urządzeń', False, 'Niepoprawnie.')
        ],
        feedback='<p>Raspberry Pi to Single Board Computer (SBC) z Linuxem. Idealny jako lokalny serwer, brama lub hub, ale wymaga stałego zasilania.</p>'
    ))
    
    # ==================== WYKŁAD 2: Język Rzeczy - Protokoły ====================
    
    # Q11 - Trójkąt niemożliwy IoT
    questions.append(create_question(
        category='Wykład 2 - Protokoły Komunikacyjne',
        qtype='multiplechoice',
        name='Q11_Trojkat_Niemozliwy',
        question_text='<p>W "Trójkącie Niemożliwym IoT" inżynier może wybrać tylko DWA z trzech parametrów. Które to parametry?</p>',
        answers=[
            ('Zasięg, Przepustowość, Czas życia na baterii', True, 'Poprawnie! Nie da się mieć wszystkich trzech jednocześnie.'),
            ('Koszt, Rozmiar, Kolor', False, 'Niepoprawnie.'),
            ('Szybkość, Bezpieczeństwo, Cena', False, 'Niepoprawnie.'),
            ('Zasięg, Bezpieczeństwo, Cena', False, 'Niepoprawnie.')
        ],
        feedback='<p>Fizyka fal elektromagnetycznych wymusza kompromis: daleki zasięg + długa bateria = niska przepustowość (LPWAN).</p>'
    ))
    
    # Q12 - Wi-Fi w IoT
    questions.append(create_question(
        category='Wykład 2 - Protokoły Komunikacyjne',
        qtype='multiplechoice',
        name='Q12_WiFi_Wady_IoT',
        question_text='<p>Dlaczego Wi-Fi jest nieodpowiednie dla czujników IoT zasilanych bateryjnie?</p>',
        answers=[
            ('Jest prądożerne - złożony handshake i beaconing zużywają setki mA', True, 'Poprawnie!'),
            ('Ma zbyt mały zasięg', False, 'Niepoprawnie. Zasięg jest wystarczający.'),
            ('Nie obsługuje szyfrowania', False, 'Niepoprawnie. WPA2/WPA3 dostępne.'),
            ('Jest zbyt wolne', False, 'Niepoprawnie. Wi-Fi jest bardzo szybkie.')
        ],
        feedback='<p>Wi-Fi wymaga ciągłego nasłuchiwania beaconów i złożonego procesu łączenia. Nadaje się tylko dla urządzeń ze stałym zasilaniem.</p>'
    ))
    
    # Q13 - BLE
    questions.append(create_question(
        category='Wykład 2 - Protokoły Komunikacyjne',
        qtype='multiplechoice',
        name='Q13_BLE_Roznica',
        question_text='<p>Czym Bluetooth Low Energy (BLE) różni się od klasycznego Bluetooth?</p>',
        answers=[
            ('BLE "usypia" radio natychmiast po wysłaniu pakietu, klasyczny BT utrzymuje ciągłe połączenie', True, 'Poprawnie!'),
            ('BLE ma większy zasięg', False, 'Niepoprawnie.'),
            ('BLE przesyła dane szybciej', False, 'Niepoprawnie.'),
            ('Nie ma różnicy', False, 'Niepoprawnie.')
        ],
        feedback='<p>BLE został zaprojektowany dla urządzeń ubieralnych i beaconów. Bateria CR2032 wystarcza na lata pracy.</p>'
    ))
    
    # Q14 - Zigbee Mesh
    questions.append(create_question(
        category='Wykład 2 - Protokoły Komunikacyjne',
        qtype='multiplechoice',
        name='Q14_Zigbee_Mesh',
        question_text='<p>Jaką zaletę ma sieć mesh (kratowa) w protokole Zigbee?</p>',
        answers=[
            ('Urządzenia zasilane z sieci działają jako wzmacniacze, przekazując sygnał dalej', True, 'Poprawnie!'),
            ('Zużywa mniej energii niż inne protokoły', False, 'Niepoprawnie.'),
            ('Ma większą przepustowość', False, 'Niepoprawnie.'),
            ('Działa bez bramki', False, 'Niepoprawnie.')
        ],
        feedback='<p>Sieć mesh jest "samolecząca" - awaria jednego węzła powoduje automatyczne znalezienie nowej trasy. Idealne dla Smart Home.</p>'
    ))
    
    # Q15 - LPWAN definicja
    questions.append(create_question(
        category='Wykład 2 - Protokoły Komunikacyjne',
        qtype='multiplechoice',
        name='Q15_LPWAN_Definicja',
        question_text='<p>Co oznacza skrót LPWAN?</p>',
        answers=[
            ('Low Power Wide Area Network', True, 'Poprawnie!'),
            ('Long Packet Wireless Access Network', False, 'Niepoprawnie.'),
            ('Local Personal Wireless Area Network', False, 'Niepoprawnie.'),
            ('Low Price Wide Access Node', False, 'Niepoprawnie.')
        ],
        feedback='<p>LPWAN to technologie dla telemetrii na kilometry: LoRaWAN, NB-IoT, Sigfox. Żywotność baterii 5-10 lat, zasięg 15-20 km.</p>'
    ))
    
    # Q16 - LoRaWAN vs NB-IoT
    questions.append(create_question(
        category='Wykład 2 - Protokoły Komunikacyjne',
        qtype='multiplechoice',
        name='Q16_LoRaWAN_NBIoT_Roznica',
        question_text='<p>Jaka jest główna różnica między LoRaWAN a NB-IoT?</p>',
        answers=[
            ('LoRaWAN pozwala na budowę własnych bramek w darmowym paśmie, NB-IoT wymaga karty SIM operatora', True, 'Poprawnie!'),
            ('LoRaWAN jest droższy', False, 'Niepoprawnie.'),
            ('NB-IoT ma mniejszy zasięg', False, 'Niepoprawnie.'),
            ('Nie ma różnicy', False, 'Niepoprawnie.')
        ],
        feedback='<p>LoRaWAN: własna infrastruktura, pasmo 868 MHz (darmowe). NB-IoT: infrastruktura operatora, lepsza penetracja budynków, abonament.</p>'
    ))
    
    # Q17 - Sigfox ograniczenia
    questions.append(create_question(
        category='Wykład 2 - Protokoły Komunikacyjne',
        qtype='multiplechoice',
        name='Q17_Sigfox_Ograniczenia',
        question_text='<p>Ile maksymalnie wiadomości dziennie może wysłać urządzenie w sieci Sigfox?</p>',
        answers=[
            ('140 wiadomości', True, 'Poprawnie! To bardzo mało, ale wystarcza do prostych zastosowań.'),
            ('1000 wiadomości', False, 'Niepoprawnie.'),
            ('10000 wiadomości', False, 'Niepoprawnie.'),
            ('Bez ograniczeń', False, 'Niepoprawnie.')
        ],
        feedback='<p>Sigfox: max 140 wiadomości dziennie, payload 12 bajtów. Idealny do potwierdzeń "jestem sprawny" raz na godzinę.</p>'
    ))
    
    # Q18 - HTTP w IoT
    questions.append(create_question(
        category='Wykład 2 - Protokoły Aplikacyjne',
        qtype='multiplechoice',
        name='Q18_HTTP_Niepasuje_IoT',
        question_text='<p>Dlaczego protokół HTTP nie jest odpowiedni dla urządzeń IoT?</p>',
        answers=[
            ('Nagłówki HTTP mogą zajmować więcej bajtów niż same dane pomiarowe', True, 'Poprawnie!'),
            ('HTTP jest zbyt wolny', False, 'Niepoprawnie.'),
            ('HTTP nie obsługuje szyfrowania', False, 'Niepoprawnie. HTTPS dostępne.'),
            ('HTTP nie działa przez Internet', False, 'Niepoprawnie.')
        ],
        feedback='<p>HTTP ma duży narzut nagłówków i model request-response, który wymaga trzymania włączonego radia. Nieefektywne dla mikrokontrolerów.</p>'
    ))
    
    # Q19 - MQTT architektura
    questions.append(create_question(
        category='Wykład 2 - Protokoły Aplikacyjne',
        qtype='multiplechoice',
        name='Q19_MQTT_Architektura',
        question_text='<p>Jaką architekturę komunikacji stosuje protokół MQTT?</p>',
        answers=[
            ('Publikacja/Subskrypcja (Pub/Sub) z Brokerem', True, 'Poprawnie!'),
            ('Request/Response', False, 'Niepoprawnie. To model HTTP.'),
            ('Peer-to-Peer', False, 'Niepoprawnie.'),
            ('Broadcast', False, 'Niepoprawnie.')
        ],
        feedback='<p>W MQTT czujniki i aplikacje nie łączą się bezpośrednio - oba komunikują się z centralnym Brokerem. Nagłówek wiadomości to tylko 2 bajty!</p>'
    ))
    
    # Q20 - MQTT QoS
    questions.append(create_question(
        category='Wykład 2 - Protokoły Aplikacyjne',
        qtype='multiplechoice',
        name='Q20_MQTT_QoS_Poziomy',
        question_text='<p>Ile poziomów QoS (Quality of Service) definiuje protokół MQTT?</p>',
        answers=[
            ('3 poziomy: QoS 0, 1, 2', True, 'Poprawnie!'),
            ('2 poziomy', False, 'Niepoprawnie.'),
            ('5 poziomów', False, 'Niepoprawnie.'),
            ('1 poziom', False, 'Niepoprawnie.')
        ],
        feedback='<p>QoS 0: wyślij i zapomnij. QoS 1: potwierdzenie dostarczenia. QoS 2: pełny handshake, gwarancja dokładnie raz.</p>'
    ))
    
    # Q21 - MQTT Last Will
    questions.append(create_question(
        category='Wykład 2 - Protokoły Aplikacyjne',
        qtype='multiplechoice',
        name='Q21_MQTT_Last_Will',
        question_text='<p>Do czego służy mechanizm "Last Will" (LWT) w MQTT?</p>',
        answers=[
            ('Automatyczne powiadomienie o awarii/rozłączeniu urządzenia', True, 'Poprawnie!'),
            ('Ostatnia wiadomość przed aktualizacją', False, 'Niepoprawnie.'),
            ('Wiadomość testowa', False, 'Niepoprawnie.'),
            ('Szyfrowanie połączenia', False, 'Niepoprawnie.')
        ],
        feedback='<p>Last Will Testament to wiadomość wysyłana przez Brokera, gdy klient niespodziewanie się rozłączy. Ważne dla monitoringu awarii.</p>'
    ))
    
    # Q22 - CoAP
    questions.append(create_question(
        category='Wykład 2 - Protokoły Aplikacyjne',
        qtype='multiplechoice',
        name='Q22_CoAP_Protokol',
        question_text='<p>Na jakim protokole transportowym bazuje CoAP (Constrained Application Protocol)?</p>',
        answers=[
            ('UDP', True, 'Poprawnie! CoAP to odpowiednik HTTP na UDP.'),
            ('TCP', False, 'Niepoprawnie. To MQTT i HTTP.'),
            ('SCTP', False, 'Niepoprawnie.'),
            ('ICMP', False, 'Niepoprawnie.')
        ],
        feedback='<p>CoAP używa UDP - szybszy, bezpołączeniowy, ale bez gwarancji dostarczenia. Idealny dla prostych interakcji na mikrokontrolerach.</p>'
    ))
    
    # ==================== WYKŁAD 3: Chmura, Smart City, Bezpieczeństwo ====================
    
    # Q23 - Platformy chmurowe
    questions.append(create_question(
        category='Wykład 3 - Cloud i Platformy',
        qtype='multiplechoice',
        name='Q23_Platformy_Chmurowe',
        question_text='<p>Które z poniższych to platformy IoT typu PaaS od gigantów technologicznych?</p>',
        answers=[
            ('AWS IoT Core, Azure IoT Hub', True, 'Poprawnie!'),
            ('Arduino IDE, PlatformIO', False, 'Niepoprawnie. To środowiska programistyczne.'),
            ('Wireshark, Nmap', False, 'Niepoprawnie. To narzędzia sieciowe.'),
            ('MySQL, PostgreSQL', False, 'Niepoprawnie. To bazy danych.')
        ],
        feedback='<p>AWS IoT Core i Azure IoT Hub to liderzy rynku. Umożliwiają masową aktualizację OTA i integrację z usługami analitycznymi.</p>'
    ))
    
    # Q24 - Vendor Lock-in
    questions.append(create_question(
        category='Wykład 3 - Cloud i Platformy',
        qtype='multiplechoice',
        name='Q24_Vendor_Lockin',
        question_text='<p>Co to jest "Vendor Lock-in" w kontekście platform IoT?</p>',
        answers=[
            ('Sytuacja, gdy firma jest uzależniona od jednego dostawcy chmury, co utrudnia migrację', True, 'Poprawnie!'),
            ('Blokada sprzętowa urządzenia', False, 'Niepoprawnie.'),
            ('Szyfrowanie danych', False, 'Niepoprawnie.'),
            ('Gwarancja na sprzęt', False, 'Niepoprawnie.')
        ],
        feedback='<p>Przykład: Google Cloud IoT Core zostało wyłączone w 2023, zmuszając firmy do kosztownej migracji. Ryzyko zależności od jednego dostawcy.</p>'
    ))
    
    # Q25 - ThingsBoard
    questions.append(create_question(
        category='Wykład 3 - Cloud i Platformy',
        qtype='multiplechoice',
        name='Q25_ThingsBoard',
        question_text='<p>Czym jest ThingsBoard?</p>',
        answers=[
            ('Open-source platforma IoT z dashboardami i zarządzaniem urządzeniami', True, 'Poprawnie!'),
            ('Protokół komunikacyjny', False, 'Niepoprawnie.'),
            ('Typ czujnika temperatury', False, 'Niepoprawnie.'),
            ('Firma produkująca bramki IoT', False, 'Niepoprawnie.')
        ],
        feedback='<p>ThingsBoard to profesjonalna platforma open-source, pozwalająca na wdrożenie on-premise bez zależności od chmury.</p>'
    ))
    
    # Q26 - Smart City Barcelona
    questions.append(create_question(
        category='Wykład 3 - Smart City i IIoT',
        qtype='multiplechoice',
        name='Q26_Barcelona_Smart_City',
        question_text='<p>Jakie korzyści przyniosło wdrożenie IoT w Barcelonie?</p>',
        answers=[
            ('30% oszczędności budżetu energetycznego na oświetleniu, 28% redukcja pustych przejazdów śmieciarek', True, 'Poprawnie!'),
            ('Zwiększenie liczby mieszkańców o 50%', False, 'Niepoprawnie.'),
            ('Całkowita eliminacja korków', False, 'Niepoprawnie.'),
            ('Darmowy Internet dla wszystkich', False, 'Niepoprawnie.')
        ],
        feedback='<p>Barcelona to pionier Smart City. Inteligentne lampy, czujniki kontenerów i nawadnianie parków to realne oszczędności.</p>'
    ))
    
    # Q27 - Predictive Maintenance
    questions.append(create_question(
        category='Wykład 3 - Smart City i IIoT',
        qtype='multiplechoice',
        name='Q27_Predictive_Maintenance',
        question_text='<p>Na czym polega Predictive Maintenance w Przemysle 4.0?</p>',
        answers=[
            ('Przewidywanie awarii maszyn na podstawie analizy wibracji i temperatury zanim do nich dojdzie', True, 'Poprawnie!'),
            ('Naprawa maszyn po awarii', False, 'Niepoprawnie. To maintenance reaktywny.'),
            ('Regularna wymiana części według harmonogramu', False, 'Niepoprawnie. To maintenance prewencyjny.'),
            ('Czyszczenie maszyn', False, 'Niepoprawnie.')
        ],
        feedback='<p>Predictive Maintenance używa danych z czujników do przewidywania awarii. Oszczędza miliony na przestojach w produkcji.</p>'
    ))
    
    # Q28 - Botnet Mirai
    questions.append(create_question(
        category='Wykład 3 - Bezpieczeństwo IoT',
        qtype='multiplechoice',
        name='Q28_Botnet_Mirai',
        question_text='<p>Co to był botnet Mirai (2016)?</p>',
        answers=[
            ('Złośliwe oprogramowanie przejmujące kontrolę nad niezabezpieczonymi kamerami IP do ataków DDoS', True, 'Poprawnie!'),
            ('Nowy protokół bezpieczeństwa', False, 'Niepoprawnie.'),
            ('Firma produkująca kamery', False, 'Niepoprawnie.'),
            ('System operacyjny dla IoT', False, 'Niepoprawnie.')
        ],
        feedback='<p>Mirai wykorzystał domyślne hasła "admin/admin" w milionach kamer. Atak na infrastrukturę DNS wyłączył m.in. Twitter i Netflix.</p>'
    ))
    
    # Q29 - Bezpieczeństwo - dobre praktyki
    questions.append(create_question(
        category='Wykład 3 - Bezpieczeństwo IoT',
        qtype='multiplechoice',
        name='Q29_Bezpieczenstwo_Praktyki',
        question_text='<p>Która z poniższych praktyk NIE jest zalecana dla bezpieczeństwa IoT?</p>',
        answers=[
            ('Pozostawienie domyślnych haseł "admin/admin"', True, 'Poprawnie! To ZŁA praktyka.'),
            ('Szyfrowanie TLS/DTLS', False, 'Niepoprawnie. To DOBRA praktyka.'),
            ('Aktualizacje OTA', False, 'Niepoprawnie. To DOBRA praktyka.'),
            ('Segmentacja sieci VLAN', False, 'Niepoprawnie. To DOBRA praktyka.')
        ],
        feedback='<p>Domyślne hasła to najczęstsza przyczyna przejęć urządzeń. Zawsze zmieniaj hasła i stosuj Defence in Depth.</p>'
    ))
    
    # Q30 - Prywatność - inteligentne liczniki
    questions.append(create_question(
        category='Wykład 3 - Bezpieczeństwo IoT',
        qtype='multiplechoice',
        name='Q30_Prywatnosc_Liczniki',
        question_text='<p>Jakie zagrożenie dla prywatności niosą inteligentne liczniki energii?</p>',
        answers=[
            ('Na podstawie pików zużycia można określić, kiedy mieszkańcy są w domu i jakie urządzenia używają', True, 'Poprawnie!'),
            ('Liczniki mogą wywołać pożar', False, 'Niepoprawnie.'),
            ('Liczniki zużywają dużo prądu', False, 'Niepoprawnie.'),
            ('Liczniki nie są dokładne', False, 'Niepoprawnie.')
        ],
        feedback='<p>Analiza zużycia co 10 sekund pozwala na profilowanie mieszkańców - kiedy wstają, wychodzą, oglądają TV. To dane wrażliwe.</p>'
    ))
    
    # ==================== WYKŁAD INTRO 1: Utopia, Dystopia, Rzeczywistość ====================
    
    # Q31 - IoT w rolnictwie
    questions.append(create_question(
        category='Wykład Intro - Zastosowania IoT',
        qtype='multiplechoice',
        name='Q31_IoT_Rolnictwo',
        question_text='<p>Jak IoT pomaga w precyzyjnym rolnictwie?</p>',
        answers=[
            ('Czujniki glebowe i mikroklimatu pozwalają minimalizować użycie oprysków i nawozów', True, 'Poprawnie!'),
            ('Automatycznie zbiera plony', False, 'Niepoprawnie.'),
            ('Sprzedaje plony online', False, 'Niepoprawnie.'),
            ('Zastępuje rolnika', False, 'Niepoprawnie.')
        ],
        feedback='<p>Precyzyjne rolnictwo używa czujników NPK, pH, wilgotności do optymalizacji nawożenia. Ochrona wód gruntowych przed wymywaniem chemii.</p>'
    ))
    
    # Q32 - Wearables w medycynie
    questions.append(create_question(
        category='Wykład Intro - Zastosowania IoT',
        qtype='multiplechoice',
        name='Q32_Wearables_Medycyna',
        question_text='<p>Co mierzą zaawansowane opaski fitness i smart-obrączki (np. Oura Ring)?</p>',
        answers=[
            ('HRV (zmienność rytmu zatokowego), nasycenie tlenem, wzorce snu', True, 'Poprawnie!'),
            ('Tylko liczbę kroków', False, 'Niepoprawnie. To podstawowe funkcje.'),
            ('Ciśnienie krwi', False, 'Niepoprawnie. Większość nie mierzy.'),
            ('Poziom glukozy', False, 'Niepoprawnie. To wymaga inwazyjnych sensorów.')
        ],
        feedback='<p>Wearables pozwalają na ekstrakcję danych "in-vivo" 24/7, budując bazy danych uczące się wzorców zdrowia.</p>'
    ))
    
    # Q33 - Tree Talker
    questions.append(create_question(
        category='Wykład Intro - Zastosowania IoT',
        qtype='multiplechoice',
        name='Q33_Tree_Talker',
        question_text='<p>Co mierzy urządzenie "Tree Talker" montowane na pniach drzew?</p>',
        answers=[
            ('Przepływ soków (Xylem sap flow), absorpcję światła, wibracje od wiatru', True, 'Poprawnie!'),
            ('Wiek drzewa', False, 'Niepoprawnie.'),
            ('Gatunek drzewa', False, 'Niepoprawnie.'),
            ('Zawartość CO2 w drewnie', False, 'Niepoprawnie.')
        ],
        feedback='<p>Tree Talker to autonomiczne opaski z panelami fotowoltaicznymi, monitorujące zdrowie lasów w czasie rzeczywistym.</p>'
    ))
    
    # Q34 - Generacja 4.0
    questions.append(create_question(
        category='Wykład Intro - Zastosowania IoT',
        qtype='multiplechoice',
        name='Q34_Generacja_4',
        question_text='<p>Co charakteryzuje Generację 4.0 w rolnictwie/przemyśle?</p>',
        answers=[
            ('Wykorzystanie IoT i AI do natychmiastowego zbioru danych i reagowania na warunki środowiska', True, 'Poprawnie!'),
            ('Używanie koni do orki', False, 'Niepoprawnie. To Generacja 1.0.'),
            ('Maszyny parowe', False, 'Niepoprawnie. To Generacja 2.0.'),
            ('Komputery i Excel', False, 'Niepoprawnie. To Generacja 3.0.')
        ],
        feedback='<p>Generacja 4.0 to systemy reagujące na warunki brzegowe, uczące się i komunikujące "językiem naturalnym".</p>'
    ))
    
    # ==================== WYKŁAD INTRO 2: Zagrożenia, AI, Nowe Horyzonty ====================
    
    # Q35 - Cambridge Analytica
    questions.append(create_question(
        category='Wykład Intro 2 - Zagrożenia',
        qtype='multiplechoice',
        name='Q35_Cambridge_Analytica',
        question_text='<p>Na czym polegała afera Cambridge Analytica?</p>',
        answers=[
            ('Wykorzystanie danych z Facebooka do mikro-targetowania wpływającego na wybory', True, 'Poprawnie!'),
            ('Kradzież haseł do kont bankowych', False, 'Niepoprawnie.'),
            ('Atak hakerski na serwery Facebooka', False, 'Niepoprawnie.'),
            ('Fałszowanie wyników wyborczych', False, 'Niepoprawnie.')
        ],
        feedback='<p>Cambridge Analytica pokazała, jak dane z "niewinnych" aplikacji mogą być użyte do manipulacji demokracjami.</p>'
    ))
    
    # Q36 - Chiński system kredytu społecznego
    questions.append(create_question(
        category='Wykład Intro 2 - Zagrożenia',
        qtype='multiplechoice',
        name='Q36_Chiny_Kredyt_Spoleczny',
        question_text='<p>Co to jest chiński System Kredytu Społecznego?</p>',
        answers=[
            ('System automatycznej weryfikacji i nadzoru nad obywatelami, oceniający ich "produktywność"', True, 'Poprawnie!'),
            ('System bankowy', False, 'Niepoprawnie.'),
            ('Program emerytalny', False, 'Niepoprawnie.'),
            ('System podatkowy', False, 'Niepoprawnie.')
        ],
        feedback='<p>To przykład dystopijnego wykorzystania IoT i Big Data do kontroli społecznej. Ktoś grający 10h dziennie w gry może być uznany za "bezproduktywnego".</p>'
    ))
    
    # Q37 - AI i rynek pracy
    questions.append(create_question(
        category='Wykład Intro 2 - Zagrożenia',
        qtype='multiplechoice',
        name='Q37_AI_Rynek_Pracy',
        question_text='<p>Jakie jest ryzyko związane z rozwojem AI w kontekście rynku pracy?</p>',
        answers=[
            ('Wypchnięcie miliardów ludzi z rynku pracy i powstanie "bezużytecznej klasy"', True, 'Poprawnie!'),
            ('Zbyt wiele nowych miejsc pracy', False, 'Niepoprawnie.'),
            ('Spadek wydajności', False, 'Niepoprawnie.'),
            ('Brak wpływu na rynek pracy', False, 'Niepoprawnie.')
        ],
        feedback='<p>AI pisze kod, stawia diagnozy medyczne, przewiduje rynki. Ryzyko to polaryzacja: deficyt wysokokwalifikowanych specjalistów vs masowe bezrobocie.</p>'
    ))
    
    # Q38 - BCI - Brain-Computer Interface
    questions.append(create_question(
        category='Wykład Intro 2 - BCI',
        qtype='multiplechoice',
        name='Q38_BCI_Eksperyment',
        question_text='<p>Co udowodnił eksperyment z interfejsem mózg-mózg (University of Washington, 2013)?</p>',
        answers=[
            ('Możliwość przesyłania intencji ruchowych przez Internet między ludźmi', True, 'Poprawnie!'),
            ('Że ludzie mogą czytać w myślach', False, 'Niepoprawnie.'),
            ('Że mózg nie potrzebuje tlenu', False, 'Niepoprawnie.'),
            ('Że Internet jest za wolny', False, 'Niepoprawnie.')
        ],
        feedback='<p>Eksperyment: Rajesh myślał o strzale, sygnał EEG szedł przez Internet, cewka TMS wywoływała drgnięcie dłoni Andrei. Sukces!</p>'
    ))
    
    # Q39 - Koszt energii
    questions.append(create_question(
        category='Wykład Intro 2 - Energia',
        qtype='multiplechoice',
        name='Q39_Koszt_Energii',
        question_text='<p>Ile energii dziennie zużywa dorosły człowiek w porównaniu do samochodu?</p>',
        answers=[
            ('~3.5 kWh (2500-3000 kcal) vs auto zużywające 2.5 MJ na kilometr', True, 'Poprawnie!'),
            ('Tyle samo', False, 'Niepoprawnie.'),
            ('Człowiek zużywa więcej', False, 'Niepoprawnie.'),
            ('Samochód nie zużywa energii', False, 'Niepoprawnie.')
        ],
        feedback='<p>Przejechanie 5 km autem zużywa więcej energii niż dobowe zapotrzebowanie całego ludzkiego organizmu. Mózg ludzki działa na ~20W!</p>'
    ))
    
    # Q40 - Literatura
    questions.append(create_question(
        category='Wykład Intro 2 - Literatura',
        qtype='multiplechoice',
        name='Q40_Literatura_Harari',
        question_text='<p>Który autor napisał "21 Lekcji na XXI Wiek" i "Homo Deus"?</p>',
        answers=[
            ('Yuval Noah Harari', True, 'Poprawnie!'),
            ('Aldous Huxley', False, 'Niepoprawnie. To "Nowy Wspaniały Świat".'),
            ('Jacek Dukaj', False, 'Niepoprawnie. To "Po słowie".'),
            ('Ramez Naam', False, 'Niepoprawnie. To trylogia Nexus.')
        ],
        feedback='<p>Harari analizuje wpływ technologii na ludzkość. Lektura obowiązkowa dla inżynierów myślących o konsekwencjach swoich projektów.</p>'
    ))
    
    return questions


def generate_moodle_xml(questions, output_path):
    """Generate Moodle XML file from questions list."""
    
    # Root element
    quiz = ET.Element('quiz')
    
    # Add questions
    for q in questions:
        quiz.append(q)
    
    # Convert to string with pretty printing
    xml_str = ET.tostring(quiz, encoding='unicode')
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent='  ', encoding='UTF-8')
    
    # Write to file
    with open(output_path, 'wb') as f:
        f.write(pretty_xml)
    
    print(f"Generated {len(questions)} questions to {output_path}")
    return len(questions)


if __name__ == '__main__':
    questions = generate_all_questions()
    output_file = 'quiz/iot_quiz_40_questions.xml'
    generate_moodle_xml(questions, output_file)
    print(f"Quiz generated successfully!")
