from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
#app.secret_key = 'asd12345'
from app import views