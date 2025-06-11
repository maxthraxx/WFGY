import os
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

class WFGYRunner:
    def __init__(self, model_id="tiiuae/falcon-7b-instruct", use_remote=False):
        self.use_remote = use_remote
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_id = model_id

        if self.use_remote:
            raise RuntimeError("❌ Remote mode is disabled in this version for Colab stability.")
        else:
            print(f"🧠 Loading local model: {model_id} on device: {self.device}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForCausalLM.from_pretrained(model_id).to(self.device)
            self.pipe = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1
            )

    def run(self, prompt, max_new_tokens=200, temperature=0.7):
        print("╭──────────────────────────────╮")
        print("│   🤖 INITIATING WFGY CORE    │")
        print("│   ⚙️  MODULE: Semantic Boost │")
        print("╰──────────────────────────────╯\n")
        print("=== Prompt ===")
        print(prompt)

        if self.use_remote:
            raise RuntimeError("❌ Remote mode is not supported in this build.")
        else:
            result = self.pipe(
                prompt,
                max_new_tokens=max_new_tokens,
                temperature=temperature
            )[0]["generated_text"]

        print("\n=== Output ===")
        print(result.strip())
        return result.strip()
