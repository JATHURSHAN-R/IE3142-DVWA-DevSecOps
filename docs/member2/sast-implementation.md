# Member 2 — Semgrep SAST implementation

Name: Mugesh Ravichandran
Student ID: IT24102004
Branch: IT24102004-Mugesh.R
Evidence recorded (UTC): 2026-09-26T15:01:30.874393+00:00
Application source HEAD during scan: e50e9995988f6368c79703d32709d0de397c661d

## Implementation
Added four focused PHP review rules and ci/sast.sh.
Scope: SQLi, Weak Session IDs, File Upload and Stored XSS.
Command: sudo bash ci/sast.sh

## Observed local result
Semgrep version: 1.90.0
Findings: 2
Required files scanned: 4/4
Scanner errors: 0
Evidence: evidence/sast/member2-semgrep.json

## Configuration hashes
- .semgrep/dvwa-rules.yml: 24960f757b4a9528c58f896d2641417c74fa761a66cd172d88361a5b0a607efb
- .semgrepignore: ea982d67e9c3c4456c951599749f693bc0695ec22021fc3368785957a26ad3e6
- ci/sast.sh: e085a3376afd845d24d9647e86212035051cf8e6d038b1b44cd07d5aa2846d87

## Policy and limitations
Findings are advisory; scanner execution and coverage errors fail.
These narrow pattern checks do not establish that DVWA is secure.
Counts are not directly comparable with the older team.yml baseline.

## Remaining integration
Member 4/leader to integrate bash ci/sast.sh into Security Gates.
Existing Trivy workflow is unchanged.
Final before/after comparison requires identical rules and scan scope.

## AI assistance
ChatGPT assisted with the rules, script and verification instructions.
