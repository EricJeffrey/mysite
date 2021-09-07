# -d daemon
# app(python file app.py):app(application name)
uwsgi -d 1 --http 0.0.0.0:8000 --module app:app