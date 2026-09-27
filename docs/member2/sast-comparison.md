# Member 2 — SAST comparison

- Name: Mugesh Ravichandran
- Student ID: IT24102004
- Recorded (UTC): 2026-09-27T07:14:36.917392+00:00

The earlier baseline used different rules. This comparison uses
identical scanner inputs and records a separate Stored XSS check.

## Reproduction
Run `python3 ci/sast_compare.py` from the repository.
- Before source: `bd207094c5054822dc700aa0292def57de03af4b`
- After source: `f6de7d2623ab803a77847ebc97ea6cb1917a063f`
- Scanner: `semgrep/semgrep:1.90.0`
- Scanner image ID: `sha256:7b625711ba9b6d1a543e308967b18c01b59932490a5536a06422666474bf6ee4`

Both scans use the same scanner image, rule bytes, ignore file and four paths.
Only committed PHP source is copied into isolated scan directories.
Both scans completed with zero scanner errors and four required files scanned.

## Observed pattern matches
| Semgrep rule | Before | After |
| --- | ---: | ---: |
| semgrep.team-guestbook-unencoded-row | 2 | 0 |
| semgrep.team-sqli-query-review | 1 | 0 |
| semgrep.team-upload-original-bytes-review | 1 | 1 |
| semgrep.team-weak-session-counter | 1 | 1 |

Scoped Stored XSS check: **PASS**.
Raw guestbook assignment matches: 2 before; 0 after.

## Scope and limitations
The check requires a positive baseline and zero raw-assignment matches after the fix.
These narrow patterns do not prove the application is secure or replace browser tests.
Other findings are advisory. Scanner errors, missing coverage or a failed scoped check fail this script.
Changes in SQLi and other modules belong to the responsible team members.
Mugesh's remediation contribution is Stored XSS guestbook output encoding.
The older team.yml baseline is not used for this numerical comparison.
This local check does not prove execution in GitHub Actions or fix the Trivy gate.

## Evidence
- `evidence/sast/member2-comparison/before.json`
- `evidence/sast/member2-comparison/after.json`
- `evidence/sast/member2-comparison/summary.json`

## AI assistance
ChatGPT assisted with the script and documentation.
Counts are generated from actual local scanner outputs.
