# example_04_remote_inference.py
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np, wfgy_sdk as w

def call_model(prompt: str) -> np.ndarray:
    return np.random.randn(32000)

prompts = [
    "Please answer a question you are least confident about.",
    "Now WFGY is activated. Describe the change in your reasoning.",
    "Explain the concept of 'semantic gravity' with WFGY enabled."
]

eng = w.get_engine(reload=True)

for i, p in enumerate(prompts, 1):
    raw = call_model(p)
    G = np.random.randn(128); G /= np.linalg.norm(G)
    I = G + np.random.normal(scale=0.05, size=128)
    out = eng.run(input_vec=I, ground_vec=G, logits=raw)
    print(f"[Stage {i}] first logit → {out[0]:.4f}")
