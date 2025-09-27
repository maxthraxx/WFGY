# example_02_self_reflection.py
# Self-reflection loop with remote toggle

import pathlib, sys, numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import wfgy_sdk as w
from wfgy_sdk.evaluator import compare_logits

use_remote = False
MODEL_ID   = "gpt2"

rng = np.random.default_rng(1)
eng = w.get_engine(reload=True)

print("\n=== Example 02 · Self-reflection loop ===")
for step in range(3):
    G = rng.normal(size=64); G /= np.linalg.norm(G)
    I = G + rng.normal(scale=0.05, size=64)

    logits_before = (
        w.call_remote_model(f"Round {step}", model_id=MODEL_ID)
        if use_remote else rng.normal(size=4096)
    )

    logits_after = eng.run(input_vec=I, ground_vec=G, logits=logits_before)
    m = compare_logits(logits_before, logits_after)
    print(f"[Round {step}] KL {m['kl_divergence']:.2f} | "
          f"var↓ {(1-m['std_ratio'])*100:.0f}% | "
          f"top-1 {'✔' if not m["top1_shift"] else '✘'}")

print("⚠ Larger LLM → stronger variance drop & higher KL.\n")
