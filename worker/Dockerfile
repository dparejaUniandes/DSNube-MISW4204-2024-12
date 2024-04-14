FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV CELERY_BROKER_URL=redis://redis_broker:6379

# CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]