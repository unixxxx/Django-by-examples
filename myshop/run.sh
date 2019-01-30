cd src  &&
(rabbitmq-server &) &&
(celery -A myshop worker -l info &) &&
(pipenv run python manage.py runserver &)