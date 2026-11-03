#!/usr/bin/env python3
"""UserPromptSubmit (cloud only): warn when an image is pasted (about 2,000 tokens; a file path costs 20)."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cloud_common import cloud_only, emit
cloud_only()
try:
    p = str(json.load(sys.stdin).get("prompt", ""))
    if "[Image" in p or "[image" in p:
        emit("UserPromptSubmit", additionalContext="[Token guard] Image in prompt costs ~2,000 tokens. Use it for visual judgement only; ask for file paths otherwise.")
except Exception:
    pass
sys.exit(0)
