# wfgy_sdk/__init__.py
# High-level convenience API
# Author: PSBigBig & Contributors
# License: MIT

from __future__ import annotations
import numpy as np
from typing import Dict, Any

from .wfgy_engine import WFGYEngine

__all__ = ["enable", "disable", "get_engine"]

# SINGLETON engine ----------------------------------------------------------
_engine: WFGYEngine | None = None


def get_engine(reload: bool = False) -> WFGYEngine:
    """
    Return a singleton WFGYEngine (reload=True 重新建立).
    """
    global _engine
    if _engine is None or reload:
        _engine = WFGYEngine(debug=True)
    return _engine


# PUBLIC API ----------------------------------------------------------------
def enable(model: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run the full WFGY pipeline on a model-like dict.

    Expected keys in `model`:
      - "I"  : np.ndarray   # input semantic vector
      - "G"  : np.ndarray   # ground-truth vector
      - "attention_logits": np.ndarray
    Output keys added / overwritten:
      - "attention": np.ndarray  # modulated logits
      - "wfgy_state": dict       # diagnostics (B_norm, f_S, etc.)
    """
    eng = get_engine()
    mod_out = eng.run(
        input_vec=model["I"],
        ground_vec=model["G"],
        logits=model["attention_logits"],
        return_all=True,   # 取 diagnostics
    )

    model["attention"] = mod_out["logits_mod"]
    model["wfgy_state"] = {
        "B_norm": mod_out["B_norm"],
        "f_S": mod_out["f_S"],
        "collapse": mod_out["_collapse"],
    }
    print("✅ WFGY 1.0 ENABLED — B_norm={:.4f}, f_S={:.4f}".format(
        mod_out["B_norm"], mod_out["f_S"]
    ))
    return model


def disable(model: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove WFGY-related keys for a clean shutdown.
    """
    for k in ("attention", "wfgy_state"):
        model.pop(k, None)
    print("❌ WFGY disabled")
    return model
