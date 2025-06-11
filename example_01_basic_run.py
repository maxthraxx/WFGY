# example_01_basic_run.py
# Basic WFGY smoke test (local, deterministic)
# Run: python examples/example_01_basic_run.py

import numpy as np
import wfgy_sdk as w

prompt = "Why don't AIs like to take showers?"
# Mock semantic vectors (demo purpose only)
I = np.random.randn(64)
G = np.random.randn(64)
logits = np.random.randn(32000)

engine = w.get_engine(reload=True)          # singleton; debug ON by default
state = engine.run(
    input_vec=I,
    ground_vec=G,
    logits=logits,
    return_all=True
)

print("\n=== Prompt ===")
print(prompt)
print("=== Modulated logits (slice) ===")
print(state["logits_mod"][:10])
print(f"=== Residue ‖B‖ = {state['B_norm']:.4f} | f_S = {state['f_S']:.4f} | collapse = {state['_collapse']}")
