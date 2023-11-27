# https://hub.docker.com/_/python
FROM python:3.8-slim

# Copy local code to the container image.
COPY . /app
WORKDIR /app

# Install production dependencies.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.

EXPOSE 8080

# for production
CMD exec gunicorn --bind 0.0.0.0:8080 --workers 1 --threads 8 app:app