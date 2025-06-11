import os
from wfgy_core import WFGYRunner

# Set Hugging Face token via environment variable (must be defined before running)
hf_token = os.environ.get("HF_TOKEN")

if not hf_token:
    raise ValueError("HF_TOKEN not found in environment variables. Set it before running.")

runner = WFGYRunner(
    model_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    use_remote=True,
    hf_token=hf_token
)

runner.run("Why don't AIs like to take showers?")
