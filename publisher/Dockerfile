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
COPY src/ /app/code/
WORKDIR /app/code/
ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
