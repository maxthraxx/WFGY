"""
Draw ΔS & λ_observe charts into images/.
"""

import argparse, os, pandas as pd, matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--csv", default="data/metrics.csv")
parser.add_argument("--threshold", type=float, default=0.4)
parser.add_argument("--outdir", default="images")
args = parser.parse_args()

df = pd.read_csv(args.csv)
os.makedirs(args.outdir, exist_ok=True)


ax = df[["ΔS_baseline", "ΔS_WFGY"]].mean().plot.bar(
        color=["#ff5722", "#4caf50"], rot=0)
ax.set_ylabel("ΔS  (lower = better)")
ax.set_title("Average ΔS Drift")
plt.tight_layout()
plt.savefig(f"{args.outdir}/drift_comparison.png", dpi=300)
plt.close()


lambda_base  = (df["ΔS_baseline"] < args.threshold).mean()
lambda_wfgy  = (df["ΔS_WFGY"]    < args.threshold).mean()

plt.bar(["Baseline", "WFGY"], [lambda_base, lambda_wfgy],
        color=["#ff5722", "#4caf50"])
plt.ylim(0, 1)
plt.ylabel("λ_observe pass‑rate")
plt.title(f"λ_observe  (ΔS < {args.threshold})")

for idx, val in enumerate([lambda_base, lambda_wfgy]):
    plt.text(idx, val + 0.02, f"{val*100:.0f}%", ha="center")

plt.tight_layout()
plt.savefig(f"{args.outdir}/lambda_pass.png", dpi=300)
plt.close()

print("✓  charts saved to images/")
