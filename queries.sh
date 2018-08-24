#!/bin/bash

rm tmp/*.txt

python main.py medalists_in_games 2000 summer > tmp/medalists_in_games_2000_summer.txt
python main.py medalists_in_games 2016 summer > tmp/medalists_in_games_2016_summer.txt
python main.py medalists_in_games 2014 winter > tmp/medalists_in_games_2014_winter.txt


python main.py marathoners_in_year 1976 m > tmp/marathoners_in_year_1976_m.txt
python main.py marathoners_in_year 1984 f > tmp/marathoners_in_year_1984_f.txt

echo 'done'
