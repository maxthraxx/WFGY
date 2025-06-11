from wfgy_core import WFGYRunner

# Create the runner
runner = WFGYRunner()

# Test prompt
prompt = "Why don't AIs like to take showers?"

# Run the model
result = runner.run(prompt)

# Output results
print("=== Prompt ===")
print(result["prompt"])

print("=== Output ===")
print(result["output"])

print("=== BBMC Residue ===")
print(result["BBMC_residue"])

print("=== BBPF Paths ===")
print(result["BBPF_paths"])

print("=== BBCR Reset State ===")
print(result["BBCR_reset_state"])

print("=== BBAM Modulated ===")
print(result["BBAM_modulated"])
