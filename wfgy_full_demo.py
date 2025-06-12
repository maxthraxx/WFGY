"""
WFGY full demo (CPU-only; 1-click Colab & HF Space)
Shows single-prompt histogram + batch table.
"""

import numpy as np, torch, matplotlib.pyplot as plt
from tabulate import tabulate
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed
from wfgy_sdk import get_engine
from wfgy_sdk.evaluator import compare_logits   # unchanged helper

MODEL   = "sshleifer/tiny-gpt2"
SEED    = 42
BOOST   = 1.0          # default demo slider value
ENGINE  = get_engine() # singleton

set_seed(SEED)
tok = AutoTokenizer.from_pretrained(MODEL)
mdl = AutoModelForCausalLM.from_pretrained(MODEL)


def run_once(prompt: str, boost: float = 1.0):
    inp   = tok(prompt, return_tensors="pt")
    rawL  = mdl(**inp).logits[0, -1].detach().cpu().float().numpy()

    I = np.random.randn(256).astype(np.float32)
    G = np.random.randn(256).astype(np.float32)

    modL = ENGINE.run(
        logits=rawL,
        input_vec=I,
        ground_vec=G,
        boost=boost,
    )
    m = compare_logits(rawL, modL)
    return prompt + tok.decode(int(rawL.argmax())), \
           prompt + tok.decode(int(modL.argmax())), \
           m, rawL, modL


# ----- SINGLE PROMPT ------------------------------------------------------- #
prompt = "Describe quantum tunnelling in emojis."
raw, mod, metrics, rl, ml = run_once(prompt, BOOST)

print("=== Single-Prompt Demo ===")
print("Prompt           :", prompt)
print("Raw continuation :", raw.split(prompt)[-1])
print("WFGY continuation:", mod.split(prompt)[-1])
print(f"variance ↓ {int(metrics['var_drop']*100)}% | KL {metrics['kl']:.2f} | top-1 {'✔' if metrics['top1'] else '✘'}")

plt.figure(figsize=(6,4))
plt.hist(rl, bins=90, alpha=.7, label="before")
plt.hist(ml, bins=90, alpha=.7, label="after")
plt.legend(); plt.title("Logit Distribution Before vs After WFGY")
plt.savefig("single_hist.png")
print("[saved → single_hist.png]")

# ----- BATCH ---------------------------------------------------------------- #
batch = [
    "Explain black holes in one sentence.",
    "Give me a haiku about entropy.",
    "Summarise Gödel's theorem for a child.",
    "Name three uses of quantum dots.",
    "Why do leaves change colour?"
]
table = []
for p in batch:
    _, _, m, *_ = run_once(p, BOOST)
    table.append([p[:30] + "…", f"{int(m['var_drop']*100)} %", f"{m['kl']:+.2f}", "✔" if m['top1'] else "✘"])

print("\n=== Batch Metrics ===")
print(tabulate(table, headers=["Prompt", "var ↓", "KL", "top-1"]))
