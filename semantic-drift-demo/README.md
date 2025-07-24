
# Semantic‑Drift-Demo

30 multi‑step prompts that expose how answers drift off topic.  
We compare plain LLM output (**Baseline**) to **WFGY + Drunk Mode**.

| Metric | Meaning | Good? |
|--------|---------|-------|
| **ΔS** | Prompt‑to‑answer distance (0 = perfect) | ↓ lower |
| **λ_observe** | % of cases with ΔS < threshold (0.4) | ↑ higher |

<div align="center">
  <img src="images/drift_comparison.png" width="420"/>
  <img src="images/lambda_pass.png"  width="420"/>
</div>

---

## Quick Start

```bash
pip install -r requirements.txt          # sklearn, pandas, matplotlib, statsmodels
python scripts/run_eval.py               # → data/metrics.csv
python scripts/plot_results.py           # → images/ charts refreshed
````

### Swap in your own answers

1. Edit `data/baseline_answers.txt` and `data/wfgydrunk_answers.txt`
   – one answer block per prompt, blank line between.
2. Run the two commands above — charts update automatically.

### Optional: κ agreement

Fill `data/error_annotations.csv` with rater votes (`ok` / `drift`), then:

```bash
python scripts/compute_kappa.py
```

---

## Folder layout

```
semantic-drift-demo/
├─ data/        prompts & answers
├─ scripts/     *.py utilities
├─ images/      output charts
└─ requirements.txt
```

---

### Concept recap

* ΔS measures *how far* an answer strays from the prompt’s meaning.
* λ\_observe shows *how often* WFGY keeps that distance below the safe limit.

  > In our demo WFGY hits 100% — every answer stays on track.

Unzip the archive → push to GitHub → readers can rerun in Colab and reproduce the same numbers. That’s the entire experiment pipeline.

```

Just unzip one of the links into your `semantic-drift-demo/` folder, paste the README block above, and commit — you’re good to go! 🎯
```
