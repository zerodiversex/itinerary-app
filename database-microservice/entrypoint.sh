#!/bin/bash

while [[ $# -gt 0 ]]; do
  case "$1" in
    --)
        shift
        launch=("$@")
        break
        ;;
    *)
        echo "Unknown argument: $1"
        exit 1
        ;;
  esac
done

echo -e "### Préparation du conteneur ###"
python manage.py makemigrations
python manage.py migrate
python manage.py import_data_lyon

echo -e "### Démarrage du conteneur ###"
exec "${launch[@]}"