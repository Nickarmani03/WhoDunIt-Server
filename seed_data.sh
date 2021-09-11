#!/bin/bash

rm -rf whodunitapi/migrations
rm db.sqlite3
python manage.py makemigrations whodunitapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata players
python manage.py loaddata movies
python manage.py loaddata genres
python manage.py loaddata movie_nights
python manage.py loaddata suspects
