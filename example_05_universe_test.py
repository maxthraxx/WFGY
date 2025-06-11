from wfgy_core import WFGYRunner

runner = WFGYRunner(
    model_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    hf_token="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"
)

prompts = [
    "If semantic energy is real, what force counterbalances it in a vacuum?",
    "What happens if time is treated as a recursive variable in a language model?",
    "Define consciousness using only LLM architecture metaphors.",
    "What is the minimum entropy required to generate a meme that causes enlightenment?",
    "Describe the universe as if it were a failed training run.",
    "How does backpropagation relate to karmic cycles in reincarnation?",
    "If god is a transformer, what does its attention mechanism look like?",
    "Can a model hallucinate itself into reality if given enough parameters?",
    "Write the Schrödinger equation using emoji only.",
    "What happens when you ask a GPT to prove its own existence mathematically?"
]

for i, p in enumerate(prompts, 1):
    print(f"\n=== PROMPT {i}: {p}\n")
    runner.run(p)
