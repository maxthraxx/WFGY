"""
WFGY full demo – single prompt + small batch metrics + histogram.
Works on free Colab CPU.  No NumPy-2, no 'show' kwarg.
"""

import io, random, numpy as np, matplotlib.pyplot as plt
from PIL import Image
from tabulate import tabulate

import wfgy_sdk as w
from wfgy_sdk.evaluator import compare_logits
from wfgy_sdk.visual    import plot_histogram

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed

# ───────────────────────── config ──────────────────────────
MODEL = "sshleifer/tiny-gpt2"     # 124 MB
set_seed(42)

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model     = AutoModelForCausalLM.from_pretrained(MODEL)

engine = w.get_engine()

# ───────────────────── helper functions ────────────────────
def run_wfgy(prompt: str, boost: float = .30):
    """Return raw txt, mod txt, metrics dict, raw & mod logits."""
    ids        = tokenizer(prompt, return_tensors="pt").input_ids
    raw_logits = model(ids).logits[0, -1].detach().cpu().numpy()

    # synthetic semantic vectors (demo only)
    G = np.random.randn(256); G /= np.linalg.norm(G)
    I = G + np.random.normal(scale=boost, size=256)

    mod_logits = engine.run(input_vec=I, ground_vec=G, logits=raw_logits)
    metrics    = compare_logits(raw_logits, mod_logits)

    raw_txt = prompt + tokenizer.decode(int(raw_logits.argmax()))
    mod_txt = prompt + tokenizer.decode(int(mod_logits.argmax()))
    return raw_txt, mod_txt, metrics, raw_logits, mod_logits


def save_hist(fig_name: str, raw_l, mod_l):
    """Draw histogram and save → PNG for later embedding."""
    fig = plot_histogram(raw_l, mod_l) or plt.gcf()
    fig.savefig(fig_name, bbox_inches="tight")
    plt.close(fig)


# ─────────────────────── single prompt ─────────────────────
prompt = "Describe quantum tunnelling in emojis."
print("=== Single-Prompt Demo ===")
r_txt, m_txt, m, r_logits, m_logits = run_wfgy(prompt)

print("Prompt           :", prompt)
print("Raw continuation :", r_txt[len(prompt):])
print("WFGY continuation:", m_txt[len(prompt):])
print(f"variance ↓ {(1-m['std_ratio'])*100:.0f}% | "
      f"KL {m['kl_divergence']:.02f} | top-1 {'✔' if m['top1_shift'] else '✘'}")

save_hist("single_hist.png", r_logits, m_logits)
print("[saved → single_hist.png]\n")

# ───────────────────── batch of 5 prompts ──────────────────
prompts = [
    "Explain black holes in one sentence.",
    "Give me a haiku about entropy.",
    "Summarise Gödel's theorem for a child.",
    "Name three uses of quantum dots.",
    "Why do leaves change colour?"
]

rows = []
for p in prompts:
    _, _, met, *_ = run_wfgy(p)
    rows.append([
        p[:35] + ("…" if len(p) > 35 else ""),
        f"{(1-met['std_ratio'])*100:.0f} %",
        f"{met['kl_divergence']:.02f}",
        "✔" if met["top1_shift"] else "✘"
    ])

print("=== Batch Metrics ===")
print(tabulate(rows, headers=["Prompt", "var ↓", "KL", "top-1"]))
