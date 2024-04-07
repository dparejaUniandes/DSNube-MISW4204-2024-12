from flask import Flask
from .modelos import *
from flask_restful import Api
from .vistas import *

def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutorial_canciones.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['JWT_SECRET_KEY'] = 'frase-secreta'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    return app

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)
api.add_resource(VistaTareas, '/api/tasks') 
api.add_resource(VistaTarea, '/api/tasks/<int:id_task>') 
api.add_resource(VistaSignIn, '/api/auth/signup')
api.add_resource(VistaLogIn, '/api/auth/login')

