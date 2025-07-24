# Semantic‑Drift Demo

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
