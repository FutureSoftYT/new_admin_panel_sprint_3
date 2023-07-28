#!/bin/bash

set -e

while ! pg_isready -U app -d movies_database; do
  sleep 1
done

psql -U app -d movies_database -f /etc/app/movies_database.ddl

