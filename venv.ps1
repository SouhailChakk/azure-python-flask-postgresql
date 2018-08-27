#!/bin/bash

# Recreate the virtual environment and reinstall libs on Windows.
# Chris Joakim, 2018/08/27

python --version

echo 'creating virtual environment...'
python -m venv .
.\Scripts\Activate.ps1

echo 'installing/upgrading libs...'
pip install --upgrade pip-tools

pip install --upgrade arrow
pip install --upgrade docopt
pip install --upgrade Flask
pip install --upgrade Jinja2
pip install --upgrade psycopg2
pip install --upgrade SQLAlchemy

echo 'pip freeze to requirements.txt...'
pip freeze > requirements_win.txt

echo 'done'
