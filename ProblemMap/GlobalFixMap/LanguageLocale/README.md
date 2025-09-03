# Language & Locale · Global Fix Map

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

Stabilize multilingual RAG and reasoning across **CJK, RTL, Indic, Latin, emoji, and locale variants**.  
This hub localizes language-layer failures and routes you to the exact structural fix. No infra change required.

---

## What this page is
- A compact **language-aware repair guide** for retrieval → ranking → reasoning.
- Structural fixes with measurable acceptance targets.
- Store-agnostic. Works with FAISS, Redis, pgvector, Elastic, Weaviate, Milvus, and more.

---

## When to use
- Corpus spans **CJK or Indic scripts** and retrieval keeps missing the correct section.  
- Queries **code-switch or mix scripts**, and top-k order drifts across runs.  
- **Accents/diacritics** or **fullwidth/halfwidth** forms break matching or citations.  
- **RTL punctuation or control chars** flip token order or offsets.  
- Token counts jump after deploy even though **data did not change**.  

---

## Open these first
- Visual recovery map → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- Retrieval knobs end-to-end → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Traceability and snippet schema → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Embedding vs meaning → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- Metric and normalization → [metric_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Embeddings/metric_mismatch.md) · [normalization_and_scaling.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Embeddings/normalization_and_scaling.md)  
- OCR confusables and hyphens → [OCR_Parsing README](https://github.com/onestardao/WFGY/blob/main/ProblemMap/OCR_Parsing/README.md)  

---

## Quick routes to per-page guides

| Topic | Page |
|-------|------|
| Tokenizer mismatch across languages | [tokenizer_mismatch.md](./tokenizer_mismatch.md) |
| Script mixing in a single query | [script_mixing.md](./script_mixing.md) |
| Locale drift and analyzer skew | [locale_drift.md](./locale_drift.md) |
| Unicode normalization policy | [unicode_normalization.md](./unicode_normalization.md) |
| CJK segmentation and word-break | [cjk_segmentation_wordbreak.md](./cjk_segmentation_wordbreak.md) |
| Fullwidth vs halfwidth, punctuation variants | [digits_width_punctuation.md](./digits_width_punctuation.md) |
| Diacritics folding rules | [diacritics_and_folding.md](./diacritics_and_folding.md) |
| RTL and bidi control characters | [rtl_bidi_control.md](./rtl_bidi_control.md) |
| Transliteration and romanization | [transliteration_and_romanization.md](./transliteration_and_romanization.md) |
| Collation and stable sort keys | [locale_collation_and_sorting.md](./locale_collation_and_sorting.md) |
| Numbering systems and sort orders | [numbering_and_sort_orders.md](./numbering_and_sort_orders.md) |
| Date and time format variants | [date_time_format_variants.md](./date_time_format_variants.md) |
| Time zones and DST stability | [timezones_and_dst.md](./timezones_and_dst.md) |
| Keyboard IMEs and composition | [keyboard_input_methods.md](./keyboard_input_methods.md) |
| Input language switching guards | [input_language_switching.md](./input_language_switching.md) |
| Emoji, ZWJ, grapheme clusters | [emoji_zwj_grapheme_clusters.md](./emoji_zwj_grapheme_clusters.md) |
| Mixed-locale metadata fields | [mixed_locale_metadata.md](./mixed_locale_metadata.md) |

---

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 on three paraphrases  
- Coverage of target section ≥ 0.70  
- λ remains convergent across two seeds  
- Tokenization variance for the same query ≤ 12% across environments  
- Normalization pass rate for NFKC + width + diacritics ≥ 0.98  

---

## Fix in 60 seconds
1. **Normalize once, up front** → Apply NFKC, collapse fullwidth/halfwidth, unify diacritics.  
2. **Match tokenizer and analyzer** → Same segmenter for CJK/Indic across embed + store analyzers.  
3. **Stabilize mixed-script queries** → Detect code-switch, split per script, rerank deterministically.  
4. **Verify** → ΔS ≤ 0.45, Coverage ≥ 0.70, λ convergent across two seeds.  

---

## FAQ (Beginner-Friendly)

**Q1: Why do answers break when I mix English and Chinese in one query?**  
A: Most vector stores tokenize differently by script. Without alignment, Chinese words get split incorrectly and English tokens dominate. Fix with [script_mixing.md](./script_mixing.md) and [tokenizer_mismatch.md](./tokenizer_mismatch.md).

**Q2: What does “locale drift” mean?**  
A: Locale drift happens when environments use different analyzers (e.g., zh_TW vs zh_CN) so the same query splits differently. See [locale_drift.md](./locale_drift.md).

**Q3: Why do “identical-looking” characters not match?**  
A: They may differ in width (fullwidth vs halfwidth), normalization (NFKC vs NFD), or diacritics. Always apply [unicode_normalization.md](./unicode_normalization.md) and [digits_width_punctuation.md](./digits_width_punctuation.md).

**Q4: How do I handle Arabic or Hebrew text?**  
A: RTL scripts can insert invisible bidi control chars that flip token order. See [rtl_bidi_control.md](./rtl_bidi_control.md).

**Q5: Do I need different embeddings for each language?**  
A: No. You can combine multilingual embeddings with deterministic normalization and alias fields. If that fails, only then use [fallback translation bridges](../Language/fallback_translation_and_glossary_bridge.md).

**Q6: How do I debug when results change between environments?**  
A: Compare tokenizer version, analyzer settings, normalization passes, and collation rules. Document them in [data-contracts.md](../../data-contracts.md).

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
