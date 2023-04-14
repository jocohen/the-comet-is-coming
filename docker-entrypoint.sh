# Apply migrations to DB
python manage.py migrate

# Copy static files to proper STATIC_ROOT dir
python manage.py collectstatic

# Run server
python manage.py runserver "0.0.0.0:80"