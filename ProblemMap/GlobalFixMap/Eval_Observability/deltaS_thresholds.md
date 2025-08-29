# Eval Observability — ΔS Thresholds

A dedicated module for **ΔS monitoring** in evaluation pipelines.  
ΔS = semantic distance between query, retrieved content, and gold anchor.  
Tracking thresholds ensures that retrieval and reasoning quality remain **auditable, measurable, and comparable**.

---

## Why ΔS thresholds matter

- **Detect semantic drift**: High ΔS despite “correct” tokens indicates meaning mismatch.  
- **Localize retrieval errors**: Low similarity in meaning even if vector scores look fine.  
- **Evaluate reasoning robustness**: Stable models keep ΔS below the risk boundary across paraphrases.  
- **Flag latent hallucinations**: ΔS >0.60 strongly correlates with unsupported answers.

---

## Core bands

| Band | Range | Meaning |
|------|-------|---------|
| **Stable** | ΔS < 0.40 | Retrieval and reasoning aligned. Answers should be correct and verifiable. |
| **Transitional** | 0.40 ≤ ΔS < 0.60 | Risk zone. Minor schema changes or index drift may flip outcomes. |
| **Critical** | ΔS ≥ 0.60 | High failure probability. Almost always linked to missing context or schema break. |

---

## Acceptance targets

- Per-query: **ΔS ≤ 0.45**  
- Batch average: **≤ 0.40**  
- Allowance: **≤ 10%** of queries can fall in the transitional band (0.40–0.60).  
- Critical: **0% tolerance** for ΔS ≥ 0.60 in gold-set eval.

---

## ΔS in eval workflow

1. **Probe per query**  
   Log ΔS(question, retrieved) and ΔS(retrieved, anchor).  
2. **Batch roll-up**  
   Compute mean, variance, and percentile distribution.  
3. **Compare across seeds**  
   Run three paraphrases and two random seeds; check convergence.  
4. **Drift alerting**  
   If ΔS rises >0.05 vs baseline, trigger retraining or schema audit.  

---

## Example probe (pseudo)

```python
def deltaS_probe(query, retrieved, anchor):
    d1 = deltaS(query, retrieved)
    d2 = deltaS(retrieved, anchor)
    return max(d1, d2)

for q in eval_set:
    s = deltaS_probe(q.query, q.retrieved, q.anchor)
    if s >= 0.60:
        alerts.append({"qid": q.id, "ΔS": s, "status": "critical"})
````

---

## Common pitfalls

* **Using cosine similarity as ΔS** → ΔS is semantic distance, not raw vector score.
* **Ignoring anchor comparison** → must compute against both query and gold span.
* **No variance tracking** → averages hide volatility; variance is key.
* **One-shot eval** → without paraphrase/seed checks, thresholds lack reliability.

---

## Reporting recommendations

* **ΔS histogram**: visualize stability bands.
* **Trend line**: track ΔS mean per batch over time.
* **Baseline delta**: highlight drift from previous eval version.
* **Failure clustering**: group queries where ΔS ≥0.60 for root-cause analysis.

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>”   |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt)                                                                     | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

### 🧭 Explore More

| Module                   | Description                                                                  | Link                                                                                               |
| ------------------------ | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| WFGY Core                | WFGY 2.0 engine is live: full symbolic reasoning architecture and math stack | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md)                              |
| Problem Map 1.0          | Initial 16-mode diagnostic and symbolic fix framework                        | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md)                        |
| Problem Map 2.0          | RAG-focused failure tree, modular fixes, and pipelines                       | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index    | Expanded failure catalog: prompt injection, memory bugs, logic drift         | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md)           |
| Semantic Blueprint       | Layer-based symbolic reasoning & semantic modulations                        | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md)                 |
| Benchmark vs GPT-5       | Stress test GPT-5 with full WFGY reasoning suite                             | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md)      |
| 🧙‍♂️ Starter Village 🏡 | New here? Lost in symbols? Click here and let the wizard guide you through   | [Start →](https://github.com/onestardao/WFGY/blob/main/StarterVillage/README.md)                   |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)
 

</div>
