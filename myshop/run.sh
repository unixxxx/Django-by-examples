cd src  &&
(rabbitmq-server &) &&
(pipenv run celery -A myshop worker -l info &) &&
(pipenv run python manage.py runserver &)