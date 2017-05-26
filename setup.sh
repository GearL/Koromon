pip install virtualenv
virtualenv env
source ./env/bin/activate
pip install -r requirements.txt
cp .env.sample .env
nano .env
honcho run python manage.py syncdb
honcho run python manage.py runserver --port 8080