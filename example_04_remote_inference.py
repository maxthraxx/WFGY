from wfgy_core import WFGYRunner

runner = WFGYRunner(
    model_id="tiiuae/falcon-7b-instruct",  
    use_remote=False                      
)

runner.run("Why don't AIs like to take showers?")
