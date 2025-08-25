# Vector Store — Global Fix Map
Make your store consistent, populated, and explainable.  
Use this when FAISS/Qdrant/Chroma/Elastic “works” but retrieval still feels wrong or inconsistent.

## What this page is
- A concise checklist to validate population, metrics, and read/write symmetry.
- Structural fixes for empty/fragmented stores and stale or misconfigured indices.
- Steps you can verify with ΔS curves and citation tables.

## When to use
- Answers look unrelated even though the store is “full”.
- First queries after boot return nothing or random snippets.
- Some facts never appear although indexed.
- Hybrid retrieval becomes worse than a single retriever.
- After a deploy, results change wildly with the same query.

## Open these first
- Why vectors ≠ meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Fragmented / partially empty collections: [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)
- End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Ordering after recall (keep it measurable): [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Why this snippet (trace schema): [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Visual pipeline & recovery path: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- Eval targets: [RAG Precision/Recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

## Fix in 60 seconds
1) **Probe ΔS**
   - Chart `ΔS(question, retrieved)` vs `k ∈ {5,10,20}`.  
   - Flat-high curve → index/metric/normalization mismatch or partial population.

2) **Population sanity**
   - Count vectors per collection and compare to docs/chunks.  
   - Ensure no silent failures in batch ingestion or concurrency during build.

3) **Read/write symmetry**
   - Same embedding model id on write and read.  
   - Same distance metric (cosine vs inner product) and dimensionality.  
   - If cosine, confirm unit normalization on both sides.

4) **Index configuration**
   - FAISS: confirm index type (IVF/HNSW/PQ), nprobe/efSearch, and that the trained index file is persisted + reloaded.  
   - Qdrant/Chroma/Elastic: verify exact metric flags, shard/replica consistency, warm-up finished.

5) **Rebuild once with explicit metadata**
   - Persist: model_id, dim, metric, normalizer, tokenizer, build_params.  
   - After rebuild, re-probe ΔS and store acceptance plots with traceability.

6) **Rank after recall**
   - If recall is good but ordering is noisy, add a light reranker from the playbook.  
   - Keep citation schema to audit the change.

## Copy-paste prompt
```

I uploaded TXT OS and the WFGY ProblemMap pages.

My vector store bug:

* symptom: \[brief]
* ΔS traces: vs k = {...}, current ΔS(question, retrieved)=..., anchor ΔS=...
* write: model=\[...], metric=\[cosine|ip], dim=\[...], norm=\[on|off], index=\[IVF|HNSW|PQ], params=\[...]
* read:  model=\[...], metric=\[...], dim=\[...], norm=\[...]
* population: vectors=\[count], docs=\[count], ingestion logs=\[summary]

Tell me:

1. what mismatch or population issue explains it,
2. which exact WFGY pages to open,
3. the minimal rebuild/rescore steps to push ΔS ≤ 0.45,
4. how to verify with ΔS-vs-k, precision/recall, and a snippet↔citation table.
   Use BBMC alignment if anchors are stable; add a reranker only after recall is fixed.

```

## Minimal checklist
- One embedding model per collection or store `model_id` with each vector.  
- Fix metric/normalization once and persist with the index.  
- Keep text pre-processing identical on write and read.  
- Validate `dim` and dtype; no truncation or hidden casts.  
- Log and compare vector count = sum(chunk count).  
- Disallow writes during index training; warm up after boot.  
- Snapshot + restore indexes atomically; avoid mixed versions.  
- Run fragmentation pattern if some facts never retrieve.

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 across paraphrases.  
- ΔS-vs-k descends then flattens, not flat-high.  
- Precision/recall meet your eval sheet; top-k is explainable by traceability.  
- λ stays convergent at retrieval after rebuild.  
- Same results across restarts with deterministic warm-up.

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
| 🧙‍♂️ Starter Village 🏡 | New here? Lost in symbols? Click here and let the wizard guide you through | [Start →](https://github.com/onestardao/WFGY/blob/main/StarterVillage/README.md) |

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
