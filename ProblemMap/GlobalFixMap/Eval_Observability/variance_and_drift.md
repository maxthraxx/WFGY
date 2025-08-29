# Eval Observability — Variance and Drift

Variance and drift checks detect when evaluation scores are **unstable across runs** or when **semantic meaning slowly shifts** without clear boundary failures.  
These probes prevent "false confidence" in benchmarks by catching hidden instability.

---

## Why variance and drift matter

- **Variance**: Scores fluctuate heavily depending on seed, paraphrase, or retriever order. Averages hide the volatility.  
- **Drift**: Performance declines slowly across sessions, data refreshes, or version bumps. Looks fine short-term but collapses long-term.  
- **Silent regressions**: Systems pass local tests but fail in production due to unmonitored entropy rise.  

---

## Acceptance targets

- **Variance (σ/μ)** ≤ 0.15 across 3 seeds and 3 paraphrases.  
- **Drift slope**: Δscore per batch ≤ 0.02 absolute over 5+ eval windows.  
- **No monotonic downward slope** longer than 3 consecutive windows.  
- **Drift alerts** fire if ΔS average increases ≥ 0.10 compared to gold anchors.

---

## Detection workflow

1. **Collect runs across seeds**  
   - At least 3 seeds, 3 paraphrases.  
   - Log ΔS, λ, coverage, citations.  

2. **Compute variance**  
   - Calculate σ/μ for each metric.  
   - High variance = unstable eval → rerun with schema locks.  

3. **Track drift over time**  
   - Compare eval batch N vs N-1.  
   - Plot moving average.  
   - Alert if slope exceeds tolerance.  

4. **Root-cause analysis**  
   - If variance high → check retriever metrics, random seeding, rerankers.  
   - If drift detected → audit embeddings, re-chunk, verify data refresh.  

---

## Common pitfalls

- **Single-run evals**: Hides high variance. Always run multi-seed.  
- **Averages without spread**: Mean looks fine, variance reveals collapse.  
- **Ignoring slow drift**: Short tests OK, but 1–2 weeks later accuracy dies.  
- **Cross-store drift**: One vector DB stable, another drifts. Must track both.  

---

## Example reporting schema

```json
{
  "metric": "ΔS",
  "seed_runs": [0.38, 0.42, 0.44],
  "variance_ratio": 0.14,
  "drift_slope": +0.03,
  "alert": true
}
````

---

## Fix modules to open

* **Retriever instability** → [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
* **Embedding mismatch** → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* **Fragmentation drift** → [vectorstore-fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-fragmentation.md)
* **Prompt instability** → [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)

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

