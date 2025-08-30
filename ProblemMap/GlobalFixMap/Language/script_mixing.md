# Script Mixing — Guardrails and Fix Patterns

Keep retrieval stable when a single query or snippet mixes scripts and directions.
Common cases: CJK + Latin acronyms, Arabic or Hebrew with numbers and English terms, Devanagari with Latin product names, and datasets where full-width digits appear beside half-width ASCII.

---

## Open these first

* Visual map and recovery: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* Why this snippet and how to cite: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Snippet schema fence: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Embedding vs meaning: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Chunk boundary sanity: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

Related in this folder:

* Tokenization drift: [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md)
* Locale and analyzer drift: [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)
* Multilingual guide hub: [multilingual\_guide.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/multilingual_guide.md)
* HyDE behavior by language: [hyde\_multilingual.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/hyde_multilingual.md)

---

## Core acceptance targets

* ΔS(question, retrieved) ≤ 0.45 for mixed-script queries
* Coverage of the target section ≥ 0.70 after repair
* λ remains convergent across three paraphrases that include different script orderings
* E\_resonance flat on long windows with numerals, punctuation, and brand names mixed in

---

## What this failure looks like

| Symptom                                                          | Likely cause                                                                | Where to fix                                                                     |
| ---------------------------------------------------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Arabic or Hebrew queries return partial hits or broken citations | Bidirectional marks and numerals flip visual order; analyzer not bidi-aware | Normalize directionality and digits before indexing and querying                 |
| CJK text with Latin acronyms splits unpredictably                | Mixed width digits, zero-width chars, or inconsistent spacing rules         | Pre-normalize width, strip zero-width, add script-boundary spacing for embedding |
| English brand + Thai sentence retrieves far sections             | Different analyzers per stage cause token joins and drops                   | Unify analyzer and pre-segment at script transitions                             |
| High similarity but wrong meaning on acronyms                    | Casing and width normalization inconsistent between corpus and query        | Apply the same ASCII, width, and case rules in both pipelines                    |

---

## Fix in 60 seconds

1. **Measure ΔS**
   Run the original mixed-script query and a variant where scripts are separated by spaces. If ΔS improves by ≥ 0.10, you have a script-mixing normalization gap.

2. **Probe λ\_observe**
   Swap the order of scripts in the query, keep semantics identical. If λ flips or citations jump, lock prompt headers and fix normalization and analyzer alignment first.

3. **Apply the smallest structural change**

* Normalize Unicode to NFC, convert full-width to half-width for digits and ASCII.
* Remove zero-width characters, directional isolates from raw text.
* Ensure the same analyzer is used for both index and query, or pre-segment before embedding.

4. **Verify**
   Coverage ≥ 0.70 and ΔS ≤ 0.45 on three paraphrases with different script orders.

---

## Minimal repair recipes by stack

### Elasticsearch / OpenSearch

* Use ICU chain for mixed scripts. Typical pipeline:
  `icu_normalizer` (NFC) → `icu_transform` (full-width to half-width) → `icu_folding` → optional CJK bigram filter.
* For Arabic or Persian add `arabic_normalization` or `persian_normalization`.
* Strip bidi control chars in a char filter.
* Set the same analyzer for `index` and `search_analyzer` on the field.
* Create a keyword subfield for exact acronyms and model names.
  Reference: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

### BM25 in code or light stores

* Preprocess text with a normalization step that performs:
  Unicode NFC, width fold for digits and ASCII, lowercasing where safe, removal of zero-width and bidi marks.
* For CJK, insert temporary spaces at script boundaries or use character bigrams for both index and query.
* Keep identical punctuation rules across stages.
  Open: [pattern\_query\_parsing\_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)

### Vector stores (FAISS, Milvus, Qdrant, Weaviate, pgvector)

* Normalize text before embedding with the same script rules for corpus and queries.
* Add lightweight lexical recall (BM25) to catch brand names and numerals, then rerank deterministically.
* Re-embed only a gold slice to validate, then batch the full rebuild.
  Open: [vectorstore-fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

---

## Diagnostic checklist

* The same normalization code runs for ingest and query.
* Width folding, casing, digit policy are identical across stages.
* Bidi control marks removed or isolated consistently.
* Chunk boundaries do not split inside script transitions that carry meaning.
* Rerank stage views the normalized text, not raw captures.

---

## Copy-paste tests

**Script order probe**

```
Q0: original mixed-script query
Q1: same words, scripts reordered
Q2: same words, add spaces at script boundaries

Return a table with ΔS per query, λ_state, and whether citations stayed in the same section.
```

**Bidi and width sanity**

```
Given a sentence with Arabic text, ASCII digits, and an English acronym:
1) Remove bidi marks and normalize widths.
2) Show the token sequence used by the retriever.
3) Verify that numbers appear in logical order and acronyms stay intact.
```

---

## When to escalate

* ΔS remains ≥ 0.60 after normalization and analyzer unification.
  Re-chunk with stable boundaries and re-embed a gold slice.
  Open: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

* Citations still jump between sections on mixed-script inputs.
  Enforce snippet schema and forbid cross-section reuse.
  Open: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md), [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

* Hybrid retrieval underperforms a single retriever.
  Align normalization rules before rerank, and make rerank deterministic.
  Open: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

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

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)

</div>
