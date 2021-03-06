# CHYTRÝ DUM
| Úloha | Splněno |
|-------|---------|
| 1. | ANO |
| 2. | ANO |
| 3. | ANO |
| 4. | ANO |
| 5. | ANO |
| 6. | ANO |
| 7. | ANO |
| 8. | ANO |
| 9. | ANO |
| 10. | ANO |
| 11. | ANO |
| 12. | ANO |
Video týmu je na adrese: https://www.youtube.com/watch?v=iWtRl39DOC8 
#### !!! IMPORTANT !!!
Projek je řešen jako jediné komplexní řešení, jehož kód naleznete v src. V jednotlivých souborech úkolů pak naleznete již pouze readme s odkazy na příslušné části kódu.


## Základní funkce

### Autoriční systém 

Pro vybranou skupinu lidí po přiložení čipu systém přejde do autorizovaného stavu, když se přiloží neznámý čip zabliká červená led a zapíská bzučák.

### Brána

Brána se otevře jen při autorizovaném stavu, bez autorizace začne blikat červená led a zapíská bzučák. Brána se zavře po 10s, pokud se v ní nachází objekt nezavře se do jeho odstranění.

### LCD

Na LCD se zobrazují základní informace o domě jako je intenzita osvětlení, teplota, tlak, autorizace, přítomnost někoho v zahradě, přítomnost objektu v bráně.

### Osvětlení 

Jsou zde dvě LED diody jedna je uvnitř, jedna venku. Ta uvnitř je ovládána dvěmi tlačítky po stisku tlačítka svítí 10s, poté zhasne. Venkovní je připojena na senzor osvětlení, úrovně při kterých se rozsvítí a zhasne jde nastavit v [Settings](python/assets/settings.json)

### PIR čidlo

Detekuje pohyb na zahradě, když ho detekuje rozsvítí se LED a zapne bzučák. Dá se hardwarově vypnout přepínačem, který odpojí napájení, je také vypnutý při autorizovaném režimu(na LCD se pořád zobrazuje)

## Dodatečné funkce

### Měření tlaku a teploty
Používáme senzor BMP180

### Kamera

### [Settings](python/assets/settings.json)
Umožnuje změnit některé parametry upravující chování domu (buď na webové stránce nebo v souboru)
Při startu se pokusíme načíst nastavení ze souboru (.json), prokud při tomto prosecu nastane chyba, načte se defaultní nastavení

### Web app

#### Login
Pro přístup k jakýmkoliv datům je potřeba zadat autorizační pin
#### Status
Zde je vidět aktuální stav celého domu (osvětlení, stav brány, hodnoty ze senzorů, čas posledního přihlášení, ...)
#### Settings
Umožnuje změnit některé parametry upravující chování domu
#### Events
List všech událostí a errorů

# Architecture
Předem se omlouvám za občasné nedodržování některých dobrých praktick pythonu není to přeci jenom můj primární jazyk. ...

## [/python](python)
obsahuje jak python scritpy pro ovládáná jednotlivých funkcí domu tak api k webu
- entry point: apy.py
- to run:
```
    export APIKEY="..." &&
    chmod +x api.py &&
    ./api.py 
```

## [/python/lib](python/lib)
    knihovny nedostupné přes pip; autor je uveden na prnívh řádkách souboru knihovny

## [/python/assets](python/assets)
    obsahuje 
    - settings.json: nastavení chování domu, které je čteno a zpracováno settings.py
    - OpenCv: encodované obličeje autortizovaných osob pro face revognition 

### vrstvy abstrakce periferií
kontrola periferií je rozdělena především mezi 3 soubory, kde každý reprezentuje stupeň abstrakce
- devEvent
    jako jediný inportuje GPIO, jedná se v podtatě o slabou abstrakční brstvu sloužící na !!!!!.
- devServise
    Zde se skládají v jednotlivé periferie do jednoúčelových služeb, které poskytují velice jednoduché api navržené pro nase účel. Jedna se take o dalsi decoupling layer například pro případ kdy na raspberry pi dojdou pin a bude se muset použít arduino jako slave zařízení<br>
    př: Light servis umožňje zapnout/vypnout/rozsvítit_po_dobu/blikat_po_dobu; Auth sevis inicializuje rfid a testuje pomocí settings servise jeho autorizovanost, následně emitne příslušný event
- main
    zde se propojují závislosti mezi služby. řeší se zde otázky jako je například co se má stát po autorizaci, jak dlouho má být otevřená brána ...
    zde se také iniciují senzory (v našem případě bh1750 a BMP085)

## [event loginng](python/eventLog.py)
vzhledem k povaze zadání se vyplatí vzužít reaktivní způsob programování. toto zajišťuje mimo jiné i eventLog.py. Jeho účelem je registrovat eventy přes emit a jejich následná distruboce. Každý event ná název, typ (debug, log, warn, err, systemLog, systemWaarn), timestamp, payload. V jakékoliv části programu můžeme buďto subscribnout na jméno/typ, nebo dostat posledních "x" eventů

## další zmíňky
- [common.py](python/common.py)
    poskytuje několik běžných struktur. př. Observable pro sebscribe emit chování, SensorTimer pro periodické volní funkce, enumy pro devServise

## [Web page](webApp/NAG)
Základ webové stránky je Angular framework. Vzhleden k tomu že se jedná o dodatečnou práci jeho architekturu zmínim jenom ve skradce. Informace o api naleznete v dalším odstavci.


## Web API
- login
    pro získání dat z api musí klient poskytnout JWT token. Který se vygeneruje po posláním hesla na /login route. zde se heslo ověří pomocí uloženého hashe v setting.json. zpátky se pošle token který je nutné poté přidat do hlavičky requestů dat. token expiruje za 60min. (aktuálně nepodporuji atomatickou aktualizaci tokenu - nechtělo se mi s tím to tuto demo verzi dělat, uživatel se skrátka musí znovu přihlásit)

- socket
    api zprostředkovává socket, pomocí kterého informuje klienta o nových datach. Avšak jelikož pro poslouchání na tomto socketu nemusíte být autorizován, neposílají se zde žádná data. socket clienta pouze informuje že si může stáhnout data ze standartních routů

- standartní routy
    pro tyto routy je nutný autirizační token
    - /state => aktuální data z apiComponents.py
    - /settings => aktuální nehashované nastavení z settings.py
    - /events => všechy eventy z eventLog.py
 

# Myšleky pro budoucí rozšíření
- kamera jako web kamera s přímým přenosem na již vytvořený web
- otvírání garážových vrat pomicí dc motorku a koncových spínařů(rolovací vrata)
- kód pro arduino mega jako výstupní I2C zařízení je již připraven(může být použito na osvětlení v domě a mnoho dalších věcí
- voice control na ovládání základních funkcí(zhasni, rozsviť, atd.)
