# evaluator.py
# Metrics for before/after WFGY logit comparison
# License: MIT

from __future__ import annotations
from typing import Dict
import numpy as np
from scipy.stats import entropy


def _softmax(logits: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    """
    Stable softmax with epsilon floor to avoid exact zeros (which would cause
    KL divergence to blow up).
    """
    logits = logits - np.max(logits)
    exp = np.exp(logits)
    probs = exp / np.sum(exp)
    return np.clip(probs, eps, 1.0)


def compare_logits(
    logits_before: np.ndarray,
    logits_after: np.ndarray,
) -> Dict[str, f]()
