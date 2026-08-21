#!/usr/bin/env python3
"""
Hands-On DevSecOps Lab Scanner
Simulates SAST & IaC Security Analysis on local files.
"""

import os
import re

def scan_file(filepath):
    print(f"\n🔍 Scanning file: {filepath}...")
    findings = []
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    for idx, line in enumerate(lines, 1):
        # Check 1: AWS Secret Key Pattern
        if re.search(r'(AKIA|ASIA)[A-Z0-9]{16}', line):
            findings.append({
                "rule": "SEC-001 (Hardcoded AWS Key)",
                "severity": "🔴 CRITICAL",
                "line": idx,
                "snippet": line.strip(),
                "recommendation": "Remove hardcoded credentials! Use OIDC or AWS IAM Roles."
            })
            
        # Check 2: Database Password Pattern
        if re.search(r'password\s*=\s*["\'][^"\']+["\']', line, re.IGNORECASE):
            findings.append({
                "rule": "SEC-002 (Hardcoded DB Password)",
                "severity": "🔴 CRITICAL",
                "line": idx,
                "snippet": line.strip(),
                "recommendation": "Move password to Secrets Manager / HashiCorp Vault."
            })

        # Check 3: Public S3 ACL
        if 'acl = "public-read"' in line or 'acl = "public-read-write"' in line:
            findings.append({
                "rule": "IAC-001 (Public S3 Bucket ACL)",
                "severity": "🔴 CRITICAL",
                "line": idx,
                "snippet": line.strip(),
                "recommendation": "Enforce S3 Public Access Block and set ACL to private."
            })
            
    return findings

def main():
    target_dir = "07_PRIMARY_PROJECT/iac/environments/dev"
    total_findings = 0
    
    print("=" * 70)
    print("  DEVSECOPS HANDS-ON SCANNER LAB — RUNNING SECURITY AUDIT")
    print("=" * 70)
    
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.tf'):
                full_path = os.path.join(root, file)
                results = scan_file(full_path)
                if results:
                    total_findings += len(results)
                    for item in results:
                        print(f"\n  [{item['severity']}] {item['rule']}")
                        print(f"   Line {item['line']}: `{item['snippet']}`")
                        print(f"   💡 Recommendation: {item['recommendation']}")
                else:
                    print(f"  ✅ Compliant (0 findings)")
                    
    print("\n" + "=" * 70)
    print(f"  SUMMARY: Total Security Vulnerabilities Detected: {total_findings}")
    print("=" * 70)

if __name__ == "__main__":
    main()
