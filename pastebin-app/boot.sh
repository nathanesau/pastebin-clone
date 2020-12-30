#!/bin/sh
source venv/bin/activate
while true; do
    # create database tables if not exist
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn -b :5001 --access-logfile - --error-logfile - pastebin-app:app
