import os
from wfgy_core import WFGYRunner

# Load Hugging Face token from environment
token = os.environ.get("HF_TOKEN")
if token is None:
    raise ValueError("HF_TOKEN not found in environment variables. Set it before running.")

# Initialize runner with a remote model
runner = WFGYRunner(
    model_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    hf_token=token,
    use_remote=True
)

# Run universe-level prompt
runner.run(
    prompt="If semantic energy is real, what force counterbalances it in a vacuum?",
    max_tokens=256,
    temperature=0.9,
    top_p=0.95
)
