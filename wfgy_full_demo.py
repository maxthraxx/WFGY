#!/usr/bin/env python
# ===============================================================
#  WFGY full CLI demo – single prompt + batch table + histogram
#  Pure CPU → Colab Free & HF Space 均能跑
# ===============================================================

import random, os, json, math
from typing import Tuple, List

import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed

from wfgy_sdk import get_engine
from wfgy_sdk.evaluator import compare_logits, pretty_print, plot_histogram

# --------------------------------------------------------------
MODEL     = "sshleifer/tiny-gpt2"          # 124 MB checkpoint
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model     = AutoModelForCausalLM.from_pretrained(MODEL)
ENGINE    = get_engine()

# reproducibility
set_seed(42)
np.random.seed(42)
random.seed(42)

# --------------------------------------------------------------
def one_pass(prompt: str) -> Tuple[str, str, dict, np.ndarray, np.ndarray]:
    """Run one prompt through raw GPT-2 + WFGY."""
    toks  = tokenizer(prompt, return_tensors="pt")
    rawL  = model(**toks).logits[0, -1].detach().cpu().numpy()

    # demo-only random semantic vectors
    G = np.random.randn(256).astype(np.float32)
    I = G + np.random.normal(scale=0.05, size=256).astype(np.float32)

    modL  = ENGINE.run(I, G, rawL)              # 3-arg API
    mets  = compare_logits(rawL, modL)

    return (
        prompt + tokenizer.decode(int(rawL.argmax())),
        prompt + tokenizer.decode(int(modL.argmax())),
        mets,
        rawL,
        modL,
    )


# --------------------------------------------------------------
if __name__ == "__main__":
    # -------- 1 · single-prompt demo --------
    print("=== Single-Prompt Demo ===")
    prompt = "Describe quantum tunnelling in emojis."
    rtxt, mtxt, m, rl, ml = one_pass(prompt)

    print(f"Prompt            : {prompt}")
    print(f"Raw continuation  : {rtxt[len(prompt):]}")
    print(f"WFGY continuation : {mtxt[len(prompt):]}")
    pretty_print(m)

    fig = plot_histogram(rl, ml)          # show=False internally
    plt.savefig("single_hist.png")
    print("[saved → single_hist.png]\n")

    # -------- 2 · batch table --------
    print("=== Batch Metrics ===")
    prompts = [
        "Explain black holes in one sentence.",
        "Give me a haiku about entropy.",
        "Summarise Gödel's theorem for a child.",
        "Name three uses of quantum dots.",
        "Why do leaves change colour?"
    ]

    table: List[List[str]] = []
    for p in prompts:
        _, _, mm, *_ = one_pass(p)
        table.append([
            p[:30] + ("…" if len(p) > 30 else ""),
            f"{int(mm['var_drop']*100)} %",
            f"{mm['kl']:.2f}",
            "✔" if mm['top1'] else "✘",
        ])

    print(tabulate(table, headers=["Prompt", "var ↓", "KL", "top-1"],
                   tablefmt="github"))

    # -------- footer --------
    print("\nPDF mode → feed I_am_not_lizardman/WFGY_1.0.pdf "
          "to any chat-LLM and prepend 'Use WFGY:'.")
    print("⭐ 10 000 GitHub stars before 2025-08-01 unlock WFGY 2.0.\n")
