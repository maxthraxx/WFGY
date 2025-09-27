import pathlib, sys, numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import wfgy_sdk as w
from wfgy_sdk.evaluator import compare_logits, pretty_print
from wfgy_sdk.visual    import plot_histogram  # ← histogram helper

# ---------- toggle remote / local ------------------------------------------------
use_remote = False
MODEL_ID   = "gpt2"
prompt     = "Why don't AIs like to take showers?"
# ---------------------------------------------------------------------------------

if use_remote:
    logits_before = w.call_remote_model(prompt, model_id=MODEL_ID)
else:
    rng = np.random.default_rng(0)
    logits_before = rng.normal(size=32000)

rng = np.random.default_rng(42)
G = rng.normal(size=128); G /= np.linalg.norm(G)
I = G + rng.normal(scale=0.05, size=128)

eng = w.get_engine(reload=True)
logits_after = eng.run(input_vec=I, ground_vec=G, logits=logits_before)

print("\n=== Example 01 · Basic Run ===")
print(f"Source : {'HF ' + MODEL_ID if use_remote else 'local random'}")
pretty_print(compare_logits(logits_before, logits_after))
print("⚠ Larger LLM → stronger variance drop & higher KL.\n")

# ---------- optional histogram ---------------------------------------------------
plot_histogram(logits_before, logits_after)
