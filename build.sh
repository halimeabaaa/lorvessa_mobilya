#!/usr/bin/env bash
set -o errexit
export USE_SQLITE="${USE_SQLITE:-true}"
export DEBUG="${DEBUG:-false}"
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
