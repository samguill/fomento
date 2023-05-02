# fomento-api

## admin account
python manage.py createsuperuser
samguill@inkacode.pe
samguill
_password

## db access
bd: fomentodb
user: fomento
pwd: dbpass

## Buil/Rebuild web image
docker-compose stop
docker-compose build web
docker-compose up -d

## to load data into the database
python manage.py load_fomento_csv --year 2023

## export data
python manage.py dumpdata > dump/dump_`date +%Y%m%d`.json

## import data
python manage.py loaddata dump/dump_`date +%Y%m%d`.json


## first time execution
python manage.py makemigrations

python manage.py migrate


