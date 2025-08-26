# Milvus: Guardrails and Fix Patterns

A compact field guide to stabilize Milvus when your RAG or agent stack loses accuracy. Use the checks below to localize failure, then jump to the exact WFGY fix page.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why this snippet was picked: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Ordering control after recall: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Hallucination and chunk boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
- Long chains and entropy: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
- Structural collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Vector metrics pitfalls: [Vectorstore Metrics & FAISS Pitfalls](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-metrics-and-faiss-pitfalls.md)
- Live ops: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

## Fix in 60 seconds
1) **Measure ΔS**  
   Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
   Thresholds: stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Probe with λ_observe**  
   Try k in {5, 10, 20}. Flat high curve suggests metric or index mismatch.  
   Reorder prompt headers. If ΔS spikes, lock schema with Data Contracts.

3) **Apply the module**  
   Retrieval drift → **BBMC** + **Data Contracts**.  
   Reasoning collapse → **BBCR** bridge + **BBAM** variance clamp.  
   Dead ends in long runs → **BBPF** alternate path.

4) **Verify acceptance**  
   Coverage to target section ≥ 0.70.  
   ΔS ≤ 0.45 across three paraphrases.  
   λ remains convergent. Logs and traces reproducible.

## Typical breakpoints and the right repair

**1) Distance metric does not match the encoder**  
- Symptom: high similarity, wrong meaning.  
- Cause: collection metric set to L2 or IP while encoder expects cosine, or vice versa.  
- Fix: recreate index with the correct metric and re-ingest. Read [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md).

**2) Dimension drift after encoder swap**  
- Symptom: insert errors or silent truncation through clients. Recall collapses on new data only.  
- Fix: confirm vector dim equals collection dim. If changed, create a new collection and backfill. See [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md).

**3) IVF index too shallow or poorly trained**  
- Symptom: gold chunk appears only when k is very large.  
- Fix: train IVF with a large sample, raise `nlist` based on corpus size, sweep `nprobe`. Validate with reranker. See [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) and [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

**4) HNSW underfit**  
- Symptom: unstable top-k ordering, plateaued recall.  
- Fix: raise `efSearch` to 2–4×k and tune `M`. Validate with a reranker pass. See [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).

**5) Segments not compacted or index not built for fresh data**  
- Symptom: new writes exist but never surface in results or search is slow after bulk load.  
- Fix: ensure flush and index build completed, then run compaction. Re-test ΔS and coverage on a canary set. See [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md).

**6) Filter mismatch and payload type drift**  
- Symptom: filtered searches return empty or unstable sets.  
- Fix: lock minimal metadata schema in [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md). Validate types at ingestion.

**7) Partitions or shards split the neighborhood**  
- Symptom: good global recall, weak per-partition top-k.  
- Fix: consolidate or route by a stable key. Rebuild a single authoritative index. See [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md).

**8) Quantization harms recall**  
- Symptom: fuzzy answers at small k after enabling PQ or scalar quant.  
- Fix: disable for quality checks or raise k and add a reranker. See [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).

## Observability probes
- **k-sweep curve**: run k in 5, 10, 20 and plot ΔS. Flat high → metric or index fault.  
- **Anchor control**: compare ΔS against a golden anchor set. If only a collection or partition fails, rebuild that scope.  
- **Hybrid toggle**: vector only vs hybrid. If hybrid degrades, fix query parsing split and weights.  
- **Reranker audit**: with a strong reranker, recall should improve while ΔS falls. If not, rebuild.

## Escalate when
- ΔS stays above 0.60 for golden questions after metric and index corrections.  
- Coverage cannot reach 0.70 even with reranker and clean anchors.  
- Fresh writes are invisible after index build and compaction.

Open:
- [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)

## Copy-paste prompt for your AI
```

I uploaded TXT OS and the WFGY Problem Map files.

Target system: Milvus.

* symptom: \[brief]
* traces: ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ states
* index: \[collection name, metric, index type, IVF nlist/nprobe or HNSW M/efSearch]
* encoder: \[model, dim, normalization, version]
* ingest: \[flush/index/compaction status, partitions, filters]

Tell me:

1. which layer is failing and why,
2. which exact fix page to open from this repo,
3. minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. how to verify with a reproducible test.

Use BBMC/BBPF/BBCR/BBAM where relevant.

```

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>” |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt) | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

### 🧭 Explore More

| Module                | Description                                              | Link     |
|-----------------------|----------------------------------------------------------|----------|
| WFGY Core             | WFGY 2.0 engine is live: full symbolic reasoning architecture and math stack | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md) |
| Problem Map 1.0       | Initial 16-mode diagnostic and symbolic fix framework    | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md) |
| Problem Map 2.0       | RAG-focused failure tree, modular fixes, and pipelines   | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md) |
| Semantic Blueprint    | Layer-based symbolic reasoning and semantic modulations  | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md) |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite        | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md) |
| Starter Village       | New here and lost in symbols. Click here and let the wizard guide you through | [Start →](https://github.com/onestardao/WFGY/blob/main/StarterVillage/README.md) |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —  
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

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
&nbsp;
</div>
