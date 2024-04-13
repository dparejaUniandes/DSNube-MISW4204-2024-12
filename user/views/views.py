from flask_restful import Resource
from ..models import *
from flask import request
from sqlalchemy import exc
import re

class LogInView(Resource):
    def post(self):
        username=request.json["username"]
        password=request.json["password"]
        user = User.query.filter(User.username == username).first()
        return {'mensaje':'Hola desde el LogIn', "password": user.password}, 200
    
class SignUpView(Resource):
    
    def post(self):
        try:
            username = str(request.json["username"])
            password1= str(request.json["password1"])
            password2= str(request.json["password2"])
            email= str(request.json["email"])
            if password1 != password2:
                return {"message": 'Password must be the same'}, 409
            if not re.search('((?=.*\d)(?=.*[A-Z])(?=.*[a-z])\w.{5,18}\w)', password1):
                 return {"message": 'Password unsafe, must contain a number, uppercase, lowercase and minimum 7 characters'}, 400
            new_user = User(username=username, 
                            password=password1,  
                            email=email)
            access_token = 1 
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError:
            return {"message": 'Email or username already exists'}, 422
        except KeyError:
            return {"message": 'All fields are needed'}, 400
        except Exception as e:
            return {"message": 'Internal server error', "error": e}, 500
        return {"message": 'User created successfully', "access_token": access_token}

class TasksView(Resource):

    def get(self):
        return {'mensaje':'Recuperar todas las tareas'}, 200
    
class TaskView(Resource):

    def get(self, id_task):
        return {'mensaje':'Recuperar tarea ' + str(id_task)}, 200
    
    def delete(self, id_task):
        return {'mensaje':'Eliminar tarea ' + str(id_task)}, 200