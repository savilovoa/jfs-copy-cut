echo off
#sqlcmd -S id-1c -U admin_dev -P Q12345! -Q "BACKUP DATABASE %1 TO  DISK = '\\id-olap\python-bakup\b_%1.bkp' WITH NOFORMAT, INIT, SKIP, NOREWIND, NOUNLOAD, STATS = 10"
ping 8.8.8.8
