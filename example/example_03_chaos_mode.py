# example_03_chaos_mode.py
# Exaggerated noise / γ to test stability limits
import numpy as np, wfgy_sdk as w

engine = w.get_engine(reload=True)  # fresh state

I, G = np.random.randn(256), np.random.randn(256)
logits = np.random.randn(4096)

# Temporarily tweak parameters
engine.gamma = 0.9                 # stronger attenuation
state = engine.run(
    input_vec=I,
    ground_vec=G,
    logits=logits,
    window_size=7,                 # local variance mode
    return_all=True
)
print(f"Chaos mode — ‖B‖={state['B_norm']:.3f} | f_S={state['f_S']:.3f}")
