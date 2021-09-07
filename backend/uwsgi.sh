# -d daemon
# app(python file app.py):app(application name)
uwsgi -d /data/site-of-jeff/uwsgi.log --http 0.0.0.0:8000 --module app:app