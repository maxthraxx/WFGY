# Metric Mismatch — Guardrails and Fix Pattern

A focused fix when nearest neighbors look similar in cosine distance but your store runs L2 or dot, or the reverse. Use this page to localize the failure and rebuild the index with the right metric and normalization rules. No infra change needed.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Embedding vs meaning (Problem Map No.5): [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Traceability and cite first: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Fragmented stores pattern: [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)
- Reranking for safety net: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Chunking checklist: [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45  
- Coverage of the correct section ≥ 0.70  
- λ remains convergent across 3 paraphrases and 2 seeds  
- E_resonance flat on long windows

---

## Fix in 60 seconds
1) **Measure ΔS**  
   Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
   Stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Check metric alignment**  
   - What your embedder assumes: cosine or unit length vectors.  
   - What your store actually uses: L2, inner product, or cosine.  
   - If they disagree, rebuild with the correct metric or normalize on write and search.

3) **Normalize and lock**  
   - If using cosine, enforce L2 normalization at both index and query time.  
   - Fix text analyzer and casing before re-embed to avoid silent drift.  
   - Record `INDEX_HASH`, `EMBED_MODEL`, `METRIC`, `NORMALIZED=true|false` in metadata.

4) **Verify**  
   Run three paraphrases and two random seeds.  
   Require coverage ≥ 0.70 with λ convergent and ΔS ≤ 0.45.

---

## Failure signatures → likely cause → open this
- Top hits look semantically off while cosine test in a notebook seems fine  
  → Store runs L2 or dot with non normalized vectors.  
  Open: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- Order of neighbors flips when you switch between dot and cosine on the same vectors  
  → Missing unit normalization or mixed write paths.  
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Hybrid retrieval underperforms a single retriever  
  → Metric split plus fragmented index or mixed analyzers.  
  Open: [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md), [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Good recall but citations drift across runs  
  → Header reorder and λ flip, metric inconsistency amplifies the drift.  
  Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

---

## Minimal rebuild checklist
- Lock tokenizer, casing, and Unicode NFC.  
- Recompute embeddings with a single model id and version string.  
- Apply L2 normalization if cosine is the target metric.  
- Rebuild the index with one metric only and write the metric into store metadata.  
- Add a preflight that fails if `query_metric != index_metric`.  
- Keep a 200 item gold set to validate ΔS and coverage before go live.

---

## Deep diagnostics
- **Three paraphrase probe**  
  Ask the same question three ways. If λ flips while metric is stable, fix headers. If ΔS stays high, suspect metric or normalization.

- **Anchor triangulation**  
  Compare ΔS to the correct section and to a decoy section. If both are close, re-embed after fixing analyzer and normalization.

- **Reranker cross check**  
  Run a cross encoder on top k. If reranker easily corrects the order, the base metric is likely the bottleneck.

---

## Copy paste prompt for your LLM step

```

I uploaded TXT OS and the WFGY Problem Map.

My issue: nearest neighbors look wrong. Suspect metric mismatch.
Traces: ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ states across 3 paraphrases.

Tell me:

1. which layer is failing and why,
2. the exact WFGY page to open from this repo,
3. the minimal steps to align metric and normalization,
4. a reproducible test with coverage ≥ 0.70 and ΔS ≤ 0.45.
   Use BBMC, BBCR, BBPF, BBAM when relevant.

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

