from tempfile import NamedTemporaryFile
import cv2
import requests
from requests.exceptions import RequestException
from os import environ, remove
from models import *
from flask import request

from google.cloud import storage
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from flask_restful import Resource

# References:
# Get JSON messages: https://cloud.google.com/pubsub/docs/samples/pubsub-subscriber-async-pull-custom-attributes?hl=es-419#pubsub_subscriber_async_pull_custom_attributes-python


project_id = "curso-nube-202412"
subscription_id = "fpv-subscription"
# Esta variable se puede poner en streaming_pull_future.result(timeout=timeout), pero quite la parte 
# de los parentesis para que no se cierre el programa despues de 5 segundos
timeout = 5.0

# TOPIC
# subscriber = pubsub_v1.SubscriberClient()
# subscription_path = subscriber.subscription_path(project_id, subscription_id)

class ProcessVideoView(Resource):
    def post(self):
        video_path=request.json["video_path"]
        filename=request.json["filename"]
        task_id=request.json["task_id"]

        # REMOVE
        task = Task.query.filter(Task.id == task_id).first()

        task.status = TaskStatus.PROCESSED
        task.name = f"processed_{filename}"
        task.video_path = f"videos/processed_{filename}"

        db.session.commit() 
        # REMOVE UNTIL HERE
        
        #return process_video(video_path, filename, task_id)
        return {"video_path": video_path, "filename": filename, "task_id": task_id}, 200
    
# TOPIC
# def callback(message: pubsub_v1.subscriber.message.Message) -> None:
#     print(f"Received {message.data!r}.")
#     if message.attributes:
#         print("Attributes:")
#         for key in message.attributes:
#             if key == 'video_path':
#                 video_path = message.attributes.get(key)
#                 print(f"{key}: {video_path}")
#             elif key == 'filename':
#                 filename = message.attributes.get(key)
#                 print(f"{key}: {filename}")
#             elif key == 'task_id':
#                 task_id = message.attributes.get(key)
#                 print(f"{key}: {task_id}")
#     message.ack()
#     process_video(video_path, filename, task_id)

def process_video(video_path, filename, task_id):
    print("*****, ", video_path)
    logo_path = 'videos/logo.png'

    bucket_name = 'bucket-fpv'

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    temp_video_path = '/tmp/' + filename

    # For answer to topic
    message, status = {'message':'Successful login'}, 200

    try:
        blob = bucket.blob("videos/pre_processed_" + filename)
        blob.download_to_filename(temp_video_path)

        video = cv2.VideoCapture(temp_video_path)
        logo = cv2.imread(logo_path)

        fps = video.get(cv2.CAP_PROP_FPS)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        new_width = width
        new_height = int(width * 9 / 16)

        top_margin = int((height - new_height) / 2)

        logo = cv2.resize(logo, (new_width, new_height))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        with NamedTemporaryFile(delete=False, suffix='.mp4') as temp_output:
            output_video = cv2.VideoWriter(temp_output.name, fourcc, fps, (new_width, new_height))
            max_duration = int(fps * 20)
            output_video.write(logo)
            frame_count = 0
            while frame_count < max_duration:
                ret, frame = video.read()
                if not ret:
                    break
                cropped_frame = frame[top_margin:top_margin+new_height, :]
                output_video.write(cropped_frame)
                frame_count += 1
            output_video.write(logo)
            output_video.release()
            
            processed_blob_name = f"videos/processed_{filename}"
            processed_blob = bucket.blob(processed_blob_name)
            processed_blob.upload_from_file(temp_output, rewind=True)

        # url = f"http://35.239.86.185:8080/api/tasks/{task_id}"
        # data = {
        #     "name": f"processed_{filename}",
        #     "video_path": f"videos/processed_{filename}"
        # }

        # try:
        #     response = requests.put(url, json=data)
        #     response.raise_for_status()
        #     print(f"Tarea {task_id} actualizada exitosamente")
        # except RequestException as e:
        #     print(f"Error al actualizar la tarea {task_id}: {str(e)}")

        task = Task.query.filter(Task.id == task_id).first()

        task.status = TaskStatus.PROCESSED
        task.name = f"processed_{filename}"
        task.video_path = f"videos/processed_{filename}"

        db.session.commit() 
        

    finally:
        # Borrar los archivos temporales
        remove(temp_video_path)
        remove(temp_output.name)
        
        video.release()
        output_video.release()
        cv2.destroyAllWindows()
        return message, status

# TOPIC
# streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
# print(f"Listening for messages on {subscription_path}..\n")

# # Wrap subscriber in a 'with' block to automatically call close() when done.
# with subscriber:
#     try:
#         # When `timeout` is not set, result() will block indefinitely,
#         # unless an exception is encountered first.
#         streaming_pull_future.result()
#     except TimeoutError:
#         streaming_pull_future.cancel()  # Trigger the shutdown.
#         streaming_pull_future.result()  # Block until the shutdown is complete.