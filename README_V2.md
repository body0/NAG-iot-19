
## ESP
### Power-Saving metody
    - použití holého čipu
    - low drop napetový regulátor
    - kondenzátor 
    - deep sleep
## APPLIKACE
### Grafana
    - jendná se o profesionální webový nástroj pro zobrazoví statických dat
### NÁvrh Propojení Jednotlivých Služeb 
    - Grafana spolu s databází (MySql) a Webové rozhraví/BD REAT API (nakonec v pythnu/flask) jsou hostovány na naSem soukromém serveru. 
    - Grafana a BD REAT API jsou přístupné skrzreverse-proxi (Nginx) terá zajišťuje "přidání" domeny, zabezpečení (HTTPS) a přesmérováváni z nezabezpečených linků.
    - Docker je zde také vzužit pro lepši managment všech služeb
    - Posílání data z Rasberi-Pi na DB API je vcelku přímočaré, Problém nastáná pokud bzchom chtéli posílat příkazy zpátky na Rasberi-Pi. Rasberi-Pi je v siti bez veřejné adresi (respektive siť je natovaná a na routr dál v síti se nedostaneme), zde se nám nabíyí únedka neklik možných variant pro zpřistupnéní takovéto konekce (Vpn + Nginx; Web Socket; SSH tunel), my jsme si vybrali třetí variantu.
    - ESP bude svá ďata posílat na DB interface. Avšak abychom nemusei ménit firmware ESP pokaždé, co jsme budeme nuset obnovit náš certifikát, BG INTERFACE je dostupné i přes druhou url, která má námi vygenerovaný certifikát s neomezenou platností (ne že by na té posledni části záleželo, jedná se přeci jenom o fingerprint certifikátu, který je na ESP kontrolován).
### Kód spravujíci Raspbery-Pi
    - védšina funkci zUstává z předchozí verze aplikace
    - původní aplikace na managment apky byla zrušena (všechnz její funkce nahradila grafana)
### GRAFANA
    - Jako datový zdroj je zde použita MySql databáze, do které jsou zapicovány data ze všech zdrojů
## SOLÁR & BATERIE