from flask import render_template, flash, redirect
from app import app
from forms import UserForm

@app.route('/', methods = ['GET', 'POST'])
def index():
    form = UserForm()
    if form.validate_on_submit():
        flash('Start process copy from "' + form.DBName.data + '" to "' + form.DBNameNew.data + '", cut=' + str(form.cut_f.data) + ', rewrite=' + str(form.rewrite_f.data))    
        
    return render_template('index.html', 
        title = '1c database start process',
        form = form
        #, form.DBName.choices = app.config['DBNAMELIST']
        )
