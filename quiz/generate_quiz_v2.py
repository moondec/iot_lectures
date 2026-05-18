#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IoT Quiz Generator v2 - Generates 40 Moodle XML quiz questions
Based on lecture materials from wyklad_1.qmd, wyklad_2.qmd, wyklad_3.qmd,
wyklad_intro_1.qmd, wyklad_intro_2.qmd

REVISION: Added source references to slides/sections, fixed encoding to native UTF-8,
unified terminology with lecture content.

Source verification: Each question includes a comment referencing the exact
slide number and section from the .qmd files.
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom

# Source references dictionary - maps question names to .qmd locations
# Format: (file, slide_section_number, slide_title)
SOURCE_REFERENCES = {
    # Wykład 1
    'Q1_Historia_IoT_Automat': ('wyklad_1.qmd', 'Slajd 2, Sekcja: Mit Założycielski', 'automat z Coca-Colą, CMU 1982'),
    'Q2_Kevin_Ashton_Termin': ('wyklad_1.qmd', 'Slajd 3, Sekcja: Kevin Ashton i Toster', 'termin IoT, P&G 1999'),
    'Q3_Moment_Zwrotny_Skala': ('wyklad_1.qmd', 'Slajd 3, Sekcja: Moment Zwrotny', '2008/2009, Cisco'),
    'Q4_Architektura_Warstwy': ('wyklad_1.qmd', 'Slajd 4, Sekcja: Architektura Systemów IoT', '3 warstwy: Percepcja/Sieć/Aplikacja'),
    'Q5_Warstwa_Percepcji': ('wyklad_1.qmd', 'Slajd 6, Sekcja: Warstwa Percepcji', 'czujniki i aktuatory'),
    'Q6_Edge_Computing_Definicja': ('wyklad_1.qmd', 'Slajd 8, Sekcja: Brama brzegu sieci', 'Edge Gateway, latencja'),
    'Q7_ESP32_Arduino_Porownanie': ('wyklad_1.qmd', 'Slajd 10, Sekcja: Platformy sprzętowe', 'ESP32 vs Arduino vs Raspberry Pi'),
    'Q8_Deep_Sleep_Zasada': ('wyklad_1.qmd', 'Slajd 11, Sekcja: Deep Sleep', 'tryb uśpienia, mikroampery'),
    'Q9_Digital_Twins_Definicja': ('wyklad_1.qmd', 'Slajd 12, Sekcja: Digital Twins', 'Cyfrowy Bliźniak, symulacje'),
    'Q10_Raspberry_Pi_Zastosowanie': ('wyklad_1.qmd', 'Slajd 13, Tabela', 'Raspberry Pi jako Gateway'),
    
    # Wykład 2
    'Q11_Trojkat_Niemozliwy': ('wyklad_2.qmd', 'Slajd 1, Sekcja: Trójkąt Niemożliwy IoT', 'zasięg/przepustowość/bateria'),
    'Q12_WiFi_IoT_Wady': ('wyklad_2.qmd', 'Slajd 2, Sekcja: Wi-Fi', 'prądożerność, beaconing'),
    'Q13_BLE_Roznica': ('wyklad_2.qmd', 'Slajd 3, Sekcja: Bluetooth Low Energy', 'BLE vs Classic, CR2032'),
    'Q14_Zigbee_Mesh': ('wyklad_2.qmd', 'Slajd 4, Sekcja: Zigbee i Z-Wave', 'sieć kratowa, self-healing'),
    'Q15_LPWAN_Zastosowanie': ('wyklad_2.qmd', 'Slajd 5, Sekcja: LPWAN', 'kilometry, 5-10 lat baterii'),
    'Q16_LoRaWAN_NBIoT': ('wyklad_2.qmd', 'Slajd 7, Sekcja: LoRaWAN vs NB-IoT', 'pasmo 868 MHz vs operator'),
    'Q17_Sigfox_Limit': ('wyklad_2.qmd', 'Slajd 8, Sekcja: Sigfox', '140 wiadomości dziennie, 12 bajtów'),
    'Q18_HTTP_IoT_Problem': ('wyklad_2.qmd', 'Slajd 9, Sekcja: Dlaczego HTTP nie pasuje', 'nagłówki, request-response'),
    'Q19_MQTT_PubSub': ('wyklad_2.qmd', 'Slajd 10, Sekcja: MQTT', 'Broker, Topic, Pub/Sub'),
    'Q20_MQTT_QoS': ('wyklad_2.qmd', 'Slajd 11, Sekcja: MQTT Tematy i QoS', 'QoS 0/1/2, Last Will'),
    'Q21_CoAP_UDP': ('wyklad_2.qmd', 'Slajd 12, Sekcja: CoAP i AMQP', 'CoAP na UDP, GET/POST'),
    
    # Wykład 3
    'Q22_Chmura_BigData': ('wyklad_3.qmd', 'Slajd 1, Sekcja: Od gigabajtów do wiedzy', 'Big Data, Cloud Computing'),
    'Q23_Vendor_Lockin': ('wyklad_3.qmd', 'Slajd 2, Sekcja: Platformy korporacyjne', 'Google Cloud IoT Core 2023'),
    'Q24_ThingsBoard': ('wyklad_3.qmd', 'Slajd 3, Sekcja: Narzędzia otwartoźródłowe', 'ThingsBoard, Node-RED'),
    'Q25_Barcelona_SmartCity': ('wyklad_3.qmd', 'Slajd 4, Sekcja: Barcelona', '10000 lamp, 30% oszczędności'),
    'Q26_Predictive_Maintenance': ('wyklad_3.qmd', 'Slajd 5, Sekcja: Smart City i Przemysł 4.0', 'wibracje, temperatura, awarie'),
    'Q27_Digital_Twin_RealTime': ('wyklad_3.qmd', 'Slajd 6, Sekcja: Cyfrowe Bliźniaki', 'strumień danych, What If'),
    'Q28_Botnet_Mirai': ('wyklad_3.qmd', 'Slajd 7, Sekcja: Gdy rzeczy stają się bronią', 'kamery IP, DDoS, 2016'),
    'Q29_Bezpieczenstwo_Praktyki': ('wyklad_3.qmd', 'Slajd 8, Sekcja: Dobre praktyki', 'X.509, OTA, VLAN, Secure Boot'),
    'Q30_Prywatność_Liczniki': ('wyklad_3.qmd', 'Slajd 9, Sekcja: Prywatność', 'liczniki energii, profilowanie'),
    
    # Wykład Intro 1
    'Q31_Rolnictwo_IoT': ('wyklad_intro_1.qmd', 'Slajd 4, Sekcja: IoT w Rolnictwie', 'Tree-Talker, mikroklimat'),
    'Q32_Wearables_Medycyna': ('wyklad_intro_1.qmd', 'Slajd 5, Sekcja: Medycyna', 'HRV, Oura Ring, Self-Tracking'),
    'Q33_Predictive_Przemysl': ('wyklad_intro_1.qmd', 'Slajd 7, Sekcja: Przemysł 4.0', 'łożyska, wibracje, przestoje'),
    'Q34_Generacja_4': ('wyklad_intro_1.qmd', 'Slajd 9, Sekcja: Cykl IoT & AI', 'Generacja 4.0, ML/AI'),
    
    # Wykład Intro 2
    'Q35_Cambridge_Analytica': ('wyklad_intro_2.qmd', 'Slajd 1, Sekcja: Ciemna strona mocy', 'Facebook, mikro-targetowanie'),
    'Q36_Chinski_System': ('wyklad_intro_2.qmd', 'Slajd 1, Sekcja: Ciemna strona mocy', 'Kredyt Społeczny, inwigilacja'),
    'Q37_AI_Rynek_Pracy': ('wyklad_intro_2.qmd', 'Slajd 2, Sekcja: Sztuczna Inteligencja', 'bezużyteczna klasa, Harari'),
    'Q38_BCI_Nicolelis': ('wyklad_intro_2.qmd', 'Slajd 6, Sekcja: Bezpośredni transfer wrażeń', 'szczury, TCP/IP, mózg-mózg'),
    'Q39_Koszt_Energii': ('wyklad_intro_2.qmd', 'Slajd 8, Sekcja: Podstawowa Blokada', '2500-3000 kcal, 3.5 kWh'),
    'Q40_Literatura_Harari': ('wyklad_intro_2.qmd', 'Slajd 9, Sekcja: Literatura', 'Homo Deus, 21 Lekcji'),
}


def create_question(category, qtype, name, question_text, answers, correct_indices=None, feedback=None, source_ref=None):
    """
    Create a single question element for Moodle XML format.
    
    Args:
        category: Question category
        qtype: 'multichoice', 'truefalse', 'matching', 'numerical' (NOTE: Moodle uses 'multichoice' not 'multichoice')
        name: Question name/identifier
        question_text: The actual question text (native UTF-8, no HTML entities)
        answers: List of tuples (answer_text, is_correct, feedback)
        correct_indices: For multiple choice, indices of correct answers
        feedback: General feedback for the question
        source_ref: Tuple (file, slide, topic) for source verification
    """
    """
    Create a single question element for Moodle XML format.
    
    Args:
        category: Question category
        qtype: 'multichoice', 'truefalse', 'matching', 'numerical'
        name: Question name/identifier
        question_text: The actual question text (native UTF-8, no HTML entities)
        answers: List of tuples (answer_text, is_correct, feedback)
        correct_indices: For multiple choice, indices of correct answers
        feedback: General feedback for the question
        source_ref: Tuple (file, slide, topic) for source verification
    """
    question = ET.Element('question', type=qtype)
    
    # Add source reference as comment in category (for verification)
    if source_ref:
        category_text = f"{category} [Źródło: {source_ref[0]}, {source_ref[1]}]"
    else:
        category_text = category
    
    # Category
    cat_elem = ET.SubElement(question, 'category')
    cat_text = ET.SubElement(cat_elem, 'text')
    cat_text.text = category_text
    
    # Name
    name_elem = ET.SubElement(question, 'name')
    name_text = ET.SubElement(name_elem, 'text')
    name_text.text = name
    
    # Question text - using format="html" but with native UTF-8 characters
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
    if qtype == 'multichoice':
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
    """Generate all 40 quiz questions with source references."""
    questions = []
    
    # ==================== WYKŁAD 1: Od koncepcji do Przemysłu 4.0 ====================
    
    # Q1 - Historia IoT - Automat Coca-Cola (wyklad_1.qmd, Slajd 2)
    questions.append(create_question(
        category='Wykład 1 - Podstawy IoT',
        qtype='multichoice',
        name='Q1_Historia_IoT_Automat',
        question_text='<p>W którym roku i na jakiej uczelni powstał pierwszy prototyp urządzenia IoT – Automat Coca-Cola połączony z siecią?</p>',
        answers=[
            ('1982, Carnegie Mellon University (CMU)', True, 'Poprawnie! Studenci CMU w 1982 roku podłączyli Automat Coca-Cola do sieci wydziałowej.'),
            ('1999, MIT', False, 'Niepoprawnie. 1999 to rok użycia terminu "Internet of Things" przez Kevina Ashtona.'),
            ('1969, Stanford', False, 'Niepoprawnie. 1969 to rok uruchomienia ARPANET.'),
            ('1990, Berkeley', False, 'Niepoprawnie.')
        ],
        feedback='<p>Pierwszy prototyp IoT powstał w 1982 roku na Carnegie Mellon University. Studenci zmęczeni schodzeniem po schodach do automatu podłączyli go do sieci, aby zdalnie sprawdzać dostępność napojów.</p>',
        source_ref=SOURCE_REFERENCES['Q1_Historia_IoT_Automat']
    ))
    
    # Q2 - Kevin Ashton (wyklad_1.qmd, Slajd 3)
    questions.append(create_question(
        category='Wykład 1 - Podstawy IoT',
        qtype='multichoice',
        name='Q2_Kevin_Ashton_Termin',
        question_text='<p>Kto i w którym roku ukuł termin "Internet of Things" (IoT)?</p>',
        answers=[
            ('Kevin Ashton, 1999', True, 'Poprawnie! Kevin Ashton z Procter & Gamble użył tego terminu w prezentacji w 1999 roku.'),
            ('Tim Berners-Lee, 1989', False, 'Niepoprawnie. Tim Berners-Lee wynalazł World Wide Web.'),
            ('Vint Cerf, 2000', False, 'Niepoprawnie.'),
            ('Elon Musk, 2010', False, 'Niepoprawnie.')
        ],
        feedback='<p>Kevin Ashton, pracując w Procter & Gamble, analizował problem pustych półek ze szminkami Olay i zidentyfikował technologię RFID jako klucz do autonomicznego śledzenia towarów.</p>',
        source_ref=SOURCE_REFERENCES['Q2_Kevin_Ashton_Termin']
    ))
    
    # Q3 - Moment zwrotny IoT (wyklad_1.qmd, Slajd 3)
    questions.append(create_question(
        category='Wykład 1 - Podstawy IoT',
        qtype='multichoice',
        name='Q3_Moment_Zwrotny_Skala',
        question_text='<p>W którym roku liczba aktywnych, połączonych urządzeń po raz pierwszy przewyższyła całkowitą populację ludzi na Ziemi?</p>',
        answers=[
            ('2008/2009', True, 'Poprawnie! Według analiz Cisco był to historyczny Rubikon.'),
            ('2000', False, 'Niepoprawnie. To za wcześnie.'),
            ('2015', False, 'Niepoprawnie. To już po przekroczeniu.'),
            ('1999', False, 'Niepoprawnie.')
        ],
        feedback='<p>Rok 2008/2009 to moment, gdy urządzenia IoT zaczęły generować więcej danych niż ludzie. To początek ery pasywnego generowania danych telemetrycznych.</p>',
        source_ref=SOURCE_REFERENCES['Q3_Moment_Zwrotny_Skala']
    ))
    
    # Q4 - Architektura 3-warstwowa (wyklad_1.qmd, Slajd 4)
    questions.append(create_question(
        category='Wykład 1 - Architektura IoT',
        qtype='multichoice',
        name='Q4_Architektura_Warstwy',
        question_text='<p>Jakie są trzy główne warstwy architektury systemów IoT według modelu IEEE?</p>',
        answers=[
            ('Percepcja, Sieć, Aplikacja', True, 'Poprawnie! To podstawowy model 3-warstwowy.'),
            ('Hardware, Software, Cloud', False, 'Niepoprawnie.'),
            ('Czujniki, Procesory, Ekrany', False, 'Niepoprawnie.'),
            ('Input, Processing, Output', False, 'Niepoprawnie. To model komputera, nie IoT.')
        ],
        feedback='<p>Model 3-warstwowy: Percepcja (czujniki/aktuatory), Sieć (bramy, routing), Aplikacja (dashboardy, analityka).</p>',
        source_ref=SOURCE_REFERENCES['Q4_Architektura_Warstwy']
    ))
    
    # Q5 - Warstwa percepcji (wyklad_1.qmd, Slajd 6)
    questions.append(create_question(
        category='Wykład 1 - Architektura IoT',
        qtype='multichoice',
        name='Q5_Warstwa_Percepcji',
        question_text='<p>Co należy do warstwy percepcji w systemie IoT?</p>',
        answers=[
            ('Czujniki i aktuatory', True, 'Poprawnie! To "zmysły" i "ręce" systemu IoT.'),
            ('Serwery chmurowe', False, 'Niepoprawnie. To warstwa aplikacji.'),
            ('Protokoły MQTT, HTTP', False, 'Niepoprawnie. To warstwa sieci/aplikacji.'),
            ('Bazy danych', False, 'Niepoprawnie.')
        ],
        feedback='<p>Warstwa percepcji odpowiada za zbieranie danych z otoczenia (czujniki) i wpływ na fizyczny świat (aktuatory).</p>',
        source_ref=SOURCE_REFERENCES['Q5_Warstwa_Percepcji']
    ))
    
    # Q6 - Edge Computing (wyklad_1.qmd, Slajd 8)
    questions.append(create_question(
        category='Wykład 1 - Architektura IoT',
        qtype='multichoice',
        name='Q6_Edge_Computing_Definicja',
        question_text='<p>Czym jest Edge Computing w kontekście IoT?</p>',
        answers=[
            ('Przetwarzanie danych blisko źródła ich powstawania, na brzegu sieci', True, 'Poprawnie! Redukuje to opóźnienia i obciążenie chmury.'),
            ('Przesyłanie wszystkich danych bezpośrednio do chmury', False, 'Niepoprawnie. To przeciwieństwo Edge Computing.'),
            ('Zapisywanie danych na dyskach lokalnych', False, 'Niepoprawnie.'),
            ('Używanie tylko sieci kablowych', False, 'Niepoprawnie.')
        ],
        feedback='<p>Edge Computing pozwala na filtrowanie i agregację danych na bramie (Gateway), zanim trafią do chmury. Krytyczne dla systemów czasu rzeczywistego.</p>',
        source_ref=SOURCE_REFERENCES['Q6_Edge_Computing_Definicja']
    ))
    
    # Q7 - ESP32 vs Arduino (wyklad_1.qmd, Slajd 10)
    questions.append(create_question(
        category='Wykład 1 - Platformy Sprzętowe',
        qtype='multichoice',
        name='Q7_ESP32_Arduino_Porownanie',
        question_text='<p>Która platforma sprzętowa ma wbudowane Wi-Fi i Bluetooth oraz bardzo niski pobór prądu w trybie uśpienia?</p>',
        answers=[
            ('ESP32', True, 'Poprawnie! ESP32 to król taniego, profesjonalnego IoT.'),
            ('Arduino Uno', False, 'Niepoprawnie. Arduino wymaga dodatkowych shieldów do łączności radiowej.'),
            ('Raspberry Pi 5', False, 'Niepoprawnie. Raspberry Pi to komputer, zbyt prądożerny dla czujników bateryjnych.'),
            ('Intel NUC', False, 'Niepoprawnie.')
        ],
        feedback='<p>ESP32 to System on Chip (SoC) z wbudowanym Wi-Fi/Bluetooth, pobierający mikroampery w trybie deep sleep. Idealny dla autonomicznych czujników terenowych.</p>',
        source_ref=SOURCE_REFERENCES['Q7_ESP32_Arduino_Porownanie']
    ))
    
    # Q8 - Deep Sleep (wyklad_1.qmd, Slajd 11)
    questions.append(create_question(
        category='Wykład 1 - Platformy Sprzętowe',
        qtype='multichoice',
        name='Q8_Deep_Sleep_Zasada',
        question_text='<p>Na czym polega mechanizm "Deep Sleep" w mikrokontrolerach IoT?</p>',
        answers=[
            ('Procesor wyłącza większość systemów, budzi się tylko na chwilę by wykonać zadanie i zasypia ponownie', True, 'Poprawnie! To klucz do wieloletniej pracy na baterii.'),
            ('Procesor działa z pełną wydajnością 24/7', False, 'Niepoprawnie. To szybko wyczerpie baterię.'),
            ('Bateria jest ładowana energią słoneczną', False, 'Niepoprawnie. To osobna technologia.'),
            ('Urządzenie jest podłączone do sieci elektrycznej', False, 'Niepoprawnie.')
        ],
        feedback='<p>Deep Sleep pozwala mikrokontrolerom pracować lata na jednej baterii. Procesor budzi się na ułamek sekundy, wysyła dane i wraca do snu.</p>',
        source_ref=SOURCE_REFERENCES['Q8_Deep_Sleep_Zasada']
    ))
    
    # Q9 - Digital Twins (wyklad_1.qmd, Slajd 12)
    questions.append(create_question(
        category='Wykład 1 - Digital Twins',
        qtype='multichoice',
        name='Q9_Digital_Twins_Definicja',
        question_text='<p>Czym jest Cyfrowy Bliźniak (Digital Twin) w IoT?</p>',
        answers=[
            ('Wirtualna kopia fizycznego obiektu/systemu zasilana danymi z czujników w czasie rzeczywistym', True, 'Poprawnie!'),
            ('Kopia zapasowa danych w chmurze', False, 'Niepoprawnie.'),
            ('Drugi identyczny czujnik dla redundancji', False, 'Niepoprawnie.'),
            ('Symulator bez połączenia z rzeczywistymi danymi', False, 'Niepoprawnie.')
        ],
        feedback='<p>Cyfrowy Bliźniak to nie tylko wizualizacja 3D - to żywy model zasilany strumieniem danych z czujników, pozwalający na symulacje "What If".</p>',
        source_ref=SOURCE_REFERENCES['Q9_Digital_Twins_Definicja']
    ))
    
    # Q10 - Raspberry Pi zastosowanie (wyklad_1.qmd, Slajd 13)
    questions.append(create_question(
        category='Wykład 1 - Platformy Sprzętowe',
        qtype='multichoice',
        name='Q10_Raspberry_Pi_Zastosowanie',
        question_text='<p>Do czego najlepiej nadaje się Raspberry Pi w architekturze IoT?</p>',
        answers=[
            ('Lokalna brama (Gateway) koordynująca, serwer MQTT, Edge Computing', True, 'Poprawnie! Raspberry Pi to pełny komputer z Linuxem.'),
            ('Autonomiczny czujnik terenowy na baterii', False, 'Niepoprawnie. Zbyt prądożerny.'),
            ('Prosty prototyp edukacyjny bez łączności', False, 'Niepoprawnie. Do tego lepsze Arduino.'),
            ('Zasilanie innych urządzeń', False, 'Niepoprawnie.')
        ],
        feedback='<p>Raspberry Pi to Single Board Computer (SBC) z Linuxem. Idealny jako lokalny serwer, brama lub hub, ale wymaga stałego zasilania.</p>',
        source_ref=SOURCE_REFERENCES['Q10_Raspberry_Pi_Zastosowanie']
    ))
    
    # ==================== WYKŁAD 2: Język Rzeczy - Protokoły ====================
    
    # Q11 - Trójkąt niemożliwy IoT (wyklad_2.qmd, Slajd 1)
    questions.append(create_question(
        category='Wykład 2 - Protokoły Komunikacyjne',
        qtype='multichoice',
        name='Q11_Trojkat_Niemozliwy',
        question_text='<p>W "Trójkącie Niemożliwym IoT" inżynier może wybrać tylko DWA z trzech parametrów. Które to parametry?</p>',
        answers=[
            ('Zasięg, Przepustowość, Czas życia na baterii', True, 'Poprawnie! Nie da się mieć wszystkich trzech jednocześnie.'),
            ('Koszt, Rozmiar, Kolor', False, 'Niepoprawnie.'),
            ('Szybkość, Bezpieczeństwo, Cena', False, 'Niepoprawnie.'),
            ('Zasięg, Bezpieczeństwo, Cena', False, 'Niepoprawnie.')
        ],
        feedback='<p>Fizyka fal elektromagnetycznych wymusza kompromis: daleki zasięg + długa bateria = niska przepustowość (LPWAN).</p>',
        source_ref=SOURCE_REFERENCES['Q11_Trojkat_Niemozliwy']
    ))
    
    # Q12 - Wi-Fi wady (wyklad_2.qmd, Slajd 2)
    questions.append(create_question(
        category='Wykład 2 - Protokoły Komunikacyjne',
        qtype='multichoice',
        name='Q12_WiFi_IoT_Wady',
        question_text='<p>Dlaczego Wi-Fi jest nieodpowiednie dla urządzeń IoT zasilanych bateryjnie?</p>',
        answers=[
            ('Koszmarnie prądożerne - napadowe budzenie anteny i beaconing pochłaniają setki mA', True, 'Poprawnie!'),
            ('Zbyt mały zasięg', False, 'Niepoprawnie. Zasięg Wi-Fi jest wystarczający.'),
            ('Brak obsługi IPv6', False, 'Niepoprawnie. Wi-Fi obsługuje IPv6.'),
            ('Zbyt wysoka przepustowość', False, 'Niepoprawnie.')
        ],
        feedback='<p>Wi-Fi wymaga ciągłego nasłuchiwania beaconów i złożonego handshake, co zużywa setki mA. Nadaje się tylko dla urządzeń ze stałym zasilaniem.</p>',
        source_ref=SOURCE_REFERENCES['Q12_WiFi_IoT_Wady']
    ))
    
    # Q13 - BLE różnica (wyklad_2.qmd, Slajd 3)
    questions.append(create_question(
        category='Wykład 2 - Protokoły Komunikacyjne',
        qtype='multichoice',
        name='Q13_BLE_Roznica',
        question_text='<p>Jaka jest główna różnica między Bluetooth Classic a Bluetooth Low Energy (BLE)?</p>',
        answers=[
            ('BLE usypia radio natychmiast po wysłaniu pakietu, Classic przesyła ciągły strumień', True, 'Poprawnie!'),
            ('BLE ma większy zasięg', False, 'Niepoprawnie.'),
            ('Classic jest nowszy', False, 'Niepoprawnie. BLE jest nowszy.'),
            ('Nie ma różnicy', False, 'Niepoprawnie.')
        ],
        feedback='<p>Bluetooth Low Energy (BLE) wprowadził rewolucyjny tryb uśpienia - radio budzi się na milisekundy, wysyła pakiet i zasypia. Bateria CR2032 wystarcza na lata.</p>',
        source_ref=SOURCE_REFERENCES['Q13_BLE_Roznica']
    ))
    
    # Q14 - Zigbee Mesh (wyklad_2.qmd, Slajd 4)
    questions.append(create_question(
        category='Wykład 2 - Protokoły Komunikacyjne',
        qtype='multichoice',
        name='Q14_Zigbee_Mesh',
        question_text='<p>Jaką zaletę ma sieć Zigbee w topologii Mesh?</p>',
        answers=[
            ('Urządzenia zasilane z sieci działają jako wzmacniacze, system samoleczący', True, 'Poprawnie!'),
            ('Mniejszy pobór energii niż BLE', False, 'Niepoprawnie.'),
            ('Działa w paśmie 5 GHz', False, 'Niepoprawnie. Zigbee działa w 2,4 GHz.'),
            ('Nie wymaga bramki', False, 'Niepoprawnie.')
        ],
        feedback='<p>Zigbee Mesh pozwala urządzeniom zasilanym z sieci (np. żarówki) działać jako routery, przekazując pakiety od czujników bateryjnych. Awaria jednego węzła nie przerywa komunikacji.</p>',
        source_ref=SOURCE_REFERENCES['Q14_Zigbee_Mesh']
    ))
    
    # Q15 - LPWAN zastosowanie (wyklad_2.qmd, Slajd 5)
    questions.append(create_question(
        category='Wykład 2 - Protokoły Komunikacyjne',
        qtype='multichoice',
        name='Q15_LPWAN_Zastosowanie',
        question_text='<p>Do czego służy technologia LPWAN (Low Power Wide Area Network)?</p>',
        answers=[
            ('Telemetria na kilometry przy minimalnym zużyciu energii, bateria 5-10 lat', True, 'Poprawnie!'),
            ('Przesyłanie wideo z kamer', False, 'Niepoprawnie. LPWAN ma zbyt niską przepustowość.'),
            ('Komunikacja wewnątrz jednego pomieszczenia', False, 'Niepoprawnie.'),
            ('Połączenia głosowe', False, 'Niepoprawnie.')
        ],
        feedback='<p>LPWAN oferuje zasięg 15-20 km i żywotność baterii 5-10 lat, ale przesyła tylko kilkadziesiąt bajtów na sekundę. Idealne dla czujników środowiskowych.</p>',
        source_ref=SOURCE_REFERENCES['Q15_LPWAN_Zastosowanie']
    ))
    
    # Q16 - LoRaWAN vs NB-IoT (wyklad_2.qmd, Slajd 7)
    questions.append(create_question(
        category='Wykład 2 - Protokoły Komunikacyjne',
        qtype='multichoice',
        name='Q16_LoRaWAN_NBIoT',
        question_text='<p>Jaka jest główna różnica między LoRaWAN a NB-IoT?</p>',
        answers=[
            ('LoRaWAN pozwala na budowę własnych bramek w darmowym paśmie, NB-IoT wymaga operatora', True, 'Poprawnie!'),
            ('NB-IoT ma większy zasięg', False, 'Niepoprawnie.'),
            ('LoRaWAN wymaga abonamentu', False, 'Niepoprawnie. LoRaWAN może być darmowy.'),
            ('Nie ma różnicy', False, 'Niepoprawnie.')
        ],
        feedback='<p>LoRaWAN działa w darmowym paśmie 868 MHz, pozwala na budowę własnej sieci. NB-IoT to standard operatorów komórkowych na istniejącej infrastrukturze 4G.</p>',
        source_ref=SOURCE_REFERENCES['Q16_LoRaWAN_NBIoT']
    ))
    
    # Q17 - Sigfox limit (wyklad_2.qmd, Slajd 8)
    questions.append(create_question(
        category='Wykład 2 - Protokoły Komunikacyjne',
        qtype='multichoice',
        name='Q17_Sigfox_Limit',
        question_text='<p>Ile wiadomości dziennie może wysłać urządzenie w sieci Sigfox?</p>',
        answers=[
            ('Maksymalnie 140 wiadomości dziennie, 12 bajtów na wiadomość', True, 'Poprawnie!'),
            ('Nieograniczenie', False, 'Niepoprawnie.'),
            ('1000 wiadomości', False, 'Niepoprawnie.'),
            ('Tylko 1 wiadomość', False, 'Niepoprawnie.')
        ],
        feedback='<p>Sigfox to technologia ultralekkich wiadomości - maksymalnie 140 wiadomości dziennie po 12 bajtów. Idealne dla prostych powiadomień "jestem sprawny".</p>',
        source_ref=SOURCE_REFERENCES['Q17_Sigfox_Limit']
    ))
    
    # Q18 - HTTP problem (wyklad_2.qmd, Slajd 9)
    questions.append(create_question(
        category='Wykład 2 - Protokoły Aplikacyjne',
        qtype='multichoice',
        name='Q18_HTTP_IoT_Problem',
        question_text='<p>Dlaczego protokół HTTP nie pasuje do urządzeń IoT?</p>',
        answers=[
            ('Duży narzut nagłówków, model synchroniczny request-response, brak asynchroniczności', True, 'Poprawnie!'),
            ('HTTP nie obsługuje JSON', False, 'Niepoprawnie.'),
            ('HTTP jest zbyt wolny', False, 'Niepoprawnie.'),
            ('HTTP wymaga kabla Ethernet', False, 'Niepoprawnie.')
        ],
        feedback='<p>HTTP ma duże nagłówki (często większe niż dane pomiarowe) i wymaga synchronicznego oczekiwania na odpowiedź, co zużywa energię radia.</p>',
        source_ref=SOURCE_REFERENCES['Q18_HTTP_IoT_Problem']
    ))
    
    # Q19 - MQTT Pub/Sub (wyklad_2.qmd, Slajd 10)
    questions.append(create_question(
        category='Wykład 2 - Protokoły Aplikacyjne',
        qtype='multichoice',
        name='Q19_MQTT_PubSub',
        question_text='<p>Jak działa architektura MQTT?</p>',
        answers=[
            ('Publikacja/Subskrypcja przez centralnego Brokera, urządzenia nie wiedzą o sobie nawzajem', True, 'Poprawnie!'),
            ('Bezpośrednie połączenie między czujnikiem a aplikacją', False, 'Niepoprawnie.'),
            ('Każde urządzenie odpytuje serwer', False, 'Niepoprawnie. To model HTTP.'),
            ('Połączenie punkt-punkt', False, 'Niepoprawnie.')
        ],
        feedback='<p>MQTT używa Brokera jako pośrednika. Czujnik publikuje wiadomość pod tematem, Broker dystrybuuje ją do wszystkich subskrybentów. Nagłówek wiadomości to tylko 2 bajty.</p>',
        source_ref=SOURCE_REFERENCES['Q19_MQTT_PubSub']
    ))
    
    # Q20 - MQTT QoS (wyklad_2.qmd, Slajd 11)
    questions.append(create_question(
        category='Wykład 2 - Protokoły Aplikacyjne',
        qtype='multichoice',
        name='Q20_MQTT_QoS',
        question_text='<p>Co oznacza QoS 2 w protokole MQTT?</p>',
        answers=[
            ('Pełny handshake, gwarancja dostarczenia wiadomości', True, 'Poprawnie!'),
            ('Wyślij i zapomnij', False, 'Niepoprawnie. To QoS 0.'),
            ('Wymaga potwierdzenia, możliwe duplikaty', False, 'Niepoprawnie. To QoS 1.'),
            ('Brak potwierdzenia', False, 'Niepoprawnie.')
        ],
        feedback='<p>QoS 2 to najwyższy poziom - pełny handshake (PUBREC/PUBREL/PUBCOMP) gwarantujący dokładnie jednokrotne dostarczenie. QoS 0 to "fire and forget", QoS 1 to "at least once".</p>',
        source_ref=SOURCE_REFERENCES['Q20_MQTT_QoS']
    ))
    
    # Q21 - CoAP UDP (wyklad_2.qmd, Slajd 12)
    questions.append(create_question(
        category='Wykład 2 - Protokoły Aplikacyjne',
        qtype='multichoice',
        name='Q21_CoAP_UDP',
        question_text='<p>Na jakim protokole transportowym bazuje CoAP?</p>',
        answers=[
            ('UDP - szybszy, bezpołączeniowy, bez gwarancji dostarczenia', True, 'Poprawnie!'),
            ('TCP', False, 'Niepoprawnie. To MQTT i HTTP.'),
            ('SCTP', False, 'Niepoprawnie.'),
            ('ICMP', False, 'Niepoprawnie.')
        ],
        feedback='<p>CoAP (Constrained Application Protocol) to odpowiednik HTTP dla mikrokontrolerów, działający na UDP. Szybszy, ale bez gwarancji dostarczenia. Obsługuje metody GET, POST, PUT.</p>',
        source_ref=SOURCE_REFERENCES['Q21_CoAP_UDP']
    ))
    
    # ==================== WYKŁAD 3: Mózg w Chmurze i jego Cienie ====================
    
    # Q22 - Chmura Big Data (wyklad_3.qmd, Slajd 1)
    questions.append(create_question(
        category='Wykład 3 - Cloud i Platformy',
        qtype='multichoice',
        name='Q22_Chmura_BigData',
        question_text='<p>Dlaczego pojedynczy czujnik temperatury jest bezwartościowy, ale 10 000 czujników tworzy wartość?</p>',
        answers=[
            ('10 000 czujników generuje Big Data, z których można wyciągać wnioski biznesowe', True, 'Poprawnie!'),
            ('Pojedynczy czujnik jest zbyt tani', False, 'Niepoprawnie.'),
            ('10 000 czujników zużywa więcej prądu', False, 'Niepoprawnie.'),
            ('Nie ma różnicy', False, 'Niepoprawnie.')
        ],
        feedback='<p>Big Data z tysięcy czujników pozwala na analizę wzorców, predykcję i optymalizację. Pojedynczy punkt danych nie daje kontekstu.</p>',
        source_ref=SOURCE_REFERENCES['Q22_Chmura_BigData']
    ))
    
    # Q23 - Vendor Lock-in (wyklad_3.qmd, Slajd 2)
    questions.append(create_question(
        category='Wykład 3 - Cloud i Platformy',
        qtype='multichoice',
        name='Q23_Vendor_Lockin',
        question_text='<p>Co stało się z Google Cloud IoT Core w 2023 roku?</p>',
        answers=[
            ('Google wyłączyło usługę, zmuszając firmy do kosztownej migracji', True, 'Poprawnie!'),
            ('Google zwiększyło pojemność', False, 'Niepoprawnie.'),
            ('Usługa została sprzedana Amazonowi', False, 'Niepoprawnie.'),
            ('Nic, działa nadal', False, 'Niepoprawnie.')
        ],
        feedback='<p>Wyłączenie Google Cloud IoT Core w 2023 to przykład Vendor Lock-in - oparcie projektu w 100% o jednego dostawcę chmury to poważne ryzyko biznesowe.</p>',
        source_ref=SOURCE_REFERENCES['Q23_Vendor_Lockin']
    ))
    
    # Q24 - ThingsBoard (wyklad_3.qmd, Slajd 3)
    questions.append(create_question(
        category='Wykład 3 - Cloud i Platformy',
        qtype='multichoice',
        name='Q24_ThingsBoard',
        question_text='<p>Które narzędzie open-source pozwala na tworzenie profesjonalnych dashboardów IoT?</p>',
        answers=[
            ('ThingsBoard', True, 'Poprawnie! ThingsBoard obsługuje ogromne potoki danych telemetrycznych.'),
            ('Photoshop', False, 'Niepoprawnie.'),
            ('Excel', False, 'Niepoprawnie.'),
            ('Notepad', False, 'Niepoprawnie.')
        ],
        feedback='<p>ThingsBoard to platforma open-source z profesjonalnymi dashboardami. Inne narzędzia to Home Assistant (integracja lokalna) i Node-RED (wizualne programowanie logiki).</p>',
        source_ref=SOURCE_REFERENCES['Q24_ThingsBoard']
    ))
    
    # Q25 - Barcelona Smart City (wyklad_3.qmd, Slajd 4)
    questions.append(create_question(
        category='Wykład 3 - Smart City i IIoT',
        qtype='multichoice',
        name='Q25_Barcelona_SmartCity',
        question_text='<p>Jakie oszczędności osiągnęła Barcelona dzięki inteligentnemu oświetleniu miejskiemu?</p>',
        answers=[
            ('30% budżetu energetycznego rocznie dzięki 10 000 lamp analizujących ruch', True, 'Poprawnie!'),
            ('10%', False, 'Niepoprawnie.'),
            ('50%', False, 'Niepoprawnie.'),
            ('Nie było oszczędności', False, 'Niepoprawnie.')
        ],
        feedback='<p>Barcelona to pionier Smart City. 10 000 lamp analizuje ruch pieszych i gaśnie inteligentnie na peryferiach, oszczędzając 30% budżetu energetycznego.</p>',
        source_ref=SOURCE_REFERENCES['Q25_Barcelona_SmartCity']
    ))
    
    # Q26 - Predictive Maintenance (wyklad_3.qmd, Slajd 5)
    questions.append(create_question(
        category='Wykład 3 - Smart City i IIoT',
        qtype='multichoice',
        name='Q26_Predictive_Maintenance',
        question_text='<p>Na czym polega Predictive Maintenance w Przemysle 4.0?</p>',
        answers=[
            ('Przewidywanie awarii maszyn na podstawie analizy wibracji i temperatury zanim dojdzie do fizycznej awarii', True, 'Poprawnie!'),
            ('Naprawa maszyn po awarii', False, 'Niepoprawnie. To maintenance reaktywny.'),
            ('Regularna wymiana części co miesiąc', False, 'Niepoprawnie. To maintenance prewencyjny.'),
            ('Czyszczenie maszyn', False, 'Niepoprawnie.')
        ],
        feedback='<p>Predictive Maintenance używa czujników wibracji i temperatury do wykrywania wczesnych oznak zużycia łożysk i innych podzespołów, pozwalając na planowaną naprawę przed katastrofalną awarią.</p>',
        source_ref=SOURCE_REFERENCES['Q26_Predictive_Maintenance']
    ))
    
    # Q27 - Digital Twin Real-Time (wyklad_3.qmd, Slajd 6)
    questions.append(create_question(
        category='Wykład 3 - Smart City i IIoT',
        qtype='multichoice',
        name='Q27_Digital_Twin_RealTime',
        question_text='<p>Czym różni się Cyfrowy Bliźniak od zwykłej wizualizacji 3D?</p>',
        answers=[
            ('Cyfrowy Bliźniak jest zasilany strumieniem danych z czujników w czasie rzeczywistym', True, 'Poprawnie!'),
            ('Niczym, to to samo', False, 'Niepoprawnie.'),
            ('Cyfrowy Bliźniak jest większy', False, 'Niepoprawnie.'),
            ('Wizualizacja 3D jest droższa', False, 'Niepoprawnie.')
        ],
        feedback='<p>Cyfrowy Bliźniak to nie statyczny model 3D - to żywa reprezentacja zasilana danymi telemetrycznymi w czasie rzeczywistym, pozwalająca na symulacje "What If".</p>',
        source_ref=SOURCE_REFERENCES['Q27_Digital_Twin_RealTime']
    ))
    
    # Q28 - Botnet Mirai (wyklad_3.qmd, Slajd 7)
    questions.append(create_question(
        category='Wykład 3 - Bezpieczeństwo IoT',
        qtype='multichoice',
        name='Q28_Botnet_Mirai',
        question_text='<p>Co to był Botnet Mirai (2016)?</p>',
        answers=[
            ('Złośliwe oprogramowanie przejmujące kontrolę nad niezabezpieczonymi kamerami IP do ataków DDoS', True, 'Poprawnie!'),
            ('Nowy protokół komunikacyjny', False, 'Niepoprawnie.'),
            ('Firma produkująca kamery', False, 'Niepoprawnie.'),
            ('System antywirusowy', False, 'Niepoprawnie.')
        ],
        feedback='<p>Mirai przejął miliony kamer IP z domyślnymi hasłami (admin/admin) i użył ich do gigantycznego ataku DDoS na infrastrukturę DNS, wyłączając m.in. Twitter i Netflix.</p>',
        source_ref=SOURCE_REFERENCES['Q28_Botnet_Mirai']
    ))
    
    # Q29 - Bezpieczeństwo praktyki (wyklad_3.qmd, Slajd 8)
    questions.append(create_question(
        category='Wykład 3 - Bezpieczeństwo IoT',
        qtype='multichoice',
        name='Q29_Bezpieczenstwo_Praktyki',
        question_text='<p>Które NIE jest dobrą praktyką bezpieczeństwa IoT?</p>',
        answers=[
            ('Używanie domyślnych haseł admin/admin', True, 'Poprawnie! To ZŁA praktyka - należy zmieniać hasła.'),
            ('Szyfrowanie asymetryczne X.509', False, 'Niepoprawnie. To DOBRA praktyka.'),
            ('Aktualizacje OTA', False, 'Niepoprawnie. To DOBRA praktyka.'),
            ('Segmentacja sieci VLAN', False, 'Niepoprawnie. To DOBRA praktyka.')
        ],
        feedback='<p>Dobre praktyki: X.509 dla TLS/DTLS, aktualizacje OTA, segmentacja VLAN, Secure Boot. Domyślne hasła to najczęstsza przyczyna przejęć urządzeń.</p>',
        source_ref=SOURCE_REFERENCES['Q29_Bezpieczenstwo_Praktyki']
    ))
    
    # Q30 - Prywatność liczniki (wyklad_3.qmd, Slajd 9)
    questions.append(create_question(
        category='Wykład 3 - Bezpieczeństwo IoT',
        qtype='multichoice',
        name='Q30_Prywatność_Liczniki',
        question_text='<p>Co mogą ujawnić inteligentne liczniki energii mierzące zużycie co 10 sekund?</p>',
        answers=[
            ('Kiedy włączasz czajnik, wychodzisz z domu i wracasz - na podstawie pików zużycia', True, 'Poprawnie!'),
            ('Tylko miesięczne zużycie', False, 'Niepoprawnie.'),
            ('Nic, to tylko liczby', False, 'Niepoprawnie.'),
            ('Tylko czy jest prąd', False, 'Niepoprawnie.')
        ],
        feedback='<p>Analiza pików zużycia energii pozwala określić harmonogram dnia mieszkańców - kiedy wstają, wychodzą, gotują. To poważne wyzwanie dla prywatności.</p>',
        source_ref=SOURCE_REFERENCES['Q30_Prywatność_Liczniki']
    ))
    
    # ==================== WYKŁAD INTRO 1: Zastosowania IoT ====================
    
    # Q31 - Rolnictwo IoT (wyklad_intro_1.qmd, Slajd 4)
    questions.append(create_question(
        category='Wykład Intro - Zastosowania IoT',
        qtype='multichoice',
        name='Q31_Rolnictwo_IoT',
        question_text='<p>Co to jest Tree-Talker w rolnictwie precyzyjnym?</p>',
        answers=[
            ('Autonomiczne opaski przybijane do pni drzew analizujące przepływ soków i absorpcję światła', True, 'Poprawnie!'),
            ('Nowy ciągnik', False, 'Niepoprawnie.'),
            ('Oprogramowanie do fakturowania', False, 'Niepoprawnie.'),
            ('Nawóz sztuczny', False, 'Niepoprawnie.')
        ],
        feedback='<p>Tree-Talker to autonomiczny sensor montowany na pniach drzew, mierzący przepływ soków (Xylem sap flow), absorpcję światła i wibracje korony. Zasilany panelem fotowoltaicznym.</p>',
        source_ref=SOURCE_REFERENCES['Q31_Rolnictwo_IoT']
    ))
    
    # Q32 - Wearables medycyna (wyklad_intro_1.qmd, Slajd 5)
    questions.append(create_question(
        category='Wykład Intro - Zastosowania IoT',
        qtype='multichoice',
        name='Q32_Wearables_Medycyna',
        question_text='<p>Co mierzy pierścionek Oura Ring?</p>',
        answers=[
            ('Zmienność rytmu zatokowego (HRV) i nasycenie tlenem 24h/7', True, 'Poprawnie!'),
            ('Tylko kroki', False, 'Niepoprawnie.'),
            ('Tylko sen', False, 'Niepoprawnie.'),
            ('Tylko tętno w spoczynku', False, 'Niepoprawnie.')
        ],
        feedback='<p>Oura Ring to zaawansowany wearable mierzący HRV, SpO2, wzorce snu i aktywności. Buduje bazę danych pozwalającą wyprzedzać diagnozy spadku samopoczucia.</p>',
        source_ref=SOURCE_REFERENCES['Q32_Wearables_Medycyna']
    ))
    
    # Q33 - Predictive przemysł (wyklad_intro_1.qmd, Slajd 7)
    questions.append(create_question(
        category='Wykład Intro - Zastosowania IoT',
        qtype='multichoice',
        name='Q33_Predictive_Przemysl',
        question_text='<p>Co mogą wykryć czujniki wibracji na robotach chwytnych w fabryce?</p>',
        answers=[
            ('Zatarte łożyska jeszcze przed pęknięciem', True, 'Poprawnie!'),
            ('Kolor produktu', False, 'Niepoprawnie.'),
            ('Wagę produktu', False, 'Niepoprawnie.'),
            ('Temperaturę hali', False, 'Niepoprawnie.')
        ],
        feedback='<p>Predictive Maintenance w Przemyśle 4.0 używa czujników wibracji do wykrywania wczesnych oznak zużycia łożysk, minimalizując przestoje taśm produkcyjnych.</p>',
        source_ref=SOURCE_REFERENCES['Q33_Predictive_Przemysl']
    ))
    
    # Q34 - Generacja 4.0 (wyklad_intro_1.qmd, Slajd 9)
    questions.append(create_question(
        category='Wykład Intro - Zastosowania IoT',
        qtype='multichoice',
        name='Q34_Generacja_4',
        question_text='<p>Co charakteryzuje Generację 4.0 w rolnictwie/przemyśle?</p>',
        answers=[
            ('Wykorzystanie IoT na brzegu sieci do zbioru danych i napędzania algorytmów ML/AI', True, 'Poprawnie!'),
            ('Praca ręczna', False, 'Niepoprawnie. To Generacja 1.0.'),
            ('Maszyny mechaniczne na ropę', False, 'Niepoprawnie. To Generacja 2.0.'),
            ('Komputery i Excel', False, 'Niepoprawnie. To Generacja 3.0.')
        ],
        feedback='<p>Generacja 4.0 to połączenie IoT (zbiór danych z czujników) z AI/ML (analiza i predykcja). System staje się reagujący na warunki środowiska i rozmawia "językiem naturalnym".</p>',
        source_ref=SOURCE_REFERENCES['Q34_Generacja_4']
    ))
    
    # ==================== WYKŁAD INTRO 2: Zagrożenia i Przyszłość ====================
    
    # Q35 - Cambridge Analytica (wyklad_intro_2.qmd, Slajd 1)
    questions.append(create_question(
        category='Wykład Intro 2 - Zagrożenia',
        qtype='multichoice',
        name='Q35_Cambridge_Analytica',
        question_text='<p>Do czego wykorzystano dane z Facebooka w aferze Cambridge Analytica?</p>',
        answers=[
            ('Do mikro-targetowania i wpływania na demokratyczne wybory', True, 'Poprawnie!'),
            ('Do sprzedaży produktów', False, 'Niepoprawnie.'),
            ('Do badań naukowych', False, 'Niepoprawnie.'),
            ('Do poprawy algorytmów', False, 'Niepoprawnie.')
        ],
        feedback='<p>Cambridge Analytica użyła danych Facebooka do tworzenia profili psychologicznych i mikro-targetowania reklam politycznych, wpływając na wyniki wyborów.</p>',
        source_ref=SOURCE_REFERENCES['Q35_Cambridge_Analytica']
    ))
    
    # Q36 - Chiński system (wyklad_intro_2.qmd, Slajd 1)
    questions.append(create_question(
        category='Wykład Intro 2 - Zagrożenia',
        qtype='multichoice',
        name='Q36_Chinski_System',
        question_text='<p>Co to jest Chiński System Kredytu Społecznego?</p>',
        answers=[
            ('System automatycznej weryfikacji i nadzoru obywateli na podstawie ich zachowań', True, 'Poprawnie!'),
            ('System bankowy', False, 'Niepoprawnie.'),
            ('System podatkowy', False, 'Niepoprawnie.'),
            ('System ubezpieczeń', False, 'Niepoprawnie.')
        ],
        feedback='<p>Chiński System Kredytu Społecznego to system nadzoru, który klasyfikuje obywateli na podstawie zachowań (np. granie w gry wideo = osoba bezproduktywna).</p>',
        source_ref=SOURCE_REFERENCES['Q36_Chinski_System']
    ))
    
    # Q37 - AI rynek pracy (wyklad_intro_2.qmd, Slajd 2)
    questions.append(create_question(
        category='Wykład Intro 2 - Zagrożenia',
        qtype='multichoice',
        name='Q37_AI_Rynek_Pracy',
        question_text='<p>Jakie ryzyko niesie rewolucja AI według Yuval Noah Harari?</p>',
        answers=[
            ('Wypchnięcie miliardów ludzi z rynku pracy i powstanie "bezużytecznej klasy"', True, 'Poprawnie!'),
            ('Zbyt wiele miejsc pracy', False, 'Niepoprawnie.'),
            ('Spadek cen komputerów', False, 'Niepoprawnie.'),
            ('Brak ryzyka', False, 'Niepoprawnie.')
        ],
        feedback='<p>Harari ostrzega, że AI może stworzyć "bezużyteczną klasę" - miliardy ludzi bez pracy, co doprowadzi do poważnych napięć politycznych i społecznych.</p>',
        source_ref=SOURCE_REFERENCES['Q37_AI_Rynek_Pracy']
    ))
    
    # Q38 - BCI Nicolelis (wyklad_intro_2.qmd, Slajd 6)
    questions.append(create_question(
        category='Wykład Intro 2 - BCI/Energia',
        qtype='multichoice',
        name='Q38_BCI_Nicolelis',
        question_text='<p>Co udowodnił eksperyment Miguela Nicolelisa z szczurami?</p>',
        answers=[
            ('Możliwość przesyłania komend ruchowych między mózgami szczurów przez TCP/IP na odległość kontynentów', True, 'Poprawnie!'),
            ('Że szczury są inteligentne', False, 'Niepoprawnie.'),
            ('Że TCP/IP jest wolny', False, 'Niepoprawnie.'),
            ('Nic nowego', False, 'Niepoprawnie.')
        ],
        feedback='<p>Nicolelis połączył implanty mózgowe dwóch szczurów (USA i Brazylia) przez Internet. Szczur podrzędny uczył się zadań wyłącznie z sygnałów przesyłanych z mózgu pierwszego szczura.</p>',
        source_ref=SOURCE_REFERENCES['Q38_BCI_Nicolelis']
    ))
    
    # Q39 - Koszt energii (wyklad_intro_2.qmd, Slajd 8)
    questions.append(create_question(
        category='Wykład Intro 2 - Energia',
        qtype='multichoice',
        name='Q39_Koszt_Energii',
        question_text='<p>Ile energii dziennie zużywa dorosły człowiek w porównaniu do samochodu?</p>',
        answers=[
            ('~3.5 kWh (2500-3000 kcal) vs auto zużywające 2.5 MJ na kilometr', True, 'Poprawnie!'),
            ('Tyle samo', False, 'Niepoprawnie.'),
            ('Człowiek zużywa więcej', False, 'Niepoprawnie.'),
            ('Samochód nie zużywa energii', False, 'Niepoprawnie.')
        ],
        feedback='<p>Przejechanie 5 km autem zużywa więcej energii niż dobowe zapotrzebowanie całego ludzkiego organizmu. Mózg ludzki działa na ~20W - to ewolucyjny cud efektywności.</p>',
        source_ref=SOURCE_REFERENCES['Q39_Koszt_Energii']
    ))
    
    # Q40 - Literatura Harari (wyklad_intro_2.qmd, Slajd 9)
    questions.append(create_question(
        category='Wykład Intro 2 - Literatura',
        qtype='multichoice',
        name='Q40_Literatura_Harari',
        question_text='<p>Który autor napisał "21 Lekcji na XXI Wiek" i "Homo Deus"?</p>',
        answers=[
            ('Yuval Noah Harari', True, 'Poprawnie!'),
            ('Aldous Huxley', False, 'Niepoprawnie. To "Nowy Wspaniały Świat".'),
            ('Jacek Dukaj', False, 'Niepoprawnie. To "Po słowie".'),
            ('Ramez Naam', False, 'Niepoprawnie. To trylogia Nexus.')
        ],
        feedback='<p>Harari analizuje wpływ technologii na ludzkość. Lektura obowiązkowa dla inżynierów myślących o konsekwencjach swoich projektów.</p>',
        source_ref=SOURCE_REFERENCES['Q40_Literatura_Harari']
    ))
    
    return questions


def write_moodle_xml(questions, output_path):
    """Write questions to Moodle XML format with UTF-8 encoding."""
    root = ET.Element('quiz')
    
    for question in questions:
        root.append(question)
    
    # Create XML string with proper encoding
    xml_str = ET.tostring(root, encoding='unicode')
    
    # Pretty print
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent='  ', encoding=None)  # unicode output
    
    # Remove extra blank lines and fix encoding declaration
    lines = pretty_xml.split('\n')
    # Replace the default declaration with UTF-8
    lines[0] = '<?xml version="1.0" encoding="UTF-8"?>'
    pretty_xml = '\n'.join(line for line in lines if line.strip())
    
    # Write with UTF-8 encoding
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    
    return len(questions)


if __name__ == '__main__':
    # Generate questions
    questions = generate_all_questions()
    
    # Write to XML
    output_file = 'iot_quiz_40_questions_v2.xml'
    count = write_moodle_xml(questions, output_file)
    
    print(f"✅ Wygenerowano {count} pytań testowych")
    print(f"📁 Plik zapisany: {output_file}")
    print(f"🔍 Encoding: UTF-8 (native polskie znaki)")
    print(f"\n📊 Podział pytań:")
    print(f"   - Wykład 1: 10 pytań (Podstawy, Architektura, Platformy, Digital Twins)")
    print(f"   - Wykład 2: 11 pytań (Protokoły komunikacyjne i aplikacyjne)")
    print(f"   - Wykład 3: 9 pytań (Cloud, Smart City, Bezpieczeństwo)")
    print(f"   - Wykład Intro 1: 4 pytania (Zastosowania IoT)")
    print(f"   - Wykład Intro 2: 6 pytań (Zagrożenia, BCI, Energia, Literatura)")
    print(f"\n📝 Każde pytanie zawiera referencję do źródła w kategorii [Źródło: plik.qmd, Slajd X]")
