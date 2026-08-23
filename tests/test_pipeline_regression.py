"""
Automated Pipeline Regression Test Suite
Validates that CI/CD workflows enforce fail-closed security invariants.
Compatible with both unittest and pytest.
"""

import unittest
from pathlib import Path
from scripts.verify_fail_closed import verify_workflows


class TestPipelineRegression(unittest.TestCase):
    def test_workflows_fail_closed(self):
        """Verifies that all GitHub Actions workflows are free from failure-masking patterns."""
        repo_root = Path(__file__).resolve().parent.parent
        workflows_dir = repo_root / ".github" / "workflows"
        self.assertTrue(workflows_dir.exists(), "Workflows directory does not exist")
        
        passed = verify_workflows(workflows_dir)
        self.assertTrue(passed, "Detected forbidden failure-masking patterns in workflows")


if __name__ == "__main__":
    unittest.main()
