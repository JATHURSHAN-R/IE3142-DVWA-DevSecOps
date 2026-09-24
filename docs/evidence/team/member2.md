# Member 2 — Stored XSS remediation

Name: Mugesh Ravichandran
Student ID: IT24102004
Branch: IT24102004-Mugesh.R
Report section: 3.4 Stored Cross-Site Scripting
Test date: 2026-09-24

## Change
The guestbook rendered stored values without HTML encoding.
Updated dvwaGuestbook() to encode names and comments using
htmlspecialchars with ENT_QUOTES, ENT_SUBSTITUTE and UTF-8.

## Actual local observations
Security level: Low.
Normal input: Hello & <test> "team"
The normal input displayed correctly.

Payload: <script>document.title='TEAM_XSS'</script>
The payload displayed as text in the lowxss entry.
document.title returned:
Vulnerability: Stored Cross Site Scripting (XSS) :: Damn Vulnerable Web Application (DVWA)

## Evidence
- evidence/xss/stored-xss-before.png
- evidence/xss/stored-xss-after.png
- evidence/xss/php-lint-after.txt
- evidence/xss/sast-before.json

## Earlier contributions
0905685: Docker setup and build records.
89ca73d: Stored XSS baseline evidence.
c3de89c: Before-fix SAST report.

## Remaining work
New Semgrep rules, ci/sast.sh and consistent scan comparison.
Peer review and merge into main.

## Limitation
This change addresses the guestbook HTML output context.
Other intentional DVWA vulnerabilities remain.

## AI assistance
ChatGPT helped prepare the fix and verification instructions.
I performed the local browser checks and captured the evidence.
