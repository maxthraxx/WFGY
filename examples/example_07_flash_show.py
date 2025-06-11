# example_07_flash_show.py
# Flashy showcase: 10 hard prompts, aggressive settings

import pathlib, sys, numpy as np, torch, textwrap
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from transformers import GPT2LMHeadModel, GPT2TokenizerFast
import wfgy_sdk as w
from wfgy_sdk.evaluator import compare_logits

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

GAMMA = 1.0
NOISE = 0.12
rng = np.random.default_rng(999)

tok = GPT2TokenizerFast.from_pretrained("gpt2")
gpt2 = GPT2LMHeadModel.from_pretrained("gpt2").eval()

eng = w.get_engine(reload=True)
eng.gamma = GAMMA

print("\n=== Example 07 · Flash-show (GPT-2 baseline) ===")
records = []
for idx, prompt in enumerate(PROMPTS, 1):
    ids = tok(prompt, return_tensors="pt").input_ids
    with torch.no_grad():
        out = gpt2(ids, output_hidden_states=True, return_dict=True)

    logits0 = out.logits[0, -1].cpu().numpy()
    hid = out.hidden_states[-2][0, -1].cpu().numpy()
    G = hid / np.linalg.norm(hid)
    I = G + rng.normal(scale=NOISE, size=G.shape)

    logits1 = eng.run(input_vec=I, ground_vec=G, logits=logits0)
    m = compare_logits(logits0, logits1)
    records.append(m)

    print(f"[{idx:02d}] KL {m['kl_divergence']:.2f} | "
          f"var↓ {(1-m['std_ratio'])*100:.0f}% | "
          f"top-1 {'✔' if m['top1_shift'] else '✘'} | "
          f"{textwrap.shorten(prompt, 45)}")

avg = {k: np.mean([r[k] for r in records]) for k in records[0]}
print("\n--- AVERAGE over 10 prompts ---")
for k, v in avg.items():
    if k == "top1_shift":
        print(f"{k}: {v*100:.0f}%")
    else:
        print(f"{k}: {v:.3f}")

print("⚠ GPT-2 demo; swap in a ≥7 B model to see even stronger numbers.\n")
