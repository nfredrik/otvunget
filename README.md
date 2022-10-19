# Allmänt

Läs ut elpriser från en hemsida. Parsa html och gör om det till json och spara till fil.

Om en lyckat läsning har gjorts görs ingen mer läsning den dagen.
Om json-datat inte  innehåller dagens datum sparas ingen fil, vilket gör 
att skriptet fortsätter att försöka läsa. 

Skriptet styrs genom en konfiguration:

| Parameter      | funktion                                        | typ   |
|----------------|-------------------------------------------------|-------|
| attempts       | antal f�rs�k mot datak�lla vid givet tillf�lle  | int   |
| interval       | tid mellan varje f�rs�k vid ett givet tillf�lle | int   |
| poll frequency | deprikerad                                       | int   |
| backoff_start  | starttid mellan tillf�llen att f�rs�ka           | int    |
| backoff_multipel | faktor att �ka tiden med mellan f�rs�k         | int    |
| backoff_stop   | maximal tid mellan tillf�llen att f�rs�ka        | int    |
| log level      | nivå på log, fatal till debug                   | string|
| mock           | mockad datakälla eller inte                     | bool  |
| filename       | namn på sparade elpriser, json                  | string|


# Logging

Vid hämting loggar skriptet om det misslyckas att hämta från datakällan.

Vi parsning av datat loggar skriptet om datat inte är konsistent, exvis
inget timestamp eller felaktikt format på priset.

Vid sparande till fil loggar skriptet om data inte har dagens datum.


## Använding
$ ./elspot.py


## TOOL

 - wrap på logg?
 - bättre parsning av pris?
 - 