FROM python:3.6-alpine

RUN apk update && apk add libpq
RUN apk add python3-dev
RUN apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev
RUN apk add dos2unix
RUN apk add bash

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app.py ./
COPY config.py ./
COPY boot.sh ./

RUN dos2unix boot.sh
RUN chmod +x boot.sh

ENTRYPOINT ["./boot.sh"]