from wfgy_core import WFGYRunner
import os

if __name__ == "__main__":
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise ValueError("HF_TOKEN not found in environment variables. Set it before running.")

    runner = WFGYRunner(remote=True, hf_token=hf_token)
    runner.run(
        prompt="What happens when you ask an AI about the meaning of life?",
        reflect=True,
        style="default",
        show_ascii=True
    )
