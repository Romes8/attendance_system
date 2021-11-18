web: gunicorn  src.attendance_system.attendance_system.wsgi:application
python manage.py collectstatic --noinput
manage.py migrate
