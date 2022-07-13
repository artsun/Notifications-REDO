FROM python:latest

VOLUME conf-logs-volume

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD requirements.txt /app/

RUN pip install -r requirements.txt

ADD app /app/
ADD conf-logs-volume /conf-logs-volume/
