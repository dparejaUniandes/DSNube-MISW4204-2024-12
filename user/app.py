from flask import Flask
from .models import *
from flask_restful import Api
from .views import *
from config import *

def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['PROPAGATE_EXCEPTIONS'] = True
    return app

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(TasksView, '/api/tasks') 
api.add_resource(TaskView, '/api/tasks/<int:id_task>') 
api.add_resource(SignInView, '/api/auth/signup')
api.add_resource(LogInView, '/api/auth/login')

