
# Data Access Object (DAO) for this app
# Chris Joakim, 2018/08/24

import csv
import json
import os
import sys
import time
import traceback

import psycopg2


class Dao(object):

    def __init__(self):
        self.host = None
        self.port = None
        self.user = None
        self.dbname = None
        self.passwd = None
        self.sslmode = None
        self.conn = None
        self.cursor = None
        try:
            self.host    = os.environ['AZURE_PSQL_DB_SERVER']
            self.port    = os.environ['AZURE_PSQL_DB_PORT']
            self.user    = os.environ['AZURE_PSQL_DB_SERVER_ADMIN']
            self.dbname  = os.environ['AZURE_PSQL_DB_NAME']
            self.passwd  = os.environ['AZURE_PSQL_DB_PASS']
            self.sslmode = os.environ['AZURE_PSQL_DB_SSLMODE'] # disable, allow, prefer, require, verify-ca, verify-full

            # Construct connection string
            conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(
                self.host, self.user, self.dbname, self.passwd, self.sslmode)
            print("Dao.__init__ conn_string: {}".format(conn_string))

            self.conn = psycopg2.connect(conn_string) 
            print("Dao.__init__ Connection established")

            self.cursor = self.conn.cursor()
            print("Dao.__init__ Cursor obtained")

            sql = 'SELECT * FROM competitors limit 8;'
            print("Dao.__init__ executing sql: {}".format(sql))

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

    def query1(self, limit):
        objects, cursor = list(), None
        try:
            cursor = self.conn.cursor()
            sql = 'SELECT id, name FROM competitors limit {};'.format(str(limit))
            print("executing sql: {}".format(sql))
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                obj = dict()
                obj['id'] = row[0]
                obj['name'] = row[1]
                objects.append(obj)
        except:
            print(sys.exc_info())
            traceback.print_exc()
        finally:
            print('closing cursor')
            # if conn:
            #     conn.commit()
            if cursor:
                cursor.close()
                print('cursor closed')
            return objects

    def close(self):
        print('Dao.close...')
        try:
            if self.conn:
                self.conn.close()
                print('Dao.closed')
        except:
            print(sys.exc_info())
            traceback.print_exc()
