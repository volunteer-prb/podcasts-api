FROM python:3.10
ENV VENV=/opt/venv
RUN python3 -m venv $VENV
ENV PATH="$VENV/bin:$PATH"
RUN pip install --upgrade pip
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY app/ /app/app/
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app
CMD ["flask", "run", "--host=0.0.0.0"]
