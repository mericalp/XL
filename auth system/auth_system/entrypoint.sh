#!/bin/bash

# Wait for the PostgreSQL database to be ready

echo "PostgreSQL started"

# Create the database and user if they don't exist
echo "Creating database and user if they don't exist..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  DO \$\$
  BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'admin1') THEN
      CREATE ROLE admin1 WITH LOGIN PASSWORD '123123';
    END IF;
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'testdb') THEN
      CREATE DATABASE testdb;
      GRANT ALL PRIVILEGES ON DATABASE testdb TO admin1;
    END IF;
  END
  \$\$;
EOSQL

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start the Django development server
echo "Starting server..."
exec "$@"