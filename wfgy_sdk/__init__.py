# wfgy_sdk/__init__.py
# Public API layer for WFGY SDK 1.0
# Author: PSBigBig & Contributors
# License: MIT

from __future__ import annotations
from typing import Dict, Any
import numpy as np

from .wfgy_engine import WFGYEngine
from . import bbmc, bbpf, bbcr, bbam  # re-export for convenience

__all__ = [
    "get_engine",
    "enable",
    "disable",
    "bbmc",
    "bbpf",
    "bbcr",
    "bbam",
]

# ------------------------------------------------------------------#
# Singleton Engine
# ------------------------------------------------------------------#
_engine: WFGYEngine | None = None


def get_engine(reload: bool = False) -> WFGYEngine:
    """
    Return a singleton WFGYEngine.  reload=True 會重建新實例。
    """
    global _engine
    if _engine is None or reload:
        _engine = WFGYEngine(debug=True)
    return _engine


# ------------------------------------------------------------------#
# High-level helpers (compatible with舊 enable/disable 流程)
# ------------------------------------------------------------------#
def enable(model: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply the full WFGY pipeline to `model`.

    Expected keys:
        "I"  : np.ndarray  # input semantic vector
        "G"  : np.ndarray  # ground-truth vector
        "attention_logits": np.ndarray  # raw logits to modulate
    """
    eng = get_engine()
    result = eng.run(
        input_vec=np.asarray(model["I"], dtype=float),
        ground_vec=np.asarray(model["G"], dtype=float),
        logits=np.asarray(model["attention_logits"], dtype=float),
        return_all=True,
    )

    # mutate & return
    model["attention"] = result["logits_mod"]
    model["wfgy_state"] = {
        "B_norm": result["B_norm"],
        "f_S": result["f_S"],
        "collapse": result["_collapse"],
    }
    return model


def disable(model: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove WFGY-specific keys from `model` (soft shutdown).
    """
    for k in ("attention", "wfgy_state"):
        model.pop(k, None)
    return model
