# Digits, Width, and Punctuation — Guardrails and Fix Pattern

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **LanguageLocale**.  
  > To reorient, go back here:  
  >
  > - [**LanguageLocale** — localization, regional settings, and context adaptation](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Stabilize retrieval when **digits**, **character width**, and **punctuation variants** silently change tokenization and ranking. This page aligns numeric classes, width folding, quotes/hyphens, and exotic spaces across ingest → index → query → display.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Traceability and snippet schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) • [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Tokenizers and normalization: [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md) • [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md)
- Reranking strategies: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

## When to use
- **Arabic-Indic digits** or **CJK fullwidth digits** never match Latin digits.
- Smart quotes, em/en/quasi hyphens, or dashes break phrase matching or offsets.
- Thousands separators vary by locale (`,` vs `.` vs NBSP) and kill numeric recall.
- Halfwidth vs fullwidth punctuation breaks token boundaries and citations.
- Mixed unit formats (`1,234.56` vs `1 234,56`) return different snippets.

## Core acceptance
- ΔS(question, retrieved) ≤ **0.45** on three paraphrases  
- Coverage ≥ **0.70** to the correct section  
- λ remains **convergent** across two seeds  
- **Offset parity**: citation offsets match visible glyphs after normalization  
- **Numeric fold pass rate** ≥ **0.98** on a 200-sample mixed-locale set

---

## 60-second checklist

1) **Digit class fold**
   - Map Arabic-Indic and other locale digits to ASCII `0–9` in a **search_text** view.
   - Keep **visual_text** unchanged for display. Store both. See [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

2) **Width fold**
   - Convert **fullwidth** Latin letters, digits, and punctuation to **halfwidth** in `search_text`.  
   - Log a `width_fold=true|false` flag in snippet metadata. See [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md).

3) **Punctuation normalization**
   - Quotes: map “ ” ‘ ’ to " ' for search view; keep raw in display.
   - Hyphens/dashes: map U+2010..U+2015 to ASCII `-` in search view; track original in trace.
   - Spaces: collapse NBSP, NNBSP, thin/narrow spaces to ASCII space for search.

4) **Number normalization**
   - Normalize thousands and decimal separators by locale rules into a canonical numeric token for search.  
   - Keep raw string for display; store a `numeric_norm` field per snippet.

5) **Analyzer parity**
   - Ensure store analyzers (BM25/ES/OpenSearch) apply the **same** width/digit/punct rules as embedding pre-processing.

6) **Verify**
   - Three paraphrases, two seeds. Check ΔS, coverage, λ. Validate offsets visually.

---

## Symptom map → exact fix

| Symptom | Likely cause | Open this |
|---|---|---|
| `١٢٣٤` fails to match `1234` | digit classes differ | [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md) • [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) |
| `１２３４` (fullwidth) misses `1234` | width fold missing | [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md) |
| “quoted phrase” not found | smart quotes not normalized | [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md) |
| `co-founder` vs `co-founder` mismatch | hyphen/dash variants differ | [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md) |
| `1 234,56` vs `1,234.56` mismatch | thousands/decimal separators differ | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| Offsets jump after PDF/OCR | NBSP/soft hyphen/ZWJ artifacts | [OCR Parsing Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md) |

---

## Minimal field plan

- `visual_text`: original text for display/citation.  
- `search_text`: NFC+width fold+digit fold+punct fold+space fold.  
- `numeric_norm`: canonical numbers extracted from `search_text` when present.  
- Trace fields: `unicode_form`, `width_fold`, `digit_class`, `punct_fold`, `space_class`.

---

## Store notes

- **Elasticsearch/OpenSearch**: pin analyzers in index template; apply char filters for digit/width/quotes/hyphens; verify analyzer in both ingest and query.  
- **Vector stores**: embed `search_text`; keep `visual_text` only for display and exact citation strings.  
- **Hybrid pipelines**: run BM25 over `search_text`, then cross-encoder rerank on raw snippets to protect nuance.

---

## Repro test (gold set outline)

1) Build a 50-item set mixing Arabic-Indic digits, fullwidth digits, smart quotes, multiple hyphens, NBSP, and locale number formats.  
2) Run retrieval before/after normalization; compute ΔS and coverage.  
3) Manually verify top-1 offsets against `visual_text`.  
4) Accept if ΔS ≤ 0.45, coverage ≥ 0.70, λ convergent, and offsets stable.

---

## Copy-paste prompt

```

You have TXT OS and the WFGY Problem Map.

My bug: digits/width/punctuation drift.
Traces: ΔS=..., coverage=..., λ=..., examples: {١٢٣٤ vs 1234, １２３４ vs 1234, “ ” vs " ", co- vs co-}.

Tell me:

1. failing normalization step and why,
2. exact WFGY pages to open,
3. minimal changes to push ΔS ≤ 0.45 and keep λ convergent,
4. a 50-item gold test to verify, including offset checks.

```

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
