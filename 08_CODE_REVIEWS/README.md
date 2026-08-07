# Code Reviews

> Every piece of code in CLOS gets reviewed across 7 dimensions. No exceptions.

---

## The 7-Dimension Review Checklist

### 1. 🔐 Security
- [ ] No hardcoded secrets or credentials
- [ ] Input validation on all external inputs
- [ ] Output encoding to prevent injection
- [ ] Authentication and authorization properly implemented
- [ ] Cryptographic operations use approved algorithms and libraries
- [ ] Error messages don't leak sensitive information
- [ ] Dependencies are up to date and free of known vulnerabilities
- [ ] OWASP Top 10 risks considered

### 2. 🔧 Maintainability
- [ ] Code follows project conventions and style guide
- [ ] Functions/methods are small and focused (single responsibility)
- [ ] No unnecessary complexity or over-engineering
- [ ] Magic numbers and strings are replaced with named constants
- [ ] No duplicated code (DRY principle applied thoughtfully)

### 3. 📖 Readability
- [ ] Variable and function names are descriptive and consistent
- [ ] Comments explain "why", not "what"
- [ ] Code is self-documenting where possible
- [ ] Complex logic has explanatory comments
- [ ] Consistent formatting and indentation

### 4. ⚡ Performance
- [ ] No N+1 query problems
- [ ] No unnecessary memory allocations
- [ ] No blocking I/O in async contexts
- [ ] Appropriate use of caching
- [ ] No premature optimization (but no obvious anti-patterns either)

### 5. 🏗️ Architecture
- [ ] Follows established architectural patterns
- [ ] Proper separation of concerns
- [ ] Dependencies point in the right direction
- [ ] No circular dependencies
- [ ] Changes are in the right layer/component

### 6. 🧪 Testing
- [ ] Unit tests cover happy path and edge cases
- [ ] Negative test cases (invalid input, error conditions)
- [ ] Tests are readable and maintainable
- [ ] No flaky tests
- [ ] Integration tests where appropriate
- [ ] Security-specific test cases (auth bypass, injection)

### 7. 📈 Scalability
- [ ] Will this work at 10x current scale?
- [ ] No single points of failure
- [ ] Stateless where possible
- [ ] Database queries are indexed
- [ ] No unbounded operations (pagination, limits)

---

## Review Process

1. **Author** submits code with context (what, why, design decisions)
2. **Reviewer** reads code against the 7-dimension checklist
3. **Reviewer** provides feedback: ✅ Approve, 💬 Comment, 🔴 Request Changes
4. **Author** addresses feedback
5. **Both** document lessons in the review log

---

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| 🔴 **Blocker** | Security vulnerability, data loss risk, broken functionality | Must fix before merge |
| 🟠 **Major** | Significant design issue, missing tests, performance problem | Should fix before merge |
| 🟡 **Minor** | Style inconsistency, naming improvement, minor optimization | Fix or acknowledge |
| 🟢 **Nit** | Personal preference, optional improvement | Author's discretion |

---

## Review Log

_Completed reviews are stored in the [reviews/](./reviews/) directory._

| # | Date | Code Reviewed | Findings | Severity | Link |
|---|------|--------------|----------|----------|------|
| 1 | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ |

---

*Every code review is a learning opportunity. Capture insights in the [Learning Log](../05_LEARNING_LOG/LEARNING_LOG.md).*
