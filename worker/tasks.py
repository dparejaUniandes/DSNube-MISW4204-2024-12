from celery import Celery
import cv2
import requests
from requests.exceptions import RequestException
from os import environ
from google.cloud import storage

celery_app = Celery('tasks', broker="redis://10.128.0.20:6379")

@celery_app.task(bind=True, name='process_video')
def process_video(self, video_path, filename, task_id):
    print("******, ", video_path)
    logo_path = 'videos/logo.png'

    try:
        video = cv2.VideoCapture(video_path)
        logo = cv2.imread(logo_path)

        fps = video.get(cv2.CAP_PROP_FPS)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        new_width = width
        new_height = int(width * 9 / 16)

        top_margin = int((height - new_height) / 2)

        logo = cv2.resize(logo, (new_width, new_height))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_video = cv2.VideoWriter(f"/home/ing_manu/remote-videos/processed_{filename}", fourcc, fps, (new_width, new_height))

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

        url = f"http://34.132.255.5:8080/api/tasks/{task_id}"
        data = {
            "name": f"processed_{filename}",
            "video_path": f"videos/processed_{filename}"
        }
        
        try:
            response = requests.put(url, json=data)
            response.raise_for_status()
            print(f"Tarea {task_id} actualizada exitosamente")
        except RequestException as e:
            print(f"Error al actualizar la tarea {task_id}: {str(e)}")
            raise self.retry(exc=e, countdown=60)

    finally:
        video.release()
        output_video.release()
        cv2.destroyAllWindows()