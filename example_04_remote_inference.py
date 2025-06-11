from wfgy_core import WFGYRunner

runner = WFGYRunner(
    model_id="sshleifer/tiny-gpt2",  
    use_remote=False
)

runner.run("Why don't AIs like to take showers?")
