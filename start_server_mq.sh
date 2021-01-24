#!/usr/bin/env bash

python app.py
#celery -A app_mq.celery worker  -l INFO
