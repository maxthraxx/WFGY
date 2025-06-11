# example_04_remote_inference.py
# Toggle between local random logits and Hugging Face remote model

import pathlib, sys, numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import wfgy_sdk as w
from wfgy_sdk.evaluator import compare_logits

# --- toggle here ---------------------------------------------------------
use_remote = False                       # True = call HF endpoint
MODEL_ID   = "tiiuae/falcon-7b-instruct"
prompt     = "Explain semantic gravity in one tweet."
# ------------------------------------------------------------------------

logits_before = (
    w.call_remote_model(prompt, model_id=MODEL_ID) if use_remote
    else np.random.randn(32000)
)

G = np.random.randn(128); G /= np.linalg.norm(G)
I = G + np.random.normal(scale=0.05, size=128)

eng = w.get_engine(reload=True)
logits_after = eng.run(input_vec=I, ground_vec=G, logits=logits_before)
m = compare_logits(logits_before, logits_after)

print("\n=== Example 04 · Remote toggle demo ===")
print(f"Source: {'HF API ' + MODEL_ID if use_remote else 'local random'}")
print(f"KL {m['kl_divergence']:.2f} | var↓ {(1-m['std_ratio'])*100:.0f}%")
print("⚠ Larger LLM → stronger variance drop & higher KL.\n")
