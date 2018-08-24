#!/bin/bash

# Recreate the virtual environment and reinstall libs.
# Chris Joakim, 2018/08/24

echo 'deleting previous venv...'
rm -rf bin/
rm -rf lib/
rm -rf include/
rm -rf man/

echo 'creating new virtual environment...'
python3 -m venv .
source bin/activate
python --version

echo 'installing/upgrading libs...'
pip install --upgrade pip-tools

pip install --upgrade arrow
pip install --upgrade docopt
pip install --upgrade Flask
pip install --upgrade Jinja2
pip install --upgrade psycopg2
pip install --upgrade SQLAlchemy

echo 'pip freeze to requirements.txt...'
pip freeze > requirements.txt

echo 'done'
