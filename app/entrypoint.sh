#!/bin/sh

set -e

flask db upgrade
personnel=$(sqlite3 instance/project.db "SELECT * FROM Personnel")

if [ -z "$personnel" ]; then
    echo "No personnel found, creating default personnel"

    GEN_LOG=$(python3 -c "from custom_paquets.converter import generate_login; print(generate_login('$ADMIN_NOM','$ADMIN_PRENOM'))")
    GEN_PASS=$(python3 -c "from custom_paquets.security import encrypt_password; print(encrypt_password('$ADMIN_PASSWORD', salt=15).decode('utf-8'))")

    sqlite3 instance/project.db < sql/db_production.sql
    sqlite3 instance/project.db "INSERT INTO Personnel (nom, prenom, login, mdp, role, email, essais, archive) VALUES ('$ADMIN_NOM', '$ADMIN_PRENOM', '$GEN_LOG', '$GEN_PASS', 'SuperAdministrateur', '$ADMIN_MAIL', 0, 0)"

    echo "Personnel created with success"
    echo "Login: $GEN_LOG"
else
    echo "Personnel found, skipping creation"
fi

gunicorn -b 0.0.0.0 'app:create_app()'

exec "$@"