#!/usr/bin/env bash
export FLASK_ENV=development
export FLASK_APP=yourapplication
pip install -e .
flask run
