# RAG + VectorDB — Global Fix Map

<details>
  <summary><strong>🏥 Quick Return to Emergency Room</strong></summary>

<br>

  > You are in a specialist desk.  
  > For full triage and doctors on duty, return here:  
  > 
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/README.md)  
  > 
  > Think of this page as a sub-room.  
  > If you want full consultation and prescriptions, go back to the Emergency Room lobby.
</details>

This hub covers **typical retrieval bugs caused by vector databases and embeddings**.  
Use this page if your RAG pipeline looks fine but answers keep drifting, citations don’t match, or hybrid retrievers underperform.  
Every page here is a guardrail with copy-paste recipes and acceptance targets.  

---

## Orientation: what each page means

| Fix Page | What it solves | Typical symptom |
|----------|----------------|-----------------|
| [metric_mismatch.md](./metric_mismatch.md) | Distance metric mismatch (cosine vs L2 vs dot) | High similarity numbers but wrong meaning |
| [normalization_and_scaling.md](./normalization_and_scaling.md) | Missing normalization or scaling issues | Embeddings with larger norms dominate |
| [tokenization_and_casing.md](./tokenization_and_casing.md) | Tokenizer or casing drift | Same text embeds differently across runs |
| [chunking_to_embedding_contract.md](./chunking_to_embedding_contract.md) | Chunking not aligned with embedding model | Citations cut mid-sentence or incoherent snippets |
| [vectorstore_fragmentation.md](./vectorstore_fragmentation.md) | Over-fragmented stores | Retrieval pulls incomplete, scattered sections |
| [dimension_mismatch_and_projection.md](./dimension_mismatch_and_projection.md) | Embedding and index dimension mismatch | Runtime errors or silent drop of vectors |
| [update_and_index_skew.md](./update_and_index_skew.md) | Index not refreshed after updates | Old sections keep showing up |
| [hybrid_retriever_weights.md](./hybrid_retriever_weights.md) | Hybrid weighting not tuned | BM25+ANN underperforms single retriever |
| [duplication_and_near_duplicate_collapse.md](./duplication_and_near_duplicate_collapse.md) | Redundant entries collapse signal | Top-k filled with near-identical chunks |
| [poisoning_and_contamination.md](./poisoning_and_contamination.md) | Malicious or noisy vectors | Hallucinations, unsafe content retrieval |

---

## When to use this folder

- Your answers look **semantically wrong** even though top-k similarity looks high.  
- Citations point to the wrong section or cannot be verified.  
- Hybrid retrieval underperforms vs single retriever.  
- Index seems “healthy” but recall/coverage stays low.  

---

## Core acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ_observe convergent across 3 paraphrases  
- E_resonance flat on long windows  

---

## FAQ for newcomers

**Why do we need these fixes if VectorDBs are mature?**  
Because RAG pipelines often break not at the infra level but at the **semantic boundary**. Even if FAISS, Milvus, or Pinecone run fine, the *contracts* between embedding, chunking, and retrieval are fragile.

**What is metric mismatch and why is it deadly?**  
If your index uses `L2` but embeddings were trained for `cosine`, the “closest” neighbors are meaningless. This is the single most common RAG failure.

**Why do duplicates matter so much?**  
If your corpus has many repeated sentences, the retriever fills top-k with clones. The LLM sees no diversity and hallucinates.

**Is poisoning really a real-world issue?**  
Yes. Even a single malicious doc can bias retrieval. This page shows how to detect and quarantine them without retraining the whole pipeline.

---

## 60-Second Fix Checklist

1. **Lock metrics and analyzers**  
   One embedding model per field. One distance metric. Same analyzer for read/write.

2. **Enforce snippet contracts**  
   Require `{snippet_id, section_id, source_url, offsets, tokens}`.  
   → See [data-contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

3. **Tune hybrid retrievers**  
   Keep candidate lists from BM25 and ANN. Detect query splits.  
   → See [rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

4. **Cold-start fences**  
   Block traffic until index hash and embedding version match.  
   → See [bootstrap-ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

5. **Observability**  
   Log ΔS and λ. Alert if ΔS ≥ 0.60.  

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
