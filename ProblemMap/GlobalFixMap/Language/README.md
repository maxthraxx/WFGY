# Language & Multilingual · Global Fix Map

A compact hub to **stabilize cross-lingual retrieval and reasoning**.  
Use this folder when your corpus or queries include CJK, RTL, Indic, Cyrillic, accented Latin, or frequent code-switching. No infra change required.

---

## Orientation — pages and what they solve

| Page | What it solves | Typical symptom |
|------|----------------|-----------------|
| [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md) | Locks tokenization and segmentation for CJK/Thai/Indic | High sim but low recall on CJK/Thai; broken tokens |
| [script_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md) | One query carries mixed scripts and analyzers split | Mixed Latin+CJK queries under-recall or flip |
| [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md) | Normalization for width/accents/variants (Hans↔Hant) | zh-Hans/zh-Hant never co-retrieve; accent variants miss |
| [multilingual_guide.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/multilingual_guide.md) | End-to-end recipes and acceptance targets | Unsure where drift comes from across languages |
| [proper_noun_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md) | Alias shield for names, brands, products | Proper nouns oscillate across spellings |
| [romanization_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md) | Romanization pairs and transliteration consistency | Inconsistent transliteration causes misses |
| [query_language_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_language_detection.md) | Stable language detection contract | Detection flips per run; routing becomes random |
| [query_routing_and_analyzers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_routing_and_analyzers.md) | Route analyzers per language + parity w/ index | Search vs index behave differently |
| [hybrid_ranking_multilingual.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/hybrid_ranking_multilingual.md) | Deterministic hybrid rerank across languages | Multilingual ranking unstable, hybrid < single |
| [stopword_and_morphology_controls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/stopword_and_morphology_controls.md) | Clamp stopwords/lemmatizers to protect meaning | Negations/particles vanish; unit words lost |
| [fallback_translation_and_glossary_bridge.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/fallback_translation_and_glossary_bridge.md) | Controlled translation bridge with glossary | Local path ΔS stays high; glossary needed |
| [code_switching_eval.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/code_switching_eval.md) | Bilingual & code-switch eval sets + checks | Cannot prove multilingual stability before ship |

---

## When to use this folder

- High similarity yet wrong meaning on bilingual or mixed-script corpora  
- Citations point to the wrong section after translating the question  
- Hybrid retrievers underperform a single retriever across languages  
- Index looks healthy while coverage stays low for non-Latin scripts  
- Names flip between native, transliteration, and English aliases  
- zh-Hans and zh-Hant never co-retrieve; Thai recall drops for no reason  

---

## Acceptance targets

- **ΔS(question, retrieved) ≤ 0.45** across language variants  
- **Coverage ≥ 0.70** to the intended section after repair  
- **λ_observe convergent** across 3 paraphrases and 2 seeds  
- **E_resonance flat** on long windows that mix scripts  
- Citation fields complete; alias noise does not leak into evidence  

---

## Map symptoms → structural fixes

| Symptom | Likely cause | Open this |
|---|---|---|
| High similarity yet wrong meaning | Embedding not multilingual or pre-normalization mismatch | [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) |
| Citations jump sections after translation | Snippet schema too loose | [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) · [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| zh-Hans and zh-Hant never co-retrieve | Variant mapping and width rules missing | [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md) |
| Thai or CJK recall collapses | Tokenizer mismatch or missing segmenter | [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md) |
| Mixed Latin + CJK query under-recalls | Analyzer split across scripts | [script_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md) |
| Hybrid worse than single | Query parsing split or mis-weighted rerank | [patterns/pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) · [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) |
| Proper nouns oscillate | Missing alias fields and entity shield | [proper_noun_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md) |
| Transliteration inconsistency | Romanization rules not aligned | [romanization_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md) |
| Language detection drifts | Detection contract weak or unlocked | [query_language_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_language_detection.md) |
| Search vs index disagree | Analyzer routing error | [query_routing_and_analyzers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_routing_and_analyzers.md) |
| Ranking unstable across languages | Mono-lingual reranker or unaligned features | [hybrid_ranking_multilingual.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/hybrid_ranking_multilingual.md) |
| Negations/particles vanish | Stopword or morphology too aggressive | [stopword_and_morphology_controls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/stopword_and_morphology_controls.md) |
| Persistent high ΔS on local path | Need glossary-backed translation bridge | [fallback_translation_and_glossary_bridge.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/fallback_translation_and_glossary_bridge.md) |

---

## Fix in 60 seconds

1) **Detect language**  
   Emit stable language + confidence. If unstable, fix detection first.  
   → [query_language_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_language_detection.md)

2) **Lock normalization and analyzers**  
   Keep locale, width, accents, and segmentation identical on write/read.  
   → [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md) · [query_routing_and_analyzers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_routing_and_analyzers.md)

3) **Protect entities and syntax**  
   Alias fields and romanization pairs; clamp stopwords/morphology for negations and units.  
   → [proper_noun_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md) · [romanization_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md) · [stopword_and_morphology_controls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/stopword_and_morphology_controls.md)

4) **Stabilize ranking**  
   Use multilingual or dual-track rerank with deterministic ordering.  
   → [hybrid_ranking_multilingual.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/hybrid_ranking_multilingual.md)

5) **Translation bridge only if needed**  
   Pair with a glossary and keep native path as default.  
   → [fallback_translation_and_glossary_bridge.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/fallback_translation_and_glossary_bridge.md)

6) **Verify**  
   With bilingual & code-switch sets confirm ΔS ≤ 0.45, Coverage ≥ 0.70, λ convergent.  
   → [code_switching_eval.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/code_switching_eval.md)

---

## Store-agnostic quick recipes

- Normalize the same way for corpus and queries before storing vectors  
- CJK/Thai require segmentation or bigrams; keep entity fields as keyword  
- If no multilingual embeddings, add a lexical sidecar and align features with a deterministic rerank

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

