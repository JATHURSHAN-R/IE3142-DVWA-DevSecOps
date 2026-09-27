#!/usr/bin/env bash
set -euo pipefail

mkdir -p reports

test -f vulnerabilities/api/composer.lock

rc=0

docker run --rm -v "$PWD:/app" \
  -w /app/vulnerabilities/api composer:2.8.12 \
  --no-plugins --no-scripts audit --locked --format=json \
  > reports/composer-audit.json || rc=$?

# Composer audit:
# 1 = vulnerable
# 2 = abandoned
# 3 = both
# These findings are advisory when a valid audit report exists.

if (( rc > 3 )); then
    exit "$rc"
fi

python3 - <<'PYCODE'
import json
from pathlib import Path

r = json.loads(Path('reports/composer-audit.json').read_text())

if 'advisories' not in r or 'abandoned' not in r:
    raise SystemExit('Invalid audit report or operational failure')

print('Dependency audit saved. Findings advisory; review JSON.')
PYCODE