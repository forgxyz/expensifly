release: python manage.py migrate && python manage.py createsuperuser --no-input
web: gunicorn expensifly.wsgi --log-file -
