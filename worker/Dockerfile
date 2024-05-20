FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8081

ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1
ENV DEBUG=true

# CMD ["flask", "run", "--host=0.0.0.0"]
# CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
CMD ["gunicorn", "--bind", "0.0.0.0:8081", "app:app"]