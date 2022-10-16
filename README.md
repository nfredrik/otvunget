# Allmänt

Läs ut elpriser från en hemsida. Parsa html och gör om det till json och spara.

Om en lyckat läsning har gjorts görs ingen mer läsning den dagen.
Om json-datat inte  innehåller dagens datum sparas ingen fil, vilket gör 
att skriptet fortsätter att läsa till det är uppfyllt. 

Skriptet styrs genom en konfiguration:

| Parameter      | funktion                                        | typ   |
|----------------|-------------------------------------------------|-------|
| attempts       | antal försök mot datakälla vid givet tillfälle  | int   |
| interval       | tid mellan varje försök vid ett givet tillfälle | int   |
| poll frequency | tid mellan varje försök                         | int   |
| log level      | nivå på log, fatal till debug                   | string|
| mock           | mockad datakälla eller inte                     | bool  |
| filename       | namn på sparade elpriser, json                  | string|


# Logging

Vid hämting loggar skriptet om det misslyckas att hämta från datakällan.

Vi parsning av datat loggar skriptet om datat inte är konsistent, exvis
inget timestamp eller dylikt.

Vid sparande till fil loggar skriptet om data inte har dagens datum




## Använding
$ ./elspot.py