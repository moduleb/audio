FROM python:3.10-slim

WORKDIR /code
COPY ../test2_audio/requirements.txt .
RUN pip install -r requirements.txt
COPY ../test2_audio .
CMD export FLASK_ENV=production && python run.py