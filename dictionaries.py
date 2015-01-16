#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sioQtool, licensed under GNU Affero GPLv3 or later.
# Copyright © Robert Błaut. See NOTICE for more information.
#

specyfika_dict = {
    0: 'brak specyfiki',
    1:	'specjalna',
    100: 'brak specyfiki'
}

kat_ucz_dict = {
    1: ['Dzieci lub młodzież', 'Młodzież'],
    2: ['Dorośli'],
    3: ['Bez kategorii']
}

publ_dict = {
    1: 'publiczna',
    2: 'niepubliczna o uprawnieniach szkoły publicznej',
    3: 'niepubliczna bez uprawnień szkoły publicznej',
    4: 'niepubliczna'
}

type_dict = {
    1: 'Przedszkole',
    3: 'Szkoła podstawowa',
    4: 'Gimnazjum',
    13: 'Zasadnicza szkoła zawodowa',
    14: 'Liceum ogólnokształcące',
    15: 'Liceum profilowane',
    16: 'Technikum',
    17: 'Liceum ogólnokształcące uzupełniające dla absolwentów '
        'zasadniczych szkół zawodowych',
    18: 'Technikum uzupełniające dla absolwentów zasadniczych szkół '
        'zawodowych',
    19: 'Szkoła policealna (ponadgimnazjalna)',
    20: 'Szkoła specjalna przysposabiająca do pracy dla uczniów z '
        'upośledzeniem umysłowym w stopniu umiarkowanym lub znacznym oraz '
        'dla uczniów z  więcej niż jedną niepełnosprawnością',
    21: 'Sześcioletnia ogólnokształcąca szkoła muzyczna I stopnia',
    22: 'Szkoła muzyczna I stopnia',  # changed in NSIO
    23: 'Szkoła muzyczna I stopnia',  # changed in NSIO
    24: 'Sześcioletnia ogólnokształcąca szkoła muzyczna II stopnia',
    25: 'Sześcioletnia szkoła muzyczna II stopnia',
    26: 'Sześcioletnia ogólnokształcąca szkoła sztuk pięknych',
    27: 'Czteroletnie liceum plastyczne',
    29: 'Dziewięcioletnia ogólnokształcąca szkoła baletowa',
    30: 'Sześcioletnia szkoła sztuki tańca',
    31: 'Czteroletnia szkoła sztuki cyrkowej',
    32: 'Policealna szkoła artystyczna',
    33: 'Szkoła pomaturalna bibliotekarska',
    34: 'Kolegium nauczycielskie',
    35: 'Nauczycielskie Kolegium Języków Obcych',
    36: 'Ośrodek politechniczny',
    37: 'Pałac młodzieży',
    38: 'Młodzieżowy dom kultury',
    39: 'Ognisko pracy pozaszkolnej',
    40: 'Międzyszkolny ośrodek sportowy',
    41: 'Ogród jordanowski',
    42: 'Pozaszkolna placówka specjalistyczna',
    43: 'Szkolne schronisko młodzieżowe',
    44: 'Placówki artystyczne (ognisko artystyczne)',
    45: 'Centrum Kształcenia Praktycznego',
    46: 'Centrum Kształcenia Ustawicznego ze szkołami',
    47: 'Ośrodek dokształcania i doskonalenia zawodowego',
    48: 'Poradnia psychologiczno-pedagogiczna',
    49: 'Poradnia specjalistyczna',
    50: 'Specjalny Ośrodek Wychowawczy',
    51: 'Specjalny Ośrodek Szkolno-Wychowawczy',
    52: 'Ośrodek Rewalidacyjno-Wychowawczy umożliwiający upośledzonym umysłowo'
        ' realizację obowiązku szkolnego i nauki',
    53: 'Młodzieżowy Ośrodek Wychowawczy',
    54: 'Młodzieżowy Ośrodek Socjoterapii ze szkołami',
    55: 'Bursa',
    56: 'Dom wczasów dziecięcych',
    57: 'Placówka doskonalenia nauczycieli',
    58: 'Biblioteki pedagogiczne',
    59: 'Publiczna placówka opiekuńczo-wychowawcza w systemie pomocy '
        'społecznej',
    60: 'Zakład poprawczy',
    61: 'Schronisko dla nieletnich',
    62: 'Rodzinny ośrodek diagnostyczno-konsultacyjny',
    63: 'Publiczny ośrodek adopcyjno-opiekuńczy',
    64: 'Niepubliczna placówka oświatowo-wychowawcza w systemie oświaty',
    65: 'Kolegium Pracowników Służb Społecznych',
    66: 'Szkoła pomaturalna animatorów kultury',
    67: 'Delegatura',
    68: 'Internat',
    69: 'Czteroletnia szkoła muzyczna II stopnia',
    70: 'Dziewięcioletnia szkoła sztuki tańca',
    73: 'Szkoła specjalna przysposabiająca do pracy na podbudowie 8-letniej '
        'szkoły podstawowej',
    74: 'Centrum Kształcenia Ustawicznego - bez szkół',
    75: 'Niepubliczna placówka kształcenia ustawicznego i praktycznego',
    76: 'Młodzieżowy Ośrodek Socjoterapii bez szkół',
    80: 'Zespół wychowania przedszkolnego',
    81: 'Punkt przedszkolny',
    82: 'Poznańska szkoła chóralna ',
    83: 'Niepubliczna placówka kształcenia ustawicznego i praktycznego ze '
        'szkołami',
    100: 'Zespół szkół i placówek oświatowych'
}

zawod_dict = {
    1: 'Korektor i stroiciel instrumentów muzycznych',
    2: 'Technik analityk',
    3: 'Technik budownictwa',
    4: 'Technik budownictwa okrętowego',
    5: 'Technik dróg i mostów kolejowych',
    6: 'Technik elektronik',
    7: 'Technik elektryk',
    8: 'Technik garbarz',
    9: 'Technik geodeta',
    10: 'Technik geofizyk',
    11: 'Technik geolog',
    12: 'Technik górnictwa odkrywkowego',
    13: 'Technik górnictwa otworowego',
    14: 'Technik górnictwa podziemnego',
    15: 'Technik hutnik',
    16: 'Technik hydrolog',
    17: 'Technik instrumentów muzycznych',
    18: 'Technik inżynierii środowiska i melioracji',
    19: 'Technik mechanik',
    20: 'Technik mechanizacji rolnictwa',
    21: 'Technik meteorolog',
    22: 'Technik ochrony środowiska',
    23: 'Technik obuwnik',
    24: 'Technik odlewnik',
    25: 'Technik papiernictwa',
    26: 'Technik poligraf',
    27: 'Technik technologii ceramicznej',
    28: 'Technik technologii chemicznej',
    29: 'Technik technologii drewna',
    30: 'Technik technologii szkła',
    31: 'Technik technologii odzieży',
    32: 'Technik technologii wyrobów skórzanych',
    33: 'Technik telekomunikacji',
    34: 'Technik transportu kolejowego',
    35: 'Technik urządzeń sanitarnych',
    36: 'Technik wiertnik',
    37: 'Technik włókiennik',
    38: 'Technik włókienniczych wyrobów dekoracyjnych',
    39: 'Technik drogownictwa',
    40: 'Technik automatyk sterowania ruchem kolejowym',
    41: 'Technik elektroenergetyk transportu szynowego',
    42: 'Technik budownictwa wodnego',
    43: 'Technik mechatronik',
    44: 'Technik informatyk',
    45: 'Technik teleinformatyk',
    46: 'Fototechnik',
    47: 'Technik urządzeń audiowizualnych',
    48: 'Fotograf',
    49: 'Asystent operatora dźwięku',
    50: 'Technik organizacji produkcji filmowej i telewizyjnej',
    51: 'Technik nawigator morski',
    52: 'Technik żeglugi śródlądowej',
    53: 'Technik mechanik okrętowy',
    54: 'Technik rybołówstwa morskiego',
    55: 'Technik mechanik lotniczy',
    56: 'Technik awionik',
    57: 'Technik bezpieczeństwa i higieny pracy',
    58: 'Technik pożarnictwa',
    59: 'Technik hodowca koni',
    60: 'Technik leśnik',
    61: 'Technik ogrodnik',
    62: 'Technik pszczelarz',
    63: 'Technik rolnik',
    64: 'Technik rybactwa śródlądowego',
    65: 'Technik architektury krajobrazu',
    66: 'Technik technologii żywności',
    67: 'Technik żywienia i gospodarstwa domowego',
    68: 'Dietetyk',
    69: 'Asystentka stomatologiczna',
    70: 'Higienistka stomatologiczna',
    71: 'Ortoptystka',
    72: 'Ratownik medyczny',
    73: 'Technik dentystyczny',
    74: 'Technik farmaceutyczny',
    75: 'Technik masażysta',
    76: 'Technik ortopeda',
    77: 'Technik weterynarii',
    78: 'Terapeuta zajęciowy',
    79: 'Technik optyk',
    80: 'Protetyk słuchu',
    82: 'Technik elektroradiolog',
    83: 'Technik agrobiznesu',
    84: 'Technik ekonomista',
    85: 'Technik handlowiec',
    86: 'Technik hotelarstwa',
    87: 'Technik obsługi turystycznej',
    88: 'Technik organizacji usług gastronomicznych',
    89: 'Technik organizacji reklamy ',
    90: 'Technik spedytor',
    91: 'Technik eksploatacji portów i terminali',
    92: 'Technik logistyk',
    93: 'Technik administracji ',
    94: 'Pracownik socjalny',
    95: 'Asystent osoby niepełnosprawnej',
    96: 'Opiekunka środowiskowa',
    97: 'Opiekun w domu pomocy społecznej',
    98: 'Aktor cyrkowy',
    99: 'Aktor scen muzycznych',
    100: 'Animator kultury  ',
    101: 'Muzyk ',
    102: 'Plastyk',
    103: 'Tancerz',
    104: 'Bibliotekarz',
    105: 'Technik archiwista',
    106: 'Technik informacji naukowej',
    107: 'Technik rachunkowości',
    108: 'Technik prac biurowych',
    109: 'Technik usług pocztowych i telekomunikacyjnych',
    110: 'Kelner',
    111: 'Kucharz',
    112: 'Kucharz małej gastronomii',
    113: 'Opiekunka dziecięca',
    114: 'Fryzjer',
    115: 'Technik usług fryzjerskich',
    116: 'Technik usług kosmetycznych',
    117: 'Technik ochrony fizycznej osób i mienia',
    118: 'Sprzedawca',
    119: 'Technik księgarstwa',
    120: 'Pszczelarz',
    121: 'Rolnik',
    122: 'Ogrodnik ',
    123: 'Rybak śródlądowy ',
    124: 'Górnik eksploatacji podziemnej',
    125: 'Górnik odkrywkowej eksploatacji złóż',
    126: 'Kamieniarz',
    127: 'Betoniarz-zbrojarz',
    128: 'Cieśla',
    129: 'Monter budownictwa wodnego',
    130: 'Monter konstrukcji budowlanych',
    131: 'Monter nawierzchni kolejowej',
    132: 'Murarz',
    133: 'Renowator zabytków architektury',
    134: 'Zdun',
    135: 'Dekarz',
    136: 'Monter instalacji i urządzeń sanitarnych',
    137: 'Monter sieci komunalnych',
    138: 'Monter systemów rurociągowych',
    139: 'Posadzkarz',
    140: 'Monter instalacji gazowych',
    141: 'Monter izolacji budowlanych',
    142: 'Malarz-tapeciarz',
    143: 'Kominiarz',
    144: 'Lakiernik',
    145: 'Blacharz',
    146: 'Monter kadłubów okrętowych',
    147: 'Blacharz samochodowy',
    148: 'Modelarz odlewniczy',
    149: 'Operator obrabiarek skrawających',
    150: 'Ślusarz',
    151: 'Kowal',
    152: 'Mechanik-monter maszyn i urządzeń',
    153: 'Mechanik-operator pojazdów i maszyn rolniczych',
    154: 'Mechanik pojazdów samochodowych',
    155: 'Monter-instalator urządzeń technicznych w budownictwie wiejskim',
    156: 'Elektryk',
    157: 'Elektromechanik pojazdów samochodowych',
    158: 'Elektromechanik',
    159: 'Monter-elektronik',
    160: 'Monter sieci i urządzeń telekomunikacyjnych ',
    161: 'Monter mechatronik',
    162: 'Mechanik automatyki przemysłowej i urządzeń precyzyjnych',
    163: 'Monter instrumentów muzycznych',
    164: 'Mechanik precyzyjny',
    165: 'Optyk-mechanik',
    166: 'Zegarmistrz',
    167: 'Złotnik-jubiler',
    168: 'Introligator',
    169: 'Cukiernik',
    170: 'Piekarz',
    171: 'Rzeźnik-wędliniarz',
    172: 'Stolarz',
    173: 'Koszykarz-plecionkarz      ',
    174: 'Krawiec',
    175: 'Kuśnierz',
    176: 'Tapicer',
    177: 'Rękodzielnik wyrobów włókienniczych',
    178: 'Kaletnik',
    179: 'Obuwnik',
    180: 'Garbarz skór',
    181: 'Górnik eksploatacji otworowej',
    182: 'Operator maszyn i urządzeń do obróbki plastycznej',
    183: 'Operator maszyn i urządzeń metalurgicznych',
    184: 'Operator maszyn i urządzeń odlewniczych',
    185: 'Operator urządzeń przemysłu ceramicznego',
    186: 'Operator urządzeń przemysłu szklarskiego',
    187: 'Operator urządzeń przemysłu chemicznego',
    188: 'Drukarz',
    189: 'Operator maszyn w przemyśle włókienniczym ',
    190: 'Operator maszyn i urządzeń przemysłu spożywczego',
    191: 'Mechanik maszyn i urządzeń drogowych',
    192: 'Operator maszyn leśnych  ',
    193: 'Pracownik pomocniczy obsługi hotelowej',
    194: 'chemiczne badanie środowiska',
    195: 'ekonomiczno-administracyjny',
    196: 'elektroniczny',
    197: 'elektrotechniczny',
    198: 'kreowanie ubiorów',
    199: 'kształtowanie środowiska',
    200: 'leśnictwo i technologia drewna',
    201: 'mechaniczne techniki wytwarzania',
    202: 'mechatroniczny',
    203: 'rolniczo-spożywczy',
    204: 'socjalny',
    205: 'transportowo-spedycyjny',
    206: 'usługowo-gospodarczy',
    207: 'zarządzanie informacją',
    208: 'język angielski',
    209: 'język francuski',
    210: 'język hiszpański',
    211: 'język niemiecki',
    212: 'język włoski',
    214: 'pedagogika opiekuńczo-wychowawcza',
    215: 'pedagogika opiekuńczo-wychowawcza z terapią pedagogiczną',
    216: 'pedagogika resocjalizacyjna',
    217: 'resocjalizacja z wychowaniem fizycznym',
    218: 'pedagogika resocjalizacyjna z elementami profilaktyki',
    219: 'pedagogika rewalidacyjna w zakresie oligofrenopedagogiki',
    220: 'pedagogika rewalidacyjna w zakresie pedagogiki terapeutycznej',
    221: 'pedagogika specjalna',
    222: 'pedagogika specjalna - oligofrenopedagogika',
    223: 'pedagogika specjalna - rewalidacyjna',
    224: 'pedagogika specjalna z edukacją informatyczną',
    225: 'pedagogika społeczna',
    226: 'pedagogika terapeutyczna i integracyjna',
    227: 'pedagogika wczesnoszkolna',
    228: 'pedagogika wczesnoszkolna i integracyjna',
    229: 'pedagogika wieku dziecięcego',
    230: 'pedagogika z wychowaniem fizycznym i zdrowotnym',
    231: 'wychowanie przedszkolne',
    232: 'nauczanie początkowe z muzyką',
    233: 'nauczanie początkowe, kształcenie zintegrowane',
    234: 'nauczanie początkowe z wychowaniem przedszkolnym',
    235: 'nauczanie początkowe z rozszerzonym programem języka angielskiego',
    236: 'edukacja wczesnoszkolna z muzyką',
    237: 'edukacja wczesnoszkolna z plastyką',
    238: 'edukacja wczesna i przedszkolna',
    239: 'edukacja wczesna i technika',
    240: 'edukacja wczesna i przyroda',
    241: 'edukacja wczesna i sztuka',
    242: 'sztuka, edukacja artystyczna',
    243: 'matematyka',
    244: 'matematyka z informatyką',
    245: 'informatyka',
    246: 'język polski',
    247: 'język polski z historią',
    248: 'język polski z muzyką',
    249: 'język polski z plastyką',
    250: 'wychowanie fizyczne',
    251: 'wychowanie fizyczne z informatyką',
    252: 'wychowanie fizyczne i zdrowotne',
    253: 'inna',
    266: 'Rzemiosło artystyczne i użytkowe w metalu',
    273: 'Technolog robót wykończeniowych w budownictwie',
    274: 'Eksperymentalny',
    275: 'Inny',
    276: 'Technik cyfrowych procesów graficznych',
    277: 'Technik pojazdów samochodowych',
    278: 'Technik dźwięku',
    279: 'Technik realizacji dźwięku',
    280: 'Technik przetwórstwa mleczarskiego',
    281: 'Technik turystyki wiejskiej',
    282: 'Technik transportu drogowego',
    283: 'Florysta',
    284: 'Technik usług pocztowych i finansowych',
    285: 'Opiekun medyczny',
    286: 'Technik przeróbki kopalin stałych',
    287: 'Opiekun osoby starszej',
    288: 'Technik sztukatorstwa i kamieniarstwa artystycznego',
    289: 'Monter izolacji przemysłowych',
    290: 'Blacharz izolacji przemysłowych',
    291: 'Wiertacz odwiertów eksploatacyjnych i geofizycznych',
    292: 'język rosyjski z rozszerzonym programem języka angielskiego',
    293: 'język polski z bibliotekoznawstwem',
    294: 'język polski z terapią pedagogiczną',
    295: 'pedagogika wczesnoszkolna z oligofrenopedagogiką',
    296: 'pedagogika wczesnoszkolna z przedszkolną',
    297: 'wychowanie fizyczne z gimnastyką korekcyjną',
    298: 'język polski z informacją naukową i bibliotekoznawstwem',
    299: 'nauczanie poczatkowe i wychowanie przedszkolne',
    300: 'pedagogika wczesnoszkolna i przedszkolna',
    301: 'nauczanie początkowe z plastyką',
    302: 'edukacja zintegrowana i przedszkolna',
    303: 'pedagogika opiekuńczo-wychowawcza i resocjalizacja',
    304: 'pedagogika niepełnosprawnych intelektualnie i terapia pedagogiczna',
    305: 'pedagogika terapeutyczna i wychowanie przedszkolne',
    306: 'nauczanie początkowe',
    307: 'edukacja artystyczna - plastyka',
    308: 'edukacja plastyczna i zintegrowana edukacja wczesnoszkolna',
    309: 'edukacja artystyczna – muzyka',
    310: 'edukacja muzyczna i edukacja przedszkolna',
    311: 'pedagogika opiekuńcza i pedagogika resocjalizacyjna',
    312: 'resocjalizacja',
    313: 'język polski z kształceniem zintegrowanym',
    314: 'pedagogika rewalidacyjna',
    315: 'pedagogika niepełnosprawnych intelektualnie z pedagogiką '
        'wczesnoszkolną',
    317: 'pedagogika resocjalizacyjna z przygotowaniem do życia w rodzinie',
    318: 'pedagogika społeczna z przygotowaniem do życia w rodzinie',
    319: 'pedagogika resocjalizacyjna i pedagogika opiekuńcza',
    320: 'wychowanie przedszkolne z muzyką',
    321: 'zintegrowana edukacja wczesnoszkolna i przedszkolna',
    322: 'edukacja przedszkolna i zintegrowana edukacja wczesnoszkolna',
    323: 'pedagogika specjalna z informatyką w kształceniu specjalnym',
    324: 'pedagogika wieku dziecięcego i muzyka',
    325: 'pedagogika wieku dziecięcego i plastyka',
    326: 'pedagogika wieku dziecięcego i przyroda',
    327: 'pedagogika wieku dziecięcego i informatyka',
    328: 'pedagogika specjalna oligofrenopedagogika i kształcenie '
        'zintegrowane',
    329: 'pedagogika resocjalizacyjna i wychowanie fizyczne',
    330: 'edukacja wczesnoszkolna i przedszkolna',
    331: 'Technik energetyk',
    332: 'Technik gazownictwa',
    333: 'Technik urządzeń i systemów energetyki odnawialnej',
    334: 'Technik tyfloinformatyk',
    335: 'Operator maszyn i urządzeń do przetwórstwa tworzyw sztucznych',
    336: 'Technik żywienia i usług gastronomicznych',
    337: 'Technik renowacji elementów architektury',
    338: 'Monter sieci, instalacji i urządzeń sanitarnych',
    339: 'Monter zabudowy i robót wykończeniowych w budownictwie',
    340: 'Stroiciel fortepianów i pianin',
    341: 'Technik budowy fortepianów i pianin',
    342: 'Asystent kierownika produkcji filmowej/telewizyjnej',
    343: 'Technik realizacji nagrań i nagłośnień',
    344: 'Technik sterylizacji medycznej',
    345: 'Technik elektroniki i informatyki medycznej',
    346: 'Technik procesów drukowania',
    347: 'Technik procesów introligatorskich',
    348: 'Wiertacz',
    349: 'Murarz-tynkarz',
    350: 'Wędliniarz'
}

typ_organu_prow_dict = {
    1: 'Gmina',
    2: 'Miasto na prawach powiatu',
    3: 'Powiat ziemski',
    4: 'Samorząd województwa',
    5: 'Minister ds. oświaty i wychowania',
    6: 'Minister ds. kultury i dziedzictwa narodowego',
    7: 'Minister ds. wewnętrznych',
    8: 'Minister ds. obrony',
    9: 'Minister ds. pomocy społecznej',
    10: 'Minister ds. sprawiedliwości',
    11: 'Minister ds. zagranicznych',
    12: 'Minister ds. rolnictwa i rozwoju wsi',
    13: 'Minister ds. środowiska',
    20: 'Kurator oświaty',
    21: 'Przedsiębiorstwo Państwowe',  # changed in NSIO
    22: 'Stowarzyszenia',
    23: 'Organizacje Społeczne inne niż wymienione',
    24: 'Związek Rzemiosła Polskiego',
    25: 'Krajowa Rada Spółdzielcza',
    26: 'Samorząd Gospodarczy i Zawodowy',
    27: 'Organizacje Związkowe',
    28: 'Organizacje Wyznaniowe',
    29: 'Przedsiębiorstwa Osób Fizycznych',
    30: 'Szkoły Wyższe Niepubliczne',  # changed in NSIO
    31: 'Spółki Handlowe',  # changed in NSIO
    32: 'Fundacje',
    33: 'Osoba fizyczna',  # changed in NSIO
    34: 'Szkoły Wyższe Publiczne',  # changed in NSIO
    35: 'Administracja rządowa na szczeblu centralnym',
    36: 'Administracja rządowa na szczeblu wojewódzkim',
    67: 'Delegatura kuratorium oświaty'
}
