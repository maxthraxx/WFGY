# example_05_universe_test.py
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np, wfgy_sdk as w

def remote_logits(prompt: str) -> np.ndarray:
    return np.random.randn(32000)

prompt = "If semantic energy is real, what force counterbalances it in a vacuum?"
raw = remote_logits(prompt)

G = np.random.randn(256); G /= np.linalg.norm(G)
I = G + np.random.normal(scale=0.05, size=256)

eng = w.get_engine(reload=True)
mod = eng.run(input_vec=I, ground_vec=G, logits=raw)
print("Enhanced first-token logit:", mod[0])
