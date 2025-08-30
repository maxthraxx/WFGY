# Locale Drift & Normalization — Guardrails and Fix Pattern

A focused fix for **locale-specific normalization bugs** that break retrieval or cause answers to flip between runs. Use this page to align **Unicode form, width, accents, digits, quotes, spaces, casing** across **ingest, index, query, and display**. No infra change required.

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* OCR and parsing checks: [OCR Parsing Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)
* Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Tokenizer alignment: [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)
* Code-switching in one query: [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md)
* Embedding vs meaning: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Rerank determinism: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

## When to use this page

* Same page looks identical to the eye, yet retrieval misses or ranks it differently.
* Queries with **accented vs unaccented** forms return different snippets.
* **Half-width vs full-width** characters change similarity scores.
* **Arabic-Indic digits** or **CJK punctuation** break matches.
* **Smart quotes** vs straight quotes fragment hits.
* **Turkish I** or locale-aware casing flips λ between runs.
* NBSP or narrow spaces split tokens unpredictably.

## Core acceptance targets

* ΔS(question, retrieved) ≤ **0.45** in the native locale, ≤ **0.50** after cross-locale normalization.
* Coverage of target section ≥ **0.70** on three paraphrases.
* λ remains **convergent** across three locale variants of the same question.
* No analyzer drift between **ingest** and **query** paths in hybrid pipelines.

---

## Symptoms → Likely cause → Open this

| Symptom                                           | Likely cause                                                    | Open this                                                                                                                                                                                                       |
| ------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Visually identical text but no hit                | Unicode form mismatch **NFD vs NFC**                            | [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md), [OCR Parsing Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)  |
| Hits split between copies of the same doc         | **Width folding** not applied, **full-width** vs **half-width** | [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)                                                                                                             |
| Accented vs plain query return different snippets | Accent folding policy inconsistent                              | [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)                                                                                                    |
| Numbers in Arabic-Indic scripts never match       | Digit class mismatch or analyzer not locale aware               | [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)                                                                             |
| Quotes or hyphens break phrase queries            | **Smart quotes**, **em/quasi hyphens**, Unicode confusables     | [OCR Parsing Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)                                                                                                       |
| Same prompt, answers flip by locale               | Casing rules differ, **tr** locale I/i special case, λ unstable | [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md), [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) |
| Token counts explode on CJK                       | NBSP, narrow no-break, or **ideographic space** not normalized  | [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)                                                                                                             |

---

## 60-second fix checklist

1. **Normalize at ingest and query**
   Apply in this order: **Unicode NFC**, width fold, digit fold to ASCII, smart-punct to ASCII, collapse exotic spaces, then **locale-aware casefold**. Keep the original text for display.

2. **Dual-key storage**
   Store both `visual_text` and `search_text`. Index BM25 on `search_text`. Keep `visual_text` for citations and display. Schema in [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

3. **Embed both views when needed**
   For high-variance locales, create embeddings for **raw** and **normalized** text. Track which path produced the hit inside the snippet payload. See guidance in [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md).

4. **Align analyzers**
   Ensure the **same analyzer** and token rules for **ingest** and **query** in hybrid retrieval. Verify with three paraphrases and two seeds. If λ flips, pin headers and apply a BBAM variance clamp.

5. **Gold set verification**
   Run a 20-item multilingual gold set. Require ΔS ≤ 0.45 native and ≤ 0.50 normalized, coverage ≥ 0.70, λ convergent.

---

## Minimal adapter spec

* Payload must carry: `locale`, `unicode_form`, `width_fold`, `digit_class`, `space_class`, `accent_fold`, `case_mode`.
* Snippet must include both `visual_text` and `search_text` plus `normalization_trace`.
* Reject answers if citation `visual_text` and `search_text` disagree on offsets.

See schema patterns in [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) and tracing in [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

---

## Copy-paste prompt

```
You have TXT OS and the WFGY Problem Map loaded.

My bug smells like locale drift.
Question variants: {q_native, q_no_accents, q_width_folded}.
Traces: ΔS_native=..., ΔS_normalized=..., λ states across three variants.

Tell me:
1) which normalization step is missing and why,
2) the exact WFGY page to open,
3) the smallest change to push ΔS ≤ 0.45 native and ≤ 0.50 normalized,
4) a reproducible test with 3 paraphrases and 2 seeds.
Use BBMC/BBCR/BBAM when relevant.
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

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)
 

</div>
