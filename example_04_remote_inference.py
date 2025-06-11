from wfgy_core import WFGYRunner

# Manually set your token here for testing only (DO NOT commit it)
hf_token = "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"

runner = WFGYRunner(
    model_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    use_remote=True,
    hf_token=hf_token
)

runner.run("Why don't AIs like to take showers?")
