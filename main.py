"""
Usage:
  python main.py medalists_in_games 2000 summer
  python main.py marathoners_in_year 1976 m
  python main.py gen_container_create_command FlaskFun python-flask-postgresql27a
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import csv
import json
import os
import sys
import time
import traceback

import psycopg2

from dao import Dao

# see http://initd.org/psycopg/docs/
# https://docs.microsoft.com/en-us/azure/postgresql/connect-python

from datetime import datetime

from docopt import docopt

from sqlalchemy import Column, Integer, Sequence, String, Numeric, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

VERSION = 'v20180827'

Base = declarative_base()

class Competitor(Base):
    __tablename__ = 'competitors'

    id          = Column(Integer, primary_key=True)
    name        = Column(String)
    sex         = Column(String)
    age         = Column(Integer)
    height      = Column(Numeric)
    weight      = Column(Numeric)
    team        = Column(String)
    noc         = Column(String)
    games       = Column(String)
    year        = Column(Integer)
    season      = Column(String)
    city        = Column(String)
    sport       = Column(String)
    event       = Column(String)
    metal       = Column(String)
    medal_value = Column(Integer)

    def __repr__(self):
        return '<Competitor id:{} name:{} s:{} a:{} games:{}>'.format(self.id, self.name, self.sex, self.age, self.games)


def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=VERSION)
    print(arguments)

def query_azure_olympics_db():
    conn, cursor = None, None
    try:
        host    = os.environ['AZURE_PSQL_DB_SERVER']
        port    = os.environ['AZURE_PSQL_DB_PORT']
        user    = os.environ['AZURE_PSQL_DB_SERVER_ADMIN']
        dbname  = os.environ['AZURE_PSQL_DB_NAME']
        passwd  = os.environ['AZURE_PSQL_DB_PASS']
        sslmode = os.environ['AZURE_PSQL_DB_SSLMODE'] # disable, allow, prefer, require, verify-ca, verify-full

        # Construct connection string
        conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, passwd, sslmode)
        print("conn_string: {}".format(conn_string))

        conn = psycopg2.connect(conn_string) 
        print("Connection established")

        cursor = conn.cursor()
        print("Cursor obtained")

        sql = 'SELECT * FROM competitors limit 8;'
        print("executing sql: {}".format(sql))

        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
            id   = row[0]
            name = row[1]
            print('{} {}'.format(str(id), name))
    except:
        print(sys.exc_info())
        traceback.print_exc()
    finally:
        if conn:
            conn.commit()
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def query_azure_olympics_db_orm():
    conn, cursor = None, None
    try:
        host    = os.environ['AZURE_PSQL_DB_SERVER']
        port    = os.environ['AZURE_PSQL_DB_PORT']
        user    = os.environ['AZURE_PSQL_DB_SERVER_ADMIN']
        dbname  = os.environ['AZURE_PSQL_DB_NAME']
        passwd  = os.environ['AZURE_PSQL_DB_PASS']
        sslmode = os.environ['AZURE_PSQL_DB_SSLMODE'] # disable, allow, prefer, require, verify-ca, verify-full

        conn_string = "postgresql+psycopg2://{}:{}@{}:{}/{}?sslmode=require".format(user, passwd, host, port, dbname)
        print("conn_string: {}".format(conn_string))
        engine = create_engine(conn_string)
        print('engine created')

        Session = sessionmaker(bind=engine)
        print('session class created')
        session = Session()
        print('session instance created')

        Base.metadata.create_all(engine)
        print('metadata created')

        # 34551|Allyson Michelle Felix
        afelix = session.query(Competitor).filter_by(id=34551).first() 
        print(afelix)
    except:
        print(sys.exc_info())
        traceback.print_exc()
    finally:
        if conn:
            conn.commit()
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def container_create_env_var_names():
    names = list()
    names.append('PORT')
    names.append('AZURE_PSQL_DB_NAME')
    names.append('AZURE_PSQL_DB_NAMESPACE')
    names.append('AZURE_PSQL_DB_PASS')
    names.append('AZURE_PSQL_DB_PORT')
    names.append('AZURE_PSQL_DB_SERVER')
    names.append('AZURE_PSQL_DB_SERVER_ADMIN')
    names.append('AZURE_PSQL_DB_SSLMODE')
    names.append('AZURE_PSQL_DB_USER')
    return names

def gen_container_create_command(rg_name, ci_name):
    print('gen_container_create_command...')
    port_number = 80
    strings = list()
    strings.append('az container create --resource-group ')
    strings.append(rg_name)
    strings.append(' --name {}'.format(ci_name))
    strings.append(' --image cjoakimacr.azurecr.io/python-flask-postgresql:latest')
    strings.append(' --cpu 1 --memory 1')
    strings.append(' --registry-username {} '.format(os.environ['AZURE_CONTAINER_REGISTRY_USER_NAME']))
    strings.append(' --registry-password {} '.format(os.environ['AZURE_CONTAINER_REGISTRY_USER_PASS']))
    strings.append(' --dns-name-label {}'.format(ci_name))
    strings.append(' --ports {}'.format(port_number))
    strings.append(' --environment-variables')

    for name in container_create_env_var_names():
        if name == 'PORT':
            val = port_number
        else:
            val = os.environ[name]
        strings.append(" '{}={}'".format(name, val))

    command = ''.join(strings)
    print(command)

    txt = '#!/bin/bash\n\n{}\n\n'.format(command)
    write('aci.sh', txt)

    txt = '\n{}\n\n'.format(command)
    write('aci.ps1', txt)

def parse_int(s):
    try:
        return str(int(s.strip()))
    except:
        return '-1'

def parse_float(s):
    try:
        return str(float(s.strip()))
    except:
        return '-1'

def parse_str(s):
    try:
        s1 = s.strip()
        if s1 == 'NA':
            s1 = ''
        s1 = s1.replace('"',"")
        s1 = s1.replace("'","")
        s1 = s1.replace(",","")
        s1 = s1.replace("|","")
        return s1
    except:
        return '?'

def medal_value(s):
    # gold, silver, bron
    try:
        s1 = s.strip().lower()
        if s1.startswith('g'):
            return '3'
        if s1.startswith('s'):
            return '2'
        if s1.startswith('b'):
            return '1'
        return '0'
    except:
        return '-1'

def write(outfile, txt):
    with open(outfile, 'w') as f:
        f.write(txt)
        print('file written: {}'.format(outfile))


if __name__ == "__main__":

    start_time = time.time()

    if len(sys.argv) > 1:
        func = sys.argv[1].lower()

        if func == 'medalists_in_games':
            dao = Dao()
            objects = dao.medalists_in_games(sys.argv[2], sys.argv[3])
            print(json.dumps(objects, sort_keys=False, indent=2))
            dao.close()

        elif func == 'marathoners_in_year':
            dao = Dao()
            objects = dao.marathoners_in_year(sys.argv[2], sys.argv[3])
            print(json.dumps(objects, sort_keys=False, indent=2))
            dao.close()
            
        elif func == 'query_azure_olympics_db':
            query_azure_olympics_db()

        elif func == 'query_azure_olympics_db_orm':
            query_azure_olympics_db_orm()

        elif func == 'gen_container_create_command':
            gen_container_create_command(sys.argv[2], sys.argv[3])
        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
        print_options('Error: no function argument provided.')
