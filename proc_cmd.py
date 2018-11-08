# -*- coding: utf-8 -*-
import threading
import subprocess
import datetime
import logging

import os
from app import app




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
    p_list = app.config['PROC_LIST']
    code = 0
    out = []
    err = []
    try:
        exec_status.append(True)    
        for p in p_list:
            if not app.debug:
                app.logger.info(p[0]  + ':' + p[1].format(dbname, dbname))            
            out_logs.append("Start " + p[0]) 
            #code = subprocess.call(p[1].format(dbname, dbnamenew, cut_f))
            subprocess.Popen(p[1].format(dbname, dbname, cut_f), shell=True, stdout=subprocess.PIPE)
            code = subprocess.wait()
            #out, err = subprocess.communicate()
            print (code)
            print(out)
            print(err)
            for o in out:
                out_logs.append([o.decode("cp866")])
                
            if err == 'None':
                if not app.debug:
                    app.logger.info(p[0]  + '= Ok' )                        
                else:
                    out_logs.append('{} - завершено успешно'.format(p[0]))
            else:
                if not app.debug:
                    app.logger.info('{} = Error: {}'.format(p[0], err) )                        
                else:
                    out_logs.append('{} = Error: {}'.format(p[0], err) )                                
            for o in err:
                out_logs.append([o.decode("cp866")])
                
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
    
    