#!/bin/sh
gunicorn --bind 0.0.0.0:8001 core.docker_wsgi -c gunicorn_docker.py