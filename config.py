CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

DBNAMELIST = [('erp_kaa', 'erp_kaa'), ('doc_ob', 'doc_ob'), ('erp_test2', 'erp_test2')]

TIMER = 1000

EXEC_STATUS = ['Stop', 'Execute']

PROC_LIST = [['backup', 
'"bin/backup.cmd" {} {} {} '], 
['restore', 
 '"bin/restore.cmd" {} {} {}  ']]
              