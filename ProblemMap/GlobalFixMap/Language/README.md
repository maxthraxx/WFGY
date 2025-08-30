# Language & Multilingual · Global Fix Map

A compact hub to **stabilize cross-lingual retrieval and reasoning**.  
Use this folder when your corpus or queries include CJK, RTL, Indic, Cyrillic, accented Latin, or frequent code-switching.

---

## Quick routes to per-page guides

- Tokenizer mismatch → [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md)
- Script mixing inside one query → [script_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md)
- Locale normalization and variants → [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)
- End-to-end overview and recipes → [multilingual_guide.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/multilingual_guide.md)
- Proper nouns and alias shield → [proper_noun_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md)
- Romanization and transliteration rules → [romanization_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md)
- Query language detection contract → [query_language_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_language_detection.md)
- Analyzer routing per language → [query_routing_and_analyzers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_routing_and_analyzers.md)
- Multilingual hybrid ranking → [hybrid_ranking_multilingual.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/hybrid_ranking_multilingual.md)
- Stopwords and morphology locks → [stopword_and_morphology_controls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/stopword_and_morphology_controls.md)
- Fallback translation with glossary → [fallback_translation_and_glossary_bridge.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/fallback_translation_and_glossary_bridge.md)
- Bilingual and code-switch eval sets → [code_switching_eval.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/code_switching_eval.md)

---

## When to use this folder

- High similarity yet wrong meaning on bilingual or mixed-script corpora
- Citations point to the wrong section after translating the question
- Hybrid retrievers underperform a single retriever across languages
- Index looks healthy while coverage stays low for non-Latin scripts
- Names flip between native, transliteration, and English aliases
- zh-Hans and zh-Hant never co-retrieve, Thai recall drops with no clear cause

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45 across language variants
- Coverage of the target section ≥ 0.70 after repair
- λ remains convergent across three paraphrases and two seeds
- E_resonance stays flat on long windows that mix scripts
- Citation fields complete, alias noise does not leak into evidence

---

## Open these first

- Visual map and recovery → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End-to-end retrieval knobs → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why this snippet and how to cite → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Snippet schema fence → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Embedding vs meaning → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Chunk boundary sanity → [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

---

## Map symptoms → structural fixes

| Symptom | Likely cause | Open this |
|---|---|---|
| High similarity yet wrong meaning | Embedding not multilingual or pre-normalization mismatch | [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) |
| Citations jump sections after translation | Snippet schema too loose | [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) · [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| zh-Hans and zh-Hant never co-retrieve | Variant mapping and width rules missing | [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md) |
| Thai or CJK recall collapses | Tokenizer mismatch or missing segmenter | [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md) |
| Mixed Latin plus CJK query under-recalls | Analyzer split across scripts | [script_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md) |
| Hybrid retriever worse than single | Query parsing split or mis-weighted rerank | [patterns/pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) · [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) |
| Proper nouns oscillate across spellings | Missing alias fields and entity shield | [proper_noun_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md) |
| Inconsistent transliteration causes misses | Romanization rules and aliases not aligned | [romanization_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md) |
| Language detection drifts | Detection contract unlocked or weak samples | [query_language_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_language_detection.md) |
| Search vs index behave differently | Analyzer routing error | [query_routing_and_analyzers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_routing_and_analyzers.md) |
| Ranking unstable across languages | Monolingual reranker or unaligned features | [hybrid_ranking_multilingual.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/hybrid_ranking_multilingual.md) |
| Negations or particles vanish | Stopword or morphology rules too aggressive | [stopword_and_morphology_controls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/stopword_and_morphology_controls.md) |
| Persistent high ΔS on local language path | Need controlled translation bridge with glossary | [fallback_translation_and_glossary_bridge.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/fallback_translation_and_glossary_bridge.md) |

---

## Fix in 60 seconds

1. **Detect language**  
   Emit stable language and confidence per the detection contract. If unstable, stop and fix detection first.  
   Open → [query_language_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_language_detection.md)

2. **Lock normalization and analyzers**  
   Keep the same locale, width, accents, and segmentation for both index and search.  
   Open → [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md) · [query_routing_and_analyzers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_routing_and_analyzers.md)

3. **Protect entities and syntax**  
   Add alias fields and romanization pairs. Clamp stopwords and morphological rules for scope words like negations or units.  
   Open → [proper_noun_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md) · [romanization_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md) · [stopword_and_morphology_controls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/stopword_and_morphology_controls.md)

4. **Stabilize ranking and hybrid flows**  
   Use multilingual reranker or dual-track lexical plus vector, keep ordering deterministic.  
   Open → [hybrid_ranking_multilingual.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/hybrid_ranking_multilingual.md)

5. **Use a translation bridge only as last resort**  
   Enable only when the native path keeps high ΔS. Always pair with a glossary.  
   Open → [fallback_translation_and_glossary_bridge.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/fallback_translation_and_glossary_bridge.md)

6. **Verify**  
   With bilingual and code-switch test sets confirm ΔS ≤ 0.45 and Coverage ≥ 0.70, λ convergent.  
   Open → [code_switching_eval.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/code_switching_eval.md)

---

## Store-agnostic quick recipes

- Normalize the same way for corpus and queries before any vector store, keep tokenizer consistent on both sides  
- CJK and Thai need segmentation or bigrams, keep critical fields as keyword to protect entities  
- If you cannot use multilingual embeddings, add a lexical sidecar then align features in a deterministic rerank


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

