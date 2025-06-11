# example_04_remote_inference.py
# Skeleton showing how to plug WFGY before/after LLM inference
# (Replace `call_model()` with real HuggingFace API / local model.)

import numpy as np, wfgy_sdk as w

def call_model(prompt: str, model_id="gpt2", use_remote=False) -> np.ndarray:
    """Dummy function: returns random logits like an LLM would."""
    vocab = 32000
    return np.random.randn(vocab)

prompts = [
    "Please answer a question you are least confident about.",
    "Now WFGY is activated. Describe the change in your reasoning.",
    "Explain the concept of 'semantic gravity' with WFGY enabled."
]

engine = w.get_engine(reload=True)

for idx, p in enumerate(prompts, 1):
    raw_logits = call_model(p)
    I, G = np.random.randn(128), np.random.randn(128)     # demo vectors
    final_logits = engine.run(
        input_vec=I, ground_vec=G, logits=raw_logits
    )
    print(f"[Stage {idx}] prompt = {p[:40]}... | mod_logits[0] = {final_logits[0]:.4f}")
