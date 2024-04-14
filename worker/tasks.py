from celery import Celery
import cv2

celery_app = Celery('tasks', broker='redis://redis_broker:6379')

@celery_app.task(name='process_video')
def process_video(video_path, filename, task_id):
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
        output_video = cv2.VideoWriter(f"videos/processed_{filename}", fourcc, fps, (new_width, new_height))

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

    finally:
        video.release()
        output_video.release()
        cv2.destroyAllWindows()