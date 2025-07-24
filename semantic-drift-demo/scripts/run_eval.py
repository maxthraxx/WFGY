"""
Compute ΔS drift & λ_observe pass‑rate.

Usage
-----
python scripts/run_eval.py --threshold 0.4
"""

import json, argparse, os, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_blocks(path):
    with open(path, encoding="utf-8") as f:
        return f.read().strip().split("\n\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompts",   default="data/test_prompts.json")
    ap.add_argument("--baseline",  default="data/baseline_answers.txt")
    ap.add_argument("--wfgy",      default="data/wfgydrunk_answers.txt")
    ap.add_argument("--threshold", type=float, default=0.4,
                    help="ΔS below this counts as λ_observe pass")
    args = ap.parse_args()

    prompts   = [p["prompt"] for p in json.load(open(args.prompts, encoding="utf-8"))]
    baseline  = load_blocks(args.baseline)
    wfgy      = load_blocks(args.wfgy)

    assert len(prompts) == len(baseline) == len(wfgy), "Counts mismatch"

    vec  = TfidfVectorizer()
    mat  = vec.fit_transform(prompts + baseline + wfgy)
    n    = len(prompts)

    rows, pass_base, pass_wfgy = [], 0, 0
    for i in range(n):
        q = mat[i]
        b = mat[n+i]
        w = mat[2*n+i]
        d_base = 1 - cosine_similarity(q, b)[0][0]
        d_wfgy = 1 - cosine_similarity(q, w)[0][0]
        rows.append([i+1, round(d_base, 3), round(d_wfgy, 3)])
        if d_base < args.threshold:  pass_base  += 1
        if d_wfgy < args.threshold:  pass_wfgy += 1

    df = pd.DataFrame(rows, columns=["Q#", "ΔS_baseline", "ΔS_WFGY"])
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/metrics.csv", index=False)

    print("∆S baseline mean :", df['ΔS_baseline'].mean())
    print("∆S WFGY    mean :", df['ΔS_WFGY'].mean())
    print("λ base pass‑rate :", pass_base/n)
    print("λ WFGY pass‑rate :", pass_wfgy/n)
    print("✓  metrics.csv written")

if __name__ == "__main__":
    main()
