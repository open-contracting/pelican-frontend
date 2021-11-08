#!/bin/sh
gunicorn --bind 0.0.0.0:$1 --timeout 120 core.wsgi -c gunicorn_docker.py