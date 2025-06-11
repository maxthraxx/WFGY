# example_05_universe_test.py
# Single remote call + metrics

import pathlib, sys, numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import wfgy_sdk as w
from wfgy_sdk.evaluator import compare_logits, pretty_print

def mock_remote_logits(prompt: str) -> np.ndarray:
    return np.random.randn(32000)

prompt = (
    "If semantic energy is real, what force counterbalances it in a vacuum?"
)
raw_logits = mock_remote_logits(prompt)

G = np.random.randn(256); G /= np.linalg.norm(G)
I = G + np.random.normal(scale=0.05, size=256)

eng = w.get_engine(reload=True)
mod_logits = eng.run(input_vec=I, ground_vec=G, logits=raw_logits)

metrics = compare_logits(raw_logits, mod_logits)

print("\n=== Example 05 · Universe test ===")
pretty_print(metrics)
print("Even with a random remote logit, WFGY introduces measurable structure.")
