import argparse
from wfgy_core import WFGYRunner

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reflect", action="store_true", help="Enable self-reflection")
    parser.add_argument("--ascii", action="store_true", help="Show ASCII banner")
    parser.add_argument("--style", type=str, default="default", help="Choose style: default/scientific/meme")

    args = parser.parse_args()

    prompt = "Why don't AIs like to take showers?"
    runner = WFGYRunner()
    runner.run(prompt, reflect=args.reflect, style=args.style, show_ascii=args.ascii)
