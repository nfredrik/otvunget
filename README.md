# Allmänt

Läs ut elpriser från en hemsida. Parsa html och gör om det till json och spara till fil.

Om en lyckad läsning har gjorts görs ingen mer läsning den dagen.
Om json-datat inte  innehåller dagens datum sparas ingen fil, vilket gör 
att skriptet fortsätter att försöka läsa.
Tiden mellan försök ökar exponentiellt till en maxtid vid misslyckade och 
nollställs till ett startvärde vid lyckad hämtning.

Skriptet styrs genom en konfiguration:

| Parameter      | funktion                                        | typ   |
|----------------|-------------------------------------------------|-------|
| attempts       | antal försök mot datakälla vid givet tillfälle  | int   |
| interval       | tid mellan varje försök vid ett givet tillfälle | int   |
| poll frequency | deprikerad                                      | int   |
| backoff_start  | starttid mellan tillfällen att försöka          | int   |
| backoff_multiple | faktor att öka tiden med mellan försök        | int   |
| backoff_stop   | maximal tid mellan tillfällen att försöka       | int   |
| log level      | nivå på log, fatal till debug                   | string|
| mock           | mockad datakälla eller inte                     | bool  |
| json_filename  | path till JSON fil med dagens elpriser          | string|
| log_filename   | path till loggfil, txt                          | string|
| csv_filename   | path till CSV fil med alla dagars prise         | string|

JSON-filen innehåller ett dygns priser i json-format.
CSV-filen innehåller alla ackumulerade dygns priser i formatet
space-separerade variabler.

Konfigurationsfilen ska lagras på samma plats som skripten.

# Logging

Vid hämting loggar skriptet om det misslyckas att hämta från datakällan.

Vi parsning av datat loggar skriptet om datat inte är konsistent, exvis
inget timestamp eller felaktikt format på priset.

Vid sparande till fil loggar skriptet om data inte har dagens datum.

## Använding
`$ ./elspot.py`
