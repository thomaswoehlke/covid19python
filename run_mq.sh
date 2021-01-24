#!/usr/bin/env bash
export FLASK_ENV=development
export FLASK_APP=covid19python_mq
pip install -e .
flask run
