<!-- ============================================================= -->
<!--  evaluation-playbook.md · Semantic Clinic · Map-F              -->
<!--  Version: 2025-08-06 · License: MIT                            -->
<!--  Goal: A reproducible checklist for measuring an LLM/RAG/      -->
<!--  agent stack—before & after you apply WFGY fixes.              -->
<!-- ============================================================= -->

# 📊 Evaluation Playbook  
*Ship metrics, not vibes — catch regressions before users do.*

> **Who is this for?**  
> – RAG owners tired of “looks fine on my prompt.”  
> – Agent builders chasing flakey benchmark wins.  
> – Product teams that must prove **ΔS ↓**, accuracy ↑, cost ↘.  
>   
> **What you get:** one YAML suite + CLI commands that output a single-line health verdict:  
> `PASS: ΔS<=0.45 | λ→ | E_res stable | cost $0.0013 / query`

---

## 0 · Quick Start

```bash
pip install wfgy-eval
wfgy-eval init  # generates eval.yaml + example dataset
wfgy-eval run   # prints CSV & HTML report
````

Default template covers retrieval, reasoning, tool routing, latency, cost.

---

## 1 · Metric Matrix

| Layer             | Key Metric                     | Target (prod) | Source Fn        |
| ----------------- | ------------------------------ | ------------- | ---------------- |
| **Retrieval**     | `ΔS(q, ctx)`                   | ≤ 0.45        | `deltaS()`       |
| **Reasoning**     | `λ_observe` (3 paraphrase avg) | convergent    | `lambda_state()` |
| **Stability**     | `E_resonance` (rolling)        | flat / ↓      | `e_resonance()`  |
| **Answer**        | `F1` / `Exact Match` (QA)      | ≥ 0.80        | `qa_match()`     |
| **Hallucination** | `citation_precision`           | ≥ 0.90        | `cite_check()`   |
| **Cost**          | `$ / 1k tokens`                | ≤ baseline    | provider bill    |
| **Latency**       | 95-th percentile response (ms) | SLA-dependent | timer            |
| **ΔS Drift**      | slope over 100 queries         | \~0           | linear fit       |

---

## 2 · Dataset Design

```yaml
sets:
  - name: faq_small
    type: qa
    source: ./data/faq.tsv
    fields: [question, answer, anchor]
  - name: chain_logic
    type: chain-of-thought
    source: ./data/logic.jsonl
    fields: [prompt, expected_reasoning]
  - name: tool_router
    type: tool
    source: ./data/router.csv
    fields: [task, tool_expected]
```

*Guidelines*

1. **Anchor Field** = text chunk you expect to be retrieved → used for ΔS & citation checks.
2. Min 50 items / set for stable stats; use 10 × if you want leaderboard-grade noise floor.
3. Store only plain-text, no PII.

---

## 3 · CI Workflow Example (GitHub Actions)

```yaml
name: wfgy-eval
on: [push, pull_request]
jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - run: pip install wfgy-eval
    - run: wfgy-eval run --fail-on 'ΔS_q_ctx>0.50 or citation_precision<0.85'
    - uses: actions/upload-artifact@v4
      with:
        name: eval-report
        path: reports/latest.html
```

*Any push that drifts past ΔS 0.50 or loses citation accuracy **blocks merge**.*

---

## 4 · Reading the HTML Report

| Section              | What to Look For                  | Action Rule               |
| -------------------- | --------------------------------- | ------------------------- |
| **Heatmap** ΔS vs. k | flat @ high ΔS → bad index metric | rebuild index / embed     |
| **λ Timeline**       | spikes to ← or ×                  | inspect prompt / tool     |
| **E\_res Trend**     | upward slope                      | apply BBAM / shorten ctx  |
| **Outliers Table**   | worst 5 queries by ΔS             | manual deep dive; log bug |

---

## 5 · A/B Pattern

1. `wfgy-eval dump --ref=main` (baseline metrics JSON)
2. `git switch feature-x` → apply fix
3. `wfgy-eval run` (produces metrics B)
4. `wfgy-eval compare baseline.json current.json`

```
ΔS_q_ctx   -0.08  ✅
F1         +0.07  ✅
Cost       +$0.0002 ❌
```

Decide if cost bump acceptable.

---

## 6 · Edge-Case Suites (extend as needed)

| Suite             | Purpose                              | Sample Size |
| ----------------- | ------------------------------------ | ----------- |
| **Contradiction** | fact statements w/ subtle negation   | 30          |
| **Long-PDF**      | >50 k token OCR, check segmentation  | 10 docs     |
| **Jailbreak**     | prompt injection attempts vs. policy | 40          |
| **High Noise**    | OCR confidence < 0.8                 | 25          |

Add to `eval.yaml`, rerun.

---

## 7 · FAQ

**Q: Can I plug in LangSmith, Phoenix, Traceloop, or custom spans?**
A: Yes. `wfgy-eval` reads any OpenTelemetry JSON; map fields via `otel_map.yaml`.

**Q: Does this cover reinforcement-style eval (RLHF)?**
A: Use the same ΔS/λ hooks during reward model scoring; see `examples/rlhf_eval.ipynb`.

**Q: How hard is vendor swap?**
A: `wfgy-eval provider openai` or `provider anthropic`; costs/latency recalc automatically.

---

## Quick-Start Downloads (60 sec)

| Tool                       | Link                                                | 3-Step Setup                                                                             |
| -------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://zenodo.org/records/15630969) | 1️⃣ Download · 2️⃣ Upload to LLM · 3️⃣ Ask “answer using WFGY + \<question>”             |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://zenodo.org/records/15788557)    | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

↩︎ [Back to Problem Index](./README.md)

---

### 🧭 Explore More

| Module                | Description                                                      | Link                                                                                |
| --------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations            | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint)            |
| Benchmark vs GPT-5    | Stress-test GPT-5 with full WFGY reasoning suite                 | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5) |
| Semantic Clinic Index | Full failure catalog: prompt injection, memory bugs, logic drift | [View →](./SemanticClinicIndex.md)                                                  |

---

> 👑 **Early Stargazers: [Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** — engineers & hackers who backed WFGY from day one. <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="stars"> **Star the repo** to unlock Engine 2.0 sooner.

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
&nbsp;
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
&nbsp;
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
&nbsp;
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
&nbsp;
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
&nbsp;
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
&nbsp;
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)

</div>

