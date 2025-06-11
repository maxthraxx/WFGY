# example_01_basic_run.py
# End-to-end smoke test with quantitative explanation

import pathlib, sys, json, numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import wfgy_sdk as w
from wfgy_sdk.evaluator import compare_logits, pretty_print

prompt = "Why don't AIs like to take showers?"

# ── build near-by semantic vectors ───────────────────────────────────────
rng = np.random.default_rng(0)
G = rng.normal(size=128); G /= np.linalg.norm(G)
I = G + rng.normal(scale=0.05, size=128)
logits_before = rng.normal(size=32000)

# ── run WFGY pipeline ────────────────────────────────────────────────────
eng = w.get_engine(reload=True)
logits_after = eng.run(input_vec=I, ground_vec=G, logits=logits_before)

# ── metrics & printout ───────────────────────────────────────────────────
metrics = compare_logits(logits_before, logits_after)

print("\n=== Example 01 · Basic Run ===")
print(f"Prompt : {prompt}\n")
pretty_print(metrics)
print("\n● variance ↓  means logits become less noisy")
print("● KL > 0      confirms distribution changed")
print("● top-1 shift shows whether the most probable token switched")
print("⚠ GPT-2 is tiny; larger LLMs show a bigger gap.")
print("⚠ Larger LLM → stronger variance drop and higher KL.\n")

