#!/usr/bin/env bash

#export FLASK_ENV=development
#export FLASK_APP=app
#pip install -e .
#flask run

. venv/bin/activate
python app_worker.py
