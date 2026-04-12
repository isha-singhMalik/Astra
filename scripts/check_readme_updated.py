#!/usr/bin/env python3
"""
ASTRA README Matrix Checker
Warns if a new technique was added without updating the matrix table in README.md
"""

import os
import sys
import subprocess
import re

def get_changed_technique_files():
    result = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        capture_output=True, text=True
    )
    files = result.stdout.strip().split("\n")
    return [
        f for f in files
        if f.startswith("docs/techniques/") and f.endswith(".md")
        and not f.endswith("index.md")
    ]

def technique_id_from_path(filepath):
    return os.path.basename(filepath).replace(".md", "")

def readme_contains_technique(technique_id):
    with open("README.md", "r") as f:
        content = f.read()
    return technique_id in content

def main():
    changed_files = get_changed_technique_files()

    if not changed_files or changed_files == [""]:
        sys.exit(0)

    missing_from_readme = []
    for filepath in changed_files:
        if not os.path.exists(filepath):
            continue
        technique_id = technique_id_from_path(filepath)
        if not readme_contains_technique(technique_id):
            missing_from_readme.append(technique_id)

    if missing_from_readme:
        print("README MATRIX NOT UPDATED\n" + "="*50)
        for tid in missing_from_readme:
            print(f"  ✗ {tid} is not in the README.md matrix table")
        print(
            "\nPlease add a row for each new technique to the "
            "matrix table in README.md.\nSee existing rows for the format."
        )
        sys.exit(1)
    else:
        print("README matrix is up to date.")
        sys.exit(0)

if __name__ == "__main__":
    main()
