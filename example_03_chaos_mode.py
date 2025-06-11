# example_03_chaos_mode.py

from wfgy_core import WFGYRunner
import random

# Chaos config: maximum semantic mutation
chaos_config = {
    "bbmc_alpha": 1.25,                # Overcorrection for wild semantic jumps
    "bbpf_noise_level": 0.25,          # Inject creative noise
    "bbcr_reset_value": 0.9,           # System barely resets, retains chaotic residue
    "bbam_modulation_scale": 1.3       # Strong modulation – overrides normal bounds
}

# Funny chaos prompt
prompt = "What happens if Schrödinger’s cat becomes a quantum influencer?"

# Instantiate runner with chaos config
runner = WFGYRunner(config=chaos_config)

# Run and extract results
results = runner.run(prompt)

# Display results
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
