import os
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import InferenceClient

class WFGYRunner:
    def __init__(self, model_id="mistralai/Mistral-7B-Instruct-v0.1", use_remote=False):
        self.use_remote = use_remote
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_id = model_id

        if self.use_remote:
            try:
                self.client = InferenceClient(model=self.model_id, token=True)
            except Exception as e:
                raise RuntimeError(f"Hugging Face login not detected or token invalid: {e}")
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
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
            result = self.client.text_generation(
                prompt=prompt,
                max_new_tokens=max_new_tokens,
                temperature=temperature
            )
        else:
            result = self.pipe(
                prompt,
                max_new_tokens=max_new_tokens,
                temperature=temperature
            )[0]["generated_text"]

        print("\n=== Output ===")
        print(result.strip())
        return result.strip()
