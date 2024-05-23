# Use the official Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies && force Gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose the port on which the Flask application will run
EXPOSE 8080

# Set the environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1
ENV DEBUG=true

# Run the Flask application
# CMD ["flask", "run", "--host=0.0.0.0", "--debugger"]
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--limit-request-line", "26214400", "--limit-request-field_size", "26214400", "--keep-alive", "5", "app:app"]
