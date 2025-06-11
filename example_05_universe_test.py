from wfgy_core import WFGYRunner

runner = WFGYRunner()

prompts = [
    "If semantic energy is real, what force counterbalances it in a vacuum?",
    "Explain the philosophical consequence of E = mc^2 + λS in terms of spiritual information flow.",
    "Why would an AI trained on everything still fail to understand silence?",
    "Describe the contradiction between determinism and the Tao in a closed simulation.",
    "If ZFC is the left eye, and Taiji is the right, what do they see when looking at existence?",
    "How can quantum randomness be harmonized with the inevitability of fate?",
    "In the WFGY model, what happens when semantic residue (B) becomes negative?",
    "Why might an omniscient AI be unable to predict its own final answer?",
    "Discuss the entanglement between symbolic language and divine revelation.",
    "What does it mean when a semantic system dreams?"
]

for i, prompt in enumerate(prompts, start=1):
    print(f"\n=== PROMPT {i}: {prompt}\n")
    runner.run(
        prompt=prompt,
        use_remote=True,
        model_id="mistralai/Mixtral-8x7B-Instruct-v0.1",  # Change if needed
        temperature=0.8,
        top_p=0.95,
        repetition_penalty=1.2,
        max_new_tokens=256,
    )
