# example_01_basic_run.py
# Basic end-to-end WFGY smoke test

import numpy as np
import wfgy_sdk as w

prompt = "Why don't AIs like to take showers?"

# Build semantically related I and G to keep residue small
rng = np.random.default_rng(0)
G = rng.normal(size=128)
G = G / np.linalg.norm(G)
I = G + rng.normal(scale=0.05, size=128)

logits = rng.normal(size=32000)

engine = w.get_engine(reload=True)    # fresh singleton
state = engine.run(
    input_vec=I,
    ground_vec=G,
    logits=logits,
    return_all=True                   # diagnostics
)

print("\n=== Prompt ===")
print(prompt)
print("=== Residue ‖B‖ ===", round(state["B_norm"], 4))
print("=== Collapse? ===", state["_collapse"])
print("=== First 5 logits (before → after) ===")
print(np.vstack([logits[:5], state["logits_mod"][:5]]).T)
