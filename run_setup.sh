#!/usr/bin/env bash

deactivate
echo "--------------------------------------------------"
echo "rm -rf venv"
echo "--------------------------------------------------"
rm -rf venv
#python3 -m venv venv
echo "--------------------------------------------------"
echo "virtualenv venv"
echo "--------------------------------------------------"
virtualenv venv
echo "--------------------------------------------------"
echo ". venv/bin/activate"
echo "--------------------------------------------------"
. venv/bin/activate
export FLASK_ENV=development
export FLASK_APP=covid19
echo "--------------------------------------------------"
echo "FLASK_ENV=$FLASK_ENV"
echo "FLASK_APP=$FLASK_APP"
echo "--------------------------------------------------"
echo "pip install -r requirements.txt"
echo "--------------------------------------------------"
pip install -r requirements.txt
echo "--------------------------------------------------"
echo "pip install -r requirements-tools.txt"
echo "--------------------------------------------------"
pip install -r requirements-tools.txt
echo "--------------------------------------------------"
echo "pip install -e ."
echo "--------------------------------------------------"
pip install -e .
echo "--------------------------------------------------"
echo " DONE"
echo "--------------------------------------------------"
pip-compile requirements/docs.in
pip-compile requirements/tests.in
pip-compile requirements/dev.in
