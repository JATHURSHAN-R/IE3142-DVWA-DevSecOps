# Day 1 of the coordinated team phase

Date: 24 September 2026  
Project: Building and Securing a DevSecOps Pipeline  
Repository: JATHURSHAN-R/IE3142-DVWA-DevSecOps  
Leader: Jathurshan Rasathurai

Today starts the coordinated team phase. Earlier work remains preliminary work with its original authors, commits and dates. This record does not reset Git history or assert that implementation and testing are complete.

## Starting point

Baseline main commit: `bd207094c5054822dc700aa0292def57de03af4b`  
Machine-readable copy: [baseline-sha.txt](../evidence/team/baseline-sha.txt)

Observed before this groundwork PR:
- PR #1 merged the advisory Semgrep baseline workflow.
- PR #2 merged the SQL source-review and acceptance-plan documentation.
- The main-branch baseline run succeeded: https://github.com/JATHURSHAN-R/IE3142-DVWA-DevSecOps/actions/runs/35830079035
- Main contains security-baseline.yml. It does not yet contain the guide's build-test.yml or security-gates.yml.
- The current SAST workflow reports findings without blocking on vulnerabilities; scanner errors fail it. A green result does not mean zero vulnerabilities.
- Main was not protected and no repository rulesets were returned during this check.
- Mugesh's branch, IT24102004-Mugesh.R, has three commits beyond its common ancestor with main, covering Docker configuration, build records and Stored XSS baseline evidence. It has no open PR at this check.
- IT24102104-Sharvika.J is identical to the baseline main commit. The branch exists, but it has no unique code contribution yet.
- docs/day2-sqli-baseline contains an additional evidence/sqli/before-semgrep.json file which was committed after PR #2 merged. That extra file is not yet on main.

Branch comparisons:
- https://github.com/JATHURSHAN-R/IE3142-DVWA-DevSecOps/compare/main...IT24102004-Mugesh.R
- https://github.com/JATHURSHAN-R/IE3142-DVWA-DevSecOps/compare/main...docs/day2-sqli-baseline

## Ownership for this phase

| Member | Name and report role | Vulnerability | Scan responsibility |
| --- | --- | --- | --- |
| 1 | Jathurshan Rasathurai — Platform & Architecture | 3.1 SQL Injection | Container image scanning with Trivy; build-test.yml; integration |
| 2 | Mugesh Ravichandran, IT24102004 — Threat Modelling & Risk | 3.4 Stored Cross-Site Scripting | SAST with Semgrep; risk mapping |
| 3 | Name and student ID to be confirmed — Vulnerability & Secure Coding | 3.3 File Upload → Remote Code Execution | Dependency / software composition scanning with Composer audit |
| 4 | Name and student ID to be confirmed — CI/CD & Secrets | 3.2 Weak Session IDs | Secrets scanning with Gitleaks; environment credentials; workflow assembly |

Sharvika has an existing branch; the leader must confirm whether she occupies Member 3 or Member 4 and record the remaining person's details. Do not infer their assignments from their branch names.

This ownership table corrects the new guide's assignment of Stored XSS to Member 4 and Weak Session IDs to Member 2. Mugesh has already started Stored XSS, so retain his ownership. Member 4 takes the guide's Weak Session IDs code. Their scanner responsibilities remain unchanged.

Preserve Mugesh's existing Docker contribution and credit him for it. Member 1 reviews and integrates that work instead of replacing it wholesale with the guide's example Dockerfile. If report Section 8 keeps the role labels above, supplement them with the actual code, setup, scan and review contributions.

## Groundwork to complete today

Leader:
- [ ] Review this PR, the current branch comparisons and the ownership table.
- [ ] Confirm the remaining two members' names, student IDs, roles and repository access.
- [ ] Arrange review of Mugesh's existing branch before starting overlapping Docker edits.
- [ ] Review the extra SQL JSON evidence and merge it through a new PR if valid.
- [ ] Agree on PR-based integration and at least one teammate review.
- [ ] Configure main-branch protection or rules if available; verify it is active before claiming protection in the report.
- [ ] Confirm the existing baseline workflow runs for this groundwork commit.
- [ ] Record the actual Day 1 completion time and PR/run URLs after review.

Each member:
- [ ] Sync main after the groundwork is merged, without discarding local work.
- [ ] Confirm their own Git author identity and assigned role.
- [ ] Keep their existing working branch if it contains relevant work.
- [ ] Check Docker and Docker Compose availability.
- [ ] Read their target source file and scanner responsibility.
- [ ] Record actual environment results and planned acceptance checks in their own notes.
- [ ] Open a small PR when there is meaningful work to review.

Not required today: finish all four fixes, implement all gates, recreate every screenshot, or claim a complete secure pipeline.

## Existing branch handling

Mugesh should preserve IT24102004-Mugesh.R, merge the current origin/main into it after preserving uncommitted work, resolve any conflicts, and open a PR. Review Docker changes, .dockerignore and evidence together. His note already records setup and XSS work; do not duplicate it under another author's name.

The leader should open a new evidence PR from docs/day2-sqli-baseline for the additional JSON, after reviewing its contents. PR #2 being merged does not include commits added to that branch afterwards.

Sharvika can continue her existing branch after syncing it with the merged main. The remaining member creates a branch using their own name or agreed member identifier. Nobody needs a fresh clone if their existing repository is correct.

## File ownership to avoid conflicts

- Member 1: SQL handler and container-scanning job; coordinates build-test.yml.
- Member 2: only dvwaGuestbook() in dvwa/includes/dvwaPage.inc.php; Semgrep rules and ci/sast.sh. Preserve all unrelated shared PHP functions.
- Member 3: upload handler and ci/dependencies.sh. Coordinate upload storage requirements with the platform owner.
- Member 4: weak-ID handler, ci/secrets.sh, environment configuration and security-gates.yml assembly.
- Dockerfile and compose.yml: review Mugesh's existing work first; one editor at a time after that.
- Each member reviews the shared workflow job invoking their scanner before integration.

## Schedule from today

| Phase day | Date | Outcome |
| --- | --- | --- |
| 1 | 24 September | Inventory, ownership, baseline and review process |
| 2 | 25 September | Integrate and verify the local two-container environment |
| 3 | 26 September | Implement and verify the assigned module changes |
| 4 | 27 September | Implement the four scanner responsibilities |
| 5 | 28 September | Review, integrate and run the shared workflows |
| 6 | 29 September | Collect final evidence and correct the report |
| 7 | 30 September | Viva practice and final deliverable review |

This is a target schedule, not a requirement to create empty commits every day. Record the dates on which work actually occurs.

## Evidence and viva

Reuse traceable before-fix evidence where it matches the baseline. After-code changes need corresponding verification. Record repository, commit, date, tool version, actual result and limitation. Never label old solo-repository Actions screenshots as results from this team repository.

The original Day 1 rules include command injection. The uploaded report covers Weak Session IDs instead. Member 2 must align the new rules with the report and measure before/after using identical rule configuration and scope. The old 13-to-6 count is not a target to reproduce.

Completion requires a member to explain their change and scanner behaviour and show actual tests, PRs and review. This plan is not itself a contribution statement or proof that those tests have happened.

## AI assistance

ChatGPT assisted the leader in checking repository state and drafting this coordination record and PR template. Team members must verify their own changes, observations and final contribution statements.
