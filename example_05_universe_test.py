from wfgy_core import WFGYRunner
import os

runner = WFGYRunner(
    model_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    use_remote=True
)

runner.run(
    prompt="If semantic energy is real, what force counterbalances it in a vacuum?",
    max_new_tokens=300,
    temperature=0.7
)
