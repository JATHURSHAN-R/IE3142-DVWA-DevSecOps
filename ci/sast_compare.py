#!/usr/bin/env python3
"""Compare committed DVWA source with identical local Semgrep rules and scope."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SCANNER = "semgrep/semgrep:1.90.0"
VERSION = "1.90.0"
RULES = ".semgrep/dvwa-rules.yml"
IGNORE = ".semgrepignore"
BASELINE_FILE = "docs/evidence/team/baseline-sha.txt"
TARGETS = (
    "vulnerabilities/sqli/source/low.php",
    "vulnerabilities/weak_id/source/low.php",
    "vulnerabilities/upload/source/low.php",
    "dvwa/includes/dvwaPage.inc.php",
)
XSS_RULE = "team-guestbook-unencoded-row"


class ComparisonError(Exception):
    pass


def command(args, **kwargs):
    return subprocess.run(args, cwd=ROOT, check=True, **kwargs)


def git_text(*args):
    return command(
        ["git", *args], stdout=subprocess.PIPE, text=True
    ).stdout.strip()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def validate_report(report):
    if not isinstance(report, dict) or not isinstance(report.get("results"), list):
        raise ComparisonError("Missing or invalid Semgrep results.")
    if report.get("version") != VERSION:
        raise ComparisonError("Unexpected Semgrep version.")
    if report.get("errors"):
        raise ComparisonError("Scanner reported errors; inspect the saved JSON.")
    scanned = set(report.get("paths", {}).get("scanned", []))
    missing = set(TARGETS) - scanned
    if missing:
        raise ComparisonError(
            "Required files not scanned: " + ", ".join(sorted(missing))
        )
    return Counter(item["check_id"] for item in report["results"])


def xss_count(counts):
    return sum(
        n for rule, n in counts.items()
        if rule.split(".")[-1] == XSS_RULE
    )


def docker_command():
    if not shutil.which("docker"):
        raise ComparisonError("Docker is not installed.")
    probe = subprocess.run(
        ["docker", "info"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if probe.returncode == 0:
        return ["docker"]
    if not shutil.which("sudo"):
        raise ComparisonError("Check Docker daemon and permissions.")
    print("Enter your Kali password if Docker asks.", flush=True)
    command(["sudo", "docker", "info"], stdout=subprocess.DEVNULL)
    return ["sudo", "docker"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replace-evidence", action="store_true")
    args = parser.parse_args()

    if os.geteuid() == 0:
        raise ComparisonError(
            "Run python3 ci/sast_compare.py without sudo."
        )
    if Path(git_text("rev-parse", "--show-toplevel")).resolve() != ROOT:
        raise ComparisonError("Install this script in the repository ci directory.")

    baseline = (ROOT / BASELINE_FILE).read_text().strip()
    if not re.fullmatch(r"[0-9a-fA-F]{40}", baseline):
        raise ComparisonError("Team baseline must contain a full commit SHA.")
    baseline = git_text("rev-parse", "--verify", baseline + "^{commit}")
    after = git_text("rev-parse", "HEAD")

    dirty = git_text(
        "status", "--porcelain", "--untracked-files=no", "--",
        *TARGETS, RULES, IGNORE, BASELINE_FILE,
    )
    if dirty:
        raise ComparisonError(
            "Preserve changes to scan inputs before comparing:\n" + dirty
        )

    evidence = ROOT / "evidence/sast/member2-comparison"
    note = ROOT / "docs/member2/sast-comparison.md"
    outputs = [
        evidence / n for n in ("before.json", "after.json", "summary.json")
    ] + [note]
    if any(p.exists() for p in outputs) and not args.replace_evidence:
        raise ComparisonError(
            "Comparison evidence exists. Review it before using --replace-evidence."
        )

    rules = (ROOT / RULES).read_bytes()
    ignore = (ROOT / IGNORE).read_bytes()
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(
        prefix="member2-sast-compare-", dir=reports
    ))
    print("Diagnostic files:", work, flush=True)

    source_hashes = {}
    for label, commit in (("before", baseline), ("after", after)):
        snapshot = work / label
        snapshot.mkdir()
        source_hashes[label] = {}
        for filename in TARGETS:
            data = command(
                ["git", "show", f"{commit}:{filename}"],
                stdout=subprocess.PIPE,
            ).stdout
            destination = snapshot / filename
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            source_hashes[label][filename] = digest(data)
        (snapshot / ".semgrep").mkdir()
        (snapshot / RULES).write_bytes(rules)
        (snapshot / IGNORE).write_bytes(ignore)

    docker = docker_command()
    command(docker + ["pull", SCANNER])
    image_id = command(
        docker + ["image", "inspect", SCANNER, "--format", "{{.Id}}"],
        stdout=subprocess.PIPE, text=True,
    ).stdout.strip()
    image_digests = json.loads(command(
        docker + [
            "image", "inspect", SCANNER,
            "--format", "{{json .RepoDigests}}",
        ],
        stdout=subprocess.PIPE, text=True,
    ).stdout)

    counts = {}
    for label in ("before", "after"):
        print("Scanning", label, "source...", flush=True)
        scan = docker + [
            "run", "--rm",
            "-v", f"{work / label}:/src:ro",
            "-w", "/src", image_id,
            "semgrep", "scan",
            "--config", RULES,
            "--metrics", "off",
            "--disable-version-check", "--json",
            *TARGETS,
        ]
        report_path = work / f"{label}.json"
        log_path = work / f"{label}.stderr.txt"
        with report_path.open("w") as output, log_path.open("w") as log:
            result = subprocess.run(
                scan, cwd=ROOT, stdout=output, stderr=log
            )
        if result.returncode:
            raise ComparisonError(
                f"{label} scan exited {result.returncode}; inspect {log_path}"
            )
        counts[label] = validate_report(
            json.loads(report_path.read_text())
        )

    xss_before = xss_count(counts["before"])
    xss_after = xss_count(counts["after"])
    regression_ok = xss_before > 0 and xss_after == 0

    summary = {
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "member": "Mugesh Ravichandran",
        "student_id": "IT24102004",
        "before_commit": baseline,
        "after_commit": after,
        "scanner_tag": SCANNER,
        "scanner_version": VERSION,
        "scanner_image_id": image_id,
        "scanner_repo_digests": image_digests,
        "rules_sha256": digest(rules),
        "ignore_sha256": digest(ignore),
        "source_sha256": source_hashes,
        "targets": list(TARGETS),
        "required_files_scanned_per_report": len(TARGETS),
        "scanner_errors": 0,
        "before_counts": dict(counts["before"]),
        "after_counts": dict(counts["after"]),
        "xss_before": xss_before,
        "xss_after": xss_after,
        "scoped_xss_check": "PASS" if regression_ok else "FAIL",
    }

    rows = [
        "| Semgrep rule | Before | After |",
        "| --- | ---: | ---: |",
    ]
    for rule in sorted(set(counts["before"]) | set(counts["after"])):
        rows.append(
            f"| {rule} | {counts['before'][rule]} | {counts['after'][rule]} |"
        )

    text = [
        "# Member 2 — SAST comparison",
        "",
        "- Name: Mugesh Ravichandran",
        "- Student ID: IT24102004",
        f"- Recorded (UTC): {summary['recorded_at_utc']}",
        "",
        "The earlier baseline used different rules. This comparison uses",
        "identical scanner inputs and records a separate Stored XSS check.",
        "",
        "## Reproduction",
        "Run `python3 ci/sast_compare.py` from the repository.",
        f"- Before source: `{baseline}`",
        f"- After source: `{after}`",
        f"- Scanner: `{SCANNER}`",
        f"- Scanner image ID: `{image_id}`",
        "",
        "Both scans use the same scanner image, rule bytes, ignore file and four paths.",
        "Only committed PHP source is copied into isolated scan directories.",
        "Both scans completed with zero scanner errors and four required files scanned.",
        "",
        "## Observed pattern matches",
        *rows,
        "",
        f"Scoped Stored XSS check: **{summary['scoped_xss_check']}**.",
        f"Raw guestbook assignment matches: {xss_before} before; {xss_after} after.",
        "",
        "## Scope and limitations",
        "The check requires a positive baseline and zero raw-assignment matches after the fix.",
        "These narrow patterns do not prove the application is secure or replace browser tests.",
        "Other findings are advisory. Scanner errors, missing coverage or a failed scoped check fail this script.",
        "Changes in SQLi and other modules belong to the responsible team members.",
        "Mugesh's remediation contribution is Stored XSS guestbook output encoding.",
        "The older team.yml baseline is not used for this numerical comparison.",
        "This local check does not prove execution in GitHub Actions or fix the Trivy gate.",
        "",
        "## Evidence",
        "- `evidence/sast/member2-comparison/before.json`",
        "- `evidence/sast/member2-comparison/after.json`",
        "- `evidence/sast/member2-comparison/summary.json`",
        "",
        "## AI assistance",
        "ChatGPT assisted with the script and documentation.",
        "Counts are generated from actual local scanner outputs.",
        "",
    ]

    evidence.mkdir(parents=True, exist_ok=True)
    note.parent.mkdir(parents=True, exist_ok=True)
    for label in ("before", "after"):
        shutil.copyfile(
            work / f"{label}.json", evidence / f"{label}.json"
        )
    (evidence / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    note.write_text("\n".join(text))

    print("\nBefore source:", baseline)
    print("After source:", after)
    print("Scanner:", SCANNER)
    print("Files scanned: 4/4 before and after; scanner errors: 0")
    print(
        "Total matches:",
        sum(counts["before"].values()), "->",
        sum(counts["after"].values()),
    )
    print("Stored XSS matches:", xss_before, "->", xss_after)
    print("Scoped Stored XSS check:", summary["scoped_xss_check"])
    print("Saved:", evidence.relative_to(ROOT), "and", note.relative_to(ROOT))
    return 0 if regression_ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (
        ComparisonError, OSError, ValueError,
        KeyError, subprocess.CalledProcessError,
    ) as error:
        print("STOP:", error, file=sys.stderr)
        sys.exit(1)
