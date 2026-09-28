#!/usr/bin/env bash
set -euo pipefail
mkdir -p reports
rc=0

docker run --rm -e GIT_CONFIG_COUNT=1 \
  -e GIT_CONFIG_KEY_0=safe.directory -e GIT_CONFIG_VALUE_0=/repo \
  -v "$PWD:/repo" -w /repo \
  zricethezav/gitleaks:v8.24.3 git /repo \
  --log-opts="--all" --redact=100 --exit-code=10 \
  --report-format=json --report-path=/repo/reports/gitleaks.json \
  || rc=$?

# 10 means findings; other nonzero codes are scanner failures.
if (( rc != 0 && rc != 10 )); then exit "$rc"; fi

python3 - <<'PYCODE'
import json
from pathlib import Path

r = json.loads(Path('reports/gitleaks.json').read_text())

if not isinstance(r, list):
    raise SystemExit('Missing Gitleaks result list')

print('Secret findings:', len(r))
print('Policy: findings advisory; scanner errors block.')
PYCODE