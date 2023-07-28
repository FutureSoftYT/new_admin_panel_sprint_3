#!/bin/bash

set -e

chown www-data:www-data /var/log

python3 manage.py migrate --no-input

uwsgi --strict --ini /opt/app/uwsgi.ini
