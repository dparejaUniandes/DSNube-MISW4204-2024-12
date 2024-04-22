from flask import Flask, send_from_directory
from flask_restful import Api
from views import *
from models import db
from os import environ
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'secret-phrase'
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024

app_context = app.app_context()
app_context.push()

jwt = JWTManager(app)

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(TasksView, '/api/tasks') 
api.add_resource(TaskView, '/api/tasks/<int:id_task>') 
api.add_resource(SignUpView, '/api/auth/signup')
api.add_resource(LogInView, '/api/auth/login')

@app.route("/videos/<path:name>")
def download_file(name):
    return send_from_directory(
        '/home/ing_manu/remote-videos', name, as_attachment=True
    )