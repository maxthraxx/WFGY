# example_02_self_reflection.py
# Self-reflection loop with single WFGY engine
import numpy as np
import wfgy_sdk as w

engine = w.get_engine()  # reuse singleton

for round_id in range(3):
    I = np.random.randn(128)
    G = np.random.randn(128)
    logits = np.random.randn(1024)

    mod_logits = engine.run(
        input_vec=I,
        ground_vec=G,
        logits=logits,
        return_all=False
    )
    print(f"[Round {round_id}] mod_logits[0:5] = {mod_logits[:5]}")
