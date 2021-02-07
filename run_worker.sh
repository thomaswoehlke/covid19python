#!/usr/bin/env bash

#
# TODO #157 run_worker.sh - this is not yet working
#

#export FLASK_ENV=development
#export FLASK_APP=app
#pip install -e .
#flask run

. venv/bin/activate
python app_worker
