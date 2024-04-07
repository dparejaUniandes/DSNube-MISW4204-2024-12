from flask_restful import Resource
from ..modelos import *
from sqlalchemy.exc import IntegrityError


class VistaLogIn(Resource):
    def post(self):
        return {'mensaje':'Hola desde el LogIn'}, 200
    
class VistaSignIn(Resource):
    
    def post(self):
        return {"mensaje": 'Hola desde SignIn'}


class VistaTareas(Resource):

    def get(self):
        return {'mensaje':'Recuperar todas las tareas'}, 200
    
    def post(self):
        return {'mensaje':'Crear tarea de edicion'}, 201
    
class VistaTarea(Resource):

    def get(self, id_task):
        return {'mensaje':'Recuperar tarea ' + str(id_task)}, 200
    
    def delete(self, id_task):
        return {'mensaje':'Eliminar tarea ' + str(id_task)}, 200
