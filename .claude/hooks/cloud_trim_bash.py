#!/usr/bin/env python3
"""PreToolUse(Bash), cloud only: pipe long command output through cloud_trim_output.py (keeps the tail)."""
import json, sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cloud_common import cloud_only, emit, project_dir
cloud_only()
BOUNDED = re.compile(r'\|\s*(tail|head)\b|cloud_trim_output\.py|--quiet|-q\b')
SKIP = re.compile(r'<<|&\s*$|\btail\s+-f\b|^\s*(cd|export|source|pushd|popd|alias|set)\b|\b(vim|vi|nano|less|more|top|watch|ssh)\b')
try:
    ev = json.load(sys.stdin)
except Exception:
    sys.exit(0)
ti = ev.get("tool_input") or {}
cmd = ti.get("command", "")
if ev.get("tool_name") != "Bash" or not cmd or BOUNDED.search(cmd) or SKIP.search(cmd) or ti.get("run_in_background"):
    sys.exit(0)
trim = os.path.join(project_dir(), ".claude", "hooks", "cloud_trim_output.py")
new = dict(ti, command=f"set -o pipefail; {{ {cmd.rstrip(chr(10)).rstrip(';')} ; }} 2>&1 | TRIM_TAIL=40 python3 {trim}")
print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "updatedInput": new}}))
