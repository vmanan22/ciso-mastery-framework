# Hall of Pain 🔥

> Every mistake is a lesson. Every lesson is progress. Track them here ruthlessly.
>
> **Rule**: No vague entries. Be specific about what happened, why, and what you'll do differently.

---

## Mistake Log

| # | Date | Category | What Happened | Root Cause | Lesson Learned | Prevention Strategy |
|---|------|----------|--------------|------------|----------------|---------------------|
| 1 | 2026-08-21 | Process / CI | Workflows placed in subdirectories were not picked up by GitHub Actions | GitHub Actions strictly mandates workflows in root `.github/workflows/` | GitHub repository root is the only valid location for Actions workflows | Always verify workflow path is `.github/workflows/*.yml` at workspace root |
| 2 | 2026-08-21 | Security / Git | Pushing workflow file rejected by remote | Git CLI token lacked explicit `workflow` OAuth scope | GitHub requires separate `workflow` scope to prevent unauthorized pipeline tampering | Run `gh auth refresh -s workflow` when managing CI/CD workflows |
| 3 | 2026-08-21 | Security / Code | Hardcoded API key found in local client script | Placeholder key left in during quick prototyping | Secrets in source files get committed if not checked | Run automated pre-commit scanners (`gitleaks`, `semgrep`) before every commit |


---

## Categories

- **Security** — Missed vulnerability, weak control, insecure design
- **Architecture** — Poor design decision, scalability miss, wrong pattern
- **Code** — Bug, anti-pattern, poor readability, missing tests
- **Communication** — Unclear explanation, wrong audience level, missing context
- **Process** — Skipped step, wrong prioritization, scope creep
- **Knowledge Gap** — Didn't know a concept, used wrong terminology

---

## Anti-Patterns I've Caught Myself Doing

| Anti-Pattern | Times Caught | Last Occurrence | Status |
|-------------|-------------|----------------|--------|
| _e.g., "Jumping to code before understanding the problem"_ | _0_ | _N/A_ | 🔴 Active |

---

## Hall of Fame (Graduated Lessons)

> When a lesson has been fully internalized (3+ weeks without repeating), move it here.

| # | Original Mistake | Lesson | Graduated Date |
|---|-----------------|--------|----------------|
| | | | |

---

*Update this after every session, weekly challenge, and code review.*
