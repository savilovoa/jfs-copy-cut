import threading
import subprocess
import datetime
import logging

import os
from app import app



out_logs = list ()
exec_status = list ()
exec_status.append(False);

def proc_thread(dbname, dbnamenew, cut_f, rewrite_f):
    p_list = []
    p_list = app.config['PROC_LIST']
    try:
        exec_status.append(True)    
        for p in p_list:
            if not app.debug:
                app.logger.info(p[0]  + ':' + p[1].format(dbname, dbnamenew, cut_f))            
            out_logs.append("Start " + p[0]) 
            proc = subprocess.Popen(p[1].format(dbname, dbnamenew, cut_f), shell=True, stdout=subprocess.PIPE)
            for out in proc.stdout.readlines():
                out_logs.append([out.decode("cp866")])
            if not app.debug:
                app.logger.info(p[0]  + '= Ok' )                        
            
                
    except:
        out_logs.append('error')
        print('error')        
    finally: 
        exec_status.append(False)    
        #print(exec_status[len(exec_status)-1])
        

def exec_copy_cut(dbname, dbnamenew, cut_f, rewrite_f):
    t = threading.Thread(target=proc_thread,
                             name="Proc 1C DB copy ",
                             args=(dbname, dbnamenew, cut_f, rewrite_f),
                             daemon=True)    
    t.start()
    
    