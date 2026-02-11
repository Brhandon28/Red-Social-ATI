#!/bin/bash
set -e

echo "Creando base de datos SQLite y aplicando migraciones..."
python manage.py migrate

# Da permisos de escritura al usuario de Apache (www-data)
chown www-data:www-data /app/db.sqlite3 || true
chmod 664 /app/db.sqlite3 || true

echo "Iniciando Apache con mod_wsgi..."
exec apache2ctl -D FOREGROUND