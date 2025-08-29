# Goldset Curation — Guardrails and Fix Patterns

A curated gold set is the foundation for evaluation stability. Without strict contracts on the gold data, all eval metrics become meaningless. This page defines how to build, audit, and maintain gold QA sets that align with WFGY acceptance targets.

---

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* Traceability schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Payload fences: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Chunk coverage: [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)
* Semantic drift control: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

---

## Acceptance targets for curated goldsets

* **Coverage ≥ 0.80** of target sections
* **ΔS(question, gold anchor) ≤ 0.35**
* **λ state stable** across 3 paraphrases and 2 seeds
* **No overlap**: each gold item maps to exactly one snippet and section

---

## Curation process

### 1. Select domains

* Identify domains relevant to the pipeline (finance, law, product docs).
* Ensure gold questions are drawn from actual user tasks.

### 2. Define anchors

* Each QA item must cite a **section ID** and **expected\_doc**.
* Anchors must reference stable problem map sections, not ephemeral text.

Example:

```json
{
  "id": "Q_0007",
  "question": "What causes hallucination re-entry after correction?",
  "answer_ref": "PM:patterns/pattern_hallucination_reentry",
  "expected_doc": "ProblemMap/patterns/pattern_hallucination_reentry.md",
  "section_id": "hallucination-reentry"
}
```

### 3. Add paraphrases

* Minimum 3 per question.
* Probe λ stability under phrasing variance.

```json
{
  "id": "Q_0007_P1",
  "question": "Why do hallucinations return after being corrected once?"
}
```

### 4. Validate citations

* Each gold item must include an **exact citation offset**.
* If offsets drift, the goldset is invalid until refreshed.

### 5. Apply regression gate

* No gold item should produce ΔS > 0.45 in baseline runs.
* Violations are logged and flagged for refresh.

---

## Common pitfalls and fixes

* **Gold overlaps across sections**
  → Fix: merge or re-scope questions, ensure one-to-one mapping.

* **Anchors point to unstable docs**
  → Fix: only link to long-lived WFGY ProblemMap pages.

* **Paraphrases flip λ**
  → Fix: clamp with BBAM variance controls and revalidate.

* **Coverage below 0.80**
  → Fix: expand questions until goldset covers every critical node.

---

## Quick workflow

1. Draft 20–30 candidate QA items.
2. Add 3 paraphrases each.
3. Link every item to an anchor section.
4. Run through `eval_harness.md`.
5. Drop items that fail regression gate.
6. Store final goldset in `datasets/gold/`.

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
