echo off
set srvsql=%1
set username=%2
set passwd=%3
set dbname=%4
set dbnamenew=%5
set dtcut=%7
sqlcmd -S %srvsql% -U %username% -P %passwd% -d %dbnamenew% -i bin/cut.sql -v newDB=%dbnamenew% dat=%dtcut%
rem echo Test cut
rem ls
rem echo "�ᯥ譮"