# Tokenizer Mismatch — Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Language**.  
  > To reorient, go back here:  
  >
  > - [**Language** — multilingual processing and semantic alignment](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Stabilize multilingual retrieval when the query and the index segment text differently.
Typical pain shows up in Chinese, Japanese, Thai, Khmer, and any mixed-script corpus where whitespace is unreliable.

---

## Open these first

* Visual map and recovery: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* Chunking checklist: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)
* Retrieval traceability: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Schema fence for snippets: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Embedding vs meaning: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

Related multilingual pages in this folder:

* Guide overview: [multilingual\_guide.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/multilingual_guide.md)
* Script direction and mixing: [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md)
* Locale and analyzer drift: [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)
* HyDE behavior across languages: [hyde\_multilingual.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/hyde_multilingual.md)

---

## Core acceptance targets

* ΔS(question, retrieved) ≤ 0.45 for both English and target language
* Coverage of target section ≥ 0.70 after repair
* λ remains convergent across three paraphrases in the target language
* E\_resonance flat across 50+ queries that mix scripts and numbers

---

## What this failure looks like

| Symptom                                                                    | Likely cause                                                               | Where to fix                                                        |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Chinese or Japanese queries return no hits, while English paraphrase works | Query tokenizer uses whitespace, index uses character n-gram or vice versa | Switch to language-aware analyzers; unify query and index pipelines |
| BM25 recall ok but citations land in the wrong sub-section                 | Token boundary misalignment between chunker and retriever                  | Rechunk with stable boundaries and same segmentation as the store   |
| Hybrid retrieval underperforms a single retriever                          | Mixed analyzers per stage, reranker sees inconsistent text                 | Normalize text pre-rerank and re-embed with the same tokenizer      |
| High similarity yet wrong meaning                                          | Embedding model trained with different normalization or casing rules       | Re-embed with consistent normalization; see Embedding ≠ Semantic    |

---

## Fix in 60 seconds

1. **Measure ΔS**
   Run the same question in English and the target language. If ΔS differs by more than 0.15, suspect tokenizer mismatch.

2. **Probe λ\_observe**
   Paraphrase the non-English query three ways. If λ flips between convergent and divergent when you reorder headers, lock the prompt schema and proceed to analyzer unification.

3. **Apply the smallest structural change**

* If your store is lexical: set **the same analyzer** for both index and query.
* If your store is vector-only: normalize and segment **before** embedding, then re-embed a small gold set and verify.

4. **Verify**
   Coverage ≥ 0.70 and ΔS ≤ 0.45 on three paraphrases. Log the analyzer and normalization used.

---

## Minimal repair recipes by stack

### Elasticsearch / OpenSearch

* Pick **one** analyzer for CJK fields and use it for both indexing and queries.
  Options that work in practice:

  * Japanese: `kuromoji`
  * Korean: `nori`
  * Chinese: `smartcn` or ICU + bigram filter
* Add a keyword subfield for exact filters and rerank features.
* Normalize to NFC and convert full-width to half-width for digits and ASCII.
* Rebuild only the affected indices, then re-run the gold set.
  See: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

### BM25 in code or light stores (Chroma, sqlite FTS, etc.)

* For CJK and Thai, use **character bigrams or trigrams** on both index and query.
* Remove language-specific stopwords when language is unknown.
* Keep punctuation normalization consistent across stages.
  See: [pattern\_query\_parsing\_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)

### Vector stores (FAISS, Milvus, pgvector, Weaviate, Qdrant)

* Do not trust the model to “fix” segmentation. Pre-normalize text:

  * Unicode NFC
  * Lowercase where appropriate
  * Full-width to half-width for numbers and ASCII
  * Optional: insert spaces between CJK and ASCII tokens for stable sentencepiece
* Re-embed both corpus and queries with the exact same normalization script.
* If recall is still low, add a lexical recall stage, then rerank.
  See: [vectorstore-fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

---

## Diagnostic checklist

* Query and index use **the same** tokenizer or analyzer.
* Chunker segmentation matches the retriever segmentation.
* Unicode form is consistent; half-width and diacritics normalized.
* Mixed scripts do not flip direction or join tokens incorrectly.
* Rerank stage sees normalized text, not raw captures.

---

## Copy-paste tests

**Three-language ΔS probe**

```
Question: "<your question>"
Languages: English, Chinese, Japanese

For each language:
1. Retrieve top-k with your current settings.
2. Compute ΔS(question, retrieved). Record λ_state.
3. If ΔS differs by > 0.15 across languages, suspect tokenizer mismatch.
Return a table: language, ΔS, λ_state, analyzer/normalizer used.
```

**Schema lock for reruns**

```
Header order: citations → facts → synthesis → caveats.
If λ flips when you change header order, lock this schema and fix analyzers first.
```

---

## When to escalate

* ΔS remains ≥ 0.60 after analyzer unification.
  Re-chunk with stable boundaries and re-embed a gold slice.
  Open: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

* Citations still jump across sections after repair.
  Enforce snippet schema and forbid cross-section reuse.
  Open: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md), [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

* Hybrid beats single only sometimes.
  Align analyzers in both stages and rerank deterministically.
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
