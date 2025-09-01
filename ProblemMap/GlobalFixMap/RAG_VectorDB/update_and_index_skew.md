# Update and Index Skew — Guardrails and Fix Pattern

Use this page when **recall flips or citations drift after a data or model update**.  
Skew appears when writers and readers see different corpus revisions, or when the index was rebuilt with changed params without a cutover plan.

---

## Open these first

- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- Retrieval knobs: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Vector store fragmentation: [vectorstore_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/vectorstore_fragmentation.md)  
- Metric mismatch: [metric_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/metric_mismatch.md)  
- Normalization and scaling: [normalization_and_scaling.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/normalization_and_scaling.md)  
- Tokenization and casing: [tokenization_and_casing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/tokenization_and_casing.md)  
- Chunking to embedding contract: [chunking_to_embedding_contract.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/chunking_to_embedding_contract.md)  

---

## Core acceptance

- Single **INDEX_HASH** is identical for writer, retriever, reranker, and LLM side prompts.  
- ΔS(question, retrieved) ≤ 0.45 on 3 paraphrases and 2 seeds after the update.  
- Coverage ≥ 0.70 to the target section, stable across shards and regions.  
- λ remains convergent during the cutover window, no flip states at header reorder.

---

## Symptoms → likely cause → open this

- Results differ between two identical queries minutes apart  
  → mixed corpus revisions or warm readers on stale index  
  → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- Top-k looks similar in distance yet meaning is off after upgrade  
  → metric or normalization changed during rebuild  
  → [metric_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/metric_mismatch.md), [normalization_and_scaling.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/normalization_and_scaling.md)

- Some shards return old docs, others new ones  
  → partial index redeploy or cache warmup skew  
  → [vectorstore_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/vectorstore_fragmentation.md)

- After model switch, recall falls only on certain languages or code blocks  
  → tokenizer or casing schema diverged  
  → [tokenization_and_casing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/tokenization_and_casing.md)

- Large jump in ΔS on long windows, citations no longer align  
  → chunk schema changed but old vectors remain  
  → [chunking_to_embedding_contract.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/chunking_to_embedding_contract.md)

---

## Fix in 60 seconds

1) **Pin the contract**  
   Compute `INDEX_HASH = sha256(model_id + tokenizer_ver + chunk_schema + metric + dim + store_params + corpus_rev)`.  
   Log it on writer, retriever, reranker, and in the LLM prompt header.

2) **Shadow read**  
   Run a gold set against current index and a rebuilt index in parallel.  
   Alert if ΔS variance > 0.05 or coverage drops below 0.70.

3) **Freeze and rebuild**  
   Stop writes. Re-embed and rebuild offline with explicit `dim`, `metric`, and `normalization`.  
   Verify tokenizer and casing are identical to the previous contract.

4) **Cutover with warmup**  
   Warm the new index. Switch read traffic via percentage ramp.  
   Abort if λ flips or ΔS exceeds 0.60 on any guardrail probe.

---

## Minimal checks you must script

- **Contract echo**  
  Every query path must log `INDEX_HASH`, `MODEL_ID`, `TOKENIZER_VER`, `CHUNK_SCHEMA_VER`.

- **Shard parity probe**  
  Run the same 25 queries to each shard or region.  
  Flag if Jaccard(top-k) < 0.6 against the reference shard.

- **Cache invalidation**  
  Clear reranker and query embedding caches when `INDEX_HASH` changes.

- **Reader staleness**  
  Reject queries if `reader_index_hash != router_index_hash`. Fail fast, do not serve stale.

---

## Common gotchas

- Silent analyzer change in a search backend re-tokenizes text while vectors are unchanged.  
- HNSW or IVF params differ between shards, causing order instability at k=10 but not at k=3.  
- APM dashboards show healthy ingestion yet the retriever reads from a lagging replica.  
- Reranker model upgraded without re-baselining acceptance targets.  
- Partial re-embed of only new docs creates a semantic seam at time T.

---

## Verification

- Gold set of 100 questions, 3 paraphrases each.  
- Require ΔS ≤ 0.45 and coverage ≥ 0.70 on both old and new indexes before cutover.  
- After cutover, repeat on two seeds. If λ remains convergent and ΔS does not spike, close the change.

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
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations   | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md) |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite         | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md) |

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
