#!/usr/bin/env bash

#
# TODO ... this is not yet working
#


. venv/bin/activate
export FLASK_ENV=development
export FLASK_APP=covid19
pip install -e .
flask run


#python covid19.__init__

