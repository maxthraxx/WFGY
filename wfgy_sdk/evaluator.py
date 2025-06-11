# evaluator.py
# Utility metrics for WFGY before/after comparison
# License: MIT

from __future__ import annotations
from typing import Dict
import numpy as np
from scipy.stats import entropy


def _softmax(logits: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    """Numerically stable softmax with small epsilon to avoid zero probs."""
    logits = logits - np.max(logits)
    exp = np.exp(logits)
    probs = exp / np.sum(exp)
    return np.clip(probs, eps, 1.0)  # avoid exact 0


def compare_logits(
    logits_before: np.ndarray,
    logits_after: np.ndarray
) -> Dict[str, float]:
    """
    Return key metrics showing how WFGY changed the distribution.

    Metrics
    -------
    std_before, std_after : float
        Standard deviation of logits.
    std_ratio : float
        std_after / std_before  (<1 means variance suppressed).
    kl_divergence : float
        KL( after || before ) on probability space.
    top1_shift : int
        1 if top-1 token changed, else 0.
    """
    std_b = float(np.std(logits_before))
    std_a = float(np.std(logits_after))
    ratio = std_a / std_b if std_b else 0.0

    p_after = _softmax(logits_after)
    p_before = _softmax(logits_before)
    kl = float(entropy(p_after, p_before))        # finite by construction

    top1_changed = int(int(np.argmax(logits_before)) != int(np.argmax(logits_after)))

    return {
        "std_before": std_b,
        "std_after": std_a,
        "std_ratio": ratio,
        "kl_divergence": kl,
        "top1_shift": top1_changed,
    }
