from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

POSTGRES = {
    #'user': 'jorgegene',
    #'db': 'jorgegene',
    #'pw': 'telocam',
    #'host': 'localhost',    
    'user': 'telocam',
    'db': 'telocam',
    'pw': 'passtelocam',
    'host': '155.210.47.51',
    'port': '15432',
}

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

from models import User, Pass


@app.route('/')
def hello():
    return "Hello World"

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run()