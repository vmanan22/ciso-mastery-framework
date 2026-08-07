# Secure Code Review

> Develop the ability to find vulnerabilities, anti-patterns, and quality issues in code.

---

## Learning Objectives

- [ ] Identify OWASP Top 10 vulnerabilities in source code
- [ ] Review code for authentication, authorization, and session management flaws
- [ ] Spot injection vulnerabilities (SQL, command, LDAP, XSS, template)
- [ ] Evaluate cryptographic implementations (key management, algorithm choice)
- [ ] Assess error handling and logging practices (information leakage)
- [ ] Review code for business logic flaws and race conditions
- [ ] Provide actionable, constructive feedback in code reviews

---

## Difficulty Levels

| Level | Description |
|-------|-------------|
| 🟢 Beginner | Find obvious injection flaws, missing input validation, hardcoded secrets |
| 🟡 Intermediate | Identify auth bypass, insecure deserialization, broken access control |
| 🔴 Advanced | Find race conditions, business logic flaws, cryptographic weaknesses |

---

## Curated Resources

- OWASP Code Review Guide v2
- OWASP Top 10 (with code examples)
- SEI CERT Coding Standards (C, Java, etc.)
- *The Art of Software Security Assessment* by Dowd, McDonald & Schuh

---

## Review Checklist

When reviewing any code, check:

- [ ] **Security** — Injection, auth, crypto, data exposure
- [ ] **Maintainability** — Naming, structure, complexity
- [ ] **Readability** — Comments, formatting, clarity
- [ ] **Performance** — N+1 queries, unnecessary allocations, blocking I/O
- [ ] **Architecture** — Separation of concerns, dependency direction
- [ ] **Testing** — Coverage, edge cases, negative tests
- [ ] **Scalability** — Bottlenecks, statelessness, caching

---

## Exercise Index

| # | Exercise | Level | Status |
|---|----------|-------|--------|
| 1 | _To be added_ | 🟢 | ⬜ |

---

*Exercises are stored in the [exercises/](./exercises/) directory.*
