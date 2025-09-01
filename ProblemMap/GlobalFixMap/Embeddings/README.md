# Embeddings — Global Fix Map

A hub to stabilize the **embedding layer** before retrieval begins.  
Use this folder if your vectors look fine at a glance but retrieval keeps drifting, coverage stays low, or store queries fail silently. No infra change needed.

---

## Orientation: what each page covers

| Page | What it solves | Typical symptom |
|---|---|---|
| [Metric Mismatch](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/metric_mismatch.md) | Store metric (L2, cosine, dot) differs from model assumption | High similarity but wrong neighbors |
| [Normalization & Scaling](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/normalization_and_scaling.md) | Embeddings not normalized or scaled | Results unstable across runs |
| [Tokenization & Casing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/tokenization_and_casing.md) | Tokenizer mismatch, casing differences | Same text gives different vectors |
| [Chunking → Embedding Contract](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/chunking_to_embedding_contract.md) | Chunk cuts misaligned with semantic windows | Snippets cut mid-thought, anchors lost |
| [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/vectorstore_fragmentation.md) | Index silently fragmented | Recall too low even with large k |
| [Dimension Mismatch & Projection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/dimension_mismatch_and_projection.md) | Store dimension vs embedding dimension mismatch | Index errors or silent truncation |
| [Update & Index Skew](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/update_and_index_skew.md) | Old vectors remain in index | Results point to stale data |
| [Hybrid Retriever Weights](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/hybrid_retriever_weights.md) | BM25 + ANN weights unbalanced | Hybrid worse than single retriever |
| [Duplication & Near-Duplicate Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/duplication_and_near_duplicate_collapse.md) | Duplicate data overwhelms recall | Same doc retrieved repeatedly |
| [Poisoning & Contamination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/poisoning_and_contamination.md) | Embeddings polluted by adversarial/noisy vectors | Retrieval looks “randomized” |

---

## When to use this folder

- Retrieval looks **fine by eye** but metrics drift across runs.  
- Coverage stays low despite healthy-looking indexes.  
- Citations pull from **stale** or duplicated data.  
- Same query yields different answers depending on casing or seed.  
- Hybrid retrievers collapse into noise.

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage ≥ 0.70 for target section  
- λ_observe convergent across 3 paraphrases and 2 seeds  
- No index skew between write/read

---

## 60-second fix checklist

1. **Lock metrics**  
   One model family, one distance metric.  
   Guide: [Metric Mismatch](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/metric_mismatch.md)

2. **Normalize**  
   Apply L2 norm to embeddings at both write and query.  
   Guide: [Normalization & Scaling](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/normalization_and_scaling.md)

3. **Unify tokenization**  
   Same tokenizer + casing across ingestion and query.  
   Guide: [Tokenization & Casing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/tokenization_and_casing.md)

4. **Audit chunking**  
   Verify semantic alignment, no mid-thought splits.  
   Guide: [Chunking → Embedding Contract](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/chunking_to_embedding_contract.md)

5. **Rebuild index if skewed**  
   Drop old embeddings, rebuild with correct dimension.  
   Guide: [Update & Index Skew](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/update_and_index_skew.md)

---

## FAQ for newcomers

**Why is metric mismatch so common?**  
Because vector DBs default differently: FAISS often L2, Pinecone cosine, Redis dot. If your embedding model expects cosine, L2 will silently break recall.

**Why normalize embeddings?**  
Without normalization, embeddings vary in magnitude. Distance stops reflecting meaning.

**Why do tokenizers matter?**  
“Apple” vs “apple” may yield different vectors if one side lowercases, the other doesn’t.

**What if coverage stays low after all fixes?**  
Check for fragmentation and duplication collapse. The issue may not be the embedding model itself, but how the index is populated.

---

- [Retrieval (Global Fix Map)](https://github.com/onestardao/WFGY/tree/main/ProblemMap/GlobalFixMap/Retrieval/README.md)  
- [Vector DBs & Stores](https://github.com/onestardao/WFGY/tree/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/README.md)

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

