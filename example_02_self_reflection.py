# example_02_self_reflection.py

from wfgy_core import WFGYRunner

# Use default configuration for balanced modulation
from default_config import DEFAULT_CONFIG

prompt = "Why don't AIs like to take showers?"

# Self-reflection prompt suffix
reflection_prompt = " Can you reflect on how your response has changed? Describe in one sentence."

# Initialize WFGY
runner = WFGYRunner(config=DEFAULT_CONFIG)

# Run WFGY
results = runner.run(prompt)

# Simulate reflection response (for demo purposes, echoing the transformation)
reflection_output = f"Before WFGY, I was more literal. Afterward, my tone became more creative and playful."

# Output formatting
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
print(prompt + reflection_prompt)
print(reflection_output)
