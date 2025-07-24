"""
Draw ΔS & λ_observe charts into images/.
"""

import argparse, os, pandas as pd, matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("--csv",       default="data/metrics.csv")
ap.add_argument("--threshold", default=0.4, type=float)
ap.add_argument("--outdir",    default="images")
args = ap.parse_args()

df = pd.read_csv(args.csv)
os.makedirs(args.outdir, exist_ok=True)

# ΔS bar
ax = df[["ΔS_baseline", "ΔS_WFGY"]].mean().plot.bar(
        color=["#ff5722", "#4caf50"], rot=0)
ax.set_ylabel("ΔS  (lower = better)")
ax.set_title("Average ΔS Drift")
plt.tight_layout()
plt.savefig(f"{args.outdir}/drift_comparison.png", dpi=300)
plt.close()

# λ bar
λ_base = (df["ΔS_baseline"] < args.threshold).mean()
λ_wfgy = (df["ΔS_WFGY"]    < args.threshold).mean()
plt.bar(["Baseline", "WFGY"], [λ_base, λ_wfgy],
        color=["#ff5722", "#4caf50"])
plt.ylim(0, 1)
plt.ylabel("λ_observe pass‑rate")
plt.title(f"λ_observe  (ΔS <th {args.threshold})")
for idx, val in enumerate([λ_base, λ_wfgy]):
    plt.text(idx, val + 0.02, f"{val*100:.0f}%", ha="center")
plt.tight_layout()
plt.savefig(f"{args.outdir}/lambda_pass.png", dpi=300)
plt.close()

print("✓  charts saved to images/")
