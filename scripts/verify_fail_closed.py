#!/usr/bin/env python3
"""
Pipeline Fail-Closed Regression & Integrity Verifier
Verifies that CI/CD workflows do NOT contain forbidden failure-masking patterns.

Forbidden Anti-Patterns:
1. `|| true` on security scanner, policy, or build commands
2. `--soft-fail` on security linters/scanners (e.g. Checkov)
3. `exit-code: "0"` or `exit-code: 0` on vulnerability blockers (Trivy)
4. Synthetic empty artifact generation (e.g. fake tfplan.json substitution)
"""

import sys
import re
from pathlib import Path

FORBIDDEN_PATTERNS = [
    (r"\|\|\s*true", "Found failure-masking '|| true'"),
    (r"--soft-fail", "Found scanner soft-fail flag '--soft-fail'"),
    (r"exit-code:\s*['\"]?0['\"]?", "Found Trivy exit-code: 0 (must be 1 for HIGH/CRITICAL)"),
    (r"echo\s+['\"].*planned_values.*['\"]\s*>\s*.*tfplan\.json", "Found fake empty Terraform plan substitution"),
]

def verify_workflows(workflows_dir: Path) -> bool:
    failed = False
    if not workflows_dir.exists():
        print(f"❌ Workflows directory not found: {workflows_dir}")
        return False

    yaml_files = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
    if not yaml_files:
        print(f"❌ No workflow files found in: {workflows_dir}")
        return False

    print(f"🔍 Scanning {len(yaml_files)} workflow file(s) for failure-masking anti-patterns...")
    
    for yf in yaml_files:
        content = yf.read_text()
        for idx, line in enumerate(content.splitlines(), start=1):
            stripped = line.strip()
            # Ignore purely comment lines
            if stripped.startswith("#"):
                continue
            for pattern, msg in FORBIDDEN_PATTERNS:
                if re.search(pattern, line):
                    print(f"  ❌ {yf.name}:{idx} -> {msg}")
                    print(f"     Line: {line.strip()}")
                    failed = True


    if not failed:
        print("  ✅ All workflow files passed fail-closed verification (0 failure-masking patterns detected).")
    return not failed

if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    workflows = repo_root / ".github" / "workflows"
    success = verify_workflows(workflows)
    sys.exit(0 if success else 1)
