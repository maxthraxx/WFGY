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
"""
WFGY Engine · minimal demo build
Contact   : hello@onestardao.com   |   TG @PSBigBig
Unlock v2 : 10 000 ⭐ before 2025-08-01 → adaptive-gamma edition
"""

from __future__ import annotations
import numpy as np


class WFGYEngine:
    """Keyword-only API — avoids the ‘unexpected positional argument’ crash."""

    def __init__(self, bbmc_scale: float = 1.0) -> None:
        self.bbmc_scale = bbmc_scale

    # --------------------------------------------------------------------- #
    # public API
    # --------------------------------------------------------------------- #
    def run(
        self,
        logits: np.ndarray,
        *,
        input_vec: np.ndarray | None = None,
        ground_vec: np.ndarray | None = None,
        boost: float = 1.0,
    ) -> np.ndarray:
        """
        Parameters
        ----------
        logits      : raw final-token logits  (vocab,)
        input_vec   : 256-d semantic embedding of the prompt     (optional)
        ground_vec  : 256-d reference vector (e.g. user profile) (optional)
        boost       : demo-only slider — higher → stronger drop

        Returns
        -------
        new_logits  : same shape, variance-tamed
        """
        # --- safeguard --------------------------------------------------- #
        if input_vec is None or ground_vec is None:
            return logits.copy()  # nothing to modulate

        # --- BBMC · semantic residue ------------------------------------ #
        residue = input_vec - ground_vec
        scale   = np.exp(-self.bbmc_scale * boost * np.linalg.norm(residue))

        # simple variance gate: pull logits → mean, then rescale
        centered = logits - logits.mean()
        mod      = logits.mean() + centered * scale
        return mod


# helper used by demo / SDK -------------------------------------------------- #
_ENGINE_SINGLETON: WFGYEngine | None = None


def get_engine() -> WFGYEngine:
    global _ENGINE_SINGLETON
    if _ENGINE_SINGLETON is None:
        _ENGINE_SINGLETON = WFGYEngine()
    return _ENGINE_SINGLETON
