# fomento-api

## first time execution
python manage.py makemigrations

python manage.py migrate


## admin account
python manage.py createsuperuser

samguill@inkacode.pe

samguill

_password


## to load data into the database
python manage.py load_fomento_csv --year 2023


## db access
bd: fomentodb
user: fomento
pwd: dbpass

## Buil/Rebuild web image
docker-compose stop

docker-compose build web

docker-compose up -d


## export data
python manage.py dumpdata > dump/dump_`date +%Y%m%d`.json

## import data
python manage.py loaddata dump/dump_`date +%Y%m%d`.json



