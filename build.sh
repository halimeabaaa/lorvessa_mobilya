#!/usr/bin/env bash
set -o errexit
export USE_SQLITE="${USE_SQLITE:-true}"
export DEBUG="${DEBUG:-false}"
pip install -r requirements.txt

if [ ! -d static/media ]; then
  echo "ERROR: static/media/ missing"
  exit 1
fi
echo "static/media files: $(find static/media -type f | wc -l)"

python manage.py collectstatic --noinput
echo "collected static/media: $(find staticfiles/media -type f 2>/dev/null | wc -l)"
python manage.py migrate --noinput
python manage.py ensure_superuser
