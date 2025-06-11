# example_03_chaos_mode.py

from wfgy_core import WFGYRunner
from transformers import pipeline

chaos_config = {
    "bbmc_alpha": 1.25,
    "bbpf_noise_level": 0.25,
    "bbcr_reset_value": 0.9,
    "bbam_modulation_scale": 1.3
}

prompt = "What happens if Schrödinger’s cat becomes a quantum influencer?"

runner = WFGYRunner(config=chaos_config)
results = runner.run(prompt)

reflection_input = (
    f"You are a linguistic critic AI.\n"
    f"Here is a prompt before transformation:\n{prompt}\n\n"
    f"Here is the transformed response:\n{results['output']}\n\n"
    "In exactly one sentence, explain how the tone or style has changed."
)

reflector = pipeline("text-generation", model="gpt2")
generated = reflector(reflection_input, max_length=60, do_sample=True, temperature=0.9)[0]["generated_text"]
reflection_output = generated.strip()

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
