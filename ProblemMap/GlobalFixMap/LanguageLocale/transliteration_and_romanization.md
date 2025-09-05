# Transliteration & Romanization — Global Fix Map

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


Stabilize queries when users type **Pinyin/Romaji/IAST/RTGS/Buckwalter** variants instead of native scripts.  
Use this page to bridge **native-script ↔ romanized** forms for retrieval, ranking, and reasoning without changing infra.

---

## What this page is
- A compact repair guide for **script-to-roman** mismatches in RAG and search.
- Concrete schema rules and query tactics that unify **multiple romanization systems** per language.
- Exact jump links to structural fixes so you can verify with measurable targets.

## When to use
- Users type **Pinyin with tone marks vs numbers** or ad-hoc English spellings.
- Japanese **Hepburn vs Kunrei** differences (“shi/si”, “tsu/tu”; macron “ō” vs “ou”).
- Korean **Revised RR vs McCune-Reischauer** (“Busan/Pusan”, “Jeju/Cheju”).
- Arabic/Persian **DIN/Buckwalter/ad-hoc** (“Muhammad/Mohamed/Mohammad”).
- Cyrillic names produce **Čajkovskij/Chaikovsky/Tchaikovsky** style drift.
- Greek/Indic/Vietnamese diacritics collapse or fold in unpredictable ways.
- Native pages index fine, yet **romanized queries miss or rank poorly**.

---

## Open these first
- Visual map and recovery: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- End-to-end knobs: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Why this snippet: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Payload schema: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Tokenizer fit: [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)  
- Diacritic folding: [diacritics_and_folding.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/diacritics_and_folding.md)  
- Locale drift: [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md)  
- CJK wordbreaks: [cjk_segmentation_wordbreak.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/cjk_segmentation_wordbreak.md)  
- Mixed scripts in one query: [script_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md)

---

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 on three paraphrases.  
- Coverage of target section ≥ 0.70.  
- λ remains convergent across two seeds.  
- **Cross-script parity**: romanized query recall ≥ 0.90 of native-script recall on your gold set.

---

## Common failure patterns → exact fix

- **Romanization system mismatch** (e.g., Hepburn vs Kunrei, RR vs MR, DIN vs ad-hoc).  
  Lock a canonical key and index both forms.  
  Open: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md), [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **Tone marks vs numbers in Pinyin** (“lǐ/lĭ/li3”).  
  Add a tone-stripped key and a numeric-tone key, dedupe at index time.  
  Open: [diacritics_and_folding.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/diacritics_and_folding.md)

- **Macrons and long vowels in Romaji** (“ō/oo/ou”).  
  Normalize to a canonical long-vowel key and store alternates.  
  Open: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **Arabic definite article or spacing drift** (“al Riyadh/Ar-Riyāḍ/Riyadh”).  
  Strip articles into a side key; keep original for display.  
  Open: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

- **Query parsing split** under hybrid retrievers when romanized variants explode terms.  
  Pin two-stage queries and rerank deterministically.  
  Open: [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md), [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

---

## 60-second fix checklist

1) **Measure ΔS and λ**  
   Compute ΔS(question, retrieved). If ΔS ≥ 0.60 and λ flips on small romanization edits, treat as schema/index mismatch.

2) **Add a Romanization Bridge** (store-agnostic)
- For each document and title, compute and store:
  - `key_native` = original script  
  - `key_roman_primary` = your chosen canonical system per language  
  - `key_roman_alt[]` = enumerated alternates (e.g., Hepburn/Kunrei, RR/MR, DIN/ad-hoc, Pinyin tone/number)  
- Index `key_native` and `key_roman_*` in the same record; **dedupe** by stable `doc_id`.
- At query time, expand to canonical plus alternates, then **rerank**.

3) **Lock the contract**  
   Require fields in the snippet payload:  
   `lang`, `script`, `roman_system`, `key_roman_primary`, `key_roman_alt`, `source_url`, `offsets`.  
   See: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

4) **Probe robustness**  
   Run a three-paraphrase test: native script, canonical romanization, alternate romanization.  
   Targets must meet **Acceptance**.

---

## Minimal per-language mapping hints

- **Chinese**: tone marks ↔ numeric tones; collapse `ü` ↔ `v` in legacy inputs.  
- **Japanese**: macron `ō/ū` ↔ `ou/oo/uu`; “shi/si”, “ji/zi”, “chi/ti”, “tsu/tu”; small “っ/tsu” doubling.  
- **Korean**: RR ↔ MR pairs (“Busan/Pusan”, “Jeju/Cheju”, “Gyeong/ Kyŏng”).  
- **Arabic/Persian**: articles `al-/el-` optional; hamza/ta marbuta variants; DIN ↔ Buckwalter map.  
- **Indic (IAST/ISO/Harvard-Kyoto)**: `ś/ṣ/ñ/ṭ/ḍ` ↔ `sh/sh/ny/t/d`.  
- **Cyrillic**: `Ч/ч` ↔ `Ch/Č`, `Ю/ю` ↔ `Yu/Iu`, etc., preserve soft sign loss with an alternate key.  
- **Greek**: `Μιχάλης` ↔ `Michalis/Michales`; handle `mp/nt` digraphs.

Document your choices inside `roman_system` so audits are reproducible.

---

## Copy-paste prompt (LLM step)

```

You have TXT OS and the WFGY Problem Map loaded.

My multilingual issue:

* symptom: romanized queries miss or rank poorly vs native script
* traces: ΔS(question,retrieved)=..., λ states across native/roman/alternate

Tell me:

1. which layer is failing and why,
2. the exact WFGY page to open,
3. the minimal Romanization Bridge to add (keys + query expansion),
4. how to verify with coverage ≥ 0.70 and ΔS ≤ 0.45 across three paraphrases.
   Reference: retrieval-playbook, retrieval-traceability, data-contracts, diacritics\_and\_folding.

```

---

## Next planned file in `LanguageLocale/`
- **mixed_numeric_systems.md**  ← numbers written in native digits vs ASCII, year/era systems, and counters.

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

