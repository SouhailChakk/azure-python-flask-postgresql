#!/bin/bash

az container create --resource-group FlaskFun --name python-flask-postgresql27a --image cjoakimacr.azurecr.io/python-flask-postgresql:latest --cpu 1 --memory 1 --registry-username cjoakimacr  --registry-password +h3ThJCPgdWmA4SgZr439mn2dTS3n791  --dns-name-label python-flask-postgresql27a --ports 80 --environment-variables 'PORT=80' 'AZURE_PSQL_DB_NAME=olympics' 'AZURE_PSQL_DB_NAMESPACE=cjoakimpsql' 'AZURE_PSQL_DB_PASS=big.DATA-18' 'AZURE_PSQL_DB_PORT=5432' 'AZURE_PSQL_DB_SERVER=cjoakimpsql.postgres.database.azure.com' 'AZURE_PSQL_DB_SERVER_ADMIN=cjoakim@cjoakimpsql' 'AZURE_PSQL_DB_SSLMODE=require' 'AZURE_PSQL_DB_USER=cjoakim'

