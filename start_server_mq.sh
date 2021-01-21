#!/usr/bin/env bash

python server_mq.py

# celery 4
celery -A server_mq.celery --loglevel=info worker

# celery 5
#celery -A server_mq.celery worker
