# -*- coding: utf-8 -*-
from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)
app.config.from_object('config')

if not app.debug:
    if not os.path.exists('logs'):
            os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/jf-copy-cut.log', maxBytes=10240,
                                           backupCount=10)            
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
app.logger.setLevel(logging.INFO)
#app.secret_key = 'asd12345'
from app import views