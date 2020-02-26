
## ESP
### Power-Saving metody
    - použití holého čipu
    - low drop napetový regulátor
    - kondenzátor 
    - deep sleep
## APPLIKACE
### GRAFANA
    - Jak je psané na oficiálních stránkách jedná se o profesionální oupen-source webovou aplikaci pro vizualizaci dat.
    - Jako datový zdroj je zde použita MySql databáze, do které jsou zapicovány data ze všech zdrojů.
    - Celou aplikaci si hostujeme sami pomocí předpřipraveného image
### Návrh Propojení Jednotlivých Služeb 
    - Grafana spolu s databází (MySql) a Webové rozhraví/BD REAT API (nakonec v pythnu/flask) jsou hostovány na naSem soukromém serveru. 
    - Grafana a BD REAT API jsou přístupné skrzreverse-proxi (Nginx) terá zajišťuje "přidání" domeny, zabezpečení (HTTPS) a přesmérováváni z nezabezpečených linků.
    - Docker je zde také vzužit pro lepši managment všech služeb
    - Posílání data z Rasberi-Pi na DB API je vcelku přímočaré, Problém nastáná pokud bzchom chtéli posílat příkazy zpátky na Rasberi-Pi. Rasberi-Pi je v siti bez veřejné adresi (respektive siť je natovaná a na routr dál v síti se nedostaneme), zde se nám nabíyí únedka neklik možných variant pro zpřistupnéní takovéto konekce (Vpn + Nginx; Web Socket; SSH tunel), my jsme si vybrali třetí variantu.
    - ESP bude svá ďata posílat také na DB interface. Avšak abychom nemusei měnit firmware ESP pokaždé, co jsme budeme nuset obnovit náš certifikát, DB API je dostupné i přes druhou url (port), která má námi vygenerovaný certifikát (námi podepsaný) s neomezenou platností (ne že by na té posledni části záleželo, jedná se přeci jenom o fingerprint certifikátu, který je na ESP kontrolován). Takto se můžeme vyhnout odchycení a zneužití správy na lokální síti.
### DB
    - MySql (docker img)
    - sql injection neni možná, protože:
        - MySQL Connector sanatizuje tuto query parametry
        - připojit se mohou jemon klienti se správným DB_API_ACCES_TOKEN (esp, pi) 
### Kód spravujíci Raspbery-Pi
    - védšina funkci zUstává z předchozí verze aplikace
    - původní aplikace na managment apky byla zrušena (všechnz její funkce nahradila grafana)
### MQTT vs HTTP
    - jedna z našich původních myšlenek byla požití MQTT oprototi HTTP, tuto myšleku jsme zahodily ze 2 důvodů
        - když jsme se pokoušeli připojit na soutěžní mqtt broker, dostávali jsme connection timeout,
        - u HTTP jsme si byli jistější ohledně toho jak celou komunikaci zabezpečit.

# LINK 
https://grafana.com/
https://www.mysql.com/
https://dev.mysql.com/doc/connector-python/en/