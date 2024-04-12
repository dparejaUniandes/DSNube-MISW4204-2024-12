from flask_restful import Resource
from ..models import *

class LogInView(Resource):
    def post(self):
        return {'mensaje':'Hola desde el LogIn'}, 200
    
class SignInView(Resource):
    
    def post(self):
        return {"mensaje": 'Hola desde SignIn'}

class TasksView(Resource):

    def get(self):
        return {'mensaje':'Recuperar todas las tareas'}, 200
    
class TaskView(Resource):

    def get(self, id_task):
        return {'mensaje':'Recuperar tarea ' + str(id_task)}, 200
    
    def delete(self, id_task):
        return {'mensaje':'Eliminar tarea ' + str(id_task)}, 200