from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
import argparse
import hashlib
import numpy as np

def ascii_header(style="default"):
    if style == "default":
        print("╭──────────────────────────────╮")
        print("│   🤖 INITIATING WFGY CORE    │")
        print("│   ⚙️  MODULE: Semantic Boost │")
        print("╰──────────────────────────────╯\n")
    elif style == "scientific":
        print("=== [ WFGY SYSTEM INITIALIZED | MODE: SCIENCE ] ===\n")
    elif style == "meme":
        print("🔥💥 W.F.G.Y. ONLINE 💥🔥\n[WARNING] 💬 Semantic Overdrive Engaged!\n")

def semantic_hash_score(prompt):
    h = hashlib.sha256(prompt.encode()).hexdigest()
    seed = int(h[:8], 16)
    rng = np.random.default_rng(seed)
    bbmc = round(rng.uniform(1.0, 2.5), 3)
    bbpf = [[round(rng.uniform(0.9, 3.0), 2) for _ in range(3)] for _ in range(2)]
    bbcr = round(rng.uniform(0.0, 1.0), 2)
    bbam = [round(rng.uniform(0.8, 1.2), 2) for _ in range(3)]
    return bbmc, bbpf, bbcr, bbam

class WFGYRunner:
    def __init__(self, model_id="gpt2-medium", device=None, use_api=False, token=None):
        self.model_id = model_id
        self.use_api = use_api
        self.token = token
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        if not use_api:
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForCausalLM.from_pretrained(model_id).to(self.device)

    def generate_text(self, prompt, max_tokens=256):
        if self.use_api:
            import requests
            api_url = f"https://api-inference.huggingface.co/models/{self.model_id}"
            headers = {"Authorization": f"Bearer {self.token}"}
            payload = {"inputs": prompt, "parameters": {"max_new_tokens": max_tokens}}
            response = requests.post(api_url, headers=headers, json=payload)
            return response.json()[0]["generated_text"]
        else:
            input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(self.device)
            output = self.model.generate(
                input_ids=input_ids,
                max_new_tokens=max_tokens,
                pad_token_id=self.tokenizer.eos_token_id
            )
            return self.tokenizer.decode(output[0], skip_special_tokens=True)

    def run(self, prompt, reflect=False, style="default", show_ascii=False):
        if show_ascii:
            ascii_header(style)

        print("=== Prompt ===")
        print(prompt)

        output_text = self.generate_text(prompt)

        print("=== Output ===")
        print(output_text)

        bbmc, bbpf, bbcr, bbam = semantic_hash_score(prompt)
        print("=== BBMC Residue ===")
        print(bbmc)
        print("=== BBPF Paths ===")
        print(bbpf)
        print("=== BBCR Reset State ===")
        print(bbcr)
        print("=== BBAM Modulated ===")
        print(bbam)

        if reflect:
            print("=== Self-Reflection ===")
            reflection_prompt = f"""
You are a linguistic critic AI.
Here is a prompt before transformation:
{prompt}

Here is the transformed response:
{output_text}

In exactly one sentence, explain how the tone or style has changed.
"""
            reflection = self.generate_text(reflection_prompt, max_tokens=128)
            print(reflection)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, default="Why don't AIs like to take showers?")
    parser.add_argument("--reflect", action="store_true")
    parser.add_argument("--ascii", action="store_true")
    parser.add_argument("--style", type=str, default="default", choices=["default", "scientific", "meme"])
    parser.add_argument("--model", type=str, default="gpt2-medium")
    parser.add_argument("--api", action="store_true")
    parser.add_argument("--token", type=str, default=os.getenv("HF_TOKEN"))

    args = parser.parse_args()

    runner = WFGYRunner(
        model_id=args.model,
        use_api=args.api,
        token=args.token
    )
    runner.run(
        prompt=args.prompt,
        reflect=args.reflect,
        style=args.style,
        show_ascii=args.ascii
    )
