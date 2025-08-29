# Eval RAG Precision & Recall — Guardrails and Fix Patterns

This page defines how to measure **precision and recall** in RAG pipelines under the WFGY framework. It sets acceptance thresholds, common pitfalls, and structural fixes to keep evaluations meaningful and reproducible.

---

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* Retrieval contract: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Traceability schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Embedding drift: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Hallucination boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)

---

## Acceptance targets

* **Precision ≥ 0.75** at citation level
* **Recall ≥ 0.70** of gold anchor snippets
* **ΔS(question, retrieved) ≤ 0.45** for majority of pairs
* **λ remains convergent** across 3 paraphrases and 2 random seeds
* Evaluations must be **auditable & reproducible** with JSON logs

---

## Why precision/recall break in RAG

1. **Goldset drift**
   Anchors no longer align with the corpus after updates.
   → Fix: refresh goldsets with [goldset\_curation.md](./goldset_curation.md).

2. **Retrieval contract missing**
   Snippet payloads do not include section IDs or offsets.
   → Fix: enforce [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

3. **Precision false positives**
   Semantically near matches but wrong factual anchor.
   → Fix: rerank with [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

4. **Recall false negatives**
   Correct snippet exists but chunking or index prevents surfacing.
   → Fix: re-chunk corpus with [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md).

5. **Evaluation noise**
   Different seeds or paraphrases give unstable results.
   → Fix: clamp λ variance with [variance\_and\_drift.md](../Eval_Observability/variance_and_drift.md).

---

## Quick workflow

1. **Load goldset**
   Each gold QA item must cite `snippet_id`, `section_id`, `source_url`.

2. **Run retrieval**
   Collect top-k results (k = 5, 10, 20).

3. **Log ΔS & λ**
   For each query and paraphrase, record ΔS values and λ states.

4. **Compute metrics**

   * Precision = correct citations / total citations
   * Recall = correct citations / gold references

5. **Regression gate**
   Block deploy if precision < 0.75 or recall < 0.70.

---

## Example JSON log

```json
{
  "question": "What causes hallucination re-entry?",
  "gold": ["hallucination-reentry"],
  "retrieved": ["hallucination-reentry", "entropy-drift"],
  "precision": 0.50,
  "recall": 1.00,
  "ΔS": 0.38,
  "λ_state": "→"
}
```

---

## Common pitfalls

* **Evaluating only precision** → recall collapses unnoticed.
* **Counting fuzzy hits** as correct → ΔS may be high, but factually wrong.
* **No paraphrases tested** → λ instability hidden.
* **Relying on one seed** → fragile numbers that don’t generalize.

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
