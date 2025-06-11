from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from huggingface_hub import InferenceClient
import os


class WFGYRunner:
    def __init__(self, model_id="tiiuae/falcon-7b-instruct", hf_token=None, use_remote=False):
        self.model_id = model_id
        self.use_remote = use_remote
        self.hf_token = hf_token or os.environ.get("HF_TOKEN")

        if not self.hf_token:
            raise ValueError("HF_TOKEN not found in environment variables or passed to constructor.")

        if self.use_remote:
            self.client = InferenceClient(model=model_id, token=self.hf_token)
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(model_id, token=self.hf_token)
            self.model = AutoModelForCausalLM.from_pretrained(model_id, token=self.hf_token)
            self.pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

    def run(self, prompt, **kwargs):
    print("╭──────────────────────────────╮")
    print("│   🤖 INITIATING WFGY CORE    │")
    print("│   ⚙️  MODULE: Semantic Boost │")
    print("╰──────────────────────────────╯\n")
    print("=== Prompt ===")
    print(prompt)

    if self.use_remote:
        result = self.client.text_generation(prompt, **kwargs)
        print("\n=== Output ===")
        print(result.strip())  # 
    else:
        result = self.pipe(prompt, **kwargs)[0]["generated_text"]
        print("\n=== Output ===")
        print(result.strip())
