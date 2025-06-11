from wfgy_core import WFGYRunner

if __name__ == "__main__":
    runner = WFGYRunner(
        model_id="mistralai/Mistral-7B-Instruct-v0.2",  # ✅ 這個是雲端可用模型
        remote=True
    )
    runner.run(
        prompt="What happens when you ask an AI about the meaning of life?",
        reflect=True,
        style="default",
        show_ascii=True
    )
