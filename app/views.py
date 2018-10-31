from flask import render_template, flash, redirect, g, session, url_for, json, jsonify, request
from app import app
from forms import UserForm
from proc_cmd import exec_copy_cut, out_logs, exec_status, exec_end


@app.route('/')
@app.route('/index')
def index():    
    if exec_end:
        if len(exec_status) <= 0:
            return redirect(url_for('order'))
        else:
            return render_template('index.html', 
                title = 'Process end',
                sess = exec_status[len(exec_status)-1],
                dbname = session['dbname'],
                dbnamenew = session['dbnamenew'],
                cut = session['cut'],
                rewrite = session['rewrite'],
                logs = out_logs[len(out_logs)-1])
    else:
        return redirect(url_for('copy_exec'))
        



@app.route('/order', methods = ['GET', 'POST'])
def order():
    form = UserForm()
    if form.validate_on_submit():
        session['dbname'] = form.DBName.data
        session['dbnamenew'] = form.DBNameNew.data
        session['cut'] = form.cut_f.data
        session['rewrite'] = form.rewrite_f.data
        exec_copy_cut()
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
        rewrite = session['rewrite'])



@app.route('/check_proc', methods = ['GET', 'POST'])
def check_proc():
    if len(exec_status) > 0:
        s = exec_status[len(exec_status)-1]
    else:
        s = 'none'
    return json.dumps({'status': s, 'exec_end': exec_end, 'logs': out_logs})

    
    