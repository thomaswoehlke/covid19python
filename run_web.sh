#!/usr/bin/env bash

. venv/bin/activate
export FLASK_ENV=development
export FLASK_APP=covid19
pip install -e .
flask run


#python covid19.__init__

