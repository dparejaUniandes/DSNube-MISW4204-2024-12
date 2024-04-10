from flask_restful import Resource
from ..models import *
from sqlalchemy.exc import IntegrityError
from celery import Celery

import json                                                     
import os
from flask import Flask, request
from werkzeug import secure_filename

#from ...worker import read_video

celery_app = Celery(__name__, broker='redis://localhost:6379:/0')


class LogInView(Resource):
    def post(self):
        return {'mensaje':'Hola desde el LogIn'}, 200
    
class SignInView(Resource):
    
    def post(self):
        return {"mensaje": 'Hola desde SignIn'}


class TasksView(Resource):

    def get(self):
        return {'mensaje':'Recuperar todas las tareas'}, 200
    
    @celery_app.task(name='upload_video')
    def upload_video(self):

        #video = request.files["video"]

        #check this flask documentation to upload files:
        #https://flask.palletsprojects.com/en/3.0.x/patterns/fileuploads/

        #check this other implementation:
        #https://stackoverflow.com/questions/56766072/post-method-to-upload-file-with-json-object-in-python-flask-app
        uploaded_file = request.files['document']
        data = json.load(request.files['data'])
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join('path/where/to/save', filename))
        print(data)

        #when to add this type of code?
       # upload_video.apply_async(args=args, queue='video_upload')

        return {'mensaje':'Crear tarea de edicion'}, 201
    
class TaskView(Resource):

    def get(self, id_task):
        return {'mensaje':'Recuperar tarea ' + str(id_task)}, 200
    
    def delete(self, id_task):
        return {'mensaje':'Eliminar tarea ' + str(id_task)}, 200
