#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

commit="$(git rev-parse HEAD)"
image="ie3142-dvwa:${commit}"
scanner="aquasec/trivy:0.72.0"
report_dir="$PWD/reports/trivy"

mkdir -p "$report_dir"
rm -f "$report_dir/trivy.json" "$report_dir/scan-exit-code.txt"

work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT

printf '%s\n' "$commit" > "$report_dir/tested-commit.txt"
date -u +'%Y-%m-%dT%H:%M:%SZ' > "$report_dir/scan-started.txt"
git status --porcelain > "$report_dir/working-tree-status.txt"

docker build --pull -t "$image" .

docker image inspect "$image" \
  --format '{{.Id}}' > "$report_dir/application-image-id.txt"

docker save --output "$work_dir/dvwa.tar" "$image"

docker pull "$scanner"

scanner_id="$(docker image inspect "$scanner" --format '{{.Id}}')"

docker image inspect "$scanner" \
  --format '{{json .RepoDigests}}' > "$report_dir/scanner-digests.json"

docker run --rm "$scanner_id" --version \
  > "$report_dir/trivy-version.txt"

scan_status=0

docker run --rm \
  --user "$(id -u):$(id -g)" \
  -e HOME=/tmp \
  -v "$work_dir:/scan:ro" \
  -v "$report_dir:/reports" \
  "$scanner_id" image \
    --cache-dir /tmp/trivy-cache \
    --input /scan/dvwa.tar \
    --scanners vuln \
    --severity HIGH,CRITICAL \
    --ignore-unfixed=false \
    --exit-code 1 \
    --timeout 15m \
    --format json \
    --output /reports/trivy.json \
  || scan_status=$?

printf '%s\n' "$scan_status" > "$report_dir/scan-exit-code.txt"

if [ "$scan_status" -ne 0 ]; then
  echo "Container gate failed. Inspect the report and scanner logs."
  exit "$scan_status"
fi

test -s "$report_dir/trivy.json"
echo "Container gate passed: no HIGH or CRITICAL findings reported."
