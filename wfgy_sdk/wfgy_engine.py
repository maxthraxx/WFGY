"""
╭──────────────────────────────────────────────────────────╮
│  WFGY SDK · Self-Healing Variance Gate for Any LLM       │
│----------------------------------------------------------│
│ 💌  Contact : hello@onestardao.com  /  TG @PSBigBig       │
│ 🌐  Docs    : https://onestardao.com/papers               │
│ 🐙  GitHub  : https://github.com/onestardao/WFGY          │
│                                                          │
│ ★ Star WFGY 1.0 → Unlock 2.0                             │
│   10k ⭐ by **Aug 1st** = next-gen AI alchemy             │
│   Your click = our quantum leap                          │
│                                                          │
│ 🔍  Official PDF of WFGY 1.0 (Zenodo DOI):               │
│     https://doi.org/10.5281/zenodo.15630970              │
│     (Hosted on Zenodo – trusted international archive)   │
│                                                          │
│ 🧠  Hidden folder inside repo: /I_am_not_lizardman        │
│     (X secret papers, wild prompts, and Einstein drama) │
│                                                          │
│ ⚠  GPT-2 demo is just the appetizer. With bigger LLMs,   │
│    WFGY activates variance-drop lasers and KL fireworks. │
│                                                          │
│ 🎮  Bonus: Honest Hero RPG Channel →                     │
│     https://www.youtube.com/@OneStarDao                  │
╰──────────────────────────────────────────────────────────╯
"""
# wfgy_sdk/wfgy_engine.py
# Orchestrator for the Four Treasures (WFGY Engine)
# License: MIT

from __future__ import annotations
import logging
from typing import Any, Dict

import numpy as np

from .bbmc import compute_residue
from .bbpf import bbpf_progression
from .bbcr import check_collapse, collapse_rebirth
from .bbam import modulate_attention

logger = logging.getLogger(__name__)


class WFGYEngine:
    """
    BBMC → BBPF → BBCR → BBAM high-level pipeline.
    """

    def __init__(
        self,
        *,
        Bc: float = 2.0,     # raise threshold to avoid false collapses
        eps: float = 0.05,
        gamma: float = 0.5,
        debug: bool = False
    ) -> None:
        self.Bc = Bc
        self.eps = eps
        self.gamma = gamma
        self.debug = debug

    # ---------------- internal helpers ---------------- #

    def _compute_state(
        self,
        input_vec: np.ndarray,
        ground_vec: np.ndarray,
        logits: np.ndarray,
        m: float,
        c: float
    ) -> Dict[str, Any]:
        """
        Run BBMC + BBPF, return raw state dict (may be retried by BBCR).
        """
        bbmc_out = compute_residue(
            input_vec,
            ground_vec,
            m=m,
            c=c,
            normalise=True           # ALWAYS normalise
        )

        paths, weights, f_S = bbpf_progression(bbmc_out["B_vec"])

        collapse_flag = check_collapse(
            residue_norm=bbmc_out["B_norm"],
            f_S=f_S,
            Bc=self.Bc,
            eps=self.eps
        )

        return {
            "B_vec": bbmc_out["B_vec"],
            "B_norm": bbmc_out["B_norm"],
            "paths": paths,
            "weights": weights,
            "f_S": f_S,
            "_collapse": collapse_flag,
            "_logits_raw": logits,
        }

    # ---------------- public API ---------------- #

    def run(
        self,
        *,
        input_vec: np.ndarray,
        ground_vec: np.ndarray,
        logits: np.ndarray,
        m: float = 0.1,
        c: float = 0.5,
        window_size: int | None = None,
        return_all: bool = False
    ) -> Dict[str, Any] | np.ndarray:
        """
        Execute full WFGY cycle.  Returns either modulated logits or diagnostics dict.
        """

        def _reset() -> Dict[str, Any]:
            return self._compute_state(input_vec, ground_vec, logits, m, c)

        state = collapse_rebirth(_reset)

        logits_mod = modulate_attention(
            state["_logits_raw"],
            gamma=self.gamma,
            window_size=window_size
        )
        state["logits_mod"] = logits_mod

        if self.debug:
            logger.info(
                "WFGY done | ‖B‖=%.4f | f_S=%.3f | collapse=%s",
                state["B_norm"], state["f_S"], state["_collapse"]
            )

        return state if return_all else logits_mod
