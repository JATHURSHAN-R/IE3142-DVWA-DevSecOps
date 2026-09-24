# Stored XSS baseline

Member: Mugesh Ravichandran
Student ID: IT24102004
Branch: IT24102004-Mugesh.R

## Test
URL: http://127.0.0.1:4280/vulnerabilities/xss_s/
Security level: Low
Name: team
Payload: <script>document.title='TEAM_XSS'</script>

## Observed result
The browser tab title changed to TEAM_XSS.
Reading document.title in Firefox Console returned TEAM_XSS.
This demonstrates JavaScript execution through the guestbook input.

## Evidence
- ../../evidence/xss/stored-xss-before.png
- ../../evidence/xss/containers-before.txt
- ../../evidence/xss/before-commit.txt

## Next steps
Save the before-fix SAST report.
Apply HTML output encoding to guestbook names and comments.
Rebuild and retest the saved payload and a normal comment.
Preserve the database for comparison.

## AI assistance
ChatGPT helped with test instructions and this document.
I ran the test and captured the browser evidence.
2026-09-23T17:09:48+05:30
