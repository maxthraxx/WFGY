# Language & Multilingual — Global Fix Map

A compact hub to **stabilize cross-lingual retrieval and reasoning**. Use this folder when your corpus or queries span CJK, RTL, Indic, Cyrillic, accented Latin, or when users code-switch.

---

## Quick routes to per-page guides

* Tokenizer mismatch → [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md)
* Script mixing in one query → [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md)
* Locale drift and normalization → [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)
* End-to-end overview and recipes → [multilingual\_guide.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/multilingual_guide.md)

---

## When to use this folder

* High similarity yet wrong meaning on bilingual or mixed-script corpora
* Citations point to the wrong section after translating the question
* Hybrid retrievers underperform a single retriever across languages
* Index “looks” healthy while coverage remains low for non-Latin scripts
* Names flip between native, transliteration, and English aliases
* zh-Hans and zh-Hant never co-retrieve, Thai recall collapses without clear reason

---

## Acceptance targets

* ΔS(question, retrieved) ≤ 0.45 across language variants
* Coverage of the target section ≥ 0.70 after repair
* λ remains convergent across three paraphrases and two seeds
* E\_resonance stays flat on long windows that mix scripts

---

## Open these first

* Visual map and recovery → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End-to-end retrieval knobs → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Why this snippet, how to cite → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Snippet schema fence → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Embedding vs meaning → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Chunk boundary sanity → [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

---

## Map symptoms → structural fixes (Problem Map)

| Symptom                                    | Likely cause                                    | Open this                                                                                                                                                                                                                           |
| ------------------------------------------ | ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Wrong-meaning hits despite high similarity | Embedding not multilingual or pre-norm mismatch | [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)                                                                                                                        |
| Citations jump sections after translation  | Snippet schema too loose                        | [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md), [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)                      |
| zh-Hans/zh-Hant never co-retrieve          | Variant mapping missing                         | [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)                                                                                                                   |
| Thai/CJK recall collapses                  | Tokenizer mismatch, missing segmenter           | [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md)                                                                                                       |
| Mixed Latin + CJK query under-recalls      | Analyzer split across scripts                   | [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md)                                                                                                                 |
| Hybrid retriever worse than single         | Query parsing split, mis-weighted rerank        | [patterns/pattern\_query\_parsing\_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md), [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) |

---

## Fix in 60 seconds

1. **Measure ΔS across variants**
   Run question in source language, target language, and a code-switched version. If ΔS improves only after transliteration or segmentation, language handling is the failing layer.

2. **Probe λ\_observe**
   Hold citations fixed and flip only script or segmentation. If λ flips, lock schema and unify analyzers.

3. **Apply the smallest change**

* Unify index and search analyzers, add Thai/CJK segmenters
* Map zh-Hans ↔ zh-Hant at ingest or store in variant subfields
* Add alias fields for proper nouns: `native`, `romanized`, `normalized`
* Normalize digits, punctuation, and diacritics for RTL/Indic consistently
* Use a multilingual embedding; otherwise add a lexical sidecar and deterministic rerank

4. **Verify**
   Coverage ≥ 0.70 and ΔS ≤ 0.45 across two languages and one mixed query. λ convergent on two seeds.

---

## Store-agnostic quick recipes

* Elasticsearch/OpenSearch: ICU normalization, width fold, bigram analyzers for CJK, Thai segmenter, keyword subfields for product names.
* Vector stores: pre-normalize identically for corpus and queries, validate with a bilingual gold set, rerank deterministically if embeddings are monolingual.

---

## MVP status for this folder

* ✅ `tokenizer_mismatch.md`
* ✅ `script_mixing.md`
* ✅ `locale_drift.md`
* ✅ `multilingual_guide.md`
* ✅ `README.md` (this page)

MVP 完成。若要擴充，建議下一步加入「測試與評估」小頁。

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

</div>


