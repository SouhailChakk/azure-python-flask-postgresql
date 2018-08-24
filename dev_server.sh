#!/bin/bash

# Bash script to start the Flask web app in development mode
# with auto restarts upon code changes.
# Chris Joakim, 2018/08/24

export FLASK_APP=app.py

python -m flask run --debugger --port $PORT
