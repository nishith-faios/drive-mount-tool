#!/usr/bin/env python3
"""PreToolUse(Bash), cloud only: same Tier-1 regex list as the Mac gate. The Mac Jev check stays on the Mac.
Deletes: move to a dated .trash/ folder instead. Fails open on unreadable input."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cloud_common import cloud_only, emit
cloud_only()
PATTERNS = [
    r"\bgit\s+(\S+\s+)*reset\s+(\S+\s+)*--hard\b",
    r"\bgit\s+(\S+\s+)*push\s+(\S+\s+)*(--force\b|-f\b)",
    r"\bgit\s+(\S+\s+)*clean\s+(\S+\s+)*-[a-z]*f",
    r"\bgit\s+filter-branch\b", r"\bgit\s+filter-repo\b",
    r"\brm\s+(-[a-z]*\s+)*-[a-z]*r[a-z]*f", r"\brm\s+-rf?\b",
    r"\bmkfs\b|\bdiskutil\s+erase",
    r"\bDROP\s+(TABLE|DATABASE)\b",
]
_RUNS = re.compile(r"\b((ba|z|k|da)?sh|python3?|perl|ruby|node|eval|xargs|sudo|ssh|source)\b")
def strip_heredocs(cmd):
    out, lines, i = [], cmd.split("\n"), 0
    while i < len(lines):
        out.append(lines[i])
        m = re.search(r"(?<!<)<<(?!<)-?\s*(['\"\\]?)([A-Za-z_][A-Za-z0-9_]*)", lines[i])
        if m and not _RUNS.search(lines[i]):
            j = i + 1
            while j < len(lines) and lines[j].strip() != m.group(2):
                j += 1
            body = "\n".join(lines[i + 1:j])
            if j < len(lines) and (m.group(1) or not re.search(r"\$\(|`", body)):
                out.append(lines[j]); i = j
        i += 1
    return "\n".join(out)
try:
    cmd = strip_heredocs((json.load(sys.stdin).get("tool_input") or {}).get("command", ""))
except Exception:
    sys.exit(0)
for p in PATTERNS:
    if re.search(p, cmd, re.I if "DROP" in p else 0):
        emit("PreToolUse", permissionDecision="deny", permissionDecisionReason=(
            "Blocked by Nishith's destructive-command gate (cloud copy). To delete, move the file to a dated "
            ".trash/ folder (mv x .trash/$(date +%F)_x). Force push, hard reset and history rewrites need "
            "Nishith to run them himself."))
        break
sys.exit(0)
