# SQL lookup baseline — Member 1

Owner: Jathurshan Rasathurai

## Scope

File: vulnerabilities/sqli/source/low.php
Database backend: MySQL/MariaDB
Planned comparison: the same Low-level module before and after remediation.

The reviewed repository commit and file object ID are recorded in:
- before-source-commit.txt
- before-source-blob.txt

## Source review

The handler obtains the user ID from request data and inserts it directly
into the SQL query text before executing the query.

This mixes untrusted input with SQL syntax. The intended remediation is
a prepared statement with a bound integer parameter, supported by
positive-integer validation.

Relevant STRIDE category: Information Disclosure.
Potential impact: records beyond the intended lookup could be exposed.
Runtime evidence and justified risk ratings still need to be recorded.

## Planned acceptance checks

- An existing valid ID returns the intended record.
- A nonexistent valid ID returns no matching record.
- Empty and non-integer input is rejected after remediation.
- Normal lookup behavior remains functional after the change.
- The relevant SAST finding is compared using the same rule and file scope.

## Scanner evidence

Rule: team-sqli-direct-query
Run URL: PENDING
Scanned commit: PENDING
SQL-rule finding count: PENDING
Scanner errors: PENDING
Original JSON report saved as: PENDING

A scanner match supports source review but does not by itself prove
runtime exploitation or successful remediation.

## Runtime evidence

Status: PENDING — team environment must be validated.
Environment/version:
Normal lookup input:
Actual output:
Screenshot:
Remaining assignment security evidence:

## Peer review

Reviewer:
Review URL:
Date:
Comments addressed:

## AI assistance

ChatGPT assisted with the initial source-review explanation and this
documentation template. Member 1 must verify and update the observations,
record actual test results, and explain the eventual implementation.
