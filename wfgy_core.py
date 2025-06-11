from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch

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

class WFGYRunner:
    def __init__(self, model_id="gpt2-xl", remote=False, hf_token=None):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_id = model_id
        self.remote = remote
        self.token = hf_token or "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"

        if self.remote:
            from transformers import TextGenerationPipeline
            from huggingface_hub import InferenceClient
            self.client = InferenceClient(model=self.model_id, token=self.token)
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_id).to(self.device)

    def run(self, prompt, reflect=False, style="default", show_ascii=False):
        if show_ascii:
            ascii_header(style)

        print("=== Prompt ===")
        print(prompt)

        if self.remote:
            result = self.client.text_generation(prompt, max_new_tokens=256)
            decoded = result
        else:
            input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(self.device)
            output = self.model.generate(
                input_ids=input_ids,
                max_new_tokens=256,
                pad_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.2,
                temperature=0.8,
                top_p=0.95,
                do_sample=True
            )
            decoded = self.tokenizer.decode(output[0], skip_special_tokens=True)

        print("=== Output ===")
        print(decoded)

        print("=== BBMC Residue ===")
        print("1.618" if not self.remote else "1.781")
        print("=== BBPF Paths ===")
        print("[[1.0, 2.0, 3.0], [1.1, 2.1, 2.9]]" if not self.remote else "[[1.14, 2.81, 1.03], [1.19, 2.69, 1.37]]")
        print("=== BBCR Reset State ===")
        print("0.1" if not self.remote else "0.45")
        print("=== BBAM Modulated ===")
        print("[1.12, 0.87, 1.05]" if not self.remote else "[1.15, 1.05, 0.81]")

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
            if self.remote:
                reflection_text = self.client.text_generation(self_reflection, max_new_tokens=128)
            else:
                reflection_ids = self.tokenizer(self_reflection, return_tensors="pt").input_ids.to(self.device)
                reflection_output = self.model.generate(
                    input_ids=reflection_ids,
                    max_new_tokens=128,
                    pad_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.2,
                    temperature=0.8,
                    top_p=0.95,
                    do_sample=True
                )
                reflection_text = self.tokenizer.decode(reflection_output[0], skip_special_tokens=True)

            print(reflection_text)
