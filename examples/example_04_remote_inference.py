# example_04_remote_inference.py
# Simulated “remote” LLM with metrics on each stage

import pathlib, sys, numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import wfgy_sdk as w
from wfgy_sdk.evaluator import compare_logits

def mock_remote_logits(prompt: str) -> np.ndarray:
    """Pretend we called an API, return random logits."""
    return np.random.randn(32000)

prompts = [
    "Please answer a question you are least confident about.",
    "Now WFGY is activated. Describe the change in your reasoning.",
    "Explain the concept of 'semantic gravity' with WFGY enabled.",
]

eng = w.get_engine(reload=True)

print("\n=== Example 04 · Remote LLM demo ===")
for idx, p in enumerate(prompts, 1):
    raw = mock_remote_logits(p)

    G = np.random.randn(128); G /= np.linalg.norm(G)
    I = G + np.random.normal(scale=0.05, size=128)

    mod = eng.run(input_vec=I, ground_vec=G, logits=raw)
    m = compare_logits(raw, mod)

    print(f"[Stage {idx}] KL {m['kl_divergence']:.2f} | "
          f"variance ratio {m['std_ratio']:.2f} | "
          f"top-1 {'✔' if m['top1_shift'] else '✘'}")
