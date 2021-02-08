#!/usr/bin/env bash

#
# Start the gaphor UML Application
#
echo "Start the gaphor UML Application"
. venv/bin/activate
pip install -r requirements.txt
gaphor