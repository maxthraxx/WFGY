# Embeddings — Global Fix Map
Make embedding space match real meaning, not just cosine tricks.  
Use this when recall looks high yet answers point to the wrong idea, or when FAISS/Qdrant “works” but context is off.

## What this page is
- A tight checklist to align models, metrics, and normalization.
- Structural fixes that do not require changing your LLM or infra.
- Steps you can verify with ΔS and small A/B probes.

## When to use
- Similarity scores look strong but retrieved snippets are semantically wrong.
- Different pipelines write/read with different distance metrics.
- Mixed models created the index and now query it.
- Some facts never show up although definitely indexed.
- Cross-language corpus drifts or tokenizers don’t match.

## Open these first
- Meaning vs vector score: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Fragmented or half-empty index: [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)
- End-to-end knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Ordering layer after recall: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Trace why a snippet was picked: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Quality gates: [RAG Precision/Recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md) · [Latency vs Accuracy](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_latency_vs_accuracy.md)

## Fix in 60 seconds
1) **Measure ΔS**
   - Compute `ΔS(question, retrieved)` and `ΔS(retrieved, expected anchor)`.
   - Triggers: ΔS ≥ 0.60 or flat-high ΔS when you vary k ∈ {5,10,20}.

2) **Check metric + normalization agreement**
   - The model that built vectors must match the model used at query time.  
   - Confirm cosine vs inner-product flags on both write and read.  
   - Unit-normalize on both sides if you use cosine.

3) **Verify dimensionality and truncation**
   - Same vector length everywhere.  
   - No hidden cast, dtype mismatch, or silent truncation.

4) **Rebuild once with explicit config**
   - Persist metric, normalizer, and model id with the index file.  
   - After rebuild, probe ΔS again and compare the ΔS-vs-k curve.

5) **Patch recall before ranking**
   - If ΔS drops yet ordering still looks noisy, enable a light reranker from the playbook.  
   - Keep citation schema from traceability to audit the change.

## Copy-paste prompt
```

I uploaded TXT OS and the WFGY ProblemMap files.

My embedding bug:

* symptom: \[brief]
* traces: ΔS(question, retrieved)=..., ΔS(retrieved, anchor)=..., curve vs k=...
* context: write-model=\[...], read-model=\[...], metric=\[cosine|ip], norm=\[on|off]

Tell me:

1. which mismatch explains the failure,
2. which exact pages to open from this repo,
3. the minimal steps to rebuild or rescore to push ΔS ≤ 0.45,
4. how to verify with a reproducible ΔS-vs-k chart and a citation table.
   Use BBMC alignment if anchors are stable, then add a lightweight reranker if needed.

```

## Minimal checklist
- One embedding model per corpus or store the model id with each vector.  
- Fix the metric flag once and persist it with the index.  
- Enforce unit normalization for cosine, never mix with raw dot product.  
- Keep text pre-processing identical on write and read.  
- Log vector counts per collection; compare to document counts.  
- Run the fragmentation pattern if some facts vanish from results.

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 across three paraphrases.  
- ΔS-vs-k curve descends then flattens, not flat-high.  
- Recall/precision meet your eval sheet thresholds.  
- λ stays convergent at the retrieval layer after the rebuild.  
- Traceability explains why each snippet was selected.

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
