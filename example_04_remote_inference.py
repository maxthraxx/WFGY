import argparse
import requests
import os

def ascii_header():
    print("╭────────────────────────────────────╮")
    print("│  🛰️  REMOTE MODEL ACTIVATED (HF API) │")
    print("╰────────────────────────────────────╯\n")

def query_huggingface(model_id, prompt, api_token):
    url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {api_token}"}
    payload = {"inputs": prompt}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Request failed: {response.status_code}\n{response.text}")
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="Run remote inference via Huggingface API")
    parser.add_argument("--model", type=str, required=True, help="Model ID on Huggingface (e.g. EleutherAI/gpt-j-6B)")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt to send to the model")
    parser.add_argument("--token", type=str, required=False, help="Huggingface API token (or set HF_TOKEN env var)")
    args = parser.parse_args()

    api_token = args.token or os.getenv("HF_TOKEN")
    if not api_token:
        raise ValueError("Missing Huggingface API token. Use --token or set HF_TOKEN environment variable.")

    ascii_header()
    print(f"=== Remote Model: {args.model} ===")
    print(f"Prompt: {args.prompt}\n")

    result = query_huggingface(args.model, args.prompt, api_token)
    output = result[0]["generated_text"] if isinstance(result, list) and "generated_text" in result[0] else result
    print("Output:")
    print(output)

if __name__ == "__main__":
    main()
