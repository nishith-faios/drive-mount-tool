"""Shared helpers for the cloud-only hooks. Every cloud hook exits at once on the Mac
(CLAUDE_CODE_REMOTE is only 'true' in cloud sessions), so the Mac hooks stay the only gate there."""
import json, os, sys

def cloud_only():
    if os.environ.get("CLAUDE_CODE_REMOTE") != "true":
        sys.exit(0)

def project_dir():
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()

def handoff_path():
    return os.path.join(project_dir(), ".claude", "handoff", "latest.md")

def last_ctx(path):
    """Context size (tokens) of the last assistant turn in the transcript tail. 0 if unknown."""
    try:
        with open(path, "rb") as f:
            f.seek(0, 2); size = f.tell(); f.seek(max(0, size - 600_000))
            lines = f.read().splitlines()
        for line in reversed(lines):
            if b'"usage"' not in line or b'"assistant"' not in line:
                continue
            try:
                u = json.loads(line)["message"]["usage"]
            except Exception:
                continue
            return sum((u.get(k) or 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
    except Exception:
        pass
    return 0

def count_user_turns(path):
    n = 0
    try:
        with open(path, "rb") as f:
            for line in f:
                if b'"type":"user"' in line or b'"role":"user"' in line:
                    n += 1
    except Exception:
        pass
    return n

def emit(event, **kw):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event, **kw}}))
