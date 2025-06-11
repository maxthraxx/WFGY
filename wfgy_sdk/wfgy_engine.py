# wfgy_engine.py
# Orchestrator for the Four Treasures (WFGY Engine)
# Author: PSBigBig & Contributors
# License: MIT

from __future__ import annotations
import logging
from typing import Any, Dict

import numpy as np

from bbmc import compute_residue
from bbpf import bbpf_progression
from bbcr import check_collapse, collapse_rebirth
from bbam import modulate_attention

logger = logging.getLogger(__name__)


class WFGYEngine:
    """
    High-level wrapper executing BBMC → BBPF → BBCR → BBAM pipeline.
    """

    def __init__(
        self,
        *,
        Bc: float = 1.0,
        eps: float = 0.05,
        gamma: float = 0.5,
        debug: bool = False
    ) -> None:
        self.Bc = Bc
        self.eps = eps
        self.gamma = gamma
        self.debug = debug

    # ------------------------ internal helpers ------------------------

    def _compute_state(
        self,
        input_vec: np.ndarray,
        ground_vec: np.ndarray,
        logits: np.ndarray,
        m: float,
        c: float
    ) -> Dict[str, Any]:
        """Return full state dict; may be called repeatedly after collapse."""
        # --- BBMC ---
        bbmc_out = compute_residue(input_vec, ground_vec, m=m, c=c)

        # --- BBPF ---
        paths, weights, f_S = bbpf_progression(bbmc_out["B_vec"])

        # --- BBCR decision ---
        collapse_flag = check_collapse(
            residue_norm=bbmc_out["B_norm"],
            f_S=f_S,
            Bc=self.Bc,
            eps=self.eps
        )

        state = {
            "B_vec": bbmc_out["B_vec"],
            "B_norm": bbmc_out["B_norm"],
            "paths": paths,
            "weights": weights,
            "f_S": f_S,
            "_collapse": collapse_flag,
            "_logits_raw": logits,
        }
        return state

    # ----------------------------- public ------------------------------

    def run(
        self,
        *,
        input_vec: np.ndarray,
        ground_vec: np.ndarray,
        logits: np.ndarray,
        m: float = 1.0,
        c: float = 1.0,
        window_size: int | None = None,
        return_all: bool = False
    ) -> Dict[str, Any] | np.ndarray:
        """
        Execute full WFGY reasoning cycle and return modulated logits
        (plus diagnostics if return_all=True).

        Parameters
        ----------
        input_vec : np.ndarray
            Input semantic vector I.
        ground_vec : np.ndarray
            Ground semantic vector G.
        logits : np.ndarray
            Raw logits prior to modulation.
        m, c : float
            BBMC parameters.
        window_size : int or None
            Local window for BBAM (None → global variant).
        return_all : bool
            If True, return detailed diagnostics.

        Returns
        -------
        np.ndarray or dict
            Modulated logits, or full state dictionary if return_all=True.
        """

        def _reset_state() -> Dict[str, Any]:
            return self._compute_state(
                input_vec, ground_vec, logits, m, c
            )

        # Execute collapse-rebirth loop
        state = collapse_rebirth(_reset_state)

        # --- BBAM ---
        logits_mod = modulate_attention(
            state["_logits_raw"],
            gamma=self.gamma,
            window_size=window_size
        )
        state["logits_mod"] = logits_mod

        if self.debug:
            logger.info(
                "WFGY run complete | ‖B‖=%.6f | f_S=%.6f | collapse=%s",
                state["B_norm"], state["f_S"], state["_collapse"]
            )

        return state if return_all else logits_mod
