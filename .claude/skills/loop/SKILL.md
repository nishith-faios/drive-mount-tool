---
name: loop
description: Goal loop for cloud threads. Use for any fix or build with a testable result, or when Nishith says loop, keep going until it works, or fix it properly.
---
1. State ONE check first: a command that exits 0 only when the goal is met (or a thing Nishith can see).
2. Make one change. Run the check. Keep the change only if the check passes; if it fails, undo it (`git checkout -- <file>`).
3. Never edit the check that scores you. Satisfying the letter while defeating the goal is a failure.
4. Max 5 tries. After that, undo, and report: tries, what failed, the exact next step.
5. Log each try as KEEP or DISCARD in your reply. End with `Checked:` (what you ran) and `Not checked:`.
