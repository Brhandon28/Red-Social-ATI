#!/bin/sh
set -e

DB_PATH="${SQLITE_PATH:-/app/db.sqlite3}"

echo "Aplicando migraciones en ${DB_PATH}..."
if ! output=$(python manage.py migrate 2>&1); then
  echo "$output"

  if echo "$output" | grep -q "InconsistentMigrationHistory"; then
    echo "Historial de migraciones inconsistente detectado."
    echo "Reiniciando base de datos SQLite de desarrollo en ${DB_PATH}..."
    rm -f "$DB_PATH"
    python manage.py migrate
  else
    exit 1
  fi
else
  echo "$output"
fi

echo "Iniciando servidor de desarrollo..."
exec python manage.py runserver 0.0.0.0:8000
