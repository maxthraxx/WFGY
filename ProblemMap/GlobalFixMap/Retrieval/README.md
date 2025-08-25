# Retrieval — Global Fix Map
Make your retriever correct, predictable, and auditable.  
Use this when recall looks random, hybrid behaves worse than single, or k-tuning never stabilizes.

## What this page is
- A short, practical path to stabilize recall and ordering
- Exact knobs for dense, sparse, and hybrid without guesswork
- How to prove fixes with ΔS curves and citation tables

## When to use
- Top-k results feel unrelated or change on every run
- Hybrid merge hurts more than single retriever
- Raising k only adds noise, does not surface the right snippet
- Filters, analyzers, or languages do not align with your corpus
- HyDE or query rewriting helps sometimes then flips back

## Open these first
- End to end knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Ordering after recall: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Why this snippet, trace schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Hybrid tokenization split: [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)
- Hallucination from bad boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
- Cosine match is not meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Some facts never retrieve: [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)
- Visual pipeline and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- Eval targets: [RAG Precision and Recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

## Fix in 60 seconds
1) **Probe ΔS vs k**
   - Record `ΔS(question, retrieved)` for k in {5, 10, 20} for each retriever separately.  
   - Flat and high for all k indicates index or metric mismatch or population gaps. Fix store first.

2) **Establish a strong single baseline**
   - Pick the retriever with the lowest stable ΔS at small k.  
   - Freeze its tokenizer, analyzer, language, stopword set. Save params to disk.

3) **Unify query parsing**
   - Ensure the same analyzer and lowercasing for write and read.  
   - If using HyDE or rewrites, log the final string sent to each retriever and keep it identical across them.

4) **Hybrid only after per retriever stability**
   - Do not mix until each single retriever yields ΔS ≤ 0.50.  
   - Start with a simple weighted sum and a light reranker. Keep citations to audit the change.

5) **Filters and fields**
   - Disable filters first to confirm baseline recall.  
   - Reapply with exact field weights and language settings. Check for case and tokenizer mismatches.

6) **Dedupe and diversity**
   - Apply MMR or novelty at the rerank stage if results cluster.  
   - Keep a per source fence so different documents do not merge.

7) **Prompt assembly sanity**
   - Use citation first schema from traceability.  
   - Do not reorder sections once stable.

8) **Warm up and cache**
   - Run a deterministic warm up after deploy.  
   - Verify repeatability across restarts.

## Copy paste prompt
```

I uploaded TXT OS and WFGY ProblemMap pages.

My retrieval bug:

* symptom: \[brief]
* ΔS vs k per retriever: {...}
* single retriever baselines: \[dense], \[BM25], \[hybrid attempt]
* analyzers/tokenizers: write=\[...], read=\[...], lowercasing=\[on|off], stopwords=\[profile]
* filters/fields: \[list]
* HyDE or rewrites: \[yes/no], final query strings logged: \[examples]

Tell me:

1. which parsing or configuration mismatch explains the failure,
2. which exact WFGY pages to open,
3. minimal steps to push ΔS ≤ 0.45 at k=10 without overfitting,
4. how to verify with precision/recall and a snippet ↔ citation table.
   Use rerankers only after recall is stable.

```

## Minimal checklist
- Same analyzer, language, and case handling on write and read  
- Log the exact query string per retriever including HyDE output  
- Stabilize a single retriever before mixing hybrids  
- Keep field weights explicit and versioned  
- Do not change k and temperature together when measuring ΔS  
- Add reranker only after recall metrics pass  
- Enforce per source fences to avoid cross document blending  
- Persist a warm up routine for post deploy parity

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 across three paraphrases  
- Precision and recall meet your eval sheet with traceable citations  
- ΔS vs k descends then stabilizes, no oscillation when k grows  
- Same answers across restarts after warm up  
- λ at retrieval remains convergent while reasoning proceeds
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
