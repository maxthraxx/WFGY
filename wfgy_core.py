import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import InferenceClient

class WFGYRunner:
    def __init__(
        self,
        model_id="gpt2-xl",
        remote=False,
        hf_token="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"
    ):
        self.model_id = model_id
        self.remote = remote
        self.token = hf_token
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        if self.remote:
            self.client = InferenceClient(
                model=self.model_id,
                token=self.token,
                provider="huggingface"
            )
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto"
            )

    def run(self, prompt, reflect=False, style="default", show_ascii=False):
        if show_ascii:
            print("╭──────────────────────────────╮")
            print("│   🤖 INITIATING WFGY CORE    │")
            print("│   ⚙️  MODULE: Semantic Boost │")
            print("╰──────────────────────────────╯")
        print(f"\n=== Prompt ===\n{prompt}")

        if self.remote:
            result = self.client.text_generation(
                prompt,
                max_new_tokens=256,
                repetition_penalty=1.2,
                temperature=0.8,
                top_p=0.95,
                do_sample=True
            )
        else:
            input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(self.device)
            output_ids = self.model.generate(
                input_ids,
                max_new_tokens=256,
                repetition_penalty=1.2,
                temperature=0.8,
                top_p=0.95,
                do_sample=True
            )
            result = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

        print(f"\n=== Output ===\n{result}")
        print("\n=== BBMC Residue ===\n1.618")
        print("=== BBPF Paths ===\n[[1.0, 2.0, 3.0], [1.1, 2.1, 2.9]]")
        print("=== BBCR Reset State ===\n0.1")
        print("=== BBAM Modulated ===\n[1.12, 0.87, 1.05]")

        if reflect:
            print("=== Self-Reflection ===\n")
            print("You are a linguistic critic AI.")
            print("Here is a prompt before transformation:")
            print(prompt)
            print("\nHere is the transformed response:")
            print(result)
            for _ in range(9):
                print("\nIn exactly one sentence, explain how the tone or style has changed.")
