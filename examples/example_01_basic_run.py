# examples/example_01_basic_run.py
# End-to-end smoke test

import numpy as np
import wfgy_sdk as w

prompt = "Why don't AIs like to take showers?"

rng = np.random.default_rng(0)
G = rng.normal(size=128)
G /= np.linalg.norm(G)                              # unit vector
I = G + rng.normal(scale=0.05, size=128)            # small perturbation

logits = rng.normal(size=32000)

eng = w.get_engine(reload=True)
state = eng.run(input_vec=I, ground_vec=G, logits=logits, return_all=True)

print("Prompt:", prompt)
print("Residue ‖B‖ =", round(state["B_norm"], 4))
print("Collapse?  ", state["_collapse"])
print("First-token before/after →",
      logits[0], "→", state["logits_mod"][0])
