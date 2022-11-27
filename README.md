# Allmänt

Läs ut elpriser från en hemsida. Parsa html och gör om det till json och spara till fil.

Om en lyckad läsning har gjorts görs ingen mer läsning den dagen.
Om json-datat inte innehåller dagens datum sparas ingen fil, vilket gör 
att skriptet fortsätter att försöka läsa.
Tiden mellan försök ökar exponentiellt till en maxtid vid misslyckade och 
nollställs till ett startvärde vid lyckad hämtning.

Skriptet styrs genom en konfiguration:

| Parameter     | funktion                               | typ   |
|---------------|----------------------------------------|-------|
| backoff_start | starttid mellan tillfällen att försöka | int   |
| backoff_multiple | faktor att öka tiden med mellan försök | int   |
| backoff_stop  | maximal tid mellan tillfällen att försöka | int   |
| loglevel      | nivå på log, fatal till debug          | string|
| json_filename | path till JSON fil med dagens elpriser | string|
| log_filename  | path till loggfil, txt                 | string|
| csv_filename  | path till CSV fil med alla dagars priser | string|

JSON-filen innehåller ett dygns priser i json-format.
CSV-filen innehåller alla ackumulerade dygns priser i formatet
space-separerade variabler.

Konfigurationsfilen ska lagras på samma plats som skripten.

# Logging

Vid hämting loggar skriptet om det misslyckas att hämta från datakällan.

Vid parsning av datat loggar skriptet om datat inte är konsistent, exvis
inget timestamp eller felaktikt format på priset.

Vid sparande till fil loggar skriptet om data inte har dagens datum.

Loggnivåer, se [lognivåer hos python](https://docs.python.org/3/library/logging.html#levels)

# Övrigt

Övergång till sommartid ger odefinierat resultat. Hemsidans utseende för dubbeltimmen är okänt. Enligt direktiv från EU ska dock olika sommartid/vintertid inte brukas längre.

## Använding
`$ ./elspot.py`

