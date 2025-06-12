#!/usr/bin/env python
# WFGY full CLI demo  –  single prompt + batch metrics + histogram
# ---------------------------------------------------------------
import os, json, math, random
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed

from wfgy_sdk import get_engine
from wfgy_sdk.evaluator import compare_logits, pretty_print, plot_histogram

# ---------------------------------------------------------------
MODEL      = "sshleifer/tiny-gpt2"      # 124 MB checkpoint – works on free Colab CPU
tokenizer  = AutoTokenizer.from_pretrained(MODEL)
model      = AutoModelForCausalLM.from_pretrained(MODEL)
ENGINE     = get_engine()

# reproducibility
set_seed(42)
np.random.seed(42)
random.seed(42)

# ---------------------------------------------------------------
def one_pass(prompt: str):
    """Returns (raw_text, mod_text, metrics_dict, raw_logits, mod_logits)."""
    toks   = tokenizer(prompt, return_tensors="pt")
    rawL   = model(**toks).logits[0, -1].detach().cpu().numpy()

    # demo-only random semantic vectors
    G = np.random.randn(256).astype(np.float32)
    I = G + np.random.normal(scale=0.05, size=256).astype(np.float32)

    modL  = ENGINE.run(I, G, rawL)          # <-- strictly 3 positional args
    mets  = compare_logits(rawL, modL)

    raw_txt = prompt + tokenizer.decode(int(rawL.argmax()))
    mod_txt = prompt + tokenizer.decode(int(modL.argmax()))
    return raw_txt, mod_txt, mets, rawL, modL


# ---------------------------------------------------------------
if __name__ == "__main__":
    # ---------- 1. single-prompt demo ----------
    print("=== Single-Prompt Demo ===")
    prompt = "Describe quantum tunnelling in emojis."
    rtxt, mtxt, m, rl, ml = one_pass(prompt)

    print(f"Prompt           : {prompt}")
    print(f"Raw continuation : {rtxt[len(prompt):]}")
    print(f"WFGY continuation: {mtxt[len(prompt):]}")
    pretty_print(m)

    fig = plot_histogram(rl, ml)            # no `show=` arg anymore
    plt.savefig("single_hist.png")
    print("[saved → single_hist.png]\n")

    # ---------- 2. batch metrics ----------
    print("=== Batch Metrics ===")
    batch_prompts = [
        "Explain black holes in one sentence.",
        "Give me a haiku about entropy.",
        "Summarise Gödel's theorem for a child.",
        "Name three uses of quantum dots.",
        "Why do leaves change colour?"
    ]

    rows = []
    for p in batch_prompts:
        _, _, mm, _, _ = one_pass(p)
        rows.append([
            p[:30] + ("…" if len(p) > 30 else ""),
            f"{int(mm['var_drop']*100)} %",
            f"{mm['kl']:.2f}",
            "✔" if mm['top1'] else "✘"
        ])

    print(tabulate(rows,
                   headers=["Prompt", "var ↓", "KL", "top-1"],
                   tablefmt="github"))

    # reminder
    print("\nPDF mode – feed I_am_not_lizardman/WFGY_1.0.pdf "
          "to any chat-LLM and prepend 'Use WFGY:'.\n"
          "⭐ 10 000 GitHub stars before 2025-08-01 unlocks WFGY 2.0.\n")
