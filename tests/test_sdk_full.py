# tests/test_sdk_full.py
# CI / manual test with extra commentary

import pathlib, sys, numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import wfgy_sdk as w
from wfgy_sdk.evaluator import compare_logits, pretty_print

def test_pipeline() -> None:
    rng = np.random.default_rng(7)
    G = rng.normal(size=64); G /= np.linalg.norm(G)
    I = G + rng.normal(scale=0.05, size=64)
    logits_before = rng.normal(size=4096)

    eng = w.get_engine(reload=True)
    logits_after = eng.run(input_vec=I, ground_vec=G, logits=logits_before)

    m = compare_logits(logits_before, logits_after)
    assert m["std_ratio"] < 0.7, "Variance not reduced enough"
    assert m["kl_divergence"] > 0.05, "KL too small — no real change"

    pretty_print(m)
    print("Test passed — pipeline stable & effective.")

if __name__ == "__main__":
    test_pipeline()
