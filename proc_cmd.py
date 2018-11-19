# -*- coding: utf-8 -*-
import threading
import subprocess
import datetime
from datetime import date
import logging

import os
from app import app
from config import PROC_LIST, SRV_NAME, SRV_NAME_REST, SRV_PASSWD, SRV_USER, PATH_BACKUP, PATH_BACKUP_REST




out_logs = list ()
exec_status = list ()
exec_status.append(False);

def lastmonth():
    d = date.today()
    if d.month == 1:
        m = 12 
        y = d.year - 1
    else:
        m = d.month - 1
        y = d.year
        return datetime.date(y, m, 1)

def proc_thread(dbname, dbnamenew, cut_f, rewrite_f):
    p_list = []
    p_list = PROC_LIST
    code = 0
    out = []
    err = []
    try:
        exec_status.append(True)    
        for p in p_list:
            if not app.debug:
                app.logger.info(p[0]  + ':' + p[1].format(dbname, dbname))            
            out_logs.append("Start " + p[0]) 
            
            #out_logs.append(p[1].format(dbname=dbname, dbnamenew=dbnamenew, srv_name=SRV_NAME, srv_user=SRV_USER,
            #                                    srv_passwd=SRV_PASSWD, path_backup=PATH_BACKUP,
            #                                    path_backup_rest=PATH_BACKUP_REST, dtcut=lastmonth().strftime('%Y%m%d') ))
            
            proc = subprocess.Popen(p[1].format(dbname=dbname, dbnamenew=dbnamenew, srv_name=SRV_NAME, srv_user=SRV_USER,
                                                srv_passwd=SRV_PASSWD, srv_name_rest=SRV_NAME_REST, path_backup=PATH_BACKUP, 
                                                path_backup_rest=PATH_BACKUP_REST, dtcut=lastmonth().strftime('%Y%m%d'))                                
                                    , shell=True, stdout=subprocess.PIPE)
            #code = proc.wait()
            out, err = proc.communicate()
            #print (code)
            out_logs.append([out.decode("cp866")])
            o2 = out.decode("cp866")
            t = False
            if (o2.find('успешно') >= 0):
                t = True
                           
            if t:
                out_logs.append('{} - завершено успешно'.format(p[0]))
            else:
                out_logs.append('{} = Error: {}'.format(p[0], err) )              
                Break
            
                
    except:
        out_logs.append('error1')
        print('error1')   
        print (code)
        print(out)
        print(err)        
    finally: 
        exec_status.append(False)    
        #print(exec_status[len(exec_status)-1])
        

def exec_copy_cut(dbname, dbnamenew, cut_f, rewrite_f):
    out_logs.clear()
    t = threading.Thread(target=proc_thread,
                             name="Proc 1C DB copy ",
                             args=(dbname, dbnamenew, cut_f, rewrite_f),
                             daemon=True)    
    t.start()
    
    