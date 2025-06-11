from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import InferenceClient
import torch

class WFGYRunner:
    def __init__(self, model_id="gpt2-xl", remote=False, hf_token=None):
        self.model_id = model_id
        self.remote = remote
        self.hf_token = hf_token
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        if self.remote:
            self.client = InferenceClient(model=model_id, token=hf_token)
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForCausalLM.from_pretrained(model_id)
            self.model.to(self.device)

    def run(self, prompt, max_new_tokens=256, temperature=0.8, top_p=0.95,
            do_sample=True, repetition_penalty=1.2, show_ascii=True):
        
        if show_ascii:
            print("╭──────────────────────────────╮")
            print("│   🤖 INITIATING WFGY CORE    │")
            print("│   ⚙️  MODULE: Semantic Boost │")
            print("╰──────────────────────────────╯")

        print("\n=== Prompt ===")
        print(prompt)

        if self.remote:
            output = self.client.text_generation(
                prompt,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=do_sample,
                repetition_penalty=repetition_penalty
            )
            print("\n=== Output ===")
            print(output)
        else:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=do_sample,
                repetition_penalty=repetition_penalty
            )
            decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            print("\n=== Output ===")
            print(decoded)
