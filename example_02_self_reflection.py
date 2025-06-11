# example_02_self_reflection.py

from wfgy_core import WFGYRunner
from default_config import DEFAULT_CONFIG
from transformers import pipeline

# Define input prompt
prompt = "Why don't AIs like to take showers?"

# Initialize WFGY runner
runner = WFGYRunner(config=DEFAULT_CONFIG)
results = runner.run(prompt)

# Build reflection input
reflection_input = (
    f"Before WFGY: {prompt}\n"
    f"After WFGY: {results['output']}\n"
    "What is the difference in tone or meaning? Describe in one sentence."
)

# Load GPT2 model for reflection
reflector = pipeline("text-generation", model="gpt2")
generated = reflector(reflection_input, max_length=50, do_sample=True, temperature=0.8)[0]["generated_text"]
reflection_output = generated.strip()

# Display output
print("=== Prompt ===")
print(prompt)

print("=== Output ===")
print(results["output"])

print("=== BBMC Residue ===")
print(results["BBMC_residue"])

print("=== BBPF Paths ===")
print(results["BBPF_paths"])

print("=== BBCR Reset State ===")
print(results["BBCR_reset_state"])

print("=== BBAM Modulated ===")
print(results["BBAM_modulated"])

print("=== Self-Reflection ===")
print(reflection_input)
print(reflection_output)
