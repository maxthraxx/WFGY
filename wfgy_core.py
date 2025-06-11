import os
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

class WFGYRunner:
    def __init__(self, model_id="gpt2", use_remote=False):
        self.use_remote = use_remote
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_id = model_id

        if self.use_remote:
            # Use Hugging Face pipeline for remote inference
            hf_token = os.environ.get("HF_TOKEN")
            if not hf_token:
                raise ValueError("HF_TOKEN not found in environment variables.")
            self.pipe = pipeline(
                "text-generation",
                model=model_id,
                token=hf_token,
                trust_remote_code=True
            )
        else:
            # Use local model loading
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForCausalLM.from_pretrained(model_id)
            self.pipe = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1
            )

    def run(self, prompt, **kwargs):
        print("╭──────────────────────────────╮")
        print("│   🤖 INITIATING WFGY CORE    │")
        print("│   ⚙️  MODULE: Semantic Boost │")
        print("╰──────────────────────────────╯\n")
        print("=== Prompt ===")
        print(prompt)

        result = self.pipe(prompt, **kwargs)[0]["generated_text"]

        print("\n=== Output ===")
        print(result.strip())
