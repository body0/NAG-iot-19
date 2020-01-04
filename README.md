# NAG TEMP REP
## TO DO
```

=====PUDIL=====
tisk
dodělat modely
návrh komunikace rasbery-arduino
dodělat návrh pythnu

=====NYKL=====
obecně naplánovat architekturu v pythnu
složitější funkce rasbery (camera; log; ...)
webové rozhraní + pytho api

=====DŽONIS=====
arduino periferie

=====POOL=====
stříhání videa
pokusit se zprovoznit rfid

```

# CHYTRÍ DUM

## Základní funkce

## Dodatečné funkce

### Kamera

### Settings
Umožnuje změnit některé parametry upravující chování domu (buď na webové stránce nebo v souboru)
Při startu se pokusíme načíst nastavení ze souboru (.json), prokud při tomto prosecu nastane chyba, načte se defaultní nastavení

### Web app

#### Login
Pro přístup k jakýmkoliv datům je potřeba zadat autoriyační pin
#### Status
Zde je vydět aktuální stav celého domu (osvětlení, stav brány, hodnoty ze senzorů, čas posledního přihlášení, ...)
#### Settings
Umožnuje změnit některé parametry upravující chování domu
#### Events
List všech událostí a errorů

### API

## Myšleky pro budoucí rozšíření
- kamera jako web kaera s přímým přenosem na již vytvořený web
- otvírání garážových vrat pomicí servo motorku