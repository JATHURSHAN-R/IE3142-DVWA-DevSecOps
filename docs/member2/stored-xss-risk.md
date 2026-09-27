# Member 2 — Stored XSS risk and control

- Name: Mugesh Ravichandran
- Student ID: IT24102004
- Prepared: 27 September 2026

## Data flow and trust boundary

Guestbook input is stored in the database. dvwaGuestbook() reads the
stored name and comment and inserts them into HTML text.
Database storage does not make user input trustworthy.

## Risk assessment

| Item | Assessment |
| --- | --- |
| Entry point | Guestbook name and message fields |
| Asset | Page integrity and actions available in the viewing user's session |
| STRIDE | Tampering; potential Information Disclosure or Elevation of Privilege depending on the victim's permissions |
| Preconditions | An attacker can store input and another user views the affected output |
| Before control | Raw database values entered HTML in levels other than Impossible |
| Demonstrated impact | Earlier local evidence showed a stored script changing the title to TEAM_XSS |
| Potential impact | Scripts could alter content or act with the viewing browser's permissions; these impacts were not demonstrated by the title test |
| Control | HTML output encoding for both fields using htmlspecialchars with ENT_QUOTES, ENT_SUBSTITUTE and UTF-8 |
| Residual risk | Other output contexts, modules and container vulnerabilities require separate review |

## Implementation and evidence

The fix is in dvwa/includes/dvwaPage.inc.php, in dvwaGuestbook().

Existing evidence:
- evidence/xss/stored-xss-before.png
- evidence/xss/stored-xss-after.png
- evidence/xss/php-lint-after.txt

These files document earlier checks, not a new browser test on
27 September. Run python3 ci/sast_compare.py to generate a dated
comparison using identical Semgrep rules and scope.

The Semgrep rule detects specific raw assignments. Zero matches
alone cannot prove absence of XSS. Total counts also include
other members' modules and are not Mugesh's remediation count.

## References

- https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
- https://www.php.net/manual/en/function.htmlspecialchars.php

## AI assistance

ChatGPT assisted with the script and wording. Observed behaviour
is limited to the identified evidence; broader impacts are conditional.
