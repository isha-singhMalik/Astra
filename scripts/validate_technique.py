#!/usr/bin/env python3
"""
ASTRA Technique Validator
Checks that all technique files in a PR meet the required format.
Run by GitHub Actions on every PR that touches docs/techniques/
"""

import os
import sys
import re
import subprocess

REQUIRED_SECTIONS = [
    "## Overview",
    "## Tactic",
    "## Protocols",
    "## Severity Score",
    "## Attack Scenario",
    "## Detection",
    "## Remediation",
    "## References",
]

VALID_TACTICS = [
    "Reconnaissance",
    "Authentication Abuse",
    "Authorization Failure",
    "Exfiltration",
    "Impact",
]

VALID_PROTOCOLS = ["REST", "GraphQL", "gRPC", "WebSocket", "SOAP"]

TECHNIQUE_ID_PATTERN = re.compile(
    r"^ASTRA-(REC|AUTH|AUTHZ|EXFIL|IMPACT)-\d{3}$"
)

def get_changed_technique_files():
    result = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        capture_output=True, text=True
    )
    files = result.stdout.strip().split("\n")
    return [
        f for f in files
        if f.startswith("docs/techniques/") and f.endswith(".md")
    ]

def validate_file(filepath):
    errors = []

    if not os.path.exists(filepath):
        return [f"File not found: {filepath}"]

    with open(filepath, "r") as f:
        content = f.read()

    filename = os.path.basename(filepath).replace(".md", "")
    if not TECHNIQUE_ID_PATTERN.match(filename):
        errors.append(
            f"Invalid technique ID format: '{filename}'. "
            f"Expected format: ASTRA-{{TACTIC}}-{{NNN}} e.g. ASTRA-REC-001"
        )

    if not content.startswith(f"# {filename}"):
        errors.append(
            f"File must start with '# {filename} — Technique Name'"
        )

    for section in REQUIRED_SECTIONS:
        if section not in content:
            errors.append(f"Missing required section: {section}")

    tactic_match = re.search(r"## Tactic\n(.+)", content)
    if tactic_match:
        tactic = tactic_match.group(1).strip()
        if tactic not in VALID_TACTICS:
            errors.append(
                f"Invalid tactic: '{tactic}'. "
                f"Must be one of: {', '.join(VALID_TACTICS)}"
            )

    protocols_match = re.search(r"## Protocols\n(.+)", content)
    if protocols_match:
        protocols_line = protocols_match.group(1).strip()
        found_protocols = [p for p in VALID_PROTOCOLS if p in protocols_line]
        if not found_protocols:
            errors.append(
                f"No valid protocols found in Protocols section. "
                f"Must include at least one of: {', '.join(VALID_PROTOCOLS)}"
            )

    if "## Severity Score" in content:
        if "Composite" not in content:
            errors.append(
                "Severity Score section must include a Composite score row"
            )
        if not any(r in content for r in ["Critical", "High", "Medium", "Low"]):
            errors.append(
                "Severity Score section must include a Rating "
                "(Critical / High / Medium / Low)"
            )

    sigma_pattern = re.search(r"ASTRA-[A-Z]+-\d{3}\.yml", content)
    if not sigma_pattern:
        errors.append(
            "Detection section must reference a Sigma rule file "
            "(e.g. ASTRA-REC-001.yml)"
        )

    return errors

def main():
    changed_files = get_changed_technique_files()

    if not changed_files or changed_files == [""]:
        print("No technique files changed — skipping technique validation.")
        sys.exit(0)

    print(f"Validating {len(changed_files)} technique file(s)...\n")

    all_errors = {}
    for filepath in changed_files:
        errors = validate_file(filepath)
        if errors:
            all_errors[filepath] = errors

    if all_errors:
        print("VALIDATION FAILED\n" + "="*50)
        for filepath, errors in all_errors.items():
            print(f"\n{filepath}:")
            for error in errors:
                print(f"  ✗ {error}")
        print(f"\n{sum(len(e) for e in all_errors.values())} error(s) found.")
        print("\nSee CONTRIBUTING.md for the technique template and format guide.")
        sys.exit(1)
    else:
        print(f"All {len(changed_files)} technique file(s) passed validation.")
        sys.exit(0)

if __name__ == "__main__":
    main()
