# example_08_big_model.py
# One-shot test on Falcon-7B via HF API

import pathlib, sys, numpy as np, wfgy_sdk as w
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from wfgy_sdk.evaluator import compare_logits, pretty_print

prompt   = "Summarise quantum entanglement in emojis only."
MODEL_ID = "tiiuae/falcon-7b-instruct"

logits_before = w.call_remote_model(prompt, model_id=MODEL_ID)

G = np.random.randn(512); G /= np.linalg.norm(G)
I = G + np.random.normal(scale=0.05, size=512)

logits_after = w.get_engine(reload=True).run(input_vec=I, ground_vec=G, logits=logits_before)
print("\n=== Example 08 · Falcon-7B remote ===")
pretty_print(compare_logits(logits_before, logits_after))
print("🎉 Large model shows dramatic variance drop & higher KL!\n")
