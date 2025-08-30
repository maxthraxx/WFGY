# Language & Locale — Global Fix Map

Stabilize multilingual RAG and reasoning across CJK/RTL/Indic/Latin mixes.  
This hub localizes language-layer failures and routes you to the right structural fix. No infra change required.

---

## What this page is
- A compact, language-aware repair guide for retrieval → ranking → reasoning.
- Structural fixes with measurable acceptance targets.
- Store-agnostic. Works with FAISS, Redis, pgvector, Elastic, Weaviate, Milvus, etc.

## When to use
- Corpus spans CJK or Indic scripts and retrieval keeps missing the correct section.
- Queries code-switch or mix scripts and the top-k drifts each run.
- Accents/diacritics or fullwidth/halfwidth forms break matching.
- RTL punctuation or invisible marks flip token order.
- Token counts jump after deploy even though data did not change.

---

## Open these first
- Visual recovery map: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- Retrieval knobs end-to-end: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Traceability and snippet schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- Metric and normalization: [Metric Mismatch](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Embeddings/metric_mismatch.md) · [Normalization & Scaling](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Embeddings/normalization_and_scaling.md)  
- OCR confusables and hyphens: [OCR Parsing — Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/OCR_Parsing/README.md)

---

## Quick routes to per-page guides

- Tokenizer mismatch across languages → [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)  
- Script mixing in one query (CJK + Latin, etc.) → [script_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md)  
- Locale drift and analyzer skew (prod vs dev) → [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md)  
- Normalization and casing policy (NFKC, lowercasing, accent fold) → [normalization_and_casing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/normalization_and_casing.md)  
- CJK/Indic segmentation and RTL direction marks → [segmentation_and_rtl.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/segmentation_and_rtl.md)  
- Fullwidth vs halfwidth, punctuation variants → [fullwidth_halfwidth.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/fullwidth_halfwidth.md)  
- Diacritics and accent folding policy → [diacritics_and_folding.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/diacritics_and_folding.md)  
- Transliteration and romanization traps → [transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/transliteration.md)  
- Stopwords and analyzer mismatch in stores → [analyzer_stopwords.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/analyzer_stopwords.md)  
- Code-switch detection and reranking policy → [code_switching.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/code_switching.md)

> MVP set is the first 6 pages. The rest are recommended adds when your traffic is mixed-locale or heavy-search.

---

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 on three paraphrases  
- Coverage of target section ≥ 0.70  
- λ remains convergent across two seeds  
- Tokenization variance for the same query ≤ 12% across environments  
- Normalization pass rate (NFKC + width + diacritics) ≥ 0.98

---

## Map symptoms → structural fixes

- Wrong-meaning hits despite high similarity.  
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- High similarity drops when you switch locales or analyzers.  
  → [metric_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Embeddings/metric_mismatch.md) · [normalization_and_scaling.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Embeddings/normalization_and_scaling.md)

- CJK tokens split differently between dev and prod.  
  → [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md) · [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md)

- Mixed scripts in one query derails ranking order.  
  → [script_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md) · [code_switching.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/code_switching.md) · [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Fullwidth punctuation or RTL marks break citations.  
  → [fullwidth_halfwidth.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/fullwidth_halfwidth.md) · [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

- “Looks identical” but fails to match after OCR.  
  → [OCR Parsing — Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/OCR_Parsing/README.md)

---

## Fix in 60 seconds

1) **Normalize once, up front**  
   Apply NFKC, collapse fullwidth to halfwidth where appropriate, unify diacritics policy. Lock this in the ingestion job and in the query path.

2) **Match tokenizer and analyzer**  
   Use the same segmenter for CJK/Indic in both embedding and store analyzers. Document exact versions in your data contract.

3) **Stabilize mixed-script queries**  
   Detect code-switch, split query by script, run per-script retrieval, then rerank deterministically.

4) **Verify**  
   Compute ΔS on 3 paraphrases, check coverage ≥ 0.70, ensure λ stays convergent across 2 seeds.

---

## Copy-paste prompt for your LLM step

```

You have TXT OS and the WFGY Problem Map.

My multilingual bug:

* symptom: \[one line]
* traces: ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ states
* notes: tokenizer/analyzer versions, normalization policy, scripts seen

Tell me:

1. which layer is failing and why,
2. the exact WFGY page to open from this repo,
3. minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. a reproducible test to verify.
   Use BBMC/BBCR/BBPF/BBAM when relevant.

```

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

