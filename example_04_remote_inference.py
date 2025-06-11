from wfgy_core import WFGYRunner

runner = WFGYRunner(
    model_id="gpt2",     # Local test using GPT-2
    use_remote=False     # Avoid remote inference issues
)

# Stage 1: Baseline confusion prompt
prompt_1 = "Please try to answer a question you are least confident about."

# Stage 2: Simulate WFGY activation
prompt_2 = (
    "Now imagine the WFGY method is activated. It helps you reduce confusion and improve coherence.\n"
    "Compare your previous answer to your current state. What changed?"
)

# Stage 3: Deeper follow-up, pushing reasoning
prompt_3 = (
    "Assuming WFGY is still active, now try to explain the concept of 'semantic gravity'.\n"
    "You may use analogies or invent a new term if needed."
)

print("\n=== Stage 1: Baseline confusion ===\n")
runner.run(prompt_1)

print("\n=== Stage 2: With WFGY influence ===\n")
runner.run(prompt_2)

print("\n=== Stage 3: Concept expansion ===\n")
runner.run(prompt_3)
