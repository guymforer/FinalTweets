#!/bin/bash
# Wait for PostgreSQL database initialization completion

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DB_URL" -p "$DB_PORT" -U "$POSTGRES_USER" -d "tweets" -c "SELECT 1 FROM db_initialized LIMIT 1;" | grep -q 1; do
  >&2 echo "Database is not yet initialized - sleeping"
  sleep 1
done

>&2 echo "Database is initialized - starting data digest"
python /usr/src/app/datadigest.py
