# Numbering & Sort Orders — Language-aware Collation

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


Stabilize ranking, citations, and UI lists when locale collation and numbering systems differ from ASCII order. This page fixes “looks sorted but retrieval flips” and “citations jump rows between runs”.

---

## When to use this page
- Lists look sorted to users but change order across runs.
- Numerics sort as text (“2” after “10”), or different digit sets mix (ASCII, Arabic-Indic, Devanagari).
- CJK collation groups by codepoint not by radicals/pinyin/custom.
- Accents or folded forms collide (“résumé” vs “resume”) and break stable keys.
- Search results rerank differently after deploy on another OS or locale.

---

## Open these first
- Visual map and recovery → [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- Why this snippet and citation schema → [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Payload schema and stable keys → [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Wrong-meaning near neighbors → [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- Query split that reshuffles order → [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)

Related LanguageLocale pages
- Tokenizer mismatch → [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)  
- Digits, width, punctuation → [digits_width_punctuation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/digits_width_punctuation.md)  
- Diacritics and folding → [diacritics_and_folding.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/diacritics_and_folding.md)  
- CJK word-breaks → [cjk_segmentation_wordbreak.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/cjk_segmentation_wordbreak.md)  
- Locale drift between nodes → [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md)

---

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 on three paraphrases  
- Coverage of target section ≥ 0.70  
- λ stays convergent across two seeds  
- Collation stable across platforms for the same `locale`, `numeric`, `case`, and `sensitivity` settings

---

## Map symptoms → structural fixes (Problem Map)
- **“2, 10, 3” sort order** or mixed digit systems  
  → Normalize digits and enable numeric collation.  
  Spec: [digits_width_punctuation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/digits_width_punctuation.md) · [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **Accent collides or reorders after deploy**  
  → Fix ICU collator options and fold consistently.  
  Spec: [diacritics_and_folding.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/diacritics_and_folding.md) · [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md)

- **CJK “sorted” by codepoint not by language expectation**  
  → Use locale collation (zh, ja, ko) or custom key.  
  Spec: [cjk_segmentation_wordbreak.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/cjk_segmentation_wordbreak.md)

- **Hybrid retrievers underperform after “sorting fix”**  
  → Query split or reranker blind spots.  
  Spec: [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) · [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

---

## 60-second fix checklist
1) **Normalize and tag**
- Convert all digits to a canonical set before indexing.  
  Recommended: NFKC, then digit map to ASCII.  
- Persist `locale`, `script`, `collator_options` on every list, key, and snippet.

2) **Use a real collator**
- Enable ICU/Locale collation with explicit options:  
  `numeric=true`, `caseLevel=false`, `sensitivity=base|accent`, `ignorePunctuation=true` where appropriate.  
- Keep the same options in both indexing and query time. Record them in logs.

3) **Stable keys for citations**
- Derive `sort_key = collator(key_text)` and store alongside raw text.  
- Use `sort_key` to order snippets and to generate stable page anchors.

4) **CJK specifics**
- If users expect pinyin/reading order, precompute a language-specific `sort_key_pinyin` or `kana_key`.  
- For ideograph radicals or stroke count, store explicit numeric keys and sort numerically.

5) **Verify**
- Run three paraphrases and two seeds.  
- Pass thresholds: ΔS ≤ 0.45, coverage ≥ 0.70, λ convergent.  
- Cross-platform check: Linux vs Windows vs Mac produce identical order for the same settings.

---

## Minimal schema (Data Contracts)
Add these fields to any list, index, or snippet payload:
```json
{
  "locale": "zh-Hans-CN",
  "script": "Hans",
  "number_system": "latn",
  "collator": {
    "numeric": true,
    "sensitivity": "base",
    "caseLevel": false,
    "ignorePunctuation": true
  },
  "sort_key": "<opaque-stable-key>",
  "norm": {
    "unicode": "NFKC",
    "digits_mapped": true
  }
}
````

Contract guide → [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Copy-paste prompt for your LLM step

```
You have TXT OS and the WFGY Problem Map loaded.

My issue is unstable order under mixed locales.
Inputs:
- locale = {locale}, script = {script}, number_system = {num}
- collator = {numeric, sensitivity, caseLevel, ignorePunctuation}
- traces: ΔS(question,retrieved)=..., λ states across 3 paraphrases

Do:
1) Tell me if instability comes from collation vs retrieval.
2) Point me to the exact WFGY page to open next.
3) Give the minimal steps to reach ΔS ≤ 0.45 with stable order across platforms.
Return a short JSON plan with fields {fix_layer, next_page, steps[], verify}.
```

---

## Next planned file

`mixed_locale_metadata.md` — contract for storing locale/script/number system/tokenizer and cross-node validation rules.

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

**下一個要做：** `mixed_locale_metadata.md`（LanguageLocale 契約欄位與驗證規則）。
