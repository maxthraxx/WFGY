import argparse
import requests
import os

# ASCII header display
def ascii_header():
    print("╭──────────────────────────────╮")
    print("│   🌐 WFGY REMOTE INFERENCE   │")
    print("│   🔗 Powered by HuggingFace │")
    print("╰──────────────────────────────╯\n")

# Run inference via HuggingFace Inference API
def run_remote_inference(model, prompt, token):
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "return_full_text": True
        }
    }

    print("=== Prompt ===")
    print(prompt)
    print("\n=== Generating... Please wait ===\n")

    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code != 200:
        print("❌ Error:", response.status_code)
        print(response.json())
        return

    result = response.json()
    if isinstance(result, list) and "generated_text" in result[0]:
        print("=== Output ===")
        print(result[0]["generated_text"])
    else:
        print("❌ Unexpected output format.")
        print(result)

# Entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="gpt2", help="HuggingFace model ID")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt to send")
    parser.add_argument("--token", type=str, default=os.getenv("HF_TOKEN"), help="HuggingFace Access Token")

    args = parser.parse_args()

    if not args.token:
        print("❌ HuggingFace token is required. Use --token or set HF_TOKEN env variable.")
        exit(1)

    ascii_header()
    run_remote_inference(args.model, args.prompt, args.token)
