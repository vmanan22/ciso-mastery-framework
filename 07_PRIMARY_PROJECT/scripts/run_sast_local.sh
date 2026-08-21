#!/usr/bin/env bash
# ==============================================================================
# Local SAST Scanner — Run Before Every Git Push
#
# LEARNING: "Shift-Left" security means catching vulnerabilities as early
# as possible — ideally on the developer's own machine, not in CI.
#
# WHY run this locally?
# CI feedback takes 5-15 minutes. Local scan takes 10 seconds.
# Finding a security bug locally means: fix it, commit, done.
# Finding it in CI means: wait 10 min, see the failure, fix it, push again, wait 10 min.
#
# HOW: Add this to your pre-commit hook or run manually before `git push`.
#
# USAGE:
#   chmod +x scripts/run_sast_local.sh
#   ./scripts/run_sast_local.sh
# ==============================================================================

set -euo pipefail
# set -e: exit immediately if any command fails
# set -u: treat undefined variables as errors
# set -o pipefail: a pipeline fails if ANY command in it fails (not just the last)
# WHY? Without these, silent failures are common: `failing_command | grep something`
# exits 0 if grep succeeds, hiding the failing_command's error.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
APP_DIR="$PROJECT_ROOT/containers/app"
RESULTS_DIR="/tmp/ssdlc-sast-results"

echo "======================================================"
echo "  SSDLC Platform — Local SAST Security Scanner"
echo "======================================================"
echo "  Scanning: $APP_DIR"
echo "  Results:  $RESULTS_DIR"
echo "======================================================"

mkdir -p "$RESULTS_DIR"

FAILED=0

# ------------------------------------------------------------------------------
# TOOL 1: Bandit — Python Security Linter
#
# LEARNING: Bandit is purpose-built for Python security issues:
# - B301: Pickle usage (arbitrary code execution risk)
# - B303: Use of MD5 (weak hash — not for security purposes)
# - B506: yaml.load without Loader (code execution via YAML)
# - B601: Paramiko shell invocation (command injection)
# - B602: subprocess with shell=True (command injection)
# - B701: Jinja2 autoescape disabled (XSS)
# ------------------------------------------------------------------------------
echo ""
echo "📋 Running Bandit Python Security Linter..."
echo "------------------------------------------------------"

if command -v bandit &>/dev/null; then
    bandit \
        -r "$APP_DIR" \
        -ll \
        --format txt \
        2>&1 | tee "$RESULTS_DIR/bandit.txt"

    # Check if any HIGH severity findings exist
    if grep -q "Severity: High" "$RESULTS_DIR/bandit.txt" 2>/dev/null; then
        echo "❌ BANDIT: HIGH severity findings detected!"
        FAILED=1
    else
        echo "✅ BANDIT: No HIGH severity findings"
    fi
else
    echo "⚠️  Bandit not installed. Install with: pip install bandit"
    echo "    Skipping Bandit scan..."
fi

# ------------------------------------------------------------------------------
# TOOL 2: Semgrep — OWASP Top 10 + Custom Rules
#
# LEARNING: Semgrep uses pattern matching on the code's AST
# (Abstract Syntax Tree — the structured representation of code).
# This is more accurate than regex because it understands code structure.
# Example: `pattern: subprocess.$FUNC(shell=True)` matches REGARDLESS of
# whether it's `subprocess.run`, `subprocess.call`, or `subprocess.Popen`.
# ------------------------------------------------------------------------------
echo ""
echo "📋 Running Semgrep OWASP + Custom Rules..."
echo "------------------------------------------------------"

if command -v semgrep &>/dev/null; then
    semgrep \
        --config=p/owasp-top-ten \
        --config=p/python \
        --config="$PROJECT_ROOT/.semgrep.yml" \
        "$APP_DIR" \
        --text \
        --output "$RESULTS_DIR/semgrep.txt" \
        --timeout 60 \
        2>&1 | tee /dev/stderr

    if grep -q "severity: ERROR" "$RESULTS_DIR/semgrep.txt" 2>/dev/null; then
        echo "❌ SEMGREP: ERROR severity findings detected!"
        FAILED=1
    else
        echo "✅ SEMGREP: No ERROR severity findings"
    fi
else
    echo "⚠️  Semgrep not installed. Install with: pip install semgrep"
    echo "    Or: brew install semgrep"
    echo "    Skipping Semgrep scan..."
fi

# ------------------------------------------------------------------------------
# TOOL 3: Gitleaks — Secret Detection
#
# Scans the git index (staged changes) + recent commits.
# This is the LOCAL version. CI scans ALL history with fetch-depth: 0.
# ------------------------------------------------------------------------------
echo ""
echo "📋 Running Gitleaks Secret Scan..."
echo "------------------------------------------------------"

if command -v gitleaks &>/dev/null; then
    gitleaks detect \
        --source "$PROJECT_ROOT" \
        --config "$PROJECT_ROOT/.gitleaks.toml" \
        --no-git \
        --report-path "$RESULTS_DIR/gitleaks.json" \
        --report-format json \
        2>&1

    if [ -s "$RESULTS_DIR/gitleaks.json" ] && \
       [ "$(cat "$RESULTS_DIR/gitleaks.json")" != "[]" ]; then
        echo "❌ GITLEAKS: Secrets detected in source files!"
        FAILED=1
    else
        echo "✅ GITLEAKS: No secrets detected"
    fi
else
    echo "⚠️  Gitleaks not installed. Install with: brew install gitleaks"
    echo "    Skipping Gitleaks scan..."
fi

# ------------------------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------------------------
echo ""
echo "======================================================"
echo "  SAST SCAN COMPLETE"
echo "======================================================"
echo "  Results saved to: $RESULTS_DIR/"
echo "======================================================"

if [ "$FAILED" -eq 1 ]; then
    echo ""
    echo "❌ FAILED: Security issues detected. Fix before pushing."
    echo "   Review detailed results in: $RESULTS_DIR/"
    exit 1
else
    echo ""
    echo "✅ PASSED: All local security checks passed."
    echo "   Safe to push. CI will run the full pipeline."
    exit 0
fi
