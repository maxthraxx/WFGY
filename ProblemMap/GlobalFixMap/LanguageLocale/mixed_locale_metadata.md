# Mixed Locale Metadata — Guardrails and Fix Pattern

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


A focused fix when **language, script, or region metadata** is inconsistent across files, snippets, headers, analyzers, or indexes. Use this page to normalize BCP-47 tags, align analyzers and encoders, and lock the schema so retrieval stays stable.

---

## Open these first
- Why this snippet and how it was chosen: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Contract fields you must carry end to end: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Tokenizer picked the wrong rules: [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)  
- Sources mix scripts in one turn: [script_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md)  
- Full and half width digits or punctuation drift: [digits_width_punctuation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/digits_width_punctuation.md)  
- Accents and folding collapse meaning: [diacritics_and_folding.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/diacritics_and_folding.md)  
- Locale choice flips between runs: [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md)  
- CJK segmentation and wordbreak checks: [cjk_segmentation_wordbreak.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/cjk_segmentation_wordbreak.md)  
- RTL and BiDi control safety: [rtl_bidi_control.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/rtl_bidi_control.md)  
- Transliteration pipelines and romanization: [transliteration_and_romanization.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/transliteration_and_romanization.md)

---

## When to use this page
- Corpus claims `lang=en` in headers while HTML meta, PDF tags, or file paths imply non-English.  
- Index analyzer set to `standard` but crawler stamped `lang=zh-Hant` or `lang=ja`.  
- Mixed `lang` values inside one document after conversions or merges.  
- Query comes from a UI locale while the text is in another, leading to wrong analyzer or stopword set.  
- Re-ingest does not update stale `lang/script/region` fields and recall becomes unstable.

---

## Acceptance targets
- **ΔS(question, retrieved) ≤ 0.45** on three paraphrases.  
- **Coverage ≥ 0.70** to the intended section.  
- **λ stays convergent** across two seeds after metadata normalization.  
- **E_resonance flat** on long windows after analyzer alignment.

---

## The core problem
Most stacks carry **only `lang`** and drop **`script`** and **`region`**, or they conflate **UI locale** with **content locale**. Encoders and analyzers then guess. That guess diverges from retrieval, chunking, and ranking, which raises ΔS and flips λ.

---

## 60-second fix
1) **Detect**  
   - Run lightweight LID on both **raw source** and **post-parser text**. Keep the probability.  
   - If `p_top − p_second < 0.20`, mark the snippet **mixed** and route to re-chunk.

2) **Normalize**  
   - Stamp **BCP-47** tags as three fields: `lang`, `script`, `region` where known.  
   - Normalize Unicode to **NFC** for CJK and most Latin, **NFKC** only when you must collapse width.

3) **Align analyzers and encoders**  
   - Choose analyzer by `(lang, script)` rather than UI locale.  
   - Record `analyzer_id`, `encoder_id`, `normal_form` in the snippet.

4) **Verify**  
   - Re-rank with a deterministic reranker.  
   - Recompute ΔS and λ across 3 paraphrases, two seeds. Ship if targets pass.

---

## Minimal contract you must carry
Add these keys to your snippet schema. See the full table in [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

```json
{
  "snippet_id": "doc:123#p4",
  "lang": "zh",
  "script": "Hant",
  "region": "TW",
  "normal_form": "NFC",
  "analyzer_id": "icu_zh_Hant",
  "encoder_id": "e5-multilingual",
  "lid": { "label": "zh-Hant", "p": 0.93, "method": "cld3|fasttext" },
  "source_meta": { "declared_lang": "en-US", "html_meta_lang": "zh-Hant", "pdf_lang": "zh" }
}
````

**Rules**

* Prefer **content-derived** LID over HTTP headers or file paths.
* If `declared_lang` disagrees with LID, trust LID and record the disagreement.
* Never mix snippets with different `(lang, script)` into the same chunk group.

---

## Quick diagnosis → fix

* Answers oscillate per run although facts exist
  → The analyzer follows UI locale. Lock analyzer by snippet fields. See [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

* High similarity yet wrong meaning
  → Encoded with a multilingual model but index analyzer used wrong token rules. Rebuild with aligned analyzer. See [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md).

* Mixed half width, punctuation, or digits break matching
  → Normalize to NFC or NFKC per policy and re-index. See [digits\_width\_punctuation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/digits_width_punctuation.md).

* Script switches mid-paragraph
  → Split at the switch and stamp each part. See [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md).

* CJK recall dips after parser change
  → Check wordbreak rules and ICU configs. See [cjk\_segmentation\_wordbreak.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/cjk_segmentation_wordbreak.md).

---

## Copy-paste prompt for your LLM step

```
I uploaded TXT OS and WFGY Problem Map.

My issue looks like mixed locale metadata:
- declared vs detected lang differ,
- analyzer_id does not match (lang, script),
- ΔS(question, retrieved) = {value}, λ = {state}

Tell me:
1) which layer is failing and why,
2) the exact WFGY page to open,
3) the minimal steps to align BCP-47, analyzer, and encoder,
4) a reproducible test that verifies ΔS ≤ 0.45 and λ convergent.
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
