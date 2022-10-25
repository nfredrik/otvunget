# Allm�nt

L�s ut elpriser fr�n en hemsida. Parsa html och g�r om det till json och spara till fil.

Om en lyckad l�sning har gjorts g�rs ingen mer l�sning den dagen.
Om json-datat inte  inneh�ller dagens datum sparas ingen fil, vilket g�r 
att skriptet forts�tter att f�rs�ka l�sa.
Tiden mellan f�rs�k �kar exponentiellt till en maxtid vid misslyckade och 
nollst�lls till en startv�rde vid lyckad h�mtning.

Skriptet styrs genom en konfiguration:

| Parameter      | funktion                                        | typ   |
|----------------|-------------------------------------------------|-------|
| attempts       | antal f�rs�k mot datak�lla vid givet tillf�lle  | int   |
| interval       | tid mellan varje f�rs�k vid ett givet tillf�lle | int   |
| poll frequency | deprikerad                                       | int   |
| backoff_start  | starttid mellan tillf�llen att f�rs�ka           | int    |
| backoff_multipel | faktor att �ka tiden med mellan f�rs�k         | int    |
| backoff_stop   | maximal tid mellan tillf�llen att f�rs�ka        | int    |
| log level      | niv� p� log, fatal till debug                   | string|
| mock           | mockad datak�lla eller inte                     | bool  |
| filename       | namn p� sparade elpriser, json                  | string|

# Logging

Vid h�mting loggar skriptet om det misslyckas att h�mta fr�n datak�llan.

Vi parsning av datat loggar skriptet om datat inte �r konsistent, exvis
inget timestamp eller felaktikt format p� priset.

Vid sparande till fil loggar skriptet om data inte har dagens datum.

## Anv�nding
`$ ./elspot.py`
