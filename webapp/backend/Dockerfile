FROM docker.io/python:3.10.4-bullseye

ENV FLASK_RUN_HOST=0.0.0.0 \
	FLASK_RUN_PORT=5000
WORKDIR /app

COPY ./webapp/backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY mediamanager /app/mediamanager
COPY ./webapp/backend .

CMD [ "flask", "run" ]
