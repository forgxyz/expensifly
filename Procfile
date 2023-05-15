release: python manage.py migrate && python manage.py ensure_administrator --no-input
web: gunicorn expensifly.wsgi --log-file -
