# -*- coding: utf-8 -*-
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

DBNAMELIST = [('erp_kaa', 'erp_kaa'), ('doc_ob', 'doc_ob'), ('erp_test2', 'erp_test2')]

TIMER = 1000

EXEC_STATUS = ['Stop', 'Execute']

PROC_LIST = [['backup', 
"sqlcmd -S id-1c -U admin_dev -P Q12345! -Q \"BACKUP DATABASE {} TO  DISK = '\\id-olap\python-backup\b_j1.bkp' WITH NOFORMAT, INIT, SKIP, NOREWIND, NOUNLOAD, STATS = 10\""], 
['restore', 
 '"bin/restore.cmd" {} {} {}  ']]
              