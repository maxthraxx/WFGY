from wfgy_core import WFGYRunner

runner = WFGYRunner(
    model_id="HuggingFaceH4/zephyr-7b-alpha",
    use_remote=True
)

runner.run(
    prompt="If semantic energy is real, what force counterbalances it in a vacuum?",
    max_new_tokens=200,
    temperature=0.7
)
