
import datetime
import json
import os
import platform
import sys
import time

import arrow

from flask import Flask, render_template, request, send_file
from flask import Response

from dao import Dao


print('__name__: {}'.format(__name__))
app = Flask(__name__, static_url_path='')

port = int(os.getenv("PORT", default=80))
print('port: {}'.format(port))

def root_dir():
    return os.path.abspath(os.path.dirname(__file__))

@app.before_first_request
def before_first_request():
    try:
        print('before_first_request')
    except Exception as e:
        app.logger.error(str(e))

@app.before_request
def before_request():
    try:
        pass
    except Exception as e:
        app.logger.error(str(e))

@app.route('/')
def index_route():
    data = dict()
    data['date'] = datetime.datetime.now()
    data['time'] = time.time()
    return render_template('index.html', data=data)

@app.route('/env')
def images_list_route():
    env_vars = list()
    for env_var_name in sorted(os.environ):
        env_var = dict()
        env_var['name'] = env_var_name
        env_var['value'] = os.getenv(env_var_name)
        env_vars.append(env_var)
    return render_template('env.html', env_vars=env_vars)

# http://localhost:3000/olympic_marathoners?year=1976&sex=m
# http://localhost:3000/olympic_marathoners?year=1984&sex=f
@app.route('/olympic_marathoners')
def olympic_marathoners():
    year = request.args['year']
    sex = request.args['sex']
    dao = Dao()
    results = dao.marathoners_in_year(year, sex)
    dao.close()
    return render_template('marathoners.html', results=results)

# curl -v 'http://localhost:3000/olympic_marathoners_json?year=1992&sex=f'
@app.route('/olympic_marathoners_json')
def olympic_marathoners_json():
    year = request.args['year']
    sex = request.args['sex']
    dao = Dao()
    results = dao.marathoners_in_year(year, sex)
    dao.close()
    jstr = json.dumps(results, sort_keys=False, indent=2)
    return Response(jstr, mimetype='application/json')


# private

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print('run port: {}'.format(port))
    app.run(host='0.0.0.0', port=port)
