FROM python:3.6-alpine

RUN apk update && apk add libpq
RUN apk add python3-dev
RUN apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY config.py ./
COPY pastebin-app.py ./
COPY boot.sh ./

RUN chmod +x boot.sh

ENV FLASK_APP app.py

# store sqlite data in /data
RUN mkdir /data

# store pastes in /pastes
RUN mkdir /pastes

EXPOSE 5001
ENTRYPOINT ["./boot.sh"]