#!/usr/bin/env bash
export FLASK_ENV=development
export FLASK_APP=covid19python
pip install -e .
flask run
