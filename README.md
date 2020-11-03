# Wiztute Project
Wiztute backend server

## Wiztute Backend Server

## Contributors
* Vishnu P S

## Django-admin superuser

| Key | Value |
|----------|------------|
| Email | vishnu@gmail.com | 
| Password| krisiz-462 |

## Setup
* virtualenv venv -p python3

* source ./venv/bin/activate
	
* pip3 install -r requirements.txt

* python manage.py makemigrations --settings=fyp_be.settings

* python manage.py migrate --settings=fyp_be.settings

* python manage.py runserver --settings=fyp_be.settings 8080

* python manage.py runserver --settings=fyp_be.settings 8080 --insecure

* python manage.py runserver --settings=fyp_be.settings 0.0.0.0:8080  --> when on server

* python manage.py runserver --settings=fyp_be.settings 0.0.0.0:8080 --insecure

* python manage.py runsslserver --certificate /etc/letsencrypt/live/wiztech.co.in/fullchain.pem --key /etc/letsencrypt/live/wiztech.co.in/privkey.pem --settings=wiztute.settings 0.0.0.0:8080

* chmod +x start.sh








