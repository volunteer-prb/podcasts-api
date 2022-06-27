FROM python:3.10

LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.revision="${SCM_REF}"
LABEL org.opencontainers.image.source="git@github.com:volunteer-prb/podcasts-api.git"
LABEL org.opencontainers.image.title="Navalny Team Podcast API"
LABEL org.opencontainers.image.description="Podcast Publisher application"
LABEL org.opencontainers.image.authors="TODO: fill authors"
LABEL org.opencontainers.image.vendor="Navalny Team"
LABEL org.opencontainers.image.licenses="(C) Copyright 2022 Navalny Team"

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
CMD ["celery", "--app=app.downloader", "worker", "--loglevel=INFO", "-Q", "media_manager_tasks"]
