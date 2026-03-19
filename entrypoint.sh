#!/bin/bash
set -e

SQLITE_PATH="${SQLITE_PATH:-/app/db.sqlite3}"
SQLITE_DIR="$(dirname "$SQLITE_PATH")"

echo "Creando base de datos SQLite y aplicando migraciones..."
python manage.py migrate

# Da permisos de escritura al usuario de Apache (www-data)
mkdir -p "$SQLITE_DIR"
touch "$SQLITE_PATH"
chown www-data:www-data "$SQLITE_DIR" || true
chmod 775 "$SQLITE_DIR" || true
if [ -f "$SQLITE_PATH" ]; then
	chown www-data:www-data "$SQLITE_PATH" || true
	chmod 664 "$SQLITE_PATH" || true
fi

echo "Iniciando Apache con mod_wsgi..."
exec apache2ctl -D FOREGROUND