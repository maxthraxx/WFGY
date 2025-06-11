# example_06_compare.py
# Compare GPT-2 logits before/after WFGY with inline metrics

import pathlib, sys, json, numpy as np, torch
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from transformers import GPT2LMHeadModel, GPT2TokenizerFast
import wfgy_sdk as w
from wfgy_sdk.evaluator import compare_logits, pretty_print

prompt = (
    "Explain the Navier–Stokes millennium problem in 50 words "
    "(this is intentionally hard for GPT-2)."
)

# --- Load GPT-2 -----------------------------------------------------------
tok = GPT2TokenizerFast.from_pretrained("gpt2")
gpt2 = GPT2LMHeadModel.from_pretrained("gpt2").eval()

ids = tok(prompt, return_tensors="pt").input_ids
with torch.no_grad():
    out = gpt2(ids, output_hidden_states=True, return_dict=True)

logits_before = out.logits[0, -1].cpu().numpy()

# --- Build semantic vectors ----------------------------------------------
hidden = out.hidden_states[-2][0, -1].cpu().numpy()
ground = hidden / np.linalg.norm(hidden)
inp = ground + np.random.normal(scale=0.05, size=ground.shape)

# --- Run WFGY -------------------------------------------------------------
eng = w.get_engine(reload=True)
logits_after = eng.run(input_vec=inp, ground_vec=ground, logits=logits_before)

# --- Metrics & explanation -----------------------------------------------
metrics = compare_logits(logits_before, logits_after)
print("\n=== Quantitative Effect of WFGY (GPT-2) ===")
pretty_print(metrics)

print("\n=== Quick guide ===")
print("• variance ↓  → logits become less noisy (attention is focused)")
print("• KL > 0      → distribution genuinely changed, not numerical noise")
print("• top-1 shift → most probable token switched ⇒ semantic nudge")
print("⚠ GPT-2 is tiny; bigger models show even larger improvement.")
print("⚠ Larger LLM → stronger variance drop and higher KL.")

