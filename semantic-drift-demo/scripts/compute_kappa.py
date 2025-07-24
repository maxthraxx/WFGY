"""
Fleiss κ agreement for drift annotations.

Create data/error_annotations.csv with columns:
Q#,rater1,rater2,rater3  (values: ok / drift)
"""

import argparse, os, pandas as pd, numpy as np
from statsmodels.stats.inter_rater import fleiss_kappa

ap = argparse.ArgumentParser()
ap.add_argument("--csv", default="data/error_annotations.csv")
args = ap.parse_args()

if not os.path.exists(args.csv):
    raise SystemExit("error_annotations.csv not found")

df = pd.read_csv(args.csv)
cats = ["ok", "drift"]
matrix = []
for _, row in df.iterrows():
    counts = [0, 0]
    for r in ("rater1", "rater2", "rater3"):
        counts[cats.index(row[r])] += 1
    matrix.append(counts)

print("Fleiss κ:", fleiss_kappa(np.asarray(matrix), method="fleiss"))
