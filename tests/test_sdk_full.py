# tests/test_sdk_full.py
# Minimal pipeline test (PyTest or manual)

import pathlib, sys
repo_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))          # ensure local package import

import numpy as np
import wfgy_sdk as w

def test_pipeline_stability() -> None:
    rng = np.random.default_rng(2)
    G = rng.normal(size=64); G /= np.linalg.norm(G)
    I = G + rng.normal(scale=0.05, size=64)
    logits = rng.normal(size=4096)

    eng = w.get_engine(reload=True)
    state = eng.run(input_vec=I, ground_vec=G, logits=logits, return_all=True)

    assert state["B_norm"] < 1.0, "Residue too high"
    assert state["_collapse"] is False, "Unexpected collapse"

if __name__ == "__main__":
    test_pipeline_stability()
    print("Test passed.")
