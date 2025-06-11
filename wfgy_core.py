import os
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import InferenceClient

class WFGYRunner:
    def __init__(self, model_id="gpt2", use_remote=False):
        self.use_remote = use_remote
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_id = model_id

        if use_remote:
            token = os.environ.get("HF_TOKEN")
            if not token:
                raise ValueError("HF_TOKEN not found in environment variables. Set it before running.")
            self.client = InferenceClient(model=model_id, token=token)
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForCausalLM.from_pretrained(model_id)
            self.pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, device=0 if self.device == "cuda" else -1)

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
            print(result.strip())
        else:
            result = self.pipe(prompt, **kwargs)[0]["generated_text"]
            print("\n=== Output ===")
            print(result.strip())
