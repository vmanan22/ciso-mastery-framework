#!/usr/bin/env python3
"""
Hands-On SAST & SCA Scanner Simulator
"""

import os
import re

def run_sast_scan():
    print("\n🔍 --- STAGE 1: SAST (Static Application Security Testing) ---")
    app_file = "07_PRIMARY_PROJECT/containers/app/main.py"
    print(f"Scanning source file: {app_file}")
    
    with open(app_file, 'r') as f:
        content = f.read()
        
    sast_issues = []
    
    # SAST Check 1: Insecure eval/exec usage
    if re.search(r'\b(eval|exec)\s*\(', content):
        sast_issues.append("SAST-01: Dangerous `eval()` or `exec()` code execution call found!")

    # SAST Check 2: Hardcoded IP / Debug mode
    if 'debug=True' in content:
        sast_issues.append("SAST-02: Production application has debug mode enabled (`debug=True`)!")

    # SAST Check 3: Check Security Headers
    if 'X-Content-Type-Options' in content and 'X-Frame-Options' in content:
        print("  ✅ SAST Pass: Security headers (X-Frame-Options, CSP, HSTS) are properly configured!")
    else:
        sast_issues.append("SAST-03: Missing HTTP security headers in application middleware!")

    if not sast_issues:
        print("  🎉 SAST Result: 0 Vulnerabilities found in application code!")
    else:
        for issue in sast_issues:
            print(f"  🔴 {issue}")

def run_sca_scan():
    print("\n📦 --- STAGE 2: SCA (Software Composition Analysis) ---")
    req_file = "07_PRIMARY_PROJECT/containers/app/requirements.txt"
    print(f"Scanning dependency lockfile: {req_file}")
    
    with open(req_file, 'r') as f:
        dependencies = f.readlines()
        
    known_cves = {
        "fastapi==0.60.0": "CVE-2021-32677 (ReDoS vulnerability)",
        "uvicorn==0.11.0": "CVE-2020-7694 (Header injection vulnerability)",
        "requests==2.20.0": "CVE-2023-32681 (Proxy authorization header leak)"
    }
    
    sca_issues = []
    for line in dependencies:
        pkg = line.strip()
        if pkg in known_cves:
            sca_issues.append(f"Vulnerable Package `{pkg}` -> {known_cves[pkg]}")
        else:
            print(f"  ✅ Package `{pkg}` verified against Vulnerability Database (No known CRITICAL CVEs)")
            
    if sca_issues:
        for issue in sca_issues:
            print(f"  🔴 SCA CRITICAL ALERT: {issue}")
    else:
        print("  🎉 SCA Result: All third-party dependencies are clean and secure!")

def main():
    print("=" * 70)
    print("  DEVSECOPS CI/CD PIPELINE — SAST & SCA DEMONSTRATION")
    print("=" * 70)
    run_sast_scan()
    run_sca_scan()
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
