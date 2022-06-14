FROM python:3.10
ENV VENV=/opt/venv
RUN python3 -m venv $VENV && \
    apt-get update && \
    apt-get install ffmpeg libsm6 libxext6 -y
ENV PATH="$VENV/bin:$PATH"
RUN pip install --upgrade pip
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY app/ /app/app
ENV PYTHONUNBUFFERED=1
CMD ["celery", "--app=app.publisher", "worker", "--loglevel=INFO", "-Q publisher_tasks"]
