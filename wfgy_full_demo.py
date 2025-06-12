#!/usr/bin/env python
# WFGY full CLI demo – single prompt + batch metrics + histogram
# --------------------------------------------------------------

from __future__ import annotations

import json, math, os, random
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed

from wfgy_sdk import get_engine
from wfgy_sdk.evaluator import compare_logits, pretty_print, plot_histogram

# --------------------------------------------------------------
MODEL = "sshleifer/tiny-gpt2"          # 124 MB – 任何免費 Colab CPU 都跑得動
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model     = AutoModelForCausalLM.from_pretrained(MODEL)
ENGINE    = get_engine()               # singleton

set_seed(42)
np.random.seed(42)
random.seed(42)

# --------------------------------------------------------------
def one_pass(prompt: str):
    """Return raw_text, mod_text, metrics, raw_logits, mod_logits."""
    toks  = tokenizer(prompt, return_tensors="pt")
    rawL  = model(**toks).logits[0, -1].detach().cpu().numpy()

    # demo-only 隨機語義向量
    G = np.random.randn(256).astype(np.float32)
    I = G + np.random.normal(scale=0.05, size=256).astype(np.float32)

    modL = ENGINE.run(I, G, rawL)

    metrics = compare_logits(rawL, modL)
    raw_txt = prompt + tokenizer.decode(int(rawL.argmax()))
    mod_txt = prompt + tokenizer.decode(int(modL.argmax()))
    return raw_txt, mod_txt, metrics, rawL, modL

# --------------------------------------------------------------
if __name__ == "__main__":
    # ---------- 1 · 單句示範 ----------
    print("=== Single-Prompt Demo ===")
    prompt = "Describe quantum tunnelling in emojis."
    rtxt, mtxt, m, rl, ml = one_pass(prompt)

    print(f"Prompt            : {prompt}")
    print(f"Raw continuation  : {rtxt[len(prompt):]}")
    print(f"WFGY continuation : {mtxt[len(prompt):]}")
    pretty_print(m)

    fig = plot_histogram(rl, ml)
    plt.savefig("single_hist.png")
    print("[saved → single_hist.png]\n")

    # ---------- 2 · 批次指標 ----------
    print("=== Batch Metrics ===")
    prompts = [
        "Explain black holes in one sentence.",
        "Give me a haiku about entropy.",
        "Summarise Gödel's theorem for a child.",
        "Name three uses of quantum dots.",
        "Why do leaves change colour?",
    ]

    table = []
    for p in prompts:
        _, _, mm, *_ = one_pass(p)
        table.append([
            p[:30] + ("…" if len(p) > 30 else ""),
            f"{int(mm['var_drop']*100)} %",
            f"{mm['kl']:.2f}",
            "✔" if mm['top1'] else "✘",
        ])

    print(tabulate(table, headers=["Prompt", "var ↓", "KL", "top-1"], tablefmt="github"))

    print(
        "\nPDF mode → feed I_am_not_lizardman/WFGY_1.0.pdf to any chat-LLM "
        "and prepend 'Use WFGY:'.\n"
        "⭐ 10 000 GitHub stars before 2025-08-01 unlock WFGY 2.0.\n"
    )
