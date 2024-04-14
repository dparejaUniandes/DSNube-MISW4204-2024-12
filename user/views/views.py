import re
import os
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.utils import secure_filename
from hashlib import sha256
from models import *
import cv2

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
        
        if 'video' not in request.files:
            return {'message': 'No video file provided'}, 400
        
        video_file = request.files['video']
        if video_file.filename == '':
            return {'message': 'No video file selected'}, 400
        
        filename = secure_filename(video_file.filename)
        pre_processed_filename = f"pre_processed_{filename}"
        video_path = os.path.join('videos', pre_processed_filename)
        video_file.save(video_path)

        new_task = Task(
            name= pre_processed_filename,
            user_id= current_user_id,
            video_path= video_path
        )
        
        # Ruta del logo
        logo_path = 'logo.png'

        try:
            # Cargar el video
            video = cv2.VideoCapture(video_path)

            # Cargar el logo
            logo = cv2.imread(logo_path)

            # Obtener las propiedades del video
            fps = video.get(cv2.CAP_PROP_FPS)
            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Calcular el nuevo ancho y alto para una relación de aspecto de 16:9
            new_width = width
            new_height = int(width * 9 / 16)

            # Calcular los márgenes superior e inferior para centrar el video
            top_margin = int((height - new_height) / 2)
            bottom_margin = height - new_height - top_margin

            # Redimensionar el logo al tamaño del video recortado
            logo = cv2.resize(logo, (new_width, new_height))

            # Crear el objeto de escritura de video
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            output_video = cv2.VideoWriter('video_recortado.mp4', fourcc, fps, (new_width, new_height))

            # Calcular la duración máxima en frames (20 segundos)
            max_duration = int(fps * 20)

            # Procesar el video
            output_video.write(logo)
            frame_count = 0
            while frame_count < max_duration:
                ret, frame = video.read()
                if not ret:
                    break

                # Recortar el video a la relación de aspecto de 16:9
                cropped_frame = frame[top_margin:top_margin+new_height, :]

                # Escribir el frame en el video de salida
                output_video.write(cropped_frame)

                frame_count += 1
            output_video.write(logo)

        finally:
            # Liberar los recursos
            video.release()
            output_video.release()
            cv2.destroyAllWindows()

        db.session.add(new_task)
        db.session.commit()

        return {"message": 'Task created successfully'}, 201
    
class TaskView(Resource):

    @jwt_required()
    def get(self, id_task):
        task = Task.query.filter(Task.id == id_task).first()

        task_schema = TaskSchema()

        return task_schema.dump(task)
    
    @jwt_required()
    def delete(self, id_task):
        task = Task.query.filter(Task.id == id_task).first()
        if task:
            db.session.delete(task)
            db.session.commit() 
            return {'message':'Task deleted successfully ' + str(id_task)}, 200
        else:
            return {'message':'Task not deleted ' + str(id_task)}, 200