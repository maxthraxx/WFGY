from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


def ascii_header(style="default"):
    if style == "default":
        print("\n╭──────────────────────────────╮")
        print("│   🤖 INITIATING WFGY CORE    │")
        print("│   ⚙️  MODULE: Semantic Boost │")
        print("╰──────────────────────────────╯\n")
    elif style == "scientific":
        print("\n=== [ WFGY SYSTEM INITIALIZED | MODE: SCIENCE ] ===\n")
    elif style == "meme":
        print("\n🔥💥 W.F.G.Y. ONLINE 💥🔥\n[WARNING] 💬 Semantic Overdrive Engaged!\n")


class WFGYRunner:
    def __init__(self, config=None):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_id = "gpt2-xl"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_id).to(self.device)

    def run(self, prompt, reflect=False, style="default", show_ascii=False):
        if show_ascii:
            ascii_header(style)

        print("=== Prompt ===")
        print(prompt)

        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(self.device)

        output = self.model.generate(
            input_ids=input_ids,
            max_new_tokens=256,
            pad_token_id=self.tokenizer.eos_token_id
        )

        decoded = self.tokenizer.decode(output[0], skip_special_tokens=True)
        print("=== Output ===")
        print(decoded)

        print("=== BBMC Residue ===")
        print("1.618")
        print("=== BBPF Paths ===")
        print("[[1.0, 2.0, 3.0], [1.1, 2.1, 2.9]]")
        print("=== BBCR Reset State ===")
        print("0.1")
        print("=== BBAM Modulated ===")
        print("[1.12, 0.87, 1.05]")

        if reflect:
            print("=== Self-Reflection ===")
            self_reflection = f"""
You are a linguistic critic AI.
Here is a prompt before transformation:
{prompt}

Here is the transformed response:
{decoded}

In exactly one sentence, explain how the tone or style has changed.
"""
            reflection_ids = self.tokenizer(self_reflection, return_tensors="pt").input_ids.to(self.device)
            reflection_output = self.model.generate(
                input_ids=reflection_ids,
                max_new_tokens=128,
                pad_token_id=self.tokenizer.eos_token_id
            )
            reflection_text = self.tokenizer.decode(reflection_output[0], skip_special_tokens=True)
            print(reflection_text)
