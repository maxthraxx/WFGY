# Locale Collation & Sorting — Consistency Guardrails and Fix Pattern

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


A focused guide to stop locale-specific sort/collation bugs that break retrieval order, deduping, join keys, and user-facing lists. Use this when lists look “random,” numbers sort as text (“v10” before “v2”), or non-English letters jump around across environments.

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Traceability and snippet schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Ordering control at re-rank stage: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
* Wrong-meaning hits despite high similarity: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Hybrid query instability: [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)

## Core acceptance targets

* **Deterministic sort** across OS/runtime/DB: the same input yields identical order on two hosts.
* **Numeric natural order** for mixed strings (“v2” < “v10”, “Chap 9” < “Chap 12”).
* **Locale-consistent letter order** under the chosen policy (e.g., tr-TR “I/ı/İ/i”, sv-SE “Å/Ä/Ö”, da-DK “Æ/Ø/Å”, es-ES “ñ”, de-DE “ä/ö/ü/ß”, ja-JP kana).
* **Retrieval stability**: top-k set and order do not change when locale/collation varies; ΔS(question, retrieved) ≤ 0.45 on three paraphrases.

---

## Fast triage — what’s breaking?

| Symptom                                              | Likely cause                         | What to check                                                                |
| ---------------------------------------------------- | ------------------------------------ | ---------------------------------------------------------------------------- |
| “v10” sorted before “v2”                             | Lexicographic sort on strings        | Enable **natural sort** with numeric keys or precomputed tokens.             |
| Turkish “I/ı/İ/i” mis-ordered or casefold joins fail | Wrong casefold/collation (not tr-TR) | Ensure **locale-aware casefold** and ICU tr-TR collation.                    |
| Swedish “ÅÄÖ” placed near A/O                        | Default UCA/English collation        | Use **sv-SE** collation; verify ICU rules.                                   |
| German “ß” vs “ss” dedupe misses                     | Collation strength mismatch          | Set **strength=secondary/tertiary** consistently; precompute collation keys. |
| Japanese kana mixed order, halfwidth/fullwidth split | Width/diacritic handling off         | Normalize to **NFC**, enable **ja collation with kana handling**.            |
| CJK sort flips between Pinyin vs stroke              | Different collation per host         | Pin **zh-u-co-pinyin** (or stroke) everywhere; store the policy centrally.   |
| RAG top-k changes across deploys                     | Store/retriever disagree on locale   | Lock analyzer + collation; move ordering to **reranker** layer.              |

---

## Fix in 60 seconds

1. **Pick one policy** and write it down
   Choose the **business collation** per language. Examples you can adopt as BCP-47/ICU tags:

   * Turkish: `tr` (case and dotted I rules)
   * Swedish: `sv` (Å/Ä/Ö order)
   * Danish: `da` (Æ/Ø/Å order)
   * Spanish: `es` (ñ, modern UCA rules)
   * German: `de` (ä/ö/ü/ß handling)
   * Japanese: `ja` with kana sensitivity
   * Chinese: `zh-u-co-pinyin` or `zh-u-co-stroke` (pick one and stick with it)

2. **Normalize before you sort**

   * Apply **Unicode NFC** for storage and indexing.
   * Apply **locale-aware casefold** where required (not global lowercasing for tr-TR).

3. **Persist a collation key**

   * Generate an ICU **sort key** per string at write time and sort by that key.
   * Keep the display text separate to avoid re-computing under mixed hosts.

4. **Enable natural sort for mixed numbers**

   * Extract number runs and sort by `(text_prefix, numeric_value, text_suffix)` or pre-tokenize with **zero-padded numeric keys**.

5. **Move “human order” to the right layer**

   * Retrieval index should stay analyzer-consistent; perform user-facing sort with the pinned collation or with a **reranker** when semantics must decide order.

Verify with: three paraphrases, two seeds, ΔS ≤ 0.45, top-k order unchanged. See [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) and [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).

---

## Engineering checklist (copy-paste)

* **Policy**: Document target collation per language (`sv-SE`, `tr-TR`, `zh-u-co-pinyin`, …) and the **ICU options**: normalization=on, strength=secondary/tertiary, caseLevel as needed.
* **Ingest**: Normalize to NFC, record a **collation\_key** column, and a **natural\_key** for number-aware ordering.
* **APIs**: Expose `sort_by=collation_key|natural_key` flags; default to the business policy.
* **DB**: Use ICU collations consistently across read/write paths; avoid OS-default discrepancies.
* **Search/RAG**: Keep tokenizer/casing consistent with store; if locale differs, **rerank** to enforce the final order.
* **Tests**: Gold lists for `tr I/ı/İ/i`, `sv Å/Ä/Ö`, `da Æ/Ø/Å`, `de ß/ss`, kana order, CJK Pinyin vs stroke; include mixed “v2/v10” and wide/narrow digits.

---

## Deeper diagnostics

* **Strength probe**: Re-sort once at **primary** strength (base letters), once at **tertiary** (case/diacritics). If order flips, lock the strength in config and rebuild keys.
* **Width probe**: Convert to halfwidth/fullwidth and verify order invariance; if not invariant, enable **width-insensitive** collation or normalize earlier.
* **CJK policy probe**: Compare `zh-u-co-pinyin` vs stroke; choose one and rebuild collation keys cluster-wide.
* **RAG stability probe**: If top-k changes when locale toggles, push final ordering to reranker and validate with [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

---

## When to escalate

* Order still unstable after policy pinning → treat as schema drift and lock payloads with [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).
* Wrong items despite perfect sorting → it’s not collation, it’s meaning. See [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) and re-index via the [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).
* Hybrid retrieval becomes worse than single → see [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) and pin deterministic weights.

---

## Copy-paste prompt for the AI

```
You have TXTOS and the WFGY Problem Map loaded.

My locale sorting issue:
- language(s): [...]
- observed order vs expected: [...]
- store/runtime: [DB/search/lib], ICU settings?, strength?, normalization?
- symptoms: top-k flip? numeric misorder? CJK strategy drift?

Tell me:
1) which layer is failing (normalization, collation, numeric natural sort, rerank),
2) the exact WFGY pages to open,
3) the minimal steps to pin the policy and rebuild keys,
4) a repeatable test to verify stability across 2 hosts and 2 seeds.
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

