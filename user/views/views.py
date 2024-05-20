import json
import re
import os
import uuid
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.utils import secure_filename
from hashlib import sha256
from models import *
from os import environ
from google.cloud import storage
from google.cloud import pubsub_v1

# References:
# Publish message: https://cloud.google.com/pubsub/docs/samples/pubsub-quickstart-publisher?hl=es-419
# https://stackoverflow.com/questions/51149091/publish-non-string-message-in-cloud-pubsub

project_id = "curso-nube-202412"
topic_id = "fpv-topic"

# TOPIC
# publisher = pubsub_v1.PublisherClient()
# topic_path = publisher.topic_path(project_id, topic_id)

class LogInView(Resource):
    def post(self):
        username=request.json["username"]
        password=sha256(request.json["password"].encode('utf-8')).hexdigest()
        user = User.query.filter(User.username == username, User.password == password).first()
        if user is None:
            return {'message':'Verify username or password'}, 404
        token = create_access_token(identity=user.id)
        return {'message':'Successful login', "token": token}, 200
    
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
            password1 = sha256(password1.encode('utf-8')).hexdigest()
            new_user = User(username=username, 
                            password=password1,  
                            email=email)
            db.session.add(new_user)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()
            return {"message": 'Email or username already exists'}, 422
        except KeyError:
            return {"message": 'All fields are needed'}, 400
        except Exception as e:
            db.session.rollback()
            return {"message": 'Internal server error', "error": e}, 500
        return {"message": 'User created successfully'}, 201

class TasksView(Resource):

    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()

        tasks = Task.query.filter(Task.user_id == current_user_id).all()

        task_schema = TaskSchema()

        return [task_schema.dump(task) for task in tasks]
    
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        _uuid = str(uuid.uuid4())
        
        if 'video' not in request.files:
            return {'message': 'No video file provided'}, 400
        
        video_file = request.files['video']
        if video_file.filename == '':
            return {'message': 'No video file selected'}, 400
        
        filename = secure_filename(video_file.filename)
        pre_processed_filename = f"pre_processed_{_uuid}_{filename}"
        video_path = os.path.join('videos', pre_processed_filename)

        bucket_name = 'bucket-fpv'

        # STORAGE
        # storage_client = storage.Client()
        # bucket = storage_client.bucket(bucket_name)
        # blob = bucket.blob(video_path)
        # blob.upload_from_file(video_file)
        # video_url = blob.public_url
        video_url = "blob.public_url"

        new_task = Task(
            name = pre_processed_filename,
            user_id = current_user_id,
            video_path = video_url
        )

        db.session.add(new_task)
        db.session.commit()

        try:
            record = {
                'video_path': video_path,
                'filename': f"{_uuid}_{filename}",
                'task_id': str(new_task.id)
            }
            data = json.dumps(record).encode("utf-8")
            # TOPIC
            # future = publisher.publish(topic_path, data, **record)
            # print(f'published message id {future.result()}')
            return {"message": 'Task created successfully'}, 201
        except Exception as e:
            print(f"Error al enviar la tarea a Celery: {str(e)}")
            return {"message": 'Error creating task'}, 500
    
class TaskView(Resource):

    @jwt_required()
    def get(self, id_task):
        task = Task.query.filter(Task.id == id_task).first()

        task_schema = TaskSchema()

        return task_schema.dump(task)
    
    def put(self, id_task):
        task = Task.query.filter(Task.id == id_task).first()

        task.status = TaskStatus.PROCESSED
        task.name = request.json["name"]
        task.video_path = request.json["video_path"]

        #db.session.update(task)
        db.session.commit() 
    
    @jwt_required()
    def delete(self, id_task):
        task = Task.query.filter(Task.id == id_task).first()
        if task:
            db.session.delete(task)
            db.session.commit() 
            return {'message':'Task deleted successfully ' + str(id_task)}, 200
        else:
            return {'message':'Task not deleted ' + str(id_task)}, 200