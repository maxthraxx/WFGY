# example_01_basic_run.py

import os
import sys

# Add WFGY SDK path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "WFGY")))

from wfgy_core import WFGYRunner

# Initialize the WFGY runner
runner = WFGYRunner()

# Define a hilarious input prompt
prompt = "Why doesn't AI like to take showers?"

# Run WFGY processing
before_output, after_output = runner.run(prompt)

# Display results
print("=== 🧼 Prompt ===")
print(prompt)

print("\n=== 🤖 Before WFGY ===")
print(before_output)

print("\n=== 🚿 After WFGY ===")
print(after_output)

print(f"\n=== 📊 Semantic Residue Score (B) ===\n{residue_score:.4f}")
