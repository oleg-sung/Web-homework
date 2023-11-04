python manage.py collectstatic --no-input
python manage.py migrate
gunicorn --bind 0.0.0.0:8000 stocks_products.wsgi