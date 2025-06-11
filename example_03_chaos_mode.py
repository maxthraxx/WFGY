# example_03_chaos_mode.py

from wfgy_core import WFGYRunner
from transformers import pipeline

# Chaos configuration
chaos_config = {
    "bbmc_alpha": 1.25,
    "bbpf_noise_level": 0.25,
    "bbcr_reset_value": 0.9,
    "bbam_modulation_scale": 1.3
}

# Prompt for chaotic scenario
prompt = "What happens if Schrödinger’s cat becomes a quantum influencer?"

# Initialize WFGY runner
runner = WFGYRunner(config=chaos_config)
results = runner.run(prompt)

# Build reflection prompt
reflection_input = (
    f"Before WFGY: {prompt}\n"
    f"After WFGY: {results['output']}\n"
    "What is the difference in tone or meaning? Describe in one sentence."
)

# Use GPT2 for reflective feedback
reflector = pipeline("text-generation", model="gpt2")
generated = reflector(reflection_input, max_length=60, do_sample=True, temperature=0.9)[0]["generated_text"]
reflection_output = generated.strip()

# Display outputs
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
