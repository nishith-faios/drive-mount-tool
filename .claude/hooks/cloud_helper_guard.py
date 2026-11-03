#!/usr/bin/env python3
"""PreToolUse(Agent|Task), cloud only. Helper agents must name a cheaper model (haiku/sonnet), or the prompt must
start with 'HEAVY: <reason>'. Project rule: at most 2 threads at once, no fan-out unless asked. Fails open."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cloud_common import cloud_only, emit
cloud_only()
try:
    ti = json.load(sys.stdin).get("tool_input") or {}
except Exception:
    sys.exit(0)
if (ti.get("subagent_type") or "") == "fork" or (ti.get("model") or "").strip() or (ti.get("prompt") or "").lstrip().upper().startswith("HEAVY:"):
    sys.exit(0)
emit("PreToolUse", permissionDecision="deny", permissionDecisionReason=(
    "Helper-model guard: set model to 'haiku' or 'sonnet', give exact paths, cap the answer at ~300 words. "
    "For real heavy work start the prompt with 'HEAVY: <reason>'. Helpers need a reason; tokens are Nishith's hardest limit."))
sys.exit(0)
