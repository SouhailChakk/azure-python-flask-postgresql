"""
Usage:
  python main.py query_azure_olympics_db
  python main.py query_azure_olympics_db_orm
  python main.py dao_query1
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

VERSION = 'v20180824'

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


if __name__ == "__main__":

    start_time = time.time()

    if len(sys.argv) > 1:
        func = sys.argv[1].lower()

        if func == 'dao_query1':
            dao = Dao()
            for i in range(3, 5):
                print('limit: {}'.format(i))
                objects = dao.query1(i)
                print(json.dumps(objects, sort_keys=True, indent=2))
            dao.close()

        elif func == 'query_azure_olympics_db':
            query_azure_olympics_db()

        elif func == 'query_azure_olympics_db_orm':
            query_azure_olympics_db_orm()
        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
        print_options('Error: no function argument provided.')
