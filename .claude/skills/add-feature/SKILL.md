---
name: add-feature
description: >
  Spec-first feature development. Generates a spec and waits for
  explicit approval before writing any implementation code.
  Always builds in order: model → service → API → tests.
---

# ✨ ADD FEATURE MODE — Active

**Rules for this skill:**
- NEVER write implementation code before the spec is approved
- ALWAYS wait for the user to say "approved", "go ahead", or "looks good"
- ALWAYS verify with tests after implementation

## PHASE 1: SPEC (no code until user approves)

Read first: `CLAUDE.md` + any files the feature will touch

Generate:
```markdown
## Feature Spec: [Name]
**Status:** 🟡 DRAFT — Awaiting Your Approval

### What We're Building
[2-3 sentences. What problem does this solve?]

### Scope
✅ In scope: [specific things]
❌ Out of scope: [things explicitly excluded]

### Files That Will Change
| File | Change | Why |
|------|--------|-----|
| src/... | New/Modify | ... |

### API / Interface Design
[function signatures, endpoint definitions, or component props]

### Edge Cases to Handle
- [ ] Null / empty input
- [ ] Concurrent requests / race conditions
- [ ] Auth / permissions
- [ ] [domain-specific edge case]

### Done Criteria ✓
- [ ] All existing tests pass
- [ ] New tests cover edge cases
- [ ] No TypeScript errors
- [ ] No lint errors
- [ ] CLAUDE.md updated if new convention added
```

End with: "Does this spec look right? Say 'approved' or let me know what to adjust."

## PHASE 2: BUILD (only after explicit approval)

Build in this exact order:
1. **Data model** (migrations if schema changes)
2. **Service layer** (business logic)
3. **API layer** (routes / controllers)
4. **Tests** (alongside each layer)

After each file: run `npm run typecheck && npm run lint` — fix before moving on.

Final check: `npm test && npm run lint && npm run typecheck`
Show the output. Do not declare done without it.

Completion report:
```
## Feature Complete ✅
- Files created: [list]
- Files modified: [list]
- Tests: X/X passing
- Edge cases covered: [list]
- CLAUDE.md needs update: Yes/No — [what to add]
```
