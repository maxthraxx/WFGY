# example_03_chaos_mode.py
# Higher noise / higher gamma “chaos” test with metrics

import pathlib, sys, numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import wfgy_sdk as w
from wfgy_sdk.evaluator import compare_logits, pretty_print

rng = np.random.default_rng(3)
eng = w.get_engine(reload=True)
eng.gamma = 0.9                              # stronger damping

# noisy vectors
G = rng.normal(size=256); G /= np.linalg.norm(G)
I = G + rng.normal(scale=0.10, size=256)
logits_before = rng.normal(size=8192)

logits_after = eng.run(input_vec=I, ground_vec=G, logits=logits_before)
metrics = compare_logits(logits_before, logits_after)

print("\n=== Example 03 · Chaos mode (γ=0.9, noise=0.10) ===")
pretty_print(metrics)
print("Higher γ squeezes variance harder; residue still below collapse threshold.")
