cp -r covid_api/static/. /app/static
gunicorn --bind 0.0.0.0:8080 --workers 4 wsgi:app