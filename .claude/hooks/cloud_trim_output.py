#!/usr/bin/env python3
"""stdin filter: keep every error-ish line + the last N lines. Used by trim_noisy_bash.py."""
import sys, re, os
N = int(os.environ.get("TRIM_TAIL", "30"))
ERR = re.compile(r'\b(error|ERROR|Error|FAIL|FAILED|failed|Traceback|Exception|fatal|panic|\
E\d{3}|warning: .*deprecated)\b')
lines = sys.stdin.read().splitlines()
if len(lines) <= N:
    print("\n".join(lines)); sys.exit(0)
tail = lines[-N:]
errs = [l for l in lines[:-N] if ERR.search(l)][:40]
if errs:
    print(f"[trimmed {len(lines)-N-len(errs)} quiet lines; {len(errs)} error lines kept]")
    print("\n".join(errs))
    print(f"--- last {N} lines ---")
else:
    print(f"[trimmed {len(lines)-N} lines, no error lines found; last {N} shown]")
print("\n".join(tail))
