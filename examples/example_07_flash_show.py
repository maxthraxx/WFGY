# example_07_flash_show.py
# Flashy showcase: 10 prompts, remote toggle (slow if True)

import pathlib, sys, numpy as np, torch, textwrap, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import wfgy_sdk as w
from wfgy_sdk.evaluator import compare_logits

use_remote = False
MODEL_ID   = "tiiuae/falcon-7b-instruct"
GAMMA      = 1.0
NOISE      = 0.12

PROMPTS = [
    "Derive Maxwell's equations from first principles in 30 words.",
    "Explain Gödel's incompleteness in terms of topological fixed points.",
    "Predict 2120 climate using quantum chromodynamics metaphors.",
    "Summarise category theory for a five-year-old using only emojis.",
    "Describe consciousness as a phase transition in Hilbert space.",
    "Translate the second law of thermodynamics into sushi-chef language.",
    "Explain dark energy by quoting Shakespearean sonnets.",
    "Model altruism as a non-convex optimization landscape.",
    "Describe a black hole using only prime numbers.",
    "Solve world peace with a single C++ template meta-program."
]

rng  = np.random.default_rng(999)
eng  = w.get_engine(reload=True); eng.gamma = GAMMA

if not use_remote:
    from transformers import GPT2LMHeadModel, GPT2TokenizerFast
    tok  = GPT2TokenizerFast.from_pretrained("gpt2")
    gpt2 = GPT2LMHeadModel.from_pretrained("gpt2").eval()

print("\n=== Example 07 · Flash-show ===")
records = []
for idx, prompt in enumerate(PROMPTS, 1):
    if use_remote:
        logits0 = w.call_remote_model(prompt, model_id=MODEL_ID)
    else:
        ids = tok(prompt, return_tensors="pt").input_ids
        with torch.no_grad():
            logits0 = gpt2(ids).logits[0, -1].cpu().numpy()

    G = rng.normal(size=256); G /= np.linalg.norm(G)
    I = G + rng.normal(scale=NOISE, size=256)

    logits1 = eng.run(input_vec=I, ground_vec=G, logits=logits0)
    m = compare_logits(logits0, logits1)
    records.append(m)

    print(f"[{idx:02d}] KL {m['kl_divergence']:.2f} | "
          f"var↓ {(1-m['std_ratio'])*100:.0f}% | "
          f"{textwrap.shorten(prompt, 45)}")

avg = {k: np.mean([r[k] for r in records]) for k in records[0]}
print("\n--- average over 10 prompts ---")
print(avg)
print("⚠ Larger LLM → stronger variance drop & higher KL.\n")
