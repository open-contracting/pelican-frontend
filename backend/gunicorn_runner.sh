#!/bin/sh
gunicorn --bind 0.0.0.0:$1 dqt.docker_wsgi -c gunicorn_docker.py