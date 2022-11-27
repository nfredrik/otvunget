# Allm�nt

L�s ut elpriser fr�n en hemsida. Parsa html och g�r om det till json och spara till fil.

Om en lyckad l�sning har gjorts g�rs ingen mer l�sning den dagen.
Om json-datat inte inneh�ller dagens datum sparas ingen fil, vilket g�r 
att skriptet forts�tter att f�rs�ka l�sa.
Tiden mellan f�rs�k �kar exponentiellt till en maxtid vid misslyckade och 
nollst�lls till ett startv�rde vid lyckad h�mtning.

Skriptet styrs genom en konfiguration:

| Parameter     | funktion                               | typ   |
|---------------|----------------------------------------|-------|
| backoff_start | starttid mellan tillf�llen att f�rs�ka | int   |
| backoff_multiple | faktor att �ka tiden med mellan f�rs�k | int   |
| backoff_stop  | maximal tid mellan tillf�llen att f�rs�ka | int   |
| loglevel      | niv� p� log, fatal till debug          | string|
| json_filename | path till JSON fil med dagens elpriser | string|
| log_filename  | path till loggfil, txt                 | string|
| csv_filename  | path till CSV fil med alla dagars priser | string|

JSON-filen inneh�ller ett dygns priser i json-format.
CSV-filen inneh�ller alla ackumulerade dygns priser i formatet
space-separerade variabler.

Konfigurationsfilen ska lagras p� samma plats som skripten.

# Logging

Vid h�mting loggar skriptet om det misslyckas att h�mta fr�n datak�llan.

Vid parsning av datat loggar skriptet om datat inte �r konsistent, exvis
inget timestamp eller felaktikt format p� priset.

Vid sparande till fil loggar skriptet om data inte har dagens datum.

Loggniv�er, se [logniv�er hos python](https://docs.python.org/3/library/logging.html#levels)

# �vrigt

�verg�ng till sommartid ger odefinierat resultat. Hemsidans utseende f�r dubbeltimmen �r ok�nt. Enligt direktiv fr�n EU ska dock olika sommartid/vintertid inte brukas l�ngre.

## Anv�nding
`$ ./elspot.py`

