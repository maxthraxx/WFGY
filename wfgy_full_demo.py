"""
WFGY full demo · Colab-safe version
 – auto-detects whether ENGINE.run accepts `bbmc_scale`
 – prints single-prompt metrics + histogram + 5-prompt table
"""

import io, inspect, numpy as np, matplotlib.pyplot as plt
from PIL import Image
from tabulate import tabulate
from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed

import wfgy_sdk as w
from wfgy_sdk.evaluator import compare_logits
from wfgy_sdk.visual    import plot_histogram

# ───── model (tiny GPT-2) ─────
MODEL = "sshleifer/tiny-gpt2"
tok   = AutoTokenizer.from_pretrained(MODEL)
mdl   = AutoModelForCausalLM.from_pretrained(MODEL)
set_seed(42)

ENGINE       = w.get_engine()
BOOST        = 1.2             # semantic deviation for demo
RUN_HAS_ARG  = "bbmc_scale" in inspect.signature(ENGINE.run).parameters

# ───── helpers ─────
def run_once(prompt: str):
    ids  = tok(prompt, return_tensors="pt").input_ids
    rawL = mdl(ids).logits[0, -1].detach().cpu().numpy()

    G = np.random.randn(256); G /= np.linalg.norm(G)
    I = G + np.random.normal(scale=BOOST, size=256)

    if RUN_HAS_ARG:
        modL = ENGINE.run(I, G, rawL, bbmc_scale=BOOST)
    else:
        modL = ENGINE.run(I, G, rawL)

    metrics = compare_logits(rawL, modL)
    raw_txt = prompt + tok.decode(int(rawL.argmax()))
    mod_txt = prompt + tok.decode(int(modL.argmax()))
    return raw_txt, mod_txt, metrics, rawL, modL


def save_hist(path, before, after):
    fig = plot_histogram(before, after) or plt.gcf()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


# ───── single prompt demo ─────
prompt = "Describe quantum tunnelling in emojis."
print("=== Single-Prompt Demo ===")
rtxt, mtxt, m, rl, ml = run_once(prompt)

print("Prompt           :", prompt)
print("Raw continuation :", rtxt[len(prompt):])
print("WFGY continuation:", mtxt[len(prompt):])
print(f"variance ↓ {(1-m['std_ratio'])*100:.0f}% | "
      f"KL {m['kl_divergence']:.02f} | "
      f"top-1 {'✔' if m['top1_shift'] else '✘'}")

save_hist("single_hist.png", rl, ml)
print("[saved → single_hist.png]\n")

# ───── batch table ─────
prompts = [
    "Explain black holes in one sentence.",
    "Give me a haiku about entropy.",
    "Summarise Gödel's theorem for a child.",
    "Name three uses of quantum dots.",
    "Why do leaves change colour?"
]
rows = []
for p in prompts:
    _, _, mt, *_ = run_once(p)
    rows.append([
        p[:33] + ("…" if len(p) > 33 else ""),
        f"{(1-mt['std_ratio'])*100:.0f} %",
        f"{mt['kl_divergence']:.02f}",
        "✔" if mt["top1_shift"] else "✘"
    ])

print("=== Batch Metrics ===")
print(tabulate(rows, headers=["Prompt", "var ↓", "KL", "top-1"]))
