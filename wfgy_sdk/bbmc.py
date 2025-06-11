# bbmc.py
# Semantic Residue (BBMC) — rigorous implementation
# Author: PSBigBig & Contributors
# License: MIT

from __future__ import annotations
import logging
from typing import Tuple, Dict

import numpy as np

logger = logging.getLogger(__name__)


def compute_residue(
    input_vec: np.ndarray,
    ground_vec: np.ndarray,
    m: float = 1.0,
    c: float = 1.0,
    return_vector: bool = True
) -> Dict[str, np.ndarray | float]:
    """
    Compute the semantic residue B = I - G + m*c^2.

    Parameters
    ----------
    input_vec : np.ndarray
        Input semantic vector I.
    ground_vec : np.ndarray
        Ground-truth semantic vector G.
    m : float, optional
        Matching coefficient.
    c : float, optional
        Context factor.
    return_vector : bool, optional
        If True, include the full residue vector in the output.

    Returns
    -------
    dict
        {
            "B_vec": np.ndarray,        # Only if return_vector is True
            "B_norm": float             # L2 norm of B_vec
        }

    Raises
    ------
    ValueError
        If the shapes of input_vec and ground_vec do not match.
    """
    if input_vec.shape != ground_vec.shape:
        raise ValueError("input_vec and ground_vec must have identical shape")

    B_vec = input_vec - ground_vec + m * (c ** 2)
    B_norm = float(np.linalg.norm(B_vec, ord=2))

    result = {"B_norm": B_norm}
    if return_vector:
        result["B_vec"] = B_vec

    logger.debug("BBMC - residue computed | ‖B‖ = %.6f", B_norm)
    return result

# -------------------- demo -------------------- #
def run_demo() -> None:
    """Quick smoke-test for BBMC."""
    import numpy as np

    I, G = np.random.randn(8), np.random.randn(8)
    out = compute_residue(I, G)
    print(f"BBMC demo ‖B‖ = {out['B_norm']:.4f}")


if __name__ == "__main__":
    run_demo()

