
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
        except:
            print(sys.exc_info())
            traceback.print_exc()

    def medalists_in_games(self, year, season):
        attr_names = 'id,name,sex,team,noc,games,year,season,city,sport,event,metal,medal_value'
        attr_list = attr_names.split(',')
        limit = str(2000)
        objects, cursor = list(), None
        try:
            y = str(int(year))
            s = 'summer'
            if str(season).lower() == 'winter':
                s = 'winter'
            cursor = self.conn.cursor()
            sql = "SELECT {} FROM competitors where year = {} and season = '{}' and medal_value > 0 order by event, medal_value limit {};".format(
                attr_names, y, s, limit)
            print("executing sql: {}".format(sql))
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                obj = dict()
                for idx, attr in enumerate(attr_list):
                    obj[attr] = row[idx]
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
            print('returning {} objects'.format(len(objects)))
            return objects


    def marathoners_in_year(self, year, sex, min_medal_value=1):
        attr_names = 'id,name,sex,team,noc,games,year,season,city,sport,event,metal,medal_value'
        attr_list = attr_names.split(',')
        limit = str(100)
        objects, cursor = list(), None
        try:
            y = str(int(year))
            s = 'm'
            if str(sex).lower() == 'f':
                s = 'f'
            cursor = self.conn.cursor()
            sql = "select {} from competitors where year = {} and sex = '{}' and event like '%marathon%' and medal_value >= {} order by medal_value desc limit {};".format(
                attr_names, y, s, min_medal_value, limit)
            print("executing sql: {}".format(sql))
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                obj = dict()
                for idx, attr in enumerate(attr_list):
                    obj[attr] = row[idx]
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
            print('returning {} objects'.format(len(objects)))
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
