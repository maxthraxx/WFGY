# example_06_compare.py
# Compare GPT-2 answers with / without WFGY

import pathlib, sys, json, numpy as np, torch
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from transformers import GPT2LMHeadModel, GPT2TokenizerFast
import wfgy_sdk as w
from scipy.stats import entropy

prompt = "Explain the Navier–Stokes millennium problem in 50 words."

# --- load GPT-2 -----------------------------------------------------------
tok = GPT2TokenizerFast.from_pretrained("gpt2")
gpt2 = GPT2LMHeadModel.from_pretrained("gpt2").eval()

ids = tok(prompt, return_tensors="pt").input_ids
with torch.no_grad():
    out = gpt2(ids, output_hidden_states=True, return_dict=True)

logits0 = out.logits[0, -1].cpu().numpy()

# --- build semantic vectors from hidden state ----------------------------
G = out.hidden_states[-2][0, -1].cpu().numpy()
G /= np.linalg.norm(G)
I = G + np.random.normal(scale=0.05, size=G.shape)

# --- run WFGY ------------------------------------------------------------
eng = w.get_engine(reload=True)
logits1 = eng.run(input_vec=I, ground_vec=G, logits=logits0)

# --- metrics -------------------------------------------------------------
sigma0, sigma1 = np.std(logits0), np.std(logits1)
kl = entropy(
    np.exp(logits1) / np.sum(np.exp(logits1)),
    np.exp(logits0) / np.sum(np.exp(logits0))
)

print(json.dumps({
    "std_before": float(sigma0),
    "std_after":  float(sigma1),
    "std_ratio":  float(sigma1 / sigma0),
    "kl_divergence": float(kl)
}, indent=2))

# --- greedy token comparison ---------------------------------------------
tok0 = tok.decode(int(np.argmax(logits0)))
tok1 = tok.decode(int(np.argmax(logits1)))
print("Top-1 token before → after :", tok0, "→", tok1)
