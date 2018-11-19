echo off
set srvsql=%1
set username=%2
set passwd=%3
set dbname=%4
set dbnamenew=%5
set pathbackup=%6
rem sqlcmd -S %srvsql% -U %username% -P %passwd% -Q "BACKUP DATABASE %dbname% TO  DISK = '%pathbackup%\b_%dbname%.bkp' WITH NOFORMAT, INIT, SKIP, NOREWIND, NOUNLOAD, STATS = 10"
echo Test backup
rem ls -l
echo "�ᯥ譮" 

