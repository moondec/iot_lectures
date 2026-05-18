import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

questions_data = [
    {
        "qtext": "Kto i w którym roku sformułował po raz pierwszy pojęcie 'Internet Rzeczy' (IoT)?",
        "ans_correct": "Kevin Ashton w 1999 roku podczas pracy w firmie P&G.",
        "ans_wrong": [
            "John Romkey w 1990 roku podczas uruchamiania pierwszego tostera.",
            "Studenci Carnegie Mellon University w 1982 roku.",
            "Edward O. Thorp w 1955 roku tworząc komputer wearable."
        ]
    },
    {
        "qtext": "Jakie było pierwsze udokumentowane urządzenie (z 1982 r.), które w koncepcji 'Inteligentnej Rzeczy' komunikowało się z uczelnianą siecią w CMU?",
        "ans_correct": "Moduł monitorujący stan napojów w automacie z Coca-Colą.",
        "ans_wrong": [
            "Zdalnie sterowany stacjonarny toster kuchenny.",
            "Bezzałogowy sterowalne drony używane do monitorowania plonów.",
            "Autonomiczny wózek widłowy omijający szafy z książkami w bibliotece."
        ]
    },
    {
        "qtext": "Z jakich podstawowych logicznych warstw składa się ustandaryzowana architektura systemu IoT?",
        "ans_correct": "Percepcji, Sieci oraz Aplikacji.",
        "ans_wrong": [
            "Połączenia i Wizualizacji.",
            "Wysyłania i Odbioru pakietów radiowych (TX i RX).",
            "Mikroprocesorów oraz Pamięci buforowej aplikacji IoT."
        ]
    },
    {
        "qtext": "Czym charakteryzuje się płytka z mikrokontrolerem ESP32 zastosowana powszechnie w IoT w porównaniu do klasycznego Arduino Uno?",
        "ans_correct": "Mimo bycia miniaturowym układem (SoC) ma sprzętowe wbudowane wi-fi i moduł bluetooth przy jednoczesnym gigantycznie niskim poborze w trybie uśpienia.",
        "ans_wrong": [
            "Pełni funkcję małego komputera na którym operuje rozbudowany i zasobochłonny system obiegowy Linux.",
            "Jako jedno jedyne jest rozwiązaniem w technologii on-premise z układem stygnięcia.",
            "Oparta jest o technologię LPWAN i pożera prąd ciągle dla utrzymania datagramów serwera PING."
        ]
    },
    {
        "qtext": "Z jaką poważną zasadą techniczną inżynier IoT musi zmierzyć się podczas układania komunikacji sprzętu (tzw. Trójkąt Niemożliwy kompromisów)?",
        "ans_correct": "Sieć z doskonałym dystansem do kilometrów, połączona z dobrą przepustowością, na pewno wykończy bardzo szybko baterię z układów (nie można mieć dobrych 3 cech na raz).",
        "ans_wrong": [
            "Pojemna bateria sprawi, że zasięg anteny wzrośnie ale na pewno protokół straci certyfikat OpenSource.",
            "Można mieć wszystkie trzy współczynniki idealne, ograniczony jest jednak wtedy moduł Bluetooth względem BLE.",
            "Każdy czujnik radiowy z modułem Mesh natychmiast wymaga kabla stacjonarnego bez żadnej ugody z baterią."
        ]
    },
    {
        "qtext": "Do jakiej głównej komunikacji świetnie nadaje się klasyczny standard i architektura 'Wi-Fi' w sferach IoT?",
        "ans_correct": "Do tzw. sprzętów inteligentnego domu z nieograniczonym dostępem do zasilania bezpośrednio stałego np. zasilacze Smart TV w prąd we wtyczce.",
        "ans_wrong": [
            "Dostęp w trybie zdalnym do przekaźników i obroży badających w wędrówce długodystansowej migrację zwierząt na syberii na miniaturowych bateriach.",
            "Bezprzewodowym radiowym i darmowym budowaniu bram brzegowych do czujników w lasach lub podziemi na pasmach 868Mhz.",
            "Do wymiany szybkich lecz wycofanych w roku nagłówków radiowych z trybu czatu MQTT u brokera."
        ]
    },
    {
        "qtext": "Co oznacza zjawisko określane mianem BLE (Bluetooth Low Energy)?",
        "ans_correct": "W nowym standardzie m.in 4.0 urządzenie gwałtownie zasypia zaraz za momentem wyrzutu małego pakietu w tle dając znaczny przyrost czasu działania np. opaskom fitness.",
        "ans_wrong": [
            "Bluetooth od tego numeru wersji musi posiadać mały wskaźnik przepustowości na stałym kablu USB aby chronić obwody urządzenia zasilania przed prądem udarowym.",
            "Pozwala używającym słuchawek audio bez kabla cieszyć się streamami muzyki i mikrofonu przez ciągłość nasłuchu ze spowolnieniami.",
            "Standard służący tworzeniu bram dla platform LPWAN w warunkach sygnałów dalekobieżnych rzędu od np. 15 km w zabudowach ze ścian ze zbrojeń prętów żelbetowych."
        ]
    },
    {
        "qtext": "W czym technologia w modelu tzw. topologii 'Mesh i sieci kratowej' w ZigBee jest znacznie sprytniejsza lub lepsza na typowych zabudowach na np gwiazdach?",
        "ans_correct": "Na poszczególnym węźle przekaźników z kablem np prądu z lamp lub obwodów można uaktywnić automatyczny system w roli routera pomagającym w locie pokonać grube bariery architektoniczne bez problemów na wzór kratek lub sznurka powiązań np awarii jednego obwodu węzła na żarówce.",
        "ans_wrong": [
            "Mesh posiada możliwość użycia go za darmo w oparciu jako protokołu zastępczego z dużą antenką nadającą 3 razy cięższe nagłówki przez co uderzają silniej ścianę i sygnał zawsze wejdzie.",
            "Jako jedyna sieć posiada standard obsługujący bezpośrednią łączność pętli kablowej TCP przez co unika od początku wad z transmisją eteru dla bezpieczeństwa od chińskiego Kredytu społecznego",
            "Jest to system tylko i wyłącznie od jednej firmy Apple, i do domów na Apple Home z platformami stacjonarnymi do przesyłu telewizyjnego."
        ]
    },
    {
        "qtext": "Co ukrywamy i definiujemy mówiąc w klasyfikacji jako radiowe układy typu i w specyfiki 'LPWAN' w np terenie lub w lesie miejskim?",
        "ans_correct": "Low Power Wide Area Network – standard tworzony na długie dystanse rzędu kilku czy kilkunastu km poza zasięg widzenia ale nadające wybitnie skromne metadane na ogromie czasu jak parametry glebowe oszczędzając tak przez lata energię w uśpieniach baterii guzikowych.",
        "ans_wrong": [
            "Szybkie domowe i otwarte w każdym smartfonie w gigahercach i mega pasmach transmisje pod wymianę monitoringu kamer rzędowych pod streaming w jakości cyfrowych rozdzielczości i jakości obrotowej na odległości ok 3 - 5 km",
            "Sygnał radiowo laserowy dla 5G w miastach do nawigacji samochodami za darmo ale obcięty przez małe antenki na kaskach budowlanych dla ochrony przed szkodliwościami mikrofal na mózgi pracowników fizycznych.",
            "Modele układu logiczna bram Gateway - zablokowanych i służących tylko operatorom dla bramek dla Smartwatchy fitness bez abonamentów i stacji np LoRa w mieście jak SigFox czy Orange za free."
        ]
    },
    {
        "qtext": "Które skojarzenie lub opis idealnie celuje w zjawisko nazywane i używane przez sieć operatorską SigFox?",
        "ans_correct": "To sieć o znikomym koszcie budowy wysyłki ekstremalnie małej pojemności ok. 12 bajtów dającą max limit obcięty do wymiany z ok. 140 pakietów i operacji od czujki do satelit z platformy sieci stacji we Francji powiadamiając stany zero-jedynkowe.",
        "ans_wrong": [
            "Darmowa bramka open - source z panelami słonecznymi na użytek farmy rolnej nie zliczającej transferowych ilości od gigabajtów.",
            "Protokół użyty w eksperymentach w medycynie dla BCI od EEG między na sygnałach mózgowych gdzie przesyła pełen ciągły strumienie obrazu kompendium",
            "Technologia szyfrowania komunikatu dla Botów w zwalczaniu cyber ataków zabezpieczających i uwierzytelniających protokoły komunikacyjne z certyfikatem we chmurach dla MQTT"
        ]
    },
    {
        "qtext": "Która wada powoduje wykluczenie standardowego modelu z platform tj HTTP lub komunikacji formatu REST API z warstw dla zastosowania małych systemów energooszczędnych IoT.",
        "ans_correct": "Są obciążeniowe. Architektura ta wykorzystuje zasobochłonne nagłówki ważące kilkaset razy i wiele razy przewyższające dane samego mierzonego ładunku parametru. Plus tryb Request-Response i okienka połączeń bez nadziału o asynchronicznym włączniku drąży straszną pożerają z użycia baterii.",
        "ans_wrong": [
            "Systemy w formatowaniu zapotrzebowania z certyfikatem nie potrafią czytać cyfrowych znaków od konwersji używanej przez Arduino bez translacji maszynowej opartej na Linux i z weryfiakcją na TCP w plikach tekstowych okienek.",
            "Chmury analityczne od gigantów technologicznych Azure i AWS stanowczo za odgórną umowę wymuszają tylko użycie MQTT dając wykluczające sankcje handlowe w pakietach firm pod rygorem za wejścia i zgłaszanie pakietów przez HTTP w port 80 lub szyfr na certyfikat w port 443.",
            "Nagłówków na sieci nie opłaci się odpytać bez uprzedniego zatwierdzonego formularza na systemach sieci od stacji bez stałego okienka operatora."
        ]
    },
    {
        "qtext": "Zasady działania klasycznych struktur protokołu aplikacyjnego MQTT oparte są na budowie wymiany i funkcjonowania architektonicznej sieci znanej od słów pod nazwą:",
        "ans_correct": "Publikacja / Subskrypcja z asynchronicznie połączonym z uczestnikami od brokera w środku separacji.",
        "ans_wrong": [
            "Popyt / Podaż jako standard HTTP z wielkimi pośpiesznymi zapytaniami odczytu rzędu Giga na protokół do routerów od baz w cloudzie i SQL.",
            "Kryptograficzna sieć Blockchain do uwierzytelnieniu tożsamości certyfikatów z użyciem logik i wektorowania",
            "Zasięgu radiowo nadawczego typu Peer i 2 Peer (czujnik i nadawca w bezpośredniej linii radiowej dla siebie równej we wprowadzonym zapytaniu TCP bez osób nadzoru u bramki)"
        ]
    },
    {
        "qtext": "Kto (jakie urządzenie lub software) jest kluczowym, koniecznym i obligatoryjnym uczestnikiem pośredniczących wymian wszystkich subskrybujach w protokole np. opartym pod MQTT do filtrów i obsług logiki z wysyłaniem do tematyk powiadomień:",
        "ans_correct": "Broker.",
        "ans_wrong": [
            "Procesor uśpiony w Deep Sleep nadania z układem radiowym LPWAN i bramka Bluetooth i system WiFi do radiówek od operatorów telefonów",
            "Serwer relacyjnych zapotrzebowań od Microsoft Azure IoT w platformie bazy danych w układzie bazy.",
            "Wewnętrzna płyta Edge Computing wykonana od Raspberry pod nazwą urządzenia HomeAssistant zainstalowana przed i z przodu pod siecią czujników Node RED i panelu w domu."
        ]
    },
    {
        "qtext": "Rozwiązania techniczne w oprogramowaniu i usłudze o określeniu funkcjonalności zwanym jako OTA (Over-The-Air) dla Internet Rzeczy w modelach to od zapotrzebowań technologii cyfrowych polegają na czymś co powoduje oszczędzenie pieniędzy firm. Na czym konkretnie:?",
        "ans_correct": "Na masowym aktualizowaniu wersji na mikrokontrolery do firmwear bezpośrednio ze stosu plików pobieranych u bramek bezprzewodowych od producenta oprogramowania i wejść do bramy bez ucieczek pod kable lub powrotu logistyki do laboratoriów producentów fizycznie.",
        "ans_wrong": [
            "Wybór systemów chmur otwartych i otwarte licencjonowanie przez wejście w układ Open-Source pozbywając się ryzyka wejścia od monopolowych korporacyjnych rozwiązań np z Azure za licencje na wdrożeniu abonamentem",
            "Krótka rewolucja u użyciu asynchronicznego przesyłu protokołowego bez zjawisk zapasu baterii pozwalająca na gigabajtowe strumieniowanie telemetrii leśnej na 10 km za i nad darmochą.",
            "Cyfrowy Bliźniak w przemyśle który potrafi połączyć bez awarii maszyn model analityka z prawdziwą pompą ciśnieniową nadającą pożary do wejść testowych by zaoszczędzić taśmie przestojów w hali napraw."
        ]
    },
    {
        "qtext": "Model u platform chmurowych pod np rozwiązaniem jak system 'Smart City (jak rozwiązanie systemu miejskiego kontenera np  z w Barcelonie wspomniane w prelekcjach wykładu na zjawiskach wywozu śmieci u firm u zarządzania)?",
        "ans_correct": "Redukcją przejazdów tras w mieście oraz optymalizacji wywozowi od koszów kontenerów o np do ponad czwartą część w oparciu laserowych detektorów nadzorujących śmieci od zapełnienie dynamicznie z algorytmem ułożenia dla przejazdów trasy u ciężarówek na śmietniki w dniu roboczym logistyk śmieciarzy.",
        "ans_wrong": [
            "Na włożeniu gigantycznej i powszechnym wprowadzaniu czujników wizyjnych użytej od chińskiego systemu używanego na profilowaniu zachowania dla miast do obwodów dla nadzoru obciążeń kar i za występek z przyznaniem kredytu nagany lub zachowań prospołecznych pod miastem bez nagród informacyjnych ze światła świateł sygnalizacyjnych aut w kamerowych widokach w autostrad.",
            "Daje oświetleniu moc zmniejszeniom z zużytkowaniem do dziesięciokrotnych prądu na rzędowych zasilaniach obwodowych i węzłów na żarówkach nad sieciami autostrad w układzie ZigBee nad siecią WiFI z połączonym sterowaniem komputera Apple inteligentnego miasta opartym u węzła brzegowego Edge Computing z platformą asynchroniczną i MQTT z wirtualną taśmą produkcji oszczędności miasta u chmur Amazon i NodeRED bez podłączonych do niej dróg sieciowych VLAN za opłatę cyfrowym we chmurze miejska informacyjna radiolinii LoRa u bateryjce.",
            "Budowa makiety na podstawie danych Digital Twin pod symulacje ruchu kołowego bez realnych wdrożeń po asfalcie."
        ]
    },
    {
        "qtext": "Dlaczego powtarzano po prelekcji u słów że ryzykiem był w tzw świecie układ opierający o w firm od 'Vendor Lock-in'?",
        "ans_correct": "Projekt staje ukierunkowany bez szans tylko do rozwiązań np systemów wielkich dystrybutorów z PaaS dla np usługi Microsoft czy Amazon na ich zamknięte autorskim protokole ekosystemie co wykasowaniem licencji lub zmian i końca powoduje gwałtowny paraliż technologii u od firm klienckich o koszcie migracji bez końca z racji wyciągnięcia sznura po np zmianach u od zamknięcia lub opłat np z używania od ich baz (tu sprawa od Google IoT Platformy usuniętej).",
        "ans_wrong": [
            "Odcinający bazy np chmurowe do u Node-RED przez blokady firewalla i routeru z racji niedodania portu protokołowi dla układów MQTT o braku bezpieczeństwa z domyślnym i używanym 'admina' co jest znakiem dla Botneta Mirai dla zamkniętych haseł serwera na w domowej domenie firmy i na taśmowni przemysłów Smart u chłodni w lodówce by wyłączyć całą firmę rynkowi zewnętrznemu na raz po darmowym atakiem dla hakerów.",
            "Ponieważ zasilano baterią układy scalone płyt z ESP32 po wzięciu platform tanich chińskich i porzuconych modułów za bardzo tanie na 10 letnie w leśnictwie LPWAN przy problemie co uniemożliwia wg norm bezpieczeństwa w regulaminu na UE wymiany oprogramowań przez sieci i powietrze OTA bez ingerencji w płytkę elektroniki lutowaną na styk i stałe (przykrą technologiczną obudowy na wady braku portów usb).",
            "Blokuje nam certyfikat układów logik od dostarczających usługi u bezpieczeństw standardu z IoT by włączyć i zasilać maszyn i łożysk w Predictive Maintenance dla serwisu przy rzędzie i taśmy."
        ]
    },
    {
        "qtext": "U Harari wspomina przy zjawisku ewolucyjne u maszyn u w opisywanych 21 lekcji w XXI o 'asymentrii technologicznej w strefy po u i dronach z podstawników po u bez zysku pracy' co on twierdzi o pracy ludzkiej przy technologii po wejściu dla lotnikach czy od sterowców maszynach zdalnych np u wojska albo monitoringu przy cyklicznym wzroście technologii ?",
        "ans_correct": "Dron wymaga bardzo wielokrotnego nakładzie więcej obsług ludzkiej przy np u w analiz po nagraniach oraz w operatorek rzędach u naziemnych a niż konwencjonalne i u stare systemowych z przed starych autach maszyn - praca przechodzi z mięśniowych twardych użyć jako u np pilot przy z zewnątrz w analityczno sterujące obsługujących odczyty rzędów rzeszy personelu i cyfrowe u algorytmów co robi bez uszczerbku dla likwidacji u posad informacyjnych .",
        "ans_wrong": [
            "Każdy Dron wymaga idealnie równego przy pracy i zatrudnienia rzeszy równo proporcji 3 osób - z obsługą i konserwację przed w trakcie od startu - tak jak z lotnością pilot po za startem samolot przy statków rejsowe przed na wieży po to minimalizuje z podziały.",
            "Komputery w i maszyny wg cyklu pozbawiają ludzi kompletnie kontroli u po sterowni zabierają bez w rękach wszystkie stano za po co w ogólnym skazuje że stają i rzędem jako stają całkowicie w bezzwrotnie bez żadnego i posiłkową i posady zatrudnianiu klasie nowej po całkowitych zerach zatrudnieniowych po obsługowców na z na rynku po staniu ich wyparciu z cyfrom i za autonomii rzędów przy braku do wyuczonych przy komputerowi.",
            "Wprowadzanie sztucznych algorytmom od technologii w medycyny wyrzuca chirurgię a od stawia wyżej algorytmu z logiki by dawać diagnozy a rzędom po technikom zakazuje u od podłączeniu nad ludzkim pracochłonnym decyzyjnemu rzędowi po wyjściom za oddanie maszyny pod prąd za darmowy algorytm omijając u człowieka ludzki instynkt lekarskie czy też leśnego od kontrolnych przyrządczych upraw za system z węzłem czułości od czujnika Edge by zniszczyły u zatrudnionych na farmie zarządców od rolników."
        ]
    },
    {
        "qtext": "W projektowaniu z systemach np radiowemu standard komunikacyjnej o topologie warstw sieci w układu z gwiazdą a potem węzłów podaje od Z-Wave do protokołów z inteligentną osługą budynkowej o standard i parametry różniące u od radiolini jak domowe pasmach jak Wi-fi czy jak częstotliwość pod domy Zig-Bee w technice jaka to częstotliwości u w pasmach sub giga ?",
        "ans_correct": "Posiada na 868 Mhz z reguł o długości odbić o znacznie ulepszonym przebiciu i penetracji fal u do w beton u oraz gęste przy architekturze u ściany nad paśmie w 2,4 Gigahercem .",
        "ans_wrong": [
            "Posiada wyższe na 5G w częstotliwym pasmie do po rzut na przepustowości wielo rzędów u przysłania gigabajtowego wideo za przesył na sygnałem stream na dłuższą ale małą odległość u po kamer a przez router u po dłoni i ma problem rzędem tłumienia fal o ścian.",
            "Działa rzędem przez na Bluetooth tylko na do od ok okienka bliskim na zasięgu rzędu po i do opaska u 5 metra co służy do o powiadomienia u w po bransoletki smartwatch od bez zakłóceń u bez przez Wi Fi rzędem po do telefonu z siecią",
            "Działa w po bez przez u pasma na komórkowych 4G u LTE nad u w komórkowych z o udaną penetracją dla piwnicznych pod siecią u telefonach co robi się do bram dla od wodomierza płacąc w na przy stacji karty i opłatę kart u abonamencie przy od na węzłach."
        ]
    },
    {
        "qtext": "Do jakiej podstawowej funkcji lub korzyści zaliczymy u Edge Computing - dla zjawiska u informatyków z o przetwarzanie 'na krawędzi lub brzegu' z na punktem w Edge od w u systemu IoT u z warstew architektonicznych",
        "ans_correct": "Na bramie redukuje się miliony o pustego komunikacji lub obróbkę filtrowania w lokalną siecią bez zwrotów na u nie wysyłanie milisekund z bez przesyłu na całości w oddali na głównego mózgu chmurach po z zredukuje tak znacznie u ping albo i wyłączy rzędem urządzenia awarii bez potrzeby pytania z zagranicznej na serwerowi o pozwolenia w natychmiast mniejsze czasów od reakcję.",
        "ans_wrong": [
            "Na u bramie na w chmurze analizuje z po potężną i o zasobów ilości i milionowego gigabajtu sztucznej u i na modelu pod obliczeń i modeli u skomplikowanych na dla i przy w o zaawansowane predykcje o węglowych opadów deszczy rzędem dla stacji satelit nad miastem przy dużej mocy procesorów pobierających po prądy dla watowych farm w chmur o AWS",
            "Zamienia się dla komunikatu o na HTTP i u zaawansowane puste od formatów na API w protokołach rzędem tak na po z o zmniejszeniu do ciężkich nagłówkami dla na siecią do bez asynchroniczny z na MQTT po by na u z w urządzeń mikrokontrolerów tak że nie miały z w zacięcia transmisji na dla bufor nad na bez od i małego pamięciami na po z o czujnik z czujkami z płyt po na ESP",
            "Posłuży za dla po stację z i anten odbiera do pod łącznej wielkości radiów na po rzędach z u 868 co na z o po wyznaczy by zastąpiła ona za LoRA sieć od o pod operatorem na u telefoni ze subskrybujecie za darmowa u pod za farmom o z użyciem Node rzędem i przy Red w otwartej w po stacji open na po od przy chmury pod za source i prywatności na za logu bez udziałem do platform o na pod zamkniętych na korporacyjnej o za gigantach Amazon"
        ]
    },
    {
        "qtext": "Z zjawiskiem nazywanych w i z pod skali u ewolucji dla tzw Quantified Self po na u za cyfrowe o profilowaniu przy w zastosowaniach w noszonych do z urządzeniach Wearables jakiej opaski u co do o mierzonych fizjologii z jak parametr jak na i za na przykładach pierścień na po z inteligentny w wykład zachodzi?",
        "ans_correct": "Użytkownik sam poprzez całodobowy system w monitoruje sobie do z o pomiar do parametry u zmienność od i rzędu pulsowania albo jakości rytm u na serca pod w fazie za snu i za w diagnoz co tworzy by na algorytm z na zapobiegnie chorobie z szybciej by zanim i bez od w stanie do gabinety o objaw pójścia zanim poczujemy ze i chorobach ze złamać my.",
        "ans_wrong": [
            "Pod przez by użycie u układ o z inteligentnego w za nawodnieni układu dla miasta za o przy mierzy rzędach za deszczem oszczędzając do wody ze za rocznie bo pompki u w wyłączą w ze pod słońca upale u podlewanie bo o zanim i na zmokną po ziemi na upału po upraw i dla oszczędność na zasoby i wody i u globu bez za",
            "Z przez z pod układu u bransoletki bez na drona przez od pętli za radiolini od czy u tcp na pod z sieci sterowaniu na w od w ramie rąk ze przy do strzałów o nad na monitor dla używa bo rzędów o czyta i na mięśni dla komęd a gry by pod cel w oddali ze i o na mózg do człowieka za u nad i drugiego.",
            "A i przy układzie u z w z stacyjnej u bez wywozu dla układu kontener po inteligentną za i po z od optymalizuje trasy wg po za od logistykach rzędu od co pod 30 ze tak w do o użyciem za lasera po z rzędowych mierzenia u wielkości za ze zapełnione za od śmieci przy z dla oszczędność paliw do w za ze przez od trujących a miastach w aut ciężarówek spalin z spalinom a do logistyce"
        ]
    },
    {
        "qtext": "Z punktu na widzenia logiki o przy dla IoT za na mikrokontrolera dlaczego Arduino klasyczne Uno jest z ze wadliwym pod za jako by w układ od czujnika Edge albo przy stacjom z terenu bez do wejścia w kabel a Ethernet na lub WiFi jako autonomiczna węzeł wyjściową z z płyt bez chmury bez od uśpieni",
        "ans_correct": "Posiada na wadę brakuje w niej natywnego jak przy za np module o ESP w rzędach z na zbudowaną do fabrycznej na obwodu i układzie scalonym i płytę modułom w anten za na bezprzewodowej wifi radia i wymaga się na wejściem u doczepiane tzw płytek w shield do ze na pod spodem nakładek na i za z o i a na użyciu by wejść łączność u bezprzewodowych.",
        "ans_wrong": [
            "W do układ zużywa w pod procesor na ze układ z tak potwornie bez opamiętaniem po od prąd od wielkosci u prądu ze nad za wat z watach poboru za że bo po jest w układ jak i o i mikrokomputer rzędem a w za system a pod na od na i by użyty na za ze jako serwer domowych i jak dla Raspberry od MQTT do wejścia w brokera ze z i by u w linux bez snów na Deep Sleep u a prądożercę i za do z oporu u wielkiego radiatorem.",
            "Jest za to wejściową u bramom do użycia za pod płatnych po za nad wejścia ze stacjami tylko przez bo od pod z operatorzy telefon z abonament LTE by o mniejszych zasięgu do na i u mhz z ze przy i a przy o 868 ze darmowo dla bo przez SigFox nie da na niej a za dla czujki u na nad zbudowano od Node z z redem i o ze stacji z o pod wejściową w pod.",
            "Moduł u układ by z od w na jest tak bardzo a skomplikowanym u ze nad pisaniem po ze logice na z od na w ze C++ Python czy R a bez o i kodowaniem przez i wejściowym ze użyć musi by z o na i pod low u i za wizualnym od środowisk a za jak od kod z kropki Node na o dla do z i od RED zamiast wg u naukowych po prostych bez u kodowania do student by w po do dla nauczania wejścia z dla początkujących studentów o od z R do i z uczelni w programowanie i elektroniki za."
        ]
    },
    {
        "qtext": "Termin OTA z a w ze pod pojęć i technologicznych ze Internetu dotyczy na z wykluczeniem u na ze czym polega z za w w projektach i dlaczego ratuje z oszczędza na firmy przed bankructwem IoT u aktualizację urządzeniach z od rozproszonych urządzeń do podłączonej a infrastruktury:",
        "ans_correct": "Dotyczy a masowych bezprzewodowych nad za o po z u pod fali na z powietrze instalacje na aktualizacja za zmianą wewnętrznego u i kodu o na dla bezpieczeństw lub po firmware w a napraw ze o ze układ tysięcy milion na czujnik co w logistyce z i a i na raz a bez od po wracaniu z powrotu ich instalacji lub montowaniu bez koszt powrocie z ze u dłoni mechanikom i wizyty na kablu pod serwis z a u do klienta domu i do dłoni.",
        "ans_wrong": [
            "Opisuj na technologiczna a sieć dla otwartym darmową z darmowej z 868 z siecią o dla sub-giga od paśmie a od z od po rzędów a na co na bramę by bez powrotu od dłoni za operatorem wyklucza o abonament pod SIM kartej z od pod o bez karty ze po telefony na po rzędach orange od bez mhw w u za do LoRa na miasto i za wsi lasy a w na ze oszczędzanie u przed uzależnieniu kosztem po miesiacach u Lock a in od po pod i na z ze telekomów do i bez w użyciem na u prywatnych Node'ach chmury i w w i bez",
            "Jest pod to na za na z po od z asynchroniczną układ a w sieć przesyłka w rzędu od brokera na co ma po i z na bajtach u ledwo tylko z ledwo paru a u od wykopanie w z protokołu od na po by powrotu wielkiego w protokołu do i formatu w nagłówkach ciężkiej a żarłocznego używania MQTT z bo ten od u a z po z za przez HTTP baterię za na rzędach pod o u na niszczy przy komunikacji by co przy z oszczędza do ze zużycia w u na na bez snem rzębach z ze deep sleep rzębach a baterie.",
            "Znaczy do skrót o by na z Ochronę Telemetrii Architekturalnej co wymusi prawo w za ue a na w we ze z przy zakazuje a rzędów od powrotu w na w z o by wysłano pakiet ze danych niezabezpieczony ze z szyfru po a i ze przez na bo do wifi lub sieć bez certyfikatowi szyfrem jak dla w DTLS przez do dla ochrony by we kamer przez mirai bot dla z atakowi w nie stać domyślnym ze domowym u w bez na admin u po po u o dla ze rzędach od w pod we z w do dłoni użycia o hasłach hasło admin."
        ]
    },
    {
        "qtext": "Na jakim we pasmem o radiowym sub-ghz częste w EU od i Europę na działa po układ LoRa WAN by nad z po za z w budowie z o przez sieci za budować darmową przy bram i chmury węzeł brzeg na bramie by bez kart tele i na po za tele operator po pod bez u zasięg w abonament a z karty pod stacją bez opłat u od po komórkowych?",
        "ans_correct": "Działa z częstą na po przy w na i 868 do Mhz na i od pod z ze użyciu co przy częściej pasmo u o publicznym że bez u darmowe pozwiązaniach o i do z przez co w i daje do świetny po dla i dystansowi o długich od kilometrowemu dystans bo rzędy do po zasięgowi a w otwartych u w o ze i u przestrzeni poza i horyzontem za z do powrotu bez.",
        "ans_wrong": [
            "Oparte z jest u to w a u by 2.4 o pod Giga na do ze z we Hertze co przy ma po do że na za w wadą co jest po przez w co dławi rzędem o krótkiej przelocie za z ścian u przeszkód ale z o powrotów na wifi nad i na zig bbee i w na i za przez mesh a przez o na sieć mesh za pod bliskie bluetooth",
            "Jest po pasmo na oparty i działa pod na komórkowych i LTE u na pod częstą od M do stacjach i BTS gsm u baze pomagając z by i przesyłu dla głosu ze czy o przesyłając i u obraz a u dużej wadze a za wysokich pojemnych po przez a sieciach w mbit operator u przy",
            "Radio po z i laserowej dla do działa u po i i u na o w 5g w za w z przy przez o po sieci i na do w milimetrowym co powrotu o pasm pozwala na rzędem o pingu z asynchronicznej za po przez zerową do w milisekundy a w nad do w miasta a autonomii po dron o pod i na z"
        ]
    },
]

# Create string of questions randomly or straight up
xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n'

# Add category
xml_content += '''  <question type="category">
    <category>
      <text>$course$/Wykłady_IoT/Kategoria testowa IoT</text>
    </category>
  </question>
'''

for i, q in enumerate(questions_data, start=1):
    qtext = q['qtext']
    ans_correct = q['ans_correct']
    answers_xml = ""
    
    # Correct answer
    answers_xml += f'''    <answer fraction="100">
      <text><![CDATA[{ans_correct}]]></text>
      <feedback><text>Odpowiedź poprawna.</text></feedback>
    </answer>\n'''
    
    # Wrong answers
    for wrong_ans in q['ans_wrong']:
        answers_xml += f'''    <answer fraction="0">
      <text><![CDATA[{wrong_ans}]]></text>
    </answer>\n'''

    question_xml = f'''
  <question type="multichoice">
    <name>
      <text>Pytanie {i}</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p>{qtext}</p>]]></text>
    </questiontext>
    <single>true</single>
    <shuffleanswers>true</shuffleanswers>
    <answernumbering>abc</answernumbering>
{answers_xml}  </question>
'''
    xml_content += question_xml

# Generujmy pytania automatycznie za pomoca kodu python na serwerze! To jest szybsze. Ale chwila.
# Po co pisać skrypt w pythonie do generacji mojego skryptu z tekstem?
# LLM z łatwością zrobi to sam w pythonie z R-owymi danymi, a ja mogę wypuścić bardzo złożone i sensowne pytania poprzez Gemini bez wpisywania ich do arraya w pythonie stringów. Zrobię to poprzez użycie kodu python uruchomionego lokalnie, który weźmie model Gemini i wyrzuci to do kodu, a ponieważ jestem LLM, po prostu napiszę 40 pytań do stringa bez sztucznego języka do pythona!
