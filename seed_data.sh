#!/bin/bash

rm -rf whodunitapi/migrations
rm db.sqlite3
python3 manage.py makemigrations whodunitapi
python3 manage.py migrate
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata players
python3 manage.py loaddata suspects
python3 manage.py loaddata genres
python3 manage.py loaddata movies
python3 manage.py loaddata movie_nights