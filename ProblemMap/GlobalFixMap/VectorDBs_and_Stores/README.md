# Vector DBs & Stores — Global Fix Map

A hub to stabilize retrieval pipelines across popular vector stores.  
Use this page to jump to per-tool guardrails and verify fixes with the same acceptance targets.

---

## Quick routes to per-store pages

- FAISS → [faiss.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/faiss.md)  
- Chroma → [chroma.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/chroma.md)  
- Qdrant → [qdrant.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/qdrant.md)  
- Weaviate → [weaviate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/weaviate.md)  
- Milvus → [milvus.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/milvus.md)  
- pgvector → [pgvector.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/pgvector.md)  
- Redis (Search/Vec) → [redis.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/redis.md)  
- Elasticsearch (kNN / dense) → [elasticsearch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/elasticsearch.md)  
- Pinecone → [pinecone.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/pinecone.md)

---

## When to use this folder

- High similarity but wrong meaning.  
- Citations don’t line up with the retrieved section.  
- Hybrid retrievers underperform a single retriever.  
- Query casing / analyzer / metric mismatches after deploy.  
- Index looks healthy yet coverage remains low.

---

## Acceptance targets for any store

- ΔS(question, retrieved) ≤ **0.45**  
- Coverage of target section ≥ **0.70**  
- λ\_observe stays **convergent** across 3 paraphrases  
- E\_resonance flat on long windows

---

## Map symptoms → structural fixes (Problem Map)

- **Embedding ≠ Semantic**  
  Wrong-meaning hits despite high similarity.  
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- **Retrieval traceability**  
  Snippet/section mismatch or unverifiable citations.  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  Payload schema: → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **Ordering / version skew**  
  Old index or analyzer used at runtime.  
  → [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) ·
  [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- **Hybrid collapse / query split**  
  HyDE vs BM25 disagreement, reranker blind spots.  
  → Pattern: [patterns/pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)  
  → Knobs: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

---

## 60-second fix checklist (store-agnostic)

1) **Lock metrics & analyzers**  
   Pin distance metric, tokenizer/casing, and normalization on both write and read.

2) **Contract the snippet**  
   Require `{snippet_id, section_id, source_url, offsets, tokens}`.

3) **Probe ΔS and λ**  
   Log ΔS(question, retrieved) and λ per step; alert at ΔS ≥ 0.60.

4) **Verify coverage**  
   Run a 10-question eval on the target section; require coverage ≥ 0.70.

5) **Reranking pass**  
   If hybrid disagrees, add a rerank step and re-measure ΔS.

---

## Copy-paste prompt for a quick audit

```

I uploaded TXT OS and the WFGY Problem Map pages.
My stack uses <store> with metric \<cosine|l2|dot>, analyzer <...>, and normalization <...>.

Do:

1. Report ΔS(question, retrieved) and λ states across retrieve → rerank → reason.
2. If ΔS ≥ 0.60, point to one minimal structural fix:
   embedding-vs-semantic, retrieval-traceability, data-contracts, rerankers.
3. Return JSON:
   { "citations":\[...], "ΔS":0.xx, "λ":"→|←|<>|×", "next\_fix":"..." }

```

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>” |
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
