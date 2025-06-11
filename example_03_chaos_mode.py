import argparse
from wfgy_core import WFGYRunner

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reflect", action="store_true", help="Enable self-reflection output")
    parser.add_argument("--ascii", action="store_true", help="Enable ASCII visual output")
    parser.add_argument("--style", type=str, default="chaos", help="Output style mode")
    parser.add_argument("--model", type=str, default="gpt2-medium", help="Model ID (e.g., gpt2, gpt2-xl)")
    args = parser.parse_args()

    config = {
        "style": args.style,
        "reflect": args.reflect,
        "ascii": args.ascii,
        "model_id": args.model
    }

    runner = WFGYRunner(config=config)
    prompt = "What happens if Schrödinger’s cat becomes a quantum influencer?"
    output = runner.run(prompt)
    print(output)
