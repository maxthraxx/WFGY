from wfgy_core import WFGYRunner

# Inject your Hugging Face token for remote inference
hf_token = "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"

runner = WFGYRunner(
    model_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    remote=True,
    hf_token=hf_token
)

runner.run("Why don't AIs like to take showers?")
