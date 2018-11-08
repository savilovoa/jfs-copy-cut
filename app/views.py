from flask import render_template, flash, redirect, g, session, url_for, json, jsonify, request
from app import app
from forms import UserForm
from proc_cmd import exec_copy_cut, out_logs, exec_status


@app.route('/')
@app.route('/index', methods = ['GET'])
def index():    
    if exec_status[len(exec_status)-1]:
        return redirect(url_for('copy_exec'))
    else:
        if len(out_logs) <= 0:
            return redirect(url_for('order'))
        else:
            return render_template('index.html', 
                title = 'Process end',
                sess = app.config['EXEC_STATUS'][int(exec_status[len(exec_status)-1])],
                dbname = session['dbname'],
                dbnamenew = app.config['PROC_LIST'], # session['dbnamenew'],
                cut = session['cut'],
                rewrite = session['rewrite'],
                #logs = out_logs[len(out_logs)-1]
                )                       
        
@app.route('/order', methods = ['GET', 'POST'])
def order():
    form = UserForm()
    if form.validate_on_submit():
        session['dbname'] = form.DBName.data
        session['dbnamenew'] = form.DBNameNew.data
        session['cut'] = form.cut_f.data
        session['rewrite'] = form.rewrite_f.data
        session['len_logs'] = 0        
        exec_copy_cut(form.DBName.data, form.DBNameNew.data, form.cut_f.data, form.rewrite_f.data)
        return redirect(url_for('copy_exec'))
        
    return render_template('order.html', 
        title = '1c database start process',
        form = form
        #, form.DBName.choices = app.config['DBNAMELIST']
        )

@app.route('/copy_exec', methods = ['GET'])
def copy_exec():
    return render_template('copy_exec.html',
        title = 'Process exec', 
        dbname = session['dbname'],
        dbnamenew = session['dbnamenew'],
        cut = session['cut'],
        rewrite = session['rewrite'],
        timerindex = app.config['TIMER'])



@app.route('/check_proc', methods = ['GET', 'POST'])
def check_proc():
    if exec_status[len(exec_status)-1]:
        s = 'Execute' 
    else:
        s = 'Stop'
    l = len(out_logs)
    if 'len_logs' in session:
        l0 = session['len_logs']
    else:
        l0 = 0
    ll = []
    if l > 0:
        for i in range(l0, l):
            ll.append(out_logs[i]);
    #print(l0, l, exec_status[len(exec_status)-1], ll, out_logs)
    #print(json.dumps({'logs': ll, 'exec_end': exec_status[len(exec_status)-1]}))
    session['len_logs'] = l
    return json.dumps({'status': s, 'exec_end': exec_status[len(exec_status)-1], 'logs_count': l-1,'logs': ll})


    
    