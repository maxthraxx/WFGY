from wfgy_core import WFGYRunner

if __name__ == "__main__":
    runner = WFGYRunner(remote=True)
    runner.run(
        prompt="What happens when you ask an AI about the meaning of life?",
        reflect=True,
        style="default",
        show_ascii=True
    )
