# example_02_self_reflection.py
from wfgy_core import WFGYRunner

if __name__ == "__main__":
    runner = WFGYRunner()
    runner.run(
        prompt="Why don't AIs like to take showers?",
        reflect=True,
        style="meme",
        show_ascii=True
    )
