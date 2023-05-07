#!/bin/bash
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata product.json
echo "----------Done Migration and installing fixtures---------"

python manage.py runserver 0.0.0.0:8000