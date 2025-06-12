"""
WFGY full demo  –  single prompt + batch table + histogram
Now uses boost = 1.2 and tells BBMC to scale accordingly,
so the effect is obvious on tiny GPT-2.
"""

import io, numpy as np, matplotlib.pyplot as plt
from PIL import Image
from tabulate import tabulate

import wfgy_sdk as w
from wfgy_sdk.evaluator import compare_logits
from wfgy_sdk.visual    import plot_histogram

from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed
MODEL = "sshleifer/tiny-gpt2"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model     = AutoModelForCausalLM.from_pretrained(MODEL)
set_seed(42)

ENGINE = w.get_engine()
BOOST  = 1.2                     # ← bigger gap
BBMC_SCALE = BOOST               # 1-to-1 for demo clarity


def one_pass(prompt: str):
    ids        = tokenizer(prompt, return_tensors="pt").input_ids
    raw_logits = model(ids).logits[0, -1].detach().cpu().numpy()

    G = np.random.randn(256); G /= np.linalg.norm(G)
    I = G + np.random.normal(scale=BOOST, size=256)

    mod_logits = ENGINE.run(I, G, raw_logits, bbmc_scale=BBMC_SCALE)
    m = compare_logits(raw_logits, mod_logits)

    raw_txt = prompt + tokenizer.decode(int(raw_logits.argmax()))
    mod_txt = prompt + tokenizer.decode(int(mod_logits.argmax()))
    return raw_txt, mod_txt, m, raw_logits, mod_logits


def save_hist(name, rl, ml):
    fig = plot_histogram(rl, ml) or plt.gcf()
    fig.savefig(name, bbox_inches="tight"); plt.close(fig)


# ─────────────────── Single prompt ──────────────────────
prompt = "Describe quantum tunnelling in emojis."
print("=== Single-Prompt Demo ===")
r_txt, m_txt, m, rl, ml = one_pass(prompt)

print("Prompt           :", prompt)
print("Raw continuation :", r_txt[len(prompt):])
print("WFGY continuation:", m_txt[len(prompt):])
print(f"variance ↓ {(1-m['std_ratio'])*100:.0f}% | "
      f"KL {m['kl_divergence']:.02f} | top-1 {'✔' if m['top1_shift'] else '✘'}")

save_hist("single_hist.png", rl, ml)
print("[saved → single_hist.png]\n")

# ───────────────── Batch table (5) ──────────────────────
prompts = [
    "Explain black holes in one sentence.",
    "Give me a haiku about entropy.",
    "Summarise Gödel's theorem for a child.",
    "Name three uses of quantum dots.",
    "Why do leaves change colour?"
]

rows = []
for p in prompts:
    _, _, met, *_ = one_pass(p)
    rows.append([
        p[:33] + ("…" if len(p) > 33 else ""),
        f"{(1-met['std_ratio'])*100:.0f} %",
        f"{met['kl_divergence']:.02f}",
        "✔" if met["top1_shift"] else "✘"
    ])

print("=== Batch Metrics ===")
print(tabulate(rows, headers=["Prompt", "var ↓", "KL", "top-1"]))
