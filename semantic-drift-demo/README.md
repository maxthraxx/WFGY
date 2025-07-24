# Semantic‑Drift Demo

30 multi‑step prompts to measure how much an answer drifts off topic.  
We compare plain LLM output (**Baseline**) with **WFGY + Drunk Mode**.

**Metrics**

| Metric | Meaning | Good? |
|--------|---------|-------|
| ΔS (drift score) | Prompt‑to‑answer distance. 0 = perfect. | lower |
| λ_observe | % of cases where ΔS < threshold (default 0.4). | higher |

**Plain English**

* ΔS bar — green (WFGY) lower ⇒ answers stay on track.  
* λ bar  — green hits 100 % ⇒ WFGY wins every prompt.

![ΔS](images/drift_comparison.png)  
![λ](images/lambda_pass.png)

---

## Quick Start

```bash
pip install -r requirements.txt          # sklearn, pandas, matplotlib, statsmodels
python scripts/run_eval.py               # → data/metrics.csv
python scripts/plot_results.py           # → images/ updated charts
