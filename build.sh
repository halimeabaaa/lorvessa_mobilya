#!/usr/bin/env bash
set -o errexit
export USE_SQLITE="${USE_SQLITE:-true}"
export DEBUG="${DEBUG:-false}"
pip install -r requirements.txt

if [ ! -d media ]; then
  echo "ERROR: media/ folder missing from repository checkout"
  exit 1
fi
MEDIA_COUNT="$(find media -type f | wc -l)"
echo "Media files in build: ${MEDIA_COUNT}"
if [ "${MEDIA_COUNT}" -lt 1 ]; then
  echo "ERROR: media/ is empty"
  exit 1
fi

python manage.py collectstatic --noinput
echo "staticfiles/media count: $(find staticfiles/media -type f 2>/dev/null | wc -l)"
python manage.py migrate --noinput
python manage.py ensure_superuser
