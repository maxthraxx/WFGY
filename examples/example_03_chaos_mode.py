# examples/example_03_chaos_mode.py
import numpy as np, wfgy_sdk as w
rng = np.random.default_rng(3)

eng = w.get_engine(reload=True)
eng.gamma = 0.9

G = rng.normal(size=256); G /= np.linalg.norm(G)
I = G + rng.normal(scale=0.1, size=256)         # larger noise
logits = rng.normal(size=8192)

state = eng.run(input_vec=I, ground_vec=G, logits=logits, return_all=True)
print(f"Chaos mode — ‖B‖={state['B_norm']:.3f} | f_S={state['f_S']:.3f}")
