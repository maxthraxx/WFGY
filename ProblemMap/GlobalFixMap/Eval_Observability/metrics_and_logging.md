# Eval Observability — Metrics and Logging

A baseline schema and checklist for logging semantic metrics (ΔS, λ, coverage, E_resonance) during live runs.  
Use this page to enforce consistent telemetry so that offline eval and online observability align.

---

## Why log metrics?

- **Drift detection**: High ΔS or divergent λ states catch retrieval/logic errors early.  
- **Comparability**: Same schema across providers, stores, and orchestration layers.  
- **Debug loops**: Logged traces accelerate reproduction and diagnosis.  
- **Regression guards**: Simple thresholds protect pipelines before release.

---

## Core metrics to capture

| Metric | Definition | Thresholds |
|--------|------------|------------|
| ΔS(question, retrieved) | Semantic distance between query and retrieved snippet | Stable ≤ 0.45, Transitional 0.45–0.60, Risk ≥ 0.60 |
| Coverage | Fraction of gold/target section retrieved | ≥ 0.70 |
| λ_observe | State of reasoning flow (→ convergent, ← divergent, <> transitional, × collapse) | Must stay convergent across 3 paraphrases |
| E_resonance | Long-window entropy of reasoning steps | Should remain flat without spikes |

---

## Logging schema (JSON example)

```json
{
  "trace_id": "uuid",
  "timestamp": "2025-08-29T12:34:56Z",
  "question": "...",
  "retrieved": [
    {
      "snippet_id": "s1",
      "section": "intro",
      "source": "docA",
      "offsets": [120, 160],
      "ΔS": 0.42
    }
  ],
  "ΔS_overall": 0.44,
  "coverage": 0.72,
  "λ_state": "→",
  "E_resonance": 0.03,
  "index_hash": "abc123",
  "dedupe_key": "sha256(...)" 
}
````

---

## Quick probes

* **ΔS probe**: Recompute ΔS on each retrieval call. Alert if ≥ 0.60.
* **λ probe**: Run three paraphrases per eval batch, log λ\_state sequence.
* **Coverage probe**: Compare retrieved sections against gold or expected anchors.
* **E\_resonance probe**: Smooth entropy over 50–100 steps, alert if spike > 2× baseline.

---

## Storage tips

* Write logs to append-only store (e.g., KV or time-series DB).
* Deduplicate with `dedupe_key = sha256(question + index_hash + snippet_id)`.
* Keep 30–90 days rolling window for regression analysis.

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
