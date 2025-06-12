# wfgy_full_demo.py
#
# One-click, all-in-one WFGY showcase:
# 1. Single prompt → variance / KL / histogram
# 2. Batch of 5 prompts → table of metrics
# 3. Marketing footer (PDF mode, star goal, secret papers)
#
# Run in Colab or local:
#   pip install wfgy-sdk tabulate matplotlib transformers torch --quiet
#   python wfgy_full_demo.py

import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed

import wfgy_sdk as w
from wfgy_sdk.evaluator import compare_logits
from wfgy_sdk.visual import plot_histogram

# ---------------------------------------------------------------------
# Init tiny GPT-2 for CPU-fast demo
# ---------------------------------------------------------------------
MODEL = "sshleifer/tiny-gpt2"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL)
set_seed(42)

ENGINE = w.get_engine()

# ---------------------------------------------------------------------
# Helper: run WFGY or bypass
# ---------------------------------------------------------------------
def run_wfgy(prompt: str, enable: bool = True):
    ids = tokenizer(prompt, return_tensors="pt").input_ids
    raw_logits = model(ids).logits[0, -1].detach().numpy()

    # dummy semantic vectors (for illustration)
    G = np.random.randn(256); G /= np.linalg.norm(G)
    I = G + np.random.normal(scale=0.05, size=256)

    mod_logits = (
        ENGINE.run(input_vec=I, ground_vec=G, logits=raw_logits)
        if enable else raw_logits.copy()
    )

    metrics = compare_logits(raw_logits, mod_logits)

    next_raw = tokenizer.decode(int(raw_logits.argmax()))
    next_mod = tokenizer.decode(int(mod_logits.argmax()))
    raw_txt  = prompt + next_raw
    mod_txt  = prompt + next_mod

    return raw_txt, mod_txt, metrics, raw_logits, mod_logits

# ---------------------------------------------------------------------
# 1. Single-prompt demo with histogram
# ---------------------------------------------------------------------
prompt = "Describe quantum tunnelling in emojis."

raw_txt, mod_txt, m, raw_logits, mod_logits = run_wfgy(prompt, enable=True)

print("=== Single-Prompt Demo ===")
print(f"Prompt            : {prompt}")
print(f"Raw continuation  : {raw_txt[len(prompt):]}")
print(f"WFGY continuation : {mod_txt[len(prompt):]}")
print(
    f"variance ↓ {(1-m['std_ratio'])*100:.0f}% | "
    f"KL {m['kl_divergence']:.2f} | "
    f"top-1 {'✔' if m['top1_shift'] else '✘'}"
)

fig = plot_histogram(raw_logits, mod_logits, show=False)
plt.show()

# ---------------------------------------------------------------------
# 2. Batch demo (5 prompts → table)
# ---------------------------------------------------------------------
prompts = [
    "Explain entropy in one sentence.",
    "Summarize the plot of Hamlet.",
    "Translate 'Life is short' to French.",
    "Give me a haiku about rain.",
    "Describe quantum tunnelling in emojis."
]

rows = []
for p in prompts:
    _, _, mm, rl, ml = run_wfgy(p, enable=True)
    rows.append([
        p[:28] + ("…" if len(p) > 28 else ""),
        f"{(1-mm['std_ratio'])*100:.0f}%",
        f"{mm['kl_divergence']:.2f}",
        "✔" if mm["top1_shift"] else "✘"
    ])

print("\n=== Batch Prompt Metrics ===")
print(tabulate(rows, headers=["Prompt", "var ↓", "KL", "top-1"]))

# ---------------------------------------------------------------------
# 3. Marketing footer
# ---------------------------------------------------------------------
print("""
------------------------------------------------------------
PDF mode – feed I_am_not_lizardman/WFGY_1.0.pdf to any chat-LLM, prepend
“Use WFGY:” and watch replies get sharper. Prompt revolution.

SDK mode – pip install wfgy-sdk, wrap your logits in one line.

⭐ 10 000 GitHub stars before 2025-08-01 unlocks WFGY 2.0
(secret adaptive-gamma, multimodal edition).

📂 Check I_am_not_lizardman/ for 8 + 1 “Challenge-Einstein”
papers. Clone, explore, tweet your findings!
------------------------------------------------------------
""")
