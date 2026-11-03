#!/usr/bin/env python3
"""SessionStart (cloud only): Nishith's contract, short, plus how cloud threads differ from his Mac."""
from cloud_common import cloud_only, emit
cloud_only()
emit("SessionStart", additionalContext=(
    "[Contract] Act on go; ask first only for money, permanent delete, sending to a person. "
    "Every output/option to Nishith = 2 plain lines (what happened / what it does). "
    "Prove before saying done; tag claims Certain/Likely/Guessing. Anything he must do: "
    "'🟠 **NISHITH, DO THIS:**' + exact text, A/B choices. Never tell him to start a new chat. "
    "[Cloud] No Mac paths, no Akira. Secrets only from ~/.vaak/env on his Mac, never in the repo. "
    "Deletes go to a dated .trash/ folder, never rm -rf. Context is small: read only needed lines. "
    "When context gets heavy a hook asks for .claude/handoff/latest.md; write it and tell the coordinator."))
