@echo off
echo Teste CGI-Skript direkt...
echo.

REM Setze Umgebungsvariablen für CGI
set REQUEST_METHOD=POST
set CONTENT_TYPE=application/x-www-form-urlencoded
set CONTENT_LENGTH=38

REM Erstelle temporäre Eingabedatei
echo zahl=255^&von_basis=10^&ziel_basis=16 > temp_input.txt

REM Führe CGI-Skript aus
python unserSkript.cgi < temp_input.txt

REM Lösche temporäre Datei
del temp_input.txt

echo.
echo Test abgeschlossen!
pause
