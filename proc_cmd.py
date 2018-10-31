import threading
import subprocess
import datetime
from config import time_step 


out_logs = list ()
exec_status = list()
exec_end = True

def proc_thread():
    exec_end = False
    out_logs.append('exec_end ' + str(exec_end))
    try:
        exec_status.append('start ping')
        raise Exception('Oj')
        proc = subprocess.Popen("ping 127.0.0.1", shell=True, stdout=subprocess.PIPE)
        for out in proc.stdout.readlines():
            out_logs.append(out.decode("cp866"))
        exec_status.append('end ping')
    except Exception as e:
        out_logs.append('error')
        print('error')
        
    finally: 
        exec_end = True    

def exec_copy_cut():
    t = threading.Thread(target=proc_thread,
                             name="Proc 1C DB copy ",
                             args=(),
                             daemon=True)    
    t.start()
    
    