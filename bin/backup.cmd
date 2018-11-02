#echo %1
#echo %2
#echo %3
# sqlcmd -S %1 -U %2 -P %3 -Q BACKUP DATABASE %4 TO  DISK = %5 WITH NOFORMAT, INIT, SKIP, NOREWIND, NOUNLOAD, STATS = 10
#Параметры:
#1 - сервер БД,
#2 - пользователь,
#3 - пароль,
#4 - БД,
#5 - файл, в который сохраняется,
set srv=id-1c
set user=admin_dev
set pass=Q12345!
set db=%1
set back_fn=d:\b_%db%.bkp
sqlcmd -S %srv% -U %user% -P %pass% -Q BACKUP DATABASE %db% TO  DISK = %back_fn% WITH NOFORMAT, INIT, SKIP, NOREWIND, NOUNLOAD, STATS = 10
