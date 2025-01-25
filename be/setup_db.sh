#!/bin/bash
python manage.py migrate --noinput
python manage.py loaddata initial_data.json
python manage.py runserver 0.0.0.0:8000

# python manage.py dumpdata --indent 2 > initial_data.json
