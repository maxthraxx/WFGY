# Elasticsearch: Guardrails and Fix Patterns

A compact field guide to stabilize Elasticsearch vector search when your RAG or agent stack loses accuracy. Use this to localize the failing layer and jump to the exact WFGY fix page.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why this snippet and trace schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Ordering after recall: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Embedding versus meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Chunk boundaries and illusions: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
- Long chains and drift checks: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
- Structural collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Vector metrics pitfalls: [Vectorstore Metrics & FAISS Pitfalls](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-metrics-and-faiss-pitfalls.md)
- Fragmented stores: [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)
- Hybrid query split: [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)
- Ops live checks: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

## Fix in 60 seconds
1) **Measure ΔS**  
   Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
   Thresholds: stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Probe with λ_observe**  
   Sweep k in {5, 10, 20}. If ΔS is flat high, suspect metric, mapping, or index mismatch.  
   Reorder prompt headers. If ΔS spikes, lock schema with Data Contracts.

3) **Apply the module**  
   Retrieval drift → **BBMC** + **Data Contracts**.  
   Reasoning collapse → **BBCR** bridge + **BBAM** variance clamp.  
   Dead ends in long runs → **BBPF** alternate path.

4) **Verify acceptance**  
   Coverage ≥ 0.70 to target section.  
   ΔS ≤ 0.45 on three paraphrases.  
   λ remains convergent. Traces reproducible.

## Elasticsearch breakpoints and the right repair

### 1) `dense_vector` mapping mismatch
**Symptoms**: insert errors, silent truncation, or chaotic top-k for new docs only.  
**Why**: vector `dims` do not match encoder, or field not indexed for KNN.  
**Fix**: set `type: dense_vector`, correct `dims`, and `index: true` for KNN. Re-index changed spans. See [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

### 2) Distance metric and normalization
**Symptoms**: high similarity yet wrong meaning; ordering flips across runs.  
**Why**: using `similarity: l2_norm` with cosine-trained embeddings, or `dot_product` without unit-norm vectors.  
**Fix**: align metric to the encoder; normalize for cosine/dot as policy. If you switch, rebuild the index. See [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) and [Vectorstore Metrics & FAISS Pitfalls](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-metrics-and-faiss-pitfalls.md).

### 3) HNSW underfit and candidate window
**Symptoms**: gold chunk appears only at very large k.  
**Why**: small `m` or `ef_construction`, and `num_candidates` too low at query time.  
**Fix**: tune `m`, raise `ef_construction`, then sweep `num_candidates` at query. Validate with a reranker. See [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) and [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

### 4) `knn` vs `script_score` confusion
**Symptoms**: inconsistent scores between approximate `knn` and exact script scoring; hybrids regress.  
**Fix**: use exact `script_score` on a canary set to bound max recall, then tune `knn` to approach it. Keep one scoring policy in production. Map to [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

### 5) Filters with KNN
**Symptoms**: empty results when adding filters; massive latency spikes.  
**Why**: pre-filter not supported in your version or filter path not indexed.  
**Fix**: ensure filtered fields are indexed and typed, test post-filter rerank, and document the path in the contract. See [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

### 6) Analyzer drift for hybrid BM25 + vector
**Symptoms**: hybrid performs worse than either branch alone.  
**Why**: default analyzers, stopwords, or stemming distort lexical scores.  
**Fix**: lock analyzers per field; normalize hybrid weights; fuse post-retrieval and rerank. See [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) and [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

### 7) Shards, replicas, and refresh
**Symptoms**: fresh writes never appear; nodes return different sets.  
**Fix**: confirm refresh policy, replica sync, and routing. Add a semantic boot fence before first prod call. See [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) and [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md).

### 8) Alias routing and multi-index fragmentation
**Symptoms**: global recall ok but weak per-alias top-k.  
**Why**: many tiny indices split the neighborhood; wrong read/write alias.  
**Fix**: consolidate to an authoritative index with a facet, fix aliases, rebuild, then rerank. See [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md).

### 9) Upsert hygiene
**Symptoms**: duplicates, stale docs, toggling answers.  
**Fix**: deterministic IDs, `doc_sha` in metadata, idempotent loaders, periodic dedupe. Validate with golden queries. See [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

## Observability probes
- **k-sweep curve**: run k in 5, 10, 20. Flat high ΔS → metric, mapping, or index fault.  
- **Exact vs approx**: compare `script_score` exact against `knn`. Large gap → retune HNSW and `num_candidates`.  
- **Hybrid toggle**: vector only vs hybrid. If hybrid regresses, repair analyzers and fusion weights.  
- **Reranker audit**: strong reranker should reduce ΔS while recall rises. If not, rebuild.

## Escalate when
- ΔS stays ≥ 0.60 on golden questions after metric, mapping, and HNSW fixes.  
- Coverage cannot reach 0.70 even with reranker and anchors.  
- Writes appear in logs but remain invisible across shards or replicas.

Open:
- [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)

## Copy-paste prompt for your AI
```

I uploaded TXT OS and the WFGY Problem Map files.

Target system: Elasticsearch.

* symptom: \[brief]
* traces: ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ states
* mapping: \[field, dims, index=true, similarity=cosine|dot\_product|l2\_norm]
* knn: \[k, num\_candidates, hnsw m, ef\_construction]
* exact: \[script\_score policy if used]
* hybrid: \[match/bm25 fields, analyzers, weights]
* ingest: \[ids, doc\_sha, upsert policy]
* routing: \[index/alias, shards, replicas, refresh]

Tell me:

1. which layer is failing and why,
2. which exact fix page to open from this repo,
3. minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. how to verify with a reproducible test.

Use BBMC/BBPF/BBCR/BBAM when relevant.

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
| Benchmark vs GPT-5    | Stress test with full WFGY reasoning suite              | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md) |
| Starter Village       | New here. Start with a guided tour                      | [Start →](https://github.com/onestardao/WFGY/blob/main/StarterVillage/README.md) |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)**  
> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is live. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

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

