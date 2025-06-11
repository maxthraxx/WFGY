from wfgy_core import WFGYRunner

runner = WFGYRunner(
    model_id="OpenAssistant/oasst-sft-1-pythia-12b",  # ✅ 改這行就好
    use_remote=True
)

runner.run(
    prompt="If semantic energy is real, what force counterbalances it in a vacuum?",
    max_new_tokens=300,
    temperature=0.7
)
