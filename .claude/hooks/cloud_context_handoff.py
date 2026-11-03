#!/usr/bin/env python3
"""UserPromptSubmit (cloud only). Cloud context is small. Past WARN tokens or 15 turns, ask Claude to wrap up
and hand off; past HARD, cloud_hard_stop.py limits tools. Never blocks. Fails silent.
Env: CLOUD_CTX_WARN (default 60000), CLOUD_CTX_HARD (default 120000)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cloud_common import cloud_only, emit, last_ctx, count_user_turns, handoff_path
cloud_only()
try:
    ev = json.load(sys.stdin)
    path = ev.get("transcript_path") or ""
    warn = int(os.environ.get("CLOUD_CTX_WARN", "60000"))
    hard = int(os.environ.get("CLOUD_CTX_HARD", "120000"))
    ctx = last_ctx(path) if path else 0
    turns = count_user_turns(path) if path else 0
    if ctx >= warn or turns >= 15:
        sf = os.path.join(os.environ.get("TMPDIR", "/tmp"), "cloud_ctx_alert_" + str(ev.get("session_id", "x")))
        level = ctx // 20000
        try:
            seen = int(open(sf).read() or -1)
        except Exception:
            seen = -1
        if level > seen:
            open(sf, "w").write(str(level))
            emit("UserPromptSubmit", additionalContext=(
                f"[Context heavy: ~{ctx // 1000}k tokens, {turns} turns] Finish only the step in progress. "
                f"Then write a 5-line handoff (goal, done with proof, left, next step, files) to {handoff_path()}, "
                "send the same 5 lines to the coordinator with message_coordinator, and tell Nishith in one line. "
                "Do NOT tell him to start a new chat; the coordinator starts the fresh thread. "
                f"Hard stop at {hard // 1000}k: after that only the handoff can be written."))
except Exception:
    pass
sys.exit(0)
