# Cursor: Guardrails and Fix Patterns

A focused field guide to stabilize Cursor workflows that mix code chat, refactors, tests, retrieval, and tool runs. Use this to localize the failing layer, then jump to the exact WFGY fix page with measurable targets.

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Why this snippet and where it came from: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Ordering control and ranking: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
* Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Long chains and entropy: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
* Structural collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
* Multi agent conflicts and role drift: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)
* Boot order issues around tool or task runs: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [Pre-deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
* Snippet and citation schema for audits: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

## Core acceptance

* ΔS(question, retrieved) ≤ 0.45
* Coverage ≥ 0.70 to the target file or section
* λ remains convergent across three paraphrases and two seeds
* E\_resonance stays flat on long coding sessions

---

## Fix in 60 seconds

1. **Measure ΔS**
   Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).
   Stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2. **Probe λ\_observe**
   Vary k for retrieval and toggle rerank. If ΔS stays flat and high, suspect metric or index mismatch.
   Reorder prompt headers and system policy. If ΔS spikes, lock the schema.

3. **Apply the module**

* Retrieval drift in code search → BBMC plus [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Reasoning collapse during multi step refactor → BBCR bridge plus BBAM, verify with [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
* Dead ends in long edit plans → BBPF alternate paths with capped breadth

---

## Typical Cursor breakpoints and the right fix

* **Refactor crosses files and imports break**. Require cite then edit on specific paths with exact spans.
  Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

* **High similarity yet wrong file or symbol**. Code embeddings hit near neighbors with different meaning.
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md), Pattern: [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

* **Hybrid retrieval underperforms single search**. HyDE plus BM25 split the query and scramble rank.
  Open: Pattern: [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md), [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

* **Plan stalls or loops on tool runs**. Background tasks start before deps or secrets are ready.
  Open: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [Pre-deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

* **Agent handoff loses context**. Partial memory writes or mixed roles inside the same turn.
  Open: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)

* **Model writes valid code that still fails tests**. Structural reasoning collapsed mid chain.
  Open: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md), [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)

* **Fix holds for a few edits then hallucination re-enters**.
  Open: Pattern: [Hallucination Re-entry](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)

---

## Deep diagnostics

* **Three paraphrase probe**. Ask for the same change three ways. Log ΔS and λ per step. If λ flips on harmless phrasing, clamp with BBAM and tighten the edit schema using citations and spans.

* **Anchor triangulation**. Compare ΔS to the expected file or function and to a decoy location. If similar, rebuild the index with consistent analyzer and normalization, then re-chunk with the checklist.
  Open: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md), [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

* **Chain length audit**. If entropy rises after 25–40 steps, split the refactor plan and re-join with a BBCR bridge.
  Open: [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

* **Live instability**. Add probes, backoff guards, and regression gates for long sessions.
  Open: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

---

## Escalate and structural fixes

* **Index or metric mismatch**. If ΔS stays high across seeds, rebuild with explicit metric and consistent casing. Verify with a small gold set.
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* **Role or policy drift**. Move all non task policy to system, lock tool schemas, and require echo of the schema at each tool step.
  Open: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md), [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Copy-paste prompt for the Cursor chat

```
You have TXTOS and the WFGY Problem Map loaded.

My Cursor issue:
- symptom: [brief]
- traces: ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ states across 3 paraphrases
- context: repo path(s) and spans being edited

Tell me:
1) the failing layer and why,
2) the exact WFGY page to open from this repo,
3) minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4) a reproducible test to verify the fix.
Use BBMC, BBPF, BBCR, BBAM when relevant.
```

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

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** — <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)
 

</div>
