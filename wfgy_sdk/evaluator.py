"""
WFGY · Metrics & Visuals
Pure-NumPy + Matplotlib helpers
"""

import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate


# ──────────────────────────────
# internal helpers
# ──────────────────────────────
def _safe_std(x: np.ndarray) -> float:
    s = float(np.std(x))
    return s if s > 0 else 1e-12


def softmax(x: np.ndarray) -> np.ndarray:
    z = x - x.max()
    e = np.exp(z)
    return e / e.sum()


# ──────────────────────────────
# main public function
# ──────────────────────────────
def compare_logits(old: np.ndarray, new: np.ndarray) -> dict:
    sr = _safe_std(new) / _safe_std(old)          # std ratio (≤ 0.7 passes)
    var_drop = 1.0 - sr
    p, q = softmax(old), softmax(new)
    kl_val = float(np.sum(p * np.log((p + 1e-8) / (q + 1e-8))))
    top1_same = int(old.argmax() == new.argmax())

    return {
        "std_ratio"     : sr,
        "var_drop"      : var_drop,
        "kl_divergence" : kl_val,   # name used by CI test
        "kl"            : kl_val,   # alias for Space UI
        "top1"          : top1_same,
    }


# ──────────────────────────────
# CLI pretty-print
# ──────────────────────────────
def pretty_print(m: dict) -> str:
    tbl = tabulate(
        [[f"{m['std_ratio']:.3f}",
          f"{m['var_drop']*100:4.1f} %",
          f"{m['kl_divergence']:.3f}",
          "✔" if m['top1'] else "✘"]],
        headers=["std_ratio", "▼ var", "KL", "Top-1"],
        tablefmt="github",
    )
    return tbl


# ──────────────────────────────
# histogram
# ──────────────────────────────
def plot_histogram(old: np.ndarray, new: np.ndarray, bins: int = 50) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=110)
    ax.hist(old, bins=bins, alpha=0.6, label="Raw", log=True)
    ax.hist(new, bins=bins, alpha=0.6, label="WFGY", log=True)
    ax.set_title("Logit Distribution (log-scale)")
    ax.set_xlabel("logit value")
    ax.set_ylabel("frequency")
    ax.legend()
    fig.tight_layout()
    return fig
