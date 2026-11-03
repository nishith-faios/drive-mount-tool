#!/usr/bin/env python3
"""PreToolUse (cloud only). Past CLOUD_CTX_HARD tokens (default 120000), allow only the handoff write,
the thread reply tools and the coordinator message. Fails open on any error."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cloud_common import cloud_only, emit, last_ctx, handoff_path
cloud_only()
try:
    ev = json.load(sys.stdin)
    hard = int(os.environ.get("CLOUD_CTX_HARD", "120000"))
    path = ev.get("transcript_path") or ""
    if not path or last_ctx(path) < hard:
        sys.exit(0)
    tool = ev.get("tool_name", "")
    if tool.startswith("mcp__hearthbot__") or tool in ("send_message", "message_coordinator", "TodoWrite"):
        sys.exit(0)
    if tool in ("Write", "Edit", "MultiEdit"):
        fp = os.path.realpath((ev.get("tool_input") or {}).get("file_path", "") or "")
        if fp == os.path.realpath(handoff_path()):
            sys.exit(0)
    emit("PreToolUse", permissionDecision="deny", permissionDecisionReason=(
        f"HARD STOP {hard // 1000}k context: write the 5-line handoff to {handoff_path()}, send it to the "
        "coordinator, tell Nishith in one line, and stop. Do not start new work."))
except Exception:
    pass
sys.exit(0)
