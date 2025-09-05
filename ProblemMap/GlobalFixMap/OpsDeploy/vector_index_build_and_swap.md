# Vector Index — Build, Validate, and Atomic Swap

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **OpsDeploy**.  
  > To reorient, go back here:  
  >
  > - [**OpsDeploy** — operations automation and deployment pipelines](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A zero-downtime pattern to rebuild your vector index offline, prove it’s correct, then cut traffic over with a single reversible pointer. Works with FAISS, Milvus, Weaviate, Qdrant, pgvector, Redis, Chroma, Vespa, Typesense, and more.

---

## Open these first
- RAG map and recovery: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- Retrieval knobs end-to-end: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why this snippet (schema): [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Embedding vs meaning: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Fragmentation failure mode: [pattern_vectorstore_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)
- Metric mismatch & normalization: [metric_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Embeddings/metric_mismatch.md), [normalization_and_scaling.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Embeddings/normalization_and_scaling.md)

---

## When to use
- You change **embedding model**, **dimension**, **normalization**, or **distance metric**.
- You modify **chunk schema**, overlaps, or anchor fields.
- You add a **reranker** or change **k, cutoff, weights**.
- You suspect **index skew** or **store fragmentation**.
- You need a **region-by-region** cutover with instant rollback.

---

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 on three paraphrases (gold set).  
- Coverage to the correct section ≥ 0.70.  
- λ remains convergent across two seeds.  
- No schema drift in required fields: `{snippet_id, section_id, source_url, offsets, tokens}`.  
- p95 latency change within ±15% of baseline at k used in prod.

---

## Build pipeline (offline)
1) **Freeze specs**  
   Pin `EMBED_MODEL_VER`, `EMBED_DIM`, `NORM`, `metric`, `TOK_VER`, `ANALYZER_CONF`, `CHUNK_SCHEMA_VER`.  
   Record as a manifest next to the index.

2) **Re-chunk & re-embed**  
   Apply your chunking checklist; write vectors with doc ids and anchor metadata.

3) **Construct index `docs_vB`**  
   Use store-appropriate build parameters. Keep `docs_vA` live.

4) **Attach reranker (if any)**  
   Persist `RERANK_CONF` and deterministic ordering parameters.

5) **Write integrity probes**  
   Store `INDEX_HASH` = hash(all vectors + manifest). Emit alongside the retriever.

---

## Validation (before any traffic)
- **Gold set eval** (20–40 Qs)  
  Run baseline `docs_vA` vs candidate `docs_vB`. Log ΔS, coverage, λ, latency.

- **Anchor triangulation**  
  Compare ΔS(retrieved, anchor) vs ΔS(retrieved, decoy). If close, fix chunking.

- **Metric sanity**  
  If cosine neighbors look right but meaning is off, re-check metric/norm rules.

- **Fragmentation scan**  
  If top-k distributions differ wildly across partitions, de-frag or rebuild.

- **Contracts**  
  Verify snippet fields and cite-then-explain are intact.

---

## Atomic swap patterns

### Alias swap (preferred)
Keep a stable read name (e.g., `docs_live`) and flip alias from `docs_vA` to `docs_vB`.  
Rollback = flip back to `docs_vA`.

### Config pointer (KV)
Keep a single `INDEX_PTR=docs_vX` in a **one-writer** KV. All readers dereference at request start.  
Rollback = set back to previous pointer.

### Per-region staged swap
Swap one region at a time; watch ΔS/coverage/λ for 15–30 minutes before next region.

---

## 60-second cutover checklist
1) Candidate `docs_vB` passes gold eval targets.  
2) `INDEX_HASH`, `EMBED_SCHEMA`, `RERANK_CONF` emitted by retriever match the manifest.  
3) Caches are primed or partitioned by `INDEX_HASH`.  
4) Canary at 5% is green.  
5) Alias flip or pointer update is **one operation** and reversible.

---

## Stop & rollback
- Hard stop if ΔS p95 drift > 0.15 or coverage < 0.60 or λ flip rate > 0.20.  
- Hard stop if tool loops or 5xx > 1%.  
- Rollback = alias flip back to `docs_vA` (or pointer revert).  
- After rollback, open: [debug_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md).

---

## Store-specific notes
- **FAISS / Chroma**: ensure build-time metric matches query-time; re-normalize if switching from dot to cosine.  
- **Qdrant / Weaviate / Milvus**: pin HNSW/IVF params; rebuild rather than mutate when dimension changes.  
- **pgvector**: match `vector_l2_ops`/`vector_cosine_ops` with embedding norm; verify `ANALYZER_CONF` if paired with text search.  
- **Redis**: keep alias via `FT.ALIASADD`; avoid multi-writer `FT.CREATE` races.  
- **Vespa / Typesense**: schema and field types versioned; perform shadow feed before activation.

---

## Pseudo commands

### Build
```bash
# generate chunks and vectors
wfgy_chunk --schema s128/o32 corpus.jsonl > chunks.jsonl
wfgy_embed --model text-embedding-3-large chunks.jsonl > vectors.fbin

# build candidate index
wfgy_index build --metric cosine --norm l2 --in vectors.fbin --out docs_vB

# compute and store manifest + hash
wfgy_index manifest --index docs_vB > manifest.json
wfgy_index hash --index docs_vB > INDEX_HASH.txt
````

### Validate vs baseline

```bash
wfgy_eval rag --gold gold_40.json \
  --indexes docs_vA,docs_vB \
  --targets "ds<=0.45,cov>=0.70,lambda=convergent"
```

### Swap and rollback (alias style)

```bash
vec alias update docs_live --to docs_vB
# rollback
vec alias update docs_live --to docs_vA
```

---

## Common pitfalls

* Mixed analyzers/tokenizers across ingest vs query.
* “Minor” embedding model update that changes dimension or norm assumptions.
* Reranker cutoff mismatch between staging and prod.
* Cache keys without `INDEX_HASH` causing stale blends.
* Two writers touching the same live alias.

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
