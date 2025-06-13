"""
WFGY · Metrics & Visuals
Pure-NumPy / Matplotlib helpers
"""

import io, math, numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

# ───────────────────────────────────────────────────────────
# 核心評量
# ───────────────────────────────────────────────────────────

def compare_logits(old: np.ndarray, new: np.ndarray) -> dict:
    """Return variance-drop, KL, and top-1 preservation."""
    var_drop = 1.0 - new.std() / (old.std() + 1e-9)
    p, q = softmax(old), softmax(new)
    kl = np.sum(p * np.log((p + 1e-8) / (q + 1e-8)))
    top1_same = int(old.argmax() == new.argmax())
    return {"var_drop": var_drop, "kl": kl, "top1": top1_same}

def pretty_print(m: dict) -> str:
    tbl = tabulate([[f"{m['var_drop']*100:4.1f} %", f"{m['kl']:.3f}", "✔" if m['top1'] else "✘"]],
                   headers=["▼ Var", "KL", "Top-1"], tablefmt="github")
    return tbl

def softmax(x: np.ndarray) -> np.ndarray:
    z = x - x.max()
    e = np.exp(z)
    return e / e.sum()

# ───────────────────────────────────────────────────────────
# 
# ───────────────────────────────────────────────────────────

def plot_histogram(old: np.ndarray, new: np.ndarray, bins: int = 50) -> plt.Figure:
    """Return a Matplotlib Figure comparing old vs. new logits."""
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=110)
    ax.hist(old, bins=bins, alpha=0.6, label="Raw", log=True)
    ax.hist(new, bins=bins, alpha=0.6, label="WFGY", log=True)
    ax.set_title("Logit Distribution (log-scale)")
    ax.set_xlabel("logit value"); ax.set_ylabel("frequency")
    ax.legend()
    fig.tight_layout()
    return fig
