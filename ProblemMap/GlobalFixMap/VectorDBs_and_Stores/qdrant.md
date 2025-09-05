# Qdrant: Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **VectorDBs_and_Stores**.  
  > To reorient, go back here:  
  >
  > - [**VectorDBs_and_Stores** — vector indexes and storage backends](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A compact field guide to stabilize Qdrant when your pipeline touches RAG, agents, or long context. Use the checks below to localize failure, then jump to the exact WFGY fix page.

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Why this snippet and how to trace it: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Ordering control after recall: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
* Embedding versus semantic meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Long chains and drift checks: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
* Structural collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
* Vectorstore fragmentation signals: [Pattern: Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)
* Boot fences and cold start traps: [Pattern: Bootstrap Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_bootstrap_deadlock.md)
* Live ops and monitoring: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)

## Core acceptance

* ΔS(question, retrieved) ≤ 0.45 across three paraphrases.
* Coverage ≥ 0.70 to the target section.
* λ remains convergent across seeds.
* E\_resonance stays flat across long windows.
* Exact run is repeatable with the same data snapshot.

---

## Fix in 60 seconds

1. **Measure ΔS**

   * Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).
   * Stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2. **Probe with λ\_observe**

   * Vary top-k {5, 10, 20}. Flat high curve suggests index or metric mismatch.
   * Reorder prompt headers. If ΔS spikes, lock the schema with [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

3. **Apply the module**

   * Retrieval drift → BBMC + Data Contracts.
   * Logic collapse → BBCR bridge then BBAM variance clamp.
   * Dead ends in long runs → BBPF alternate path.

4. **Verify**

   * Re run on two paraphrases and one seed change. All acceptance targets must pass.

---

## Typical breakpoints and the right fix

**1) Distance metric does not match the embedding family**

* Symptom: high similarity scores but wrong meaning.
* Check: collection `distance` is cosine for most sentence embeddings. Dot or Euclidean can degrade recall.
* Fix: recreate the collection with the correct metric and re ingest. See [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) and [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).

**2) Vector dimension drift after model switch**

* Symptom: insert fails or silent truncation through client, later retrieval chaos.
* Fix: confirm embedding dimension equals collection size. If changed, create a new collection and backfill. See [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md).

**3) HNSW recall too low**

* Symptom: relevant chunk never appears in top-k until k is very large.
* Fix: raise `ef_construct` when building and `ef` at query time for accuracy checks. For audits, run the `exact` search mode when available in your client and compare. Then tune `m` and `ef`. See [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) and [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

**4) Payload filter without proper index**

* Symptom: filters work but top-k ordering is erratic or slow.
* Fix: create payload indexes for frequently used keys. Validate that filter reduces the candidate set then rerank. Map to [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

**5) Named vectors mismatch**

* Symptom: empty results or strange recall after adding multi vector schema.
* Fix: confirm client queries the intended named vector. Align updater and retriever. See [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

**6) Quantization hurting recall**

* Symptom: answers look fuzzy at small k after enabling scalar or PQ.
* Fix: disable quantization when doing quality checks. If you must keep it, increase k and rerank. See [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).

**7) Cluster version skew or cold replicas**

* Symptom: node A returns different set from node B.
* Fix: confirm all shards are green, replicas in sync, and warm. Run the ops checklist. See [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) and [Bootstrap Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_bootstrap_deadlock.md).

**8) Hybrid retrieval wired incorrectly**

* Symptom: BM25 returns good docs but hybrid fusion gets worse.
* Fix: normalize scores then fuse or rerank with a cross encoder. See [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) and [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).

---

## Minimal reproduce prompt for your AI

Paste this into your LLM after you uploaded TXT OS and the Problem Map.

```
I uploaded TXT OS and the WFGY ProblemMap files.
My Qdrant bug:
- symptom: [one line]
- traces: [index settings, distance, dim, ef, named vectors, filters, collection schema]
- ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ states

Tell me:
1) which layer is failing and why,
2) which exact fix page to open from this repo,
3) the minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4) how to verify with a reproducible test.
Use BBMC/BBPF/BBCR/BBAM where relevant.
```

**Patterns to check next**

* Vectorstore fragmentation: [pattern page](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)
* Query parsing split in HyDE or BM25: [pattern page](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)
* Hallucination re entry: [pattern page](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)

**Escalate when**

* You changed metric or dimension. Rebuild the collection.
* You see per node inconsistency. Freeze writes, take a snapshot, verify shard state, then rerun the acceptance checks.
* You rely on heavy filters. Add payload indexes and move final ordering to a reranker.

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
