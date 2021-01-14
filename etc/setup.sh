#!/usr/bin/env bash

deactivate
rm -rf venv
#python3 -m venv venv
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
