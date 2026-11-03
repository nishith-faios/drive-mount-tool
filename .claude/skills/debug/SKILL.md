---
name: debug
description: >
  Auto-triggered 2-phase debug workflow. Phase 1 = diagnosis only,
  Phase 2 = targeted fix + regression test. Never skips diagnosis.
---

# 🔍 DEBUG MODE — Active

**Rules for this skill:**
- NEVER suggest a code fix before completing Phase 1
- NEVER say "I think the issue is X, let me fix it" — always hypothesize first
- ALWAYS end Phase 2 by running tests and showing output

## PHASE 1: DIAGNOSIS

Ask the user for if not already provided:
- Exact error / stack trace
- Relevant code snippet or file path
- What they already tried

Then output:
```
## Root Cause Analysis
**Error:** [one-line summary]
**Affected files:** [list]

### Hypothesis 1 (~X% likely) — [label]
- Cause: [what is wrong]
- Evidence: [what supports this in code/logs]
- Explains: [why the error occurs]

### Hypothesis 2 (~X% likely) — [label]
...

### Hypothesis 3 (~X% likely) — [label]
...

**To confirm Hypothesis 1, I need:**
- [ ] [specific log line or command to run]
- [ ] [specific test to execute]
```

End with: "Which hypothesis should I investigate? Or share more context and I'll refine."

## PHASE 2: FIX (only after user confirms diagnosis)

1. Implement minimal targeted fix for confirmed root cause
2. Add inline comment: `// Fix: [why this solves the root cause]`
3. Write a regression test:
   ```typescript
   // This test would have caught the bug before production
   it('should [expected behavior] when [the edge case that caused the bug]', () => {
     // Arrange / Act / Assert
   })
   ```
4. Run: `npm test [relevant file] && npm run lint`
5. Show the passing output — do not proceed until green

Output fix summary:
```
## Fix Summary ✅
- Root Cause: [confirmed hypothesis]
- Fix: [what changed and why]
- Files modified: [list]
- Regression test: [test name + file]
- Confidence: High / Medium — [reason]
```
