#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p reports

docker run --rm -v "$PWD:/src:ro" -w /src \
  semgrep/semgrep:1.90.0 semgrep scan \
  --config .semgrep/dvwa-rules.yml \
  --metrics off --disable-version-check --json \
  vulnerabilities/sqli/source/low.php \
  vulnerabilities/weak_id/source/low.php \
  vulnerabilities/upload/source/low.php \
  dvwa/includes/dvwaPage.inc.php > reports/semgrep.json

python3 - <<'PY'
import json
from pathlib import Path
from collections import Counter

report = json.loads(Path('reports/semgrep.json').read_text())
if not isinstance(report.get('results'), list):
    raise SystemExit('FAIL: missing SAST results')
if report.get('errors'):
    raise SystemExit('FAIL: scanner errors; inspect reports/semgrep.json')

expected = {
    'vulnerabilities/sqli/source/low.php',
    'vulnerabilities/weak_id/source/low.php',
    'vulnerabilities/upload/source/low.php',
    'dvwa/includes/dvwaPage.inc.php',
}
scanned = set(report.get('paths', {}).get('scanned', []))
if not expected.issubset(scanned):
    raise SystemExit('FAIL: some required files were not scanned')

print('Scanner version:', report.get('version'))
print('Required files scanned: 4/4')
print('Scanner errors: 0')
print('SAST findings:', len(report['results']))
for rule, count in sorted(Counter(r['check_id'] for r in report['results']).items()):
    print(f'  {rule}: {count}')
print('Policy: findings advisory; scanner errors block.')
PY
