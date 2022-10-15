# Allmänt

Läs ut elpriser från en hemsida. Parsa html och gör om det till json och spara.

Om en lyckat läsning har gjorts under dagen görs ingen med läsning den dagen.
Om json-datat inte inte innehållerdagens datum sparas ingen fil, vilket gör 
att skriptet fortsätter att läsa till det är uppfyllt. 

Skriptet styrs genom en konfiguration:

| Parameter      | funktion                                        | typ   |
|----------------|-------------------------------------------------|-------|
| ATTEMPTS       | Antal försök mot datakälla vid givet tillfälle  | int   |
| INTERVAL       | Tid mellan varje försök vid ett givet tillfälle | int   |
| POLL_FREQUENCY | Tid mellan varje försök                         | int   |
| LOG_LEVEL      | Nivå på log, FATAL till DEBUG                   | string|
| MOCK           | Mockad datakälla eller inte                     | bool  |
| FILENAME       | Namn på sparade elpriser, json                  | string|


# Logging

Vid hämting loggar skriptet om det misslyckas att hämta från datakällan.

Vi parsning av datat loggar skriptet om datat inte är konsistent, exvis
inget timestamp eller dylikt.

Vid sparande till fil loggar skriptet om data inte har dagens datum




## Använding
$ ./elspot.py