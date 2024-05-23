from flask import Flask
from flask_restful import Api
from tasks import *
from models import db
from os import environ

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'secret-phrase'
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app) 
api.add_resource(ProcessVideoView, '/process-file') 