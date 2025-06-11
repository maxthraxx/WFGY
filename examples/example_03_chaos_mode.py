# example_03_chaos_mode.py
# Chaos test with gamma=0.9, remote toggle

import pathlib, sys, numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import wfgy_sdk as w
from wfgy_sdk.evaluator import compare_logits, pretty_print

use_remote = False
MODEL_ID   = "gpt2"

rng = np.random.default_rng(3)
eng = w.get_engine(reload=True)
eng.gamma = 0.9

G = rng.normal(size=256); G /= np.linalg.norm(G)
I = G + rng.normal(scale=0.10, size=256)

logits_before = (
    w.call_remote_model("Chaos prompt", model_id=MODEL_ID)
    if use_remote else rng.normal(size=8192)
)

logits_after = eng.run(input_vec=I, ground_vec=G, logits=logits_before)
print("\n=== Example 03 · Chaos mode ===")
pretty_print(compare_logits(logits_before, logits_after))
print("⚠ Larger LLM → stronger variance drop & higher KL.\n")
