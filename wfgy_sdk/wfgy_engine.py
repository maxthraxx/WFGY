# --------------------------------------------------------------
#  Core orchestrator – pure-NumPy reference implementation
# --------------------------------------------------------------
from __future__ import annotations   # 必須放最前面

from typing import Any, Dict, Optional
import numpy as np


class WFGYEngine:
    """
    Stateless logit modulator.
    Call   run(input_vec, ground_vec, logits)   → new logits.
    """

    def __init__(self, *, cfg: Dict[str, Any] | None = None,
                 debug: bool = False, **_: Any) -> None:
        self.cfg   = cfg or {}
        self.debug = debug

    # ---------------- main entry -----------------
    def run(
        self,
        input_vec:  np.ndarray,
        ground_vec: np.ndarray,
        logits:     np.ndarray,
    ) -> np.ndarray:
        """simple cosine gate + soft rescale (demo version)"""
        iv = input_vec.astype(np.float32)
        gv = ground_vec.astype(np.float32)
        iv /= (np.linalg.norm(iv) + 1e-8)
        gv /= (np.linalg.norm(gv) + 1e-8)

        gamma = 1.0 - 0.30 * (iv @ gv)          # shrink if vectors align
        return logits.astype(np.float32) * gamma


# --------------------------------------------------------------
_engine: Optional[WFGYEngine] = None


def get_engine(*, reload: bool = False, **kwargs) -> WFGYEngine:
    """Singleton factory (reload=True 重新建)."""
    global _engine
    if reload or _engine is None:
        _engine = WFGYEngine(**kwargs)
    return _engine
