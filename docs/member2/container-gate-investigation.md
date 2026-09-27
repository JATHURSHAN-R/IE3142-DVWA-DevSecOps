# Member 2 — Container gate investigation

Name: Mugesh Ravichandran
Student ID: IT24102004
Date: 2026-09-26
Branch: IT24102004-Mugesh.R

## Day 4 contribution
Semgrep rules, SAST runner and local scan evidence were pushed
in commit e41e5c5. Integration of ci/sast.sh into the shared
workflow is still pending.

## Container investigation
The existing Trivy CI gate reported 102 HIGH and 16 CRITICAL
package/CVE findings.

A separate local image, dvwa-member2:trixie-trial, was built
using PHP 8.4 on Debian Trixie and --no-install-recommends.

The local Trivy 0.72.0 report contains:
- HIGH: 72
- CRITICAL: 1

These were separate CI and local scans, not a controlled
comparison using an identical vulnerability database snapshot.

## Remaining blocker
Package: libxml2
CVE: CVE-2026-6653
Installed: 2.12.7+dfsg+really2.9.14-2.1+deb13u3
Fixed version in scan report: NOT LISTED

Vendor reference:
https://security-tracker.debian.org/tracker/CVE-2026-6653

The trial still fails the HIGH/CRITICAL gate policy.
The scanner process exit code was not recorded.

## Evidence and next action
Report: evidence/trivy/member2-trial/trivy.json
Candidate: evidence/trivy/member2-trial/Dockerfile.trixie

This commit records the local trial for review.
The candidate has not replaced the application Dockerfile.
Full application runtime validation remains pending.

Member 1/platform owner should review the remaining findings
and remediation options before integrating a base-image change.
