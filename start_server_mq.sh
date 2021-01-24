#!/usr/bin/env bash

python app_mq.py
celery -A app_mq.celery worker  -l INFO
