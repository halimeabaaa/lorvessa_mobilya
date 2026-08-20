#!/usr/bin/env bash
set -o errexit
export USE_SQLITE="${USE_SQLITE:-true}"
export DEBUG="${DEBUG:-false}"
pip install -r requirements.txt

if [ ! -d media ]; then
  echo "ERROR: media/ folder missing from repository checkout"
  exit 1
fi
echo "Media files in build: $(find media -type f | wc -l)"

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py ensure_superuser
# Build sırasında da seed (MEDIA_ROOT yerelde media/); Render runtime /tmp'ye kopyalar
RENDER= python manage.py seed_media_catalog || true
