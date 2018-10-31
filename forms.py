from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, SelectField
from wtforms.validators import Required
from app import app

class UserForm(FlaskForm):
    DBName = SelectField('BaseName', choices = app.config['DBNAMELIST'], validators = [Required()])
    DBNameNew = TextField('New db name', validators = [Required()])
    cut_f = BooleanField('Cut', default = True)
    rewrite_f = BooleanField('Rewrite new db', default = True)
