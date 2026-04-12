#!/usr/bin/env python3
"""
ASTRA Sigma Rule Validator
Checks that Sigma rules in a PR meet required format and map to a technique.
"""

import os
import sys
import yaml
import subprocess
import re

REQUIRED_SIGMA_FIELDS = ["title", "id", "status", "description", "references",
                         "author", "date", "tags", "logsource", "detection"]

TECHNIQUE_ID_PATTERN = re.compile(r"^ASTRA-(REC|AUTH|AUTHZ|EXFIL|IMPACT)-\d{3}$")

def get_changed_sigma_files():
    result = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        capture_output=True, text=True
    )
    files = result.stdout.strip().split("\n")
    return [
        f for f in files
        if f.startswith("detection-rules/sigma/") and f.endswith(".yml")
    ]

def validate_sigma_file(filepath):
    errors = []

    if not os.path.exists(filepath):
        return [f"File not found: {filepath}"]

    filename = os.path.basename(filepath).replace(".yml", "")
    if not TECHNIQUE_ID_PATTERN.match(filename):
        errors.append(
            f"Sigma file must be named after its technique ID: "
            f"e.g. ASTRA-REC-001.yml"
        )

    try:
        with open(filepath, "r") as f:
            rule = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"Invalid YAML: {e}"]

    if not isinstance(rule, dict):
        return ["Sigma file must be a valid YAML dictionary"]

    for field in REQUIRED_SIGMA_FIELDS:
        if field not in rule:
            errors.append(f"Missing required Sigma field: '{field}'")

    if "tags" in rule:
        tags = rule["tags"] if isinstance(rule["tags"], list) else []
        astra_tags = [t for t in tags if str(t).startswith("astra.")]
        if not astra_tags:
            errors.append(
                "Sigma rule tags must include the ASTRA technique ID "
                "prefixed with 'astra.' e.g. 'astra.ASTRA-REC-001'"
            )

    if "detection" in rule:
        detection = rule["detection"]
        if not isinstance(detection, dict):
            errors.append("'detection' field must be a dictionary")
        elif "condition" not in detection:
            errors.append("'detection' must include a 'condition' field")

    technique_file = (
        f"docs/techniques/"
        f"{_tactic_slug(filename)}/"
        f"{filename}.md"
    )
    if not os.path.exists(technique_file):
        errors.append(
            f"No matching technique file found at: {technique_file}. "
            f"Sigma rules must have a corresponding technique entry."
        )

    return errors

def _tactic_slug(technique_id):
    tactic_map = {
        "REC": "reconnaissance",
        "AUTH": "authentication-abuse",
        "AUTHZ": "authorization-failure",
        "EXFIL": "exfiltration",
        "IMPACT": "impact",
    }
    parts = technique_id.split("-")
    if len(parts) >= 2:
        return tactic_map.get(parts[1], "unknown")
    return "unknown"

def main():
    changed_files = get_changed_sigma_files()

    if not changed_files or changed_files == [""]:
        print("No Sigma rule files changed — skipping Sigma validation.")
        sys.exit(0)

    print(f"Validating {len(changed_files)} Sigma rule file(s)...\n")

    all_errors = {}
    for filepath in changed_files:
        errors = validate_sigma_file(filepath)
        if errors:
            all_errors[filepath] = errors

    if all_errors:
        print("SIGMA VALIDATION FAILED\n" + "="*50)
        for filepath, errors in all_errors.items():
            print(f"\n{filepath}:")
            for error in errors:
                print(f"  ✗ {error}")
        sys.exit(1)
    else:
        print(f"All {len(changed_files)} Sigma rule file(s) passed validation.")
        sys.exit(0)

if __name__ == "__main__":
    main()
