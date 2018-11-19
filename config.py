# -*- coding: utf-8 -*-
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

DBNAMELIST = [('erp', 'erp'), ('doc_ob', 'doc_ob'), ('erp_test2', 'erp_test2')]

TIMER = 1000

EXEC_STATUS = ['Stop', 'Execute']

PROC_LIST = [['backup', 
'"bin/backup.cmd" {srv_name} {srv_user} {srv_passwd} {dbname} {dbnamenew} {path_backup} '], 
['restore', 
 '"bin/restore.cmd" {srv_name_rest} {srv_user} {srv_passwd} {dbname} {dbnamenew} {path_backup_rest} '],
['cut', 
 '"bin/cut.cmd" {srv_name_rest} {srv_user} {srv_passwd} {dbname} {dbnamenew} {dtcut} ']]

SRV_NAME = 'id-1c'
SRV_NAME_REST = 'id-olap'
SRV_USER = 'admin_dev'
SRV_PASSWD = 'Q12345!'
PATH_BACKUP = '\\\id-olap\python-backup'
PATH_BACKUP_REST = 'e:\python-backup'

              