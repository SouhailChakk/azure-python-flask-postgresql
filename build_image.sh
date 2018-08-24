#!/bin/bash

# Recreate the virtual environment and reinstall libs.
# Requires Python 3
# Chris Joakim, 2018/08/24

rm -rf __pycache__
rm -rf tmp/
rm txt_merged.txt
# rm pip-selfcheck.json
# rm pyvenv.cfg

docker build -t cjoakim/python-flask-postgresql . 

docker image ls | grep python-flask-postgresql

echo 'done'
