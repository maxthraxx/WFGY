#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ================================================================
#  WFGY Core Engine  •  Lightweight → CPU-friendly
# ================================================================

from __future__ import annotations      # ★ 一定要放檔案最前面（除 shebang / encoding）

import numpy as np


class WFGYEngine:
    """
    Self-Healing Variance Gate:
    I  = input semantic vector   (np.float32, shape (256,))
    G  = ground semantic vector  (same)
    L  = logits  (np.float32, shape (vocab,))
    Returns new logits (same shape / dtype)
    """
    def __init__(self, bbmc_scale: float = 0.5):
        self.bbmc_scale = bbmc_scale

    # -------- public API --------
    def run(self,
            input_vec:  np.ndarray,
            ground_vec: np.ndarray,
            logits:     np.ndarray) -> np.ndarray:
        """Apply BBMC → BBPF → BBCR → BBAM in a single pass."""
        z = self._bbmc(logits, input_vec, ground_vec)
        z = self._bbpf(z)
        z = self._bbcr(z)
        z = self._bbam(z)
        return z

    # -------- internal modules (toy demo) --------
    def _bbmc(self, L, I, G):
        # BigBig Semantic Residue Formula (variance gate)
        alpha = self.bbmc_scale
        return L - alpha * (I @ G) * 0.001

    def _bbpf(self, L):
        # BigBig Progression Formula (dummy: tanh)
        return np.tanh(L)

    def _bbcr(self, L):
        # BigBig Collapse–Rebirth (dummy: shift by mean)
        return L - L.mean()

    def _bbam(self, L):
        # BigBig Attention Modulation (dummy: scale to unit variance)
        return L / (L.std() + 1e-5)


# global singleton (matches get_engine() helper)
_ENGINE: WFGYEngine | None = None


def get_engine() -> WFGYEngine:
    """External helper so demos can do `from wfgy_sdk import get_engine`."""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = WFGYEngine()
    return _ENGINE
