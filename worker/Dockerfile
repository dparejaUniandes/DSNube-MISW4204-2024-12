FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1
ENV DEBUG=true

# CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--limit-request-line", "26214400", "--limit-request-field_size", "26214400", "--keep-alive", "5", "app:app"]