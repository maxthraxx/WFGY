# examples/example_02_self_reflection.py
# Three successive runs on a single engine

import numpy as np, wfgy_sdk as w
rng = np.random.default_rng(1)
eng = w.get_engine(reload=True)

for step in range(3):
    G = rng.normal(size=64)
    G /= np.linalg.norm(G)
    I = G + rng.normal(scale=0.05, size=64)
    logits = rng.normal(size=4096)

    out = eng.run(input_vec=I, ground_vec=G, logits=logits)
    print(f"[Round {step}] logit[0] after WFGY = {out[0]:.4f}")
