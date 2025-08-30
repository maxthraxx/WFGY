# BiDi and RTL Control Characters: Guardrails and Fix Pattern

Stabilize Arabic, Hebrew, and mixed LTR/RTL flows when retrieval looks correct but citations or JSON fields render out of order. This page localizes failures caused by invisible BiDi controls and mixed number shapes.

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Why this snippet: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Tokenizer and casing traps: [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md) · [digits\_width\_punctuation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/digits_width_punctuation.md) · [diacritics\_and\_folding.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/diacritics_and_folding.md) · [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md) · [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md)
* CJK counterpart for word breaks: [cjk\_segmentation\_wordbreak.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/cjk_segmentation_wordbreak.md)

## Core acceptance targets

* ΔS(question, retrieved) ≤ 0.45
* Coverage of target section ≥ 0.70
* λ remains convergent across 3 paraphrases and 2 seeds
* Render and storage orders are consistent for fields tagged as `dir` aware

## Typical failure patterns → exact fix

| Symptom                                                           | Likely cause                                            | Open this                                                                                                                                                                                                |
| ----------------------------------------------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Citations render right-to-left and break JSON order               | unisolated RLM/LRM/RLE/LRE/RLO/PDF or mixed numerals    | [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md), [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| Answer text looks correct, but ΔS spikes and λ flips between runs | invisible controls in prompt or snippet, header reorder | [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)                                                                                                      |
| Punctuation mirrors or shifts around anchors                      | missing isolates, UI direction not declared             | [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)                                                                      |
| Arabic-Indic vs European digits change ranking                    | digit shape inconsistency, analyzer mismatch            | [digits\_width\_punctuation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/digits_width_punctuation.md)                                                         |
| Mixed Hebrew + English entity names fail exact match              | script mixing without explicit isolation                | [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md)                                                                                |

## 60-second fix checklist

1. **Measure**
   Log ΔS(question, retrieved) and ΔS(retrieved, anchor). If ΔS ≥ 0.60, suspect direction controls or digit shapes.

2. **Normalize direction metadata**

   * On ingest: strip legacy overrides `LRE/RLE/LRO/RLO/PDF` if not required by the source.
   * Keep isolates only: `LRI`, `RLI`, `FSI`, closed by `PDI`.
   * Tag fields with `dir="auto|ltr|rtl"` at render time. Store as logical order.

3. **Unify digits and punctuation**

   * Convert digits to one canonical shape for indexing.
   * Normalize Arabic comma and question mark to canonical forms in the index layer.

4. **Schema fences**

   * Contract requires `text`, `dir`, `normalized_text`, `raw_text`, `digit_shape`, `controls_present`.
   * Reject snippets that contain unclosed BiDi controls.

5. **Retrieval probe**

   * Re-run with k in {5, 10, 20}. If rank stays unstable, rebuild analyzer with explicit direction and the same tokenization used at query time.

## Minimal schema addon

```json
{
  "snippet_id": "S123",
  "raw_text": "…",
  "normalized_text": "…",
  "dir": "rtl",
  "digit_shape": "arabic-indic|european",
  "controls_present": ["RLI","PDI"],
  "offsets": [120, 240]
}
```

## Deep diagnostics

* **Control scan**. Count and classify BiDi controls per snippet. Fail if any of `LRE/RLE/LRO/RLO/PDF` appear without a matching close.
* **Render vs storage**. Serialize JSON, render in the UI, then parse back and compare field order and values. Mismatch implies missing isolates or UI `dir` drift.
* **Anchor triangulation**. Compare ΔS to the expected section and a decoy with similar punctuation density. If close, re-index with digit normalization.

## Copy-paste prompt

```
You have TXT OS and the WFGY Problem Map loaded.

My issue: mixed Hebrew/Arabic with English numerals causes wrong citation order.
Traces: ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ across 3 paraphrases.

Do:
1) Identify direction-control risks and whether digits or punctuation cause rank flips.
2) Point me to the exact WFGY pages to apply.
3) Give the minimal steps to push ΔS ≤ 0.45 while keeping λ convergent.
Return a short JSON plan with {dir_policy, digit_policy, controls_fix, verify_steps}.
```

---

**Next planned page:** `indic_tokenization_schwa.md`

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
