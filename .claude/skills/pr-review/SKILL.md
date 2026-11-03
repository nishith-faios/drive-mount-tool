---
name: pr-review
description: >
  Systematic 5-pass PR review. Checks correctness, security,
  convention compliance, test coverage, and performance.
  Outputs structured GitHub-ready review comments.
---

# 🔎 PR REVIEW MODE — Active

**Rules for this skill:**
- Run ALL 5 passes — never skip one, even if the code looks clean
- Check against conventions in `CLAUDE.md` specifically
- Always output the summary table at the end

## Content Index
- **Setup** (Line ~20)
- **The 5 Review Passes** (Line ~28)
  - Pass 1: Bugs & Correctness
  - Pass 2: Security & Vulnerabilities
  - Pass 3: Convention Compliance (`CLAUDE.md`)
  - Pass 4: Test Coverage & Edge Cases
  - Pass 5: Performance & Resource Hygiene
- **Output Format & Summary Scorecard** (Line ~75)

---

## Setup
Before reviewing, read:
1. `CLAUDE.md` → conventions to enforce
2. The diff / files provided by the user
3. Run `git log --oneline -5` if in a Claude Code session

## The 5 Passes

### Pass 1 — Bugs & Correctness 🔴
- Logic errors, off-by-one, null/undefined not handled
- Async/await misuse, unhandled promise rejections
- Error swallowing (empty catch blocks)
- Mutations of shared/external state
- Memory leaks (event listeners, open connections, intervals)

### Pass 2 — Security 🔐
- SQL/NoSQL injection (user input reaching a query)
- Unvalidated or unsanitized input
- Hardcoded secrets or tokens (even in test files)
- Missing auth/permission checks on sensitive routes
- Sensitive data appearing in logs
- Overly permissive CORS headers

### Pass 3 — Convention Compliance 📋
Cross-check against CLAUDE.md conventions:
- Naming conventions
- Forbidden patterns (raw throws, console.log, `any` types)
- Required patterns (custom error class, logger, db singleton)
- File structure and placement

### Pass 4 — Test Coverage 🧪
- Is every new public function tested?
- Are edge cases covered (null, empty, max values)?
- Are tests meaningful (not just happy path assertions)?
- Would these tests catch a regression if the code broke?

### Pass 5 — Performance ⚡
- N+1 query problems (DB calls inside loops)
- Missing indexes for new query patterns
- Blocking synchronous ops that should be async
- Unnecessary re-computation or re-renders
- Large payload sizes not being paginated

## Output Format

```markdown
# PR Review: [Branch / PR Title]
**Date:** [today] | **Overall:** ✅ Approve / ⚠️ Approve with Comments / 🔴 Request Changes

---

## 🔴 MUST FIX (Blockers)
### [File.ts:Line] — [Issue Title]
**Problem:** [what is wrong]
**Risk:** [what could go wrong in production]
**Fix:**
\`\`\`typescript
// corrected code here
\`\`\`

---

## ⚠️ SHOULD FIX (Non-blocking but important)
### [File.ts:Line] — [Issue Title]
**Problem:** [description]
**Suggested Fix:** [how to fix]

---

## 💡 NICE TO HAVE (Optional)
- [suggestion]

---

## ✅ What's Done Well
- [positive observation]

---

## 📊 Summary
| Area | Status | Notes |
|------|--------|-------|
| Correctness | ✅/⚠️/🔴 | |
| Security | ✅/⚠️/🔴 | |
| Conventions | ✅/⚠️/🔴 | |
| Test Coverage | ✅/⚠️/🔴 | |
| Performance | ✅/⚠️/🔴 | |
```
