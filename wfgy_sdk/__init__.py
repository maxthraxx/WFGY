# wfgy_sdk/__init__.py
# Public API layer for WFGY SDK
# License: MIT

from __future__ import annotations
from typing import Dict, Any, List
import os, requests, numpy as np, importlib.util
import logging

from .wfgy_engine import WFGYEngine           # core orchestrator
from . import bbmc, bbpf, bbcr, bbam          # re-export
from .evaluator import compare_logits, pretty_print

__all__ = [
    "get_engine", "enable", "disable",
    "call_remote_model", "compare_logits", "pretty_print",
    "bbmc", "bbpf", "bbcr", "bbam"
]

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------ #
# 1. Singleton Engine
# ------------------------------------------------------------------------ #
_engine: WFGYEngine | None = None

def get_engine(reload: bool = False) -> WFGYEngine:
    global _engine
    if _engine is None or reload:
        _engine = WFGYEngine(debug=True)
    return _engine

# ------------------------------------------------------------------------ #
# 2. High-level enable / disable helpers (mutable model dict pattern)
# ------------------------------------------------------------------------ #
def enable(model: Dict[str, Any]) -> Dict[str, Any]:
    eng = get_engine()
    logits_in  = np.asarray(model["attention_logits"], dtype=float)
    input_vec  = np.asarray(model["I"], dtype=float)
    ground_vec = np.asarray(model["G"], dtype=float)

    res = eng.run(input_vec=input_vec,
                  ground_vec=ground_vec,
                  logits=logits_in,
                  return_all=True)

    model["attention"]   = res["logits_mod"]
    model["wfgy_state"]  = {
        "B_norm": res["B_norm"],
        "f_S": res["f_S"],
        "collapse": res["_collapse"],
    }
    return model


def disable(model: Dict[str, Any]) -> Dict[str, Any]:
    for k in ("attention", "wfgy_state"):
        model.pop(k, None)
    return model

# ------------------------------------------------------------------------ #
# 3. Remote Hugging Face helper
# ------------------------------------------------------------------------ #
HF_ENDPOINT = "https://api-inference.huggingface.co/models/"

def call_remote_model(
    prompt: str,
    model_id: str = "gpt2",
    timeout: int = 60
) -> np.ndarray:
    """
    Fetch logits from Hugging Face Inference API.
    Requires HF_TOKEN in env var for higher rate limit.
    """
    headers = {}
    if token := os.getenv("HF_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"

    payload = {"inputs": prompt, "parameters": {"return_logits": True}}
    resp = requests.post(HF_ENDPOINT + model_id,
                         headers=headers, json=payload, timeout=timeout)
    resp.raise_for_status()
    logits = np.array(resp.json()["logits"], dtype=float)
    return logits

# ------------------------------------------------------------------------ #
# 4. Optional Torch GPU acceleration (automatic)
# ------------------------------------------------------------------------ #
def _torch_tensor(x: np.ndarray):
    if importlib.util.find_spec("torch") is None:
        return x
    import torch
    if torch.cuda.is_available():
        return torch.as_tensor(x).cuda()
    return torch.as_tensor(x)

# expose for advanced users
to_torch_tensor = _torch_tensor
