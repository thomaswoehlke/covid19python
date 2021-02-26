#!/usr/bin/env bash

#
# TODO #156 run_web.sh - this is not yet working
#


. venv/bin/activate
export FLASK_ENV=development
export FLASK_APP=covid19
pip install -e .
flask run
# python covid19.run_web
