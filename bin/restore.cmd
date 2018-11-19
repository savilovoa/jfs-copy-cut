echo off
set srvsql=%1
set username=%2
set passwd=%3
set dbname=%4
set dbnamenew=%5
set pathbackup=%6
sqlcmd -S %srvsql% -U %username% -P %passwd% -i bin/restore_db.sql -v dfile="%pathbackup%\b_%dbname%.bkp" newDB=%dbnamenew%
rem echo Test restore
rem type bin/restore_db.sql
rem ls 
rem echo "�ᯥ譮"

