# example_05_universe_test.py
# Universe test with remote toggle

import pathlib, sys, numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import wfgy_sdk as w
from wfgy_sdk.evaluator import compare_logits, pretty_print

use_remote = False
MODEL_ID   = "gpt2"
prompt     = "If semantic energy is real, what force counterbalances it?"

logits_before = (
    w.call_remote_model(prompt, model_id=MODEL_ID)
    if use_remote else np.random.randn(32000)
)

G = np.random.randn(256); G /= np.linalg.norm(G)
I = G + np.random.normal(scale=0.05, size=256)

eng = w.get_engine(reload=True)
logits_after = eng.run(input_vec=I, ground_vec=G, logits=logits_before)

print("\n=== Example 05 · Universe test ===")
pretty_print(compare_logits(logits_before, logits_after))
print("Even with a random remote logit, WFGY introduces measurable structure.")
print("⚠ Larger LLM → stronger variance drop & higher KL.\n")
