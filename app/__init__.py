from flask import Flask
from mongokit import Connection, Document

# create the little application object
app = Flask(__name__)
app.config.from_object('config')

# connect to the database
connection = Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])

from app import views, models