# wfgy_sdk/wfgy_engine.py
# ==============================================================
#  Core orchestrator – stateless, pure-NumPy implementation
# ==============================================================

from __future__ import annotations

import numpy as np
from typing import Optional, Union, Dict, Any


class WFGYEngine:
    """
    Stateless logit modulator.
    Call :meth:`run` with (input_vec, ground_vec, logits) → new_logits.
    """

    def __init__(
        self,
        *,
        cfg: Optional[Dict[str, Any]] = None,
        debug: bool = False,     # <-- keep for backward-compat, no effect
        **_: Any                 # swallow any other legacy kwargs
    ) -> None:
        self.cfg   = cfg or {}
        self.debug = debug

    # ----------------------------------------------------------
    def run(
        self,
        input_vec:  np.ndarray,
        ground_vec: np.ndarray,
        logits:     np.ndarray,
    ) -> np.ndarray:
        """Minimal demo version: cosine gate + soft rescale."""
        # normalise
        iv = input_vec.astype(np.float32)
        gv = ground_vec.astype(np.float32)
        iv /= (np.linalg.norm(iv) + 1e-8)
        gv /= (np.linalg.norm(gv) + 1e-8)

        cos = iv @ gv                    # [-1, 1]
        gamma = 1.0 - cos * 0.3          # shrink when vectors align

        out = logits.astype(np.float32) * gamma
        return out

# --------------------------------------------------------------
# helper exported for sdk users
_engine: Optional[WFGYEngine] = None

def get_engine(*, reload: bool = False, **kwargs) -> WFGYEngine:
    """
    Return a singleton engine.
    `reload=True`  → rebuild (useful in tests).
    Extra kwargs are forwarded but ignored by default.
    """
    global _engine
    if reload or _engine is None:
        _engine = WFGYEngine(**kwargs)
    return _engine
