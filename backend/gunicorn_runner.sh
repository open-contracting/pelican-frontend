#!/bin/sh
gunicorn --bind 0.0.0.0:$1 --timeout 120 dqt.docker_wsgi -c gunicorn_docker.py