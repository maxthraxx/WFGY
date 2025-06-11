# example_02_self_reflection.py

from wfgy_core import WFGYRunner
from default_config import prompt_humorous

# Initialize WFGY
runner = WFGYRunner()

# Use a funny prompt to test
prompt = prompt_humorous  # Example: "Why don't AIs like to take showers?"

# Run through WFGY system
result = runner.run(prompt)

# Extract results
output_text = result["output"]
residue = result["BBMC_residue"]

# Display output and reflection
print("=== Prompt ===")
print(prompt)
print("\n=== Output ===")
print(output_text)
print("\n=== BBMC Residue ===")
print(residue)
print("\n=== Self-Reflection ===")

# Ask model to self-reflect
reflection_prompt = (
    f"Your previous response to the prompt '{prompt}' was:\n\n"
    f"\"{output_text}\"\n\n"
    "Now, reflect on how this output differs from your initial expectation or phrasing. "
    "Describe this change in one sentence."
)

# Let model try to describe what it did differently
try:
    import openai
    openai.api_key = "sk-..."  # Optional: replace with real key if using OpenAI backend

    reflection = runner.llm_generate(reflection_prompt)
    print(reflection)
except Exception:
    print("🟡 Reflection model not connected. Skipping self-analysis.")
